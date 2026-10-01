#!/usr/bin/env python3
"""
Sustituye la ilustración SVG de un reloj por su foto real en TODAS las
páginas del sitio donde aparezca (ficha propia, index, categorías,
"también te puede interesar" en otras fichas), y actualiza también las
referencias de datos (JSON-LD "image" y el "image_url" embebido en los
scripts de comparador/herramienta/colección).

Uso: python3 scripts/wire_real_photos.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# aria_label -> (slug del archivo de imagen real, alt text corto)
WATCHES = {
    "Citizen Tsuyosa Automático NJ0151-53M": ("citizen-tsuyosa-real.jpg", "Citizen Tsuyosa"),
    "Citizen Promaster Eco-Drive Diver BN0151-09L": ("citizen-promaster-eco-drive-diver-real.jpg", "Citizen Promaster Eco-Drive Diver"),
    "Hamilton Khaki Field Mechanical H69439931": ("hamilton-khaki-field-mechanical-real.jpg", "Hamilton Khaki Field Mechanical"),
    "Orient Bambino Versión 5 RA-AC0001S10A": ("orient-bambino-v5-real.jpg", "Orient Bambino Versión 5"),
    "Seiko Presage Cocktail Time SRPB41": ("seiko-presage-srpb41-real.jpg", "Seiko Presage Cocktail Time"),
    "Baltic Aquascaphe MK2": ("baltic-aquascaphe-mk2-real.png", "Baltic Aquascaphe MK2"),
    "Seiko 5 Sports Automático (SRPD)": ("seiko-5-sports-real.png", "Seiko 5 Sports"),
    "Seiko Prospex Alpinist SPB210": ("seiko-alpinist-spb210-real.png", "Seiko Prospex Alpinist"),
}

# slug del png antiguo (mal etiquetado) -> slug del jpg real nuevo, para
# las referencias de datos (JSON-LD "image", "image_url" en los scripts)
OLD_PNG = {
    "citizen-tsuyosa.png": "citizen-tsuyosa-real.jpg",
    "citizen-promaster-eco-drive-diver.png": "citizen-promaster-eco-drive-diver-real.jpg",
    "hamilton-khaki-field-mechanical.png": "hamilton-khaki-field-mechanical-real.jpg",
    "orient-bambino-v5.png": "orient-bambino-v5-real.jpg",
    "seiko-presage-srpb41.png": "seiko-presage-srpb41-real.jpg",
    "baltic-aquascaphe-mk2.png": "baltic-aquascaphe-mk2-real.png",
    "seiko-5-sports.png": "seiko-5-sports-real.png",
    "seiko-alpinist-spb210.png": "seiko-alpinist-spb210-real.png",
}

WATCHFACE_RE_TMPL = (
    r'(<div class="watchface"[^>]*role="img" aria-label="{label}">)'
    r'<svg.*?</svg>'
    r'(</div>)'
)


def replace_watchfaces(text: str) -> tuple[str, int]:
    total = 0
    for label, (img_slug, alt) in WATCHES.items():
        pattern = WATCHFACE_RE_TMPL.format(label=re.escape(label))
        img_tag = (
            f'<img src="/img/{img_slug}?v=2" alt="{alt}" '
            'style="width:100%;height:100%;object-fit:cover;border-radius:8px;">'
        )
        new_text, n = re.subn(
            pattern, r"\1" + img_tag.replace("\\", "\\\\") + r"\2", text, flags=re.DOTALL
        )
        text = new_text
        total += n
    return text, total


def replace_data_refs(text: str) -> tuple[str, int]:
    total = 0
    for old_png, new_jpg in OLD_PNG.items():
        new_text, n = re.subn(re.escape(old_png), new_jpg, text)
        text = new_text
        total += n
    return text, total


def main() -> None:
    html_files = sorted(ROOT.glob("*.html"))
    watchface_total = 0
    dataref_total = 0
    touched = []

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        new_text, n1 = replace_watchfaces(text)
        new_text, n2 = replace_data_refs(new_text)
        if n1 or n2:
            path.write_text(new_text, encoding="utf-8")
            touched.append((path.name, n1, n2))
            watchface_total += n1
            dataref_total += n2

    print(f"Watchfaces SVG -> foto real: {watchface_total} sustituciones")
    print(f"Referencias de datos (image/image_url): {dataref_total} sustituciones")
    print()
    for name, n1, n2 in touched:
        print(f"  {name}: {n1} watchface(s), {n2} referencia(s) de datos")


if __name__ == "__main__":
    main()
