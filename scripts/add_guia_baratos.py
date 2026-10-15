#!/usr/bin/env python3
"""Genera guia-mejores-relojes-vestir.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-mejores-relojes-baratos.html"
TITLE = "Mejores relojes por menos de 250€ (2026)"
DESC = "Los tres relojes de nuestro catálogo por menos de 250€: un solar certificado de buceo y dos automáticos. Precios, agua, movimiento y cuál elegir."
W = [
 ("reloj-orient-bambino-v5.html","Orient Bambino Versión 5","220 €","30 m","Automático","40,5 mm","El más barato y de dial clásico: para vestir, no para mojarlo."),
 ("reloj-seiko-5-sports.html","Seiko 5 Sports (SRPD)","229 €","100 m","Automático","42,5 mm","Automático deportivo que sí aguanta nadar."),
 ("reloj-citizen-promaster-eco-drive-diver.html","Citizen Promaster Eco-Drive Diver","229 €","200 m (ISO 6425)","Cuarzo solar","44 mm","El más resistente y el que menos mantenimiento pide: solar y certificado de buceo."),
]
FAQ = [
 ("¿Se puede comprar un buen reloj por menos de 250 €?",
  "Sí. En nuestro catálogo hay tres opciones por menos de 250 €: Orient Bambino V5 (220 €), Seiko 5 Sports (229 €) y Citizen Promaster Eco-Drive Diver (229 €)."),
 ("¿Cuál es el mejor reloj por menos de 250 €?",
  "Depende del uso. Para el día a día con camisa, el Orient Bambino; para algo robusto y automático, el Seiko 5 Sports; si priorizas resistencia y cero mantenimiento, el Citizen Promaster solar."),
 ("¿Merece la pena subir un poco de presupuesto?",
  "Por unos 100 € más tienes cristal de zafiro: el Citizen Tsuyosa (329 €) o el Scurfa Diver One (345 €). Si no te importa el zafiro, no hace falta."),
 ("¿Hay relojes automáticos baratos que sean fiables?",
  "El Orient Bambino V5 y el Seiko 5 Sports usan calibres con décadas de uso (Orient F6724 y Seiko 4R36), pensados para este rango de precio."),
]
def build():
    rows = "".join(f'<tr><td><a href="/{s}">{n}</a></td><td>{p}</td><td>{a}</td><td>{m}</td><td>{c}</td></tr>' for s,n,p,a,m,c,_ in W)
    picks = "".join(f'<li><a href="/{s}"><strong>{n}</strong></a> ({p}): {v}</li>' for s,n,p,a,m,c,v in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{SLUG}","author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/"guia-mejores-relojes-buceo.html").read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace("guia-mejores-relojes-buceo.html", SLUG)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Mejores relojes por menos de 250€ en 2026</h1>
  <p>Por menos de 250 € ya hay relojes de verdad: dos automáticos y un solar certificado de buceo. Esta guía compara los tres modelos de nuestro catálogo que entran en ese presupuesto y te dice cuál elegir según el uso.</p>
  <h2>1. Qué puedes esperar por este precio</h2>
  <p>Cristal mineral o Hardlex en lugar de zafiro, acabados correctos y movimientos fiables pero sin lujos. A cambio, el precio es la mejor puerta de entrada a la relojería: el Seiko 5 y el Orient llevan calibres automáticos conocidos y fáciles de mantener.</p>
  <h2>2. Qué mirar antes de comprar</h2>
  <p>Decide primero el uso: vestir (Orient, 30 m), día a día y agua (Seiko 5, 100 m) o buceo y cero mantenimiento (Citizen solar, 200 m). En la <a href="/herramienta-talla-reloj.html">herramienta de talla</a> puedes ver si 42,5 o 44 mm te quedan bien.</p>
  <h2>3. Comparativa rápida</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Agua</th><th>Movimiento</th><th>Caja</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>4. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a>. Es automático, aguanta 100 m y cuesta 229 €. Si prefieres no cambiar pilas ni dar cuerda, el <a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster solar</a>.</p>
  <ul>{picks}</ul>
  <p>Todos están en el <a href="/comparador.html">comparador</a> y en la categoría de <a href="/categoria-automaticos.html">relojes automáticos</a>. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">qué movimiento elegir</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        m = re.search(r"<url><loc>[^<]*guia-mejores-relojes-vestir\.html</loc>.*?</url>\n", t)
        assert m
        sm.write_text(t[:m.end()] + f'  <url><loc>{BASE}/{SLUG}</loc></url>\n' + t[m.end():], encoding="utf-8"); print("✓ sitemap")
    add = f'<p>Si tu presupuesto es ajustado, mira la <a href="/{SLUG}">guía de relojes por menos de 250€</a>.</p>\n'
    for n in ["guia-relojes-automaticos-entrada.html","guia-cuando-pagar-mas-reloj.html","categoria-automaticos.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        if "</article>" in t:
            t = t.replace("</article>", add+"</article>",1)
        else:
            t = t.replace('</div></div>', ' <a href="/'+SLUG+'">Lee la guía de relojes baratos</a>.</div></div>',1) if False else re.sub(r'(<div class="section-head"><h1>[^<]*</h1><div class="sub">[^<]*)(</div></div>)', lambda m: m.group(1)+f' <a href="/{SLUG}">Lee la guía de relojes baratos</a>.'+m.group(2), t, 1)
        p.write_text(t, encoding="utf-8"); print("✓ enlace en", n)
    # footer
    old = '<a href="/guia-mejores-relojes-vestir.html">Guía: relojes de vestir</a>'
    new = old + f'\n      <a href="/{SLUG}">Guía: relojes por menos de 250€</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,new),encoding="utf-8")
if __name__ == "__main__": main()
