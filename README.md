# Sitio web 1RedBrand

Sitio estático (HTML, CSS y JavaScript), sin base de datos ni código de servidor. Sustituye al sitio actual de https://www.1redbrand.com.

## Qué se publica

Todo lo que está en la raíz del repositorio, **excepto**:

| No se publica | Qué es |
|---|---|
| `tools/` | Generador de páginas (Python). Solo se usa para editar contenido. |
| `dist/` | Paquetes .zip generados. |
| `.git/`, `.gitignore`, `.claude/` | Control de versiones y archivos de trabajo. |
| `README.md`, `nginx-1redbrand.conf`, `_headers`, `.htaccess` | Documentación y configuración del servidor. |

La forma más simple es usar el paquete: `python tools/package.py` crea `dist/1redbrand-web-AAAAMMDD.zip` con dos carpetas:

- `sitio/`: el contenido que va en la raíz web del dominio.
- `servidor/`: la configuración (`nginx-1redbrand.conf`, más `.htaccess` y `_headers` por si el hosting cambia).

## Publicación en el servidor actual (nginx)

El dominio responde hoy desde **nginx**, que no lee `.htaccess`.

1. **Respaldo.** Respalda la raíz web actual antes de reemplazar nada.
2. **Aviso de privacidad.** Hay que conservar `/en/Aviso_de_Privacidad_1RedBrand.pdf` en la misma ruta, porque el formulario y el pie de página enlazan ahí. Si la carpeta `/en/` del sitio actual se borra, hay que volver a subir ese PDF.
3. **Subir el sitio.** Sube el contenido de `sitio/` a la raíz web, incluida la carpeta oculta `.well-known/`.
4. **Configurar nginx.** Pega el contenido de `servidor/nginx-1redbrand.conf` dentro del bloque `server { }` del dominio con HTTPS. Luego ejecuta `nginx -t` y recarga nginx.
5. **HTTPS y www.** El certificado HTTPS debe estar vigente (por ejemplo, Let's Encrypt). Los bloques de `:80` y del dominio sin www deben redirigir con `return 301 https://www.1redbrand.com$request_uri;`.
6. **URLs anteriores.** Si el sitio actual tenía otras URLs indexadas en Google, hay que redirigirlas con 301 a su equivalente nuevo para no perder posicionamiento. Search Console muestra la lista de URLs indexadas.

### Comprobaciones después de publicar

- `https://www.1redbrand.com/`, `/plataforma/`, `/blog/que-es-software-gobernanza-de-marca/` y una URL inexistente (debe mostrar la página 404).
- `https://www.1redbrand.com/.git/config` y `/tools/build_pages.py` deben responder **404**.
- Cabeceras de seguridad: https://securityheaders.com (objetivo A o A+).
- Datos estructurados: https://search.google.com/test/rich-results
- Dar de alta el dominio en Google Search Console y Bing Webmaster Tools y enviar `https://www.1redbrand.com/sitemap.xml`.

## Publicar con git

Hay dos opciones:

- **A (recomendada).** En tu equipo o en un CI, corre `python tools/package.py` y sube `dist/.../sitio/` al servidor (rsync, SFTP o el panel del hosting).
- **B.** Clona el repositorio en el servidor y apunta la raíz de nginx a esa carpeta. La configuración incluida bloquea `.git/`, `tools/`, `dist/`, los `.md` y los archivos de configuración. Para actualizar, basta con `git pull`.

## Editar contenido

Requisitos: Python 3.10+ y Node.js 18+. Node solo se usa para leer el contenido de la Home. Para regenerar las imágenes, además hace falta Pillow.

| Qué cambiar | Dónde |
|---|---|
| Módulos e industrias (páginas interiores) | `tools/site_data.py` |
| Textos de la Home | `index.html` y `assets/js/content.js` |
| Artículos del blog | `tools/blog_data.py` |
| Títulos, descripciones, datos estructurados, robots.txt, sitemap y llms.txt | `tools/seo.py` |

Después de cualquier cambio:

```bash
python tools/build_pages.py
```

Ese comando regenera todas las páginas interiores, la versión estática de la Home para buscadores, el sitemap, robots.txt, llms.txt y la 404.

Imagen para redes y favicons: `python tools/make_images.py`.

## Pendientes conocidos

- **Formulario.** Hoy abre el cliente de correo del visitante (mailto) hacia hello@1redbrand.com. Para enviarlo desde el servidor:
  - pon `data-endpoint="/ruta"` en el `<form>`; el formulario envía JSON por POST;
  - agrega el captcha en `[data-captcha]` y en `getCaptchaToken()`, en `assets/js/contact-form.js`;
  - suma el dominio del captcha a la Content-Security-Policy.
- **Analítica y anuncios.** Para Google Analytics 4, Google Ads y Meta Pixel hacen falta sus IDs y un aviso de cookies. También hay que sumar sus dominios a la CSP en `nginx-1redbrand.conf`.
- **Versión en inglés.** Hoy el inglés se muestra con un selector dentro de la misma URL. Para SEO en inglés hace falta una versión `/en/` con URLs propias.
