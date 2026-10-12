#!/usr/bin/env python3
"""Enriquece las 3 guías antiguas: tabla comparativa, FAQ visible y JSON-LD Article+FAQPage (idempotente)."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
STYLE = ('<style>table.guide-table{width:100%;border-collapse:collapse;font-size:0.9rem;min-width:520px}'
 'table.guide-table th,table.guide-table td{text-align:left;padding:10px 8px;border-top:1px solid var(--line)}'
 'table.guide-table th{color:var(--steel);font-weight:600;border-top:0}article.guide h3{font-size:1.05rem;margin-top:1.2em}</style>\n')

def table(rows, heads):
    th = "".join(f"<th>{h}</th>" for h in heads)
    tr = "".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div style="overflow-x:auto;"><table class="guide-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def L(s,n): return f'<a href="/{s}">{n}</a>'

G = {
"guia-relojes-automaticos-entrada.html": dict(
  anchor='<p>Usa el <a href="/comparador.html">comparador</a>',
  h2="Comparativa rápida de los automáticos de entrada",
  heads=["Reloj","Precio","Reserva de marcha","Agua","Caja"],
  rows=[[L("reloj-orient-bambino-v5.html","Orient Bambino V5"),"220 €","40 h","30 m","40,5 mm"],
        [L("reloj-seiko-5-sports.html","Seiko 5 Sports"),"229 €","41 h","100 m","42,5 mm"],
        [L("reloj-citizen-tsuyosa.html","Citizen Tsuyosa"),"329 €","40 h","50 m","40 mm"],
        [L("reloj-seiko-presage-srpb41.html","Seiko Presage Cocktail Time"),"350 €","41 h","50 m","40,5 mm"]],
  faq=[("¿Cuánto cuesta un buen reloj automático de entrada?","Entre 220 € y 350 € hay cuatro opciones fiables en nuestro catálogo: Orient Bambino V5, Seiko 5 Sports, Citizen Tsuyosa y Seiko Presage Cocktail Time."),
       ("¿Cuál es el mejor primer reloj automático?","El Seiko 5 Sports, por 229 €: 100 m de resistencia al agua y un calibre 4R36 muy probado. Si prefieres diseño, el Citizen Tsuyosa."),
       ("¿Cuánta reserva de marcha tienen?","Unas 40 horas: si lo dejas quieto un fin de semana largo, se para y hay que darle cuerda o ponerlo en hora.")]),
"guia-cuando-pagar-mas-reloj.html": dict(
  anchor='<p>Compara las dos franjas',
  h2="Comparativa de las dos franjas de precio",
  heads=["Reloj","Precio","Cristal","Reserva de marcha","Agua"],
  rows=[[L("reloj-seiko-5-sports.html","Seiko 5 Sports"),"229 €","Hardlex","41 h","100 m"],
        [L("reloj-citizen-tsuyosa.html","Citizen Tsuyosa"),"329 €","Zafiro","40 h","50 m"],
        [L("reloj-hamilton-khaki-field-mechanical.html","Hamilton Khaki Field Mechanical"),"575 €","Zafiro","80 h","50 m"],
        [L("reloj-baltic-aquascaphe-mk2.html","Baltic Aquascaphe MK2"),"630 €","Zafiro","42 h","200 m"],
        [L("reloj-seiko-alpinist-spb210.html","Seiko Prospex Alpinist SPB210"),"650 €","Zafiro","70 h","200 m"]],
  faq=[("¿Merece la pena pagar 600 € por un reloj frente a uno de 250 €?","Si lo vas a usar a diario durante años, sí en algunos casos: zafiro, más resistencia al agua o más reserva de marcha (Hamilton 80 h, Alpinist 70 h). Pero no siempre: el Baltic cuesta 630 € y tiene 42 h."),
       ("¿Un reloj más caro es más preciso?","No necesariamente. Los automáticos de ambas franjas rondan los mismos márgenes de error diarios; un cuarzo como el Tissot PRX es más preciso que cualquiera de ellos."),
       ("¿Qué recomendáis si es mi primer reloj mecánico?","Quedarte en la franja de entrada (Seiko 5 Sports o Citizen Tsuyosa) y subir de gama en el segundo o tercer reloj, cuando sepas qué echas en falta.")]),
"guia-tipos-de-movimiento.html": dict(
  anchor='<h2>¿Y si no sabes cuál elegir?</h2>',
  h2="Un ejemplo de cada tipo en nuestro catálogo",
  heads=["Tipo","Ejemplo","Precio","Reserva / autonomía"],
  rows=[["Automático",L("reloj-seiko-5-sports.html","Seiko 5 Sports"),"229 €","41 h"],
        ["Cuarzo",L("reloj-tissot-prx-quartz.html","Tissot PRX Cuarzo"),"395 €","Batería"],
        ["Solar",L("reloj-citizen-promaster-eco-drive-diver.html","Citizen Promaster Eco-Drive"),"229 €","Hasta 6 meses a oscuras tras carga completa"],
        ["Manual",L("reloj-hamilton-khaki-field-mechanical.html","Hamilton Khaki Field Mechanical"),"575 €","80 h"]],
  faq=[("¿Qué movimiento es mejor para empezar?","Un automático barato como el Seiko 5 Sports si te atrae lo mecánico; un cuarzo o solar si priorizas precisión y cero mantenimiento."),
       ("¿Qué diferencia hay entre automático y manual?","El automático se carga con el movimiento de la muñeca; el manual hay que darle cuerda con la corona."),
       ("¿El solar necesita cambiar pila?","El Citizen Promaster Eco-Drive se carga con la luz y puede aguantar hasta 6 meses a oscuras tras una carga completa.")]),
}

def main():
    for name, g in G.items():
        p = ROOT/name; t = p.read_text(encoding="utf-8")
        if "FAQPage" in t: print("=", name); continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", t); title = re.sub("<[^>]+>","",m.group(1))
        d = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
        faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in g["faq"])
        block = f'<h2>{g["h2"]}</h2>\n  {table(g["rows"], g["heads"])}\n  {faq_html}\n  '
        assert g["anchor"] in t, name
        t = t.replace(g["anchor"], block+g["anchor"], 1)
        ld = [{"@context":"https://schema.org","@type":"Article","headline":title,"description":d,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{name}","author":{"@type":"Organization","name":"Calibre & Correa"}},
              {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in g["faq"]]}]
        # sustituir Article antiguo si existe
        t = re.sub(r'<script type="application/ld\+json">\{[^<]*"@type": ?"Article"[^<]*</script>\n?', "", t)
        ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
        t = t.replace("</head>", STYLE + ld_html + "</head>", 1)
        p.write_text(t, encoding="utf-8"); print("✓", name)
if __name__ == "__main__": main()
