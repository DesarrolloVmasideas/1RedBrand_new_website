# -*- coding: utf-8 -*-
"""Genera la imagen para redes (Open Graph 1200x630) y los íconos cuadrados.
Uso: python tools/make_images.py"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
RED, INK = (222, 11, 23), (26, 22, 23)
mark = Image.open(os.path.join(IMG, "logo-mark.png")).convert("RGBA")

def fit(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

def font(name, size):
    for p in (os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name), name):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

# --- Open Graph
og = Image.new("RGB", (1200, 630), "white")
m = fit(mark, 430)
og.paste(m, (120, 100), m)
d = ImageDraw.Draw(og)
d.text((470, 175), "1RedBrand", font=font("segoeuisl.ttf", 92), fill=INK)
lines = ["Plataforma de gobernanza y", "automatización de branding", "y marketing"]
for i, ln in enumerate(lines):
    d.text((474, 305 + i * 54), ln, font=font("segoeuil.ttf", 44), fill=(70, 64, 66))
d.line([(474, 500), (1080, 500)], fill=RED, width=4)
og.save(os.path.join(IMG, "og-1redbrand.png"), optimize=True)

# --- íconos cuadrados
for size, name in ((512, "favicon-512.png"), (180, "apple-touch-icon.png")):
    ic = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    m = fit(mark, round(size * 0.8))
    ic.paste(m, ((size - m.width) // 2, (size - m.height) // 2), m)
    ic.convert("RGB").save(os.path.join(IMG, name), optimize=True)
print("ok")
