#!/usr/bin/env python3
"""
Valida que cada página HTML del sitio corresponde a sí misma:
- El <link rel="canonical"> apunta al propio nombre de archivo.
- El <title> y el <h1> (si existen) son consistentes entre sí dentro
  de la misma página.
- robots.txt y sitemap.xml no son en realidad páginas HTML coladas
  por error (el bug que causó el incidente del 29/09/2026).

Se ejecuta antes de cada despliegue (a mano, o vía GitHub Actions en
.github/workflows/validate.yml). Sale con código != 0 si encuentra
algún problema, para que el CI falle de forma visible en vez de dejar
pasar un sitio con páginas cruzadas.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_RE = re.compile(r'rel="canonical"\s+href="https://[^/]+/([^"]+)"')
TITLE_RE = re.compile(r"<title>([^<]*)</title>")
H1_RE = re.compile(r"<h1[^>]*>([^<]+)")

# Palabras que, si aparecen en el <title>, casi seguro indican que el
# archivo lleva el contenido de otra página (nombre de otro reloj,
# de otra categoría, etc. en vez del propio).
SKIP_CANONICAL_CHECK = {
    "404.html",
    "panel-ideas-privado.html",  # noindex, no necesita canonical
}
# Archivos que no son páginas del sitio (verificación de Google, etc.)
SKIP_FILES = {"googleaa8b9c4981793855.html"}


def check_html_file(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8", errors="replace")

    # 1) El archivo no debe ser en realidad un robots.txt/sitemap.xml
    if text.lstrip().startswith("User-agent:") or text.lstrip().startswith(
        "<?xml"
    ):
        problems.append(
            f"{path.name}: contiene un robots.txt/sitemap.xml en vez de HTML"
        )
        return problems

    # 2) canonical debe terminar en el propio nombre de archivo
    if path.name not in SKIP_CANONICAL_CHECK:
        m = CANONICAL_RE.search(text)
        if not m:
            problems.append(f"{path.name}: no tiene <link rel=\"canonical\">")
        elif m.group(1) != path.name:
            problems.append(
                f"{path.name}: canonical apunta a '{m.group(1)}' en vez de a sí mismo"
            )

    # 3) title y h1 no deben estar vacíos ni contradecirse entre sí
    #    de forma evidente (comprobación best-effort, no exhaustiva).
    title_m = TITLE_RE.search(text)
    h1_m = H1_RE.search(text)
    if title_m and h1_m:
        title = title_m.group(1).strip()
        h1 = h1_m.group(1).strip()
        # Si ninguna palabra "significativa" del h1 aparece en el title,
        # probablemente son de páginas distintas.
        h1_words = {w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", h1)}
        title_lower = title.lower()
        if h1_words and not any(w in title_lower for w in h1_words):
            problems.append(
                f"{path.name}: el <title> ('{title}') y el <h1> ('{h1}') "
                "no comparten ninguna palabra — posible contenido cruzado"
            )

    return problems


def check_text_file(path: Path, expected_start: str, label: str) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace").lstrip()
    if not text.startswith(expected_start):
        return [
            f"{path.name}: no empieza como un {label} válido "
            f"(esperaba que empezara con '{expected_start}')"
        ]
    return []


def main() -> int:
    problems: list[str] = []

    for html_file in sorted(ROOT.glob("*.html")):
        if html_file.name in SKIP_FILES:
            continue
        problems.extend(check_html_file(html_file))

    robots = ROOT / "robots.txt"
    if robots.exists():
        problems.extend(check_text_file(robots, "User-agent:", "robots.txt"))

    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        problems.extend(check_text_file(sitemap, "<?xml", "sitemap.xml"))

    if problems:
        print(f"✗ {len(problems)} problema(s) encontrados:\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    html_count = len(list(ROOT.glob("*.html")))
    print(f"✓ {html_count} páginas HTML + robots.txt + sitemap.xml OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
