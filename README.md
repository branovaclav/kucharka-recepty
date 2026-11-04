# Rodinná kuchařka — static visual cookbook (SAMPLE)

Private, static HTML cookbook for reading on an iPad while cooking.
No build step, no runtime dependencies (fonts are self-hosted), all paths relative —
works opened as plain files (`file://`) or served from any static host.
Published as a static GitHub Pages site (https://branovaclav.github.io/kucharka-recepty/) so it can be embedded in Notion; still `robots.txt` + `<meta name="robots" content="noindex,nofollow">` on every page.

## Structure

```
cookbook/
├── index.html                 # recipe list (photo cards)
├── robots.txt                 # Disallow: /
├── assets/
│   ├── style.css              # THE shared stylesheet — every page uses only this
│   └── fonts/                 # Fraunces (headings) + Atkinson Hyperlegible (body), woff2, SIL OFL
├── images/                    # <recipe-slug>-hero.jpg, <slug>-krok-N.jpg, <slug>-galerie-N.jpg
├── recipes/
│   └── kureci-rizek.html      # one file per recipe = the template
└── .nojekyll                  # serve files as-is on GitHub Pages
```

## Visual style: "Smalt & puntík"

Czech enamelware kitchen: cream enamel background (`--cream`), cobalt-blue rims and ink
(`--cobalt`), tomato-red accents (`--tomato`), mustard tip labels (`--mustard`), blue/white
polka-dot bands (`.dots`), thick 3 px borders with hard offset shadows (no blur) like a
printed kitchen card. Headings: Fraunces (soft/wonky variable axes); body: Atkinson
Hyperlegible at ~19–23 px, steps ~21–26 px, for reading at arm's length.
All colours/sizes are CSS variables at the top of `style.css` — change them there only.

Layout: single column on phone & iPad portrait (ingredients in 2 columns on portrait);
from 1000 px (iPad landscape) ingredients become a sticky left column next to the steps.

## Adding a recipe

1. Slug: lowercase ASCII with hyphens, e.g. `svickova-na-smetane`.
2. Images → `images/<slug>-hero.jpg` (main photo, ~4:3), optional `images/<slug>-krok-<N>.jpg`.
3. Copy `recipes/kureci-rizek.html` → `recipes/<slug>.html` and replace content only:
   - `<title>`, the `<!-- RECIPE: ... -->` comment, and `data-recipe-id="<slug>"` on `<main>`
     (this keys the localStorage tick-off state, must be unique).
   - Top `.credit` and bottom `.source-foot` links → original recipe URL + author. Always both.
   - `.hero`: photo, `.kicker` (category), `<h1>`, `.lede` (source perex), `.rating` (only if the source has one).
   - `.meta` strip: Čas / Porce / Obtížnost / Spotřebiče (`.chip`). Drop any item the source lacks.
   - Ingredients: one `<li><button aria-pressed="false"><span class="box"></span><span class="text"><span class="qty">…</span> …</span></button></li>` per line. Wrap the quantity in `.qty`.
   - Steps: one `<li class="step">` each; numbering is automatic (CSS counter). Optional `<h3>`,
     optional `<figure class="step-photo">` with a `<figcaption>`, keep the `.step-done` button.
   - Tips: `<aside class="tip">` (mustard label) or `<aside class="tip tip--alt">` (red label) with
     `.tip-label`, `<h3>`, text and a `.tip-source` line. Mark clearly whether a tip comes from a
     source (link it) or was added by us.
   - Leave the inline `<script>` blocks and the `.frame-open` bar untouched — they are generic (ingredient + step ticking in
     localStorage, "Začít znovu" reset, screen wake-lock button where supported; when embedded in an iframe
     such as Notion, an "Otevřít na celou obrazovku" link appears and the wake-lock button is hidden).
4. Content rule: copy the source text exactly (light formatting only). If the source lacks
   something, omit it — never invent.
5. In `index.html` copy the `<!-- CARD -->…<!-- /CARD -->` block, update link/photo/title/facts,
   update the `.count` text, and delete one "Další recept už brzy" placeholder (remove them all
   once there are 3+ recipes).
6. Check it: `./shot.sh file://$PWD/recipes/<slug>.html 820 /tmp/check.png` (also try 1180 and 390).

## Credits

Recipe "Kuřecí řízek" and its photos: Toprecepty.cz (author blazena.blazkova).
Air-fryer variant: Toprecepty.cz, "Jak udělat řízek v horkovzdušné fritéze?" (Kristýna Anna Vondálová).
Fonts: Fraunces, Atkinson Hyperlegible — SIL Open Font License.
