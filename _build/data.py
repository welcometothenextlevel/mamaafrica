# -*- coding: utf-8 -*-
"""Business facts for Mama Africa Beauty, Payerne.
Prices: her October 2026 "Investissement" price list and offer flyers (sent on WhatsApp, 14.10.2026)
take precedence over the older Salonkee list, which is kept only for services the new flyers don't cover."""

PITCH = True  # lead pitch: keep noindex until she signs
BASE = "https://welcometothenextlevel.github.io/mamaafrica/"
V = "10"  # cache-busting for css/js

NAME = "Mama Africa Beauty"
SHORT = "Mama Africa"
PHONE = "078 259 77 38"
TEL = "+41782597738"
WA = "41782597738"  # confirmed: her code flyer shows this number with the WhatsApp logo
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
G_COUNT = 1

HOURS = [  # her flyer: "Lundi au samedi 9h00 – 18h30"
    ("Lundi", "09:00", "18:30"), ("Mardi", "09:00", "18:30"), ("Mercredi", "09:00", "18:30"),
    ("Jeudi", "09:00", "18:30"), ("Vendredi", "09:00", "18:30"), ("Samedi", "09:00", "18:30"),
    ("Dimanche", None, None),
]

# ---------- current offers (her flyers) ----------
OFFERS = [
    dict(id="tresses-africaines", title="Tresses africaines", price="150", img="box-braids-longues",
         badge="Mèches offertes", flyer=None,
         lead="Box braids longues, du brun chocolat au blond 613. Les paquets de mèches sont offerts.",
         incl=["Paquets de mèches offerts", "Toutes longueurs, toutes couleurs", "Sur rendez-vous"]),
    dict(id="boheme", title="Tresses bohème", price="150", img="boheme-1", badge="Promo",
         flyer="affiche-promo-boheme",
         lead="Tresses fines et boucles libres, effet bohème. Deux paquets de cheveux offerts, inclus dans le prix.",
         incl=["2 paquets de cheveux offerts", "Boucles libres sur toute la longueur", "Blond miel, cuivré ou brun"]),
    dict(id="twist-curly", title="Twist & Curly", price="150", img="boheme-3", badge="Longue tenue",
         flyer="affiche-twist-curly",
         lead="Twists torsadées avec boucles : un style élégant, soigné et propre, pour toutes les occasions.",
         incl=["Longue tenue", "Style élégant", "Soigné et propre"]),
    dict(id="rasta-elegance", title="Rasta longues · Élégance", price="135", img="nattes-portrait",
         badge="Cheveux inclus", flyer="affiche-rasta-135",
         lead="Nattes collées longues au dessin travaillé, avec baby hair. Cheveux, soin et finition compris.",
         incl=["Cheveux inclus", "Soin et finition", "Baby hair"]),
    dict(id="perles", title="Modèles avec perles", price="130", img="perles-1", badge="Tradition",
         flyer="affiche-perles",
         lead="Tresses soignées ornées de perles : élégance, style et tradition. Les perles s'achètent sur place.",
         incl=["Tresses soignées", "Perles de qualité en boutique", "Style unique"]),
    dict(id="tissage", title="Tissage cousu", price="135", pre="dès", img="tissage-ondule", badge="Naturel",
         flyer="affiche-tissage",
         lead="Pose de tissage cousue sur nattes, pour un résultat naturel. Coiffage compris.",
         incl=["Pose professionnelle", "Tresses bien faites", "Coiffage inclus", "Finition soignée"]),
    dict(id="extensions-longues", title="Extensions longues", price="150", img="extensions-lisses", badge="Longueur",
         flyer="affiche-extensions",
         lead="Pose d'extensions longues, lisses ou bouclées, sur tresses bien faites. Résultat naturel, coiffage compris.",
         incl=["Pose professionnelle", "Résultat naturel", "Coiffage inclus"]),
    dict(id="renovation-perruque", title="Rénovation de perruque", price="110", img="perruque-glam", badge="Seconde vie",
         flyer="affiche-renovation-perruque",
         lead="Votre perruque comme neuve : nettoyage, soin, démêlage, remise en forme, ajustement et finition.",
         incl=["Nettoyage, soin, démêlage", "Remise en forme, ajustement", "Finition professionnelle"]),
]

# ---------- model codes (her catalogue flyer) ----------
CODES = [(1, "125"), (2, "100"), (3, "125"), (4, "125"), (5, "125"), (6, "135"), (7, "125"), (8, "135"), (9, "115")]

# ---------- price list ----------
MENU = {
    "tresses": ("Tresses & nattes", [
        ("Nattes simples", "70", "Nattes simples et naturelles"),
        ("Rasta courtes", "100", "Nattes collées avec locks courtes"),
        ("Diverses tresses avec ajout", "110", "Tresses variées avec mèches"),
        ("Modèles avec perles", "130", "Perles à acheter sur place"),
        ("Rasta longues · Élégance", "135", "Cheveux inclus, soin, finition, baby hair"),
        ("Tresses africaines", "150", "Paquets de mèches offerts"),
        ("Tresses bohème", "150", "2 paquets de cheveux offerts"),
        ("Twist & Curly", "150", "Longue tenue"),
        ("Rasta longues", "165", "Nattes collées avec locks longues"),
        ("Crochet bouclé", "120", "Cheveux et pose inclus"),
        ("Transplas · 2 / 4 tresses", "65 / 100", "Cheveux à acheter sur place"),
    ]),
    "tissage": ("Tissage & extensions", [
        ("Extensions", "135", "Pose d'extensions ou tissage"),
        ("Tissage cousu sur nattes", "dès 135", "Coiffage inclus"),
        ("Extensions longues", "150", "Coiffage inclus"),
    ]),
    "soins": ("Soins, lissage & perruques", [
        ("Défrisage des cheveux", "65", "Défrisage et soin protecteur"),
        ("Brushing", "65", "Brushing simple ou wavy"),
        ("Rénovation de perruque", "110", "Nettoyage, soin, remise en forme"),
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
    ("Mèches & extensions", "Mèches pour tresses, crochets, cheveux naturels."),
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
    ("Les mèches sont-elles comprises ?", "Sur nos modèles à 150 CHF (tresses africaines, bohème), les paquets de mèches sont offerts. Les rasta longues Élégance (135 CHF) et le crochet bouclé (120 CHF) incluent les cheveux. Pour les autres coiffures, les mèches s'achètent sur place et nous vous aidons à choisir la quantité et la couleur."),
    ("Comment choisir mon modèle ?", "Parcourez notre catalogue de codes (1 à 9) ou envoyez-nous une photo sur WhatsApp. Indiquez simplement le code au moment de réserver."),
    ("Faut-il prendre rendez-vous ?", "Oui pour la coiffure : sur Salonkee, sur WhatsApp ou au 078 259 77 38. La boutique est ouverte sans rendez-vous du lundi au samedi."),
    ("Combien de temps dure une pose ?", "Cela dépend du modèle, de la longueur et de l'épaisseur. Envoyez une photo sur WhatsApp, nous vous donnons une estimation avant le rendez-vous."),
    ("Vous coiffez les enfants ?", "Oui : nattes, transplas et tresses se font aussi pour les enfants. Précisez l'âge en réservant."),
    ("Vous rénovez les perruques ?", "Oui, 110 CHF : nettoyage, soin, démêlage, remise en forme, ajustement et finition professionnelle."),
]
