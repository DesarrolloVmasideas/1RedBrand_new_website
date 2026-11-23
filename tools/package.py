# -*- coding: utf-8 -*-
"""Crea dist/1redbrand-web-AAAAMMDD.zip listo para entregar a IT.
  sitio/     → contenido de la raíz web
  servidor/  → configuración de nginx (y Apache/Netlify por si cambia el hosting)
  LEEME.md   → instrucciones de publicación
Uso: python tools/package.py"""
import os, zipfile, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"tools", "dist", ".git", ".claude", "__pycache__"}
EXCLUDE_FILES = {"README.md", ".gitignore", ".gitattributes", "nginx-1redbrand.conf", "_headers", ".htaccess"}
EXCLUDE_PATHS = {os.path.join("assets", "img", "clients")}  # logos sin uso en el sitio
SERVER_FILES = ["nginx-1redbrand.conf", ".htaccess", "_headers"]

def main():
    stamp = datetime.date.today().strftime("%Y%m%d")
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", f"1redbrand-web-{stamp}.zip")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for base, dirs, files in os.walk(ROOT):
            rel = os.path.relpath(base, ROOT)
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and os.path.normpath(os.path.join(rel, d)) not in EXCLUDE_PATHS]
            for f in files:
                if rel == "." and f in EXCLUDE_FILES:
                    continue
                src = os.path.join(base, f)
                z.write(src, os.path.join("sitio", os.path.normpath(os.path.join(rel, f))))
                n += 1
        for f in SERVER_FILES:
            z.write(os.path.join(ROOT, f), os.path.join("servidor", f))
        z.write(os.path.join(ROOT, "README.md"), "LEEME.md")
    print(f"{out}  ({n} archivos del sitio, {os.path.getsize(out) // 1024} KB)")

if __name__ == "__main__":
    main()
