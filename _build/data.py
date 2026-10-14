# -*- coding: utf-8 -*-
"""Business facts for Mama Africa Beauty, Payerne.
Sources: Salonkee (salon/mamaafrica-brut), Google Maps listing, Instagram @mamaafricabeauty_,
her shop flyers, and the previous mama-africa-beauty.ch site."""

PITCH = True  # lead pitch: keep noindex until she signs
BASE = "https://welcometothenextlevel.github.io/mamaafrica/"
V = "3"  # cache-busting for css/js

NAME = "Mama Africa Beauty"
SHORT = "Mama Africa"
OWNER = "Neneth"
PHONE = "078 259 77 38"
TEL = "+41782597738"
WA = "41782597738"  # assumed to be on WhatsApp (her business chat exists)
STREET = "Rue de Lausanne 38B"
CITY = "1530 Payerne"
REGION = "Vaud"
GEO = (46.8195624, 6.936667)

SALONKEE = "https://salonkee.ch/salon/mamaafrica-brut"
INSTAGRAM = "https://www.instagram.com/mamaafricabeauty_/"
IG_HANDLE = "@mamaafricabeauty_"
PLACE_ID = "ChIJ0cFaUjh3jkcR9RJt4YtSH2Y"
GMAPS = "https://maps.google.com/?cid=7358691076882633461"
G_REVIEWS = f"https://search.google.com/local/reviews?placeid={PLACE_ID}"
G_WRITE = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"
G_RATING = "5,0"
G_COUNT = 1

# Mon=0 … Sun=6 ; IG bio, local.ch, flyer and old site agree on Mon–Sat 9:00–18:30
HOURS = [
    ("Lundi", "09:00", "18:30"),
    ("Mardi", "09:00", "18:30"),
    ("Mercredi", "09:00", "18:30"),
    ("Jeudi", "09:00", "18:30"),
    ("Vendredi", "09:00", "18:30"),
    ("Samedi", "09:00", "18:30"),
    ("Dimanche", None, None),
]

# ---------- braids (Salonkee + flyers) ----------
STYLES = [
    dict(id="box-braids", name="Box braids & knotless", img="braids-portrait", price="95", unit="CHF",
         tag="Le classique", desc="Tresses avec ajout, carrées ou sans nœud, du chignon au bas du dos.",
         long="La tresse avec ajout dans toutes ses versions : box braids, knotless, tresses fines ou épaisses. Les mèches se choisissent au salon, la longueur et la couleur se décident ensemble.",
         note="Prestation « Diverses tresses avec ajout ». Mèches en vente sur place.", cat="tresses"),
    dict(id="boheme", name="Tresses bohème", img="braids-smile", price="150", unit="CHF",
         tag="4 modèles", desc="Tresses fines et mèches bouclées libres pour un effet bohème, léger et lumineux.",
         long="Quatre modèles bohème, du blond miel au brun profond, avec des boucles libérées tout le long des tresses. Un style qui se porte détaché comme en chignon.",
         note="Les mèches s'achètent sur place.", cat="tresses"),
    dict(id="crochet", name="Crochet bouclé", img="crochet-volume", price="120", unit="CHF",
         tag="Cheveux inclus", desc="Bouclé classique, volume, naturel ou tendance. Cheveux et pose compris.",
         long="Quatre bouclés au choix, chacun en quatre coloris : classique (1B, 2, 4, 27), volume (27, 30, 350, 613), naturel (1B/30, T1B/27, T4/30, T350) et tendance (99J, BUG, RED, T1B/BUG). Léger, confortable et prêt pour toutes les occasions.",
         note="Prix tout compris : cheveux et pose.", cat="crochet"),
    dict(id="rasta-longues", name="Rasta longues", img="braids-sitting", price="150", unit="CHF",
         tag="Signature", desc="De longues tresses fines et régulières, posées une à une avec patience.",
         long="Des tresses longues, nettes et régulières, pensées pour durer. Le travail le plus minutieux du salon, et l'un des plus demandés.",
         note="Mèches en vente sur place.", cat="tresses"),
    dict(id="rasta-courtes", name="Rasta courtes", img="braids-brick", price="85", unit="CHF",
         tag="Mi-longues", desc="Le même soin, à hauteur d'épaules : pratique, élégant, vite posé.",
         long="La version courte des rastas : une coupe à hauteur d'épaules ou de menton, facile à vivre au quotidien.",
         note="Mèches en vente sur place.", cat="tresses"),
    dict(id="transplas", name="Transplas", img="transplas-4", price="65", unit="CHF", pre="dès",
         tag="2 ou 4 tresses", desc="Tresses plaquées propres et durables : 2 transplas 65 CHF, 4 transplas 100 CHF.",
         long="Les tresses plaquées façon « boxer braids » : deux transplas à 65 CHF, quatre à 100 CHF. Propre, élégant, durable, et adapté aux enfants comme aux adultes.",
         note="Cheveux à acheter sur place.", cat="tresses"),
    dict(id="nattes", name="Nattes simples", img="cornrows-portrait", price="55", unit="CHF",
         tag="Sans ajout", desc="Nattes collées sur vos cheveux naturels, motifs droits ou dessinés.",
         long="Des nattes collées réalisées avec vos propres cheveux, en lignes droites ou en motifs. Idéal pour protéger la chevelure entre deux coiffures.",
         note="", cat="tresses"),
    dict(id="twists", name="Twists", img="locs-2", price=None, unit="", tag="Sur demande",
         desc="Vanilles et twists avec ou sans ajout, pour un tombé souple et naturel.",
         long="Des twists à deux brins, avec vos cheveux ou avec ajout, pour un rendu souple qui respecte la texture naturelle.",
         note="Tarif selon longueur et volume : demandez sur WhatsApp.", cat="tresses"),
]

CROCHET_MODELS = [
    ("Bouclé classique", "crochet-classique", ["#1a1410", "#3b2516", "#5a3a22", "#b07a3e"], "1B · 2 · 4 · 27"),
    ("Bouclé volume", "crochet-volume", ["#b07a3e", "#8a3e1c", "#9c3a22", "#e8d6a8"], "27 · 30 · 350 · 613"),
    ("Bouclé naturel", "crochet-naturel", ["#2a1a12", "#6b4426", "#5a3a22", "#7a2e20"], "1B/30 · T1B/27 · T4/30 · T350"),
    ("Bouclé tendance", "crochet-tendance", ["#5a1420", "#4a1222", "#9e1c24", "#3a1418"], "99J · BUG · RED · T1B/BUG"),
]

# ---------- full price list (Salonkee categories) ----------
MENU = [
    ("Tresses & coiffures", "Les tresses africaines traditionnelles et modernes, posées au salon sur rendez-vous.", [
        ("Nattes simples", "55", "Sur cheveux naturels, sans ajout"),
        ("Rasta courtes", "85", "Mèches en vente sur place"),
        ("Diverses tresses avec ajout", "95", "Box braids, knotless…"),
        ("Rasta longues", "150", "Mèches en vente sur place"),
        ("Tresses bohème · 4 modèles", "150", "Mèches à acheter sur place"),
        ("Transplas · 2 tresses", "65", "Cheveux à acheter sur place"),
        ("Transplas · 4 tresses", "100", "Cheveux à acheter sur place"),
        ("Crochet bouclé · 4 modèles", "120", "Cheveux et pose inclus"),
    ]),
    ("Extensions & traitements", "Pour gagner en longueur ou transformer la texture.", [
        ("Extensions", "120", "Cheveux naturels disponibles au salon"),
        ("Défrisage des cheveux", "50", ""),
    ]),
    ("Soins capillaires", "Des soins ciblés pour cheveux crépus, bouclés, lisses ou en transition.", [
        ("Bio-plastie capillaire (clinique)", "95", "Sur rendez-vous téléphonique"),
        ("Soin cheveux lisses ou ondulés", "85", ""),
        ("Traitement produits Lowell", "95", ""),
    ]),
    ("Coupes, coiffage & couleur", "", [
        ("Coupe", "45", ""),
        ("Brushing", "65", ""),
        ("Teinture", "55", ""),
    ]),
    ("Beauté du regard & maquillage", "", [
        ("Extension de cils · cil à cil", None, "Sur demande"),
        ("Extension de cils · volume russe", None, "Sur demande"),
        ("Épilation des sourcils", None, "Sur demande"),
        ("Maquillage", None, "Sur demande"),
    ]),
]

SOINS = [
    dict(name="Bio-plastie capillaire", img="hands-scalp", price="95", tag="Clinique",
         desc="Un soin reconstructeur en profondeur pour redonner force, souplesse et brillance aux cheveux fragilisés.",
         note="Réservation par téléphone"),
    dict(name="Traitement Lowell", img="products-terracotta", price="95", tag="Gamme Lowell",
         desc="Le soin aux produits Lowell, la gamme brésilienne que l'on trouve aussi en boutique."),
    dict(name="Soin lisses ou ondulés", img="afro-glam", price="85", tag="Hydratation",
         desc="Nourrir, discipliner, faire briller : un soin pensé pour les cheveux lisses ou ondulés."),
    dict(name="Extensions", img="curls-laugh", price="120", tag="Longueur",
         desc="Des extensions en cheveux naturels de qualité, choisies au salon pour un résultat invisible."),
    dict(name="Défrisage", img="portrait-ochre-2", price="50", tag="Lissage",
         desc="Un défrisage professionnel, appliqué avec méthode pour respecter le cuir chevelu."),
    dict(name="Brushing", img="afro-1", price="65", tag="Coiffage",
         desc="Volume, mouvement ou lissé parfait : le brushing qui sublime votre texture."),
    dict(name="Coupe", img="curls-portrait", price="45", tag="Forme",
         desc="Une coupe qui respecte la boucle et dessine une forme nette, du crépu au lisse."),
    dict(name="Teinture", img="curls-eyes", price="55", tag="Couleur",
         desc="Une couleur uniforme et lumineuse, du naturel au cuivré."),
]

BOUTIQUE_CATS = [
    ("meches", "Mèches & extensions", "Mèches pour tresses, crochets et extensions en cheveux naturels."),
    ("perruques", "Perruques", "Perruques et cheveux, à essayer au salon."),
    ("soins", "Soins capillaires", "Masques, crèmes coiffantes, huiles et shampoings pour cheveux texturés."),
    ("cosmetiques", "Cosmétiques", "Soins du visage et du corps, maquillage."),
    ("accessoires", "Accessoires de beauté", "Peignes, bonnets, foulards, élastiques, bijoux de tresses."),
]
BRANDS = ["Lola Cosmetics", "Salon Line", "Novex", "Mielle", "O Boticário", "Lowell"]

REVIEWS = [
    dict(name="Pierre Fall", meta="Local Guide · Avis Google", initial="P",
         text="Une expérience client des plus riches et un accueil super professionnel. Je vous recommande fortement comme coiffeur et esthétique. Vite, vite, elle vous attend !"),
]
REVIEW_PLACEHOLDERS = 7  # replace with real Google reviews as they come in

FAQ = [
    ("Faut-il prendre rendez-vous ?", "Oui, les coiffures se font sur rendez-vous. Réservez en ligne sur Salonkee, écrivez-nous sur WhatsApp ou appelez le 078 259 77 38. La boutique, elle, est ouverte du lundi au samedi sans rendez-vous."),
    ("Les mèches sont-elles comprises dans le prix ?", "Cela dépend de la coiffure. Pour le crochet bouclé, cheveux et pose sont inclus (120 CHF). Pour les tresses bohème, les rastas et les transplas, les mèches s'achètent sur place, au salon : nous vous aidons à choisir la bonne quantité et la bonne couleur."),
    ("Combien de temps dure une pose de tresses ?", "Tout dépend du modèle, de la longueur et de l'épaisseur des tresses. Dites-nous ce que vous voulez sur WhatsApp, photo à l'appui : nous vous donnons une estimation avant le rendez-vous."),
    ("Je peux venir avec une photo du modèle ?", "Bien sûr. Envoyez-la sur WhatsApp avant votre visite, ou montrez-la au salon : c'est la meilleure façon de partir avec exactement la coiffure dont vous rêviez."),
    ("Vous coiffez les enfants ?", "Oui. Nattes, transplas et tresses se font aussi pour les enfants. Indiquez simplement l'âge lors de la réservation."),
    ("Puis-je acheter mes produits sans rendez-vous ?", "Oui. La boutique (soins capillaires, mèches, perruques, cosmétiques et accessoires) est ouverte du lundi au samedi, de 9h00 à 18h30."),
]
