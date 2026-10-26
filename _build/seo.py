# -*- coding: utf-8 -*-
"""SEO layer for the Mama Africa site: per-page titles/descriptions, JSON-LD, and the editorial
content of the area page and the "Conseils" articles.

Keyword map (one main query per page, so pages don't compete with each other):
  index            coiffeuse afro Payerne / salon de coiffure afro Payerne
  tresses          tresses africaines Payerne (box braids, knotless, perles, bohème, nattes collées)
  hommes-enfants   tresses homme Payerne, cornrows, tresses enfant
  tissage          tissage Payerne, pose d'extensions
  soins            coiffeuse femme Payerne, défrisage, lissage, rénovation de perruque
  beaute           extension de cils Payerne
  offres           offre tresses / mèches offertes Payerne
  tarifs           prix tresses africaines
  boutique         produits cheveux afro Payerne, mèches, perruques, Mielle / Lola / Salon Line
  coiffure-afro-broye   coiffeuse afro Estavayer / Avenches / Moudon / Fribourg (one hub, no page per town)
  conseils + 3 articles  long-tail questions
"""
import json
from data import *  # noqa

SALON_ID = BASE + "#salon"

META = {
    "index": ("Coiffeuse afro à Payerne · Tresses africaines | Mama Africa",
              "Salon de coiffure afro à Payerne : tresses africaines, box braids, nattes, tissage, défrisage, perruques. Mèches offertes sur nos offres. Boutique afro."),
    "tresses": ("Tresses africaines à Payerne · Box braids, perles, bohème",
                "Tresses africaines à Payerne dès 40 CHF : box braids, knotless, tresses avec perles, bohème, twist, rasta, nattes collées. Mèches offertes sur nos offres."),
    "hommes-enfants": ("Tresses homme et enfant à Payerne · Dès 50 CHF",
                       "Tresses pour hommes à Payerne : cornrows, zigzag, couronne, motifs, 69 CHF. Tresses enfant avec perles colorées 65 CHF, tresses garçon 50 CHF. Sur rendez-vous, Rue de Lausanne 38B."),
    "tissage": ("Tissage et extensions à Payerne · Pose cousue dès 100 CHF",
                "Tissage cousu dès 100 CHF, extensions longues 100 CHF, pour toutes les textures de cheveux, lisses à crépues, toutes origines. Coiffage compris, Rue de Lausanne 38B, Payerne."),
    "soins": ("Coiffeuse femme à Payerne · Défrisage, lissage, perruques",
              "Coiffeuse pour femmes à Payerne : défrisage 65 CHF, brushing, bio-plastie, soins Lowell, coupe, couleur, rénovation de perruque. Tous types de cheveux."),
    "beaute": ("Extension de cils à Payerne · Cil à cil, volume russe",
               "Extensions de cils cil à cil et volume russe, épilation des sourcils et maquillage à Payerne, par une spécialiste certifiée. Sur rendez-vous."),
    "offres": ("Offres tresses à Payerne · Mèches offertes | Mama Africa",
               "Les offres du moment à Payerne : tresses avec perles 85 CHF, tresses africaines 110 CHF mèches offertes, promo bohème 120 CHF, tresses homme 69 CHF, enfant 65 CHF."),
    "tarifs": ("Prix des tresses africaines à Payerne · Tarifs Mama Africa",
               "Tous nos tarifs : transplas dès 40 CHF, tresses homme 69 CHF, nattes 70 CHF, perles 85 CHF, tresses avec ajout 100 CHF, tresses africaines 110 CHF, tissage dès 100 CHF."),
    "boutique": ("Produits cheveux afro à Payerne · Mèches, perruques, Mielle",
                 "Boutique afro à Payerne : Mielle, Lola Cosmetics, Salon Line, Novex, mèches X-pression, perruques et cheveux naturels. Des marques rares en Suisse romande."),
    "galerie": ("Photos de tresses africaines · Galerie Mama Africa Payerne",
                "Nos tresses africaines, nattes, tissages et perruques en photos, réalisés au salon Mama Africa à Payerne, et nos affiches d'offres."),
    "salon": ("Salon afro à Payerne · Mama Africa, Rue de Lausanne 38B",
              "Mama Africa, salon de coiffure afro et boutique de beauté au centre de Payerne, à 3 minutes de la gare. Tresses, soins, produits pour cheveux texturés."),
    "avis": ("Avis clients · Mama Africa, coiffeuse afro à Payerne",
             "Les avis Google de nos clientes sur Mama Africa, salon de coiffure afro à Payerne. Laissez votre avis en un clic."),
    "reservation": ("Prendre rendez-vous · Coiffeuse afro à Payerne | Mama Africa",
                    "Réservez vos tresses africaines, tissage, soin ou beauté à Payerne : en ligne sur Salonkee, sur WhatsApp ou au 078 624 29 24. Lundi au samedi, 9h – 18h30."),
    "contact": ("Contact · Mama Africa, Rue de Lausanne 38B, Payerne",
                "Mama Africa Beauty, Rue de Lausanne 38B, 1530 Payerne, à 3 minutes de la gare. 078 624 29 24, WhatsApp, Instagram. Lundi au samedi 9h00 – 18h30."),
    "coiffure-afro-broye": ("Coiffeuse afro près d'Estavayer, Avenches et Fribourg",
                            "Salon afro de la Broye, à 15 min d'Estavayer et d'Avenches, 25 min de Fribourg, 30 min d'Yverdon. Tresses africaines, tissage et produits afro à Payerne."),
    "conseils": ("Conseils cheveux afro et tresses · Mama Africa Payerne",
                 "Entretien des tresses africaines, choisir entre box braids, knotless et bohème, où trouver des produits pour cheveux afro en Suisse romande : nos conseils."),
    "entretien-tresses-africaines": ("Entretenir ses tresses africaines : le guide pratique",
                                     "Combien de temps garder ses tresses, laver le cuir chevelu, dormir avec, hydrater et défaire ses tresses sans abîmer ses cheveux : nos conseils."),
    "box-braids-knotless-boheme": ("Box braids, knotless ou bohème : quelles tresses choisir ?",
                                   "Les différences entre box braids, knotless braids et tresses bohème : tension, rendu, entretien, prix. Le guide de Mama Africa, salon de tresses à Payerne."),
    "produits-cheveux-afro-suisse-romande": ("Où acheter des produits pour cheveux afro en Suisse romande",
                                             "Mielle, Lola Cosmetics, Salon Line, Novex, mèches X-pression : où trouver des produits pour cheveux crépus et bouclés en Suisse romande, et comment les choisir."),
}

SERVICE_TYPES = {
    "tresses": ("Tresses africaines", ["tresses"]),
    "hommes-enfants": ("Tresses homme et enfant", ["famille"]),
    "tissage": ("Tissage et extensions", ["tissage"]),
    "soins": ("Soins capillaires, défrisage et lissage", ["soins"]),
    "beaute": ("Extensions de cils et maquillage", ["beaute"]),
}

AREA = ["Payerne", "Corcelles-près-Payerne", "Granges-Marnand", "Estavayer-le-Lac", "Avenches", "Moudon", "Lucens",
        "Romont", "Morat", "Fribourg", "Yverdon-les-Bains", "Broye", "Vully"]

def _price(p):
    try: return str(int(str(p).replace("dès", "").split("/")[0].strip()))
    except Exception: return None

def _offers(keys):
    out = []
    for k in keys:
        for n, p, d in MENU[k][1]:
            o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
            v = _price(p)
            if v:
                o.update({"price": v, "priceCurrency": "CHF"})
            out.append(o)
    return out

def salon_jsonld(full=True):
    d = {"@type": "HairSalon", "@id": SALON_ID, "name": NAME, "alternateName": "Mama Africa Beauty Shop",
         "url": BASE, "telephone": TEL, "image": [BASE + "assets/img/logo.png", BASE + "assets/img/boutique-rayons-1.webp"],
         "logo": BASE + "assets/img/logo-embleme.png", "priceRange": "CHF 40 – 150",
         "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressRegion": "VD", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]}, "hasMap": GMAPS,
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:30"}],
         "sameAs": [INSTAGRAM, SALONKEE, GMAPS], "slogan": SLOGAN,
         "areaServed": [{"@type": "Place", "name": a} for a in AREA],
         "knowsLanguage": ["fr"],
         "department": {"@type": "Store", "name": "Mama Africa Beauty Shop", "description": "Boutique de produits pour cheveux afro, mèches, perruques et cosmétiques",
                        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "1530", "addressLocality": "Payerne", "addressCountry": "CH"}, "telephone": TEL},
         "potentialAction": {"@type": "ReserveAction", "target": SALONKEE}}
    if full:
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Prestations",
                                "itemListElement": [{"@type": "OfferCatalog", "name": MENU[k][0], "itemListElement": _offers([k])} for k in ("tresses", "famille", "tissage", "soins", "beaute")]}
    return d

def jsonld(slug, crumbs=None, faq=None, article=None):
    """crumbs: [(name, slug)], faq: [(q, a)], article: dict(headline, description, image)"""
    graph = [salon_jsonld(full=slug in ("index", "tarifs", "contact", "salon"))]
    if slug == "index":
        graph.append({"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME, "inLanguage": "fr-CH", "publisher": {"@id": SALON_ID}})
    if slug in SERVICE_TYPES:
        name, keys = SERVICE_TYPES[slug]
        graph.append({"@type": "Service", "name": name + " à Payerne", "serviceType": name, "provider": {"@id": SALON_ID},
                      "areaServed": [{"@type": "Place", "name": a} for a in AREA[:9]], "url": BASE + slug,
                      "offers": _offers(keys)})
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE}]
        items += [{"@type": "ListItem", "position": i + 2, "name": n, "item": BASE + s} for i, (n, s) in enumerate(crumbs)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if article:
        graph.append({"@type": "Article", "headline": article["headline"], "description": article["description"],
                      "image": BASE + "assets/img/" + article["image"] + ".webp", "inLanguage": "fr-CH",
                      "datePublished": article.get("date", "2026-10-20"), "dateModified": article.get("date", "2026-10-20"),
                      "author": {"@id": SALON_ID}, "publisher": {"@id": SALON_ID}, "mainEntityOfPage": BASE + article["slug"]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"

CRUMB = {"tresses": "Tresses", "hommes-enfants": "Hommes & enfants", "tissage": "Tissage", "soins": "Soins & perruques",
         "beaute": "Beauté", "offres": "Offres", "tarifs": "Tarifs", "boutique": "Boutique", "galerie": "Galerie",
         "salon": "Le salon", "avis": "Avis", "reservation": "Réserver", "contact": "Contact",
         "coiffure-afro-broye": "Broye et environs", "conseils": "Conseils"}

# ---------------------------------------------------------------- boutique: the rare-brands argument
BRAND_NOTES = [
    ("Mielle", "La marque américaine connue pour son huile romarin-menthe, et ses soins pour cheveux texturés et bouclés."),
    ("Lola Cosmetics", "Soins brésiliens pour cheveux bouclés et crépus : masques, crèmes coiffantes, après-shampoings."),
    ("Salon Line", "La référence brésilienne des boucles : crèmes de coiffage et gels pour des boucles définies."),
    ("Novex", "Masques hydratants brésiliens en grand format, pour nourrir les cheveux secs et abîmés."),
    ("O Boticário", "Cosmétiques et soins brésiliens pour le corps, le visage et les cheveux."),
    ("Lowell", "Soins professionnels brésiliens, utilisés au salon et vendus à la boutique."),
    ("X-pression", "Les mèches pour tresses que l'on utilise au salon, dans toutes les couleurs."),
    ("Ecolchi", "Masque au collagène et au beurre de karité, pour réparer et faire briller."),
]
BOUTIQUE_FAQ = [
    ("Où trouver des produits pour cheveux afro près de Payerne ?", "À la boutique Mama Africa, Rue de Lausanne 38B à Payerne. Nous vendons des marques pour cheveux crépus, bouclés et en transition qu'on trouve rarement ailleurs dans la région : Mielle, Lola Cosmetics, Salon Line, Novex, Lowell, ainsi que des mèches X-pression et des perruques."),
    ("Faut-il prendre rendez-vous pour acheter des produits ?", "Non, la boutique est ouverte du lundi au samedi de 9h00 à 18h30, sans rendez-vous."),
    ("Vous vendez des mèches pour tresses ?", "Oui, des mèches pour tresses et crochets dans de nombreuses couleurs (1B, 2, 4, 27, 30, 350, 613, bordeaux…), ainsi que des cheveux naturels pour tissages et extensions."),
    ("Je ne trouve pas un produit, pouvez-vous le commander ?", "Écrivez-nous sur WhatsApp avec le nom ou la photo du produit : nous vous disons s'il est en stock ou s'il peut être commandé."),
]
REGION_FAQ = [
    ("Y a-t-il une coiffeuse afro près d'Estavayer-le-Lac ou d'Avenches ?", "Oui : Mama Africa est à Payerne, à environ 15 minutes en voiture d'Estavayer-le-Lac et d'Avenches. Tresses africaines, tissage, défrisage et soins pour cheveux crépus, sur rendez-vous."),
    ("Comment venir en train ?", "Le salon est à 3 minutes à pied de la gare de Payerne, desservie directement depuis Fribourg, Yverdon-les-Bains, Moudon et Lausanne."),
    ("Puis-je réserver à distance ?", "Oui, en ligne sur Salonkee, sur WhatsApp ou par téléphone au 078 624 29 24. Envoyez une photo du modèle souhaité pour une estimation."),
]

TOWNS = [  # (town, by car, by train) — rounded travel times to Rue de Lausanne 38B
    ("Corcelles-près-Payerne", "5 min", "—"), ("Granges-Marnand", "10 min", "8 min"), ("Avenches", "15 min", "10 min"),
    ("Estavayer-le-Lac", "15 min", "15 min"), ("Lucens", "15 min", "15 min"), ("Moudon", "20 min", "20 min"),
    ("Morat", "20 min", "20 min"), ("Fribourg", "25 min", "25 min"), ("Romont", "25 min", "—"),
    ("Yverdon-les-Bains", "30 min", "30 min"), ("Lausanne", "45 min", "55 min"),
]

ARTICLES = {
    "entretien-tresses-africaines": dict(
        h1="Entretenir ses tresses africaines : le guide pratique", img="perles-a", date="2026-10-20",
        intro="Des tresses bien entretenues restent belles plus longtemps et protègent vraiment vos cheveux. Voici ce que nous conseillons à nos clientes au salon, à Payerne.",
        sections=[
            ("Combien de temps garder ses tresses ?", "Comptez en général entre quatre et huit semaines selon le modèle et la pousse. Au-delà, les cheveux qui repoussent s'emmêlent à la racine et les tresses tirent davantage. Après les avoir défaites, laissez idéalement vos cheveux respirer quelques jours avec un soin profond avant une nouvelle pose."),
            ("Laver le cuir chevelu sans abîmer les tresses", "Toutes les une à deux semaines, diluez un shampoing doux dans de l'eau et appliquez-le directement sur le cuir chevelu, entre les raies, en massant du bout des doigts. Rincez abondamment, puis essorez les tresses dans une serviette sans frotter. Séchez bien les longueurs : des tresses qui restent humides longtemps peuvent sentir mauvais."),
            ("Hydrater sans graisser", "Un spray hydratant léger sur les longueurs et quelques gouttes d'huile sur le cuir chevelu suffisent. Évitez les produits lourds qui s'accumulent à la base des tresses. À la boutique, nous avons des huiles, sprays et crèmes adaptés aux cheveux crépus."),
            ("La nuit : foulard ou bonnet en satin", "Le satin limite les frottements, garde l'hydratation et évite les frisottis. C'est le geste le plus simple pour garder des tresses nettes plus longtemps."),
            ("Les signes qu'une tresse est trop serrée", "Des petits boutons à la racine, une douleur qui dure plus de deux jours ou un cuir chevelu qui tire sont des signaux à ne pas ignorer. Une bonne pose ne doit pas faire mal. Si c'est le cas, passez nous voir."),
            ("Défaire ses tresses", "Prenez votre temps : coupez la mèche sous la longueur naturelle, défaites la tresse, puis démêlez doucement avec un peu d'huile ou d'après-shampoing, du bas vers le haut. Les cheveux perdus pendant la pose sont normaux : ils sont restés coincés dans la tresse."),
        ],
        faq=[("Combien de temps peut-on garder des tresses africaines ?", "Entre quatre et huit semaines en général, selon le modèle et la pousse de vos cheveux."),
             ("Peut-on laver ses cheveux avec des tresses ?", "Oui, toutes les une à deux semaines, en appliquant un shampoing dilué directement sur le cuir chevelu, puis en séchant bien les longueurs.")]),
    "box-braids-knotless-boheme": dict(
        h1="Box braids, knotless ou bohème : quelles tresses choisir ?", img="boheme-a", date="2026-10-20",
        intro="Ce sont les trois demandes les plus fréquentes au salon. Elles se ressemblent, mais ne se posent pas de la même façon et ne donnent pas le même rendu.",
        sections=[
            ("Les box braids, le grand classique", "La tresse démarre par un petit nœud à la racine, autour duquel on ajoute la mèche. Le résultat est très net, avec une base bien marquée, et la coiffure tient longtemps. C'est un style polyvalent, des tresses fines aux plus épaisses, de toutes les longueurs."),
            ("Les knotless braids, plus légères à la racine", "Pas de nœud : on commence la tresse avec vos propres cheveux et on ajoute la mèche progressivement. La racine est plus plate et plus naturelle, et la tension sur le cuir chevelu plus douce dès le premier jour. La pose demande un peu plus de temps."),
            ("Les tresses bohème, l'effet libre", "Des tresses fines dans lesquelles on laisse des boucles s'échapper sur toute la longueur. Le rendu est plus léger, plus romantique. Les boucles demandent un peu d'entretien : un spray hydratant et quelques gouttes d'huile pour les garder définies."),
            ("Et les prix chez Mama Africa ?", "Diverses tresses avec ajout dès 100 CHF, tresses africaines longues à 110 CHF et tresses bohème à 150 CHF avec les paquets de mèches inclus, tresses avec perles à 85 CHF avec perles et un paquet de mèches offerts. Tous les tarifs sont sur notre page Tarifs."),
            ("Comment choisir ?", "Si vous voulez une coiffure très nette qui dure, les box braids. Si votre cuir chevelu est sensible ou si vous voulez un rendu plus naturel, les knotless. Pour un look plus doux et féminin, la bohème. Le plus simple : envoyez-nous une photo du modèle sur WhatsApp, nous vous conseillons."),
        ],
        faq=[("Quelle est la différence entre box braids et knotless ?", "Les box braids démarrent par un nœud à la racine ; les knotless commencent avec vos propres cheveux, sans nœud, pour une racine plus plate et moins de tension."),
             ("Combien coûtent des tresses bohème à Payerne ?", "Chez Mama Africa, de 110 à 150 CHF selon le modèle, et 120 CHF pour la promo bohème avec deux paquets de cheveux offerts.")]),
    "produits-cheveux-afro-suisse-romande": dict(
        h1="Où acheter des produits pour cheveux afro en Suisse romande ?", img="boutique-rayons-1", date="2026-10-20",
        intro="Trouver des soins pour cheveux crépus et bouclés dans les grandes surfaces suisses reste compliqué. Beaucoup commandent en ligne depuis la France, avec les frais de port et parfois de douane. À Payerne, il existe une autre solution.",
        sections=[
            ("Des marques rares dans la région, en rayon à Payerne", "La boutique Mama Africa propose des marques qu'on trouve très peu ailleurs en Suisse romande : Mielle, Lola Cosmetics, Salon Line, Novex, O Boticário, Lowell, ainsi que les mèches X-pression, des cheveux naturels et des perruques. Vous voyez le produit, vous demandez conseil, vous repartez avec."),
            ("Bien choisir selon son type de cheveux", "Les cheveux crépus aiment l'eau et les corps gras : un leave-in hydratant, puis une huile ou un beurre pour sceller l'hydratation. Les cheveux bouclés préfèrent des crèmes de coiffage et des gels qui définissent la boucle sans l'alourdir. Les cheveux en transition ont besoin de soins profonds réguliers pour fortifier la zone de démarcation."),
            ("Masques et soins profonds", "Une fois par semaine, un masque nourrissant fait une vraie différence sur des cheveux secs. Les grands formats brésiliens (Novex, Lola) sont économiques et très appréciés. Pour réparer en profondeur, nous proposons aussi des soins au salon : bio-plastie, traitement Lowell."),
            ("Mèches, perruques et accessoires", "Pour une pose de tresses, la bonne quantité de mèches dépend de la longueur et de l'épaisseur voulues : nous vous la calculons. La boutique propose aussi bonnets et foulards en satin, peignes, perles pour tresses et des produits africains comme le savon noir et le beurre de karité."),
        ],
        faq=BOUTIQUE_FAQ[:3]),
}
