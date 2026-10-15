# -*- coding: utf-8 -*-
"""Static generator for the Mama Africa site (v3, editorial, no 3D). Run: python3 _build/build.py
Writes every page to the repo root (GitHub Pages serves clean URLs)."""
import os, json, html, sys
from urllib.parse import quote
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from data import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
esc = html.escape

I = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-.99.24-3.33-.69-2.81-1.11-4.6-3.98-4.74-4.17-.14-.18-1.13-1.5-1.13-2.87s.72-2.03.97-2.31c.26-.28.56-.35.74-.35l.54.01c.17 0 .41-.07.64.49.25.58.83 2.01.9 2.15.08.14.12.3.03.49-.1.19-.14.3-.28.47-.14.16-.3.37-.42.49-.14.14-.29.29-.12.57.16.28.73 1.2 1.56 1.94 1.07.95 1.98 1.25 2.26 1.39.28.14.44.12.61-.07.16-.19.71-.83.9-1.11.19-.28.37-.23.63-.14.26.09 1.65.78 1.93.92.28.14.47.21.54.33.07.11.07.66-.18 1.35Z"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="1.5"/><path d="M8 2.5v4M16 2.5v4M3 10h18"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.3 7-12a7 7 0 1 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "arr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg>',
 "g": '<svg class="g-logo" viewBox="0 0 48 48" aria-label="Google"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>',
}
ARR_W = I["arr"].replace('<svg', '<svg class="arr"')
STARS = '<span class="stars" aria-label="5 étoiles sur 5">★★★★★</span>'
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

def wa(msg="Bonjour Mama Africa, j'aimerais prendre rendez-vous."):
    return f"https://wa.me/{WA}?text={quote(msg)}"

_d = {}
def dims(n):
    if n not in _d:
        try:
            with Image.open(os.path.join(IMG, n + ".webp")) as im: _d[n] = im.size
        except FileNotFoundError: _d[n] = (1200, 1500)
    return _d[n]

def img(n, alt, sizes="(max-width: 760px) 100vw, 50vw", eager=False, lazy=True, cls=""):
    w, h = dims(n)
    srcset = ""
    if os.path.exists(os.path.join(IMG, n + "-m.webp")):
        srcset = f' srcset="assets/img/{n}-m.webp {dims(n + "-m")[0]}w, assets/img/{n}.webp {w}w" sizes="{sizes}"'
    load = 'fetchpriority="high"' if eager else ('loading="lazy"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    return f'<img src="assets/img/{n}.webp"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async"{c}>'

def video(n, label="", cls="", poster=True):
    aria = f' aria-label="{esc(label)}"' if label else ' aria-hidden="true"'
    c = f' class="{cls}"' if cls else ""
    p = f' poster="assets/video/{n}.webp"' if poster else ""
    return f'<video{c} src="assets/video/{n}.mp4"{p} muted loop playsinline autoplay preload="metadata"{aria}></video>'

def kicker(t, c=False):
    return f'<p class="kicker{" kicker--c" if c else ""}">{t}</p>'

def veil(inner, ratio=None, cls="ph"):
    st = f' style="aspect-ratio:{ratio}"' if ratio else ""
    return f'<div class="{cls} veil"{st}>{inner}<span class="veil-c"></span></div>'

def chf(p, pre=None):
    if not p: return '<span class="pr" style="font-size:20px">Sur demande</span>'
    return f'<span class="pr">{("<em>" + pre + "</em>") if pre else ""}{p}<small>CHF</small></span>'

# ---------------------------------------------------------------- shell
NAV = [("index", "Accueil", "./"), ("tresses", "Tresses", "tresses"), ("hommes-enfants", "Hommes & enfants", "hommes-enfants"),
       ("tissage", "Tissage", "tissage"), ("soins", "Soins & perruques", "soins"), ("beaute", "Beauté", "beaute"),
       ("offres", "Offres", "offres"), ("tarifs", "Tarifs", "tarifs"), ("boutique", "Boutique", "boutique"),
       ("galerie", "Galerie", "galerie"), ("salon", "La maison", "salon"), ("avis", "Avis", "avis"), ("contact", "Contact", "contact")]
LEFT = ["tresses", "offres", "tarifs"]
RIGHT = ["boutique", "galerie", "contact"]

def header(cur, on_hero):
    a = lambda keys: "".join(f'<a href="{h}"{" aria-current=page" if s == cur else ""}>{l}</a>' for s, l, h in NAV if s in keys)
    mnav = "".join(f'<a class="big" href="{h}"><small>{ROMAN[i] if i < len(ROMAN) else i + 1}</small>{l}</a>' for i, (s, l, h) in enumerate(NAV))
    cls = " on-hero" if on_hero else ""
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="hdr{cls}" id="hdr"><div class="wrap">
  <nav class="nav" aria-label="Navigation">{a(LEFT)}</nav>
  <a class="mark" href="./" aria-label="Mama Africa, accueil"><img src="assets/img/logo-embleme.webp" width="582" height="582" alt=""><span>Mama Africa<small>Beauty · Payerne</small></span></a>
  <div class="hdr-cta"><nav class="nav nav--r" aria-label="Navigation (suite)">{a(RIGHT)}</nav><button class="btn" type="button" data-book>Réserver</button>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button></div>
</div></header>
<nav class="mnav" id="mnav" aria-label="Menu">{mnav}
  <div class="mnav-foot"><button class="btn btn--light" type="button" data-book>{I["cal"]}Réserver</button><a class="btn btn--line-light" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a><a class="btn btn--line-light" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div>
</nav>'''

def ways(light=False):
    c = " ways--light" if light else ""
    return f'''<div class="ways{c}">
  <a class="way" href="{SALONKEE}" target="_blank" rel="noopener"><span class="ic">{I["cal"]}</span><span><b>En ligne, sur Salonkee</b><small>Choisissez votre créneau, 24h/24</small></span>{ARR_W}</a>
  <a class="way" href="{wa()}" target="_blank" rel="noopener"><span class="ic">{I["wa"]}</span><span><b>Sur WhatsApp</b><small>Envoyez le code ou la photo du modèle</small></span>{ARR_W}</a>
  <a class="way" href="tel:{TEL}"><span class="ic">{I["tel"]}</span><span><b>{PHONE}</b><small>Du lundi au samedi, 9h00 – 18h30</small></span>{ARR_W}</a>
</div>'''

def hours_list():
    out = ""
    for i, (d, o, c) in enumerate(HOURS):
        v = f"{o.replace(':', 'h')} – {c.replace(':', 'h')}" if o else '<span class="off">Fermé</span>'
        out += f'<li data-day="{(i + 1) % 7}"><span>{d}</span><span>{v}</span></li>'
    return f'<ul class="hours">{out}</ul>'

def footer():
    col = lambda keys: "".join(f'<li><a href="{h}">{l}</a></li>' for s, l, h in NAV if s in keys)
    return f'''<footer class="ftr"><div class="wrap">
  <p class="ftr-mark" aria-hidden="true">Mama Africa</p>
  <div class="ftr-sub"><p>Votre beauté, notre passion.</p><a class="tlink" href="reservation" style="color:var(--on-dark)">Prendre rendez-vous {I["arr"]}</a></div>
  <div class="ftr-grid">
    <div><a class="logo" href="./"><img src="assets/img/logo-embleme.webp" width="582" height="582" alt="Mama Africa Beauty Shop" loading="lazy"></a>
      <p class="small">Maison de tresses africaines et boutique beauté, au centre de Payerne.</p>
      <div class="socials"><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a><a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["wa"]}</a><a href="{GMAPS}" target="_blank" rel="noopener" aria-label="Google Maps">{I["pin"]}</a><a href="{SALONKEE}" target="_blank" rel="noopener" aria-label="Salonkee">{I["cal"]}</a></div></div>
    <div><h4>Coiffure</h4><ul>{col(["tresses", "hommes-enfants", "tissage", "soins", "beaute"])}</ul></div>
    <div><h4>La maison</h4><ul>{col(["offres", "tarifs", "boutique", "galerie", "salon", "avis"])}</ul></div>
    <div><h4>Nous trouver</h4><ul><li><a href="{GMAPS}" target="_blank" rel="noopener">{STREET}<br>{CITY}</a></li><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></li><li style="color:var(--on-dark-2)">Lundi – samedi<br>9h00 – 18h30</li></ul></div>
  </div>
  <div class="ftr-bot"><span>© 2026 {NAME}, Payerne</span><span><a href="contact">Contact</a> · <a href="confidentialite">Confidentialité</a></span></div>
</div></footer>'''

def overlays(away):
    return f'''<div class="abar{" is-away" if away else ""}" id="abar">
  <a class="a-tel" href="tel:{TEL}" aria-label="Appeler le {PHONE}">{I["tel"]}Appeler</a>
  <a class="a-wa" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a>
  <button class="a-book" type="button" data-book>{I["cal"]}Réserver</button>
</div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-t" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-panel"><button class="x" type="button" data-close aria-label="Fermer">{I["x"]}</button>
    {kicker("Rendez-vous")}<h2 class="d-m" id="sheet-t" style="margin-bottom:26px">Comment souhaitez-vous réserver&nbsp;?</h2>
    {ways(light=True)}
    <p class="hint" style="margin-top:20px">Vous avez choisi un modèle ? <a href="tresses#codes" style="text-decoration:underline">Réservez par code</a>.</p>
  </div>
</div>
<div class="lb" id="lb" aria-hidden="true"><button class="x" type="button" aria-label="Fermer">{I["x"]}</button><button class="pv" type="button" aria-label="Précédente">{I["prev"]}</button><img alt=""><button class="nx" type="button" aria-label="Suivante">{I["arr"]}</button><p></p></div>
<div class="hover-img" id="hover-img" aria-hidden="true"><img alt=""></div>'''

def schema():
    d = {"@context": "https://schema.org", "@type": "HairSalon", "name": NAME, "slogan": SLOGAN,
         "image": BASE + "assets/img/logo.png", "url": BASE, "telephone": TEL, "priceRange": "CHF 45 – 165",
         "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressRegion": "VD", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:30"}],
         "sameAs": [INSTAGRAM, SALONKEE, GMAPS]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def page(slug, title, desc, body, og="box-braids-longues", on_hero=True):
    url = BASE + ("" if slug == "index" else slug)
    robots = '<meta name="robots" content="noindex, nofollow">' if PITCH else ""
    return f'''<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1b120d">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CH"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/{og}.webp">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/bodoni.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={V}">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__ma)document.documentElement.classList.remove('js')}},3500)</script>
{schema() if slug in ("index", "contact") else ""}
</head>
<body data-page="{slug}">
{header(slug, on_hero)}
<main id="main">
{body}
</main>
{footer()}
{overlays(slug == "index")}
<script>window.MA_WA="{WA}";</script>
<script src="assets/js/vendor/lenis.min.js"></script>
<script src="assets/js/vendor/gsap.min.js"></script>
<script src="assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="assets/js/site.js?v={V}"></script>
</body>
</html>'''

# ---------------------------------------------------------------- blocks
def phero(crumb, kick, h1, lede, bg, badge=None):
    b = f'<div class="badge" data-reveal><small>{badge[0]}</small><b>{badge[1]}<small>CHF</small></b></div>' if badge else ""
    return f'''<section class="phero"><div class="bg">{bg}</div>
<div class="wrap"><nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>/</span><span>{crumb}</span></nav>
{kicker(kick)}<h1 class="d-xl" data-reveal>{h1}</h1><p class="lede" data-reveal>{lede}</p></div>{b}</section>'''

def sig(o, i):
    return f'''<article class="sig"><a href="offres#{o["id"]}" aria-label="{esc(o["title"])}">
  {veil(img(o["img"], o["title"], "(max-width: 760px) 78vw, 400px") + f'<span class="tag">{o["badge"]}</span>')}
  <div class="cap"><span class="num">{i:02d}</span><h3>{o["title"]}</h3>{chf(o["price"], o.get("pre"))}<p>{o["incl"][0]}</p></div></a></article>'''

def rail(items):
    cards = "".join(sig(o, i) for i, o in enumerate(items, 1))
    return f'''<div class="rail-wrap"><div class="rail" id="rail">{cards}</div>
<div class="wrap rail-ctrl"><div class="rail-bar" aria-hidden="true"><i></i></div><div class="arrows"><button type="button" data-rail="-1" aria-label="Précédent">{I["prev"]}</button><button type="button" data-rail="1" aria-label="Suivant">{I["arr"]}</button></div></div></div>'''

CARTE_IMG = {
    "Nattes simples": "nattes-chignon", "Rasta courtes": "box-braids-sourire", "Diverses tresses avec ajout": "tresses-miel",
    "Tresses avec perles": "perles-1", "Rasta longues · Élégance": "nattes-portrait", "Tresses africaines": "box-braids-longues",
    "Tresses bohème · 4 modèles": "boheme-1", "Twist & Curly": "boheme-3", "Rasta longues": "box-braids-dos",
    "Crochet bouclé": "crochet-volume", "Transplas · 2 / 4 tresses": "transplas-4",
    "Tresses hommes · 6 modèles": "homme-tresses", "Tresses enfants avec perles colorées": "enfant-perles-3",
    "Extensions": "tissage-ondule", "Tissage cousu sur nattes": "tissage-ondule", "Extensions longues": "extensions-lisses",
    "Défrisage des cheveux": "lissage", "Brushing": "afro-studio", "Rénovation de perruque": "perruque-glam",
    "Bio-plastie capillaire": "hands-scalp", "Soin cheveux lisses ou ondulés": "afro-glam", "Traitement produits Lowell": "products-terracotta",
    "Coupe": "curls-portrait", "Teinture": "curls-eyes",
    "Extension de cils · cil à cil": "makeup", "Extension de cils · volume russe": "makeup", "Épilation des sourcils": "portrait-ochre-1", "Maquillage": "portrait-gold",
}

def carte(keys=("tresses", "famille", "tissage", "soins", "beaute"), intro=True):
    INTRO = {"tresses": "Mèches offertes ou incluses sur nos offres.", "famille": "Cornrows pour hommes, tresses à perles pour les enfants.",
             "tissage": "Coiffage compris.", "soins": "Pour cheveux crépus, bouclés, lisses ou en transition.", "beaute": "Par une spécialiste certifiée."}
    blocks = []
    for i, k in enumerate(keys):
        title, items = MENU[k]
        lis = ""
        for n, p, d in items:
            pr = f'{p}<small>CHF</small>' if p else '<small style="font-size:11px">Sur demande</small>'
            gift = " gift" if d and ("offert" in d or "inclus" in d.lower()) else ""
            dd = f'<span class="d{gift}">{d}</span>' if d else ""
            hv = f' data-hover="assets/img/{CARTE_IMG[n]}.webp"' if n in CARTE_IMG else ""
            lis += f'<li{hv}><span class="n">{n}</span><span class="p">{pr}</span>{dd}</li>'
        it = f"<p>{INTRO[k]}</p>" if intro else ""
        blocks.append((k, f'<div class="carte-cat" data-reveal><h3><span class="num">{ROMAN[i]}.</span>{title}</h3>{it}<ul>{lis}</ul></div>'))
    if len(blocks) == 1:  # single category: split its list over two columns
        return f'<div class="carte carte--one">{blocks[0][1]}</div>'
    left = "".join(b for k, b in blocks if k == "tresses")
    right = "".join(b for k, b in blocks if k != "tresses")
    if not left:
        half = (len(blocks) + 1) // 2
        left, right = "".join(b for _, b in blocks[:half]), "".join(b for _, b in blocks[half:])
    return f'<div class="carte"><div>{left}</div><div>{right}</div></div>'

def codes_block():
    items = "".join(f'<button class="code" type="button" data-code="{c}" data-price="{p}" aria-pressed="false"><span class="ph" style="display:block">{img(f"code-{c}", f"Modèle code {c}", "140px")}</span><b>Code {c}</b><strong>{p}<small>CHF</small></strong></button>' for c, p in CODES)
    return f'''<div class="codes">{items}</div>
<div class="code-cta"><p id="code-sel">Touchez un modèle pour le choisir.</p><div class="btns"><a class="btn" id="code-wa" href="{wa("Bonjour Mama Africa, je souhaite réserver un modèle de votre catalogue.")}" target="_blank" rel="noopener">{I["wa"]}Réserver ce code</a><button class="btn btn--line btn--sm" type="button" data-flyer="affiche-codes">Voir le catalogue</button></div></div>'''

def feature(o, i, rev=False):
    incl = "".join(f"<li>{x}</li>" for x in o["incl"])
    fl = f'<button class="fly" type="button" data-flyer="{o["flyer"]}">Voir l\'affiche</button>' if o.get("flyer") else ""
    return f'''<article class="feat{" rev" if rev else ""}" id="{o["id"]}">
  <div class="f-img">{veil(img(o["img"], o["title"], "(max-width: 960px) 100vw, 58vw"))}</div>
  <div class="f-txt" data-reveal><span class="num">{ROMAN[i - 1]}. {o["badge"]}</span><h3>{o["title"]}</h3><p class="lede" style="font-size:17px">{o["lead"]}</p>
    <div class="pr">{("<em>" + o["pre"] + "</em>") if o.get("pre") else ""}{o["price"]}<small>CHF</small></div><ul class="incl">{incl}</ul>
    <div class="btns" style="align-items:center;gap:22px"><a class="btn" href="{wa("Bonjour Mama Africa, je souhaite réserver : " + o["title"] + " (" + o["price"] + " CHF).")}" target="_blank" rel="noopener">{I["wa"]}Réserver</a>{fl}</div></div>
</article>'''

def reviews(head=True):
    real = lambda r: f'<article class="rv-card"><div class="rv-top"><span class="rv-av">{r["initial"]}</span><div><b>{esc(r["name"])}</b><small>{r["meta"]}</small></div>{I["g"]}</div>{STARS}<p>« {esc(r["text"])} »</p></article>'
    ph = lambda: f'<article class="rv-card is-ph" aria-hidden="true"><div class="rv-top"><span class="rv-av">G</span><div><b style="color:var(--muted)">Avis Google</b><small>Emplacement réservé</small></div>{I["g"]}</div>{STARS}<div class="sk"></div><div class="sk"></div><div class="sk"></div><em>Le prochain avis s\'affichera ici.</em></article>'
    cta = f'<article class="rv-card is-cta"><b>Vous êtes venue chez nous&nbsp;?</b><p>Votre avis aide d\'autres femmes à trouver une maison qui prend soin de leurs cheveux.</p><a class="btn btn--light btn--sm" href="{G_WRITE}" target="_blank" rel="noopener">Laisser un avis</a></article>'
    r1 = [real(r) for r in REVIEWS] + [ph(), ph(), cta, ph(), ph()]
    r2 = [ph(), cta, ph()] + [real(r) for r in REVIEWS] + [ph(), ph()]
    tr = lambda c: f'<div class="rv-track">{"".join(c)}<div style="display:contents" aria-hidden="true">{"".join(c)}</div></div>'
    h = f'''<div class="wrap"><div class="head"><div>{kicker("Avis Google")}<h2 class="d-l" data-reveal>Elles en parlent.</h2></div>
<a class="gscore" href="{G_REVIEWS}" target="_blank" rel="noopener" data-reveal>{I["g"]}<b>{G_RATING}</b><span>{STARS}<small>{G_COUNT} avis sur Google</small></span></a></div></div>''' if head else ""
    return f'{h}<div class="rv">{tr(r1)}</div><div class="rv rv--rev">{tr(r2)}</div>'

def booking():
    return f'''<section class="sec book"><div class="wrap book-grid">
  <div>{kicker("Rendez-vous")}<h2 class="d-l" data-reveal>Prendre rendez-vous.</h2><p class="lede" style="margin-top:24px;color:var(--on-dark-2)" data-reveal>En ligne, sur WhatsApp avec le code ou la photo de votre modèle, ou par téléphone.</p></div>
  <div data-reveal>{ways()}</div>
</div></section>'''

def visit():
    return f'''<section class="sec" id="visite"><div class="wrap visit">
  <div>{kicker("Nous trouver")}<h2 class="d-l" data-reveal>Rue de Lausanne 38B, Payerne.</h2>
    <p class="lede" style="margin:24px 0 28px">Le salon et la boutique sont réunis à la même adresse, au centre de Payerne.</p>
    <span class="open" id="open-now"><i></i><span>Horaires</span></span>{hours_list()}
    <div class="btns" style="margin-top:32px"><a class="btn" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Itinéraire</a><a class="btn btn--line" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div></div>
  <div class="map" data-reveal><iframe title="Carte : Mama Africa Beauty, {STREET}, Payerne" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={quote('Mama Africa beauty shopping, Rue de Lausanne 38, 1530 Payerne')}&z=16&output=embed"></iframe></div>
</div></section>'''

def faq(items=FAQ):
    return '<div class="faq">' + "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in items) + '</div>'

def collage():
    return f'''<div class="collage">
  <figure class="c1" data-reveal>{veil(img("reel-nattes", "Deux longues tresses collées, réalisées au salon", "(max-width: 960px) 100vw, 42vw") + '<span class="real">Fait au salon</span>')}<figcaption><span class="num">i.</span>Tresses collées longues, réalisées au salon</figcaption></figure>
  <figure class="c2" data-reveal><div class="ph">{video("salon-tresses", "Pose de tresses au salon")}</div><figcaption><span class="num">ii.</span>Une pose en cours</figcaption></figure>
  <figure class="c3" data-reveal>{veil(img("transplas-4", "Transplas réalisés au salon", "(max-width: 960px) 50vw, 25vw") + '<span class="real">Fait au salon</span>')}<figcaption><span class="num">iii.</span>Quatre transplas</figcaption></figure>
  <figure class="c4" data-reveal>{veil(img("boutique-cheveux", "Le comptoir des cheveux et mèches", "(max-width: 960px) 50vw, 25vw"))}<figcaption><span class="num">iv.</span>Le comptoir des mèches</figcaption></figure>
  <figure class="c5" data-reveal><div class="ph">{video("salon-visite", "La boutique")}</div><figcaption><span class="num">v.</span>La boutique</figcaption></figure>
</div>'''

def duo():
    h, e = OFFER["hommes"], OFFER["enfants"]
    card = lambda o, href, kick: f'''<a class="duo-card" href="{href}" data-reveal><div class="ph">{img(o["img"], o["title"], "(max-width: 960px) 100vw, 50vw")}</div>
  <div class="in"><p class="kicker">{kick}</p><h3>{o["title"]}</h3><span class="pr">{o["price"]}<small>CHF</small></span><p>{o["lead"]}</p></div></a>'''
    return f'<div class="duo">{card(h, "hommes-enfants#hommes", "Pour lui")}{card(e, "hommes-enfants#enfants", "Pour les petites")}</div>'

def shades():
    return '<div class="shades">' + "".join(f'<span style="--c:{c}"><i></i><span>{k}<small>{n}</small></span></span>' for k, c, n in SHADES) + '</div>'

# ================================================================ PAGES
def p_index():
    p = OFFER["perles"]
    body = f'''
<section class="hero" id="hero">
  <div class="hero-media">{video("hero-film", "Femme aux longues tresses", cls="v-d")}{video("hero-film-m", "", cls="v-m")}</div>
  <div class="wrap hero-in">
    <p class="kicker" data-in="1">Maison de tresses africaines · Payerne</p>
    <h1 class="d-xl" data-in="2">L'art de la tresse africaine.</h1>
    <div class="hero-foot">
      <div><p class="lede" data-in="3">Tresses, nattes, tissage, soins et perruques, réalisés avec patience Rue de Lausanne 38B. Sur nos offres, les mèches sont incluses.</p>
        <div class="btns" data-in="4"><button class="btn btn--light" type="button" data-book>Prendre rendez-vous</button><a class="btn btn--line-light" href="#signatures">Les offres</a></div></div>
      <a class="hero-offer" href="offres#perles" data-in="4"><img src="assets/img/{p["img"]}-m.webp" alt="" width="64" height="80"><span><small>Offre du moment</small><b>{p["title"]}, {p["price"]} CHF</b><span>Perles et un paquet de mèches offerts</span></span></a>
    </div>
  </div>
  <span class="scroll-line" aria-hidden="true"></span>
</section>

<section class="sec manifesto"><div class="wrap">
  {kicker("La maison", c=True)}
  <p class="statement" data-reveal>Une adresse pour vos tresses, vos soins et vos produits. Le geste juste, le temps qu'il faut, et des mèches offertes sur nos modèles signature.</p>
  <div class="facts" data-reveal>
    <div><b>{G_RATING} <span class="stars">★★★★★</span></b><span>Note Google</span></div>
    <div><b>Lun – Sam</b><span>9h00 – 18h30</span></div>
    <div><b>dès 70 CHF</b><span>Nattes, tresses, soins</span></div>
    <div><b>38B</b><span>Rue de Lausanne, Payerne</span></div>
  </div>
</div></section>

<section class="sec sec--paper" id="signatures" style="overflow:hidden">
  <div class="wrap"><div class="head"><div>{kicker("Les signatures")}<h2 class="d-l" data-reveal>Les offres de la maison.</h2></div>
  <p class="lede" data-reveal>Mèches offertes, cheveux inclus, prix ronds. Faites glisser pour parcourir.</p></div></div>
  {rail(OFFERS)}
</section>

<section class="sec" id="carte"><div class="wrap">
  <div class="head"><div>{kicker("La carte")}<h2 class="d-l" data-reveal>Prestations &amp; tarifs.</h2></div><a class="tlink" href="tarifs">Tous les tarifs {I["arr"]}</a></div>
  {carte(("tresses", "famille", "tissage", "soins"))}
</div></section>

<section class="sec sec--sand" id="codes"><div class="wrap">
  <div class="head"><div>{kicker("Le catalogue")}<h2 class="d-l" data-reveal>Choisissez votre code.</h2></div><p class="lede" data-reveal>Neuf modèles de nattes et de tresses. Choisissez, réservez en un message.</p></div>
  {codes_block()}
</div></section>

<section class="sec sec--dark"><div class="wrap">
  <div class="head"><div>{kicker("Hommes &amp; enfants")}<h2 class="d-l" data-reveal>Pour toute la famille.</h2></div><p class="lede" data-reveal>Cornrows pour hommes en six modèles, tresses à perles colorées pour les enfants.</p></div>
  {duo()}
</div></section>

<section class="sec"><div class="wrap">
  <div class="head"><div>{kicker("En vrai")}<h2 class="d-l" data-reveal>La maison, sans filtre.</h2></div><a class="tlink" href="galerie">La galerie {I["arr"]}</a></div>
  {collage()}
</div></section>

<section class="sec sec--paper" style="overflow:hidden">{reviews()}</section>

<section class="sec"><div class="wrap">
  <div class="head"><div>{kicker("La boutique")}<h2 class="d-l" data-reveal>Tout pour vos cheveux.</h2></div><p class="lede" data-reveal>Mèches, perruques, soins capillaires, cosmétiques et produits africains. Ouvert sans rendez-vous.</p></div>
  <div class="shop">{"".join(f'<div data-reveal>{img(f"produit-{i}", "Produit capillaire en boutique", "(max-width: 760px) 50vw, 20vw")}</div>' for i in (1, 4, 5, 9, 10))}</div>
  <div class="brands" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div>
  <div class="btns" style="justify-content:center;margin-top:44px"><a class="btn btn--line" href="boutique">Entrer dans la boutique</a></div>
</div></section>
{booking()}
{visit()}'''
    return page("index", "Mama Africa · Maison de tresses africaines à Payerne",
                "Tresses africaines, nattes, tissage, soins et perruques à Payerne. Mèches incluses sur nos offres. Réservation Salonkee, WhatsApp ou 078 259 77 38.", body)

def p_tresses():
    sel = [OFFER[k] for k in ("perles", "boheme", "tresses-africaines", "twist-curly", "rasta-elegance")]
    feats = "".join(feature(o, i, i % 2 == 0) for i, o in enumerate(sel, 1))
    body = phero("Tresses", "Tresses &amp; nattes", "Toutes les tresses, faites main.",
                 "Perles, bohème, box braids, twist &amp; curly, rasta, nattes, crochet et transplas. Choisissez un style ou un code.",
                 img("reel-nattes", "Tresses collées réalisées au salon", "100vw", eager=True), badge=("Mèches incluses dès", "130")) + f'''
<section class="sec"><div class="wrap">{feats}</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="head"><div>{kicker("La carte")}<h2 class="d-l" data-reveal>Tresses &amp; nattes.</h2></div><a class="tlink" href="tarifs">Tous les tarifs {I["arr"]}</a></div>{carte(("tresses",), intro=False)}</div></section>
<section class="sec sec--sand" id="codes"><div class="wrap"><div class="head"><div>{kicker("Le catalogue")}<h2 class="d-l" data-reveal>Choisissez votre code.</h2></div><p class="lede" data-reveal>Le modèle qui vous plaît, réservé en un message.</p></div>{codes_block()}</div></section>
<section class="sec"><div class="wrap split">
  <div>{kicker("Les couleurs")}<h2 class="d-l" data-reveal>Toutes les teintes, en boutique.</h2><p class="lede" style="margin-top:22px" data-reveal>Du noir naturel 1B au blond platine 613, en passant par le miel, le cuivré et le bordeaux : choisissez votre couleur au salon.</p>{shades()}</div>
  <div class="frame" style="aspect-ratio:4/5">{veil(img("tresses-miel", "Tresses couleur miel", "(max-width: 960px) 100vw, 45vw"), cls="ph")}</div>
</div></section>
{booking()}'''
    return page("tresses", "Tresses africaines à Payerne · Perles, bohème, box braids | Mama Africa",
                "Tresses avec perles 130 CHF (perles et mèches offertes), bohème et box braids 150 CHF mèches incluses, twist & curly, rasta, nattes, crochet à Payerne.", body, og="reel-nattes")

def p_famille():
    h, e = OFFER["hommes"], OFFER["enfants"]
    men = "".join(f"<li>{x}</li>" for x in MEN_STYLES)
    body = phero("Hommes &amp; enfants", "Pour toute la famille", "Hommes &amp; enfants.",
                 "Cornrows pour hommes en six modèles à 90 CHF. Tresses avec perles colorées pour les enfants à 100 CHF.",
                 img("homme-tresses-2", "Homme aux tresses", "100vw", eager=True)) + f'''
<section class="sec"><div class="wrap">
  <article class="feat" id="hommes"><div class="f-img">{veil(img(h["img"], h["title"], "(max-width: 960px) 100vw, 58vw"))}</div>
    <div class="f-txt" data-reveal><span class="num">I. Pour lui</span><h3>{h["title"]}</h3><p class="lede" style="font-size:17px">Une coupe nette et des finitions propres, avec des produits de qualité. Rapide et professionnel.</p>
    <div class="pr">{h["price"]}<small>CHF</small></div><ul class="incl">{men}</ul>
    <div class="btns" style="align-items:center;gap:22px"><a class="btn" href="{wa("Bonjour Mama Africa, je souhaite réserver des tresses homme (90 CHF).")}" target="_blank" rel="noopener">{I["wa"]}Réserver</a><button class="fly" type="button" data-flyer="{h["flyer"]}">Voir l'affiche</button></div></div></article>
  {feature(e, 2, True)}
</div></section>
<section class="sec sec--paper"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5">{veil(img("enfant-perles", "Fillette aux tresses et perles", "(max-width: 960px) 100vw, 45vw"), cls="ph")}</div>
  <div>{kicker("Les enfants")}<h2 class="d-l" data-reveal>Douceur et patience.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Des tresses légères et confortables, qui protègent les cheveux et durent.</p><p>Les petites choisissent la couleur de leurs perles. Nattes, transplas et tresses se font aussi pour les enfants : précisez simplement l'âge en réservant.</p></div></div>
</div></section>
{booking()}'''
    return page("hommes-enfants", "Tresses hommes et enfants à Payerne | Mama Africa",
                "Tresses hommes 90 CHF (cornrows, zigzag, couronne, motifs) et tresses enfants avec perles colorées 100 CHF à Payerne.", body, og="homme-tresses")

def p_tissage():
    sel = [OFFER["tissage"], OFFER["extensions-longues"]]
    body = phero("Tissage", "Tissage &amp; extensions", "De la longueur, en toute discrétion.",
                 "Tissage cousu sur nattes, extensions longues, lisses ou bouclées. Résultat naturel, coiffage compris.",
                 img("extensions-lisses", "Longs cheveux lisses", "100vw", eager=True), badge=("Dès", "135")) + f'''
<section class="sec"><div class="wrap">{"".join(feature(o, i, i % 2 == 0) for i, o in enumerate(sel, 1))}</div></section>
<section class="sec sec--paper"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5">{veil(img("boutique-cheveux", "Cheveux naturels au comptoir de la boutique", "(max-width: 960px) 100vw, 45vw") + '<span class="real">Au salon</span>', cls="ph")}</div>
  <div>{kicker("Les cheveux")}<h2 class="d-l" data-reveal>Choisis avec vous.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Cheveux naturels lisses, ondulés ou bouclés, au comptoir de la boutique.</p><p>Nous vous conseillons la longueur, la couleur et la quantité avant la pose. Extensions classiques : 135 CHF.</p></div></div>
</div></section>
{booking()}'''
    return page("tissage", "Tissage & extensions à Payerne | Mama Africa", "Tissage cousu dès 135 CHF, extensions 135 CHF, extensions longues 150 CHF, coiffage compris, à Payerne.", body, og="tissage-ondule")

def p_soins():
    body = phero("Soins &amp; perruques", "Soins, lissage &amp; perruques", "Des cheveux en bonne santé.",
                 "Défrisage, brushing, bio-plastie, soins Lowell, coupe et couleur. Et vos perruques retrouvent une seconde vie.",
                 img("afro-or", "Cheveux afro naturels", "100vw", eager=True), badge=("Rénovation de perruque", "110")) + f'''
<section class="sec"><div class="wrap">{feature(OFFER["renovation-perruque"], 1)}</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="head"><div>{kicker("La carte")}<h2 class="d-l" data-reveal>Soins &amp; lissage.</h2></div></div>{carte(("soins",), intro=False)}</div></section>
<section class="sec"><div class="wrap split">
  <div>{kicker("Notre approche")}<h2 class="d-l" data-reveal>Le soin avant tout.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Avant chaque soin, on observe la texture, la porosité et le cuir chevelu.</p><p>Puis on choisit le bon geste et le bon produit, souvent disponible en boutique pour prolonger le soin chez vous. La gamme Lowell est utilisée au salon et vendue sur place.</p></div></div>
  <div class="frame" style="aspect-ratio:4/5">{veil(img("hands-scalp", "Soin du cuir chevelu", "(max-width: 960px) 100vw, 45vw"), cls="ph")}</div>
</div></section>
{booking()}'''
    return page("soins", "Soins capillaires, défrisage & rénovation de perruque à Payerne | Mama Africa", "Défrisage 65 CHF, brushing 65 CHF, rénovation de perruque 110 CHF, bio-plastie, soins Lowell, coupe et teinture à Payerne.", body, og="perruque-glam")

def p_beaute():
    body = phero("Beauté", "Regard &amp; maquillage", "La beauté jusqu'au bout des cils.",
                 "Extensions de cils cil à cil et volume russe, sourcils et maquillage, par une spécialiste certifiée.",
                 video("beaute-maquillage", "Essai de rouges à lèvres")) + f'''
<section class="sec"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5">{veil(img("neneth-certificat", "Neneth et son certificat d'extension de cils", "(max-width: 960px) 100vw, 45vw"), cls="ph")}</div>
  <div>{kicker("Savoir-faire certifié")}<h2 class="d-l" data-reveal>Le regard, signé Neneth.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Avant Mama Africa, il y avait Neneth Beauty, spécialiste des extensions de cils.</p><p>Certifiée cil à cil et volume russe, Neneth apporte la même précision à chaque mise en beauté. Tarifs sur demande, selon la technique.</p></div>
  <div class="btns" style="margin-top:28px"><a class="btn" href="{wa("Bonjour Mama Africa, je souhaite un rendez-vous beauté (cils, sourcils ou maquillage).")}" target="_blank" rel="noopener">{I["wa"]}Demander un rendez-vous</a></div></div>
</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="head"><div>{kicker("La carte")}<h2 class="d-l" data-reveal>Beauté.</h2></div></div>{carte(("beaute",), intro=False)}</div></section>
{booking()}'''
    return page("beaute", "Extensions de cils, sourcils & maquillage à Payerne | Mama Africa", "Extensions de cils cil à cil et volume russe, sourcils et maquillage à Payerne.", body, og="makeup")

def p_offres():
    feats = "".join(feature(o, i, i % 2 == 0) for i, o in enumerate(OFFERS, 1))
    body = phero("Offres", "Offres du moment", "Les offres de la maison.",
                 "Mèches offertes, cheveux inclus, prix ronds. Chaque offre a son affiche originale, à consulter en un clic.",
                 img("boheme-2", "Tresses bohème", "100vw", eager=True), badge=("Perles et mèches offertes", "130")) + f'''
<section class="sec"><div class="wrap">{feats}</div></section>
{booking()}'''
    return page("offres", "Offres du moment · Mama Africa Payerne", "Tresses avec perles 130 CHF, bohème et tresses africaines 150 CHF mèches incluses, tresses hommes 90 CHF, enfants 100 CHF, rénovation de perruque 110 CHF.", body, og="boheme-1")

def p_tarifs():
    body = phero("Tarifs", "Tarifs 2026", "La carte.",
                 "Tous nos tarifs, selon la liste en vigueur au salon. Mèches offertes ou incluses lorsque c'est indiqué.",
                 img("edito-nuit", "Portrait, tresses", "100vw", eager=True)) + f'''
<section class="sec"><div class="wrap">{carte()}
<p class="hint" style="margin-top:20px">Prix en francs suisses. Sauf mention « offert » ou « inclus », les mèches s'achètent au salon. La bio-plastie se réserve par téléphone.</p>
<div class="btns" style="margin-top:34px"><a class="btn" href="{SALONKEE}" target="_blank" rel="noopener">{I["cal"]}Réserver sur Salonkee</a><button class="btn btn--line" type="button" data-flyer="affiche-tarifs">Voir l'affiche des tarifs</button></div></div></section>
<section class="sec sec--sand" id="codes"><div class="wrap"><div class="head"><div>{kicker("Le catalogue")}<h2 class="d-l" data-reveal>Tarifs par code.</h2></div></div>{codes_block()}</div></section>
{booking()}'''
    return page("tarifs", "Tarifs · Mama Africa Beauty Payerne", "Nattes 70 CHF, tresses hommes 90 CHF, enfants 100 CHF, rasta courtes 100 CHF, tresses avec ajout 110 CHF, perles 130 CHF, bohème 150 CHF, rasta longues 165 CHF.", body, og="edito-nuit")

def p_boutique():
    cats = "".join(f'<div data-reveal><span class="num">{ROMAN[i]}.</span><b>{t}</b><small>{d}</small></div>' for i, (t, d) in enumerate(BOUTIQUE_CATS))
    body = phero("Boutique", "La boutique", "Tout pour vos cheveux, sous un même toit.",
                 "Mèches, perruques, soins capillaires, cosmétiques, accessoires et produits africains. Du lundi au samedi, sans rendez-vous.",
                 video("salon-visite", "La boutique")) + f'''
<section class="sec"><div class="wrap"><div class="cats">{cats}</div></div></section>
<section class="sec sec--paper"><div class="wrap"><div class="head"><div>{kicker("En rayon")}<h2 class="d-l" data-reveal>Les soins que vos boucles réclament.</h2></div></div>
<div class="shop">{"".join(f'<div data-reveal>{img(f"produit-{i}", "Produit en vente à la boutique", "(max-width: 760px) 50vw, 20vw")}</div>' for i in range(1, 11))}</div>
<div class="brands" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div></div></section>
<section class="sec"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5">{veil(img("boutique-allee", "Les rayons de la boutique", "(max-width: 960px) 100vw, 45vw") + '<span class="real">La boutique</span>', cls="ph")}</div>
  <div>{kicker("Conseil")}<h2 class="d-l" data-reveal>On vous aide à choisir.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Quel masque pour des cheveux secs ? Combien de paquets pour des rastas longues ?</p><p>Passez nous voir ou écrivez-nous : nous vous répondons avec plaisir.</p></div>
  <div class="btns" style="margin-top:28px"><a class="btn" href="{wa("Bonjour Mama Africa, avez-vous ce produit en stock ?")}" target="_blank" rel="noopener">{I["wa"]}Demander un produit</a><button class="btn btn--line" type="button" data-flyer="affiche-boutique">L'affiche de la boutique</button></div></div>
</div></section>
{visit()}'''
    return page("boutique", "Boutique beauté afro à Payerne · Mèches, perruques, soins | Mama Africa", "Mèches, perruques, soins capillaires pour cheveux texturés, cosmétiques et produits africains à Payerne.", body, og="produit-10")

GALLERY = [
    ("reel-nattes", "Tresses collées longues", "tresses", True), ("box-braids-longues", "Box braids longues", "tresses", False),
    ("realisation-tresses", "Pose de tresses au salon", "tresses", True), ("perles-1", "Tresses avec perles", "tresses", False),
    ("transplas-4", "Transplas", "tresses", True), ("boheme-1", "Tresses bohème", "tresses", False),
    ("homme-tresses", "Tresses homme", "famille", False), ("enfant-perles-3", "Tresses enfant avec perles", "famille", False),
    ("boutique-cheveux", "Le comptoir des mèches", "salon", True), ("edito-nuit", "Tresses, portrait", "tresses", False),
    ("crochet-volume", "Crochet bouclé volume", "tresses", True), ("tissage-ondule", "Tissage ondulé", "tissage", False),
    ("salon-fauteuil", "Le coin shampoing", "salon", True), ("enfant-perles", "Perles colorées", "famille", False),
    ("realisation-tresses-2", "Tresses en cours", "tresses", True), ("extensions-lisses", "Extensions lisses", "tissage", False),
    ("boutique-allee", "Les rayons soins", "salon", True), ("nattes-motif", "Nattes à motif", "tresses", False),
    ("crochet-tendance", "Crochet bouclé tendance", "tresses", True), ("perruque-glam", "Perruque", "tissage", False),
    ("salon-rose", "Le coin beauté", "salon", True), ("garcon-tresses", "Nattes garçon", "famille", False),
    ("edito-profil", "Profil, tresses", "tresses", False), ("produit-10", "Gamme Mielle", "salon", True),
]
FLYERS = ["affiche-perles-130", "affiche-offre-coiffure", "affiche-hommes", "affiche-enfants", "affiche-twist-curly", "affiche-rasta-135",
          "affiche-tissage", "affiche-extensions", "affiche-renovation-perruque", "affiche-crochet", "affiche-transplas", "affiche-codes", "affiche-tarifs", "affiche-boutique"]

def p_galerie():
    figs = "".join(f'<figure data-cat="{c}" data-reveal>{img(n, cap, "(max-width: 760px) 100vw, 33vw")}<span class="src{" is-real" if real else ""}">{"Salon" if real else "Inspiration"}</span></figure>' for n, cap, c, real in GALLERY)
    figs += "".join(f'<figure data-cat="affiches" data-reveal>{img(f, "Affiche Mama Africa", "(max-width: 760px) 100vw, 33vw")}<span class="src is-real">Affiche</span></figure>' for f in FLYERS)
    filt = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in [("all", "Tout"), ("tresses", "Tresses"), ("famille", "Hommes & enfants"), ("tissage", "Tissage & perruques"), ("salon", "La maison"), ("affiches", "Affiches")])
    body = phero("Galerie", "Réalisations &amp; inspirations", "Regardez, choisissez.",
                 "Nos réalisations et les coulisses (« Salon »), des inspirations pour votre prochain style, et toutes nos affiches.",
                 img("edito-tresses-cuir", "Tresses, portrait", "100vw", eager=True)) + f'''
<section class="sec"><div class="wrap"><div class="filters" role="group" aria-label="Filtrer">{filt}</div><div class="masonry" id="masonry">{figs}</div></div></section>
{booking()}'''
    return page("galerie", "Galerie · Mama Africa Payerne", "Réalisations du salon Mama Africa à Payerne, inspirations et affiches : tresses, perles, bohème, hommes, enfants, tissage, perruques.", body, og="reel-nattes")

def p_salon():
    body = phero("La maison", "Notre histoire", "Mama Africa, la beauté africaine à Payerne.",
                 "Un salon de tresses africaines et une boutique de beauté, réunis Rue de Lausanne 38B.",
                 video("salon-tresses", "Pose de tresses au salon")) + f'''
<section class="sec manifesto"><div class="wrap">{kicker("Qui sommes-nous", c=True)}<p class="statement" data-reveal>Venez pour les produits, restez pour la coiffure, repartez avec le sourire et des cheveux sublimés.</p></div></section>
<section class="sec sec--paper"><div class="wrap split">
  <div class="prose" data-reveal><p class="big">Mama Africa est une boutique de cosmétiques et de soins capillaires tournée vers la beauté naturelle et l'identité africaine.</p><p>Des produits pour tous les types de cheveux, en particulier crépus, bouclés et en transition. Mais notre vrai cœur, c'est le salon : tresses, nattes, tissage, soins, coiffures africaines traditionnelles et modernes. Chaque rendez-vous est une expérience où beauté rime avec authenticité.</p></div>
  <div class="frame" style="aspect-ratio:4/5">{veil(img("salon-fauteuil", "Le salon Mama Africa", "(max-width: 960px) 100vw, 45vw") + '<span class="real">La maison</span>', cls="ph")}</div>
</div></section>
<section class="sec"><div class="wrap split">
  <div class="frame" style="aspect-ratio:4/5">{veil(img("neneth-certificat", "Neneth, fondatrice", "(max-width: 960px) 100vw, 45vw"), cls="ph")}</div>
  <div>{kicker("La fondatrice")}<h2 class="d-l" data-reveal>Neneth.</h2><div class="prose" style="margin-top:24px" data-reveal><p class="big">Avant Mama Africa, il y avait Neneth Beauty, spécialiste certifiée des extensions de cils.</p><p>Neneth a fait grandir son activité jusqu'à ouvrir une adresse qui réunit le geste et le produit. {SLOGAN}</p></div>
  <div class="btns" style="margin-top:28px"><a class="btn btn--line" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}Instagram</a></div></div>
</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="head"><div>{kicker("Le lieu")}<h2 class="d-l" data-reveal>La maison, sans filtre.</h2></div></div>{collage()}</div></section>
{booking()}'''
    return page("salon", "La maison · Notre histoire | Mama Africa Payerne", "Mama Africa, maison de tresses africaines et boutique beauté à Payerne, fondée par Neneth.", body, og="salon-fauteuil")

def p_avis():
    body = phero("Avis", "Avis Google", "Ce qu'elles disent de nous.",
                 "Merci à toutes celles et ceux qui partagent leur expérience. Votre avis aide d'autres femmes à nous trouver.",
                 img("edito-profil", "Portrait de profil", "100vw", eager=True)) + f'''
<section class="sec sec--paper" style="overflow:hidden">{reviews()}
<div class="wrap"><div class="btns" style="justify-content:center;margin-top:56px"><a class="btn" href="{G_WRITE}" target="_blank" rel="noopener">Laisser un avis Google</a><a class="btn btn--line" href="{G_REVIEWS}" target="_blank" rel="noopener">Voir sur Google</a></div></div></section>
{booking()}'''
    return page("avis", "Avis clients · Mama Africa Payerne", "Avis Google sur Mama Africa Beauty, maison de tresses africaines à Payerne.", body, og="edito-profil")

def p_reservation():
    def num(p):
        try: return int(str(p).split("/")[0].replace("dès", "").strip())
        except Exception: return 0
    def chip(n, p):
        lbl = (p + " CHF") if p else "sur demande"
        return f'<label><input type="checkbox" name="svc" value="{esc(n)}" data-price="{num(p)}"><span>{n}<em>{lbl}</em></span></label>'
    picks = "".join(f'<div class="field"><span class="lbl">{MENU[k][0]}</span><div class="pick">{"".join(chip(n, p) for n, p, d in MENU[k][1])}</div></div>' for k in ("tresses", "famille", "tissage", "soins", "beaute"))
    codes = "".join(f'<label><input type="radio" name="code" value="{c}"><span>Code {c}<em>{p} CHF</em></span></label>' for c, p in CODES)
    form = f'''<form class="form form-card" id="book-form" novalidate>
  {kicker("Demande de rendez-vous")}<p class="hint" style="margin-top:-12px">Votre demande s'ouvre dans WhatsApp, prête à envoyer. Nous confirmons par message.</p>
  {picks}<div class="field"><span class="lbl">Un modèle du catalogue ? (facultatif)</span><div class="pick">{codes}</div></div>
  <div class="total"><span>Estimation</span><b id="bf-total">0 CHF</b></div>
  <div class="two"><div class="field"><label for="bf-date">Date souhaitée</label><input id="bf-date" name="date" type="date"></div>
  <div class="field"><label for="bf-time">Moment</label><select id="bf-time" name="time"><option>Matin (9h – 12h)</option><option>Midi (12h – 14h)</option><option>Après-midi (14h – 18h30)</option><option>Peu importe</option></select></div></div>
  <div class="two"><div class="field"><label for="bf-name">Prénom et nom</label><input id="bf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="bf-tel">Téléphone</label><input id="bf-tel" name="tel" type="tel" autocomplete="tel"></div></div>
  <div class="field"><label for="bf-msg">Couleur, longueur, questions</label><textarea id="bf-msg" name="msg" placeholder="Ex. couleur 27, longueur bas du dos…"></textarea></div>
  <button class="btn" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button><p class="hint">Aucune donnée n'est enregistrée sur ce site.</p>
</form>'''
    body = phero("Réserver", "Rendez-vous", "Réservez votre moment.",
                 "En ligne sur Salonkee, sur WhatsApp ou par téléphone. Ou détaillez votre demande ci-dessous.",
                 img("salon-fauteuil", "Le salon", "100vw", eager=True)) + f'''
<section class="sec"><div class="wrap split" style="align-items:start">
  <div>{kicker("Trois façons de réserver")}{ways(light=True)}<div style="margin-top:56px">{kicker("Horaires")}{hours_list()}</div></div>
  {form}
</div></section>
<section class="sec sec--paper"><div class="wrap split" style="align-items:start"><div>{kicker("Questions fréquentes")}<h2 class="d-l" data-reveal>Bon à savoir.</h2></div>{faq()}</div></section>'''
    return page("reservation", "Réserver · Mama Africa Payerne", "Réservez vos tresses, tissage, soins ou beauté à Payerne : Salonkee, WhatsApp ou 078 259 77 38.", body, og="salon-fauteuil")

def p_contact():
    form = f'''<form class="form form-card" id="contact-form" novalidate>{kicker("Écrivez-nous")}
  <div class="two"><div class="field"><label for="cf-name">Prénom et nom</label><input id="cf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="cf-subj">Sujet</label><select id="cf-subj" name="subj"><option>Rendez-vous coiffure</option><option>Offre du moment</option><option>Produit de la boutique</option><option>Rénovation de perruque</option><option>Autre</option></select></div></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="msg" required></textarea></div>
  <button class="btn" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button><p class="hint">Aucune donnée n'est enregistrée sur ce site.</p></form>'''
    body = phero("Contact", "Contact", "Parlons de vos cheveux.",
                 "Une question sur un modèle, une offre, un produit ? Appelez, écrivez sur WhatsApp, ou passez nous voir.",
                 img("boutique-allee", "La boutique", "100vw", eager=True)) + f'''
<section class="sec"><div class="wrap split" style="align-items:start"><div>{kicker("Joindre la maison")}{ways(light=True)}<div style="margin-top:56px">{kicker("Questions fréquentes")}{faq(FAQ[:4])}</div></div>{form}</div></section>
{visit()}'''
    return page("contact", "Contact · Mama Africa, Rue de Lausanne 38B, Payerne", "Mama Africa Beauty, Rue de Lausanne 38B, 1530 Payerne. 078 259 77 38, WhatsApp, Instagram. Lundi – samedi 9h00 – 18h30.", body, og="boutique-allee")

def p_conf():
    body = f'''<section class="sec" style="padding-top:calc(var(--hdr) + 80px)"><div class="wrap wrap--narrow">{kicker("Informations légales")}<h1 class="d-l">Confidentialité.</h1>
<div class="prose" style="margin-top:36px"><p><b>Éditeur.</b> {NAME}, {STREET}, {CITY}, Suisse. {PHONE}.</p>
<p><b>Données.</b> Ce site n'enregistre aucune donnée. Les formulaires préparent un message WhatsApp que vous envoyez vous-même. Les réservations en ligne passent par Salonkee.</p>
<p><b>Services tiers.</b> La carte est fournie par Google Maps, qui peut déposer des cookies. Les liens Instagram, WhatsApp, Salonkee et Google ouvrent ces services, soumis à leurs propres règles.</p>
<p><b>Crédits.</b> Photos du salon, de la boutique et affiches : {NAME}. Photos et vidéos d'inspiration : Unsplash et Pexels.</p></div></div></section>'''
    return page("confidentialite", "Confidentialité · Mama Africa", "Informations légales et confidentialité.", body, on_hero=False)

def p_404():
    body = f'<section class="nf"><div>{kicker("Erreur 404", c=True)}<h1 class="d-xl">Page introuvable.</h1><p class="lede" style="margin:24px auto 34px">La page demandée n\'existe pas ou a été déplacée.</p><div class="btns" style="justify-content:center"><a class="btn" href="./">Accueil</a><button class="btn btn--line" type="button" data-book>Réserver</button></div></div></section>'
    return page("404", "Page introuvable · Mama Africa", "Page introuvable.", body, on_hero=False)

PAGES = {"index": p_index, "tresses": p_tresses, "hommes-enfants": p_famille, "tissage": p_tissage, "soins": p_soins, "beaute": p_beaute,
         "offres": p_offres, "tarifs": p_tarifs, "boutique": p_boutique, "galerie": p_galerie, "salon": p_salon, "avis": p_avis,
         "reservation": p_reservation, "contact": p_contact, "confidentialite": p_conf, "404": p_404}

if __name__ == "__main__":
    for f in os.listdir(ROOT):
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
