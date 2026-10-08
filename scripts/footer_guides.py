#!/usr/bin/env python3
"""Sustituye el enlace único 'Guías de compra' del footer por las 4 guías (idempotente)."""
import glob
OLD = '<a href="/guia-relojes-automaticos-entrada.html">Guías de compra</a>'
NEW = ('<a href="/guia-relojes-automaticos-entrada.html">Guía: automáticos de entrada</a>\n'
       '      <a href="/guia-mejores-relojes-buceo.html">Guía: relojes de buceo</a>\n'
       '      <a href="/guia-tipos-de-movimiento.html">Guía: tipos de movimiento</a>\n'
       '      <a href="/guia-cuando-pagar-mas-reloj.html">Guía: cuándo pagar más</a>')
n = 0
for f in glob.glob("*.html"):
    t = open(f, encoding="utf-8").read()
    if OLD in t:
        open(f, "w", encoding="utf-8").write(t.replace(OLD, NEW)); n += 1
print(n, "páginas")
