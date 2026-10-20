# -*- coding: utf-8 -*-
"""Static generator for the Mama Africa site (v4, warm African luxury). Run: python3 _build/build.py"""
import os, json, html, sys
from urllib.parse import quote
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from data import *  # noqa
import seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
esc = html.escape

I = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-.99.24-3.33-.69-2.81-1.11-4.6-3.98-4.74-4.17-.14-.18-1.13-1.5-1.13-2.87s.72-2.03.97-2.31c.26-.28.56-.35.74-.35l.54.01c.17 0 .41-.07.64.49.25.58.83 2.01.9 2.15.08.14.12.3.03.49-.1.19-.14.3-.28.47-.14.16-.3.37-.42.49-.14.14-.29.29-.12.57.16.28.73 1.2 1.56 1.94 1.07.95 1.98 1.25 2.26 1.39.28.14.44.12.61-.07.16-.19.71-.83.9-1.11.19-.28.37-.23.63-.14.26.09 1.65.78 1.93.92.28.14.47.21.54.33.07.11.07.66-.18 1.35Z"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="2.5"/><path d="M8 2.5v4M16 2.5v4M3 10h18"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.3 7-12a7 7 0 1 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "arr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 "g": '<svg class="g-logo" viewBox="0 0 48 48" aria-label="Google"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>',
}
ARR_W = I["arr"].replace('<svg', '<svg class="arr"')
STARS = '<span class="stars" aria-label="5 étoiles sur 5">★★★★★</span>'

def wa(msg="Bonjour Mama Africa, j'aimerais prendre rendez-vous."):
    return f"https://wa.me/{WA}?text={quote(msg)}"

_d = {}
def dims(n):
    if n not in _d:
        try:
            with Image.open(os.path.join(IMG, n + ".webp")) as im: _d[n] = im.size
        except FileNotFoundError: _d[n] = (1200, 1500)
    return _d[n]

def img(n, alt, sizes="(max-width: 760px) 100vw, 50vw", eager=False, cls=""):
    w, h = dims(n)
    srcset = ""
    if os.path.exists(os.path.join(IMG, n + "-m.webp")):
        srcset = f' srcset="assets/img/{n}-m.webp {dims(n + "-m")[0]}w, assets/img/{n}.webp {w}w" sizes="{sizes}"'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="assets/img/{n}.webp"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async"{c}>'

def video(n, label=""):
    aria = f' aria-label="{esc(label)}"' if label else ' aria-hidden="true"'
    return f'<video src="assets/video/{n}.mp4" poster="assets/video/{n}.webp" muted loop playsinline autoplay preload="metadata"{aria}></video>'

def tag(t):
    return f'<p class="tag">{t}</p>'

def medal(p, pre=None):
    if not p: return ""
    e = f"<em>{pre}</em>" if pre else ""
    return f'<span class="medal" aria-label="{(pre + " ") if pre else ""}{p} francs"><span>{e}<b>{p}</b><small>CHF</small></span></span>'

# ---------------------------------------------------------------- shell
NAV = [("index", "Accueil", "./"), ("tresses", "Tresses", "tresses"), ("hommes-enfants", "Hommes & enfants", "hommes-enfants"),
       ("tissage", "Tissage", "tissage"), ("soins", "Soins & perruques", "soins"), ("beaute", "Beauté", "beaute"),
       ("offres", "Offres", "offres"), ("tarifs", "Tarifs", "tarifs"), ("boutique", "Boutique", "boutique"),
       ("galerie", "Galerie", "galerie"), ("salon", "Le salon", "salon"), ("avis", "Avis", "avis"), ("conseils", "Conseils", "conseils"), ("contact", "Contact", "contact")]
DESK = ["tresses", "hommes-enfants", "tissage", "soins", "offres", "tarifs", "boutique", "contact"]

def header(cur):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if s == cur else ""}>{l}</a>' for s, l, h in NAV if s in DESK)
    mnav = "".join(f'<a class="big" href="{h}">{l}{"<small>Ici</small>" if s == cur else ""}</a>' for s, l, h in NAV)
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="hdr" id="hdr"><div class="wrap">
  <a class="logo" href="./" aria-label="Mama Africa Beauty Shop, accueil"><img src="assets/img/logo.webp" width="731" height="377" alt="Mama Africa Beauty Shop"></a>
  <nav class="nav" aria-label="Navigation">{nav}</nav>
  <div class="hdr-r"><a class="hdr-tel" href="tel:{TEL}">{I["tel"]}<span>{PHONE}</span></a><button class="btn btn--gold btn--sm" type="button" data-book>Prendre rendez-vous</button>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button></div>
</div><div class="ribbon" style="height:7px;background-size:auto 7px"></div></header>
<nav class="mnav" id="mnav" aria-label="Menu">{mnav}
  <div class="mnav-foot"><button class="btn btn--gold" type="button" data-book>{I["cal"]}Prendre rendez-vous</button><a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a><a class="btn" style="box-shadow:inset 0 0 0 1.5px var(--line-d)" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div>
</nav>'''

def ways(light=False):
    c = " ways--light" if light else ""
    return f'''<div class="ways{c}">
  <a class="way" href="{SALONKEE}" target="_blank" rel="noopener"><span class="ic">{I["cal"]}</span><span><b>En ligne sur Salonkee</b><small>Choisissez votre créneau, 24h/24</small></span>{ARR_W}</a>
  <a class="way wa" href="{wa()}" target="_blank" rel="noopener"><span class="ic">{I["wa"]}</span><span><b>Sur WhatsApp</b><small>Envoyez le code ou une photo du modèle</small></span>{ARR_W}</a>
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
    return f'''<footer class="ftr"><div class="ribbon"></div><div class="wrap">
  <div class="ftr-top">
    <div><a class="emb" href="./"><img src="assets/img/logo-embleme.webp" width="582" height="582" alt="" loading="lazy"><span><b>Mama Africa</b><small>Beauty Shop · Payerne</small></span></a>
      <p>Coiffeuse afro et boutique de produits pour cheveux afro à Payerne, Rue de Lausanne 38B, à 3 minutes de la gare. {SLOGAN}</p>
      <div class="socials"><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a><a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["wa"]}</a><a href="{GMAPS}" target="_blank" rel="noopener" aria-label="Google Maps">{I["pin"]}</a><a href="{SALONKEE}" target="_blank" rel="noopener" aria-label="Salonkee">{I["cal"]}</a></div></div>
    <div><h4>Coiffure</h4><ul>{col(["tresses", "hommes-enfants", "tissage", "soins", "beaute"])}</ul></div>
    <div><h4>Mama Africa</h4><ul>{col(["offres", "tarifs", "boutique", "galerie", "salon", "avis", "conseils"])}<li><a href="coiffure-afro-broye">Broye, Fribourg et environs</a></li></ul></div>
    <div><h4>Nous trouver</h4><ul><li><a href="{GMAPS}" target="_blank" rel="noopener">{STREET}<br>{CITY}</a></li><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></li><li style="color:var(--on-2)">Lundi au samedi, 9h00 – 18h30</li></ul></div>
  </div>
  <div class="ftr-bot"><span>© 2026 {NAME}</span><span><a href="reservation">Réserver</a> · <a href="confidentialite">Confidentialité</a></span></div>
</div></footer>'''

def overlays():
    return f'''<div class="abar is-away" id="abar">
  <a class="a-tel" href="tel:{TEL}" aria-label="Appeler le {PHONE}">{I["tel"]}Appeler</a>
  <a class="a-wa" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a>
  <button class="a-book" type="button" data-book>{I["cal"]}Réserver</button>
</div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-t" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-panel"><div class="ribbon"></div><button class="x" type="button" data-close aria-label="Fermer">{I["x"]}</button>
    <div class="sheet-in"><h2 class="h3" id="sheet-t" style="font-size:30px;margin:0 50px 6px 0">Prendre rendez-vous</h2><p class="muted" style="margin:0 0 20px">Choisissez ce qui vous arrange.</p>
    {ways(light=True)}
    <p class="hint" style="margin-top:18px">Vous avez repéré un modèle&nbsp;? <a href="tresses#codes" style="text-decoration:underline">Réservez-le par son code</a>.</p></div>
  </div>
</div>
<div class="lb" id="lb" aria-hidden="true"><button class="x" type="button" aria-label="Fermer">{I["x"]}</button><button class="pv" type="button" aria-label="Précédente">{I["prev"]}</button><img alt=""><button class="nx" type="button" aria-label="Suivante">{I["arr"]}</button><p></p></div>'''

def schema():
    d = {"@context": "https://schema.org", "@type": "HairSalon", "name": NAME, "slogan": SLOGAN,
         "image": BASE + "assets/img/logo.png", "url": BASE, "telephone": TEL, "priceRange": "CHF 45 – 165",
         "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressRegion": "VD", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:30"}],
         "sameAs": [INSTAGRAM, SALONKEE, GMAPS]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def page(slug, title, desc, body, og="perles-1", ld=None):
    if slug in seo.META: title, desc = seo.META[slug]
    if ld is None:
        ld = seo.jsonld(slug, crumbs=[(seo.CRUMB[slug], slug)] if slug in seo.CRUMB else None)
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
<meta name="theme-color" content="#f6ecdd">
<meta property="og:type" content="{"article" if slug in seo.ARTICLES else "website"}"><meta property="og:site_name" content="Mama Africa Beauty"><meta property="og:locale" content="fr_CH"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/{og}.webp">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/gambetta-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/author-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={V}">
<script>(function(p){{if(p.slice(-5)===".html"){{history.replaceState(null,"",p.slice(-11)==="/index.html"?p.slice(0,-10):p.slice(0,-5)+location.search+location.hash)}}}})(location.pathname);document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__ma)document.documentElement.classList.remove('js')}},3500)</script>
{ld if slug != "404" else ""}
</head>
<body data-page="{slug}">
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
{overlays()}
<script>window.MA_WA="{WA}";</script>
<script src="assets/js/vendor/lenis.min.js"></script>
<script src="assets/js/vendor/gsap.min.js"></script>
<script src="assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="assets/js/site.js?v={V}"></script>
</body>
</html>'''

# ---------------------------------------------------------------- blocks
def pintro(crumb, h1, intro, pic, price=None, pre=None, btns=True, extra=""):
    b = f'<div class="btns"><button class="btn btn--gold" type="button" data-book>{I["cal"]}Prendre rendez-vous</button><a class="btn btn--line" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a></div>' if btns else ""
    return f'''<section class="pintro"><div class="wrap pintro-grid">
  <div><nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>›</span><span>{crumb}</span></nav>
    <h1 class="h1">{h1}</h1><p class="intro">{intro}</p>{b}{extra}</div>
  <div class="pintro-pic"><div class="ph">{pic}</div>{medal(price, pre)}</div>
</div></section>'''

def book_msg(o):
    return wa("Bonjour Mama Africa, je souhaite réserver : " + o["title"] + " (" + o["price"] + " CHF).")

def poster(o):
    fl = f'<button class="fly" type="button" data-flyer="{o["flyer"]}">Voir l\'affiche</button>' if o.get("flyer") else ""
    return f'''<article class="poster" data-reveal>
  <a class="ph" href="offres#{o["id"]}">{img(o["img"], o["title"], "(max-width: 760px) 76vw, 25vw")}<span class="gift">{o["badge"]}</span>{medal(o["price"], o.get("pre"))}</a>
  <h3>{o["title"]}</h3><p>{o["incl"][0]}</p>
  <div class="acts"><a class="btn btn--sm" href="{book_msg(o)}" target="_blank" rel="noopener">Réserver</a>{fl}</div>
</article>'''

def detail(o, rev=False):
    incl = "".join(f"<li>{x}</li>" for x in o["incl"])
    fl = f'<button class="fly" type="button" data-flyer="{o["flyer"]}">Voir l\'affiche</button>' if o.get("flyer") else ""
    return f'''<article class="detail{" rev" if rev else ""}" id="{o["id"]}">
  <div class="d-pic" data-reveal>{img(o["img"], o["title"], "(max-width: 960px) 100vw, 46vw")}<span class="gift">{o["badge"]}</span>{medal(o["price"], o.get("pre"))}</div>
  <div class="d-txt" data-reveal><h2>{o["title"]}</h2><p class="intro">{o["lead"]}</p><ul class="checks">{incl}</ul>
    <div class="d-acts"><a class="btn btn--gold" href="{book_msg(o)}" target="_blank" rel="noopener">{I["wa"]}Réserver ce modèle</a>{fl}</div></div>
</article>'''

INTROS = {"tresses": "Mèches offertes ou incluses sur nos offres.", "famille": "Pour lui et pour les petites.",
          "tissage": "Coiffage compris.", "soins": "Pour cheveux crépus, bouclés, lisses ou en transition.", "beaute": "Par une spécialiste certifiée."}

def ptable(k):
    title, items = MENU[k]
    lis = ""
    for n, p, d in items:
        pr = f'{p}<small>CHF</small>' if p else '<small style="font-size:14px;color:inherit">Sur demande</small>'
        gift = " gift" if d and ("offert" in d or "inclus" in d.lower()) else ""
        dd = f'<span class="d{gift}">{d}</span>' if d else ""
        lis += f'<li><span class="n">{n}</span><span class="p">{pr}</span>{dd}</li>'
    return f'<div class="ptable" data-reveal><div class="ribbon"></div><div class="ptable-in"><h3>{title}</h3><p>{INTROS.get(k, "")}</p><ul>{lis}</ul></div></div>'

def ptables(keys):
    if len(keys) == 1:
        return f'<div style="max-width:760px">{ptable(keys[0])}</div>'
    left = [k for k in keys if k == "tresses"] or list(keys[: (len(keys) + 1) // 2])
    right = [k for k in keys if k not in left]
    return f'<div class="ptables"><div style="display:grid;gap:20px">{"".join(ptable(k) for k in left)}</div><div style="display:grid;gap:20px">{"".join(ptable(k) for k in right)}</div></div>'

def codes_block():
    items = "".join(f'<button class="code" type="button" data-code="{c}" data-price="{p}" aria-pressed="false"><span class="ph">{img(f"code-{c}", f"Modèle code {c}", "140px")}</span><b>Code {c}</b><strong>{p} CHF</strong></button>' for c, p in CODES)
    return f'''<div class="codes">{items}</div>
<div class="code-cta"><p id="code-sel">Touchez un modèle pour le choisir.</p><div class="btns"><a class="btn btn--wa" id="code-wa" href="{wa("Bonjour Mama Africa, je souhaite réserver un modèle de votre catalogue.")}" target="_blank" rel="noopener">{I["wa"]}Réserver ce code</a><button class="btn btn--line btn--sm" type="button" data-flyer="affiche-codes">Voir le catalogue</button></div></div>'''

SERVICES = [
    ("tresses", "Tresses & nattes", "Perles, bohème, box braids, twist, rasta, crochet", "70", "perles-a"),
    ("hommes-enfants", "Hommes & enfants", "Cornrows en 6 modèles, tresses à perles colorées", "90", "enfants-a"),
    ("tissage", "Tissage & extensions", "Tissage cousu, extensions longues, coiffage inclus", "135", "tissage-ondule"),
    ("soins", "Soins & perruques", "Défrisage, brushing, bio-plastie, rénovation de perruque", "45", "perruque-b"),
    ("beaute", "Beauté du regard", "Extensions de cils, sourcils, maquillage", None, "makeup"),
]

def services():
    rows = "".join(f'''<a class="svc-row{" is-on" if i == 0 else ""}" href="{s}" data-pic="{i}"><span class="th">{img(pic, "", "64px")}</span><span><b>{t}</b><span class="d">{d}</span></span><span class="from">{("<small>dès</small>" + p + " CHF") if p else "<small>tarif</small>sur demande"}</span></a>''' for i, (s, t, d, p, pic) in enumerate(SERVICES))
    pics = "".join(img(pic, t, "40vw", cls="is-on" if i == 0 else "") for i, (s, t, d, p, pic) in enumerate(SERVICES))
    return f'<div class="svc"><div class="svc-list">{rows}</div><div class="svc-pic" aria-hidden="true">{pics}</div></div>'

def strip():
    items = [
        (img("reel-nattes", "Tresses collées longues, réalisées au salon", "300px"), "Tresses collées longues", True),
        (video("salon-tresses", "Pose de tresses au salon"), "Une pose en cours", True),
        (img("transplas-4", "Quatre transplas", "300px"), "Quatre transplas", True),
        (img("crochet-volume", "Crochet bouclé volume", "300px"), "Crochet bouclé volume", True),
        (img("boutique-meches", "Le mur des mèches à tresser", "300px"), "Le mur des mèches", False),
        (img("boutique-cheveux-2", "Cheveux naturels et tissages", "300px"), "Cheveux naturels et tissages", False),
        (video("salon-visite", "La boutique"), "La boutique", False),
        (img("realisation-tresses-2", "Tresses en cours", "300px"), "Tresses avec ajout", True),
        (img("boutique-rayons-2", "Les rayons de soins", "300px"), "Les rayons de soins", False),
    ]
    figs = "".join(f'<figure data-reveal><div class="ph">{m}{"<span class=real>Fait au salon</span>" if r else ""}</div><figcaption>{c}</figcaption></figure>' for m, c, r in items)
    return f'<div class="strip">{figs}</div>'

def soin_videos(head=True):
    vids = [("soin-lissage", "Lissage et soin protecteur", "Du cheveu crépu au lisse brillant, étape par étape."),
            ("soin-masque", "Masque au collagène et beurre de karité", "Le soin nourrissant qui répare et fait briller.")]
    cards = "".join(f'''<figure class="vcard" data-reveal><div class="ph">{video(v, t)}<button class="snd" type="button" aria-label="Activer le son" aria-pressed="false"><span class="on">Son activé</span><span class="off">Activer le son</span></button></div><figcaption><b>{t}</b><span>{d}</span></figcaption></figure>''' for v, t, d in vids)
    return f'''<div class="vsplit"><div>{tag("Les soins en vidéo")}<h2 class="h2">Voyez le résultat</h2>
  <p class="intro" style="margin:18px 0 26px">Lissage, défrisage et masques nourrissants : des soins qui transforment le cheveu, du crépu au lisse brillant. Les produits sont en vente à la boutique.</p>
  <div class="btns"><a class="btn btn--gold" href="{wa("Bonjour Mama Africa, je souhaite un rendez-vous pour un soin (lissage, défrisage ou masque).")}" target="_blank" rel="noopener">{I["wa"]}Réserver un soin</a><a class="btn btn--line" href="soins">Tous les soins</a></div></div>
  <div class="vcards">{cards}</div></div>'''

def reviews():
    real = lambda r: f'<article class="rv-card"><div class="rv-top"><span class="rv-av">{r["initial"]}</span><div><b>{esc(r["name"])}</b><small>{r["meta"]}</small></div>{I["g"]}</div>{STARS}<p>« {esc(r["text"])} »</p></article>'
    ph = lambda: f'<article class="rv-card is-ph" aria-hidden="true"><div class="rv-top"><span class="rv-av">G</span><div><b style="color:var(--muted)">Avis Google</b><small>Emplacement réservé</small></div>{I["g"]}</div>{STARS}<div class="sk"></div><div class="sk"></div><div class="sk"></div><em>Le prochain avis s\'affichera ici.</em></article>'
    cta = f'<article class="rv-card is-cta"><b>Vous êtes venue chez nous&nbsp;?</b><p>Votre avis aide d\'autres femmes à nous trouver.</p><a class="btn btn--gold btn--sm" href="{G_WRITE}" target="_blank" rel="noopener">Laisser un avis</a></article>'
    r1 = [real(r) for r in REVIEWS] + [ph(), ph(), cta, ph(), ph()]
    r2 = [ph(), cta, ph()] + [real(r) for r in REVIEWS] + [ph(), ph()]
    tr = lambda c: f'<div class="rv-track">{"".join(c)}<div style="display:contents" aria-hidden="true">{"".join(c)}</div></div>'
    return f'''<div class="wrap"><div class="shead"><div>{tag("Avis Google")}<h2 class="h2">Ce que nos clientes en disent</h2></div>
<a class="gscore" href="{G_REVIEWS}" target="_blank" rel="noopener">{I["g"]}<b>{G_RATING}</b><span>{STARS}<small>{G_COUNT} avis sur Google</small></span></a></div></div>
<div class="rv">{tr(r1)}</div><div class="rv rv--rev">{tr(r2)}</div>'''

def booking():
    return f'''<section class="sec sec--dark"><div class="wrap book">
  <div>{tag("Rendez-vous")}<h2 class="h2">Réservez votre prochaine coiffure</h2><p class="intro" style="margin-top:18px">En ligne, sur WhatsApp avec le code ou une photo de votre modèle, ou par téléphone. Nous vous répondons rapidement.</p></div>
  {ways()}
</div></section>'''

def visit(top=False):
    st = '' if top else ' style="padding-top:0"'
    return f'''<section class="sec sec--dark" id="visite"{st}><div class="wrap visit">
  <div>{tag("Nous trouver")}<h2 class="h2">Rue de Lausanne 38B, Payerne</h2>
    <p class="intro" style="margin:16px 0 20px">Le salon et la boutique sont à la même adresse, au centre de Payerne.</p>
    <span class="open" id="open-now"><i></i><span>Horaires</span></span>{hours_list()}
    <div class="btns" style="margin-top:26px"><a class="btn btn--gold" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Itinéraire</a><a class="btn btn--line" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div></div>
  <div class="map"><iframe title="Carte : Mama Africa Beauty, {STREET}, Payerne" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={quote('Mama Africa beauty shopping, Rue de Lausanne 38, 1530 Payerne')}&z=16&output=embed"></iframe></div>
</div></section>'''

def why_us():
    brands = "".join(f"<li>{b}</li>" for b in ["Mielle", "Lola Cosmetics", "Salon Line", "Novex", "O Boticário", "Lowell", "X-pression"])
    return f'''<section class="sec"><div class="wrap why">
  <div class="prose" data-reveal>{tag("Coiffeuse afro à Payerne")}<h2 class="h2" style="margin-bottom:22px">Une adresse afro rare dans la Broye</h2>
    <p class="lead">Trouver une coiffeuse qui sait travailler les cheveux crépus et bouclés, sans faire une heure de route : c'est pour ça que Mama Africa existe.</p>
    <p>Au salon de la Rue de Lausanne 38B, à 3 minutes à pied de la gare de Payerne, nous réalisons <a href="tresses">tresses africaines</a>, box braids, knotless, nattes collées, <a href="tissage">tissages</a>, <a href="soins">défrisages et soins</a>, pour les femmes, les <a href="hommes-enfants">hommes et les enfants</a>.</p>
    <p>Nos clientes viennent de Payerne, mais aussi d'Estavayer-le-Lac, d'Avenches, de Moudon, de Fribourg ou d'Yverdon-les-Bains. <a href="coiffure-afro-broye">Venir depuis la région</a>.</p></div>
  <aside class="rare" data-reveal><div class="ribbon"></div><div class="rare-in">{tag("La boutique")}<h3 class="h3">Des produits qu'on ne trouve presque nulle part ailleurs dans la région</h3>
    <p>Les grandes surfaces suisses proposent très peu de soins pour cheveux afro. À la boutique, ces marques sont en rayon :</p><ul class="rare-list">{brands}</ul>
    <p>Mèches pour tresses, cheveux naturels, perruques, cosmétiques et produits africains complètent la sélection.</p>
    <a class="btn btn--gold" href="boutique">Découvrir la boutique {I["arr"]}</a></div></aside>
</div></section>'''

def brand_notes():
    cards = "".join(f'<div class="bnote" data-reveal><b>{n}</b><p>{d}</p></div>' for n, d in seo.BRAND_NOTES)
    return f'''<div class="shead"><div>{tag("Nos marques")}<h2 class="h2">Des marques rares en Suisse romande, en rayon à Payerne</h2></div><p class="intro">Inutile de commander à l'étranger et d'attendre la livraison : venez voir les produits, demandez conseil, repartez avec.</p></div>
<div class="bnotes">{cards}</div>'''

def faq(items=FAQ):
    return '<div class="faq">' + "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in items) + '</div>'

def shop():
    cats = "".join(f'<li><span><b>{t}</b><span>{d}</span></span></li>' for t, d in BOUTIQUE_CATS)
    return f'''<div class="shop">
  <div class="shop-pic" data-reveal>{img("boutique-rayons-1", "Les rayons de soins de la boutique Mama Africa", "(max-width: 960px) 100vw, 42vw")}<span class="real">La boutique</span></div>
  <div data-reveal>{tag("La boutique")}<h2 class="h2">Tout pour vos cheveux, sous le même toit</h2>
    <p class="intro" style="margin-top:16px">Mielle, Lola Cosmetics, Salon Line, Novex, Lowell : des marques pour cheveux crépus, bouclés et en transition qu'on trouve très peu ailleurs dans la région. Chez nous, elles sont en rayon, avec les conseils en plus. Ouvert du lundi au samedi, sans rendez-vous.</p>
    <ul class="cats">{cats}</ul>
    <div class="prods">{"".join(f'<div>{img(f"produit-{i}", "Produit en vente à la boutique", "160px")}</div>' for i in (1, 4, 9, 10))}</div>
    <div class="brands">{"".join(f"<span>{b}</span>" for b in BRANDS)}</div></div>
</div>'''

# ================================================================ PAGES
def p_index():
    p = OFFER["perles"]
    body = f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    {tag("Salon de tresses africaines à Payerne")}
    <h1 class="h1">Coiffeuse afro à Payerne : tresses, tissage et soins</h1>
    <p class="intro">Tresses, nattes, tissage, soins et perruques, réalisés à la main Rue de Lausanne 38B. Sur nos offres, les mèches sont incluses.</p>
    <a class="offer-tag" href="offres#perles">{medal(p["price"])}<span class="ot"><small>En ce moment</small><b>{p["title"]}</b><span>Perles et un paquet de mèches offerts, coiffure comprise</span></span></a>
    <div class="btns"><button class="btn btn--gold" type="button" data-book>{I["cal"]}Prendre rendez-vous</button><a class="btn btn--line" href="{wa()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a></div>
    <div class="hero-trust"><span>{STARS} {G_RATING} sur Google</span><span>{I["clock"]}Lun – sam, 9h – 18h30</span><span>{I["pin"]}Rue de Lausanne 38B</span></div>
  </div>
  <div class="hero-pic">
    <div class="hero-main">{video("tresses-portrait", "Femme aux longues tresses")}</div>
    <div class="hero-inset">{img("reel-nattes", "Tresses collées réalisées au salon", "220px", eager=True)}<p>Réalisé au salon</p></div>
  </div>
</div></section>

<section class="sec sec--paper" id="offres"><div class="wrap">
  <div class="shead"><div>{tag("Les offres du moment")}<h2 class="h2">Les mèches sont pour nous</h2></div><a class="more" href="offres">Toutes les offres {I["arr"]}</a></div>
  <div class="posters">{"".join(poster(OFFER[k]) for k in ("perles", "boheme", "hommes", "enfants"))}</div>
</div></section>

<div class="ribbon"></div>
<section class="sec sec--dark"><div class="wrap">
  <div class="shead"><div>{tag("Nos prestations")}<h2 class="h2">Ce que nous faisons</h2></div><a class="more" href="tarifs">Tous les tarifs {I["arr"]}</a></div>
  {services()}
</div></section>
<div class="ribbon"></div>

<section class="sec sec--paper"><div class="wrap">{soin_videos()}</div></section>

<section class="sec" id="codes"><div class="wrap">
  <div class="shead"><div>{tag("Le catalogue")}<h2 class="h2">Choisissez votre modèle par son code</h2></div><p class="intro">Neuf modèles de nattes et de tresses, de 100 à 135 CHF. Indiquez simplement le code en réservant.</p></div>
  {codes_block()}
</div></section>

<section class="sec sec--sand"><div class="wrap">
  <div class="shead"><div>{tag("Au salon")}<h2 class="h2">Notre travail, sans filtre</h2></div><a class="more" href="galerie">La galerie {I["arr"]}</a></div>
  {strip()}
</div></section>

<section class="sec sec--paper" style="overflow:hidden">{reviews()}</section>

{why_us()}
<section class="sec sec--paper"><div class="wrap">{shop()}</div></section>
<div class="ribbon"></div>
{booking()}
{visit()}'''
    return page("index", "Mama Africa Beauty · Tresses africaines à Payerne",
                "Salon de tresses africaines à Payerne : tresses avec perles, bohème, box braids, nattes, tissage, soins et perruques. Mèches incluses sur nos offres.", body)

def p_tresses():
    sel = [OFFER[k] for k in ("perles", "boheme", "tresses-africaines", "twist-curly", "rasta-elegance")]
    body = pintro("Tresses", "Tresses africaines à Payerne",
                  "Perles, bohème, box braids, twist &amp; curly, rasta, nattes, crochet et transplas. Choisissez un style ou un code du catalogue.",
                  img("reel-nattes", "Tresses collées réalisées au salon", "(max-width: 960px) 100vw, 40vw", eager=True) + '<span class="real">Réalisé au salon</span>', "130", "dès") + f'''
<section class="sec sec--paper"><div class="wrap">{"".join(detail(o, i % 2 == 1) for i, o in enumerate(sel))}</div></section>
<section class="sec" id="codes"><div class="wrap"><div class="shead"><div>{tag("Le catalogue")}<h2 class="h2">Choisissez votre modèle par son code</h2></div></div>{codes_block()}</div></section>
<section class="sec sec--sand"><div class="wrap"><div class="shead"><div>{tag("Tarifs")}<h2 class="h2">Tresses et nattes</h2></div><a class="more" href="tarifs">Tous les tarifs {I["arr"]}</a></div>{ptables(("tresses",))}</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("tresses", "Tresses africaines à Payerne · Perles, bohème, box braids | Mama Africa",
                "Tresses avec perles 130 CHF (perles et mèches offertes), bohème et box braids 150 CHF mèches incluses, twist & curly, rasta, nattes, crochet à Payerne.", body, og="reel-nattes")

def p_famille():
    h, e = OFFER["hommes"], OFFER["enfants"]
    hm = dict(h, incl=MEN_STYLES)
    body = pintro("Hommes &amp; enfants", "Tresses homme et tresses enfant à Payerne",
                  "Six modèles de cornrows pour hommes à 90 CHF. Des tresses légères avec perles colorées pour les enfants à 100 CHF.",
                  img("homme-tresses-2", "Homme aux tresses", "(max-width: 960px) 100vw, 40vw", eager=True), "90", "dès") + f'''
<section class="sec sec--paper"><div class="wrap">{detail(hm)}</div></section>
<section class="sec"><div class="wrap"><div class="shead"><div>{tag("Tresses hommes")}<h2 class="h2">Six modèles, un prix : 90 CHF</h2></div><button class="fly" type="button" data-flyer="affiche-hommes">Voir l'affiche</button></div>
<div class="mstyles">{"".join(f'<figure data-reveal><div class="ph">{img(f"homme-style-{i}", s, "(max-width: 760px) 50vw, 30vw")}</div><figcaption>{s}</figcaption></figure>' for i, s in enumerate(MEN_STYLES, 1))}</div></div></section>
<section class="sec sec--paper"><div class="wrap">{detail(e)}
<div class="mstyles mstyles--4" style="margin-top:40px">{"".join(f'<figure data-reveal><div class="ph">{img(n, "Tresses enfant avec perles", "(max-width: 760px) 50vw, 24vw")}</div></figure>' for n in ("enfants-a", "enfants-b", "enfants-c", "enfants-d"))}</div></div></section>
<div class="ribbon"></div>{booking()}'''
    return page("hommes-enfants", "Tresses hommes et enfants à Payerne | Mama Africa", "Tresses hommes 90 CHF (cornrows, zigzag, couronne, motifs) et tresses enfants avec perles colorées 100 CHF à Payerne.", body, og="homme-tresses-2")

def p_tissage():
    body = pintro("Tissage", "Tissage et extensions à Payerne",
                  "Tissage cousu sur nattes, extensions longues, lisses ou bouclées. Un résultat naturel, coiffage compris.",
                  img("extensions-b", "Extensions bouclées", "(max-width: 960px) 100vw, 40vw", eager=True), "135", "dès") + f'''
<section class="sec sec--paper"><div class="wrap">{detail(OFFER["tissage"])}{detail(OFFER["extensions-longues"], True)}</div></section>
<section class="sec"><div class="wrap split">
  <div class="frame" data-reveal>{img("boutique-cheveux-2", "Cheveux naturels et tissages en boutique", "(max-width: 960px) 100vw, 45vw")}<span class="real">Au salon</span></div>
  <div data-reveal>{tag("Les cheveux")}<h2 class="h2">Choisis avec vous, au salon</h2><div class="prose" style="margin-top:20px"><p class="lead">Cheveux naturels lisses, ondulés ou bouclés, au comptoir de la boutique.</p><p>Nous vous conseillons la longueur, la couleur et la quantité avant la pose. Extensions classiques : 135 CHF.</p></div></div>
</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("tissage", "Tissage & extensions à Payerne | Mama Africa", "Tissage cousu dès 135 CHF, extensions 135 CHF, extensions longues 150 CHF, coiffage compris, à Payerne.", body, og="tissage-ondule")

def p_soins():
    body = pintro("Soins &amp; perruques", "Coiffeuse femme à Payerne : soins, lissage et perruques",
                  "Coupe, couleur, brushing, défrisage, lissage et soins profonds : une coiffeuse pour toutes les femmes, quels que soient vos cheveux, crépus, bouclés, ondulés ou lisses. Et vos perruques retrouvent une seconde vie.",
                  img("perruque-a", "Cheveux lisses et brillants", "(max-width: 960px) 100vw, 40vw", eager=True), "45", "dès") + f'''
<section class="sec sec--paper"><div class="wrap">{detail(OFFER["renovation-perruque"])}</div></section>
<section class="sec"><div class="wrap">{soin_videos()}</div></section>
<section class="sec"><div class="wrap"><div class="shead"><div>{tag("Tarifs")}<h2 class="h2">Soins et lissage</h2></div></div>{ptables(("soins",))}</div></section>
<section class="sec sec--sand"><div class="wrap split">
  <div data-reveal>{tag("Notre approche")}<h2 class="h2">Des cheveux en bonne santé d'abord</h2><div class="prose" style="margin-top:20px"><p class="lead">Avant chaque soin, on regarde la texture, la porosité et le cuir chevelu.</p><p>Puis on choisit le bon geste et le bon produit, souvent disponible à la boutique pour continuer le soin chez vous. La gamme Lowell est utilisée au salon et vendue sur place.</p></div></div>
  <div class="frame" data-reveal>{img("hands-scalp", "Soin du cuir chevelu", "(max-width: 960px) 100vw, 45vw")}</div>
</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("soins", "Soins, défrisage & rénovation de perruque à Payerne | Mama Africa", "Défrisage 65 CHF, brushing 65 CHF, rénovation de perruque 110 CHF, bio-plastie, soins Lowell, coupe et teinture à Payerne.", body, og="perruque-glam")

def p_beaute():
    body = pintro("Beauté", "Extensions de cils et maquillage à Payerne",
                  "Extensions de cils cil à cil et volume russe, sourcils et maquillage, par une spécialiste certifiée.",
                  video("beaute-maquillage", "Essai de rouges à lèvres")) + f'''
<section class="sec sec--paper"><div class="wrap split">
  <div class="frame" data-reveal>{img("neneth-certificat", "Neneth et son certificat d'extension de cils", "(max-width: 960px) 100vw, 45vw")}</div>
  <div data-reveal>{tag("Savoir-faire certifié")}<h2 class="h2">Le regard, par Neneth</h2><div class="prose" style="margin-top:20px"><p class="lead">Avant Mama Africa, il y avait Neneth Beauty, spécialiste des extensions de cils.</p><p>Certifiée cil à cil et volume russe, Neneth apporte la même précision à chaque mise en beauté. Tarifs sur demande, selon la technique.</p></div>
  <div class="btns" style="margin-top:24px"><a class="btn btn--gold" href="{wa("Bonjour Mama Africa, je souhaite un rendez-vous beauté (cils, sourcils ou maquillage).")}" target="_blank" rel="noopener">{I["wa"]}Demander un rendez-vous</a></div></div>
</div></section>
<section class="sec"><div class="wrap">{ptables(("beaute",))}</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("beaute", "Extensions de cils, sourcils & maquillage à Payerne | Mama Africa", "Extensions de cils cil à cil et volume russe, sourcils et maquillage à Payerne.", body, og="makeup")

def p_offres():
    body = pintro("Offres", "Les offres du moment à Payerne",
                  "Mèches offertes, cheveux inclus, prix ronds. Chaque offre a son affiche, à consulter en un clic.",
                  img("boheme-b", "Tresses bohème", "(max-width: 960px) 100vw, 40vw", eager=True), "130", "dès") + f'''
<section class="sec sec--paper"><div class="wrap">{"".join(detail(o, i % 2 == 1) for i, o in enumerate(OFFERS))}</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("offres", "Offres du moment · Mama Africa Payerne", "Tresses avec perles 130 CHF, bohème et tresses africaines 150 CHF mèches incluses, tresses hommes 90 CHF, enfants 100 CHF, rénovation de perruque 110 CHF.", body, og="boheme-1")

def p_tarifs():
    body = pintro("Tarifs", "Tarifs des tresses et soins à Payerne",
                  "Tous nos tarifs, selon la liste en vigueur au salon. Mèches offertes ou incluses lorsque c'est indiqué.",
                  img("rasta-a", "Tresses rasta longues", "(max-width: 960px) 100vw, 40vw", eager=True),
                  extra=f'<p style="margin-top:20px"><button class="fly" type="button" data-flyer="affiche-tarifs">Voir l\'affiche des tarifs</button></p>') + f'''
<section class="sec sec--paper"><div class="wrap">{ptables(("tresses", "famille", "tissage", "soins", "beaute"))}
<p class="hint" style="margin-top:22px">Prix en francs suisses. Sauf mention « offert » ou « inclus », les mèches s'achètent au salon. La bio-plastie se réserve par téléphone.</p></div></section>
<section class="sec" id="codes"><div class="wrap"><div class="shead"><div>{tag("Le catalogue")}<h2 class="h2">Tarifs par code</h2></div></div>{codes_block()}</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("tarifs", "Tarifs · Mama Africa Beauty Payerne", "Nattes 70 CHF, tresses hommes 90 CHF, enfants 100 CHF, rasta courtes 100 CHF, tresses avec ajout 110 CHF, perles 130 CHF, bohème 150 CHF, rasta longues 165 CHF.", body, og="nattes-portrait")

def p_boutique():
    prods = "".join(f'<div class="poster" data-reveal><div class="ph" style="aspect-ratio:1;background:#fff">{img(f"produit-{i}", "Produit en vente à la boutique", "(max-width: 760px) 70vw, 20vw")}</div></div>' for i in range(1, 11))
    body = pintro("Boutique", "Produits pour cheveux afro à Payerne",
                  "Mielle, Lola Cosmetics, Salon Line, Novex, Lowell, mèches X-pression, perruques et cheveux naturels : des marques qu'on trouve très peu ailleurs dans la région, en rayon à Payerne. Du lundi au samedi, sans rendez-vous.",
                  video("salon-visite", "La boutique"), btns=False,
                  extra=f'<div class="btns" style="margin-top:28px"><a class="btn btn--gold" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Venir à la boutique</a><a class="btn btn--line" href="{wa("Bonjour Mama Africa, avez-vous ce produit en stock ?")}" target="_blank" rel="noopener">{I["wa"]}Demander un produit</a></div>') + f'''
<section class="sec sec--paper"><div class="wrap">{shop()}</div></section>
<section class="sec"><div class="wrap">{brand_notes()}</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="shead"><div>{tag("En photos")}<h2 class="h2">La boutique, rayon par rayon</h2></div><button class="fly" type="button" data-flyer="affiche-produits">Nos produits en boutique</button></div>
<div class="shopgrid">{"".join(f'<figure data-reveal class="sg{i}"><div class="ph">{img(n, c, "(max-width: 760px) 100vw, 40vw")}</div><figcaption>{c}</figcaption></figure>' for i, (n, c) in enumerate([("boutique-rayons-1", "Les soins capillaires"), ("boutique-meches", "Le mur des mèches à tresser"), ("boutique-cheveux-2", "Cheveux naturels, tissages et perruques"), ("boutique-rayons-2", "Masques, crèmes et huiles"), ("boutique-vitrine", "L'entrée de la boutique")], 1))}</div></div></section>
<section class="sec"><div class="wrap">{soin_videos()}</div></section>
<section class="sec sec--paper"><div class="wrap"><div class="shead"><div>{tag("En rayon")}<h2 class="h2">Quelques-uns de nos produits</h2></div><button class="fly" type="button" data-flyer="affiche-boutique">L'affiche de la boutique</button></div>
<div class="posters posters--5">{prods}</div></div></section>
<section class="sec"><div class="wrap split" style="align-items:start"><div>{tag("Questions fréquentes")}<h2 class="h2">La boutique en pratique</h2><p class="intro" style="margin-top:16px">Comment choisir ses soins ? Lisez notre guide <a href="produits-cheveux-afro-suisse-romande" style="text-decoration:underline">où acheter des produits pour cheveux afro en Suisse romande</a>.</p></div>{faq(seo.BOUTIQUE_FAQ)}</div></section>
<div class="ribbon"></div>{visit(top=True)}'''
    return page("boutique", "", "", body, og="boutique-rayons-1", ld=seo.jsonld("boutique", crumbs=[("Boutique", "boutique")], faq=seo.BOUTIQUE_FAQ))

GALLERY = [  # (image, caption, filter, is_real_salon_photo) — her own images first, stock only as inspiration
    ("reel-nattes", "Tresses collées longues", "tresses", True), ("perles-a", "Tresses avec perles", "tresses", False),
    ("realisation-tresses", "Pose de tresses au salon", "tresses", True), ("africaines-a", "Tresses africaines", "tresses", False),
    ("transplas-4", "Transplas", "tresses", True), ("boheme-a", "Tresses bohème", "tresses", False),
    ("rasta-a", "Rasta longues Élégance", "tresses", False), ("boutique-meches", "Le mur des mèches", "salon", True),
    ("perles-c", "Modèle avec perles", "tresses", False), ("twist-b", "Twist & curly", "tresses", True),
    ("homme-style-5", "Tresses homme en couronne", "famille", False), ("enfants-a", "Tresses enfant avec perles", "famille", False),
    ("boutique-rayons-1", "Les soins capillaires", "salon", True), ("crochet-volume", "Crochet bouclé volume", "tresses", True),
    ("africaines-b", "Tresses blond 613", "tresses", False), ("extensions-a", "Extensions longues", "tissage", False),
    ("tissage-a", "Tissage cousu sur nattes", "tissage", False), ("perruque-b", "Perruque rénovée", "tissage", False),
    ("boutique-cheveux-2", "Cheveux naturels et tissages", "salon", True), ("twist-a", "Twists torsadées", "tresses", True),
    ("homme-style-1", "Cornrows classiques", "famille", False), ("enfants-d", "Chignon et perles", "famille", False),
    ("perles-d", "Perles et tresses fines", "tresses", False), ("boheme-b", "Bohème cuivré", "tresses", False),
    ("salon-fauteuil", "Le coin shampoing", "salon", True), ("crochet-tendance", "Crochet bouclé tendance", "tresses", True),
    ("rasta-b", "Nattes collées", "tresses", False), ("boutique-rayons-2", "Masques et crèmes", "salon", True),
    ("homme-style-6", "Tresses modernes à motifs", "famille", False), ("enfants-c", "Queue et perles roses", "famille", False),
    ("perruque-a", "Perruque lisse", "tissage", False), ("boutique-vitrine", "L'entrée de la boutique", "salon", True),
    ("realisation-tresses-2", "Tresses en cours", "tresses", True), ("salon-rose", "Le coin beauté", "salon", True),
]
FLYERS = ["affiche-produits", "affiche-perles-130", "affiche-offre-coiffure", "affiche-hommes", "affiche-enfants", "affiche-twist-curly", "affiche-rasta-135",
          "affiche-tissage", "affiche-extensions", "affiche-renovation-perruque", "affiche-crochet", "affiche-transplas", "affiche-codes", "affiche-tarifs", "affiche-boutique"]

def p_galerie():
    figs = "".join(f'<figure data-cat="{c}" data-reveal>{img(n, cap, "(max-width: 760px) 100vw, 33vw")}<span class="src{" is-real" if real else ""}">{"Au salon" if real else "Inspiration"}</span></figure>' for n, cap, c, real in GALLERY)
    figs += "".join(f'<figure data-cat="affiches" data-reveal>{img(f, "Affiche Mama Africa", "(max-width: 760px) 100vw, 33vw")}<span class="src is-real">Affiche</span></figure>' for f in FLYERS)
    filt = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in [("all", "Tout"), ("tresses", "Tresses"), ("famille", "Hommes & enfants"), ("tissage", "Tissage & perruques"), ("salon", "Le salon"), ("affiches", "Nos affiches")])
    body = pintro("Galerie", "Nos tresses en photos",
                  "Nos réalisations et les coulisses du salon (« Au salon »), des idées pour votre prochain style, et toutes nos affiches.",
                  img("perles-c", "Tresses avec perles", "(max-width: 960px) 100vw, 40vw", eager=True), btns=False) + f'''
<section class="sec sec--paper"><div class="wrap"><div class="filters" role="group" aria-label="Filtrer">{filt}</div><div class="masonry" id="masonry">{figs}</div></div></section>
<div class="ribbon"></div>{booking()}'''
    return page("galerie", "Galerie · Mama Africa Payerne", "Réalisations du salon Mama Africa à Payerne, inspirations et affiches.", body, og="reel-nattes")

def p_salon():
    body = pintro("Le salon", "Mama Africa, salon afro et boutique à Payerne",
                  "Un salon de tresses africaines et une boutique de beauté, réunis Rue de Lausanne 38B.",
                  video("salon-tresses", "Pose de tresses au salon")) + f'''
<section class="sec sec--paper"><div class="wrap split">
  <div class="prose" data-reveal>{tag("Qui sommes-nous")}<p class="lead">Mama Africa est une boutique de cosmétiques et de soins capillaires tournée vers la beauté naturelle et l'identité africaine.</p><p>Des produits pour tous les types de cheveux, en particulier crépus, bouclés et en transition. Mais notre vrai cœur, c'est le salon : tresses, nattes, tissage, soins, coiffures africaines traditionnelles et modernes.</p><p>Venez pour les produits, restez pour la coiffure, et repartez avec le sourire.</p></div>
  <div class="frame" data-reveal>{img("salon-fauteuil", "Le salon Mama Africa", "(max-width: 960px) 100vw, 45vw")}<span class="real">Le salon</span></div>
</div></section>
<section class="sec"><div class="wrap split">
  <div class="frame" data-reveal>{img("neneth-certificat", "Neneth, fondatrice", "(max-width: 960px) 100vw, 45vw")}</div>
  <div class="prose" data-reveal>{tag("La fondatrice")}<h2 class="h2" style="margin-bottom:18px">Neneth</h2><p class="lead">Avant Mama Africa, il y avait Neneth Beauty, spécialiste certifiée des extensions de cils.</p><p>Neneth a fait grandir son activité jusqu'à ouvrir une adresse qui réunit le geste et le produit. {SLOGAN}</p>
  <div class="btns" style="margin-top:22px"><a class="btn btn--line" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}Suivre sur Instagram</a></div></div>
</div></section>
<section class="sec sec--sand"><div class="wrap"><div class="shead"><div>{tag("Au salon")}<h2 class="h2">Notre travail, sans filtre</h2></div></div>{strip()}</div></section>
<div class="ribbon"></div>{booking()}'''
    return page("salon", "Le salon · Mama Africa Payerne", "Mama Africa, salon de tresses africaines et boutique beauté à Payerne, fondé par Neneth.", body, og="salon-fauteuil")

def p_avis():
    body = pintro("Avis", "Avis de nos clientes",
                  "Merci à toutes celles et ceux qui partagent leur expérience. Un avis aide d'autres femmes à nous trouver.",
                  img("africaines-b", "Tresses blondes", "(max-width: 960px) 100vw, 40vw", eager=True), btns=False,
                  extra=f'<div class="btns" style="margin-top:28px"><a class="btn btn--gold" href="{G_WRITE}" target="_blank" rel="noopener">Laisser un avis Google</a><a class="btn btn--line" href="{G_REVIEWS}" target="_blank" rel="noopener">Voir sur Google</a></div>') + f'''
<section class="sec sec--paper" style="overflow:hidden">{reviews()}</section>
<div class="ribbon"></div>{booking()}'''
    return page("avis", "Avis clients · Mama Africa Payerne", "Avis Google sur Mama Africa Beauty, salon de tresses africaines à Payerne.", body, og="afro-bijoux")

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
  <h2>Votre demande</h2><p class="hint" style="margin-top:-8px">Elle s'ouvre dans WhatsApp, prête à envoyer. Nous confirmons le créneau par message.</p>
  {picks}<div class="field"><span class="lbl">Un modèle du catalogue ? (facultatif)</span><div class="pick">{codes}</div></div>
  <div class="total"><span>Estimation</span><b id="bf-total">0 CHF</b></div>
  <div class="two"><div class="field"><label for="bf-date">Date souhaitée</label><input id="bf-date" name="date" type="date"></div>
  <div class="field"><label for="bf-time">Moment</label><select id="bf-time" name="time"><option>Matin (9h – 12h)</option><option>Midi (12h – 14h)</option><option>Après-midi (14h – 18h30)</option><option>Peu importe</option></select></div></div>
  <div class="two"><div class="field"><label for="bf-name">Prénom et nom</label><input id="bf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="bf-tel">Téléphone</label><input id="bf-tel" name="tel" type="tel" autocomplete="tel"></div></div>
  <div class="field"><label for="bf-msg">Couleur, longueur, questions</label><textarea id="bf-msg" name="msg" placeholder="Par ex. couleur 27, longueur bas du dos…"></textarea></div>
  <button class="btn btn--wa" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button><p class="hint">Aucune donnée n'est enregistrée sur ce site.</p>
</form>'''
    body = pintro("Réserver", "Prendre rendez-vous",
                  "En ligne sur Salonkee, sur WhatsApp ou par téléphone. Ou détaillez votre demande ci-dessous.",
                  img("salon-fauteuil", "Le salon", "(max-width: 960px) 100vw, 40vw", eager=True), btns=False,
                  extra=f'<div style="margin-top:28px">{ways(light=True)}</div>') + f'''
<section class="sec sec--paper"><div class="wrap split" style="align-items:start">
  {form}<div class="light">{tag("Horaires")}{hours_list()}<div style="margin-top:44px">{tag("Questions fréquentes")}{faq()}</div></div>
</div></section>'''
    return page("reservation", "", "", body, og="salon-fauteuil", ld=seo.jsonld("reservation", crumbs=[("Réserver", "reservation")], faq=FAQ))

def p_contact():
    form = f'''<form class="form form-card" id="contact-form" novalidate><h2>Écrivez-nous</h2>
  <div class="two"><div class="field"><label for="cf-name">Prénom et nom</label><input id="cf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="cf-subj">Sujet</label><select id="cf-subj" name="subj"><option>Rendez-vous coiffure</option><option>Offre du moment</option><option>Produit de la boutique</option><option>Rénovation de perruque</option><option>Autre</option></select></div></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="msg" required></textarea></div>
  <button class="btn btn--wa" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button><p class="hint">Aucune donnée n'est enregistrée sur ce site.</p></form>'''
    body = pintro("Contact", "Nous contacter",
                  "Une question sur un modèle, une offre ou un produit ? Appelez, écrivez sur WhatsApp, ou passez nous voir.",
                  img("boutique-vitrine", "La boutique Mama Africa", "(max-width: 960px) 100vw, 40vw", eager=True), btns=False,
                  extra=f'<div style="margin-top:28px">{ways(light=True)}</div>') + f'''
<section class="sec sec--paper"><div class="wrap split" style="align-items:start">{form}<div>{tag("Questions fréquentes")}{faq(FAQ[:4])}</div></div></section>
<div class="ribbon"></div>{visit(top=True)}'''
    return page("contact", "", "", body, og="boutique-vitrine", ld=seo.jsonld("contact", crumbs=[("Contact", "contact")], faq=FAQ[:4]))

def p_region():
    rows = "".join(f"<tr><th scope=row>{t}</th><td>{c}</td><td>{tr}</td></tr>" for t, c, tr in seo.TOWNS)
    body = pintro("Broye et environs", "Coiffeuse afro pour la Broye, Fribourg et le Nord vaudois",
                  "Il y a très peu de salons spécialisés dans les cheveux afro entre Fribourg et Yverdon. Mama Africa est au centre de Payerne, à 3 minutes à pied de la gare : facile d'accès depuis toute la région.",
                  img("africaines-a", "Tresses africaines longues", "(max-width: 960px) 100vw, 40vw", eager=True)) + f'''
<section class="sec sec--paper"><div class="wrap split" style="align-items:start">
  <div class="prose" data-reveal>{tag("Pourquoi venir à Payerne")}<h2 class="h2" style="margin-bottom:20px">Le salon afro le plus proche de chez vous</h2>
    <p class="lead">Tresses africaines, nattes collées, tissage, défrisage, soins pour cheveux crépus : tout au même endroit, sans aller jusqu'à Lausanne ou Berne.</p>
    <p>Nos clientes viennent d'Estavayer-le-Lac, d'Avenches, de Moudon, de Lucens, de Romont, de Morat, de Fribourg et d'Yverdon-les-Bains. Beaucoup en profitent pour faire le plein de produits à la <a href="boutique">boutique</a> : des marques pour cheveux afro qu'on trouve très peu ailleurs dans la région.</p>
    <p>Pour gagner du temps, envoyez la photo de votre modèle sur WhatsApp : nous vous donnons le prix et la durée avant de venir, et nous préparons les mèches.</p></div>
  <div data-reveal><h3 class="h3" style="margin-bottom:14px">Temps de trajet jusqu'au salon</h3>
    <table class="towns"><thead><tr><th scope=col>Depuis</th><th scope=col>En voiture</th><th scope=col>En train</th></tr></thead><tbody>{rows}</tbody></table>
    <p class="hint" style="margin-top:12px">Temps indicatifs. En train, le salon est à 3 minutes à pied de la gare de Payerne.</p></div>
</div></section>
<section class="sec"><div class="wrap"><div class="shead"><div>{tag("Les offres du moment")}<h2 class="h2">Ce qui vaut le déplacement</h2></div><a class="more" href="offres">Toutes les offres {I["arr"]}</a></div>
  <div class="posters">{"".join(poster(OFFER[k]) for k in ("perles", "boheme", "hommes", "enfants"))}</div></div></section>
<section class="sec sec--paper"><div class="wrap split" style="align-items:start"><div>{tag("Questions fréquentes")}<h2 class="h2">Venir au salon</h2></div>{faq(seo.REGION_FAQ)}</div></section>
<div class="ribbon"></div>{booking()}
{visit()}'''
    return page("coiffure-afro-broye", "", "", body, og="africaines-a", ld=seo.jsonld("coiffure-afro-broye", crumbs=[("Broye et environs", "coiffure-afro-broye")], faq=seo.REGION_FAQ))

def p_conseils():
    cards = "".join(f'''<article class="poster" data-reveal><a class="ph" href="{s}">{img(a["img"], a["h1"], "(max-width: 760px) 76vw, 33vw")}</a><h3><a href="{s}">{a["h1"]}</a></h3><p>{a["intro"][:150].rsplit(" ", 1)[0]}…</p><div class="acts"><a class="more" href="{s}">Lire l\'article {I["arr"]}</a></div></article>''' for s, a in seo.ARTICLES.items())
    body = pintro("Conseils", "Conseils cheveux afro et tresses",
                  "Entretien des tresses, choix du modèle, produits pour cheveux crépus et bouclés : les réponses aux questions qu'on nous pose le plus souvent au salon.",
                  img("perles-c", "Tresses avec perles", "(max-width: 960px) 100vw, 40vw", eager=True), btns=False) + f'''
<section class="sec sec--paper"><div class="wrap"><div class="posters posters--3">{cards}</div></div></section>
<div class="ribbon"></div>{booking()}'''
    return page("conseils", "", "", body, og="perles-c")

def p_article(slug):
    a = seo.ARTICLES[slug]
    secs = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in a["sections"])
    others = "".join(f'<li><a href="{s}">{o["h1"]}</a></li>' for s, o in seo.ARTICLES.items() if s != slug)
    body = f'''<article class="art"><div class="wrap art-grid">
  <div><nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>›</span><a href="conseils">Conseils</a></nav>
    <h1 class="h1" style="font-size:clamp(36px,4.6vw,60px)">{a["h1"]}</h1>
    <p class="intro" style="margin:20px 0 30px">{a["intro"]}</p>
    <div class="art-pic">{img(a["img"], a["h1"], "(max-width: 960px) 100vw, 60vw", eager=True)}</div>
    <div class="art-body prose">{secs}<h2>Questions fréquentes</h2>{faq(a["faq"])}</div></div>
  <aside class="art-side"><div class="rare"><div class="ribbon"></div><div class="rare-in"><h3 class="h3">Prendre rendez-vous</h3><p>Mama Africa, salon de coiffure afro et boutique, Rue de Lausanne 38B à Payerne.</p>{ways(light=True)}</div></div>
    <h3 class="h3" style="margin:34px 0 12px">À lire aussi</h3><ul class="art-more">{others}<li><a href="tarifs">Nos tarifs</a></li></ul></aside>
</div></article>
<div class="ribbon"></div>{booking()}'''
    ld = seo.jsonld(slug, crumbs=[("Conseils", "conseils"), (a["h1"], slug)], faq=a["faq"],
                    article=dict(headline=a["h1"], description=seo.META[slug][1], image=a["img"], slug=slug, date=a["date"]))
    return page(slug, "", "", body, og=a["img"], ld=ld)

def p_conf():
    body = f'''<section class="sec"><div class="wrap" style="max-width:820px">{tag("Informations légales")}<h1 class="h1">Confidentialité</h1>
<div class="prose" style="margin-top:30px"><p><b>Éditeur.</b> {NAME}, {STREET}, {CITY}, Suisse. {PHONE}.</p>
<p><b>Données.</b> Ce site n'enregistre aucune donnée. Les formulaires préparent un message WhatsApp que vous envoyez vous-même. Les réservations en ligne passent par Salonkee.</p>
<p><b>Services tiers.</b> La carte est fournie par Google Maps, qui peut déposer des cookies. Les liens Instagram, WhatsApp, Salonkee et Google ouvrent ces services, soumis à leurs propres règles.</p>
<p><b>Crédits.</b> Photos du salon, de la boutique et affiches : {NAME}. Photos et vidéos d'inspiration : Unsplash et Pexels.</p></div></div></section>'''
    return page("confidentialite", "Confidentialité · Mama Africa", "Informations légales et confidentialité.", body)

def p_404():
    body = f'<section class="nf"><div>{tag("Erreur 404")}<h1 class="h1">Cette page est introuvable</h1><p class="intro" style="margin:20px auto 30px">Elle n\'existe pas ou a été déplacée.</p><div class="btns" style="justify-content:center"><a class="btn" href="./">Retour à l\'accueil</a><button class="btn btn--gold" type="button" data-book>Prendre rendez-vous</button></div></div></section>'
    return page("404", "Page introuvable · Mama Africa", "Page introuvable.", body)

PAGES = {"index": p_index, "tresses": p_tresses, "hommes-enfants": p_famille, "tissage": p_tissage, "soins": p_soins, "beaute": p_beaute,
         "offres": p_offres, "tarifs": p_tarifs, "boutique": p_boutique, "galerie": p_galerie, "salon": p_salon, "avis": p_avis,
         "reservation": p_reservation, "contact": p_contact, "confidentialite": p_conf, "404": p_404,
         "coiffure-afro-broye": p_region, "conseils": p_conseils}
for _s in seo.ARTICLES:
    PAGES[_s] = (lambda s: (lambda: p_article(s)))(_s)

if __name__ == "__main__":
    for f in os.listdir(ROOT):
        if f.endswith(".html") and f[:-5] not in PAGES:
            os.remove(os.path.join(ROOT, f))
    for slug, fn in PAGES.items():
        with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        import datetime
        today = datetime.date.today().isoformat()
        prio = {"index": "1.0", "tresses": "0.9", "boutique": "0.9", "hommes-enfants": "0.8", "tissage": "0.8", "soins": "0.8", "tarifs": "0.8", "offres": "0.8", "coiffure-afro-broye": "0.8", "reservation": "0.7", "contact": "0.7"}
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{'' if s == 'index' else s}</loc><lastmod>{today}</lastmod><priority>{prio.get(s, '0.6')}</priority></url>\n" for s in PAGES if s not in ("404", "confidentialite")) + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\n" + ("Disallow: /\n" if PITCH else f"Allow: /\nSitemap: {BASE}sitemap.xml\n"))
    print("built", len(PAGES), "pages")
