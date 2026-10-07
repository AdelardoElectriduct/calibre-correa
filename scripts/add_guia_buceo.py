#!/usr/bin/env python3
"""Genera guia-mejores-relojes-buceo.html (idempotente) y la enlaza en sitemap, guías e índice."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-mejores-relojes-buceo.html"
TITLE = "Mejores relojes de buceo y resistentes al agua (2026)"
DESC = "Guía para elegir un reloj de buceo o resistente al agua entre 229€ y 650€: qué significa 100, 200 o 500 m y 6 modelos comparados."

W = [  # slug, nombre, precio, agua, movimiento, caja, veredicto
 ("reloj-citizen-promaster-eco-drive-diver.html","Citizen Promaster Eco-Drive Diver","229 €","200 m (ISO 6425)","Cuarzo solar","44 mm","Es el buceador certificado más barato de la selección y no necesita pilas."),
 ("reloj-seiko-5-sports.html","Seiko 5 Sports (SRPD)","229 €","100 m","Automático","42,5 mm","La opción económica para quien quiere automático y nadar sin miedo."),
 ("reloj-scurfa-diver-one-d1-500.html","Scurfa Diver One D1-500","345 €","500 m","Cuarzo suizo","40 mm","El que más agua aguanta de la lista, con zafiro y caja de 40 mm."),
 ("reloj-nodus-sector-ii-dive-gmt.html","Nodus Sector II Dive GMT","480 €","100 m","Automático con GMT","40 mm","Para quien quiere un segundo huso horario además de poder nadar."),
 ("reloj-baltic-aquascaphe-mk2.html","Baltic Aquascaphe MK2","630 €","200 m","Automático","39,5 mm","Es el más pulido de acabado y el de mejor equilibrio estético."),
 ("reloj-seiko-alpinist-spb210.html","Seiko Prospex Alpinist SPB210","650 €","200 m","Automático","39,5 mm","Más de montaña que de mar, pero con 200 m y zafiro."),
]
FAQ = [
 ("¿100 m de resistencia al agua sirven para bucear?",
  "No. 100 m significa que aguanta bien nadar, el snorkel y las salpicaduras, pero no es un reloj de buceo con botellas. Para eso se busca una certificación específica como ISO 6425 y, como mínimo, 200 m."),
 ("¿Qué reloj de buceo barato recomendáis?",
  "El Citizen Promaster Eco-Drive Diver, por 229 €: 200 m con certificación ISO 6425, cuarzo solar y 44 mm de caja."),
 ("¿Automático o cuarzo para un reloj de agua?",
  "Ambos sirven. El cuarzo (como el Promaster o el Scurfa) es más preciso y necesita menos mantenimiento; el automático (Seiko 5 Sports, Nodus, Baltic) aporta el componente mecánico."),
 ("¿Puedo ducharme con un reloj resistente al agua?",
  "Con 100 m o más aguanta técnicamente, pero el agua caliente y el vapor castigan las juntas con el tiempo, así que lo mejor es evitarlo."),
]

def esc(s): return s.replace("&","&amp;")

def build():
    rows = "".join(
      f'<tr><td><a href="/{s}">{esc(n)}</a></td><td>{p}</td><td>{a}</td><td>{m}</td><td>{c}</td></tr>' for s,n,p,a,m,c,_ in W)
    picks = "".join(f'<li><a href="/{s}"><strong>{esc(n)}</strong></a> ({p}): {v}</li>' for s,n,p,a,m,c,v in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{SLUG}","author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/"guia-relojes-automaticos-entrada.html").read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace("guia-relojes-automaticos-entrada.html", SLUG)
    head = head.replace(f'/{SLUG}" class="active"', '/guia-relojes-automaticos-entrada.html" class="active"')
    head = head.replace("</head>", ld_html+"</head>")
    head = head.replace('</head>', '<style>table.guide-table{width:100%;border-collapse:collapse;font-size:0.9rem;min-width:520px}table.guide-table th,table.guide-table td{text-align:left;padding:10px 8px;border-top:1px solid var(--line)}table.guide-table th{color:var(--steel);font-weight:600;border-top:0}article.guide h3{font-size:1.05rem;margin-top:1.2em}article.guide ul{color:var(--paper-dim)}</style>\n</head>',1)
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Mejores relojes de buceo y resistentes al agua en 2026</h1>
  <p>Si quieres un reloj para nadar, hacer snorkel o simplemente no preocuparte por el agua, hay modelos desde 229 € que lo permiten. Lo difícil es entender qué significan los números que pone cada marca. Esta guía los traduce y compara los seis modelos resistentes de nuestro catálogo.</p>
  <h2>1. Qué significa realmente 50, 100, 200 o 500 m</h2>
  <p>Con 50 m el reloj aguanta lluvia y lavarse las manos, no nadar. Con 100 m ya es válido para piscina, mar y snorkel. Con 200 m o más entramos en territorio de buceo, y si además lleva certificación <strong>ISO 6425</strong> (el estándar de relojes de buceo) tienes la garantía de que se ha probado como tal. El Scurfa llega a 500 m, aunque para un uso normal esa cifra es más margen que necesidad.</p>
  <h2>2. Qué mirar además de la cifra</h2>
  <p>Fíjate en el cristal (el zafiro resiste mejor los arañazos que el mineral), en el tamaño de la caja (por encima de 42 mm se ve grande en muñecas finas, puedes comprobarlo con la <a href="/herramienta-talla-reloj.html">herramienta de talla</a>) y en el tipo de movimiento: cuarzo o automático.</p>
  <h2>3. Comparativa rápida</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Agua</th><th>Movimiento</th><th>Caja</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>4. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver</a>. Es el único de la selección de 229 € con certificación ISO 6425 y 200 m, y al ser solar no hay que cambiar pila. Si prefieres un automático barato para nadar, el <a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a>; si quieres un microbrand con mejor acabado, el <a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a>.</p>
  <ul>{picks}</ul>
  <p>Todos están en el <a href="/comparador.html">comparador</a> y en la categoría de <a href="/categoria-resistentes.html">relojes resistentes al agua</a>. Para decidir entre automático y cuarzo lee <a href="/guia-tipos-de-movimiento.html">qué movimiento elegir</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        line = f'  <url><loc>{BASE}/guia-tipos-de-movimiento.html</loc></url>\n'
        assert line in t
        sm.write_text(t.replace(line, line+f'  <url><loc>{BASE}/{SLUG}</loc></url>\n'), encoding="utf-8"); print("✓ sitemap")
    # enlace cruzado desde las otras guías y categoría resistentes
    add = f'<p>Si lo que buscas es un reloj para el agua, mira la <a href="/{SLUG}">guía de relojes de buceo y resistentes al agua</a>.</p>\n'
    for n in ["guia-relojes-automaticos-entrada.html","guia-tipos-de-movimiento.html","guia-cuando-pagar-mas-reloj.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG not in t:
            p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
if __name__ == "__main__": main()
