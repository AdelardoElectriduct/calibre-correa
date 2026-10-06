#!/usr/bin/env python3
"""Pulido SEO idempotente: JSON-LD válido, h1 en páginas de lista, títulos y descripciones."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def rw(name, fn):
    p = ROOT / name
    t = p.read_text(encoding="utf-8")
    n = fn(t)
    if n != t:
        p.write_text(n, encoding="utf-8"); print("✓", name)

def set_title(t, title):
    t = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", t, 1)
    return t

def set_desc(t, d):
    t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+d+m.group(2), t, 1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+d+m.group(2), t, 1)
    t = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+d+m.group(2), t, 1)
    return t

# (a) JSON-LD
def fix_ld(t):
    def f(m):
        body = m.group(2)
        try: json.loads(body); return m.group(0)
        except Exception: pass
        import ast
        return m.group(1)+json.dumps(ast.literal_eval(body.strip()), ensure_ascii=False)+m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', f, t, flags=re.S)
rw("guia-tipos-de-movimiento.html", fix_ld)

# (b) h1
H1 = ["categoria-automaticos","categoria-aventura","categoria-cuarzo","categoria-manual","categoria-microbrands",
      "categoria-resistentes","categoria-vestir","comparador","herramienta-talla-reloj","mi-coleccion","ofertas","sugiere-un-reloj"]
def h1(t):
    if "<h1" in t: return t
    return re.sub(r'(<div class="section-head">)<h2>(.*?)</h2>', r'\1<h1>\2</h1>', t, 1, flags=re.S)
for n in H1: rw(n+".html", h1)
css = ROOT/"css/styles.css"; c = css.read_text(encoding="utf-8")
if ".section-head h1" not in c:
    c = c.replace(".section-head h2{font-size:1.7rem;max-width:26ch;}", ".section-head h1,.section-head h2{font-size:1.7rem;max-width:26ch;}")
    css.write_text(c, encoding="utf-8"); print("✓ css")

# (c) títulos de fichas
for p in ROOT.glob("reloj-*.html"):
    rw(p.name, lambda t: re.sub(r"<title>([^<]*?): ficha técnica y valoración \| Calibre (?:&amp;|&) Correa</title>", r"<title>\1: ficha y opinión</title>", t))

# (d)/(e) títulos y descripciones sueltos
TITLES = {
 "index.html": "Calibre & Correa: comparativas de relojes automáticos y cuarzo",
 "categoria-microbrands.html": "Microbrands independientes: comparativa y fichas",
 "categoria-resistentes.html": "Relojes resistentes al agua (100 m+): fichas",
 "guia-cuando-pagar-mas-reloj.html": "¿Cuándo pagar más por un reloj? 500-650€ vs 200-350€",
 "guia-relojes-automaticos-entrada.html": "Mejores relojes automáticos de entrada bajo 400€ (2026)",
 "guia-tipos-de-movimiento.html": "Automático, cuarzo, solar o manual: qué elegir",
}
for n, ti in TITLES.items(): rw(n, lambda t, ti=ti: set_title(t, ti))
DESCS = {
 "categoria-automaticos.html": "Relojes con movimiento mecánico que se carga con el movimiento de la muñeca, sin batería. La puerta de entrada habitual a la relojería como afición.",
 "categoria-cuarzo.html": "Relojes de cuarzo: más precisos día a día que un automático y con mantenimiento mínimo. Ideales si priorizas la exactitud sobre lo mecánico.",
 "ofertas.html": "Bajadas de precio puntuales en relojes automáticos y de cuarzo de gama media, revisadas a mano antes de publicarlas.",
 "aviso-legal-afiliados.html": "Aviso legal y transparencia de Calibre & Correa: sin programas de afiliación ni publicidad por ahora, con opiniones independientes.",
}
for n, d in DESCS.items(): rw(n, lambda t, d=d: set_desc(t, d))
