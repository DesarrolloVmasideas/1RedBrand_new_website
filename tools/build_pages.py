# -*- coding: utf-8 -*-
"""Genera las páginas interiores estáticas de 1RedBrand.
Uso:  python tools/build_pages.py   (desde la raíz del proyecto)
Edita el contenido en tools/site_data.py y vuelve a correr el script."""
import os, re, sys, json, struct, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from site_data import MODULES, INDUSTRIES, STEPS, GUIDES, MORE
from blog_data import POSTS
from legal_data import TERMS, PRIVACY
from clients_data import CLIENTS
import seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "26"
MOD = {m["id"]: m for m in MODULES}
IND = {d["id"]: d for d in INDUSTRIES}

def B(pair, en=None):
    es, en = (pair if en is None else (pair, en))
    if es == en:
        return es
    return f'<span lang="es">{es}</span><span lang="en">{en}</span>'

def esc_attr(s):
    return s.replace('"', "&quot;")

# --------------------------------------------------------------- piezas comunes
NAV = [("plataforma", ("Plataforma", "Platform")), ("industrias", ("Industrias", "Industries")),
       ("resultados", ("Resultados", "Results")), ("recursos", ("Recursos", "Resources")),
       ("compania", ("Compañía", "Company"))]

CHEV = '<svg class="nav__chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5"/></svg>'

def modules_dd(section, current_id=None):
    """Menú desplegable "Módulos" (patrón de divulgación: botón + panel)."""
    items = []
    for m in MODULES:
        cur = ' aria-current="page"' if m["id"] == current_id else ""
        items.append(
            f'<li><a class="dd__link" href="/plataforma/{m["id"]}/"{cur}>'
            f'<svg class="dd__glyph" viewBox="0 0 100 100" aria-hidden="true"><path d="{m["glyph"]}"/></svg>'
            f'<span class="dd__name">{B(m["name"])}</span><span class="dd__p">{B(m["promise"])}</span></a></li>')
    cls = " is-current" if section == "modulos" else ""
    return (f'<div class="nav__dd" data-dd>\n'
            f'      <button class="nav__btn{cls}" type="button" aria-expanded="false" aria-controls="dd-modulos">{B("Módulos", "Modules")}{CHEV}</button>\n'
            f'      <div class="dd" id="dd-modulos">\n'
            f'        <ul class="dd__grid">{"".join(items)}</ul>\n'
            f'        <div class="dd__foot"><span>{B("8 módulos que funcionan por separado o integrados.", "8 modules that work on their own or together.")}</span>'
            f'<a class="link" href="/plataforma/">{B("Ver cómo se conectan", "See how they connect")}</a></div>\n'
            f'      </div>\n'
            f'    </div>')

def nav_html(section, current_id=None):
    out = []
    for k, v in NAV:
        cur = ' aria-current="page"' if k == section else ""
        out.append(f'<a href="/{k}/"{cur}>{B(v)}</a>')
        if k == "plataforma":
            out.append(modules_dd(section, current_id))
    inner = "\n    ".join(out)
    return f'<nav class="nav" id="nav" aria-label="Principal">\n    {inner}\n  </nav>'

def header(section, current_id=None):
    return f'''<a class="skip" href="#main">{B("Saltar al contenido", "Skip to content")}</a>
<header class="site-header">
  <a class="brand" href="/" aria-label="1RedBrand, inicio">
    <img src="/assets/img/logo-mark.png" alt="" width="22" height="32">
    <span class="brand__word">one red brand</span>
  </a>
  {nav_html(section, current_id)}
  <div class="header__actions">
    <button class="lang" type="button" data-lang-toggle aria-label="Cambiar idioma / Change language">
      <span class="lang__opt" data-v="es">ES</span><span class="lang__opt" data-v="en">EN</span>
    </button>
    <a class="btn btn--small" href="/contacto/">{B("Agenda una demo", "Book a demo")}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" data-burger>
      <span></span><span></span><span class="sr">{B("Menú", "Menu")}</span>
    </button>
  </div>
</header>'''

def footer():
    mods = "".join(f'<li><a href="/plataforma/{m["id"]}/">{B(m["name"])}</a></li>' for m in MODULES)
    inds = "".join(f'<li><a href="/industrias/{d["id"]}/">{B(d["name"])}</a></li>' for d in INDUSTRIES)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <img src="/assets/img/logo-1redbrand.png" alt="one red brand" class="footer__logo" width="891" height="822">
      <p class="footer__cat">Branding &amp; Marketing Governance and Automation Platform</p>
    </div>
    <div class="footer__cols">
      <div><h3>{B("Plataforma", "Platform")}</h3><ul>{mods}</ul></div>
      <div><h3>{B("Industrias", "Industries")}</h3><ul>{inds}</ul></div>
      <div><h3>{B("Recursos", "Resources")}</h3><ul>
        <li><a href="/recursos/#blog">Blog</a></li>
        <li><a href="/recursos/#guias">{B("Guías", "Guides")}</a></li></ul></div>
      <div><h3>{B("Compañía", "Company")}</h3><ul>
        <li><a href="/compania/">{B("Nosotros", "About")}</a></li>
        <li><a href="/contacto/">{B("Contacto", "Contact")}</a></li></ul></div>
    </div>
    <div class="footer__legal">
      <span>© 2026 1RedBrand LLC · <a href="https://www.1redbrand.com/en/Aviso_de_Privacidad_1RedBrand.pdf" target="_blank" rel="noopener">{B("Aviso de privacidad", "Privacy notice")}</a> · <a href="/terminos/">{B("Términos y condiciones", "Terms and conditions")}</a></span>
      <button class="lang lang--foot" type="button" data-lang-toggle aria-label="Cambiar idioma / Change language">
        <span class="lang__opt" data-v="es">Español</span><span class="lang__opt" data-v="en">English</span>
      </button>
    </div>
  </div>
</footer>'''

def crumbs_from(body):
    """Lee la ruta de migas del hero para el BreadcrumbList (nombre en español + ruta)."""
    m = re.search(r'<ol class="crumbs">(.*?)</ol>', body, re.S)
    out = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1) if m else "", re.S):
        h = re.search(r'href="([^"]+)"', li)
        es = re.search(r'<span lang="es">(.*?)</span>', li)
        name = es.group(1) if es else re.sub(r"<[^>]+>", "", li)
        out.append((name.strip(), h.group(1).strip("/") if h else None))
    return out

def seo_title(path, title):
    if path in seo.TITLES:
        return seo.TITLES[path]
    kind, _, pid = path.partition("/")
    if kind == "plataforma":
        return f"{title}: {seo.MODULE_KW[pid]} | 1RedBrand"
    if kind == "industrias":
        return f"Branding y marketing para {seo.INDUSTRY_KW[pid]} | 1RedBrand"
    return f"{title} | 1RedBrand"

def page(path, title, desc, section, body, extra_js="", current_id=None, nodes=None, noindex=False, seo_title_override=None):
    t = seo_title_override or seo_title(path, title)
    graph = [seo.org(), seo.website(), seo.webpage(path, t, desc)]
    cr = crumbs_from(body)
    if cr:
        graph.append(seo.breadcrumbs(path, [(n, path if h is None else h) for n, h in cr]))
    graph += nodes or []
    if len(desc) > 160:
        print(f"  aviso: descripción de /{path}/ tiene {len(desc)} caracteres")
    html = f'''<!doctype html>
<html lang="es" data-lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="/assets/js/lang.js?v={V}"></script>
{seo.head_tags(path, t, desc, None if noindex else graph, noindex=noindex)}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css?v={V}">
<link rel="stylesheet" href="/assets/css/pages.css?v={V}">
</head>
<body>
{header(section, current_id)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/nav.js?v={V}"></script>
<script src="/assets/js/page.js?v={V}"></script>{extra_js}
</body>
</html>
'''
    out = os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return path

def glyph_svg(d, cls="ph__glyph"):
    p = lambda c: f'<path class="{c}" d="{d}" pathLength="1"/>'
    return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true">{p("t-shadow")}{p("t-main")}{p("t-hi")}</svg>'

def small_glyph(d):
    return f'<svg viewBox="0 0 100 100" aria-hidden="true"><path d="{d}"/></svg>'

def hero(crumbs, kicker, title, lede, ctas, art, to=""):
    cr = "".join(f'<li><a href="{h}">{B(t)}</a></li>' if h else f'<li aria-current="page">{B(t)}</li>' for t, h in crumbs)
    ct = "".join(f'<a class="btn{" btn--ghost" if i else ""}" href="{h}">{B(t)}</a>' for i, (t, h) in enumerate(ctas))
    mark_cls = " ph--mark" if art == "mark" else ""
    art_html = ('<img class="ph__mark" src="/assets/img/logo-mark.png" alt="" width="528" height="781">'
                if art == "mark" else glyph_svg(art))
    return f'''<section class="ph{mark_cls}{" ph--to-" + to if to else ""}">
  <div class="ph__copy">
    <nav aria-label="Ruta"><ol class="crumbs">{cr}</ol></nav>
    <p class="kicker">{B(kicker)}</p>
    <h1 class="ph__title">{B(title)}</h1>
    <p class="ph__lede">{B(lede)}</p>
    <div class="ph__ctas">{ct}</div>
  </div>
  <div class="ph__art" aria-hidden="true"><span class="ph__blob"></span>{art_html}</div>
</section>'''

def final(title, primary, secondary=(("Hablar con ventas", "Talk to sales"), "/contacto/")):
    return f'''<section class="final">
  <div class="wrap final__wrap">
    <h2>{B(title)}</h2>
    <div class="final__ctas" data-tail>
      <a class="btn btn--big" href="{primary[1]}">{B(primary[0])}</a>
      <a class="btn btn--ghost btn--big" href="{secondary[1]}">{B(secondary[0])}</a>
    </div>
  </div>
</section>'''

READY = ("Conversemos sobre tu marca.", "Let's talk about your brand.")
HOME = (("Inicio", "Home"), "/")

def mcard(m, more=("Ver el módulo", "See the module")):
    return f'''<a class="mcard" href="/plataforma/{m["id"]}/">
      {small_glyph(m["glyph"])}
      <span class="mcard__name">{B(m["name"])}</span>
      <span class="mcard__p">{B(m["promise"])}</span>
      <span class="mcard__more">{B(more)}</span>
    </a>'''

def tl_item(node_html, name, text, href=None, more=None):
    tag = "a" if href else "div"
    h = f' href="{href}"' if href else ""
    mr = f'<span class="tl-more">{B(more)}</span>' if more else ""
    return f'''<{tag} class="tl-item"{h}>
        <span class="tl-node" data-node>{node_html}</span>
        <span class="tl-body"><span class="tl-name">{B(name)}</span><span class="tl-text">{B(text)}</span>{mr}</span>
      </{tag}>'''

# --------------------------------------------------------------- mockups
def L(es, en):
    return B(es, en)

def mock(kind, m):
    bar = f'<div class="mock__bar"><i></i><i></i><i></i><b>{B(m["name"])}</b></div>'
    if kind == "branding":
        body = f'''<div class="split">
          <div class="poster"><img src="/assets/img/logo-mark.png" alt=""><strong>{L("Gran apertura", "Grand opening")}<br>Sucursal Centro</strong><small>{L("Sábado 10:00", "Saturday 10:00")}</small></div>
          <div style="display:grid;gap:.5rem;align-content:start">
            <div class="field is-locked"><small>{L("Logotipo", "Logo")} <span class="lock"></span></small>{L("Bloqueado", "Locked")}</div>
            <div class="field is-locked"><small>{L("Colores", "Colors")} <span class="lock"></span></small>{L("Paleta oficial", "Official palette")}</div>
            <div class="field"><small>{L("Sede", "Location")}</small>Sucursal Centro</div>
            <div class="field"><small>{L("Fecha", "Date")}</small>{L("Sábado 10:00", "Saturday 10:00")}</div>
          </div></div>
          <div class="row"><span>{L("Exportar", "Export")}</span><span><span class="chip">PDF</span> <span class="chip">PNG</span> <span class="chip chip--red">{L("Redes", "Social")}</span></span></div>'''
    elif kind == "marketing":
        days = [("Lun", "Mon"), ("Mar", "Tue"), ("Mié", "Wed"), ("Jue", "Thu"), ("Vie", "Fri")]
        ev = [[("Orgánico", "Organic", "")], [("Pauta Meta", "Meta ads", "r")], [], [("Lanzamiento", "Launch", "r"), ("Orgánico", "Organic", "")], [("Pauta Google", "Google ads", "")]]
        cal = "".join(f'<span>{L(*d)}{"".join(f"<em class={chr(34)}{c}{chr(34)}>{L(a, b)}</em>" for a, b, c in e)}</span>' for d, e in zip(days, ev))
        body = f'''<div class="row"><b>{L("Calendario por región", "Calendar by region")}</b><span class="chip chip--blush">{L("Región Norte", "North region")}</span></div>
          <div class="cal">{cal}</div>
          <div class="row"><small>{L("Leads por campaña", "Leads by campaign")}</small><small>{L("Conectado al CRM", "Connected to CRM")}</small></div>
          <div class="bars"><i style="height:40%"></i><i style="height:62%"></i><i class="on" style="height:88%"></i><i style="height:55%"></i><i style="height:70%"></i><i style="height:46%"></i></div>'''
    elif kind == "concierge":
        body = f'''<div class="row"><b>WhatsApp</b><span class="chip chip--blush">{L("23:48 · fuera de horario", "11:48 pm · after hours")}</span></div>
          <div class="bubble-in">{L("¿Tienen habitación para el viernes?", "Any rooms for Friday?")}</div>
          <div class="bubble-out">{L("¡Hola! Sí, tenemos disponibilidad el viernes. ¿Para cuántas personas?", "Hi! Yes, we have availability on Friday. For how many guests?")}</div>
          <div class="bubble-in">{L("Dos adultos.", "Two adults.")}</div>
          <div class="bubble-out">{L("Listo. Te comparto las opciones y puedo apartar tu reserva.", "Done. Here are the options, and I can hold your booking.")}</div>
          <div class="row"><small>{L("Registrado en CRM", "Logged in CRM")}</small><span class="chip">{L("Escalar a humano", "Hand off to a human")}</span></div>'''
    elif kind == "crm":
        rows = [("Laura M.", "WhatsApp", ("Sede Centro", "Downtown")), ("Jorge P.", "Meta Ads", ("Sede Norte", "North")),
                ("Ana R.", ("Sitio web", "Website"), ("Sede Sur", "South")), ("Luis G.", "Concierge", ("Sede Centro", "Downtown"))]
        rr = "".join(f'<div class="row"><span>{n}<br><small>{L(*s)}</small></span><span class="chip{" chip--red" if i == 1 else ""}">{L(*src) if isinstance(src, tuple) else src}</span></div>' for i, (n, src, s) in enumerate(rows))
        body = f'''<div class="row"><b>{L("Leads de hoy", "Today's leads")}</b><span class="chip chip--blush">{L("Con origen", "With source")}</span></div>{rr}'''
    elif kind == "seo":
        body = f'''<div class="row"><span>🔍&nbsp; {L("hotel cerca de mí", "hotel near me")}</span><small>{L("Local", "Local")}</small></div>
          <div class="serp"><small>tumarca.com › sede-centro</small><a href="#" tabindex="-1">{L("Tu Marca Sede Centro · Reserva directa", "Your Brand Downtown · Book direct")}</a><span style="color:var(--ink-2);font-size:.82rem">{L("Horarios, ubicación y recorrido virtual, actualizados desde un panel.", "Hours, location and virtual tour, updated from one dashboard.")}</span></div>
          <div class="ai-card"><small>{L("Respuesta de asistente de IA", "AI assistant answer")}</small><br>{L("Según su sitio oficial, Tu Marca Sede Centro abre todos los días y ofrece estacionamiento.", "According to its official site, Your Brand Downtown is open every day and offers parking.")}</div>
          <div class="row"><small>{L("Fichas sincronizadas", "Listings in sync")}</small><span class="chip chip--red">{L("12 de 12 sedes", "12 of 12 locations")}</span></div>'''
    elif kind == "loyalty":
        body = f'''<div class="split" style="align-items:center">
            <div style="display:grid;place-items:center;gap:.5rem"><span class="qr-big"></span><small style="color:var(--ink-2)">{L("Escanea en caja", "Scan at checkout")}</small></div>
            <div style="display:grid;gap:.5rem">
              <div class="field"><small>{L("Nivel", "Tier")}</small>{L("Oro", "Gold")}</div>
              <div class="field"><small>{L("Puntos", "Points")}</small>1,240</div>
              <div class="meter"><i></i></div><small style="color:var(--ink-2)">{L("Faltan 260 para Platino", "260 to Platinum")}</small>
            </div></div>
          <div class="row"><small>{L("Campaña por nivel", "Campaign by tier")}</small><span class="chip chip--red">{L("Oro: 2x1 en café", "Gold: 2-for-1 coffee")}</span></div>'''
    elif kind == "menu":
        items = [(("Café de olla", "Clay-pot coffee"), "$45"), (("Chilaquiles verdes", "Green chilaquiles"), "$120"),
                 (("Pan dulce", "Sweet bread"), "$28"), (("Jugo natural", "Fresh juice"), "$55")]
        ii = "".join(f'<div class="row"><span>{L(*n)}</span><b>{p}</b></div>' for n, p in items)
        body = f'''<div class="phone"><div class="row" style="background:var(--red);color:#fff"><b>{L("Desayunos", "Breakfast")}</b><small style="color:#ffe1e3">{L("Actualizado hoy", "Updated today")}</small></div>{ii}</div>
          <div class="row"><small>{L("Lo más consultado", "Most viewed")}</small><span class="chip chip--blush">{L("Chilaquiles verdes", "Green chilaquiles")}</span></div>'''
    else:  # tours
        body = f'''<div class="pano"><span class="hot" style="left:22%;top:56%"></span><span class="hot" style="left:63%;top:44%"></span><span class="hot" style="left:80%;top:64%"></span><span class="compass">360°</span></div>
          <div class="row"><span>{L("Lobby · Sede Centro", "Lobby · Downtown")}</span><span><span class="chip">Google</span> <span class="chip chip--red">{L("Sitio", "Website")}</span></span></div>'''
    return f'<div class="mock-stage"><div class="mock">{bar}<div class="mock__body">{body}</div></div></div>'

# --------------------------------------------------------------- páginas de módulo
def module_page(m):
    pains = "".join(f"<li>{B(p)}</li>" for p in m["pains"])
    steps = "".join(f'<li class="how__step"><span class="how__node" data-node>{i + 1}</span><p class="how__t">{B(s)}</p></li>' for i, s in enumerate(m["how"]))
    rel = "".join(mcard(MOD[r]) for r in m["related"])
    used = [d for d in INDUSTRIES if m["id"] in d["mods"]]
    used_html = "".join(f'<li><a class="link" href="/industrias/{d["id"]}/">{B(d["name"])}</a></li>' for d in used)
    used_html += f'<li><a class="link link--more" href="/industrias/">{B(("Ver todas las industrias", "See all industries"))}</a></li>'
    body = f'''{hero([HOME, (("Plataforma", "Platform"), "/plataforma/"), (m["name"], None)], m["name"], m["promise"],
        ("Un módulo de 1RedBrand, la plataforma modular de gobernanza y automatización de branding y marketing. Funciona por sí solo o integrado con los otros siete.",
         "A 1RedBrand module, the modular branding and marketing governance and automation platform. It works on its own or integrated with the other seven."),
        [(m["cta"], "/contacto/"), (("Ver los 8 módulos", "See the 8 modules"), "/plataforma/#modulos")], m["glyph"], to="ink")}

<section class="pains">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Lo que pasa hoy sin este módulo.", "What happens today without this module.")}</h2></div>
    <ul class="pains__list">{pains}</ul>
  </div>
</section>

<section class="how">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Cómo funciona.", "How it works.")}</h2></div>
    <ol class="how__list" data-node-group>{steps}</ol>
  </div>
</section>

<section class="see">
  <div class="wrap see__grid">
    <div>
      <h2 class="sec-head" style="margin:0"><span style="font-size:clamp(1.9rem,5.4vw,3.2rem);display:block;line-height:1.05">{B("Así se ve en la plataforma.", "This is how it looks in the platform.")}</span></h2>
      <p class="see__note">{B("Vista ilustrativa con datos de ejemplo.", "Illustrative view with sample data.")}</p>
    </div>
    {mock(m["mock"], m)}
  </div>
</section>

<section class="rel">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Funciona mejor con.", "Works best with.")}</h2></div>
    <div class="cards">{rel}</div>
    <div class="usedin"><p class="usedin__l">{B("Se usa en", "Used in")}</p><ul class="usedin__list">{used_html}</ul></div>
  </div>
</section>

{final(READY, (m["cta"], "/contacto/"))}'''
    name = m["name"][0]
    return page(f"plataforma/{m['id']}", name, f"{name}: {m['promise'][0]} Un módulo de 1RedBrand.", "modulos", body, current_id=m["id"], nodes=[seo.module_app(m)])

# --------------------------------------------------------------- páginas de industria
def industry_page(d):
    mods = "".join(tl_item(small_glyph(MOD[k]["glyph"]), MOD[k]["name"], MOD[k]["promise"], f"/plataforma/{k}/", ("Ver el módulo", "See the module")) for k in d["mods"])
    clients = ""
    if d["clients"]:
        names = "".join(f"<li>{c}</li>" for c in d["clients"])
        clients = f'''
<section class="clients">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:0">
      <h2>{B("Ya gobiernan su marca con 1RedBrand.", "Already governing their brand with 1RedBrand.")}</h2>
    </div>
    <ul class="clients__names">{names}</ul>
  </div>
</section>'''
    body = f'''{hero([HOME, (("Industrias", "Industries"), "/industrias/"), (d["name"], None)], d["name"], d["pain"], d["lede"],
        [(d["cta"], "/contacto/"), (("Ver los módulos", "See the modules"), "#modulos")], d["glyph"])}

<section class="sec" id="modulos">
  <div class="wrap">
    <div class="sec-head"><h2>{B(d.get("mods_title", ("Los módulos que más pesan aquí.", "The modules that matter most here.")))}</h2>
      <p class="lede">{B(d.get("mods_lede", ("Integrados entre sí: lo que produce uno lo aprovecha el siguiente.", "Integrated with each other: what one produces, the next one uses.")))}</p></div>
    <div class="threadlist" data-node-group>{mods}</div>
    <div class="usedin"><ul class="usedin__list"><li><a class="link" href="/plataforma/">{B("Cómo se conectan los módulos", "How the modules connect")}</a></li><li><a class="link" href="/resultados/">{B("Ver resultados", "See results")}</a></li></ul></div>
  </div>
</section>
{clients}
{final(READY, (d["cta"], "/contacto/"))}'''
    name = d["name"][0]
    desc = d["lede"][0] if len(d["lede"][0]) <= 160 else f"1RedBrand para {name.lower()}: {d['pain'][0]}"
    return page(f"industrias/{d['id']}", f"{name}", desc, "industrias", body)

def industries_index():
    items = "".join(tl_item(small_glyph(d["glyph"]), d["name"], d["pain"], f"/industrias/{d['id']}/", (f"Ver {d['name'][0]}", f"See {d['name'][1]}")) for d in INDUSTRIES)
    items += tl_item("<b>+</b>", MORE["name"], MORE["short"], "/contacto/", MORE["cta"])
    body = f'''{hero([HOME, (("Industrias", "Industries"), None)], ("Industrias", "Industries"),
        ("Cada industria tiene retos de marca distintos.", "Every industry has different brand challenges."),
        ("Desde un negocio independiente hasta organizaciones con muchas sedes. Elige tu industria para ver cómo se aplica la plataforma.",
         "From a single independent business to organizations with many locations. Pick your industry to see how the platform applies."),
        [(("Agenda una demo", "Book a demo"), "/contacto/"), (("Ver la plataforma", "See the platform"), "/plataforma/")], "mark")}

<section class="sec">
  <div class="wrap">
    <div class="threadlist" data-node-group>{items}</div>
  </div>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    return page("industrias", "Industrias", "1RedBrand en hoteles, franquicias, universidades, retail, corporativos y automotriz: desde un negocio independiente hasta organizaciones con muchas sedes.", "industrias", body)

# --------------------------------------------------------------- plataforma
def platform_page():
    steps = "".join(tl_item(f"<b>{i + 1}</b>", s, m) for i, (s, m) in enumerate(STEPS))
    cards = "".join(mcard(m) for m in MODULES)
    body = f'''{hero([HOME, (("Plataforma", "Platform"), None)], ("Plataforma", "Platform"), ("Una plataforma modular para tu marca.", "A modular platform for your brand."),
        ("Un ciclo que aprende: los módulos comparten información entre sí: la marca aprobada guía cada campaña y cada conversación, y los resultados orientan el siguiente plan.",
         "A cycle that learns: the modules share information with each other: the approved brand guides every campaign and conversation, and the results shape the next plan."),
        [(("Agenda una demo", "Book a demo"), "/contacto/"), (("Ver los 8 módulos", "See the 8 modules"), "#modulos")],
        "M50,14 C72,14 86,30 86,50 C86,72 70,86 50,86 C28,86 14,70 14,50 C14,33 25,20 40,15", to="ink")}

<section class="sec sec--ink curved">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Cinco pasos, un solo ciclo.", "Five steps, one cycle.")}</h2></div>
    <div class="threadlist" data-node-group>{steps}</div>
    <p class="loop-note">{B("El paso 5 alimenta de nuevo el paso 1: lo que aprendes de tus clientes vuelve al plan de marca.", "Step 5 feeds back into step 1: what you learn from customers goes back into the brand plan.")}</p>
  </div>
</section>

<section class="rel" id="modulos">
  <div class="wrap">
    <div class="sec-head"><h2>{B("8 módulos, un solo ecosistema de marca.", "8 modules, one brand ecosystem.")}</h2>
      <p class="lede">{B("Cada módulo funciona por sí solo y se integra con los demás. Empieza con el que necesitas hoy y suma otros cuando tu operación lo pida.", "Each module works on its own and integrates with the rest. Start with the one you need today and add others as your operation grows.")}</p></div>
    <div class="cards cards--8" data-rail>{cards}</div>
    <div class="rail-ui"><p class="hint">{B("Desliza o usa los puntos para recorrer los 8 módulos", "Swipe or use the dots to browse the 8 modules")}</p><div class="rail-dots" data-rail-dots></div></div>
  </div>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    return page("plataforma", "Plataforma", "1RedBrand: plataforma modular de gobernanza y automatización de branding y marketing, con 8 módulos que funcionan por separado o integrados.", "plataforma", body, nodes=[seo.platform(MODULES)])


# --------------------------------------------------------------- carrusel de clientes (Home y Resultados)
def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])

LOGO_SCALE = {"mottoz": 0.82, "zamora-live": 0.82}  # logos de bloque sólido pesan más a la vista

def clients_bar(sid="clientes", extra=""):
    """Barra de logotipos en movimiento continuo. Solo logos: sin módulos ni casos."""
    items = []
    for slug, name, *_ in CLIENTS:
        w, h = png_size(os.path.join(ROOT, "assets", "img", "clients", f"{slug}.png"))
        dh = round(min(66, 86 / (w / h) ** 0.55) * LOGO_SCALE.get(slug, 1))
        items.append((slug, name, w, h, dh))
    def ul(hidden):
        lis = "".join(f'<li><img src="/assets/img/clients/{slug}.png?v={V}" alt="{"" if hidden else esc_attr(name)}" width="{w}" height="{h}" style="--h:{dh}" loading="lazy" decoding="async"></li>'
                      for slug, name, w, h, dh in items)
        hid = ' aria-hidden="true"' if hidden else ""
        return f'<ul class="marquee__list"{hid}>{lis}</ul>'
    title = B("Organizaciones que trabajan con 1RedBrand.", "Organizations that work with 1RedBrand.")
    return (f'<section class="logobar" id="{sid}" aria-labelledby="{sid}-t"{extra}>\n'
            f'  <div class="wrap"><h2 class="logobar__t" id="{sid}-t">{title}</h2></div>\n'
            f'  <div class="marquee">{ul(False)}{ul(True)}</div>\n</section>')

# --------------------------------------------------------------- resultados
def results_page():
    inds = "".join(f'<li><a class="link" href="/industrias/{d["id"]}/">{B(d["name"])}</a></li>' for d in INDUSTRIES)
    inds += f'<li><a class="link link--more" href="/contacto/">{B(MORE["name"])}</a></li>'
    body = f'''{hero([HOME, (("Resultados", "Results"), None)], ("Resultados", "Results"),
        ("Lo que cambia cuando la marca se gestiona desde una sola plataforma.", "What changes when the brand is managed from one platform."),
        ("Cuando cada pieza nace de un diseño aprobado, la producción crece y la marca se mantiene consistente en cada canal y ubicación.",
         "When every piece starts from an approved design, output grows and the brand stays consistent across every channel and location."),
        [(("Agenda una demo", "Book a demo"), "/contacto/"), (("Ver la plataforma", "See the platform"), "/plataforma/")], "mark", to="ink")}

<section class="sec sec--ink curved">
  <div class="wrap figs">
    <div class="fig">
      <p class="fig__n" data-count="402942" aria-label="402,942">402,942</p>
      <p class="fig__l">{B("diseños on-brand generados en un año por uno de nuestros clientes.", "on-brand designs generated in one year by one of our clients.")}</p>
    </div>
    <div style="display:grid;gap:2.4rem">
      <div class="fig"><p class="fig__n" style="font-size:clamp(2.6rem,9vw,4.4rem)" data-count="1104" aria-label="1,104">1,104</p>
        <p class="fig__l">{B("adaptaciones al día, en promedio, sin pasar por diseño central.", "adaptations a day, on average, without going through central design.")}</p></div>
      <div class="fig"><p class="fig__n" style="font-size:clamp(2.6rem,9vw,4.4rem)">95–98%</p>
        <p class="fig__l">{B("de retención histórica de clientes.", "historical client retention.")}</p></div>
    </div>
  </div>
</section>

{clients_bar()}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Dónde trabajamos.", "Where we work.")}</h2>
      <p class="lede">{B("Negocios independientes y organizaciones con varias sedes en estas industrias y otras: grupos hospitalarios, plazas comerciales y más.", "Independent businesses and multi-location organizations in these industries and others: hospital groups, shopping centers and more.")}</p></div>
    <ul style="display:flex;flex-wrap:wrap;gap:1rem 2rem;font-size:1.3rem;font-weight:300">{inds}</ul>
  </div>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    return page("resultados", "Resultados", "Resultados de 1RedBrand: 402,942 diseños on-brand generados en un año por uno de nuestros clientes.", "resultados", body)

# --------------------------------------------------------------- recursos
def res_card(kind, title, desc, href=None, more_label=None):
    tag, h = ("a", f' href="{href}"') if href else ("div", "")
    if more_label:
        more = f'<span class="res__more">{B(more_label)}</span>'
    else:
        more = f'<span class="res__more">{B("Leer", "Read")}</span>' if href else f'<span class="res__more soon">{B("Próximamente", "Coming soon")}</span>'
    return f'''<li><{tag} class="res__card"{h}>
        <span class="res__type">{B(kind)}</span>
        <span class="res__title">{B(title)}</span>
        <span class="res__desc">{B(desc)}</span>{more}
      </{tag}></li>'''

def resources_page():
    guides = "".join(res_card(("Guía por industria", "Industry guide"), GUIDES[d["id"]],
        (f"Para {d['name'][0].lower()}: qué bloquear, qué liberar y cómo medirlo. Guía próximamente.", f"For {d['name'][1].lower()}: what to lock, what to release and how to measure it. Guide coming soon."),
        f"/industrias/{d['id']}/", (f"Ver la página de {d['name'][0]}", f"See the {d['name'][1]} page")) for d in INDUSTRIES)
    blog = "".join(res_card(("Blog", "Blog"), p["title"], p["card"], f"/blog/{p['slug']}/", ("Leer el artículo", "Read the article")) for p in POSTS)
    body = f'''{hero([HOME, (("Recursos", "Resources"), None)], ("Recursos", "Resources"),
        ("Recursos para gobernar tu marca.", "Resources for governing your brand."),
        ("Guías por industria y artículos para equipos que administran una marca, en una ubicación o en muchas.",
         "Industry guides and articles for teams that manage a brand, in one location or many."),
        [(("Agenda una demo", "Book a demo"), "/contacto/"), (("Ver guías", "See guides"), "#guias")], "mark")}

<section class="sec">
  <div class="wrap">
    <div class="rgroup" id="guias"><h2>{B("Guías por industria", "Industry guides")}</h2><ul class="res res--wide">{guides}</ul></div>
    <div class="rgroup" id="blog"><h2>Blog</h2><ul class="res res--wide">{blog}</ul></div>
  </div>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    return page("recursos", "Recursos", "Guías y artículos sobre gobernanza y automatización de branding y marketing.", "recursos", body)

# --------------------------------------------------------------- blog
def render_blocks(blocks):
    """Bloques de contenido (blog, páginas legales) → lista de fragmentos HTML."""
    parts = []
    for kind, c in blocks:
        if kind == "h2":
            parts.append(f"<h2>{B(c)}</h2>")
        elif kind == "p":
            parts.append(f"<p>{B(c)}</p>")
        elif kind in ("ul", "ol"):
            parts.append(f"<{kind}>" + "".join(f"<li>{B(x)}</li>" for x in c) + f"</{kind}>")
        elif kind == "faq":
            qa = "".join(f'<div class="faq__item"><h3>{B(q)}</h3><p>{B(a)}</p></div>' for q, a in c)
            parts.append(f'<section class="faq" aria-labelledby="faq-t"><h2 id="faq-t">{B("Preguntas frecuentes", "Frequently asked questions")}</h2>{qa}</section>')
    return parts

def terms_page():
    t = TERMS
    y, mo, d = (int(x) for x in t["updated"].split("-"))
    date = B(f"{d} de {MESES[mo - 1]} de {y}", f"{MONTHS[mo - 1]} {d}, {y}")
    body = f'''{hero([HOME, (("Términos y condiciones", "Terms and conditions"), None)], ("Legal", "Legal"), t["title"], t["lede"],
        [(("Contáctanos", "Contact us"), "/contacto/"), (("Aviso de privacidad", "Privacy notice"), PRIVACY)], "mark")}

<section class="sec post-sec">
  <article class="wrap post">
    <p class="post__meta">{B("Última actualización", "Last updated")}: <time datetime="{t["updated"]}">{date}</time></p>
    {"".join(render_blocks(t["blocks"]))}
  </article>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    page("terminos", t["title"][0], "Términos y condiciones de uso del sitio de 1RedBrand: uso permitido, propiedad intelectual, datos personales, cookies, responsabilidad y ley aplicable.", "", body)
    return "terminos"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def post_page(p):
    y, mo, d = (int(x) for x in p["date"].split("-"))
    date = B(f"{d} de {MESES[mo - 1]} de {y}", f"{MONTHS[mo - 1]} {d}, {y}")
    parts = render_blocks(p["blocks"])
    summary = "".join(f"<li>{B(x)}</li>" for x in p["summary"])
    path = f"blog/{p['slug']}"
    body = f'''{hero([HOME, (("Recursos", "Resources"), "/recursos/"), (("Blog", "Blog"), "/recursos/#blog"), (p["title"], None)],
        ("Blog", "Blog"), p["title"], p["lede"],
        [(("Agenda una demo", "Book a demo"), "/contacto/"), (("Ir a las preguntas frecuentes", "Go to the FAQs"), "#faq-t")], "mark")}

<section class="sec post-sec">
  <article class="wrap post">
    <p class="post__meta"><time datetime="{p["date"]}">{date}</time> · {B(f"{p['minutes']} min de lectura", f"{p['minutes']} min read")} · {B("Equipo 1RedBrand", "1RedBrand team")}</p>
    <aside class="post__sum" aria-labelledby="sum-t">
      <p class="post__sum-t" id="sum-t">{B("En resumen", "In short")}</p>
      <ul>{summary}</ul>
    </aside>
    {"".join(parts)}
  </article>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    faq = next((c for k, c in p["blocks"] if k == "faq"), [])
    nodes = [seo.blog_posting(path, p), seo.faq_page(path, faq)] if faq else [seo.blog_posting(path, p)]
    page(path, p["title"][0], p["desc"][0], "recursos", body, nodes=nodes, seo_title_override=p["seo_title"])
    return path

# --------------------------------------------------------------- compañía
def company_page():
    purpose = ("Empoderamos a las organizaciones para preservar el valor de su identidad de marca, su comunicación con clientes y su fidelización, de manera automatizada, eficiente y a gran escala.",
               "We empower organizations to preserve the value of their brand identity, their customer communication and their loyalty, in an automated, efficient way and at scale.")
    story = [
        ("2000", ("Inicio como agencia digital", "Started as a digital agency"),
         ("Iniciamos en México como agencia digital.", "We started in Mexico as a digital agency.")),
        ("2015", ("Nace 1RedBrand", "1RedBrand is born"),
         ("Para hacer más eficiente la colaboración con nuestros clientes, creamos 1RedBrand: una plataforma propia para producir, aprobar y publicar con la misma marca.",
          "To make our collaboration with clients more efficient, we created 1RedBrand: our own platform to produce, approve and publish under the same brand.")),
        ("2022", ("Llegada a Estados Unidos", "Expansion to the United States"),
         ("Se registra 1RedBrand LLC en Florida y la plataforma empieza a operar como SaaS independiente, lista para empresas.",
          "1RedBrand LLC is registered in Florida and the platform begins operating as a standalone, enterprise-ready SaaS.")),
        (("Hoy", "Today"), ("Una plataforma modular", "A modular platform"),
         ("8 módulos que funcionan por separado o integrados: gobernanza de marca, marketing digital, atención con IA, CRM, SEO, lealtad, menús digitales y recorridos virtuales.",
          "8 modules that work on their own or together: brand governance, digital marketing, AI customer care, CRM, SEO, loyalty, digital menus and virtual tours.")),
    ]
    items = "".join(tl_item(f"<b>{B(y) if isinstance(y, tuple) else y}</b>", n, t) for y, n, t in story)
    facts = [
        (("México", "Mexico"), ("Agencia digital desde 2000 y 1RedBrand desde 2015. Se comercializa a través de Vmasideas.", "Digital agency since 2000 and 1RedBrand since 2015. Sold through Vmasideas.")),
        (("Estados Unidos", "United States"), ("Desde 2022, como 1RedBrand LLC, con sede legal en Florida.", "Since 2022, as 1RedBrand LLC, registered in Florida.")),
    ]
    ff = "".join(f'<div class="fact"><p class="fact__k">{B(k)}</p><p class="fact__v">{B(v)}</p></div>' for k, v in facts)
    body = f'''{hero([HOME, (("Compañía", "Company"), None)], ("Nosotros", "About"),
        ("Una plataforma modular para gobernar y automatizar tu marca.", "A modular platform to govern and automate your brand."),
        ("1RedBrand es una plataforma modular de gobernanza y automatización de branding y marketing. Ayuda a negocios independientes y a organizaciones con varias sedes a producir, publicar y atender con la misma marca.",
         "1RedBrand is a modular branding and marketing governance and automation platform. It helps independent businesses and multi-location organizations produce, publish and serve customers under the same brand."),
        [(("Contáctanos", "Contact us"), "/contacto/"), (("Ver la plataforma", "See the platform"), "/plataforma/")], "mark")}

<section class="sec">
  <div class="wrap">
    <h2 class="purpose__t">{B("Nuestro propósito", "Our purpose")}</h2>
    <p class="purpose">{B(purpose)}</p>
  </div>
</section>

<section class="sec sec--ink curved">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Nuestra historia.", "Our story.")}</h2>
      <p class="lede">{B("Más de 25 años en el mundo digital: 1RedBrand nació de nuestra experiencia como agencia y hoy opera en México y Estados Unidos.", "Over 25 years in digital: 1RedBrand grew out of our agency experience and now operates in Mexico and the United States.")}</p></div>
    <div class="threadlist" data-node-group>{items}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>{B("Dónde estamos.", "Where we are.")}</h2></div>
    <div class="facts">{ff}</div>
  </div>
</section>

{final(READY, (("Agenda una demo", "Book a demo"), "/contacto/"))}'''
    return page("compania", "Nosotros", "1RedBrand ayuda a preservar el valor de tu marca, tu comunicación con clientes y su fidelización. Nace en 2015 de una agencia digital fundada en 2000.", "compania", body)

# --------------------------------------------------------------- contacto
def contact_page():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = re.search(r"<!--#include contact-form-->(.*?)<!--/include contact-form-->", src, re.S)
    form = m.group(1).replace('data-anchor data-at="tail"', "data-tail")
    body = f'''{hero([HOME, (("Contacto", "Contact"), None)], ("Contacto", "Contact"),
        ("Hablemos de tu marca.", "Let's talk about your brand."),
        ("Cuéntanos de tu marca y qué te gustaría resolver. Te contactamos para agendar una demo.",
         "Tell us about your brand and what you want to solve. We'll reach out to book a demo."),
        [(("Ir al formulario", "Go to the form"), "#formulario")], "mark")}

<section class="sec" id="formulario">
  <div class="wrap contact">
    {form}
    <aside style="display:grid;gap:1rem;align-content:start">
      <h2 style="font-size:clamp(1.5rem,4vw,2rem)">{B("Escríbenos directo", "Write to us directly")}</h2>
      <p><a class="link" href="mailto:hello@1redbrand.com">hello@1redbrand.com</a></p>
      <p class="lede" style="font-size:.95rem">{B("Teléfono y dirección: pendientes de confirmar qué datos se publican.", "Phone and address: pending confirmation of which details are public.")}</p>
    </aside>
  </div>
</section>'''
    return page("contacto", "Contacto", "Agenda una demo de 1RedBrand. Cuéntanos de tu marca y te mostramos cómo gobernar y automatizar tu branding y marketing.", "compania", body,
                extra_js=f'\n<script src="/assets/js/contact-form.js?v={V}"></script>')

def update_home_nav():
    """La Home es HTML a mano: se le reemplaza solo el bloque <nav> y las versiones."""
    p = os.path.join(ROOT, "index.html")
    src = open(p, encoding="utf-8").read()
    src = re.sub(r'<nav class="nav" id="nav" aria-label="Principal">.*?</nav>', lambda _: nav_html("inicio"), src, count=1, flags=re.S)
    src = re.sub(r'<script src="assets/js/nav\.js[^"]*"></script>\n', "", src)
    src = re.sub(r'(<script src="assets/js/main\.js[^"]*"></script>)', lambda m: f'<script src="assets/js/nav.js?v={V}"></script>\n' + m.group(1), src, count=1)
    src = re.sub(r'styles\.css\?v=\d+', f"styles.css?v={V}", src)
    src = re.sub(r'main\.js\?v=\d+', f"main.js?v={V}", src)
    src = re.sub(r'contact-form\.js\?v=\d+', f"contact-form.js?v={V}", src)
    src = re.sub(r'content\.js\?v=\d+', f"content.js?v={V}", src)
    src = update_home_seo(src)
    open(p, "w", encoding="utf-8").write(src)

# --------------------------------------------------------------- Home: SEO + HTML estático
GSAP = {
    "gsap.min.js": "sha512-7eHRwcbYkK4d9g/6tD/mhkf++eoTHwpNM9woBxtPUBWm67zeAfFC+HrdoE2GanKeocly/VxeLvIqwvCdk7qScg==",
    "ScrollTrigger.min.js": "sha512-onMTRKJBKz8M1TnqqDuGBlowlH0ohFzMXYRNebz+yOcc5TQr/zAKsthzhuv0hiyUKEiQEQXEynnXCvNTOk50dg==",
}

def home_content():
    """Lee assets/js/content.js (la misma fuente que usa la Home) con Node."""
    js = os.path.join(ROOT, "assets", "js", "content.js").replace("\\", "/")
    out = subprocess.run(["node", "-e", f"global.window={{}};require({json.dumps(js)});process.stdout.write(JSON.stringify(window.RB))"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return json.loads(out)

def tj(o):
    return o if isinstance(o, str) else B(o["es"], o["en"])

def home_static(RB):
    """Mismo marcado que genera main.js, para que buscadores y motores de IA lean la Home sin ejecutar JS."""
    curls = ["M10,190 C40,60 90,170 120,80 S190,10 170,110 C160,160 120,150 130,120",
             "M190,190 C160,90 100,160 80,90 C60,20 140,10 150,70 C160,130 40,140 20,60",
             "M20,40 C80,10 120,90 70,120 C30,145 60,190 120,170 S190,110 180,60"]
    steps = "".join(f'<li class="step"><span class="step__n">{i + 1}</span><span class="step__t">{B(s["es"], s["en"])}</span>'
                    f'<span class="step__m">{tj(s["m"])}</span></li>' for i, s in enumerate(RB["steps"]))
    n = len(RB["modules"])
    mods = "".join(
        f'<article class="mod{" mod--feature" if m.get("feature") else ""}" id="mod-{m["id"]}" aria-label="{i + 1} / {n}" data-pre>'
        f'<svg class="mod__glyph" viewBox="0 0 100 100" aria-hidden="true"><path d="{m["glyph"]}"/></svg>'
        f'<h3 class="mod__name">{tj(m["name"])}</h3><p class="mod__promise">{tj(m["promise"])}</p>'
        f'<ol class="mod__how">{"".join(f"<li>{B(s, m["how"]["en"][k])}</li>" for k, s in enumerate(m["how"]["es"]))}</ol>'
        f'<a class="mod__cta" href="/plataforma/{m["id"]}/">{tj(m["cta"])}</a></article>' for i, m in enumerate(RB["modules"]))
    inds = "".join(
        f'<article class="ind" id="ind-{d["id"]}"><svg class="ind__bg" viewBox="0 0 200 200" aria-hidden="true"><path d="{curls[i % 3]}"/></svg>'
        f'<h3 class="ind__name">{tj(d["name"])}</h3><p class="ind__pain">{tj(d["pain"])}</p>'
        f'<ul class="ind__mods">{"".join(f"<li>{tj(x)}</li>" for x in d["mods"])}</ul>'
        f'<a class="ind__cta" href="/industrias/{d["id"]}/">{B("Ver " + d["name"]["es"], "See " + d["name"]["en"])}</a></article>'
        for i, d in enumerate(RB["industries"]))
    inds += (f'<article class="ind ind--more" id="ind-mas"><span class="ind__plus" aria-hidden="true">+</span>'
             f'<h3 class="ind__name">{B(MORE["name"])}</h3><p class="ind__pain">{B(MORE["short"])}</p>'
             f'<a class="ind__cta" href="#demo">{B(MORE["cta"])}</a></article>')
    fmods = "".join(f'<li><a href="/plataforma/{m["id"]}/">{tj(m["name"])}</a></li>' for m in RB["modules"])
    finds = "".join(f'<li><a href="/industrias/{d["id"]}/">{tj(d["name"])}</a></li>' for d in RB["industries"])
    return steps, mods, inds, fmods, finds

def update_home_seo(src):
    desc = re.search(r'<meta name="description" content="([^"]*)">', src).group(1)
    t = seo.TITLES[""]
    graph = [seo.org(), seo.website(), seo.platform(MODULES), seo.webpage("", t, desc)]
    head = f'<script src="assets/js/lang.js?v={V}"></script>\n' + seo.head_tags("", t, desc, graph, asset_prefix="")
    # todo lo que va entre viewport y las fuentes se regenera (título, descripción, canonical, OG, JSON-LD, iconos)
    src = re.sub(r'(<meta name="viewport"[^>]*>\n).*?(<link rel="preconnect" href="https://fonts\.googleapis\.com">)',
                 lambda m: m.group(1) + head + m.group(2), src, count=1, flags=re.S)
    # GSAP con integridad (SRI)
    for f, h in GSAP.items():
        src = re.sub(rf'<script src="(https://cdnjs\.cloudflare\.com/ajax/libs/gsap/3\.12\.5/{re.escape(f)})"[^>]*></script>',
                     lambda m: f'<script src="{m.group(1)}" integrity="{h}" crossorigin="anonymous" referrerpolicy="no-referrer"></script>', src)
    # contenido estático dentro de los contenedores que main.js vuelve a pintar
    steps, mods, inds, fmods, finds = home_static(home_content())
    src = re.sub(r'(<ol class="steps" data-steps>).*?(</ol>)', lambda m: m.group(1) + steps + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r'(<svg class="track__thread" aria-hidden="true" data-track-thread></svg>).*?(\n      </div>\n    </div>)',
                 lambda m: m.group(1) + mods + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r'(<div class="ind__rail" data-ind-rail[^>]*>).*?(</div>\n  <div class="wrap"><div class="ind__bar">)',
                 lambda m: m.group(1) + inds + m.group(2), src, count=1, flags=re.S)
    bar = clients_bar(extra=" data-thread").replace('src="/assets/', 'src="assets/')
    src = re.sub(r'<!-- ============ CLIENTES ============ -->\n<section class="logobar".*?</section>\n\n', "", src, count=1, flags=re.S)
    src = src.replace("<!-- ============ RECURSOS ============ -->",
                      "<!-- ============ CLIENTES ============ -->\n" + bar + "\n\n<!-- ============ RECURSOS ============ -->", 1)
    src = re.sub(r'(<ul data-foot-modules>).*?(</ul>)', lambda m: m.group(1) + fmods + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r'(<ul data-foot-ind>).*?(</ul>)', lambda m: m.group(1) + finds + m.group(2), src, count=1, flags=re.S)
    return src

# --------------------------------------------------------------- archivos raíz
def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def not_found_page():
    body = hero([HOME, (("Página no encontrada", "Page not found"), None)], ("Error 404", "Error 404"),
                ("Esta página no existe.", "This page doesn't exist."),
                ("Puede que el enlace esté mal escrito o que la página haya cambiado de lugar.",
                 "The link may be mistyped or the page may have moved."),
                [(("Ir al inicio", "Go home"), "/"), (("Ver la plataforma", "See the platform"), "/plataforma/")], "mark")
    page("_404", "Página no encontrada", "La página que buscas no existe.", "", body, noindex=True)
    src = os.path.join(ROOT, "_404", "index.html")
    os.replace(src, os.path.join(ROOT, "404.html"))
    os.rmdir(os.path.join(ROOT, "_404"))

def root_files(paths):
    write("robots.txt", seo.robots_txt())
    write("sitemap.xml", seo.sitemap_xml([""] + [p.replace(os.sep, "/") for p in paths]))
    write("llms.txt", seo.llms_txt(MODULES, INDUSTRIES, MORE, POSTS))
    write(".well-known/security.txt", seo.SECURITY_TXT)

if __name__ == "__main__":
    update_home_nav()
    out = [platform_page(), industries_index(), results_page(), resources_page(), company_page(), contact_page()]
    out += [module_page(m) for m in MODULES]
    out += [industry_page(d) for d in INDUSTRIES]
    out += [post_page(p) for p in POSTS]
    out.append(terms_page())
    not_found_page()
    root_files(out)
    print(len(out), "páginas + 404, robots.txt, sitemap.xml, llms.txt, security.txt:")
    for p in out:
        print(" /" + p.replace(os.sep, "/") + "/")
