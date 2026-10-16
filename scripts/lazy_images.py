#!/usr/bin/env python3
"""Añade loading=lazy y decoding=async a todas las <img> salvo la primera de cada página (posible LCP). Idempotente."""
import re, glob
n = 0
for f in sorted(glob.glob("*.html")):
    t = open(f, encoding="utf-8").read(); first = [True]
    def fix(m):
        tag = m.group(0)
        if first[0]:
            first[0] = False; return tag
        if "loading=" in tag: return tag
        return tag[:-1].rstrip() + ' loading="lazy" decoding="async">'
    t2 = re.sub(r"<img\b[^>]*>", fix, t)
    if t2 != t: open(f, "w", encoding="utf-8").write(t2); n += 1
print(n, "páginas")
