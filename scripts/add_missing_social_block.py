#!/usr/bin/env python3
"""
Añade el bloque Open Graph / Twitter Card completo (no solo la imagen)
a las páginas que nunca lo tuvieron: categoria-microbrands.html,
guia-tipos-de-movimiento.html, novedades.html.

Usa <title> + <meta name="description"> + canonical como fuente de
og:title / og:description / og:url, y el banner genérico como imagen.

Uso: python3 scripts/add_missing_social_block.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://calibre-correa.adelardo.workers.dev"
BANNER = (f"{BASE_URL}/img/social-banner.png?v=2", 1500, 500)

PAGES = [
    "categoria-microbrands.html",
    "guia-tipos-de-movimiento.html",
    "novedades.html",
]

TITLE_RE = re.compile(r"<title>([^<]*)</title>")
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)">')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)">\n')
ROBOTS_RE = re.compile(r'(<meta name="robots"[^>]*>\n)')


def main() -> None:
    for name in PAGES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")

        title = TITLE_RE.search(text).group(1)
        desc = DESC_RE.search(text).group(1)
        canonical_m = CANONICAL_RE.search(text)
        url = canonical_m.group(1)
        img_url, w, h = BANNER

        block = (
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:site_name" content="Calibre & Correa">\n'
            f'<meta property="og:image" content="{img_url}">\n'
            f'<meta property="og:image:width" content="{w}">\n'
            f'<meta property="og:image:height" content="{h}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n'
            f'<meta name="twitter:description" content="{desc}">\n'
            f'<meta name="twitter:image" content="{img_url}">\n'
        )

        new_text, n = ROBOTS_RE.subn(r"\1" + block.replace("\\", "\\\\"), text, count=1)
        if n != 1:
            print(f"✗ {name}: no se encontró <meta name=\"robots\"> para insertar después")
            continue

        path.write_text(new_text, encoding="utf-8")
        print(f"✓ {name}: bloque social añadido")


if __name__ == "__main__":
    main()
