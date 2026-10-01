#!/usr/bin/env python3
"""
Refuerza el enlazado interno añadiendo enlaces contextuales dentro del
texto editorial de cada ficha de reloj (no en el bloque final de
"también te puede interesar", sino integrados en la prosa).

1) Linkifica la mención ya existente a "Tissot PRX" en la ficha del
   Citizen Tsuyosa (estaba en texto plano).
2) Añade una frase comparativa breve al final de la sección "¿Con qué
   outfit combinarlo?" de cada una de las otras 8 fichas, enlazando a
   un reloj relacionado por categoría (buceo, aventura, vestir...).

Uso: python3 scripts/add_contextual_links.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug de página -> alt text corto usado en los <img> (para que el
# enlace nuevo coincida con el estilo del resto del sitio)
PAGE_NAME = {
    "reloj-baltic-aquascaphe-mk2.html": "Baltic Aquascaphe MK2",
    "reloj-citizen-promaster-eco-drive-diver.html": "Citizen Promaster Eco-Drive Diver",
    "reloj-citizen-tsuyosa.html": "Citizen Tsuyosa",
    "reloj-hamilton-khaki-field-mechanical.html": "Hamilton Khaki Field Mechanical",
    "reloj-orient-bambino-v5.html": "Orient Bambino Versión 5",
    "reloj-seiko-5-sports.html": "Seiko 5 Sports",
    "reloj-seiko-alpinist-spb210.html": "Seiko Prospex Alpinist",
    "reloj-seiko-presage-srpb41.html": "Seiko Presage Cocktail Time",
    "reloj-tissot-prx-quartz.html": "Tissot PRX",
}

# página -> frase adicional (con el <a> ya incluido) que se añade al
# final del párrafo de "¿Con qué outfit combinarlo?"
EXTRA_SENTENCES = {
    "reloj-baltic-aquascaphe-mk2.html": (
        ' Si buscas un buceador con otro enfoque, el '
        '<a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver</a> '
        'es una alternativa igual de resistente pero con tecnología solar.'
    ),
    "reloj-citizen-promaster-eco-drive-diver.html": (
        ' Dentro de los sumergibles de la comparativa, el '
        '<a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a> '
        'es otra opción a tener en cuenta, con un enfoque más vintage y de microbrand.'
    ),
    "reloj-hamilton-khaki-field-mechanical.html": (
        ' Para un perfil de aventura similar pero automático, el '
        '<a href="/reloj-seiko-alpinist-spb210.html">Seiko Prospex Alpinist SPB210</a> '
        'es otra opción con una estética de montaña muy marcada.'
    ),
    "reloj-orient-bambino-v5.html": (
        ' Dentro de los relojes de vestir de la comparativa, el '
        '<a href="/reloj-seiko-presage-srpb41.html">Seiko Presage Cocktail Time</a> '
        'es otra alternativa a considerar, con un enfoque más colorista en el dial.'
    ),
    "reloj-seiko-5-sports.html": (
        ' Si te gusta la robustez diaria pero quieres algo más orientado a montaña, el '
        '<a href="/reloj-seiko-alpinist-spb210.html">Seiko Prospex Alpinist SPB210</a> '
        'comparte familia pero con otro carácter.'
    ),
    "reloj-seiko-alpinist-spb210.html": (
        ' Dentro de la comparativa, es primo cercano del '
        '<a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field Mechanical</a>: '
        'ambos combinan bien con ropa de exterior, aunque con mecanismos muy distintos '
        '(automático con brújula frente a cuerda manual).'
    ),
    "reloj-seiko-presage-srpb41.html": (
        ' Comparte perfil de vestir con el '
        '<a href="/reloj-orient-bambino-v5.html">Orient Bambino Versión 5</a> '
        'de esta comparativa, aunque con un acabado de dial muy distinto.'
    ),
    "reloj-tissot-prx-quartz.html": (
        ' Dentro de los relojes de cuarzo de la comparativa, el '
        '<a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver</a> '
        'es la alternativa más orientada a buceo y uso activo.'
    ),
}

OUTFIT_RE = re.compile(
    r'(<h2>¿Con qué outfit combinarlo\?</h2><p[^>]*>)(.*?)(</p>)'
)

TSUYOSA_FILE = "reloj-citizen-tsuyosa.html"
TSUYOSA_OLD = (
    "un género que también puso de moda el Tissot PRX por las mismas fechas"
)
TSUYOSA_NEW = (
    'un género que también puso de moda el '
    '<a href="/reloj-tissot-prx-quartz.html">Tissot PRX</a> por las mismas fechas'
)


def main() -> None:
    touched = []

    # 1) Linkificar la mención existente en la ficha del Tsuyosa
    path = ROOT / TSUYOSA_FILE
    text = path.read_text(encoding="utf-8")
    if TSUYOSA_OLD in text:
        text = text.replace(TSUYOSA_OLD, TSUYOSA_NEW)
        path.write_text(text, encoding="utf-8")
        touched.append((TSUYOSA_FILE, "mención existente enlazada"))

    # 2) Añadir frase comparativa a las otras 8 fichas
    for name, sentence in EXTRA_SENTENCES.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")

        def repl(m, sentence=sentence):
            return m.group(1) + m.group(2) + sentence + m.group(3)

        new_text, n = OUTFIT_RE.subn(repl, text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            touched.append((name, "frase + enlace añadidos"))
        else:
            print(f"✗ {name}: no se encontró la sección de outfit")

    print(f"\n{len(touched)} página(s) modificadas:")
    for name, what in touched:
        print(f"  {name}: {what}")


if __name__ == "__main__":
    main()
