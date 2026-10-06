#!/usr/bin/env python3
"""
Auditoría estática del sitio. No toca nada: solo informa.

Comprueba, para cada página HTML:
  - enlaces internos (href/src) que apuntan a archivos inexistentes
  - imágenes sin alt o con alt vacío
  - <title> y meta description: ausentes, duplicados o fuera de longitud
  - un único <h1>
  - JSON-LD que no parsea como JSON
  - URLs del sitemap que no existen y páginas indexables que faltan en el sitemap
  - peso del HTML
  - imágenes del directorio img/ sin referencias (huérfanas) y su peso

Uso: python3 scripts/audit_site.py
"""
import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SKIP = {"googleaa8b9c4981793855.html"}
NOINDEX = {"panel-ideas-privado.html", "404.html"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.h1 = [], [], 0
        self.ld, self._ld, self.title, self._t = [], False, "", False
        self.desc = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img", "source") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._t = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        if tag == "script":
            self._ld = False

    def handle_data(self, d):
        if self._t:
            self.title += d
        if self._ld:
            self.ld[-1] += d


def target_exists(href: str) -> bool:
    if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
        return True
    u = urlparse(href)
    if u.scheme in ("http", "https"):
        if not href.startswith(BASE):
            return True  # externo: no se comprueba
        path = u.path
    else:
        path = u.path
    path = path.lstrip("/")
    if path == "":
        return True
    return (ROOT / path).exists()


def main() -> int:
    issues = defaultdict(list)
    titles, descs = defaultdict(list), defaultdict(list)
    referenced = set()
    pages = sorted(p for p in ROOT.glob("*.html") if p.name not in SKIP)

    for p in pages:
        text = p.read_text(encoding="utf-8")
        pg = Page()
        pg.feed(text)
        for h in pg.links:
            u = urlparse(h)
            clean = u.path.lstrip("/")
            referenced.add(clean)
            if not target_exists(h):
                issues["Enlace/recurso interno roto"].append(f"{p.name} -> {h}")
        for im in pg.imgs:
            if not im.get("alt", "").strip():
                issues["Imagen sin alt"].append(f"{p.name} -> {im.get('src')}")
        t, d = pg.title.strip(), (pg.desc or "").strip()
        titles[t].append(p.name)
        descs[d].append(p.name)
        if p.name not in NOINDEX:
            if not t:
                issues["Sin <title>"].append(p.name)
            elif len(t) > 65:
                issues["Title largo (>65)"].append(f"{p.name} ({len(t)})")
            if not d:
                issues["Sin meta description"].append(p.name)
            elif len(d) > 165:
                issues["Description larga (>165)"].append(f"{p.name} ({len(d)})")
            elif len(d) < 70:
                issues["Description corta (<70)"].append(f"{p.name} ({len(d)})")
            if pg.h1 != 1:
                issues["H1 distinto de 1"].append(f"{p.name} ({pg.h1})")
        for blob in pg.ld:
            try:
                json.loads(blob)
            except Exception as e:
                issues["JSON-LD inválido"].append(f"{p.name}: {e}")
        kb = len(text.encode()) / 1024
        if kb > 150:
            issues["HTML pesado (>150 KB)"].append(f"{p.name} ({kb:.0f} KB)")

    for t, names in titles.items():
        if t and len(names) > 1:
            issues["Title duplicado"].append(f"{t!r}: {', '.join(names)}")
    for d, names in descs.items():
        if d and len(names) > 1:
            issues["Description duplicada"].append(f"{', '.join(names)}")

    # sitemap
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    in_sm = {urlparse(l).path.lstrip("/") for l in locs}
    for l in locs:
        if not (ROOT / urlparse(l).path.lstrip("/")).exists():
            issues["URL del sitemap inexistente"].append(l)
    for p in pages:
        if p.name not in NOINDEX and p.name not in in_sm:
            issues["Página indexable fuera del sitemap"].append(p.name)

    # imágenes huérfanas / pesadas
    img_dir = ROOT / "img"
    css_js = "".join(f.read_text(encoding="utf-8", errors="ignore")
                     for f in list(ROOT.glob("css/*")) + list(ROOT.glob("js/*")))
    html_all = "".join(p.read_text(encoding="utf-8") for p in pages)
    for f in sorted(img_dir.glob("*")):
        rel = f"img/{f.name}"
        if f.name not in html_all and f.name not in css_js:
            issues["Imagen huérfana"].append(f"{rel} ({f.stat().st_size/1024:.0f} KB)")
        if f.stat().st_size > 200 * 1024:
            issues["Imagen pesada (>200 KB)"].append(f"{rel} ({f.stat().st_size/1024:.0f} KB)")

    total = sum(len(v) for v in issues.values())
    print(f"Páginas auditadas: {len(pages)}  |  Hallazgos: {total}\n")
    for k in sorted(issues):
        print(f"## {k} ({len(issues[k])})")
        for line in issues[k][:25]:
            print("  -", line)
        if len(issues[k]) > 25:
            print(f"  ... y {len(issues[k]) - 25} más")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
