#!/usr/bin/env python3
"""
Añade al catálogo dos microbrands nuevos con enlace directo a la web de la
marca (no Amazon):

  - Scurfa Diver One D1-500 Original  (cuarzo suizo, 500 m, Reino Unido)
  - Nodus Sector II Dive GMT          (automático GMT, Los Ángeles)

Hace TODO lo necesario para integrarlos de forma coherente:
  * crea las dos fichas (clonando la estructura de la de Baltic)
  * genera una ilustración SVG y su PNG (sin fotos de terceros)
  * añade los productos a los PRODUCTS embebidos en comparador,
    mi-coleccion y herramienta-talla-reloj (+ chips del comparador)
  * añade las tarjetas a categorías, index y sitemap
  * recalcula los contadores de categoría del index (estaban desfasados)
  * corrige el botón "Ver en Amazon" de js/comparador.js para microbrands
  * restaura el radar de la ficha de Baltic (le faltaba el script)

Es idempotente: si los productos ya existen, no los duplica.

Uso: python3 scripts/add_microbrand_watches.py
"""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"

# --------------------------------------------------------------------------
# Datos de los dos relojes (solo hechos contrastados con la web oficial de la
# marca o con reseñas publicadas; lo subjetivo está marcado como valoración).
# --------------------------------------------------------------------------
SCURFA = {
    "id": "scurfa-diver-one-d1-500",
    "marca": "Scurfa",
    "modelo": "Diver One D1-500 Original",
    "color": "#1b1e24",
    "precio": "345",
    "hook": "Microbrand británica: diver de cuarzo suizo con 500 m de resistencia, bisel de cerámica y zafiro abombado, vendido directo por la marca.",
    "categorias": ["cuarzo", "resistentes", "microbrands"],
    "specs": [
        ["Movimiento", "Cuarzo suizo ETA F06.412 (HeavyDrive y PreciDrive)"],
        ["Reserva de marcha", "Cuarzo con pila (autonomía no indicada por la marca)"],
        ["Diámetro de caja", "40 mm"],
        ["Grosor", "14,4 mm"],
        ["Resistencia al agua", "500 m"],
        ["Cristal", "Zafiro abombado con antirreflejante azul en la cara interior"],
        ["Correa", "Caucho de 20 mm"],
        ["Distancia entre asas", "47,7 mm"],
        ["Garantía", "12 meses"],
    ],
    "pros": [
        "500 m de resistencia al agua con corona de rosca de 7 mm y cuatro juntas: margen de sobra para cualquier uso",
        "Cuarzo suizo ETA F06.412: preciso y sin más mantenimiento que cambiar la pila",
        "Zafiro abombado con antirreflejante y bisel de cerámica de 120 clics, algo poco habitual a este precio",
        "Super-LumiNova BGW9 grado A en esfera, agujas y marcas del bisel",
    ],
    "contras": [
        "Es de cuarzo: si buscas un movimiento mecánico, no es tu reloj",
        "14,4 mm de grosor y 47,7 mm entre asas: puede resultar voluminoso en muñecas pequeñas",
        "Solo se vende en la web de la marca, con envío desde Reino Unido (aduanas e impuestos según destino); en la fecha de esta ficha figuraba como \"a la espera de stock\"",
    ],
    "ideal": "Quien quiere un diver de herramienta —robusto, sin mantenimiento y con especificaciones de buceo reales— sin pagar precio de marca suiza grande.",
    "resenas": "Aparece con frecuencia en reseñas independientes de divers asequibles, como las de Watch Clicker, Two Broke Watch Snobs o Analogue Collective. Transparencia: aún no hemos tenido este reloj en la muñeca; la ficha se basa en las especificaciones oficiales de la marca y en reseñas publicadas. Precio: 298 £ en su web (cambio aproximado).",
    "val": {"diseno": 7, "robustez": 9, "precision": 9, "versatilidad": 6, "precio": 8},
    "enlace": "https://www.scurfawatches.com/product/diver-one-d1-500-original/",
    "es_microbrand": True,
    "image_url": "img/scurfa-diver-one-d1-500.png",
    "diametro_mm": 40,
}

NODUS = {
    "id": "nodus-sector-ii-dive-gmt",
    "marca": "Nodus",
    "modelo": "Sector II Dive GMT",
    "color": "#1f4d7a",
    "precio": "480",
    "hook": "Microbrand californiana: diver GMT automático con movimiento Seiko NH34, zafiro y brazalete estilo Oyster, ensamblado en Los Ángeles.",
    "categorias": ["automaticos", "resistentes", "microbrands"],
    "specs": [
        ["Movimiento", "Automático Seiko (TMI) NH34 con función GMT"],
        ["Reserva de marcha", "Unas 41 horas (según el calibre NH34)"],
        ["Diámetro de caja", "40 mm"],
        ["Grosor", "11,9 mm"],
        ["Resistencia al agua", "100 m"],
        ["Cristal", "Zafiro"],
        ["Correa", "Brazalete de acero estilo Oyster con módulo de ajuste NodeX"],
        ["Origen", "Ensamblado en Los Ángeles (EE. UU.)"],
    ],
    "pros": [
        "GMT automático con aguja dedicada para una segunda zona horaria, a un precio muy por debajo del de las marcas suizas",
        "11,9 mm de grosor: la caja se adelgazó 0,6 mm respecto a la generación anterior, y se nota bajo el puño",
        "Cristal de zafiro y brazalete de acero con módulo de ajuste NodeX para afinar el ajuste sin herramientas",
        "Tres colores de esfera (azul, verde espuma de mar o naranja) y dos opciones de bisel",
    ],
    "contras": [
        "100 m de resistencia: suficiente para nadar, pero menos que el Baltic Aquascaphe (200 m) o el Scurfa D1-500 (500 m)",
        "Calibre NH34: fiable y fácil de reparar, pero con la precisión típica de la familia NH (segundos al día), no la de un cronómetro",
        "Venta directa en la web de Nodus con envío desde EE. UU.: sin devolución tipo Amazon y con servicio técnico dependiente de la marca",
    ],
    "ideal": "Quien viaja o trabaja con dos husos horarios y quiere un GMT automático con aspecto de diver, sin pagar precio de marca suiza.",
    "resenas": "Medios como Fratello Watches y Gear Patrol lo han calificado, respectivamente, como el mejor reloj de viaje asequible y como un GMT que rinde por encima de su precio. Transparencia: aún no hemos tenido este reloj en la muñeca; la ficha se basa en las especificaciones publicadas y en reseñas. Precio de referencia: 525 $ (Gear Patrol, febrero de 2025); conviene comprobar el actual en la web de la marca.",
    "val": {"diseno": 8, "robustez": 7, "precision": 7, "versatilidad": 8, "precio": 7},
    "enlace": "https://www.noduswatches.com/sector-dive-gmt",
    "es_microbrand": True,
    "image_url": "img/nodus-sector-ii-dive-gmt.png",
    "diametro_mm": 40,
}

# Textos propios de la ficha (no van a los PRODUCTS embebidos)
PAGE_EXTRA = {
    SCURFA["id"]: {
        "badges": ["Relojes de cuarzo", "Resistentes al agua (100 m+)", "Microbrands independientes"],
        "crumb_cat": ("categoria-cuarzo.html", "Relojes de cuarzo"),
        "price_note": "298 £ en la web de la marca (cambio aproximado)",
        "button": "Ver en Scurfa Watches",
        "historia": "Scurfa es una microbrand con sede en el Reino Unido y el Diver One (D1) es su reloj de buceo de referencia. Según la propia marca, la correa de caucho de 20 mm se inspira en las correas italianas de cuero que llevaban muchos relojes de buceo vintage.",
        "funciones": "Bisel unidireccional de 120 clics con inserto de cerámica y marcas luminosas, para cronometrar el tiempo de inmersión. El movimiento de cuarzo ETA F06.412 incorpora HeavyDrive (protección antichoque) y PreciDrive (compensación térmica), según la marca.",
        "outfit": 'Es un reloj de herramienta: con la correa de caucho encaja en piscina, playa y uso diario informal. Por tamaño (40 mm de caja y 14,4 mm de grosor) se lleva mejor con ropa casual que bajo el puño de una camisa de vestir. Si prefieres un buceador mecánico, el <a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a> o el <a href="/reloj-nodus-sector-ii-dive-gmt.html">Nodus Sector II Dive GMT</a> son alternativas automáticas.',
        "related": ["citizen-promaster-eco-drive-diver", "baltic-aquascaphe-mk2", "tissot-prx-quartz"],
        "faq": [
            ("¿El Scurfa Diver One D1-500 es sumergible?", "Sí: con 500 m de resistencia, corona de rosca y bisel de buceo está pensado para buceo, no solo para nadar."),
            ("¿Qué movimiento lleva el Scurfa Diver One D1-500?", "Cuarzo suizo ETA F06.412, con tecnologías HeavyDrive (antichoque) y PreciDrive (compensación térmica)."),
            ("¿Dónde se compra, en Amazon?", "No: Scurfa vende desde su propia web, scurfawatches.com, con envío desde el Reino Unido."),
        ],
        "ld_desc": "Microbrand británica: diver de cuarzo suizo con 500 m de resistencia, bisel de cerámica y zafiro abombado.",
        "offer": {"priceCurrency": "GBP", "price": "298", "availability": "https://schema.org/BackOrder"},
        "svg": {"dial": "#15181d", "dial2": "#101317", "ring": "#2b3038", "text": "SCURFA", "gmt": False},
        "radar_color": "#7c95a8",
    },
    NODUS["id"]: {
        "badges": ["Relojes automáticos", "Resistentes al agua (100 m+)", "Microbrands independientes"],
        "crumb_cat": ("categoria-automaticos.html", "Relojes automáticos"),
        "price_note": "525 $ de referencia (cambio aproximado; comprueba el precio actual en su web)",
        "button": "Ver en Nodus Watches",
        "historia": "Nodus Watches es una microbrand con sede en Los Ángeles, y el Sector Dive original salió en enero de 2020. El Sector II es su segunda generación, con una caja más delgada (0,6 mm menos que la anterior); la versión GMT añade una aguja para seguir una segunda zona horaria.",
        "funciones": "Aguja GMT dedicada para leer una segunda zona horaria, bisel giratorio unidireccional con marcas luminosas y Super-LumiNova en agujas e índices. El movimiento es un Seiko (TMI) NH34, la variante GMT de la familia NH.",
        "outfit": 'Con el brazalete de acero de estilo Oyster sube de categoría: encaja con ropa casual y smart-casual, y sus 11,9 mm de grosor ayudan a que pase bajo un puño. Si buscas un buceador sin GMT y más resistente, el <a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a> (200 m) o el <a href="/reloj-scurfa-diver-one-d1-500.html">Scurfa Diver One D1-500</a> (500 m, cuarzo) son alternativas a tener en cuenta.',
        "related": ["baltic-aquascaphe-mk2", "scurfa-diver-one-d1-500", "seiko-5-sports"],
        "faq": [
            ("¿El Nodus Sector II Dive GMT es sumergible?", "Sí, con 100 m sirve para nadar y snorkel; para buceo más exigente conviene un reloj con más resistencia."),
            ("¿Qué movimiento lleva el Nodus Sector II Dive GMT?", "Un automático Seiko (TMI) NH34 con función GMT, con aguja dedicada para una segunda zona horaria."),
            ("¿Dónde se compra, en Amazon?", "No: Nodus vende directamente desde su web, noduswatches.com, con ensamblaje en Los Ángeles."),
        ],
        "ld_desc": "Microbrand californiana: diver GMT automático con movimiento Seiko NH34, zafiro y brazalete estilo Oyster.",
        "offer": {"priceCurrency": "USD", "price": "525"},
        "svg": {"dial": "#1f4d7a", "dial2": "#183e63", "ring": "#9aa0a8", "text": "NODUS", "gmt": True},
        "radar_color": "#7c95a8",
    },
}

NEW = [SCURFA, NODUS]
CAT_PAGE = {
    "automaticos": "categoria-automaticos.html",
    "cuarzo": "categoria-cuarzo.html",
    "vestir": "categoria-vestir.html",
    "resistentes": "categoria-resistentes.html",
    "manual": "categoria-manual.html",
    "microbrands": "categoria-microbrands.html",
    "aventura": "categoria-aventura.html",
}


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def write(name: str, text: str) -> None:
    (ROOT / name).write_text(text, encoding="utf-8")


def make_svg(dial, dial2, ring, text, gmt=False) -> str:
    """Ilustración con el mismo lenguaje visual que las originales del sitio."""
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1, y1 = 50 + 32 * math.cos(a), 50 + 32 * math.sin(a)
        x2, y2 = 50 + 28 * math.cos(a), 50 + 28 * math.sin(a)
        ticks += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                  'stroke="#f3eee4" stroke-width="1.4" opacity="0.85"/>')
    gmt_hand = ('<line x1="50" y1="50" x2="50" y2="24" stroke="#e07b39" stroke-width="1.6" '
                'stroke-linecap="round"/>' if gmt else "")
    return (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">'
        f'<circle cx="50" cy="50" r="46" fill="{dial}" stroke="#20242c" stroke-width="3"/>'
        f'<circle cx="50" cy="50" r="40" fill="none" stroke="{ring}" stroke-width="6"/>'
        f'<circle cx="50" cy="50" r="34" fill="{dial2}"/>'
        f"{ticks}"
        '<line x1="50" y1="50" x2="36.1" y2="40.2" stroke="#f3eee4" stroke-width="2.6" stroke-linecap="round"/>'
        '<line x1="50" y1="50" x2="72.1" y2="37.2" stroke="#f3eee4" stroke-width="2" stroke-linecap="round"/>'
        f"{gmt_hand}"
        '<circle cx="50" cy="50" r="2.2" fill="#e3c894"/>'
        f'<text x="50" y="35.7" font-family="Georgia,serif" font-size="5" fill="#f3eee4" '
        f'text-anchor="middle" opacity="0.9">{text}</text>'
        '<rect x="40" y="2" width="20" height="10" rx="2" fill="#2a2f35"/>'
        '<rect x="40" y="88" width="20" height="10" rx="2" fill="#2a2f35"/></svg>'
    )


def spec_value(p, label):
    return next(v for k, v in p["specs"] if k == label)


def strip_html(p) -> str:
    diam = spec_value(p, "Diámetro de caja")
    water = re.match(r"\d+ m", spec_value(p, "Resistencia al agua")).group(0)
    kind = spec_value(p, "Movimiento").split(" ")[0]
    return (f'<div class="spec-strip"><span><b>{diam}</b></span>'
            f'<span><b>{water}</b></span><span>{kind}</span></div>')


def img_face(p, size_attr="") -> str:
    full = f'{p["marca"]} {p["modelo"]}'
    if p["id"] in PAGE_EXTRA:
        inner = p["illustration"]
    else:
        inner = (f'<img src="/img/{Path(p["image_url"]).name}?v=2" alt="{esc(full)}" '
                 'style="width:100%;height:100%;object-fit:cover;border-radius:8px;">')
    return (f'<a href="/reloj-{p["id"]}.html" aria-hidden="true" tabindex="-1">'
            f'<div class="watchface" style="{size_attr}" role="img" aria-label="{esc(full)}">{inner}</div></a>')


def catalog_item(p, indent="  ") -> str:
    full = f'{p["marca"]} {p["modelo"]}'
    return (
        f'{indent}<div class="catalog-item">\n'
        f'  {img_face(p)}\n'
        f'  <div><h3><a href="/reloj-{p["id"]}.html">{esc(full)}</a></h3>'
        f'<div class="hook">{esc(p["hook"])}</div></div>\n'
        f'  {strip_html(p)}\n'
        f'  <div class="buy-col"><span class="price">{p["precio"]} €</span>'
        f'<a class="btn btn-ghost" href="/reloj-{p["id"]}.html">Ver ficha</a></div>\n'
        '</div>'
    )


def load_products():
    t = read("comparador.html")
    i = t.index("const PRODUCTS = ") + len("const PRODUCTS = ")
    data, end = json.JSONDecoder().raw_decode(t[i:])
    return data


# --------------------------------------------------------------------------
# Piezas
# --------------------------------------------------------------------------
def build_product_page(p, products_by_id) -> str:
    x = PAGE_EXTRA[p["id"]]
    base = read("reloj-baltic-aquascaphe-mk2.html")
    full = f'{p["marca"]} {p["modelo"]}'
    url = f"{BASE}/reloj-{p['id']}.html"
    img_url = f"{BASE}/{p['image_url']}?v=2"
    title = f"{full}: ficha y opinión"
    desc = f"Ficha completa del {full}: especificaciones, pros y contras, y para quién es ideal."

    # --- cabecera (metas) ---
    head_a = base[: base.index("<title>")]
    head_b = base[base.index('<link rel="preconnect" href="https://fonts.googleapis.com">'):
                  base.index('<script type="application/ld+json">')]
    metas = (
        f"<title>{esc(title)}</title>\n"
        f'<meta name="description" content="{esc(desc)}">\n'
        f'<link rel="canonical" href="{url}">\n'
        '<meta name="robots" content="index, follow">\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{url}">\n'
        '<meta property="og:site_name" content="Calibre & Correa">\n'
        f'<meta property="og:image" content="{img_url}">\n'
        '<meta property="og:image:width" content="600">\n'
        '<meta property="og:image:height" content="600">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{esc(title)}">\n'
        f'<meta name="twitter:description" content="{esc(desc)}">\n'
        f'<meta name="twitter:image" content="{img_url}">\n'
    )

    # --- JSON-LD ---
    offer = {"@type": "Offer", **x["offer"], "url": p["enlace"]}
    ld_product = {"@context": "https://schema.org", "@type": "Product", "name": full,
                  "image": img_url, "brand": {"@type": "Brand", "name": p["marca"]},
                  "description": x["ld_desc"], "offers": offer}
    cat_file, cat_name = x["crumb_cat"]
    ld_crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/index.html"},
        {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"{BASE}/{cat_file}"},
        {"@type": "ListItem", "position": 3, "name": full, "item": url}]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in x["faq"]]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n'
                 for o in (ld_product, ld_crumb, ld_faq))

    # --- cuerpo: cabecera de sitio verbatim desde Baltic ---
    nav = base[base.index('<script>try{var t=localStorage'): base.index('<div id="app">') + len('<div id="app">')]

    badges = "".join(f'<span class="badge">{b}</span>' for b in x["badges"])
    rows = "\n".join(f"<tr><td>{k}</td><td>{esc(v)}</td></tr>" for k, v in p["specs"])
    pros = "\n".join(f"<li>{esc(s)}</li>" for s in p["pros"])
    cons = "\n".join(f"<li>{esc(s)}</li>" for s in p["contras"])
    related = "\n".join(catalog_item(products_by_id[r], indent="") for r in x["related"])
    faq = "".join(f"<h3>{esc(q)}</h3><p style='color:var(--paper-dim)'>{esc(a)}</p>" for q, a in x["faq"])
    face = (f'<a href="/reloj-{p["id"]}.html" aria-hidden="true" tabindex="-1"><div class="watchface" '
            f'style="" role="img" aria-label="{esc(full)}">{p["illustration"]}</div></a>')

    content = f"""

<div class="wrap">
  <div class="breadcrumb"><a href="/index.html">Inicio</a> / <a href="/{cat_file}">{cat_name}</a> / {esc(p["marca"])}</div>
  <div class="product-head">
    <div>{face}</div>
    <div>
      <div>{badges}</div>
      <h1 style="font-size:1.9rem;margin-top:10px;">{esc(full)}</h1>
      <p style="color:var(--paper-dim)">{esc(p["hook"])}</p>
      <span class="price" style="font-size:1.6rem;">{p["precio"]} €</span><br>
      <small style="color:var(--paper-dim)">{esc(x["price_note"])}</small><br>
      <a class="btn btn-primary" href="{p["enlace"]}" target="_blank" rel="nofollow noopener">{x["button"]}</a>
    </div>
  </div>
</div>
<section><div class="wrap two-col">
  <div><h2>Ficha técnica</h2><table class="spec-table">{rows}</table></div>
  <div><h2>Valoración por criterios</h2><canvas class="radar" id="radarSingle"></canvas></div>
</div></section>
<section><div class="wrap two-col">
  <div><h2>Puntos a favor</h2><ul class="plain pros">{pros}</ul></div>
  <div><h2>Puntos en contra</h2><ul class="plain cons">{cons}</ul></div>
</div></section>
<section><div class="wrap">
  <h2>¿Para quién es ideal?</h2><p style="color:var(--paper-dim);max-width:65ch;">{esc(p["ideal"])}</p>
  <h2 style="margin-top:32px;">Lo que dicen las reseñas</h2><p style="color:var(--paper-dim);max-width:65ch;">{esc(p["resenas"])}</p>
</div></section>
<section><div class="wrap two-col">
  <div><h2>Historia y diseño</h2><p style="color:var(--paper-dim);max-width:65ch;">{esc(x["historia"])}</p></div>
  <div><h2>Complicaciones y funciones</h2><p style="color:var(--paper-dim);max-width:65ch;">{esc(x["funciones"])}</p></div>
</div></section>
<section><div class="wrap"><h2>¿Con qué outfit combinarlo?</h2><p style="color:var(--paper-dim);max-width:65ch;">{x["outfit"]}</p></div></section>
<section><div class="wrap"><h2>También te puede interesar</h2>{related}</div></section>
<section><div class="wrap"><h2>Preguntas frecuentes</h2>{faq}</div></section>
"""
    tail = base[base.index("</div>\n<footer"):]
    vals = [p["val"][k] for k in ("diseno", "robustez", "precision", "versatilidad", "precio")]
    radar = (f'<script src="/js/radar.js"></script>\n'
             f'<script>drawRadar(document.getElementById("radarSingle"), [{{values:{vals}, '
             f'color:"{x["radar_color"]}"}}], ["Diseño","Robustez","Precisión","Versatilidad","Precio"]);</script>\n')
    tail = tail.replace("</body>", radar + "</body>")
    return head_a + metas + head_b + ld + nav + content + tail


def render_png(p) -> None:
    """Rasteriza la ilustración a PNG 600x600 (para og:image y JSON-LD)."""
    from playwright.sync_api import sync_playwright
    html = ('<html><body style="margin:0;background:#12151b;display:flex;align-items:center;'
            f'justify-content:center;width:600px;height:600px"><div style="width:520px;height:520px">{p["illustration"]}</div></body></html>')
    out = ROOT / p["image_url"]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 600, "height": 600})
        pg.set_content(html)
        pg.screenshot(path=str(out))
        b.close()


def insert_after_last_item(text: str, item: str) -> str:
    k = text.rindex('class="buy-col"')
    m = re.compile(r"</a></div>\s*</div>").search(text, k)
    e = m.end()
    return text[:e] + "\n" + item + text[e:]


def main() -> None:
    products = load_products()
    existing_ids = {p["id"] for p in products}
    for p in NEW:
        x = PAGE_EXTRA[p["id"]]
        p["illustration"] = make_svg(**x["svg"])
    to_add = [p for p in NEW if p["id"] not in existing_ids]

    # 0) PNG de las ilustraciones (siempre, por si faltan)
    for p in NEW:
        if not (ROOT / p["image_url"]).exists():
            render_png(p)
            print("PNG:", p["image_url"])

    all_products = products + to_add
    by_id = {p["id"]: p for p in all_products}

    # 1) Fichas
    for p in NEW:
        write(f"reloj-{p['id']}.html", build_product_page(p, by_id))
        print("Ficha:", f"reloj-{p['id']}.html")

    # 2) PRODUCTS embebidos (insertando texto para no tocar nada más)
    if to_add:
        for name in ("comparador.html", "mi-coleccion.html", "herramienta-talla-reloj.html"):
            t = read(name)
            i = t.index("const PRODUCTS = ") + len("const PRODUCTS = ")
            _, end = json.JSONDecoder().raw_decode(t[i:])
            arr_end = i + end - 1  # posición del ']' final
            extra = "".join(", " + json.dumps(p, ensure_ascii=False) for p in to_add)
            t = t[:arr_end] + extra + t[arr_end:]
            write(name, t)
            print("PRODUCTS +", len(to_add), "en", name)

        # chips del comparador
        t = read("comparador.html")
        chips = "".join(
            f'\n      <label class="pick-chip"><input type="checkbox" value="{p["id"]}"> {p["marca"]} {p["modelo"]}</label>'
            for p in to_add)
        anchor = 'Baltic Aquascaphe MK2</label>'
        assert anchor in t
        t = t.replace(anchor, anchor + chips, 1)
        write("comparador.html", t)

    # 3) Tarjetas en categorías
    for p in NEW:
        for cat in p["categorias"]:
            name = CAT_PAGE[cat]
            t = read(name)
            if f'/reloj-{p["id"]}.html' in t:
                continue
            write(name, insert_after_last_item(t, catalog_item(p)))
            print("Tarjeta:", p["id"], "->", name)

    # 4) Index: tarjetas, subtítulo y contadores de categoría
    t = read("index.html")
    for p in NEW:
        if f'/reloj-{p["id"]}.html' not in t:
            t = insert_after_last_item(t, catalog_item(p))
    # Contadores recalculados a partir de los datos
    for cat, page in CAT_PAGE.items():
        n = sum(1 for p in all_products if cat in p["categorias"])
        t = re.sub(rf'(href="/{re.escape(page)}"><div class="n">)\d+(</div>)', rf"\g<1>{n}\g<2>", t)
    n_total = len(all_products)
    words = {9: "Nueve", 10: "Diez", 11: "Once", 12: "Doce"}
    t = re.sub(r"Seis relojes de gama media y media-alta",
               f"{words.get(n_total, str(n_total))} relojes de gama media y media-alta", t)
    write("index.html", t)

    # 5) Sitemap
    t = read("sitemap.xml")
    for p in NEW:
        loc = f"{BASE}/reloj-{p['id']}.html"
        if loc not in t:
            t = t.replace("</urlset>", f"  <url><loc>{loc}</loc></url>\n</urlset>")
    write("sitemap.xml", t)

    # 6) Guía de movimientos: el recuento de relojes
    t = read("guia-tipos-de-movimiento.html")
    t = t.replace("Con los 9 relojes de nuestro catálogo", f"Con los {n_total} relojes de nuestro catálogo")
    write("guia-tipos-de-movimiento.html", t)

    # 7) Botón del comparador: microbrands no se compran en Amazon
    js = read("js/comparador.js")
    old = '>Ver en Amazon</a></td>'
    new = '>${p.es_microbrand ? "Ver en la web de la marca" : "Ver en Amazon"}</a></td>'
    if old in js:
        write("js/comparador.js", js.replace(old, new))
        print("comparador.js: botón según microbrand")

    # 8) Radar de la ficha de Baltic (le faltaba el script)
    t = read("reloj-baltic-aquascaphe-mk2.html")
    if "drawRadar" not in t:
        b = by_id["baltic-aquascaphe-mk2"]["val"]
        vals = [b[k] for k in ("diseno", "robustez", "precision", "versatilidad", "precio")]
        radar = ('<script src="/js/radar.js"></script>\n'
                 f'<script>drawRadar(document.getElementById("radarSingle"), [{{values:{vals}, '
                 'color:"#5b8db8"}], ["Diseño","Robustez","Precisión","Versatilidad","Precio"]);</script>\n')
        write("reloj-baltic-aquascaphe-mk2.html", t.replace("</body>", radar + "</body>"))
        print("Baltic: radar restaurado")


if __name__ == "__main__":
    main()
