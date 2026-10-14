# -*- coding: utf-8 -*-
"""Static generator for the Mama Africa Beauty site (v2). Run: python3 _build/build.py
Writes every page to the repo root (GitHub Pages serves clean URLs)."""
import os, json, html, sys
from urllib.parse import quote
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from data import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
esc = html.escape

# ---------------------------------------------------------------- icons
I = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-.99.24-3.33-.69-2.81-1.11-4.6-3.98-4.74-4.17-.14-.18-1.13-1.5-1.13-2.87s.72-2.03.97-2.31c.26-.28.56-.35.74-.35l.54.01c.17 0 .41-.07.64.49.25.58.83 2.01.9 2.15.08.14.12.3.03.49-.1.19-.14.3-.28.47-.14.16-.3.37-.42.49-.14.14-.29.29-.12.57.16.28.73 1.2 1.56 1.94 1.07.95 1.98 1.25 2.26 1.39.28.14.44.12.61-.07.16-.19.71-.83.9-1.11.19-.28.37-.23.63-.14.26.09 1.65.78 1.93.92.28.14.47.21.54.33.07.11.07.66-.18 1.35Z"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="3"/><path d="M8 2.5v4M16 2.5v4M3 10h18M8 14h2M14 14h2M8 17.5h2"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.3 7-12a7 7 0 1 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="5" rx="1"/><path d="M12 8v13M5 13v8h14v-8M12 8S10.5 3 8 3a2.5 2.5 0 0 0 0 5M12 8s1.5-5 4-5a2.5 2.5 0 0 1 0 5"/></svg>',
 "arr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 6-6 6 6 6"/></svg>',
 "next": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>',
 "g": '<svg class="g-logo" viewBox="0 0 48 48" aria-label="Google"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>',
}
ARR_W = I["arr"].replace('<svg', '<svg class="arr"')
STAR5 = '<span class="stars" aria-label="5 étoiles sur 5">★★★★★</span>'
KENTE = '<span class="kente" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'
SUNDEF = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="sunGrad" x1="0" x2="1"><stop offset="0" stop-color="#f4b23e"/><stop offset=".5" stop-color="#e8692a"/><stop offset="1" stop-color="#bf2e1e"/></linearGradient></defs></svg>'
UL = '<svg viewBox="0 0 200 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 14 C 40 4, 90 3, 120 8 S 180 16, 197 6"/></svg>'

def wa(msg="Bonjour Mama Africa, j'aimerais prendre rendez-vous."):
    return f"https://wa.me/{WA}?text={quote(msg)}"

_d = {}
def dims(n):
    if n not in _d:
        try:
            with Image.open(os.path.join(IMG, n + ".webp")) as im: _d[n] = im.size
        except FileNotFoundError: _d[n] = (1200, 1500)
    return _d[n]

def img(n, alt, sizes="(max-width: 760px) 100vw, 50vw", cls="", eager=False, lazy=True, style=""):
    w, h = dims(n)
    srcset = ""
    if os.path.exists(os.path.join(IMG, n + "-m.webp")):
        srcset = f' srcset="assets/img/{n}-m.webp {dims(n + "-m")[0]}w, assets/img/{n}.webp {w}w" sizes="{sizes}"'
    load = 'fetchpriority="high"' if eager else ('loading="lazy"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f'<img src="assets/img/{n}.webp"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async"{c}{s}>'

def video(n, label=""):
    aria = f' aria-label="{esc(label)}"' if label else ' aria-hidden="true"'
    return f'<video src="assets/video/{n}.mp4" poster="assets/video/{n}.webp" muted loop playsinline autoplay preload="metadata"{aria}></video>'

def label(t):
    return f'<p class="label">{KENTE}{t}</p>'

def price(p, pre=None):
    if not p: return '<span class="price" style="font-size:22px">Sur demande</span>'
    pre = f'<em>{pre}</em>' if pre else ''
    return f'<span class="price">{pre}{p}<small>CHF</small></span>'

# ---------------------------------------------------------------- shell
NAV = [("index", "Accueil", "./"), ("tresses", "Tresses", "tresses"), ("tissage", "Tissage", "tissage"),
       ("soins", "Soins & perruques", "soins"), ("offres", "Offres", "offres"), ("tarifs", "Tarifs", "tarifs"),
       ("boutique", "Boutique", "boutique"), ("galerie", "Galerie", "galerie"), ("salon", "Le salon", "salon"),
       ("avis", "Avis", "avis"), ("contact", "Contact", "contact")]
DESK_NAV = ["tresses", "tissage", "soins", "offres", "tarifs", "boutique", "galerie", "contact"]

def header(cur):
    cur_attr = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur_attr if s == cur else ""}>{l}</a>' for s, l, h in NAV if s in DESK_NAV)
    mnav = "".join(f'<a class="big" href="{h}">{l}<small>{i:02d}</small></a>' for i, (s, l, h) in enumerate(NAV, 1))
    return f'''<a class="skip" href="#main">Aller au contenu</a>{SUNDEF}
<header class="hdr" id="hdr"><div class="wrap">
  <a class="brand" href="./" aria-label="{SHORT}, accueil"><img src="assets/img/logo.webp" width="731" height="377" alt="Mama Africa Beauty Shop"></a>
  <nav class="nav" aria-label="Navigation principale">{nav}</nav>
  <div class="hdr-r">
    <a class="icon-btn" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a>
    <button class="btn btn--sun btn--sm" type="button" data-book>{I["cal"]}Réserver</button>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
</div></header>
<nav class="mnav" id="mnav" aria-label="Menu">{mnav}
  <div class="mnav-foot"><a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a><a class="btn btn--ghost" href="tel:{TEL}">{I["tel"]}{PHONE}</a><a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}{IG_HANDLE}</a></div>
</nav>'''

def hours_list():
    out = ""
    for i, (d, o, c) in enumerate(HOURS):
        v = f"{o.replace(':', 'h')} – {c.replace(':', 'h')}" if o else '<span class="off">Fermé</span>'
        out += f'<li data-day="{(i + 1) % 7}"><span>{d}</span><span>{v}</span></li>'
    return f'<ul class="hours">{out}</ul>'

def ways(light=False):
    c = " ways--light" if light else ""
    return f'''<div class="ways{c}">
  <a class="way" href="{SALONKEE}" target="_blank" rel="noopener"><span class="ic">{I["cal"]}</span><span><b>En ligne sur Salonkee</b><small>Choisissez votre créneau, 24h/24</small></span>{ARR_W}</a>
  <a class="way wa" href="{wa()}" target="_blank" rel="noopener"><span class="ic">{I["wa"]}</span><span><b>Sur WhatsApp</b><small>Envoyez le code ou la photo du modèle</small></span>{ARR_W}</a>
  <a class="way tel" href="tel:{TEL}"><span class="ic">{I["tel"]}</span><span><b>{PHONE}</b><small>Lundi – samedi, 9h00 – 18h30</small></span>{ARR_W}</a>
</div>'''

def footer():
    col = lambda items: "".join(f'<li><a href="{h}">{l}</a></li>' for s, l, h in NAV if s in items)
    return f'''<footer class="ftr"><div class="wrap">
  <p class="ftr-big">Votre beauté,<br><span class="sun-text">notre passion.</span></p>
  <div class="ftr-grid">
    <div><a class="logo-chip" href="./"><img src="assets/img/logo.webp" width="731" height="377" alt="Mama Africa Beauty Shop" loading="lazy"></a>
      <p>Salon de tresses africaines et boutique beauté au centre de Payerne.</p>
      <div class="socials"><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a><a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["wa"]}</a><a href="{GMAPS}" target="_blank" rel="noopener" aria-label="Google Maps">{I["pin"]}</a><a href="{SALONKEE}" target="_blank" rel="noopener" aria-label="Salonkee">{I["cal"]}</a></div></div>
    <div><h4>Coiffure</h4><ul>{col(["tresses", "tissage", "soins", "offres", "tarifs"])}<li><a href="beaute">Beauté</a></li></ul></div>
    <div><h4>Mama Africa</h4><ul>{col(["boutique", "galerie", "salon", "avis", "contact"])}<li><a href="reservation">Réserver</a></li></ul></div>
    <div><h4>Nous trouver</h4><ul><li><a href="{GMAPS}" target="_blank" rel="noopener">{STREET}<br>{CITY}</a></li><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></li><li style="color:var(--on-night-2)">Lun – Sam · 9h00 – 18h30</li></ul></div>
  </div>
  <div class="ftr-bot"><span>© 2026 {NAME} · Payerne</span><a href="confidentialite">Confidentialité</a></div>
</div></footer>'''

def overlays():
    return f'''<div class="abar" id="abar">
  <a class="a-tel" href="tel:{TEL}" aria-label="Appeler le {PHONE}">{I["tel"]}Appeler</a>
  <a class="a-wa" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a>
  <button class="a-book" type="button" data-book>{I["cal"]}Réserver</button>
</div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-t" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-panel"><button class="x" type="button" data-close aria-label="Fermer">{I["x"]}</button>
    {label("Rendez-vous")}<h2 class="h-m" id="sheet-t" style="margin-bottom:20px">Comment voulez-vous réserver&nbsp;?</h2>
    {ways(light=True)}
    <p class="hint" style="margin-top:16px">Vous connaissez votre modèle ? <a class="link" href="tresses#codes">Choisir un code</a></p>
  </div>
</div>
<div class="sheet" id="offer" role="dialog" aria-modal="true" aria-labelledby="offer-t" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-panel offer-panel"><button class="x" type="button" data-close aria-label="Fermer">{I["x"]}</button>
    <div class="offer-in"><div class="ph"><img alt="" data-o="img"></div>
      <div class="bd"><span class="chip chip--sun" style="align-self:flex-start" data-o="badge"></span><h2 class="h-m" id="offer-t" data-o="title"></h2><div data-o="price"></div><p class="muted" data-o="lead" style="margin:0"></p><ul data-o="incl"></ul>
      <div class="btns" style="margin-top:8px"><a class="btn btn--wa" data-o="wa" target="_blank" rel="noopener">{I["wa"]}Réserver sur WhatsApp</a><button class="btn btn--ghost btn--sm" type="button" data-o="flyer">Voir l'affiche</button></div></div></div>
  </div>
</div>
<div class="lb" id="lb" aria-hidden="true"><button class="x" type="button" aria-label="Fermer">{I["x"]}</button><button class="pv" type="button" aria-label="Précédente">{I["prev"]}</button><img alt=""><button class="nx" type="button" aria-label="Suivante">{I["next"]}</button><p></p></div>'''

def schema():
    d = {"@context": "https://schema.org", "@type": "HairSalon", "name": NAME, "slogan": SLOGAN,
         "image": BASE + "assets/img/logo.png", "url": BASE, "telephone": TEL, "priceRange": "CHF 45 – 165",
         "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressRegion": "VD", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:30"}],
         "sameAs": [INSTAGRAM, SALONKEE, GMAPS]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def page(slug, title, desc, body, og="box-braids-longues"):
    url = BASE + ("" if slug == "index" else slug)
    robots = '<meta name="robots" content="noindex, nofollow">' if PITCH else ""
    offers_json = json.dumps({o["id"]: {k: o.get(k) for k in ("title", "price", "pre", "img", "badge", "flyer", "lead", "incl")} for o in OFFERS}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#fffcf7">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CH"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/{og}.webp">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/cabinet-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/satoshi-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={V}">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__ma)document.documentElement.classList.remove('js')}},3500)</script>
{schema() if slug in ("index", "contact") else ""}
</head>
<body data-page="{slug}">
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
{overlays()}
<script>window.MA_OFFERS={offers_json};window.MA_WA="{WA}";</script>
<script src="assets/js/vendor/lenis.min.js"></script>
<script src="assets/js/vendor/gsap.min.js"></script>
<script src="assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="assets/js/site.js?v={V}"></script>
<script type="importmap">{{"imports":{{"three":"./assets/js/vendor/three.module.min.js"}}}}</script>
<script type="module" src="assets/js/scene.js?v={V}"></script>
</body>
</html>'''

# ---------------------------------------------------------------- blocks
def phero(crumb, lab, h1, lead, media, sticker=None, extra=""):
    st = f'<span class="sticker">{sticker[0]}<b>{sticker[1]}</b></span>' if sticker else ""
    return f'''<section class="phero"><div class="wrap phero-grid">
  <div><nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>/</span><span>{crumb}</span></nav>
    {label(lab)}<h1 class="h-xl" data-split>{h1}</h1><p class="lead" data-reveal>{lead}</p>
    {extra or f'<div class="btns" style="margin-top:30px" data-reveal><button class="btn btn--sun" type="button" data-book>{I["cal"]}Réserver</button><a class="btn btn--ghost" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a></div>'}</div>
  <div class="phero-media" data-reveal>{media}{st}</div>
</div></section>'''

def wa_msg(o):
    if o.get("flyer") or o.get("id"):
        return f"Bonjour Mama Africa, je souhaite réserver l'offre « {o['title']} » ({o['price']} CHF)."
    return f"Bonjour Mama Africa, je souhaite un rendez-vous pour : {o['title']}."

def offer_card(o, big=False):
    fl = f'<button class="flyer-btn" type="button" data-flyer="{o["flyer"]}">Voir l\'affiche</button>' if o.get("flyer") else ""
    incl = "".join(f"<li>{x}</li>" for x in o["incl"])
    return f'''<article class="card" data-reveal>
  <div class="ph">{img(o["img"], o["title"], "(max-width: 760px) 100vw, 33vw")}<span class="badge badge--sun">{o["badge"]}</span></div>
  <div class="bd"><h3>{o["title"]}</h3><p>{o["lead"]}</p><ul>{incl}</ul>
  <div class="row">{price(o["price"], o.get("pre"))}<div style="display:flex;gap:14px;align-items:center">{fl}<a class="btn btn--sm" href="{wa(wa_msg(o))}" target="_blank" rel="noopener">Réserver</a></div></div></div>
</article>'''

def ring():
    cards = "".join(f'''<button class="ring-card" type="button" data-offer="{o["id"]}" aria-label="{esc(o["title"])}, {o["price"]} CHF">{img(o["img"], "", "320px", lazy=False)}<span class="rc-b">{o["badge"]}</span><span class="rc-t"><b>{o["title"]}</b><span>{("<em>" + o["pre"] + "</em>") if o.get("pre") else ""}{o["price"]}<small>CHF</small></span></span></button>''' for o in OFFERS)
    return f'''<div class="ring-stage" id="ring" data-reveal="fade"><div class="ring">{cards}</div></div>
<div class="ring-ctrl"><button type="button" data-ring="-1" aria-label="Offre précédente">{I["prev"]}</button><button type="button" data-ring="1" aria-label="Offre suivante">{I["next"]}</button></div>'''

def codes_block():
    items = "".join(f'<button class="code" type="button" data-code="{c}" data-price="{p}" aria-pressed="false"><span class="ph">{img(f"code-{c}", f"Modèle code {c}", "120px")}</span><b>Code {c}</b><strong>{p}<small> CHF</small></strong></button>' for c, p in CODES)
    return f'''<div class="codes" id="codes-grid">{items}</div>
<div class="code-cta"><p id="code-sel">Touchez un modèle pour le sélectionner.</p><div class="btns"><a class="btn btn--wa" id="code-wa" href="{wa("Bonjour Mama Africa, je souhaite réserver un modèle de votre catalogue.")}" target="_blank" rel="noopener">{I["wa"]}Réserver ce code</a><button class="btn btn--ghost btn--sm" type="button" data-flyer="affiche-codes">Voir le catalogue</button></div></div>'''

def tabs_block(keys=("tresses", "tissage", "soins", "beaute")):
    tabs = "".join(f'<button type="button" role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if i == 0 else "false"}">{MENU[k][0]}</button>' for i, k in enumerate(keys))
    panels = ""
    for i, k in enumerate(keys):
        lis = ""
        for n, p, d in MENU[k][1]:
            pr = f'{p}<small>CHF</small>' if p else '<small style="opacity:1;font-size:14px">Sur demande</small>'
            dd = f'<span class="d">{d}</span>' if d else ""
            lis += f'<li><span class="n">{n}</span><span class="p">{pr}</span>{dd}</li>'
        panels += f'<div class="panel" role="tabpanel" id="p-{k}" aria-labelledby="t-{k}"{"" if i == 0 else " hidden"}><ul class="plist">{lis}</ul></div>'
    return f'<div class="tabs" role="tablist">{tabs}</div>{panels}'

def swatches_block():
    sw = "".join(f'<button class="sw" type="button" data-shade="{c}" style="--c:{h}" aria-pressed="false"><i></i><span><b>{c}</b><small>{n}</small></span></button>' for c, h, n in SHADES)
    return f'''<div class="shade-grid">
  <div>{label("Couleurs des mèches")}<h2 class="h-l" data-split>Essayez une couleur. La tresse suit.</h2>
    <p class="lead" style="margin-top:20px" data-reveal>Touchez une teinte : la tresse 3D qui vous accompagne sur le site prend sa couleur. Toutes ces mèches sont en vente au salon.</p>
    <div class="swatches" data-reveal>{sw}</div>
    <p class="shade-now" id="shade-now"><i></i><span>Couleur actuelle : <b>4 · Châtain</b></span></p></div>
  <div class="shade-visual" data-reveal>{img("tresses-miel", "Tresses couleur miel", "(max-width: 960px) 100vw, 45vw")}<span class="tag"><i></i><span id="shade-tag">Mèches en boutique, toutes teintes</span></span></div>
</div>'''

def reviews_block(head=True):
    real = lambda r: f'<article class="rv-card"><div class="rv-top"><span class="rv-av">{r["initial"]}</span><div><b>{esc(r["name"])}</b><small>{r["meta"]}</small></div>{I["g"]}</div>{STAR5}<p>{esc(r["text"])}</p></article>'
    ph = lambda: f'<article class="rv-card is-ph" aria-hidden="true"><div class="rv-top"><span class="rv-av">★</span><div><b style="color:var(--muted)">Avis Google</b><small>Emplacement réservé</small></div>{I["g"]}</div>{STAR5}<div class="sk"></div><div class="sk"></div><div class="sk"></div><em>Le prochain avis s\'affichera ici.</em></article>'
    cta = f'<article class="rv-card is-cta"><b>Vous êtes venue au salon&nbsp;?</b><p style="color:var(--on-night-2)">Votre avis aide d\'autres femmes à nous trouver.</p><a class="btn btn--light btn--sm" href="{G_WRITE}" target="_blank" rel="noopener">{I["g"]}Laisser un avis</a></article>'
    r1 = [real(r) for r in REVIEWS] + [ph(), ph(), cta, ph(), ph()]
    r2 = [ph(), cta, ph()] + [real(r) for r in REVIEWS] + [ph(), ph()]
    tr = lambda c: f'<div class="rv-track">{"".join(c)}<div style="display:contents" aria-hidden="true">{"".join(c)}</div></div>'
    h = f'''<div class="wrap"><div class="head"><div>{label("Avis Google")}<h2 class="h-l" data-split>Elles en parlent.</h2></div>
<a class="g-score" href="{G_REVIEWS}" target="_blank" rel="noopener">{I["g"]}<b>{G_RATING}</b><span>{STAR5}<small>{G_COUNT} avis sur Google</small></span></a></div></div>''' if head else ""
    return f'{h}<div class="rv">{tr(r1)}</div><div class="rv rv--rev">{tr(r2)}</div>'

def book_band():
    return f'''<section class="sec--tight"><div class="wrap"><div class="book" data-reveal><div class="book-grid">
  <div>{label("Prendre rendez-vous")}<h2 class="h-l" data-split>Votre prochaine coiffure commence ici.</h2><p class="lead">Réservez en ligne, envoyez le code ou la photo de votre modèle sur WhatsApp, ou appelez-nous.</p></div>
  {ways()}
</div></div></div></section>'''

def visit():
    return f'''<section class="sec" id="visite"><div class="wrap visit">
  <div>{label("Nous trouver")}<h2 class="h-l" data-split>Rue de Lausanne 38B, Payerne.</h2>
    <p class="lead" style="margin:20px 0 22px">Salon et boutique à la même adresse, au centre de Payerne.</p>
    <span class="open-now" id="open-now"><i></i><span>Horaires</span></span>{hours_list()}
    <div class="btns" style="margin-top:28px"><a class="btn" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Itinéraire</a><a class="btn btn--ghost" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div></div>
  <div class="map" data-reveal="fade"><iframe title="Carte : Mama Africa Beauty, {STREET}, Payerne" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={quote('Mama Africa beauty shopping, Rue de Lausanne 38, 1530 Payerne')}&z=16&output=embed"></iframe></div>
</div></section>'''

def faq(items=FAQ):
    return '<div class="faq">' + "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in items) + '</div>'

REAL = [  # her own photos and footage
    ("reel-nattes", "Deux longues tresses collées, réalisées au salon"),
    ("realisation-tresses", "Pose de tresses avec ajout au salon"),
    ("transplas-4", "Quatre transplas réalisés au salon"),
    ("boutique-cheveux", "Le comptoir des cheveux et mèches"),
    ("salon-fauteuil", "Le coin shampoing du salon"),
]

def mosaic():
    figs = f'<figure data-reveal>{img(REAL[0][0], REAL[0][1], "(max-width: 960px) 100vw, 40vw")}<span class="tag-real">Fait au salon</span><figcaption>Tresses collées longues</figcaption></figure>'
    figs += f'<figure data-reveal style="aspect-ratio:4/5">{video("salon-tresses", "Pose de tresses au salon Mama Africa")}<span class="tag-real">En vrai</span><figcaption>Pose en cours</figcaption></figure>'
    figs += f'<figure data-reveal style="aspect-ratio:4/5">{img("transplas-4", REAL[2][1], "(max-width: 960px) 50vw, 25vw")}<span class="tag-real">Fait au salon</span><figcaption>Transplas</figcaption></figure>'
    figs += f'<figure data-reveal style="aspect-ratio:4/5">{img("boutique-cheveux", REAL[3][1], "(max-width: 960px) 50vw, 25vw")}<figcaption>Le mur des mèches</figcaption></figure>'
    figs += f'<figure data-reveal style="aspect-ratio:4/5">{video("salon-visite", "Visite de la boutique")}<figcaption>La boutique</figcaption></figure>'
    return f'<div class="mosaic">{figs}</div>'

# ================================================================ PAGES
def p_index():
    body = f'''
<section class="hero" data-braid-hero>
  <div class="hero-stick">
    <div class="wrap hero-grid">
      <div>
        {label("Salon de tresses africaines · Payerne")}
        <h1 class="h-xl">Tresses africaines à <span class="ul">Payerne{UL}</span>.</h1>
        <p class="lead">Box braids, bohème, twists, nattes, tissage et perruques. Sur nos modèles à 150 CHF, les paquets de mèches sont offerts.</p>
        <div class="btns"><button class="btn btn--sun" type="button" data-book>{I["cal"]}Réserver un rendez-vous</button><a class="btn btn--ghost" href="#offres">Voir les offres {I["arr"]}</a></div>
        <div class="proof"><span class="chip chip--sun">{I["gift"]}<b>Mèches offertes</b></span><a class="chip" href="{G_REVIEWS}" target="_blank" rel="noopener"><b>{G_RATING}</b>{STAR5}</a><span class="chip">{I["clock"]}Lun – Sam · 9h – 18h30</span></div>
      </div>
      <div class="hero-slot" data-braid-slot aria-hidden="true"><span class="hero-glow"></span><span class="hero-ring"></span></div>
    </div>
    <div class="hero-hint" aria-hidden="true">Défilez, la tresse se fait<i></i></div>
    <div class="hero-step" aria-hidden="true"><span>Le geste</span><b id="hero-step">Trois mèches</b></div>
  </div>
</section>

<section class="sec" id="offres" style="overflow:hidden">
  <div class="wrap"><div class="head"><div>{label("Offres du moment")}<h2 class="h-l" data-split>Les offres de la maison.</h2></div>
    <p class="lead" data-reveal>Faites tourner le carrousel, touchez une offre pour le détail, l'affiche et la réservation.</p></div></div>
  {ring()}
</section>

<section class="sec sec--sand" id="codes">
  <div class="wrap"><div class="head"><div>{label("Le catalogue")}<h2 class="h-l" data-split>Choisissez votre code.</h2></div>
    <p class="lead" data-reveal>Neuf modèles de nattes et tresses. Choisissez votre code, réservez-le en un message.</p></div>
  {codes_block()}</div>
</section>

<section class="sec" id="tarifs">
  <div class="wrap"><div class="head"><div>{label("Prestations & tarifs")}<h2 class="h-l" data-split>Des prix clairs.</h2></div>
    <a class="link" href="tarifs">Tous les tarifs {I["arr"]}</a></div>
  {tabs_block()}</div>
</section>

<section class="sec sec--sand"><div class="wrap">{swatches_block()}</div></section>

<section class="sec">
  <div class="wrap"><div class="head"><div>{label("Fait chez nous")}<h2 class="h-l" data-split>Le salon, en vrai.</h2></div>
    <p class="lead" data-reveal>Pas de filtre : nos réalisations, notre mur de mèches, notre boutique.</p></div>
  {mosaic()}
  <div class="btns" style="margin-top:28px"><a class="btn" href="galerie">Toute la galerie {I["arr"]}</a><a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}{IG_HANDLE}</a></div></div>
</section>

<section class="sec sec--sand" style="overflow:hidden">{reviews_block()}</section>

<section class="sec">
  <div class="wrap"><div class="head"><div>{label("La boutique")}<h2 class="h-l" data-split>Tout pour vos cheveux.</h2></div>
    <p class="lead" data-reveal>Mèches, perruques, soins capillaires, cosmétiques et produits africains. Ouvert sans rendez-vous.</p></div>
  <div class="prods">{"".join(f'<div data-reveal>{img(f"produit-{i}", "Produit capillaire en boutique", "(max-width: 760px) 50vw, 20vw")}</div>' for i in (1, 4, 5, 9, 10))}</div>
  <div class="brands" style="margin-top:26px" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div>
  <div class="btns" style="margin-top:30px"><a class="btn" href="boutique">La boutique {I["arr"]}</a></div></div>
</section>
{book_band()}
{visit()}'''
    return page("index", "Mama Africa Beauty · Tresses africaines à Payerne",
                "Salon de tresses africaines à Payerne : box braids, bohème, twists, nattes, tissage, perruques. Mèches offertes sur nos modèles à 150 CHF. Réservation Salonkee, WhatsApp ou téléphone.", body)

def p_tresses():
    styles = [o for o in OFFERS if o["id"] in ("tresses-africaines", "boheme", "twist-curly", "rasta-elegance", "perles")]
    more = [
        dict(title="Rasta longues", price="165", img="box-braids-dos", badge="Locks longues", lead="Nattes collées avec locks longues, posées une à une.", incl=["Longueur jusqu'au bas du dos", "Mèches en vente au salon"]),
        dict(title="Rasta courtes", price="100", img="box-braids-sourire", badge="Mi-longues", lead="Nattes collées avec locks courtes, à hauteur d'épaules.", incl=["Pratique au quotidien", "Mèches en vente au salon"]),
        dict(title="Diverses tresses avec ajout", price="110", img="tresses-miel", badge="Sur mesure", lead="Tresses variées avec mèches : knotless, fines, épaisses, colorées.", incl=["Toutes tailles", "Toutes couleurs"]),
        dict(title="Nattes simples", price="70", img="nattes-chignon", badge="Sans ajout", lead="Nattes simples et naturelles, sur vos propres cheveux.", incl=["Lignes droites ou motifs", "Enfants bienvenus"]),
        dict(title="Crochet bouclé", price="120", img="crochet-volume", badge="Cheveux inclus", lead="Quatre bouclés au choix, chacun en quatre coloris. Cheveux et pose compris.", incl=["Classique, volume, naturel, tendance", "Cheveux inclus"]),
        dict(title="Transplas", price="65", pre="dès", img="transplas-4", badge="Fait au salon", lead="Deux transplas 65 CHF, quatre transplas 100 CHF. Propre, élégant, durable.", incl=["Adultes et enfants", "Cheveux à acheter sur place"]),
    ]
    cards = "".join(offer_card(o) for o in styles) + "".join(offer_card(dict(o, flyer=None, id="")) for o in more)
    body = phero("Tresses", "Tresses & nattes", "Toutes les tresses, au même endroit.",
                 "Box braids, bohème, twist & curly, rasta, perles, nattes, crochet et transplas. Choisissez votre style ou votre code, nous nous occupons du reste.",
                 img("reel-nattes", "Tresses collées réalisées au salon", "(max-width: 960px) 90vw, 500px", eager=True) + '<span class="tag-real">Fait au salon</span>', sticker=("Mèches offertes dès", "150 CHF")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="cards">{cards}</div>
<p class="note">{I["info"]}La durée dépend du modèle, de la longueur et de l'épaisseur. Envoyez une photo sur WhatsApp pour une estimation.</p></div></section>
<section class="sec sec--sand" id="codes"><div class="wrap"><div class="head"><div>{label("Le catalogue")}<h2 class="h-l" data-split>Choisissez votre code.</h2></div><p class="lead" data-reveal>Le modèle qui vous plaît, réservé en un message.</p></div>{codes_block()}</div></section>
<section class="sec"><div class="wrap">{swatches_block()}</div></section>
{book_band()}'''
    return page("tresses", "Tresses africaines à Payerne · Box braids, bohème, rasta | Mama Africa",
                "Box braids, tresses bohème, twist & curly, rasta longues et courtes, modèles avec perles, nattes, crochet et transplas à Payerne. Mèches offertes dès 150 CHF.", body, og="box-braids-longues")

def p_tissage():
    items = [o for o in OFFERS if o["id"] in ("tissage", "extensions-longues")]
    items.append(dict(title="Extensions", price="135", img="tissage-ondule", badge="Classique", lead="Pose d'extensions ou tissage, en cheveux naturels disponibles au salon.", incl=["Cheveux naturels en boutique", "Pose soignée"], flyer=None, id=""))
    body = phero("Tissage", "Tissage & extensions", "De la longueur, en toute discrétion.",
                 "Tissage cousu sur nattes, extensions longues lisses ou bouclées : un résultat naturel, coiffage compris.",
                 img("extensions-lisses", "Longs cheveux lisses", "(max-width: 960px) 90vw, 500px", eager=True), sticker=("Dès", "135 CHF")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="cards">{"".join(offer_card(o) for o in items)}</div></div></section>
<section class="sec sec--sand"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5" data-reveal>{img("boutique-cheveux", "Cheveux naturels en vente au salon", "(max-width: 960px) 100vw, 45vw")}<span class="tag-real">Au salon</span></div>
  <div>{label("Les cheveux")}<h2 class="h-l" data-split>Choisis avec vous, au salon.</h2>
  <div class="prose" style="margin-top:20px" data-reveal><p>Cheveux naturels lisses, ondulés ou bouclés : le comptoir de la boutique propose de quoi réaliser votre tissage ou vos extensions, dans la longueur et la couleur que vous voulez.</p><p>Nous vous conseillons sur la quantité nécessaire avant la pose.</p></div></div>
</div></section>
{book_band()}'''
    return page("tissage", "Tissage & extensions à Payerne | Mama Africa Beauty",
                "Tissage cousu sur nattes dès 135 CHF, extensions 135 CHF, extensions longues 150 CHF à Payerne. Coiffage inclus.", body, og="tissage-ondule")

def p_soins():
    reno = [o for o in OFFERS if o["id"] == "renovation-perruque"][0]
    soins = [
        dict(title="Défrisage", price="65", img="lissage", badge="Lissage", lead="Défrisage et soin protecteur, appliqués avec méthode.", incl=["Soin protecteur inclus"]),
        dict(title="Brushing", price="65", img="afro-studio", badge="Coiffage", lead="Brushing simple ou wavy, pour sublimer votre texture.", incl=["Simple ou wavy"]),
        dict(title="Bio-plastie capillaire", price="95", img="hands-scalp", badge="Clinique", lead="Soin reconstructeur en profondeur pour cheveux fragilisés.", incl=["Sur rendez-vous téléphonique"]),
        dict(title="Traitement Lowell", price="95", img="products-terracotta", badge="Gamme Lowell", lead="Le soin aux produits Lowell, la gamme brésilienne vendue en boutique.", incl=["Produits en vente au salon"]),
        dict(title="Soin lisses ou ondulés", price="85", img="afro-glam", badge="Hydratation", lead="Nourrir, discipliner, faire briller.", incl=["Cheveux lisses ou ondulés"]),
        dict(title="Coupe & teinture", price="45", pre="dès", img="curls-portrait", badge="Forme & couleur", lead="Coupe 45 CHF, teinture 55 CHF.", incl=["Du crépu au lisse"]),
    ]
    body = phero("Soins & perruques", "Soins, lissage & perruques", "Des cheveux en bonne santé.",
                 "Défrisage, brushing, bio-plastie, soins Lowell, coupe et couleur. Et vos perruques retrouvent une seconde vie.",
                 img("afro-or", "Cheveux afro naturels et soignés", "(max-width: 960px) 90vw, 500px", eager=True), sticker=("Rénovation perruque", "110 CHF")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="cards">{offer_card(reno)}{"".join(offer_card(dict(o, flyer=None, id="")) for o in soins)}</div></div></section>
{book_band()}'''
    return page("soins", "Soins capillaires, défrisage & rénovation de perruque à Payerne | Mama Africa",
                "Défrisage 65 CHF, brushing 65 CHF, rénovation de perruque 110 CHF, bio-plastie, soins Lowell, coupe et teinture à Payerne.", body, og="perruque-glam")

def p_beaute():
    items = [dict(title="Extension de cils · cil à cil", price=None, img="neneth-certificat", badge="Certifiée", lead="Une extension sur chaque cil naturel, pour un regard intense et naturel.", incl=["Technique certifiée"]),
             dict(title="Volume russe", price=None, img="makeup", badge="Volume", lead="Des bouquets ultra-fins pour un regard plus dense, toujours léger.", incl=["Technique certifiée"]),
             dict(title="Sourcils & maquillage", price=None, img="portrait-gold", badge="Mise en beauté", lead="Épilation des sourcils et maquillage pour vos événements.", incl=["Mariage, soirée, photo"])]
    body = phero("Beauté", "Regard & maquillage", "La beauté jusqu'au bout des cils.",
                 "Extensions de cils cil à cil et volume russe, sourcils et maquillage, par une spécialiste certifiée.",
                 video("beaute-maquillage", "Essai de rouges à lèvres")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="cards">{"".join(offer_card(dict(o, flyer=None, id="")) for o in items)}</div>
<p class="note">{I["info"]}Tarifs communiqués sur demande selon la technique. Écrivez-nous sur WhatsApp.</p></div></section>
{book_band()}'''
    return page("beaute", "Extensions de cils, sourcils & maquillage à Payerne | Mama Africa", "Extensions de cils cil à cil et volume russe, sourcils et maquillage à Payerne, par une spécialiste certifiée.", body, og="makeup")

def p_offres():
    body = phero("Offres", "Offres du moment", "Les offres de la maison.",
                 "Mèches offertes, cheveux inclus, prix ronds : les offres en cours au salon. Touchez « Voir l'affiche » pour l'affiche originale.",
                 img("boheme-2", "Tresses bohème", "(max-width: 960px) 90vw, 500px", eager=True), sticker=("2 paquets offerts", "150 CHF")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px);overflow:hidden">{ring()}</section>
<section class="sec sec--sand"><div class="wrap"><div class="cards">{"".join(offer_card(o) for o in OFFERS)}</div></div></section>
{book_band()}'''
    return page("offres", "Offres du moment · Mama Africa Beauty Payerne", "Tresses africaines 150 CHF mèches offertes, bohème 150 CHF 2 paquets offerts, perles 130 CHF, tissage dès 135 CHF, rénovation de perruque 110 CHF.", body, og="boheme-1")

def p_tarifs():
    body = phero("Tarifs", "Tarifs 2026", "Investissement beauté.",
                 "Tous nos tarifs, selon la liste en vigueur au salon. Les paquets de mèches sont offerts sur nos modèles à 150 CHF.",
                 img("affiche-tarifs", "Affiche des tarifs Mama Africa", "(max-width: 960px) 90vw, 500px", eager=True)) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">{tabs_block()}
<p class="note">{I["info"]}Prix en francs suisses. Mèches non comprises sauf mention « offertes » ou « inclus » : elles s'achètent au salon. La bio-plastie se réserve par téléphone.</p>
<div class="btns" style="margin-top:28px"><a class="btn btn--sun" href="{SALONKEE}" target="_blank" rel="noopener">{I["cal"]}Réserver sur Salonkee</a><button class="btn btn--ghost" type="button" data-flyer="affiche-tarifs">Voir l'affiche des tarifs</button></div></div></section>
<section class="sec sec--sand" id="codes"><div class="wrap"><div class="head"><div>{label("Le catalogue")}<h2 class="h-l" data-split>Tarifs par code.</h2></div></div>{codes_block()}</div></section>
{book_band()}'''
    return page("tarifs", "Tarifs · Tresses, tissage, soins | Mama Africa Beauty Payerne", "Nattes 70 CHF, rasta courtes 100 CHF, tresses avec ajout 110 CHF, extensions 135 CHF, rasta longues 165 CHF, défrisage 65 CHF, brushing 65 CHF.", body, og="affiche-tarifs")

def p_boutique():
    cats = "".join(f'<div class="cat" data-reveal><span class="num">{i:02d}</span><b>{t}</b><small>{d}</small></div>' for i, (t, d) in enumerate(BOUTIQUE_CATS, 1))
    body = phero("Boutique", "La boutique", "Tout pour vos cheveux, sous un même toit.",
                 "Mèches, perruques, soins capillaires, cosmétiques, accessoires et produits africains. Ouvert du lundi au samedi, sans rendez-vous.",
                 video("salon-visite", "Visite de la boutique"),
                 extra=f'<div class="btns" style="margin-top:30px" data-reveal><a class="btn btn--sun" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Venir à la boutique</a><a class="btn btn--ghost" href="{wa("Bonjour Mama Africa, avez-vous ce produit en stock ?")}" target="_blank" rel="noopener">{I["wa"]}Demander un produit</a></div>') + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="cats">{cats}</div></div></section>
<section class="sec sec--sand"><div class="wrap"><div class="head"><div>{label("En rayon")}<h2 class="h-l" data-split>Les soins que vos boucles réclament.</h2></div></div>
<div class="prods">{"".join(f'<div data-reveal>{img(f"produit-{i}", "Produit en vente à la boutique", "(max-width: 760px) 50vw, 20vw")}</div>' for i in range(1, 11))}</div>
<div class="brands" style="margin-top:26px" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div></div></section>
<section class="sec"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5" data-reveal>{img("boutique-allee", "Les rayons de la boutique", "(max-width: 960px) 100vw, 45vw")}<span class="tag-real">La boutique</span></div>
  <div>{label("Conseil")}<h2 class="h-l" data-split>On vous aide à choisir.</h2><div class="prose" style="margin-top:20px" data-reveal><p>Quel masque pour des cheveux secs ? Combien de paquets pour des rastas longues ? Quelle couleur pour un crochet ? Passez nous voir ou écrivez-nous.</p></div>
  <button class="btn btn--ghost" type="button" data-flyer="affiche-boutique" style="margin-top:8px">Voir l'affiche de la boutique</button></div>
</div></section>
{visit()}'''
    return page("boutique", "Boutique beauté afro à Payerne · Mèches, perruques, soins | Mama Africa", "Mèches, perruques, soins capillaires pour cheveux texturés, cosmétiques et produits africains à Payerne.", body, og="produit-10")

GALLERY = [
    ("reel-nattes", "Tresses collées longues", "tresses", True), ("box-braids-longues", "Box braids longues", "tresses", False),
    ("realisation-tresses", "Pose de tresses au salon", "tresses", True), ("boheme-1", "Tresses bohème", "tresses", False),
    ("transplas-4", "Transplas", "tresses", True), ("perles-1", "Tresses avec perles", "tresses", False),
    ("boutique-cheveux", "Cheveux et mèches au comptoir", "salon", True), ("nattes-motif", "Nattes à motif", "tresses", False),
    ("crochet-volume", "Crochet bouclé volume", "tresses", True), ("tissage-ondule", "Tissage ondulé", "tissage", False),
    ("salon-fauteuil", "Le coin shampoing", "salon", True), ("boheme-3", "Twist & curly", "tresses", False),
    ("realisation-tresses-2", "Tresses en cours", "tresses", True), ("extensions-lisses", "Extensions lisses", "tissage", False),
    ("boutique-allee", "Les rayons soins", "salon", True), ("nattes-queue", "Nattes en queue haute", "tresses", False),
    ("crochet-tendance", "Crochet bouclé tendance", "tresses", True), ("perruque-glam", "Perruque", "tissage", False),
    ("salon-rose", "Le coin beauté", "salon", True), ("perles-4", "Perles et tresses fines", "tresses", False),
    ("produit-10", "Gamme Mielle", "salon", True), ("nattes-relevees", "Nattes relevées", "tresses", False),
]

def p_galerie():
    figs = "".join(f'<figure data-cat="{c}" data-reveal>{img(n, cap, "(max-width: 760px) 100vw, 33vw")}<span class="src{" is-real" if real else ""}">{"Salon" if real else "Inspiration"}</span><figcaption class="sr">{cap}</figcaption></figure>' for n, cap, c, real in GALLERY)
    flyers = ["affiche-promo-boheme", "affiche-twist-curly", "affiche-perles", "affiche-rasta-135", "affiche-tissage", "affiche-extensions", "affiche-renovation-perruque", "affiche-codes", "affiche-tarifs", "affiche-boutique"]
    figs += "".join(f'<figure data-cat="affiches" data-reveal>{img(f, "Affiche Mama Africa", "(max-width: 760px) 100vw, 33vw")}<span class="src is-real">Affiche</span><figcaption class="sr">Affiche Mama Africa</figcaption></figure>' for f in flyers)
    filt = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in [("all", "Tout"), ("tresses", "Tresses"), ("tissage", "Tissage & perruques"), ("salon", "Salon & boutique"), ("affiches", "Affiches")])
    body = phero("Galerie", "Réalisations & inspirations", "Regardez, choisissez.",
                 "Nos réalisations et les coulisses du salon (étiquette « Salon »), des inspirations pour votre prochain style, et nos affiches.",
                 img("nattes-motif", "Nattes à motif", "(max-width: 960px) 90vw, 500px", eager=True)) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap"><div class="filters" role="group" aria-label="Filtrer">{filt}</div><div class="masonry" id="masonry">{figs}</div></div></section>
{book_band()}'''
    return page("galerie", "Galerie · Tresses et coiffures africaines | Mama Africa Payerne", "Réalisations du salon Mama Africa à Payerne, inspirations et affiches : tresses, bohème, perles, nattes, tissage, perruques.", body, og="reel-nattes")

def p_salon():
    body = phero("Le salon", "Notre histoire", "Mama Africa, la beauté africaine à Payerne.",
                 "Un salon de tresses africaines et une boutique de beauté, réunis Rue de Lausanne 38B.",
                 video("salon-tresses", "Pose de tresses au salon")) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap split">
  <div>{label("Qui sommes-nous")}<h2 class="h-l" data-split>Venez pour les produits, restez pour la coiffure.</h2></div>
  <div class="prose" data-reveal><p><b>Mama Africa</b> est une boutique de cosmétiques et de soins capillaires tournée vers la beauté naturelle et l'identité africaine, avec des produits pour tous les types de cheveux, en particulier crépus, bouclés et en transition.</p><p>Mais notre vrai cœur, c'est le salon : tresses, nattes, tissage, soins, coiffures africaines traditionnelles et modernes. Chaque rendez-vous est une expérience où beauté rime avec authenticité.</p><p><b>{SLOGAN}</b></p></div>
</div></section>
<section class="sec sec--sand"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5" data-reveal>{img("neneth-certificat", "Neneth avec son certificat d'extension de cils", "(max-width: 960px) 100vw, 45vw")}</div>
  <div>{label("La fondatrice")}<h2 class="h-l" data-split>Neneth.</h2><div class="prose" style="margin-top:20px" data-reveal><p>Avant Mama Africa, il y avait <b>Neneth Beauty</b>, spécialiste des extensions de cils, certifiée cil à cil et volume russe. Neneth a fait grandir son activité jusqu'à ouvrir une adresse qui réunit le geste et le produit.</p></div>
  <div class="btns" style="margin-top:24px"><a class="btn" href="beaute">Beauté du regard {I["arr"]}</a><a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}Instagram</a></div></div>
</div></section>
<section class="sec"><div class="wrap"><div class="head"><div>{label("Le lieu")}<h2 class="h-l" data-split>Un salon plein de couleurs.</h2></div></div>{mosaic()}</div></section>
{book_band()}'''
    return page("salon", "Le salon · Notre histoire | Mama Africa Beauty Payerne", "Mama Africa, salon de tresses africaines et boutique beauté à Payerne, fondé par Neneth.", body, og="salon-fauteuil")

def p_avis():
    body = phero("Avis", "Avis Google", "Ce qu'elles disent de nous.",
                 "Merci à toutes celles et ceux qui partagent leur expérience. Votre avis aide d'autres femmes à nous trouver.",
                 img("afro-bijoux", "Cliente souriante", "(max-width: 960px) 90vw, 500px", eager=True), sticker=("Google", "5,0 ★"),
                 extra=f'<div class="btns" style="margin-top:30px" data-reveal><a class="btn btn--sun" href="{G_WRITE}" target="_blank" rel="noopener">{I["g"]}Laisser un avis</a><a class="btn btn--ghost" href="{G_REVIEWS}" target="_blank" rel="noopener">Voir sur Google</a></div>') + f'''
<section class="sec sec--sand" style="overflow:hidden">{reviews_block()}</section>
{book_band()}'''
    return page("avis", "Avis clients · Mama Africa Beauty Payerne", "Avis Google sur Mama Africa Beauty, salon de tresses africaines à Payerne.", body, og="afro-bijoux")

def p_reservation():
    groups = [("Tresses", [(n, p) for n, p, d in MENU["tresses"][1]]), ("Tissage & extensions", [(n, p) for n, p, d in MENU["tissage"][1]]),
              ("Soins & perruques", [(n, p) for n, p, d in MENU["soins"][1]]), ("Beauté", [(n, p) for n, p, d in MENU["beaute"][1]])]
    def num(p):
        try: return int(str(p).split("/")[0].replace("dès", "").strip())
        except Exception: return 0
    def chip(n, p):
        lbl = (p + " CHF") if p else "sur demande"
        return f'<label><input type="checkbox" name="svc" value="{esc(n)}" data-price="{num(p)}"><span>{n}<em>{lbl}</em></span></label>'
    picks = "".join(f'<div class="field"><span class="lbl">{g}</span><div class="pick">{"".join(chip(n, p) for n, p in items)}</div></div>' for g, items in groups)
    codes = "".join(f'<label><input type="radio" name="code" value="{c}"><span>Code {c}<em>{p} CHF</em></span></label>' for c, p in CODES)
    form = f'''<form class="form form-card" id="book-form" novalidate>
  <h2 class="h-m">Demande de rendez-vous</h2><p class="hint">Votre demande s'ouvre dans WhatsApp, prête à envoyer. Nous confirmons par message.</p>
  {picks}<div class="field"><span class="lbl">Un modèle du catalogue ? (facultatif)</span><div class="pick">{codes}</div></div>
  <div class="form-total"><span>Estimation</span><b id="bf-total">0 CHF</b></div>
  <div class="two"><div class="field"><label for="bf-date">Date souhaitée</label><input id="bf-date" name="date" type="date"></div>
  <div class="field"><label for="bf-time">Moment</label><select id="bf-time" name="time"><option>Matin (9h – 12h)</option><option>Midi (12h – 14h)</option><option>Après-midi (14h – 18h30)</option><option>Peu importe</option></select></div></div>
  <div class="two"><div class="field"><label for="bf-name">Prénom et nom</label><input id="bf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="bf-tel">Téléphone</label><input id="bf-tel" name="tel" type="tel" autocomplete="tel"></div></div>
  <div class="field"><label for="bf-msg">Couleur, longueur, questions</label><textarea id="bf-msg" name="msg" placeholder="Ex. couleur 27, longueur bas du dos…"></textarea></div>
  <button class="btn btn--wa" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button>
  <p class="hint">Aucune donnée n'est enregistrée sur ce site.</p>
</form>'''
    body = phero("Réserver", "Rendez-vous", "Réservez votre moment.",
                 "En ligne sur Salonkee, sur WhatsApp ou par téléphone. Ou détaillez votre demande dans le formulaire.",
                 img("salon-fauteuil", "Le salon Mama Africa", "(max-width: 960px) 90vw, 500px", eager=True), extra=f'<div style="margin-top:30px" data-reveal>{ways(light=True)}</div>') + f'''
<section class="sec" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap split" style="align-items:start">
  {form}<div>{label("Horaires")}{hours_list()}<div style="margin-top:44px">{label("Questions fréquentes")}{faq()}</div></div>
</div></section>'''
    return page("reservation", "Réserver · Mama Africa Beauty Payerne", "Réservez vos tresses, tissage, soins ou prestation beauté à Payerne : Salonkee, WhatsApp ou 078 259 77 38.", body, og="salon-fauteuil")

def p_contact():
    form = f'''<form class="form form-card" id="contact-form" novalidate><h2 class="h-m">Écrivez-nous</h2>
  <div class="two"><div class="field"><label for="cf-name">Prénom et nom</label><input id="cf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="cf-subj">Sujet</label><select id="cf-subj" name="subj"><option>Rendez-vous coiffure</option><option>Offre du moment</option><option>Produit de la boutique</option><option>Rénovation de perruque</option><option>Autre</option></select></div></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="msg" required></textarea></div>
  <button class="btn btn--wa" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button><p class="hint">Le message s'ouvre dans WhatsApp. Aucune donnée n'est enregistrée sur ce site.</p></form>'''
    body = phero("Contact", "Contact", "Parlons de vos cheveux.",
                 "Une question sur un modèle, une offre, un produit ? Appelez, écrivez sur WhatsApp ou passez au salon.",
                 img("boutique-allee", "La boutique Mama Africa", "(max-width: 960px) 90vw, 500px", eager=True), extra=f'<div style="margin-top:30px" data-reveal>{ways(light=True)}</div>') + f'''
<section class="sec" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap split" style="align-items:start">{form}<div>{label("Questions fréquentes")}{faq(FAQ[:4])}</div></div></section>
{visit()}'''
    return page("contact", "Contact · Mama Africa Beauty, Rue de Lausanne 38B, Payerne", "Mama Africa Beauty, Rue de Lausanne 38B, 1530 Payerne. 078 259 77 38, WhatsApp, Instagram. Lundi – samedi 9h00 – 18h30.", body, og="boutique-allee")

def p_conf():
    body = f'''<section class="sec" style="padding-top:calc(var(--hdr) + 70px)"><div class="wrap" style="max-width:820px">{label("Informations légales")}<h1 class="h-l">Confidentialité</h1>
<div class="prose" style="margin-top:30px"><p><b>Éditeur.</b> {NAME}, {STREET}, {CITY}, Suisse. {PHONE}.</p>
<p><b>Données.</b> Ce site n'enregistre aucune donnée. Les formulaires préparent un message WhatsApp que vous envoyez vous-même. Les réservations en ligne passent par Salonkee.</p>
<p><b>Services tiers.</b> La carte est fournie par Google Maps, qui peut déposer des cookies. Les liens Instagram, WhatsApp, Salonkee et Google ouvrent ces services, soumis à leurs propres règles.</p>
<p><b>Navigateur.</b> Le site retient la couleur de mèche choisie le temps de votre visite (stockage de session), rien de plus.</p>
<p><b>Crédits.</b> Photos du salon, de la boutique et affiches : {NAME}. Photos d'inspiration : Unsplash et Pexels.</p></div></div></section>'''
    return page("confidentialite", "Confidentialité · Mama Africa Beauty", "Informations légales et confidentialité.", body)

def p_404():
    body = f'<section class="nf"><div>{label("Erreur 404")}<h1 class="h-xl">Cette page s\'est dé-tressée.</h1><p class="lead" style="margin:22px auto 30px">La page demandée n\'existe pas.</p><div class="btns" style="justify-content:center"><a class="btn" href="./">Accueil</a><button class="btn btn--sun" type="button" data-book>{I["cal"]}Réserver</button></div></div></section>'
    return page("404", "Page introuvable · Mama Africa Beauty", "Page introuvable.", body)

PAGES = {"index": p_index, "tresses": p_tresses, "tissage": p_tissage, "soins": p_soins, "beaute": p_beaute, "offres": p_offres,
         "tarifs": p_tarifs, "boutique": p_boutique, "galerie": p_galerie, "salon": p_salon, "avis": p_avis,
         "reservation": p_reservation, "contact": p_contact, "confidentialite": p_conf, "404": p_404}

if __name__ == "__main__":
    for f in os.listdir(ROOT):  # remove pages that no longer exist
        if f.endswith(".html") and f[:-5] not in PAGES:
            os.remove(os.path.join(ROOT, f))
    for slug, fn in PAGES.items():
        with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{'' if s == 'index' else s}</loc></url>\n" for s in PAGES if s != "404") + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\n" + ("Disallow: /\n" if PITCH else f"Allow: /\nSitemap: {BASE}sitemap.xml\n"))
    print("built", len(PAGES), "pages")
