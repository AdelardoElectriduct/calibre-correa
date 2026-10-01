#!/usr/bin/env python3
"""
Añade meta tags og:image / twitter:image (+ dimensiones) a todas las
páginas del sitio. Las fichas de reloj (reloj-*.html) usan su propia
foto real; el resto de páginas usan el banner genérico de fallback
(img/social-banner.png).

También sube twitter:card de "summary" a "summary_large_image" para
que la imagen se muestre en grande en Twitter/X.

Uso: python3 scripts/add_social_images.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://calibre-correa.adelardo.workers.dev"

# slug de la página de reloj -> (archivo de imagen, ancho, alto)
WATCH_IMAGES = {
    "reloj-citizen-tsuyosa.html": ("citizen-tsuyosa-real.jpg", 227, 395),
    "reloj-citizen-promaster-eco-drive-diver.html": ("citizen-promaster-eco-drive-diver-real.jpg", 299, 500),
    "reloj-hamilton-khaki-field-mechanical.html": ("hamilton-khaki-field-mechanical-real.jpg", 345, 675),
    "reloj-orient-bambino-v5.html": ("orient-bambino-v5-real.jpg", 195, 320),
    "reloj-seiko-presage-srpb41.html": ("seiko-presage-srpb41-real.jpg", 350, 625),
    "reloj-baltic-aquascaphe-mk2.html": ("baltic-aquascaphe-mk2-real.png", 260, 360),
    "reloj-seiko-5-sports.html": ("seiko-5-sports-real.png", 436, 436),
    "reloj-seiko-alpinist-spb210.html": ("seiko-alpinist-spb210-real.png", 347, 467),
    "reloj-tissot-prx-quartz.html": ("tissot-prx-quartz-real.jpg", 306, 500),
}

FALLBACK_IMAGE = ("social-banner.png", 1500, 500)

OG_SITE_NAME_RE = re.compile(r'(<meta property="og:site_name"[^>]*>\n)')
TWITTER_DESC_RE = re.compile(r'(<meta name="twitter:description"[^>]*>\n)')
TWITTER_CARD_RE = re.compile(r'<meta name="twitter:card" content="summary">')


def add_tags(text: str, img_slug: str, width: int, height: int) -> tuple[str, int]:
    changes = 0
    img_url = f"{BASE_URL}/img/{img_slug}?v=2"

    if "og:image" not in text:
        og_tags = (
            f'<meta property="og:image" content="{img_url}">\n'
            f'<meta property="og:image:width" content="{width}">\n'
            f'<meta property="og:image:height" content="{height}">\n'
        )
        new_text, n = OG_SITE_NAME_RE.subn(r"\1" + og_tags.replace("\\", "\\\\"), text, count=1)
        if n:
            text = new_text
            changes += 1

    if "twitter:image" not in text:
        twitter_tags = f'<meta name="twitter:image" content="{img_url}">\n'
        new_text, n = TWITTER_DESC_RE.subn(r"\1" + twitter_tags.replace("\\", "\\\\"), text, count=1)
        if n:
            text = new_text
            changes += 1

    new_text, n = TWITTER_CARD_RE.subn(
        '<meta name="twitter:card" content="summary_large_image">', text
    )
    if n:
        text = new_text
        changes += 1

    return text, changes


def main() -> None:
    touched = []
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if "og:site_name" not in text:
            # páginas sin bloque social completo (404, verificación de Google, etc.)
            continue

        if path.name in WATCH_IMAGES:
            img_slug, w, h = WATCH_IMAGES[path.name]
        else:
            img_slug, w, h = FALLBACK_IMAGE

        new_text, n = add_tags(text, img_slug, w, h)
        if n:
            path.write_text(new_text, encoding="utf-8")
            touched.append((path.name, img_slug, n))

    print(f"{len(touched)} página(s) modificadas\n")
    for name, img, n in touched:
        print(f"  {name}: imagen={img}, {n} bloque(s) añadido(s)/actualizado(s)")


if __name__ == "__main__":
    main()
