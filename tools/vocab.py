"""Shared vocabularies: Notion (English) values → page (Czech) text, keys and tints. Single place to edit."""
import re, unicodedata

SITE = 'https://branovaclav.github.io/kucharka-recepty/'
DEFAULT_THEME = 'smalt'
INDEX_THEME = 'smalt'

LABELS_CS = {"Quick": "Rychlé", "Beginner": "Pro začátečníky", "Kids' favourite candidate": "Tip pro děti", "Sweet": "Sladké",
             "Meatless": "Bez masa", "Weekend": "Na víkend", "To try": "Vyzkoušet", "Classic": "Klasika", "Fried": "Smažené",
             "Slovak": "Slovenské", "Italian": "Italské"}
# The six appliances the family owns. Notion name → (icon key, Czech text). Ask Braňo before adding any.
APPLIANCES = {
    "Gas stove": ("gas-stove", "Plynový sporák"), "Air fryer": ("air-fryer", "Horkovzdušná fritéza"),
    "Rice cooker": ("rice-cooker", "Rýžovar"), "Microwave": ("microwave", "Mikrovlnka"),
    "Oven (grill + steam)": ("oven", "Trouba (gril + pára)"),
    "Meat probe": ("meat-probe", "Sonda do masa (jen v troubě)")}  # wired to the oven: oven-only
DIFFICULTY = {"Easy": ("easy", "Snadné"), "Medium": ("medium", "Střední"), "Hard": ("hard", "Náročné")}
RATING = {"Loved": "loved", "OK": "ok", "Disliked": "disliked"}
RATING_CS = {"loved": "Chutná", "ok": "Ujde", "disliked": "Nechutná"}
PEOPLE = [("brano", "Braňo"), ("zuzka", "Zuzka"), ("andrej", "Andrej"), ("tomas", "Tomáš"), ("lukas", "Lukáš")]
FEMININE = {"zuzka"}
MAIN_TINT = {"Poultry": "chicken", "Pork & beef": "pork-beef", "Minced meat": "minced", "Pasta / rice / potatoes": "pasta-rice",
             "Fish & seafood": "fish", "Vegetarian": "veg"}

def slugify(title):
    s = unicodedata.normalize('NFKD', title or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'recept'


def appliance_order(name):
    """Canonical display/storage order of appliances = order of APPLIANCES above; unknown ones last, alphabetically."""
    names = list(APPLIANCES)
    return (names.index(name), '') if name in APPLIANCES else (len(names), name)
