# -*- coding: utf-8 -*-
"""Recorta los logos de clientes de la lámina fuente y los exporta como PNG monocromáticos
(tinta negra con transparencia) en assets/img/clients/. El color final lo da el CSS.
Uso: python tools/make_logos.py   (requiere Pillow)"""
import os, statistics
from PIL import Image
from clients_data import SOURCE, CLIENTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "clients")

def corner_bg(g):
    w, h = g.size; px = g.load(); k = 4
    vals = [px[x, y] for (cx, cy) in ((0, 0), (w - k, 0), (0, h - k), (w - k, h - k))
            for x in range(cx, cx + k) for y in range(cy, cy + k)]
    return statistics.median(vals)

def main():
    sheet = Image.open(SOURCE).convert("L")
    os.makedirs(OUT, exist_ok=True)
    for slug, name, box, *cut in CLIENTS:
        g = sheet.crop(box)
        if cut:
            bg = cut[0]
        else:
            bg = corner_bg(g)
            bg = bg if bg > 200 else 255      # fondo claro (AHETA) se vuelve transparente
            bg = min(bg, 250) - 6
        ink = g.getextrema()[0]
        span = max(1, bg - ink)
        a = g.point(lambda v: 0 if v >= bg else min(255, int((bg - v) / span * 255)))
        a = a.point(lambda v: 0 if v < 22 else v)
        bb = a.getbbox()
        a = a.crop(bb)
        img = Image.new("RGBA", a.size, (0, 0, 0, 0))
        img.putalpha(a)
        img.save(os.path.join(OUT, f"{slug}.png"), optimize=True)
        print(f"{slug:18} {a.size}")

if __name__ == "__main__":
    main()
