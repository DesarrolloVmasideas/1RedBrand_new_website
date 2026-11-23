# -*- coding: utf-8 -*-
"""SEO, datos estructurados y archivos para buscadores y motores de IA.
Lo usa tools/build_pages.py; no se corre solo."""
import json, html as _html

SITE = "https://www.1redbrand.com"
LASTMOD = "2026-11-23"
OG_IMAGE = "/assets/img/og-1redbrand.png"
ORG_ID, WEB_ID, PLATFORM_ID = SITE + "/#org", SITE + "/#website", SITE + "/#platform"

ORG_DESC = ("1RedBrand es una plataforma modular de gobernanza y automatización de branding y marketing, "
            "desde un negocio independiente hasta organizaciones con varias sedes, marcas o canales.")

# Títulos <title> pensados para búsqueda (≈60 caracteres). Clave = ruta sin barras.
TITLES = {
    "": "1RedBrand: gobernanza y automatización de branding y marketing",
    "plataforma": "Plataforma de gobernanza y automatización de marca | 1RedBrand",
    "industrias": "Industrias: hoteles, franquicias, universidades y más | 1RedBrand",
    "resultados": "Resultados: 402,942 diseños on-brand en un año | 1RedBrand",
    "recursos": "Guías y recursos de gobernanza de marca | 1RedBrand",
    "compania": "Sobre 1RedBrand: plataforma modular de branding y marketing",
    "contacto": "Contacto y demo | 1RedBrand",
    "terminos": "Términos y condiciones de uso | 1RedBrand",
}
MODULE_KW = {
    "branding-automation": "automatización de branding y aprobaciones",
    "digital-marketing-platform": "marketing digital multicanal",
    "ai-digital-concierge": "atención 24/7 con IA",
    "crm": "seguimiento de leads por canal",
    "open-seo": "SEO local y para motores de IA",
    "loyalty-qr": "programa de lealtad con QR",
    "menu-digital": "menús y catálogos digitales",
    "recorridos-360": "visitas virtuales para tu marca",
}
INDUSTRY_KW = {
    "hoteles": "hoteles", "franquicias": "franquicias", "universidades": "universidades",
    "retail": "retail", "corporativos": "corporativos", "automotriz": "el sector automotriz",
}

def url(path):
    path, _, frag = path.partition("#")
    path = path.strip("/")
    u = f"{SITE}/{path}/" if path else f"{SITE}/"
    return u + ("#" + frag if frag else "")

def org():
    return {"@type": "Organization", "@id": ORG_ID, "name": "1RedBrand", "legalName": "1RedBrand LLC",
            "url": SITE + "/", "logo": SITE + "/assets/img/logo-1redbrand.png", "image": SITE + OG_IMAGE,
            "email": "hello@1redbrand.com", "foundingDate": "2015", "slogan": "Empoderamos a las organizaciones para preservar el valor de su identidad de marca, su comunicación con clientes y su fidelización, de manera automatizada, eficiente y a gran escala.", "description": ORG_DESC}

def website():
    return {"@type": "WebSite", "@id": WEB_ID, "url": SITE + "/", "name": "1RedBrand",
            "inLanguage": "es", "publisher": {"@id": ORG_ID}}

def platform(modules):
    return {"@type": "SoftwareApplication", "@id": PLATFORM_ID, "name": "1RedBrand",
            "applicationCategory": "BusinessApplication", "applicationSubCategory": "Brand governance and marketing automation",
            "operatingSystem": "Web", "url": SITE + "/plataforma/", "description": ORG_DESC,
            "publisher": {"@id": ORG_ID},
            "featureList": [f'{m["name"][0]}: {m["promise"][0]}' for m in modules]}

def module_app(m):
    return {"@type": "SoftwareApplication", "@id": url(f"plataforma/{m['id']}") + "#module",
            "name": f'1RedBrand {m["name"][0]}', "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web", "description": m["promise"][0], "isPartOf": {"@id": PLATFORM_ID},
            "publisher": {"@id": ORG_ID}, "featureList": [h[0] for h in m["how"]]}

def webpage(path, title, desc, about_platform=True):
    p = {"@type": "WebPage", "@id": url(path) + "#webpage", "url": url(path), "name": title,
         "description": desc, "inLanguage": "es", "isPartOf": {"@id": WEB_ID}}
    if about_platform:
        p["about"] = {"@id": PLATFORM_ID}
    return p

def breadcrumbs(path, crumbs):
    """crumbs = [(nombre_es, ruta|None), ...]; la última es la página actual."""
    items = []
    for i, (name, href) in enumerate(crumbs, 1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": url(href)})
    return {"@type": "BreadcrumbList", "@id": url(path) + "#breadcrumbs", "itemListElement": items}

def blog_posting(path, p):
    return {"@type": "BlogPosting", "@id": url(path) + "#article", "headline": p["title"][0],
            "description": p["desc"][0], "datePublished": p["date"], "dateModified": p["date"],
            "inLanguage": "es", "mainEntityOfPage": {"@id": url(path) + "#webpage"}, "image": SITE + OG_IMAGE,
            "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "about": {"@id": PLATFORM_ID},
            "timeRequired": f"PT{p['minutes']}M"}

def _plain(s):
    import re
    return re.sub(r"<[^>]+>", "", s)

def faq_page(path, faq):
    return {"@type": "FAQPage", "@id": url(path) + "#faq", "inLanguage": "es",
            "mainEntity": [{"@type": "Question", "name": q[0],
                            "acceptedAnswer": {"@type": "Answer", "text": _plain(a[0])}} for q, a in faq]}

def jsonld(nodes):
    data = {"@context": "https://schema.org", "@graph": nodes}
    s = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{s}</script>'

def head_tags(path, title, desc, nodes, noindex=False, asset_prefix="/"):
    a = lambda s: _html.escape(s, quote=True)
    u = url(path)
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n'
    canon = "" if noindex else f'<link rel="canonical" href="{u}">\n'
    return (f'<title>{a(title)}</title>\n'
            f'<meta name="description" content="{a(desc)}">\n'
            f'{robots}{canon}'
            f'<meta name="referrer" content="strict-origin-when-cross-origin">\n'
            f'<meta name="theme-color" content="#DE0B17">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="1RedBrand">\n'
            f'<meta property="og:locale" content="es_MX">\n'
            f'<meta property="og:locale:alternate" content="en_US">\n'
            f'<meta property="og:title" content="{a(title)}">\n'
            f'<meta property="og:description" content="{a(desc)}">\n'
            f'<meta property="og:url" content="{u}">\n'
            f'<meta property="og:image" content="{SITE}{OG_IMAGE}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="1RedBrand, plataforma de gobernanza y automatización de branding y marketing">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{a(title)}">\n'
            f'<meta name="twitter:description" content="{a(desc)}">\n'
            f'<meta name="twitter:image" content="{SITE}{OG_IMAGE}">\n'
            f'<link rel="icon" href="{asset_prefix}assets/img/favicon-512.png" type="image/png" sizes="512x512">\n'
            f'<link rel="apple-touch-icon" href="{asset_prefix}assets/img/apple-touch-icon.png">\n'
            + ("" if not nodes else jsonld(nodes) + "\n"))

# ------------------------------------------------------------------ archivos raíz
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]

def robots_txt():
    bots = "\n".join(f"User-agent: {b}" for b in AI_BOTS)
    rules = "Allow: /\nDisallow: /tools/\n"
    return (f"# 1RedBrand: buscadores y motores de IA pueden leer todo el sitio público.\n"
            f"{bots}\n{rules}\nUser-agent: *\n{rules}\nSitemap: {SITE}/sitemap.xml\n")

def sitemap_xml(paths):
    rows = []
    for p in paths:
        pr = "1.0" if p == "" else ("0.9" if p in ("plataforma", "industrias") else "0.8" if p.count("/") == 1 else "0.6")
        rows.append(f"  <url><loc>{url(p)}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")

def llms_txt(modules, industries, more, posts=()):
    L = ["# 1RedBrand", "",
         f"> {ORG_DESC} Sus 8 módulos funcionan por separado o integrados en un solo ecosistema.", "",
         "Propósito: empoderamos a las organizaciones para preservar el valor de su identidad de marca, su comunicación con clientes y su fidelización, de manera automatizada, eficiente y a gran escala.",
         "El equipo detrás de 1RedBrand inició en México en el año 2000 como agencia digital. En 2015 creó 1RedBrand para hacer más eficiente la colaboración con sus clientes. En México se comercializa a través de Vmasideas; en Estados Unidos opera desde 2022 como 1RedBrand LLC, registrada en Florida.",
         "Contacto: hello@1redbrand.com", "",
         "## Plataforma", "",
         f"- [Plataforma 1RedBrand]({url('plataforma')}): cómo se integran los 8 módulos en un ciclo de marca, campaña, atención, CRM y lealtad.", "",
         "## Módulos", ""]
    L += [f"- [{m['name'][0]}]({url('plataforma/' + m['id'])}): {m['promise'][0]}" for m in modules]
    L += ["", "## Industrias", ""]
    L += [f"- [{d['name'][0]}]({url('industrias/' + d['id'])}): {d['pain'][0]}" for d in industries]
    L += [f"- {more['name'][0]}: {more['short'][0]}", "",
          "## Resultados", "",
          f"- [Resultados]({url('resultados')}): uno de nuestros clientes generó 402,942 diseños on-brand en un año, cerca de 1,104 adaptaciones al día, sin pasar por diseño central.", "",
          "## Compañía", "",
          f"- [Sobre 1RedBrand]({url('compania')})",
          f"- [Contacto y demo]({url('contacto')})",
          f"- [Recursos]({url('recursos')}): guías por industria y artículos sobre gobernanza de marca.", ""]
    if posts:
        L += ["## Blog", ""] + [f"- [{p['title'][0]}]({url('blog/' + p['slug'])}): {p['desc'][0]}" for p in posts] + [""]
    return "\n".join(L)

SECURITY_TXT = f"""Contact: mailto:hello@1redbrand.com
Expires: 2027-11-23T00:00:00.000Z
Preferred-Languages: es, en
Canonical: {SITE}/.well-known/security.txt
"""
