#!/usr/bin/env python3
"""Añade/actualiza <lastmod> en sitemap.xml con la fecha del último commit de cada página (idempotente)."""
import re, subprocess
from pathlib import Path
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parent.parent
sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
def d(path):
    r = subprocess.run(["git","log","-1","--format=%cs","--",path],cwd=ROOT,capture_output=True,text=True).stdout.strip()
    return r
def fix(m):
    loc = m.group(1); path = urlparse(loc).path.lstrip("/") or "index.html"
    date = d(path)
    return f"<url><loc>{loc}</loc><lastmod>{date}</lastmod></url>" if date else m.group(0)
t2 = re.sub(r"<url><loc>([^<]+)</loc>(?:<lastmod>[^<]*</lastmod>)?</url>", fix, t)
if t2 != t: sm.write_text(t2, encoding="utf-8"); print("✓ lastmod actualizado")
