#!/usr/bin/env python3
"""Genera guia-mejores-relojes-vestir.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-mejores-relojes-vestir.html"
TITLE = "Mejores relojes de vestir por menos de 400€ (2026)"
DESC = "Guía para elegir un reloj de vestir entre 220€ y 395€: qué mirar en un reloj elegante y 4 modelos comparados, automáticos y de cuarzo."
W = [
 ("reloj-orient-bambino-v5.html","Orient Bambino Versión 5","220 €","30 m","Automático","40,5 mm","El más barato y de dial clásico: para camisa y traje, no para mojarlo."),
 ("reloj-citizen-tsuyosa.html","Citizen Tsuyosa NJ0151-53M","329 €","50 m","Automático","40 mm","Zafiro y diseño moderno con brazalete: el más versátil entre vestir y diario."),
 ("reloj-seiko-presage-srpb41.html","Seiko Presage Cocktail Time SRPB41","350 €","50 m","Automático","40,5 mm","El dial con más carácter de la lista, pensado para lucirlo."),
 ("reloj-tissot-prx-quartz.html","Tissot PRX Cuarzo","395 €","100 m","Cuarzo suizo","40 x 39,5 mm","El más resistente y preciso, con zafiro y estética de los años 70."),
]
FAQ = [
 ("¿Qué tamaño de caja es mejor para un reloj de vestir?",
  "Entre 38 y 41 mm funciona con casi cualquier muñeca. Los cuatro modelos de esta guía están entre 40 y 40,5 mm."),
 ("¿Automático o cuarzo para vestir?",
  "El automático (Orient, Citizen, Seiko) da el componente mecánico que muchos buscan en un reloj elegante; el cuarzo del Tissot PRX es más preciso y casi no requiere mantenimiento."),
 ("¿Cuál recomendáis si solo puedo comprar uno?",
  "El Citizen Tsuyosa, por 329 €: cristal de zafiro, 40 mm, automático y un diseño que sirve tanto con traje como con ropa casual."),
 ("¿Sirven para mojarse?",
  "Los de 30 m o 50 m (Orient, Tsuyosa, Presage) solo aguantan salpicaduras y lluvia. El Tissot PRX llega a 100 m y sí admite nadar."),
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
  <h1 style="font-size:2rem;">Mejores relojes de vestir por menos de 400€ en 2026</h1>
  <p>Un reloj de vestir no tiene que costar un sueldo. Entre 220 € y 395 € hay opciones con movimiento automático o cuarzo suizo, cristal de zafiro en algunos casos y diales que funcionan igual de bien con camisa que con un jersey. Esta guía compara los cuatro modelos de vestir de nuestro catálogo.</p>
  <h2>1. Qué hace que un reloj sea "de vestir"</h2>
  <p>Caja de 38 a 41 mm, poco grosor para que pase bajo el puño de la camisa, dial limpio y sin elementos deportivos como bisel giratorio. La resistencia al agua pasa a segundo plano: con 30 o 50 m basta para el día a día.</p>
  <h2>2. Qué mirar antes de comprar</h2>
  <p>El cristal importa más de lo que parece: el zafiro apenas se raya, mientras que el mineral o Hardlex es más económico pero se marca con el uso. Revisa también la correa y si el reloj admite cambiarla; en la <a href="/herramienta-talla-reloj.html">herramienta de talla</a> puedes comprobar cómo te quedaría el diámetro.</p>
  <h2>3. Comparativa rápida</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Agua</th><th>Movimiento</th><th>Caja</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>4. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a>. Combina zafiro, automático y un diseño versátil por 329 €. Si tu presupuesto es menor, el <a href="/reloj-orient-bambino-v5.html">Orient Bambino Versión 5</a> es la forma más barata de entrar en la relojería clásica.</p>
  <ul>{picks}</ul>
  <p>Todos están en el <a href="/comparador.html">comparador</a> y en la categoría de <a href="/categoria-vestir.html">relojes de vestir</a>. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">qué movimiento elegir</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        line = f'  <url><loc>{BASE}/guia-mejores-relojes-buceo.html</loc></url>\n'
        assert line in t
        sm.write_text(t.replace(line, line+f'  <url><loc>{BASE}/{SLUG}</loc></url>\n'), encoding="utf-8"); print("✓ sitemap")
    add = f'<p>Si buscas un reloj elegante, mira la <a href="/{SLUG}">guía de relojes de vestir por menos de 400€</a>.</p>\n'
    for n in ["guia-relojes-automaticos-entrada.html","guia-cuando-pagar-mas-reloj.html","guia-mejores-relojes-buceo.html","categoria-vestir.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        if "</article>" in t:
            t = t.replace("</article>", add+"</article>",1)
        else:
            t = t.replace('</div></div>', ' <a href="/'+SLUG+'">Lee la guía de relojes de vestir</a>.</div></div>',1) if False else re.sub(r'(<div class="section-head"><h1>[^<]*</h1><div class="sub">[^<]*)(</div></div>)', lambda m: m.group(1)+f' <a href="/{SLUG}">Lee la guía de relojes de vestir</a>.'+m.group(2), t, 1)
        p.write_text(t, encoding="utf-8"); print("✓ enlace en", n)
    # footer
    old = '<a href="/guia-cuando-pagar-mas-reloj.html">Guía: cuándo pagar más</a>'
    new = old + f'\n      <a href="/{SLUG}">Guía: relojes de vestir</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,new),encoding="utf-8")
if __name__ == "__main__": main()
