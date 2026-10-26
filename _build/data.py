# -*- coding: utf-8 -*-
"""Business facts for Mama Africa Beauty, Payerne.
Prices: her October 2026 "Investissement" price list and offer flyers (sent on WhatsApp, 14.10.2026)
take precedence over the older Salonkee list, which is kept only for services the new flyers don't cover."""

PITCH = True  # lead pitch: keep noindex until she signs
BASE = "https://welcometothenextlevel.github.io/mamaafrica/"
V = "46"  # cache-busting for css/js

NAME = "Mama Africa Beauty"
SHORT = "Mama Africa"
PHONE = "078 624 29 24"
TEL = "+41786242924"
WA = "41786242924"  # her main number since 23.10.2026 (meeting notes)
STREET = "Rue de Lausanne 38B"
CITY = "1530 Payerne"
GEO = (46.8195624, 6.936667)
SLOGAN = "Votre beauté, notre passion."

SALONKEE = "https://salonkee.ch/salon/mamaafrica-brut"
INSTAGRAM = "https://www.instagram.com/mamaafricabeauty_/"
IG_HANDLE = "@mamaafricabeauty_"
PLACE_ID = "ChIJ0cFaUjh3jkcR9RJt4YtSH2Y"
GMAPS = "https://maps.google.com/?cid=7358691076882633461"
G_REVIEWS = f"https://search.google.com/local/reviews?placeid={PLACE_ID}"
G_WRITE = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"
G_RATING = "5,0"
G_COUNT = 2

HOURS = [  # her flyer: "Lundi au samedi 9h00 – 18h30"
    ("Lundi", "09:00", "18:30"), ("Mardi", "09:00", "18:30"), ("Mercredi", "09:00", "18:30"),
    ("Jeudi", "09:00", "18:30"), ("Vendredi", "09:00", "18:30"), ("Samedi", "09:00", "18:30"),
    ("Dimanche", None, None),
]

# ---------- current offers (her flyers, latest first: 14–15.10.2026) ----------
OFFERS = [
    dict(id="perles", title="Tresses avec perles", price="130", img="perles-a", badge="Perles offertes",
         flyer="affiche-perles-130",
         lead="Tresses soignées ornées de perles. Les perles et un paquet de mèches sont offerts par la maison, coiffure comprise.",
         incl=["Perles offertes", "1 paquet de mèches offert", "Coiffure comprise dans le prix"]),
    dict(id="boheme", title="Tresses bohème", price="150", img="boheme-a", badge="Mèches incluses",
         flyer="affiche-offre-coiffure",
         lead="Quatre modèles bohème, boucles libres sur toute la longueur. Paquets de mèches inclus : 150 CHF pour chaque modèle.",
         incl=["Paquets de mèches inclus", "4 modèles au choix", "Boucles libres, effet naturel"]),
    dict(id="tresses-africaines", title="Tresses africaines", price="150", img="africaines-a", badge="Mèches offertes",
         flyer="affiche-africaines",
         lead="Box braids longues, du brun chocolat au blond 613. Les paquets de mèches sont offerts.",
         incl=["Paquets de mèches offerts", "Toutes longueurs", "Toutes couleurs"]),
    dict(id="twist-curly", title="Twist & Curly", price="150", img="twist-b", badge="Longue tenue",
         flyer="affiche-twist-curly",
         lead="Twists torsadées et boucles : un style élégant, soigné et propre, pour toutes les occasions.",
         incl=["Longue tenue", "Style élégant", "Soigné et propre"]),
    dict(id="rasta-elegance", title="Rasta longues Élégance", price="135", img="rasta-a", badge="Cheveux inclus",
         flyer="affiche-rasta-135",
         lead="Nattes collées longues au dessin travaillé, avec baby hair. Cheveux, soin et finition compris.",
         incl=["Cheveux inclus", "Soin et finition", "Baby hair"]),
    dict(id="hommes", title="Tresses hommes", price="90", img="homme-style-5", badge="6 modèles",
         flyer="affiche-hommes",
         lead="Cornrows classiques, droites vers l'arrière, zigzag, raie au milieu, couronne ou motifs modernes.",
         incl=["Coupe nette, finitions propres", "Produits de qualité", "Rapide et professionnel"]),
    dict(id="enfants", title="Tresses enfants avec perles", price="100", img="enfants-a", badge="Perles colorées",
         flyer="affiche-enfants",
         lead="Des tresses jolies, légères et confortables, adaptées aux enfants, avec perles de couleur.",
         incl=["Tresses légères", "Protection des cheveux", "Perles de différentes couleurs"]),
    dict(id="boheme-4", title="Bohème « comme celle-là »", price="150", img="boheme-a", badge="4 modèles",
         flyer="affiche-4-modeles",
         lead="Quatre modèles bohème bouclés, 150 CHF chacun. Les mèches s'achètent sur place, nous vous aidons à choisir.",
         incl=["4 modèles au choix", "150 CHF par modèle", "Mèches à acheter sur place"]),
    dict(id="promo-boheme", title="Promo bohème", price="150", img="boheme-b", badge="Cheveux offerts",
         flyer="affiche-promo-boheme",
         lead="Le modèle bohème bouclé à 150 CHF, avec deux paquets de cheveux offerts, inclus dans le prix.",
         incl=["2 paquets de cheveux offerts", "Inclus dans le prix", "Sur rendez-vous"]),
    dict(id="transplas", title="Transplas", price="65", pre="dès", img="transplas-4", badge="2 ou 4 tresses",
         flyer="affiche-transplas",
         lead="Deux transplas 65 CHF, quatre transplas 100 CHF. Propre, élégant et durable. Les cheveux s'achètent sur place.",
         incl=["2 transplas : 65 CHF", "4 transplas : 100 CHF", "Cheveux à acheter sur place"]),
    dict(id="crochet", title="Crochet bouclé", price="120", img="crochet-volume", badge="4 modèles",
         flyer="affiche-crochet",
         lead="Quatre bouclés au choix (classique, volume, naturel, tendance), chacun en plusieurs couleurs. Cheveux et pose inclus.",
         incl=["Cheveux et pose inclus", "4 modèles, plusieurs couleurs", "Léger et naturel"]),
    dict(id="garcons", title="Tresses garçons", price="50", img="garcon-4", badge="Avec ou sans ajouts",
         flyer="affiche-garcons-50",
         lead="Des nattes collées pour les garçons, avec ou sans ajouts : lignes droites, motifs, couronnes. Choisissez le modèle, on s'occupe du reste.",
         incl=["Avec ou sans ajouts", "Lignes, motifs ou couronnes", "Propre et durable"]),
    dict(id="tissage", title="Tissage cousu", price="120", pre="dès", img="tissage-a", badge="Coiffage inclus",
         flyer="affiche-tissage",
         lead="Pose de tissage cousue sur nattes, pour un résultat naturel. Coiffage compris.",
         incl=["Pose professionnelle", "Tresses bien faites", "Finition soignée"]),
    dict(id="extensions-longues", title="Extensions longues", price="150", img="extensions-a", badge="Toutes textures",
         flyer="affiche-extensions",
         lead="Des extensions pour tous les types de cheveux : lisses, ondulées, bouclées, frisées ou crépues, en cheveux naturels de toutes origines. Posées sur tresses bien faites, pour un résultat naturel.",
         incl=["Toutes les textures de cheveux", "Cheveux de toutes origines", "Pose professionnelle, coiffage inclus"]),
    dict(id="soin-collagene", title="Soin nourrissant collagène & karité", price="95", img="soin-collagene", badge="Cheveux secs et abîmés",
         flyer="affiche-soin-collagene",
         lead="Le masque Ecolchi au collagène et au beurre de karité, appliqué au salon : il nourrit les cheveux secs et abîmés, et leur rend douceur et souplesse.",
         incl=["Aide à nourrir les cheveux", "Douceur et souplesse", "Traitement réalisé au salon"]),
    dict(id="soin-brillance", title="Soin douceur & brillance", price="95", img="lissage-a", badge="Lissage professionnel",
         flyer="affiche-lissage",
         lead="Un lissage professionnel avec le shampoing et le soin EVORK : il lisse la fibre, réduit le volume et discipline les frisottis, pour des cheveux doux, brillants effet miroir et faciles à coiffer.",
         incl=["Cheveux doux et soyeux", "Brillants et faciles à coiffer", "Soin réalisé au salon"]),
    dict(id="soin-boucles", title="Soin des boucles Meu Cacho", price="95", img="boucles-a", badge="Ammatrão Meu Cacho",
         flyer="affiche-meu-cacho",
         lead="Un soin pour mettre vos boucles à l'honneur, avec la crème Ammatrão Meu Cacho : des boucles bien définies et un volume naturel.",
         incl=["Définition des boucles", "Volume naturel", "Soin réalisé au salon"]),
    dict(id="soin-botox", title="Botox capillaire Onix", price="95", img="lissage-a", badge="Brillance, douceur, souplesse",
         flyer="affiche-botox-onix",
         lead="Le soin botox capillaire Onix offre un nouvel éclat à vos cheveux : brillance, douceur et souplesse. Le traitement est réalisé au salon, sur rendez-vous.",
         incl=["Brillance, douceur, souplesse", "95 CHF le traitement", "Sur rendez-vous"]),
    dict(id="soin-botox-gold", title="Botox Lisoplastia Gold Show", price="95", img="lissage-a", badge="Huile d'argan, coco, karité",
         flyer="affiche-botox-gold",
         lead="Un botox ultra hydratant, anti-volume et anti-frisottis, à l'huile d'argan, à l'huile de coco et au beurre de karité, sans formol. Traitement au salon, produit aussi disponible à l'achat.",
         incl=["Ultra hydratant, anti-frisottis", "0 % formol", "Produit aussi en vente"]),
    dict(id="renovation-perruque", title="Rénovation de perruque", price="50", img="perruque-b", badge="Seconde vie",
         flyer="affiche-perruque-50",
         lead="Nettoyage, soin, démêlage, remise en forme, ajustement et finition professionnelle.",
         incl=["Nettoyage, soin, démêlage", "Remise en forme, ajustement", "Finition professionnelle"]),
]
OFFER = {o["id"]: o for o in OFFERS}

MEN_STYLES = ["Tresses classiques (cornrows)", "Tresses droites vers l'arrière", "Tresses en zigzag", "Raie au milieu (center part)", "Tresses en couronne (style royal)", "Tresses modernes à motifs"]

# ---------- model codes (her catalogue flyer) ----------
CODES = [(1, "125"), (2, "100"), (3, "125"), (4, "125"), (5, "125"), (6, "135"), (7, "125"), (8, "135"), (9, "115")]

# ---------- price list ----------
MENU = {
    "tresses": ("Tresses & nattes", [
        ("Nattes simples", "70", "Nattes simples et naturelles"),
        ("Rasta courtes", "100", "Nattes collées avec locks courtes"),
        ("Diverses tresses avec ajout", "100", "Tresses variées avec mèches"),
        ("Tresses avec perles", "130", "Perles + 1 paquet de mèches offerts, coiffure comprise"),
        ("Rasta longues · Élégance", "135", "Cheveux inclus, soin, finition, baby hair"),
        ("Tresses africaines", "150", "Paquets de mèches offerts"),
        ("Tresses bohème · 4 modèles", "150", "Paquets de mèches inclus"),
        ("Twist & Curly", "150", "Longue tenue"),
        ("Rasta longues", "120", "Nattes collées avec locks longues"),
        ("Crochet bouclé", "120", "Cheveux et pose inclus"),
        ("Transplas · 2 / 4 tresses", "65 / 100", "Cheveux à acheter sur place"),
    ]),
    "famille": ("Hommes & enfants", [
        ("Tresses hommes · 6 modèles", "90", "Cornrows, zigzag, couronne, motifs…"),
        ("Tresses enfants avec perles colorées", "100", "Légères, confortables, perles au choix"),
        ("Tresses garçons", "50", "Avec ou sans ajouts"),
    ]),
    "tissage": ("Tissage & extensions", [
        ("Extensions ou tissage", "120", "Pose d'extensions ou tissage"),
        ("Tissage cousu sur nattes", "dès 120", "Coiffage inclus"),
        ("Extensions longues", "150", "Coiffage inclus"),
    ]),
    "soins": ("Soins, lissage & perruques", [
        ("Défrisage des cheveux", "65", "Défrisage et soin protecteur"),
        ("Brushing", "65", "Brushing simple ou wavy"),
        ("Soin nourrissant collagène & karité", "95", "Masque Ecolchi, pour cheveux secs et abîmés"),
        ("Soin douceur & brillance", "95", "Rituel EVORK, shampoing et après-shampoing"),
        ("Soin des boucles Meu Cacho", "95", "Définition des boucles et volume naturel"),
        ("Soin au collagène Karseell", "95", "Douceur, souplesse, brillance"),
        ("Botox capillaire Onix", "95", "Brillance, douceur, souplesse"),
        ("Botox Lisoplastia Gold Show", "95", "Ultra hydratant, anti-frisottis"),
        ("Rénovation de perruque", "50", "Nettoyage, soin, remise en forme"),
        ("Bio-plastie capillaire", "95", "Sur rendez-vous téléphonique"),
        ("Soin cheveux lisses ou ondulés", "85", ""),
        ("Traitement produits Lowell", "95", ""),
        ("Coupe", "45", ""),
        ("Teinture", "55", ""),
    ]),
    "beaute": ("Beauté", [
        ("Extension de cils · cil à cil", None, "Sur demande"),
        ("Extension de cils · volume russe", None, "Sur demande"),
        ("Épilation des sourcils", None, "Sur demande"),
        ("Maquillage", None, "Sur demande"),
    ]),
}

SHADES = [  # braiding hair colour codes, as on her crochet flyer
    ("1B", "#1f1611", "Noir naturel"), ("2", "#3a2213", "Brun très foncé"), ("4", "#5a341b", "Châtain"),
    ("27", "#b57a3c", "Blond miel"), ("30", "#8a4320", "Auburn"), ("350", "#9c4519", "Cuivré"),
    ("613", "#dcc08a", "Blond platine"), ("BUG", "#6a1828", "Bordeaux"), ("99J", "#52122e", "Prune"),
]

BOUTIQUE_CATS = [
    ("Mèches & extensions", "Mèches pour tresses et crochets, extensions pour toutes les textures, cheveux de toutes origines."),
    ("Perruques", "À essayer au salon, rénovation possible."),
    ("Soins capillaires", "Masques, crèmes coiffantes, huiles pour cheveux texturés."),
    ("Cosmétiques", "Soins visage et corps, maquillage."),
    ("Accessoires", "Perles, peignes, bonnets, foulards."),
    ("Produits africains", "Savon noir, beurre de karité, farine de maïs…"),
]
BRANDS = ["Lola Cosmetics", "Salon Line", "Novex", "Mielle", "O Boticário", "Lowell", "X-pression"]

REVIEWS = [
    dict(name="Pierre Fall", meta="Local Guide · Avis Google", initial="P",
         text="Une expérience client des plus riches et un accueil super professionnel. Je vous recommande fortement comme coiffeur et esthétique. Vite, vite, elle vous attend !"),
]

FAQ = [
    ("Les mèches sont-elles comprises ?", "Oui sur nos offres : tresses africaines et tresses bohème à 150 CHF (paquets de mèches inclus), tresses avec perles à 130 CHF (perles et un paquet offerts), rasta longues Élégance à 135 CHF et crochet bouclé à 120 CHF (cheveux inclus). Pour les autres coiffures, les mèches s'achètent sur place et nous vous aidons à choisir la quantité et la couleur."),
    ("Comment choisir mon modèle ?", "Parcourez notre catalogue de codes (1 à 9) ou envoyez-nous une photo sur WhatsApp. Indiquez simplement le code au moment de réserver."),
    ("Faut-il prendre rendez-vous ?", "Oui pour la coiffure : sur Salonkee, sur WhatsApp ou au 078 624 29 24. La boutique est ouverte sans rendez-vous du lundi au samedi."),
    ("Combien de temps dure une pose ?", "Cela dépend du modèle, de la longueur et de l'épaisseur. Envoyez une photo sur WhatsApp, nous vous donnons une estimation avant le rendez-vous."),
    ("Vous coiffez les enfants ?", "Oui : nattes, transplas et tresses se font aussi pour les enfants. Précisez l'âge en réservant."),
    ("Vous rénovez les perruques ?", "Oui, 50 CHF : nettoyage, soin, démêlage, remise en forme, ajustement et finition professionnelle."),
]
