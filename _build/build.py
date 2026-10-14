# -*- coding: utf-8 -*-
"""Static generator for the Mama Africa Beauty site. Run: python3 _build/build.py
Writes every page to the repo root (GitHub Pages serves clean URLs)."""
import os, json, html
from urllib.parse import quote
from PIL import Image
import sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
esc = html.escape

# ---------------------------------------------------------------- icons
I = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-.99.24-3.33-.69-2.81-1.11-4.6-3.98-4.74-4.17-.14-.18-1.13-1.5-1.13-2.87s.72-2.03.97-2.31c.26-.28.56-.35.74-.35l.54.01c.17 0 .41-.07.64.49.25.58.83 2.01.9 2.15.08.14.12.3.03.49-.1.19-.14.3-.28.47-.14.16-.3.37-.42.49-.14.14-.29.29-.12.57.16.28.73 1.2 1.56 1.94 1.07.95 1.98 1.25 2.26 1.39.28.14.44.12.61-.07.16-.19.71-.83.9-1.11.19-.28.37-.23.63-.14.26.09 1.65.78 1.93.92.28.14.47.21.54.33.07.11.07.66-.18 1.35Z"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="3"/><path d="M8 2.5v4M16 2.5v4M3 10h18M8 14h2M14 14h2M8 17.5h2"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.3 7-12a7 7 0 1 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "arr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 6-6 6 6 6"/></svg>',
 "next": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>',
 "g": '<svg class="g-logo" viewBox="0 0 48 48" aria-label="Google"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>',
 "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
 "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11Z"/><path d="M9.5 14.5a2.6 2.6 0 0 0 2.5 2.5"/></svg>',
 "wig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 20c-1-4-1-9 2-12s8-3 10 0 3 8 2 12"/><path d="M8 20c0-5 1-8 4-9 3 1 4 4 4 9"/></svg>',
 "braid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M9 2c0 3 6 3 6 6s-6 3-6 6 6 3 6 6M15 2c0 3-6 3-6 6s6 3 6 6-6 3-6 6"/></svg>',
 "lip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 21h6V11H9v10Z"/><path d="M10 11V6l4-3v8"/></svg>',
 "comb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 3h10v6H7z"/><path d="M8 9v12M10.7 9v12M13.3 9v12M16 9v12"/></svg>',
}
STAR5 = '<span class="stars" aria-label="5 étoiles sur 5">★★★★★</span>'
KENTE = '<span class="kente" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'

BOGOLAN = '''<svg class="bogolan" viewBox="0 0 1200 28" preserveAspectRatio="none" aria-hidden="true"><defs><pattern id="bgl" width="60" height="28" patternUnits="userSpaceOnUse"><path d="M0 14h12l6-8 6 16 6-16 6 16 6-8h18" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="3" cy="4" r="1.3" fill="currentColor"/><circle cx="3" cy="24" r="1.3" fill="currentColor"/><circle cx="57" cy="4" r="1.3" fill="currentColor"/><circle cx="57" cy="24" r="1.3" fill="currentColor"/></pattern></defs><rect width="1200" height="28" fill="url(#bgl)"/></svg>'''

def wa_link(msg="Bonjour Mama Africa, j'aimerais prendre rendez-vous."):
    return f"https://wa.me/{WA}?text={quote(msg)}"

_dims = {}
def dims(name):
    if name not in _dims:
        try:
            with Image.open(os.path.join(IMG, name + ".webp")) as im:
                _dims[name] = im.size
        except FileNotFoundError:
            _dims[name] = (1600, 1067)
    return _dims[name]

def img(name, alt, sizes="(max-width: 760px) 100vw, 50vw", cls="", eager=False, extra="", lazy=True):
    w, h = dims(name)
    has_m = os.path.exists(os.path.join(IMG, name + "-m.webp"))
    src = f"assets/img/{name}.webp"
    srcset = f' srcset="assets/img/{name}-m.webp {dims(name + "-m")[0]}w, {src} {w}w" sizes="{sizes}"' if has_m else ""
    load = 'fetchpriority="high"' if eager else ('loading="lazy"' if lazy else '')
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async"{c}{extra}>'

def video(name, cls="", label=""):
    c = f' class="{cls}"' if cls else ""
    aria = f' aria-label="{esc(label)}"' if label else ' aria-hidden="true"'
    return f'<video{c} src="assets/video/{name}.mp4" poster="assets/video/{name}.webp" muted loop playsinline autoplay preload="metadata"{aria}></video>'

def price_html(p, unit="CHF", pre=None):
    if not p:
        return '<span class="price" style="font-size:20px">Sur demande</span>'
    pre_s = f'<small style="margin:0 4px 0 0">{pre}</small>' if pre else ""
    return f'<span class="price">{pre_s}{p}<small>{unit}</small></span>'

# ---------------------------------------------------------------- shell
NAV = [
    ("index", "Accueil", "./"),
    ("tresses", "Tresses", "tresses"),
    ("soins", "Soins", "soins"),
    ("beaute", "Beauté", "beaute"),
    ("tarifs", "Tarifs", "tarifs"),
    ("boutique", "Boutique", "boutique"),
    ("galerie", "Galerie", "galerie"),
    ("salon", "Le salon", "salon"),
    ("avis", "Avis", "avis"),
    ("contact", "Contact", "contact"),
]
PRESTA = ["tresses", "soins", "beaute", "tarifs"]

def header(cur):
    def a(slug, label, href):
        ac = ' aria-current="page"' if slug == cur else ""
        return f'<a href="{href}"{ac}>{label}</a>'
    dd_cur = " is-current" if cur in PRESTA else ""
    panel = "".join(f'<a href="{h}">{img(i, "", "200px")}<span>{t}<small>{s}</small></span></a>' for h, i, t, s in [
        ("tresses", "braids-portrait", "Tresses", "Box braids, bohème, rastas"),
        ("soins", "afro-glam", "Soins", "Bio-plastie, Lowell, extensions"),
        ("beaute", "makeup", "Beauté", "Cils, sourcils, maquillage"),
        ("tarifs", "products-terracotta2", "Tarifs", "Toutes les prestations"),
    ])
    nav = (a("index", "Accueil", "./") +
           f'<div class="dd{dd_cur}"><button type="button" aria-haspopup="true">Prestations {I["chev"]}</button><div class="dd-panel">{panel}</div></div>' +
           "".join(a(s, l, h) for s, l, h in NAV if s in ("boutique", "galerie", "salon", "avis", "contact")))
    mnav = "".join(f'<a class="big" href="{h}" style="transition-delay:{0.05 + i*0.04:.2f}s">{l}<small>{n:02d}</small></a>' for i, ((s, l, h), n) in enumerate(zip(NAV, range(1, 20))))
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="hdr" id="hdr"><div class="wrap">
  <a class="brand" href="./" aria-label="{SHORT}, accueil"><img src="assets/img/logo.webp" width="731" height="377" alt="Mama Africa Beauty Shop"></a>
  <nav class="nav" aria-label="Navigation principale">{nav}</nav>
  <div class="hdr-cta">
    <a class="icon-btn" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a>
    <a class="icon-btn" href="tel:{TEL}" aria-label="Appeler le {PHONE}">{I["tel"]}</a>
    <button class="btn btn--terra btn--sm" type="button" data-book>{I["cal"]}Réserver</button>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
</div></header>
<nav class="mnav" id="mnav" aria-label="Menu mobile">{mnav}
  <div class="mnav-foot">
    <button class="btn btn--terra" type="button" data-book>{I["cal"]}Réserver un rendez-vous</button>
    <a class="btn btn--light" href="{wa_link()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a>
    <a class="btn btn--ghost" href="tel:{TEL}">{I["tel"]}{PHONE}</a>
  </div>
</nav>'''

def hours_list():
    rows = ""
    for i, (d, o, c) in enumerate(HOURS):
        val = f"{o.replace(':', 'h')} – {c.replace(':', 'h')}" if o else '<span class="off">Fermé</span>'
        rows += f'<li data-day="{(i + 1) % 7}"><span>{d}</span><span>{val}</span></li>'
    return f'<ul class="hours">{rows}</ul>'

def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for s, l, h in NAV[1:6])
    links2 = "".join(f'<li><a href="{h}">{l}</a></li>' for s, l, h in NAV[6:]) + '<li><a href="reservation">Réservation</a></li>'
    return f'''<footer class="ftr">
  <div class="wrap">
    <p class="ftr-big">Venez pour les produits,<br>restez pour <a href="reservation">la coiffure.</a></p>
    <div class="ftr-grid">
      <div>
        <a class="logo-chip" href="./"><img src="assets/img/logo.webp" width="731" height="377" alt="Mama Africa Beauty Shop" loading="lazy"></a>
        <p>Salon de coiffure africaine et boutique de beauté au centre de Payerne.</p>
        <div class="socials">
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a>
          <a href="{wa_link()}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["wa"]}</a>
          <a href="{GMAPS}" target="_blank" rel="noopener" aria-label="Google Maps">{I["pin"]}</a>
          <a href="{SALONKEE}" target="_blank" rel="noopener" aria-label="Réserver sur Salonkee">{I["cal"]}</a>
        </div>
      </div>
      <div><h4>Prestations</h4><ul>{links}</ul></div>
      <div><h4>Découvrir</h4><ul>{links2}</ul></div>
      <div><h4>Nous trouver</h4><ul>
        <li><a href="{GMAPS}" target="_blank" rel="noopener">{STREET}<br>{CITY}</a></li>
        <li><a href="tel:{TEL}">{PHONE}</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></li>
        <li class="muted" style="color:var(--on-night-2)">Lun – Sam · 9h00 – 18h30</li>
      </ul></div>
    </div>
    <div class="ftr-bot"><span>© 2026 {NAME} · Payerne, Suisse</span><span><a href="confidentialite">Confidentialité</a></span></div>
  </div>
</footer>'''

def dock():
    return f'''<div class="dock" id="dock">
  <a class="d-wa" href="{wa_link()}" target="_blank" rel="noopener" aria-label="WhatsApp"><span class="ic">{I["wa"]}</span><span class="tx">Écrire sur WhatsApp</span></a>
  <a class="d-tel" href="tel:{TEL}" aria-label="Appeler"><span class="ic">{I["tel"]}</span><span class="tx">{PHONE}</span></a>
  <button class="d-book" type="button" data-book><span class="ic">{I["cal"]}</span><span class="tx">Réserver</span></button>
</div>
<div class="mbar" id="mbar">
  <a class="m-tel" href="tel:{TEL}">{I["tel"]}Appeler</a>
  <a class="m-wa" href="{wa_link()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a>
  <button class="m-book" type="button" data-book>{I["cal"]}Réserver</button>
</div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-t" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-panel">
    <button class="x" type="button" data-close aria-label="Fermer">{I["x"]}</button>
    <p class="eyebrow">{KENTE}Rendez-vous</p>
    <h2 id="sheet-t">Comment préférez-vous réserver&nbsp;?</h2>
    <p class="muted" style="margin:0">Trois façons, une même attention. Réponse rapide pendant les heures d'ouverture.</p>
    {ways()}
    <p class="form-hint" style="margin-top:18px">Vous préférez détailler votre demande ? <a class="link" href="reservation">Formulaire de réservation {I["arr"]}</a></p>
  </div>
</div>
<div class="lb" id="lb" aria-hidden="true"><button class="x" type="button" aria-label="Fermer">{I["x"]}</button><button class="pv" type="button" aria-label="Précédente">{I["prev"]}</button><img alt=""><button class="nx" type="button" aria-label="Suivante">{I["next"]}</button><p></p></div>'''

def ways():
    return f'''<div class="ways">
      <a class="way" href="{SALONKEE}" target="_blank" rel="noopener"><span class="ic">{I["cal"]}</span><span><b>En ligne sur Salonkee</b><small>Choisissez la prestation et le créneau, 24h/24</small></span>{I["arr"].replace('<svg', '<svg class="arr"')}</a>
      <a class="way wa" href="{wa_link()}" target="_blank" rel="noopener"><span class="ic">{I["wa"]}</span><span><b>Sur WhatsApp</b><small>Envoyez une photo du modèle que vous voulez</small></span>{I["arr"].replace('<svg', '<svg class="arr"')}</a>
      <a class="way tel" href="tel:{TEL}"><span class="ic">{I["tel"]}</span><span><b>Par téléphone</b><small>{PHONE} · Lun – Sam, 9h00 – 18h30</small></span>{I["arr"].replace('<svg', '<svg class="arr"')}</a>
    </div>'''

def schema():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    d = {
        "@context": "https://schema.org", "@type": "HairSalon", "name": NAME,
        "image": BASE + "assets/img/logo.png", "logo": BASE + "assets/img/logo-embleme.png",
        "url": BASE, "telephone": TEL, "priceRange": "CHF 45 – 150",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressRegion": "VD", "addressCountry": "CH"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": "09:00", "closes": "18:30"}],
        "sameAs": [INSTAGRAM, SALONKEE, GMAPS],
        "hasMap": GMAPS,
    }
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def page(slug, title, desc, body, scenes=False, og="portrait-ochre-1"):
    url = BASE + ("" if slug == "index" else slug)
    robots = '<meta name="robots" content="noindex, nofollow">' if PITCH else ""
    three = ('<script type="importmap">{"imports":{"three":"./assets/js/vendor/three.module.min.js"}}</script>\n'
             f'<script type="module" src="assets/js/scene.js?v={V}"></script>') if scenes else ""
    return f'''<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f5efe5">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CH">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/{og}.webp">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/zodiak-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/general-500.woff2" as="font" type="font/woff2" crossorigin>
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
{dock()}
<script src="assets/js/vendor/lenis.min.js"></script>
<script src="assets/js/vendor/gsap.min.js"></script>
<script src="assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="assets/js/site.js?v={V}"></script>
{three}
</body>
</html>'''

# ---------------------------------------------------------------- shared blocks
def eyebrow(t, dark=False):
    return f'<p class="eyebrow">{KENTE}{t}</p>'

def phero(crumb, eyebrow_t, h1, lead, right="", scene=None, tone="espresso", ctas=True, extra=""):
    variant = ' data-variant="edge"' if right and scene == "cowries" else ""
    sc = f'<div class="scene-layer" data-scene-host><canvas data-scene="{scene}" data-tone="{tone}"{variant} aria-hidden="true"></canvas></div>' if scene else ""
    btns = f'''<div class="btns" style="margin-top:34px"><button class="btn btn--terra" type="button" data-book>{I["cal"]}Réserver</button><a class="btn btn--ghost" href="{wa_link()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp</a></div>''' if ctas else ""
    return f'''<section class="phero">
  {sc}
  <div class="wrap phero-grid">
    <div>
      <nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>/</span><span>{crumb}</span></nav>
      {eyebrow(eyebrow_t)}
      <h1 class="display" data-split>{h1}</h1>
      <p class="lead" data-reveal>{lead}</p>
      {btns}{extra}
    </div>
    <div>{right}</div>
  </div>
</section>'''

def arch_media(inner):
    return f'<div class="phero-media veil" data-reveal="fade">{inner}<span class="veil-c"></span></div>'

def style_card(s, book=True):
    p = price_html(s["price"], s["unit"], s.get("pre"))
    return f'''<article class="style-card">
  <div class="ph">{img(s["img"], s["name"], "(max-width: 760px) 78vw, 360px", lazy=False)}<span class="tag">{s["tag"]}</span></div>
  <div class="bd"><h3>{s["name"]}</h3><p>{s["desc"]}</p>
  <div class="row">{p}<a class="btn btn--sm btn--ghost" href="{wa_link("Bonjour Mama Africa, je suis intéressée par : " + s["name"] + ". Quelles sont vos disponibilités ?")}" target="_blank" rel="noopener">Réserver</a></div></div>
</article>'''

def reviews_block(dark=False, title=True):
    def real(r):
        return f'''<article class="rv-card"><div class="rv-top"><span class="rv-av">{r["initial"]}</span><div><b>{esc(r["name"])}</b><small>{r["meta"]}</small></div>{I["g"]}</div>{STAR5}<p>{esc(r["text"])}</p></article>'''
    def ph(i):
        return f'''<article class="rv-card is-ph" aria-hidden="true"><div class="rv-top"><span class="rv-av">★</span><div><b style="color:var(--muted)">Avis Google</b><small>Emplacement réservé</small></div>{I["g"]}</div>{STAR5}<div class="sk w1"></div><div class="sk w2"></div><div class="sk w3"></div><em>Le prochain avis s'affichera ici.</em></article>'''
    cta = f'''<article class="rv-card is-cta"><b>Vous êtes venue au salon&nbsp;?</b><p style="color:var(--on-night-2)">Votre avis aide d'autres femmes à nous trouver.</p><a class="btn btn--light btn--sm" href="{G_WRITE}" target="_blank" rel="noopener">{I["g"]}Laisser un avis</a></article>'''
    row1 = [real(r) for r in REVIEWS] + [ph(i) for i in range(3)] + [cta] + [ph(i) for i in range(2)]
    row2 = [ph(i) for i in range(2)] + [real(r) for r in REVIEWS] + [ph(i) for i in range(2)] + [cta] + [ph(0)]
    def track(cards):
        c = "".join(cards)
        return f'<div class="rv-track">{c}<div style="display:contents" aria-hidden="true">{c}</div></div>'
    head = f'''<div class="wrap"><div class="rv-head">
      <div>{eyebrow("Avis clients")}<h2 class="title" data-split>Elles en parlent<br>mieux que nous.</h2></div>
      <a class="g-score" href="{G_REVIEWS}" target="_blank" rel="noopener">{I["g"]}<div><b>{G_RATING}</b></div><div>{STAR5}<small>{G_COUNT} avis sur Google</small></div></a>
    </div></div>''' if title else ""
    return f'''{head}
  <div class="rv" data-reveal="fade">{track(row1)}</div>
  <div class="rv rv--rev" data-reveal="fade">{track(row2)}</div>'''

def book_band():
    return f'''<section class="sec--tight"><div class="wrap">
  <div class="book" data-reveal>
    <div class="book-grid">
      <div>{eyebrow("Prendre rendez-vous")}<h2 class="title" data-split>Votre prochaine<br>coiffure commence ici.</h2>
      <p class="lead" style="margin-top:22px">Réservez en ligne, envoyez la photo de votre modèle sur WhatsApp ou appelez-nous : on s'occupe du reste.</p></div>
      {ways()}
    </div>
    <svg class="pattern" viewBox="0 0 200 200" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3"><path d="M0 20h200M0 60h200M0 100h200M0 140h200M0 180h200"/><path d="M10 40l20-20 20 20 20-20 20 20 20-20 20 20 20-20 20 20 20-20M10 120l20-20 20 20 20-20 20 20 20-20 20 20 20-20 20 20 20-20"/></g><g fill="currentColor"><circle cx="20" cy="80" r="5"/><circle cx="60" cy="80" r="5"/><circle cx="100" cy="80" r="5"/><circle cx="140" cy="80" r="5"/><circle cx="180" cy="80" r="5"/><circle cx="40" cy="160" r="5"/><circle cx="80" cy="160" r="5"/><circle cx="120" cy="160" r="5"/><circle cx="160" cy="160" r="5"/></g></svg>
  </div>
</div></section>'''

def visit_block(title=True):
    return f'''<section class="sec" id="visite"><div class="wrap visit">
  <div>
    {eyebrow("Nous rendre visite")}
    <h2 class="title" data-split>Au cœur<br>de Payerne.</h2>
    <p class="lead" style="margin:22px 0 26px">{STREET}, {CITY}. Le salon et la boutique sont réunis à la même adresse.</p>
    <span class="open-now" id="open-now"><i></i><span>Horaires</span></span>
    {hours_list()}
    <div class="btns" style="margin-top:30px"><a class="btn" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Itinéraire</a><a class="btn btn--ghost" href="tel:{TEL}">{I["tel"]}{PHONE}</a></div>
  </div>
  <div class="map" data-reveal="fade">
    <iframe title="Carte : Mama Africa Beauty, {STREET}, Payerne" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={quote('Mama Africa beauty shopping, Rue de Lausanne 38, 1530 Payerne')}&z=16&output=embed"></iframe>
    <div class="map-card"><img src="assets/img/logo-embleme.webp" width="582" height="582" alt="" loading="lazy"><div><b>{NAME}</b><small>{STREET} · {CITY}</small></div></div>
  </div>
</div></section>'''

def faq_block(items=FAQ):
    rows = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in items)
    return f'<div class="faq">{rows}</div>'

def menu_block(cats=MENU, dark=False):
    out = ""
    for title, intro, items in cats:
        lis = ""
        for nm, pr, ds in items:
            prh = f'{pr} <small>CHF</small>' if pr else '<small>Sur demande</small>'
            d = f'<span class="ds">{ds}</span>' if ds else ""
            lis += f'<li><span class="nm">{nm}</span><span class="pr">{prh}</span>{d}</li>'
        ip = f"<p>{intro}</p>" if intro else ""
        out += f'<div class="menu-cat" data-reveal><h3>{KENTE}{title}</h3>{ip}<ul class="menu-list">{lis}</ul></div>'
    return f'<div class="menu-grid">{out}</div>'

# ================================================================ PAGES
def p_index():
    cards = "".join(style_card(s) for s in STYLES)
    uni = f'''<div class="uni">
      <a href="tresses" data-tilt>{img("braids-beads-back", "Tresses avec perles, vue de dos", "(max-width: 960px) 50vw, 33vw")}<span class="uni-num">01</span><span class="uni-txt"><b>Tresses &amp; coiffures</b><p>Box braids, bohème, crochet, rastas, transplas, nattes.</p><span class="pill">Découvrir {I["arr"]}</span></span></a>
      <a href="soins" data-tilt>{img("afro-glam", "Cheveux afro volumineux et soignés", "(max-width: 960px) 50vw, 33vw")}<span class="uni-num">02</span><span class="uni-txt"><b>Soins &amp; beauté</b><p>Bio-plastie, Lowell, extensions, cils et maquillage.</p><span class="pill">Découvrir {I["arr"]}</span></span></a>
      <a href="boutique" data-tilt>{img("boutique-allee", "Allée de la boutique Mama Africa à Payerne", "(max-width: 960px) 100vw, 33vw")}<span class="uni-num">03</span><span class="uni-txt"><b>La boutique</b><p>Mèches, perruques, soins capillaires et cosmétiques.</p><span class="pill">Découvrir {I["arr"]}</span></span></a>
    </div>'''
    steps = [
        ("01", "Le diagnostic", "On regarde votre cheveu, on écoute votre envie. Texture, longueur, cuir chevelu : chaque coiffure part de là."),
        ("02", "La préparation", "Démêlage, soin, séparation des raies au millimètre. La base invisible qui fait tenir une tresse des semaines."),
        ("03", "Le tressage", "Trois mèches, des milliers de gestes. Patience, tension régulière, et des mains qui connaissent le métier."),
        ("04", "La signature", "Finitions, bijoux, mise en forme. Vous repartez avec le sourire, et des cheveux sublimés."),
    ]
    st = "".join(f'<div class="weave-step{" is-on" if i == 0 else ""}"><span class="n">{n} / 04</span><b>{t}</b><p>{d}</p></div>' for i, (n, t, d) in enumerate(steps))
    top_menu = [("Tresses & coiffures", "", [("Nattes simples", "55", ""), ("Rasta courtes", "85", ""), ("Tresses avec ajout", "95", "Box braids, knotless…"), ("Crochet bouclé", "120", "Cheveux et pose inclus"), ("Rasta longues", "150", "")]),
                ("Soins & coiffage", "", [("Coupe", "45", ""), ("Défrisage", "50", ""), ("Brushing", "65", ""), ("Bio-plastie capillaire", "95", ""), ("Traitement Lowell", "95", "")])]
    body = f'''
<section class="hero">
  <div class="scene-layer scene-desk" data-scene-host><canvas data-scene="hero" data-tone="ombre" aria-hidden="true"></canvas></div>
  <div class="wrap hero-grid">
    <div>
      {eyebrow("Salon de coiffure africaine · Payerne")}
      <h1 class="display" data-split>L'art de la<br>tresse,<br>porté avec <em>fierté.</em></h1>
      <p class="lead" data-reveal>Tresses, crochets, soins capillaires et boutique de beauté afro, réunis au {STREET} à Payerne. Pour tous les types de cheveux, en particulier crépus, bouclés et en transition.</p>
      <div class="btns" data-reveal>
        <button class="btn btn--terra" type="button" data-book>{I["cal"]}Réserver un rendez-vous</button>
        <a class="btn btn--ghost" href="tarifs">Voir les tarifs {I["arr"]}</a>
      </div>
      <div class="hero-meta" data-reveal>
        <div><b>{G_RATING} {STAR5}</b>Note Google</div>
        <div><b>Lun – Sam</b>9h00 – 18h30</div>
        <div><b>dès 45 CHF</b>Coupe, tresses, soins</div>
      </div>
    </div>
    <div class="hero-visual" data-reveal="fade">
      <div class="arch">{video("tresses-portrait", label="Femme aux longues tresses")}</div>
      <div class="scene-layer scene-mob" data-scene-host><canvas data-scene="hero" data-variant="arch" data-tone="ombre" aria-hidden="true"></canvas></div>
      <figure class="hero-inset" style="margin:0">{video("salon-tresses", label="Pose de tresses au salon Mama Africa")}<figcaption>Au salon, à Payerne</figcaption></figure>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true">Défiler<i></i></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:end">
      <div>{eyebrow("Trois univers, une adresse")}<h2 class="title" data-split>Coiffer, soigner,<br>sublimer.</h2></div>
      <p class="lead" data-reveal>Mama Africa, c'est un salon où l'on prend le temps et une boutique où l'on trouve enfin les produits adaptés aux cheveux texturés. La beauté naturelle, et l'identité africaine, mises en valeur.</p>
    </div>
    {uni}
  </div>
</section>

<section class="weave" data-scene-track>
  <div class="weave-stick">
    <span class="weave-bg-word" aria-hidden="true">tresser</span>
    <div class="weave-stage" data-scene-host><canvas data-scene="weave" data-tone="espresso" aria-hidden="true"></canvas></div>
    <div class="weave-copy">
      {eyebrow("Le geste")}
      <h2 class="title">Une tresse, quatre temps.</h2>
      <div class="weave-steps">{st}</div>
      <div class="weave-bar" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
    </div>
  </div>
</section>

<section class="hcat" id="catalogue">
  <div class="hcat-stick">
    <div class="wrap hcat-head">
      <div>{eyebrow("Le catalogue")}<h2 class="title" data-split>Nos tresses signatures.</h2></div>
      <a class="link" href="tresses">Toutes les coiffures {I["arr"]}</a>
    </div>
    <div class="hcat-track">{cards}</div>
    <div class="hcat-progress"><i></i></div>
  </div>
</section>

<section class="sec sec--sand">
  <div class="wrap real">
    <div class="phones">
      <div class="phone" data-reveal>{video("salon-visite", label="Visite du salon et de la boutique")}<span class="lbl"><img src="assets/img/logo-embleme.webp" alt="" width="582" height="582">mamaafricabeauty_</span></div>
      <div class="phone" data-reveal>{video("salon-tresses", label="Pose de tresses au salon")}<span class="lbl"><img src="assets/img/logo-embleme.webp" alt="" width="582" height="582">Au salon</span></div>
    </div>
    <div>
      {eyebrow("Le salon, en vrai")}
      <h2 class="title" data-split>Pas de filtre.<br>Juste le métier.</h2>
      <p class="lead" style="margin-top:22px" data-reveal>Des murs de mèches de toutes les couleurs, des étagères de soins venus du Brésil, des États-Unis et d'Afrique, et un fauteuil où l'on prend le temps. Bienvenue chez Mama Africa.</p>
      <div class="facts" data-reveal>
        <div><b>6 jours</b><span>sur 7, du lundi au samedi</span></div>
        <div><b>15+</b><span>prestations coiffure et beauté</span></div>
        <div><b>Salon</b><span>et boutique à la même adresse</span></div>
        <div><b>Tous</b><span>les types de cheveux</span></div>
      </div>
      <div class="btns" style="margin-top:30px"><a class="btn" href="salon">Découvrir le salon {I["arr"]}</a><a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}Instagram</a></div>
    </div>
  </div>
</section>

<section class="sec sec--night">
  <div class="wrap">
    <div class="split" style="align-items:end;margin-bottom:clamp(40px,5vw,70px)">
      <div>{eyebrow("Tarifs")}<h2 class="title" data-split>Des prix clairs,<br>affichés.</h2></div>
      <p class="lead" data-reveal>Les mêmes tarifs que sur Salonkee, sans surprise. Pour les mèches, nous vous conseillons au salon la bonne quantité et la bonne couleur.</p>
    </div>
    {menu_block(top_menu)}
    <div class="btns" style="margin-top:44px"><a class="btn btn--light" href="tarifs">Tous les tarifs {I["arr"]}</a><button class="btn btn--ghost" type="button" data-book>{I["cal"]}Réserver</button></div>
  </div>
</section>

<section class="sec">
  <div class="wrap ba-grid">
    <div class="ba" data-ba data-reveal="fade">
      {img("avant-1", "Avant : cheveux longs abîmés", "(max-width: 960px) 100vw, 50vw")}
      {img("apres-1", "Après : cheveux lisses et brillants", "(max-width: 960px) 100vw, 50vw", cls="after")}
      <span class="handle" aria-hidden="true"></span><span class="lab l">Avant</span><span class="lab r">Après</span>
      <input class="sr" type="range" min="0" max="100" value="50" aria-label="Comparer avant et après">
    </div>
    <div>
      {eyebrow("Transformation")}
      <h2 class="title" data-split>Glissez.<br>Voyez la différence.</h2>
      <p class="lead" style="margin-top:22px" data-reveal>Soin, lissage, coupe : un rendez-vous peut tout changer. Faites glisser le curseur pour comparer.</p>
      <div class="btns" style="margin-top:30px"><a class="btn" href="soins">Les soins {I["arr"]}</a><a class="btn btn--ghost" href="galerie">La galerie</a></div>
    </div>
  </div>
</section>

<section class="sec sec--sand" style="overflow:hidden">{reviews_block()}</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:end;margin-bottom:clamp(36px,5vw,60px)">
      <div>{eyebrow("La boutique")}<h2 class="title" data-split>Les bons produits<br>pour vos boucles.</h2></div>
      <p class="lead" data-reveal>Masques, crèmes coiffantes, huiles, mèches et perruques : une sélection pointue pour cheveux crépus, bouclés et en transition, en vente au salon.</p>
    </div>
    <div class="prod-strip">{"".join(f'<div class="prod" data-reveal>{img(f"produit-{i}", "Produits capillaires en vente à la boutique", "(max-width: 760px) 50vw, 20vw")}</div>' for i in (1, 4, 5, 9, 10))}</div>
    <div class="brands" style="margin-top:44px" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div>
    <div class="btns" style="margin-top:36px"><a class="btn" href="boutique">Entrer dans la boutique {I["arr"]}</a></div>
  </div>
</section>

{book_band()}
{visit_block()}
'''
    return page("index", "Mama Africa Beauty · Salon de coiffure africaine à Payerne",
                "Tresses africaines, crochet, rastas, soins capillaires et boutique beauté afro au cœur de Payerne. Réservation en ligne sur Salonkee, WhatsApp ou par téléphone.",
                body, scenes=True)

def p_tresses():
    right = arch_media(img("braids-forest", "Femme aux longues tresses dans la nature", "(max-width: 960px) 90vw, 460px", eager=True))
    feats = ""
    for i, s in enumerate(STYLES):
        rev = " rev" if i % 2 else ""
        p = price_html(s["price"], s["unit"], s.get("pre"))
        note = f'<p class="note">{I["info"]}{s["note"]}</p>' if s["note"] else ""
        extra = ""
        if s["id"] == "crochet":
            models = "".join(f'''<div class="svc" style="box-shadow:0 0 0 1px var(--line)"><div class="ph" style="aspect-ratio:1">{img(im, nm, "(max-width: 760px) 50vw, 220px")}</div><div class="bd" style="padding:16px"><h3 style="font-size:20px">{nm}</h3><div class="colors">{"".join(f'<i style="background:{c}"></i>' for c in cols)}</div><p style="font-size:12.5px">{codes}</p></div></div>''' for nm, im, cols, codes in CROCHET_MODELS)
            extra = f'<div class="svc-grid svc-grid--mini">{models}</div>'
        feats += f'''<article class="feature{rev}" id="{s["id"]}" style="margin-bottom:clamp(70px,9vw,130px)">
  <div class="f-img frame veil" data-reveal="fade" style="border-radius:{"999px 999px var(--r-lg) var(--r-lg)" if i % 3 == 0 else "var(--r-lg)"}">{img(s["img"], s["name"], "(max-width: 960px) 100vw, 58vw")}<span class="veil-c"></span></div>
  <div class="f-txt">
    <p class="eyebrow">{KENTE}{s["tag"]}</p>
    <h2 class="title-s" data-split>{s["name"]}</h2>
    <p class="lead" style="font-size:18px;margin:18px 0 22px" data-reveal>{s["long"]}</p>
    <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap" data-reveal>{p}<a class="btn btn--terra btn--sm" href="{wa_link("Bonjour Mama Africa, je souhaite réserver : " + s["name"] + ".")}" target="_blank" rel="noopener">{I["wa"]}Réserver ce style</a><a class="btn btn--ghost btn--sm" href="{SALONKEE}" target="_blank" rel="noopener">Salonkee</a></div>
    {note}{extra}
  </div>
</article>'''
    body = phero("Tresses", "Tresses & coiffures africaines",
                 "Chaque tresse raconte une histoire.",
                 "Box braids, tresses bohème, crochet bouclé, rastas, transplas et nattes : les coiffures africaines traditionnelles et modernes, posées avec patience au salon de Payerne.",
                 right, scene="hero", tone="miel") + f'''
<section class="sec" style="padding-top:clamp(40px,5vw,70px)"><div class="wrap">
  <div class="filters" role="list">{"".join(f'<a class="chip" href="#{s["id"]}" role="listitem" style="padding:11px 16px;font-size:14px">{s["name"]}</a>' for s in STYLES)}</div>
  <div style="height:clamp(30px,5vw,60px)"></div>
  {feats}
  <p class="note">{I["info"]}La durée d'une pose dépend du modèle, de la longueur et de l'épaisseur. Envoyez une photo de votre modèle sur WhatsApp : nous vous répondons avec une estimation avant le rendez-vous.</p>
</div></section>
<section class="sec sec--sand"><div class="wrap split">
  <div>{eyebrow("Les mèches")}<h2 class="title" data-split>Les mèches,<br>on les a ici.</h2>
  <p class="lead" style="margin-top:22px" data-reveal>Pas besoin de courir les magasins : mèches pour tresses et crochets, cheveux naturels et perruques sont en vente à la boutique. On vous aide à choisir la couleur et la quantité.</p>
  <div class="btns" style="margin-top:30px"><a class="btn" href="boutique">La boutique {I["arr"]}</a></div></div>
  <div class="frame frame--arch veil" data-reveal="fade" style="aspect-ratio:4/5;max-width:520px">{img("boutique-cheveux", "Cheveux et mèches en vente au salon Mama Africa", "(max-width: 960px) 100vw, 45vw")}<span class="veil-c"></span></div>
</div></section>
{book_band()}'''
    return page("tresses", "Tresses africaines à Payerne · Box braids, crochet, rastas | Mama Africa",
                "Box braids, knotless, tresses bohème, crochet bouclé, rastas longues et courtes, transplas et nattes à Payerne. Tarifs affichés et réservation en ligne.", body, scenes=True, og="braids-portrait")

def p_soins():
    cards = ""
    for s in SOINS:
        note = f'<span class="chip chip--green">{s["note"]}</span>' if s.get("note") else ""
        cards += f'''<article class="svc" data-reveal><div class="ph">{img(s["img"], s["name"], "(max-width: 760px) 100vw, (max-width: 960px) 50vw, 33vw")}</div>
  <div class="bd"><div class="meta"><span class="chip chip--terra">{s["tag"]}</span>{note}</div><h3>{s["name"]}</h3><p>{s["desc"]}</p>
  <div class="row">{price_html(s["price"])}<a class="btn btn--sm btn--ghost" href="{wa_link("Bonjour Mama Africa, je souhaite réserver : " + s["name"] + ".")}" target="_blank" rel="noopener">Réserver</a></div></div></article>'''
    body = phero("Soins", "Soins capillaires",
                 "Le soin qui respecte votre boucle.",
                 "Bio-plastie, traitement Lowell, soins hydratants, extensions, défrisage, coupe et couleur : des soins pensés pour les cheveux crépus, bouclés, lisses ou en transition.",
                 "", scene="pick") + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
  <div class="svc-grid">{cards}</div>
</div></section>
<section class="sec sec--night"><div class="wrap split">
  <div class="frame veil" data-reveal="fade" style="aspect-ratio:4/5;border-radius:999px 999px var(--r-lg) var(--r-lg);max-width:520px">{img("hands-scalp", "Soin du cuir chevelu", "(max-width: 960px) 100vw, 45vw")}<span class="veil-c"></span></div>
  <div>{eyebrow("Notre approche")}<h2 class="title" data-split>Des cheveux en<br>bonne santé d'abord.</h2>
  <div class="prose" style="margin-top:24px" data-reveal><p>Nous travaillons avec des produits de qualité qui répondent à tous les types de cheveux, en particulier les cheveux crus, bouclés et en transition.</p><p>Avant chaque soin, on observe la texture, la porosité et l'état du cuir chevelu. Puis on choisit le bon geste, et le bon produit, souvent disponible à la boutique pour prolonger le soin chez vous.</p></div>
  <ul class="ticks" data-reveal><li>Diagnostic du cheveu avant chaque prestation</li><li>Gamme Lowell utilisée au salon et vendue en boutique</li><li>Conseils d'entretien à la maison</li></ul></div>
</div></section>
<section class="sec"><div class="wrap ba-grid">
  <div class="ba" data-ba data-reveal="fade">{img("avant-1", "Avant le soin", "(max-width: 960px) 100vw, 50vw")}{img("apres-1", "Après le soin", "(max-width: 960px) 100vw, 50vw", cls="after")}<span class="handle" aria-hidden="true"></span><span class="lab l">Avant</span><span class="lab r">Après</span><input class="sr" type="range" min="0" max="100" value="50" aria-label="Comparer avant et après"></div>
  <div>{eyebrow("Avant / après")}<h2 class="title" data-split>Le résultat<br>parle de lui-même.</h2><p class="lead" style="margin-top:22px" data-reveal>Faites glisser pour comparer.</p></div>
</div></section>
{book_band()}'''
    return page("soins", "Soins capillaires à Payerne · Bio-plastie, Lowell, extensions | Mama Africa",
                "Bio-plastie capillaire, traitement Lowell, soins cheveux lisses ou ondulés, extensions, défrisage, brushing, coupe et teinture à Payerne.", body, scenes=True, og="afro-glam")

def p_beaute():
    right = arch_media(video("beaute-maquillage", label="Essai de rouges à lèvres"))
    items = [
        ("Extension de cils · cil à cil", "neneth-certificat", "Regard", "Une extension posée sur chaque cil naturel pour un regard intense et naturel. Technique certifiée."),
        ("Extension de cils · volume russe", "makeup", "Volume", "Des bouquets ultra-fins pour un regard plus dense, plus glamour, toujours léger."),
        ("Épilation des sourcils", "portrait-ochre-1", "Sourcils", "Une ligne de sourcils nette et adaptée à votre visage."),
        ("Maquillage", "portrait-gold", "Teint & mise en beauté", "Pour un mariage, une soirée ou une séance photo : un maquillage qui sublime les peaux mates et foncées."),
    ]
    cards = "".join(f'''<article class="svc" data-reveal><div class="ph">{img(im, nm, "(max-width: 760px) 100vw, 50vw")}</div><div class="bd"><div class="meta"><span class="chip chip--terra">{tg}</span></div><h3>{nm}</h3><p>{d}</p><div class="row"><span class="price" style="font-size:20px">Sur demande</span><a class="btn btn--sm btn--ghost" href="{wa_link("Bonjour Mama Africa, je souhaite un rendez-vous pour : " + nm + ".")}" target="_blank" rel="noopener">Demander</a></div></div></article>''' for nm, im, tg, d in items)
    body = phero("Beauté", "Regard, sourcils & maquillage",
                 "La beauté, jusqu'au bout des cils.",
                 "Extensions de cils cil à cil et volume russe, épilation des sourcils et maquillage : la touche finale, réalisée au salon par une spécialiste certifiée.",
                 right, scene="cowries", tone="espresso") + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
  <div class="svc-grid svc-grid--2">{cards}</div>
  <p class="note">{I["info"]}Tarifs communiqués sur demande, selon la technique et le temps de pose. Écrivez-nous sur WhatsApp ou appelez le {PHONE}.</p>
</div></section>
<section class="sec sec--sand"><div class="wrap split">
  <div class="frame veil" data-reveal="fade" style="aspect-ratio:4/5;max-width:500px">{img("neneth-certificat", "Neneth avec son certificat d'extension de cils", "(max-width: 960px) 100vw, 45vw")}<span class="veil-c"></span></div>
  <div>{eyebrow("Savoir-faire certifié")}<h2 class="title" data-split>Formée, certifiée,<br>passionnée.</h2>
  <div class="prose" style="margin-top:24px" data-reveal><p>Avant Mama Africa, il y avait <b>Neneth Beauty</b>, spécialiste des extensions de cils. Neneth est certifiée en extension cil à cil et en volume russe, deux techniques qui demandent précision et patience.</p><p>Ce même soin du détail se retrouve aujourd'hui dans chaque prestation du salon.</p></div>
  <div class="btns" style="margin-top:28px"><a class="btn" href="salon">Notre histoire {I["arr"]}</a></div></div>
</div></section>
{book_band()}'''
    return page("beaute", "Extensions de cils, sourcils & maquillage à Payerne | Mama Africa",
                "Extensions de cils cil à cil et volume russe, épilation des sourcils et maquillage à Payerne, par une spécialiste certifiée.", body, scenes=True, og="makeup")

def p_tarifs():
    body = phero("Tarifs", "Tarifs 2026",
                 "Des prix clairs, sans surprise.",
                 "Toutes nos prestations et leurs tarifs, identiques à ceux affichés sur Salonkee. Les mèches sont en vente au salon, sauf mention « inclus ».",
                 "", scene="hero", tone="bordeaux") + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
  {menu_block()}
  <p class="note">{I["info"]}Prix en francs suisses. La bio-plastie capillaire se réserve par téléphone. Pour les tresses, la quantité de mèches dépend de la longueur et de l'épaisseur souhaitées : nous vous conseillons au salon.</p>
  <div class="btns" style="margin-top:34px"><a class="btn btn--terra" href="{SALONKEE}" target="_blank" rel="noopener">{I["cal"]}Réserver sur Salonkee</a><a class="btn btn--ghost" href="{wa_link("Bonjour Mama Africa, j'ai une question sur vos tarifs.")}" target="_blank" rel="noopener">{I["wa"]}Une question ?</a></div>
</div></section>
<section class="sec sec--sand"><div class="wrap">
  <div class="split" style="align-items:end;margin-bottom:clamp(36px,5vw,60px)"><div>{eyebrow("En images")}<h2 class="title" data-split>Choisir son style.</h2></div><p class="lead" data-reveal>Un aperçu des coiffures les plus demandées, avec leur prix.</p></div>
  <div class="svc-grid svc-grid--4">{"".join(f'<a class="svc" href="tresses#{s["id"]}" data-reveal><div class="ph" style="aspect-ratio:4/5">{img(s["img"], s["name"], "(max-width: 760px) 100vw, 25vw")}</div><div class="bd" style="padding:18px"><h3 style="font-size:22px">{s["name"]}</h3><div class="row" style="padding-top:8px">{price_html(s["price"], s["unit"], s.get("pre"))}</div></div></a>' for s in STYLES)}</div>
</div></section>
{book_band()}'''
    return page("tarifs", "Tarifs · Tresses, soins & beauté à Payerne | Mama Africa",
                "Tous les tarifs de Mama Africa Beauty à Payerne : nattes 55 CHF, tresses avec ajout 95 CHF, crochet 120 CHF, rastas 150 CHF, soins dès 45 CHF.", body, scenes=True, og="products-terracotta")

def p_boutique():
    right = arch_media(video("salon-visite", label="Visite de la boutique Mama Africa"))
    icons = {"meches": I["braid"], "perruques": I["wig"], "soins": I["drop"], "cosmetiques": I["lip"], "accessoires": I["comb"]}
    cats = "".join(f'<div class="cat" data-reveal>{icons[k]}<div><b>{t}</b><small>{d}</small></div></div>' for k, t, d in BOUTIQUE_CATS)
    prods = "".join(f'<div class="prod" data-reveal>{img(f"produit-{i}", "Produit capillaire en vente à la boutique Mama Africa", "(max-width: 760px) 50vw, 20vw")}</div>' for i in range(1, 11))
    body = phero("Boutique", "La boutique beauté afro",
                 "Tout pour vos cheveux, sous un même toit.",
                 "Mèches, perruques, soins capillaires, cosmétiques et accessoires de beauté : une boutique pensée pour les cheveux crépus, bouclés et en transition. Ouverte du lundi au samedi, sans rendez-vous.",
                 right, scene="cowries", tone="espresso", ctas=False,
                 extra=f'<div class="btns" style="margin-top:34px"><a class="btn btn--terra" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}Venir à la boutique</a><a class="btn btn--ghost" href="{wa_link("Bonjour Mama Africa, avez-vous ce produit en stock ?")}" target="_blank" rel="noopener">{I["wa"]}Demander un produit</a></div>') + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
  <div class="cats">{cats}</div>
</div></section>
<section class="sec sec--sand"><div class="wrap">
  <div class="split" style="align-items:end;margin-bottom:clamp(36px,5vw,60px)"><div>{eyebrow("En rayon")}<h2 class="title" data-split>Les soins que vos<br>boucles réclament.</h2></div>
  <p class="lead" data-reveal>Des gammes reconnues pour les cheveux texturés, venues du Brésil, des États-Unis et d'ailleurs, et la gamme Lowell utilisée au salon.</p></div>
  <div class="prod-strip">{prods}</div>
  <div class="brands" style="margin-top:50px" data-reveal>{"".join(f"<span>{b}</span>" for b in BRANDS)}</div>
</div></section>
<section class="sec"><div class="wrap split">
  <div class="phones" style="max-width:520px"><div class="phone" data-reveal>{video("salon-visite", label="Rayons de la boutique")}</div><div class="phone" data-reveal>{img("boutique-cheveux", "Cheveux et mèches au comptoir de la boutique", "260px", extra=' style="width:100%;height:100%;object-fit:cover"')}</div></div>
  <div>{eyebrow("Conseil")}<h2 class="title" data-split>On vous aide<br>à choisir.</h2>
  <div class="prose" style="margin-top:22px" data-reveal><p>Quel masque pour des cheveux secs ? Combien de paquets de mèches pour des rastas longues ? Quelle couleur pour un crochet ? Passez à la boutique ou envoyez-nous un message : on vous répond avec plaisir.</p></div>
  <ul class="ticks" data-reveal><li>Ouvert du lundi au samedi, 9h00 – 18h30</li><li>Sans rendez-vous</li><li>Conseils personnalisés selon votre type de cheveux</li></ul></div>
</div></section>
{visit_block()}'''
    return page("boutique", "Boutique beauté afro à Payerne · Mèches, perruques, soins | Mama Africa",
                "Mèches, perruques, soins capillaires pour cheveux crépus et bouclés, cosmétiques et accessoires de beauté à Payerne. Lola Cosmetics, Salon Line, Novex, Mielle, Lowell.", body, scenes=True, og="produit-10")

GALLERY = [
    ("realisation-tresses", "Tresses avec ajout, posées au salon", "tresses", "Salon"),
    ("transplas-4", "Transplas, réalisés au salon", "tresses", "Salon"),
    ("salon-fauteuil", "Le coin shampoing du salon", "salon", "Salon"),
    ("braids-portrait", "Box braids longues", "tresses", "Inspiration"),
    ("crochet-volume", "Crochet bouclé volume", "crochet", "Salon"),
    ("salon-interieur", "Le salon Mama Africa à Payerne", "salon", "Salon"),
    ("braids-beads-back", "Tresses avec perles", "tresses", "Inspiration"),
    ("crochet-tendance", "Crochet bouclé tendance", "crochet", "Salon"),
    ("cornrows-top", "Nattes collées géométriques", "tresses", "Inspiration"),
    ("apres-1", "Après soin et lissage", "soins", "Salon"),
    ("braids-yellow", "Tresses avec ajout", "tresses", "Inspiration"),
    ("crochet-classique", "Crochet bouclé classique", "crochet", "Salon"),
    ("boutique-cheveux", "Cheveux naturels et mèches en boutique", "salon", "Salon"),
    ("realisation-tresses-2", "Pose de tresses en cours", "tresses", "Salon"),
    ("boutique-rayon", "Rayons de la boutique", "salon", "Salon"),
    ("afro-portrait", "Afro naturel", "soins", "Inspiration"),
    ("transplas-2", "Deux transplas", "tresses", "Salon"),
    ("braids-blonde", "Tresses blond miel", "tresses", "Inspiration"),
    ("crochet-naturel", "Crochet bouclé naturel", "crochet", "Salon"),
    ("cornrows-back2", "Nattes et tresses, vue de dos", "tresses", "Inspiration"),
    ("produit-8", "Soins en boutique", "salon", "Salon"),
    ("curls-portrait", "Boucles définies", "soins", "Inspiration"),
    ("braids-beads", "Tresses et perles colorées", "tresses", "Inspiration"),
    ("locs-portrait", "Twists longs", "tresses", "Inspiration"),
    ("produit-10", "Gamme Mielle en boutique", "salon", "Salon"),
    ("boutique-allee", "Les rayons soins de la boutique", "salon", "Salon"),
    ("salon-rose", "Le coin beauté", "salon", "Salon"),
    ("afro-cowrie", "Afro et bijoux cauris", "soins", "Inspiration"),
]

def p_galerie():
    right = arch_media(img("cornrows-back", "Nattes collées, vue de dos", "(max-width: 960px) 90vw, 460px", eager=True))
    figs = "".join(f'<figure data-cat="{c}" data-reveal>{img(n, cap, "(max-width: 760px) 100vw, 33vw")}<span class="src">{src}</span><figcaption>{cap}</figcaption></figure>' for n, cap, c, src in GALLERY)
    filt = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in [("all", "Tout"), ("tresses", "Tresses"), ("crochet", "Crochet"), ("soins", "Soins & coupes"), ("salon", "Salon & boutique")])
    vids = "".join(f'<div class="vid" data-reveal>{video(v, label=l)}<span>{l}</span></div>' for v, l in [("salon-tresses", "Pose de tresses au salon"), ("salon-visite", "Visite du salon et de la boutique"), ("tresses-portrait", "Inspiration : tresses longues"), ("tresses-terracotta", "Inspiration : tresses fines")])
    body = phero("Galerie", "Réalisations & inspirations",
                 "Regardez, choisissez, on s'occupe du reste.",
                 "Les coiffures et les coulisses du salon, et une sélection d'inspirations pour trouver votre prochain style. Les photos marquées « Salon » viennent de chez nous.",
                 right) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
  <div class="filters" role="group" aria-label="Filtrer la galerie">{filt}</div>
  <div class="masonry" id="masonry">{figs}</div>
</div></section>
<section class="sec sec--night"><div class="wrap">
  <div class="split" style="align-items:end;margin-bottom:clamp(36px,5vw,60px)"><div>{eyebrow("En vidéo")}<h2 class="title" data-split>Le salon en mouvement.</h2></div>
  <p class="lead" data-reveal>Plus de vidéos sur notre Instagram <a class="link" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></p></div>
  <div class="vids">{vids}</div>
</div></section>
{book_band()}'''
    return page("galerie", "Galerie · Tresses, crochets et coiffures africaines | Mama Africa Payerne",
                "Réalisations du salon Mama Africa à Payerne et inspirations : box braids, crochet bouclé, transplas, nattes, soins et coupes.", body, og="braids-beads-back")

def p_salon():
    right = arch_media(video("salon-tresses", label="Pose de tresses au salon Mama Africa"))
    vals = [("Authenticité", "Valoriser la beauté naturelle et l'identité africaine, sans la transformer en mode passagère."),
            ("Savoir-faire", "Des gestes transmis et appris, certifiés pour certains, perfectionnés à chaque rendez-vous."),
            ("Accueil", "Un salon où l'on se sent bien, où l'on prend le temps, et d'où l'on repart avec le sourire.")]
    v = "".join(f'<div class="cat" data-reveal style="min-height:240px"><span class="serif-num" style="font-size:44px;color:var(--terra)">0{i + 1}</span><div><b>{t}</b><small>{d}</small></div></div>' for i, (t, d) in enumerate(vals))
    body = phero("Le salon", "Notre histoire",
                 "Mama Africa, la beauté africaine à Payerne.",
                 "Un salon de coiffure africaine et une boutique de beauté, réunis au cœur de Payerne. Notre vrai cœur ? La coiffure.",
                 right) + f'''
<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap split">
  <div>{eyebrow("Qui sommes-nous")}<h2 class="title" data-split>Venez pour les produits,<br>restez pour la coiffure.</h2></div>
  <div class="prose" data-reveal><p><b>Mama Africa</b> est une boutique spécialisée dans la vente de cosmétiques et de produits de soins capillaires, tournée vers la mise en valeur de la beauté naturelle et de l'identité africaine.</p><p>Nous travaillons avec des produits de qualité qui répondent à tous les types de cheveux, en particulier les cheveux crus, bouclés et en transition.</p><p>Mais notre vrai cœur, c'est le salon. Tresses, soins naturels, coupes, coiffures africaines traditionnelles et modernes : chaque rendez-vous est une expérience où beauté rime avec authenticité. Venez pour les produits, restez pour la coiffure, et repartez avec le sourire et des cheveux sublimés.</p></div>
</div></section>
<section class="sec sec--sand"><div class="wrap feature">
  <div class="f-img frame veil" data-reveal="fade" style="aspect-ratio:4/5;grid-column:1/6">{img("neneth-payerne", "Neneth, fondatrice de Mama Africa, à Payerne", "(max-width: 960px) 100vw, 40vw")}<span class="veil-c"></span></div>
  <div class="f-txt" style="grid-column:7/13">{eyebrow("La fondatrice")}<h2 class="title" data-split>Neneth.</h2>
  <div class="prose" style="margin-top:22px" data-reveal><p>Tout a commencé avec <b>Neneth Beauty</b>, spécialiste des extensions de cils. Certifiée en extension cil à cil et en volume russe, Neneth a fait grandir son activité jusqu'à ouvrir Mama Africa : une adresse où l'on trouve à la fois le geste et le produit.</p><p>Aujourd'hui, le salon de la Rue de Lausanne réunit coiffure africaine, soins, beauté du regard et une boutique bien fournie, avec la même exigence du détail.</p></div>
  <div class="btns" style="margin-top:28px"><a class="btn" href="beaute">Beauté du regard {I["arr"]}</a><a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{I["ig"]}Suivre sur Instagram</a></div></div>
</div></section>
<section class="sec"><div class="wrap">
  {eyebrow("Nos valeurs")}<h2 class="title" data-split style="margin-bottom:clamp(36px,5vw,60px)">Ce qui nous guide.</h2>
  <div class="cats cats--3">{v}</div>
</div></section>
<section class="sec sec--night"><div class="wrap real">
  <div class="phones"><div class="phone" data-reveal>{video("salon-visite", label="Visite du salon")}</div><div class="phone" data-reveal>{img("salon-fauteuil", "Fauteuil et bac à shampoing du salon", "260px", extra=' style="width:100%;height:100%;object-fit:cover"')}</div></div>
  <div>{eyebrow("Le lieu")}<h2 class="title" data-split>Un salon<br>plein de couleurs.</h2>
  <p class="lead" style="margin-top:22px" data-reveal>Murs de mèches, étagères de soins, fauteuils de coiffure et bac à shampoing : tout est là, à deux pas du centre de Payerne.</p>
  <div class="btns" style="margin-top:28px"><a class="btn btn--light" href="{GMAPS}" target="_blank" rel="noopener">{I["pin"]}{STREET}</a></div></div>
</div></section>
{book_band()}'''
    return page("salon", "Le salon · Notre histoire | Mama Africa Beauty Payerne",
                "Mama Africa, salon de coiffure africaine et boutique de beauté à Payerne, fondé par Neneth, spécialiste certifiée en extension de cils.", body, og="salon-interieur")

def p_avis():
    real = "".join(f'''<article class="rv-card" data-reveal style="width:auto"><div class="rv-top"><span class="rv-av">{r["initial"]}</span><div><b>{esc(r["name"])}</b><small>{r["meta"]}</small></div>{I["g"]}</div>{STAR5}<p style="font-size:19px;font-family:var(--serif);line-height:1.4">« {esc(r["text"])} »</p></article>''' for r in REVIEWS)
    body = f'''<section class="phero" style="min-height:auto">
  <div class="scene-layer" data-scene-host><canvas data-scene="cowries" data-tone="espresso" aria-hidden="true"></canvas></div>
  <div class="wrap phero-grid" style="align-items:center">
    <div><nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Accueil</a><span>/</span><span>Avis</span></nav>
    {eyebrow("Avis Google")}<h1 class="display" data-split>Ce qu'elles disent de nous.</h1>
    <p class="lead" data-reveal>Votre confiance est notre plus belle vitrine. Merci à toutes celles et ceux qui prennent le temps de partager leur expérience.</p>
    <div class="btns" style="margin-top:34px"><a class="btn btn--terra" href="{G_WRITE}" target="_blank" rel="noopener">{I["g"]}Laisser un avis Google</a><a class="btn btn--ghost" href="{G_REVIEWS}" target="_blank" rel="noopener">Voir sur Google</a></div></div>
    <div><a class="g-score" href="{G_REVIEWS}" target="_blank" rel="noopener" style="padding:30px 34px;justify-self:end;max-width:380px" data-reveal>{I["g"].replace('class="g-logo"', 'class="g-logo" style="width:46px;height:46px"')}<div><b style="font-size:72px">{G_RATING}</b></div><div>{STAR5}<small>{G_COUNT} avis Google</small></div></a></div>
  </div>
</section>
<section class="sec" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap" style="max-width:860px">{real}</div></section>
<section class="sec sec--sand" style="overflow:hidden">{reviews_block(title=False)}</section>
<section class="sec"><div class="wrap split">
  <div>{eyebrow("Votre avis compte")}<h2 class="title" data-split>Trente secondes<br>qui changent tout.</h2>
  <p class="lead" style="margin-top:22px" data-reveal>Un avis Google aide d'autres femmes à trouver un salon qui sait prendre soin de leurs cheveux. Un clic suffit, même sans écrire de texte.</p>
  <div class="btns" style="margin-top:28px"><a class="btn btn--terra" href="{G_WRITE}" target="_blank" rel="noopener">{I["g"]}Écrire un avis</a></div></div>
  <div class="frame frame--arch veil" data-reveal="fade" style="aspect-ratio:4/5;max-width:480px">{img("curls-laugh", "Cliente souriante aux cheveux bouclés", "(max-width: 960px) 100vw, 45vw")}<span class="veil-c"></span></div>
</div></section>
{book_band()}'''
    return page("avis", "Avis clients · Mama Africa Beauty Payerne",
                "Avis Google sur Mama Africa Beauty, salon de coiffure africaine à Payerne. Laissez votre avis en un clic.", body, scenes=True, og="curls-laugh")

def p_reservation():
    groups = [("Tresses & coiffures", [(s["name"], s["price"]) for s in STYLES]),
              ("Soins & coiffage", [(s["name"], s["price"]) for s in SOINS]),
              ("Beauté", [("Extension de cils", None), ("Épilation des sourcils", None), ("Maquillage", None)])]
    chips = ""
    for g, items in groups:
        c = "".join(f'<label><input type="checkbox" name="svc" value="{esc(n)}" data-price="{p or 0}"><span>{n}<em>{(p + " CHF") if p else "sur demande"}</em></span></label>' for n, p in items)
        chips += f'<div class="field"><span class="lbl">{g}</span><div class="chips">{c}</div></div>'
    form = f'''<form class="form form-card" id="book-form" novalidate>
  <h2 class="title-s">Demande de rendez-vous</h2>
  <p class="form-hint" style="margin-top:-6px">Votre demande s'ouvre dans WhatsApp, prête à envoyer. Nous confirmons le créneau par message.</p>
  {chips}
  <div class="form-total"><span>Estimation</span><b id="bf-total">0 CHF</b></div>
  <div class="two">
    <div class="field"><label for="bf-date">Date souhaitée</label><input id="bf-date" name="date" type="date"></div>
    <div class="field"><label for="bf-time">Moment</label><select id="bf-time" name="time"><option>Matin (9h – 12h)</option><option>Midi (12h – 14h)</option><option>Après-midi (14h – 18h30)</option><option>Peu importe</option></select></div>
  </div>
  <div class="two">
    <div class="field"><label for="bf-name">Prénom et nom</label><input id="bf-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="bf-tel">Téléphone</label><input id="bf-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel"></div>
  </div>
  <div class="field"><label for="bf-msg">Votre modèle, vos questions</label><textarea id="bf-msg" name="msg" placeholder="Longueur, couleur des mèches, photo à envoyer ensuite…"></textarea></div>
  <button class="btn btn--green" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button>
  <p class="form-hint">Aucune donnée n'est enregistrée sur ce site : le message part directement depuis votre WhatsApp.</p>
</form>'''
    body = phero("Réservation", "Prendre rendez-vous",
                 "Réservez votre moment.",
                 "En ligne sur Salonkee, sur WhatsApp ou par téléphone : choisissez la façon qui vous ressemble. Ou remplissez le formulaire, on vous répond rapidement.",
                 "", scene="cowries", tone="espresso", ctas=False) + f'''
<section class="sec" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap split" style="align-items:start">
  <div>
    {eyebrow("Trois façons de réserver")}
    <div class="book" style="padding:clamp(22px,3vw,36px)">{ways()}</div>
    <div style="margin-top:40px">{eyebrow("Horaires")}{hours_list()}</div>
  </div>
  {form}
</div></section>
<section class="sec sec--sand"><div class="wrap split" style="align-items:start">
  <div>{eyebrow("Questions fréquentes")}<h2 class="title" data-split>Bon à savoir<br>avant de venir.</h2></div>
  {faq_block()}
</div></section>'''
    return page("reservation", "Réserver · Mama Africa Beauty Payerne",
                "Réservez votre coiffure africaine, soin ou prestation beauté à Payerne : en ligne sur Salonkee, sur WhatsApp ou au 078 259 77 38.", body, scenes=True, og="braids-smile")

def p_contact():
    form = f'''<form class="form form-card" id="contact-form" novalidate>
  <h2 class="title-s">Écrivez-nous</h2>
  <div class="two"><div class="field"><label for="cf-name">Prénom et nom</label><input id="cf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="cf-subj">Sujet</label><select id="cf-subj" name="subj"><option>Rendez-vous coiffure</option><option>Question sur un produit</option><option>Beauté du regard</option><option>Autre demande</option></select></div></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="msg" required></textarea></div>
  <button class="btn btn--green" type="submit" style="width:100%">{I["wa"]}Envoyer sur WhatsApp</button>
  <p class="form-hint">Le message s'ouvre dans WhatsApp, prêt à envoyer. Aucune donnée n'est enregistrée sur ce site.</p>
</form>'''
    tiles = f'''<div class="ways" style="margin-top:30px">
      <a class="way" style="background:var(--card);box-shadow:0 0 0 1px var(--line)" href="tel:{TEL}"><span class="ic" style="background:var(--ochre);color:var(--ink)">{I["tel"]}</span><span><b>{PHONE}</b><small class="muted">Appel ou SMS</small></span></a>
      <a class="way wa" style="background:var(--card);box-shadow:0 0 0 1px var(--line)" href="{wa_link()}" target="_blank" rel="noopener"><span class="ic">{I["wa"]}</span><span><b>WhatsApp</b><small class="muted">Réponse rapide, photos bienvenues</small></span></a>
      <a class="way" style="background:var(--card);box-shadow:0 0 0 1px var(--line)" href="{INSTAGRAM}" target="_blank" rel="noopener"><span class="ic" style="background:var(--ink)">{I["ig"]}</span><span><b>{IG_HANDLE}</b><small class="muted">Nos dernières réalisations</small></span></a>
      <a class="way" style="background:var(--card);box-shadow:0 0 0 1px var(--line)" href="{GMAPS}" target="_blank" rel="noopener"><span class="ic">{I["pin"]}</span><span><b>{STREET}</b><small class="muted">{CITY} · Itinéraire</small></span></a>
    </div>'''
    body = phero("Contact", "Contact",
                 "Parlons de vos cheveux.",
                 "Une question sur une coiffure, un produit, un tarif ? Appelez, écrivez sur WhatsApp ou passez au salon : nous sommes là du lundi au samedi.",
                 "", scene="pick", ctas=False, extra=tiles) + f'''
<section class="sec" style="padding-top:clamp(20px,3vw,40px)"><div class="wrap split" style="align-items:start">
  {form}
  <div>{eyebrow("Questions fréquentes")}{faq_block(FAQ[:4])}</div>
</div></section>
{visit_block()}'''
    return page("contact", "Contact · Mama Africa Beauty, Rue de Lausanne 38B, Payerne",
                "Contactez Mama Africa Beauty à Payerne : 078 259 77 38, WhatsApp, Instagram. Rue de Lausanne 38B, 1530 Payerne. Lundi – samedi 9h00 – 18h30.", body, scenes=True, og="portrait-ochre-2")

def p_confidentialite():
    body = f'''<section class="sec" style="padding-top:calc(var(--hdr) + 80px)"><div class="wrap" style="max-width:820px">
  {eyebrow("Informations légales")}<h1 class="title">Confidentialité</h1>
  <div class="prose" style="margin-top:34px">
  <h3>Éditeur</h3><p>{NAME}, {STREET}, {CITY}, Suisse. Téléphone : {PHONE}.</p>
  <h3>Données personnelles</h3><p>Ce site n'enregistre aucune donnée. Les formulaires de réservation et de contact préparent un message dans WhatsApp : c'est vous qui l'envoyez, depuis votre propre application. Les réservations en ligne passent par Salonkee, selon ses propres conditions.</p>
  <h3>Services tiers</h3><p>La carte est fournie par Google Maps. En l'affichant, Google peut déposer des cookies et traiter votre adresse IP selon sa politique de confidentialité. Les liens vers Instagram, WhatsApp, Salonkee et Google ouvrent ces services, soumis à leurs propres règles.</p>
  <h3>Cookies</h3><p>Le site lui-même n'utilise ni cookies publicitaires ni outil de mesure d'audience.</p>
  <h3>Crédits photo</h3><p>Photos du salon et de la boutique : {NAME}. Photos d'inspiration : Unsplash et Pexels, sous leurs licences respectives.</p>
  <h3>Contact</h3><p>Pour toute question : {PHONE} ou sur WhatsApp.</p>
  </div>
</div></section>'''
    return page("confidentialite", "Confidentialité · Mama Africa Beauty", "Informations légales et confidentialité du site Mama Africa Beauty, Payerne.", body)

def p_404():
    body = f'''<section class="nf"><div>{eyebrow("Erreur 404")}<h1 class="display">Cette page s'est<br>dé-tressée.</h1><p class="lead" style="margin:24px auto 34px">La page que vous cherchez n'existe pas ou a été déplacée.</p><div class="btns" style="justify-content:center"><a class="btn" href="./">Retour à l'accueil</a><button class="btn btn--terra" type="button" data-book>{I["cal"]}Réserver</button></div></div></section>'''
    return page("404", "Page introuvable · Mama Africa Beauty", "Page introuvable.", body)

PAGES = {
    "index": p_index, "tresses": p_tresses, "soins": p_soins, "beaute": p_beaute, "tarifs": p_tarifs,
    "boutique": p_boutique, "galerie": p_galerie, "salon": p_salon, "avis": p_avis,
    "reservation": p_reservation, "contact": p_contact, "confidentialite": p_confidentialite, "404": p_404,
}

if __name__ == "__main__":
    for slug, fn in PAGES.items():
        with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    urls = [BASE + ("" if s == "index" else s) for s in PAGES if s not in ("404",)]
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\n" + ("Disallow: /\n" if PITCH else f"Allow: /\nSitemap: {BASE}sitemap.xml\n"))
    print("built", len(PAGES), "pages")
