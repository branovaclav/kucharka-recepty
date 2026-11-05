# Agent handover — Rodinná kuchařka

Everything a new agent needs with **only this repo + a Notion connector + `gh` as branovaclav**.

## Purpose

A private family cookbook:

- **Reading / cooking view:** standalone static HTML pages in Smalt design A (“Smalt & puntík”), published on GitHub Pages, embeddable in Notion (framing detection + “⤢ Otevřít na celou obrazovku”).
- **Admin / source of truth for family data:** English Notion workspace (ratings, last prepared, notes, labels, time, difficulty, appliances, ingredients, “at home”).
- **Bridge:** deterministic Python sync (`tools/sync.py`) that updates only the family regions on each page and regenerates the index. Recipe *text* (ingredients, steps, tips) is never rewritten by sync — it is the original Czech/Slovak source, kept in `tools/content/*.json` and baked into the HTML by `tools/render.py`.

Live site: https://branovaclav.github.io/kucharka-recepty/  
Repo: https://github.com/branovaclav/kucharka-recepty (`gh` logged in as **branovaclav**).

## Architecture (one picture)

```
Notion (English admin)          tools/content/<slug>.json     tools/style/* + cookbook/
  ratings, time, labels,    +   verbatim CZ/SK recipe text  + Smalt CSS/JS components
  appliances, ingredients       + our tip boxes only
                 \                    |                    /
                  \                   v                   /
                   \            tools/render.py         /
                    \           → recipes/<slug>.html  /
                     \               (full page)      /
                      \                |             /
                       +------→ tools/sync.py ←------+
                                  | updates data-sync regions + recipe-meta
                                  | regenerates index.html from template
                                  v
                     GitHub Pages (branovaclav.github.io/kucharka-recepty)
```

- **Notion** owns mutable family state.
- **Content JSON** owns immutable-ish source text (+ our marked tip boxes).
- **HTML pages** are the cooking UI; sync patches them in place.
- **`designs/`** are frozen visual proposals (A/B/C). Official pages use A only. Never auto-edit `designs/`.

## Live URLs

| What | URL |
|---|---|
| Index | https://branovaclav.github.io/kucharka-recepty/ |
| Kuřecí řízek | …/recipes/kureci-rizek.html |
| Bryndzové halušky | …/recipes/bryndzove-halusky.html |
| Špagety carbonara | …/recipes/spagety-carbonara.html |
| Palačinky | …/recipes/palacinky.html |
| Design previews (frozen) | …/designs/ (A Smalt, B Len, C Sesit) |
| Fonts / thumbs / covers | …/recipes/fonts/*.woff2, …/images/thumbs/<slug>.jpg, …/images/covers/<slug>.jpg |

Every HTML page has `<meta name="robots" content="noindex,nofollow">`. Root `robots.txt` is `Disallow: /`. Keep both.

## Notion URLs (English admin)

| Page / DB | URL / id |
|---|---|
| Top page **Family Cookbook** | https://app.notion.com/p/40e3c877b172818686f5d1fe12709436 |
| **Recipes** database | https://app.notion.com/p/f8d3a6ad1aee4910ac9e467957aa884f · collection `9b68c9d5-1b02-4da1-93e6-2f8f7ca09fec` |
| **Ingredients** database | https://app.notion.com/p/e1f1a5becfd84653a38314ddb4587679 · collection `149886f0-356c-4c6e-9ea9-7dd23726f825` |
| **Appliances** database | https://app.notion.com/p/617f1856c64c4419a602eb73084a0dd6 · collection `989e8ee4-75b8-4a27-ac47-2bc880709ef2` |

The same `app.notion.com/p/…` links work for the owner and for guests once the page/DB is shared with them. The static index links to the Family Cookbook top page as **„Správa v Notion“**.

### Recipes DB — properties

| Property | Type | Notes |
|---|---|---|
| Title | title | Czech recipe name (page H1) |
| Overall, Braňo, Zuzka, Andrej, Tomáš, Lukáš | select | **Loved / OK / Disliked** only. Leave empty until real data exists. |
| Last prepared | date | Empty until cooked. |
| Labels | multi-select | Beginner, Classic, Fried, Kids' favourite candidate, Sweet, Meatless, To try, Slovak, Italian, Quick, Weekend — **no commas in option names**. |
| Total time | number | Minutes. |
| Difficulty | select | Easy / Medium / Hard → Czech Snadné / Střední / Náročné. |
| Main ingredient | select | Poultry · Pork & beef · Minced meat · **Pasta / rice / potatoes** · Fish & seafood · Vegetarian → CSS tint (see cookbook §O3). |
| Appliances | relation → Appliances | Only the six owned appliances. |
| Ingredients | relation → Ingredients | Auto-add new ingredient rows when needed; English Name + Czech name. |
| Notes | rich text | Empty until real notes. |
| Page | url | Live cooking URL `…/recipes/<slug>.html`. |
| Source | url | Original recipe URL. |
| At home count | rollup | From Ingredients.At home. |
| Have at home | formula | `format(prop("At home count")) + " / " + format(length(prop("Ingredients")))` |

Views: **Gallery**, **Under 45 min**, **Table**.

**Manual step (tools cannot set this):** Gallery → Layout → Card preview → **Page cover**.

Each recipe page body should contain only:

```
## 📱 Cooking view
<embed source="https://branovaclav.github.io/kucharka-recepty/recipes/<slug>.html"></embed>
⤢ [Open full screen](https://branovaclav.github.io/kucharka-recepty/recipes/<slug>.html)
```

Plus a cover image pointing at `…/images/covers/<slug>.jpg`.

### Ingredients DB

- **Name** (English title), **Czech name** (what the index filter chips show), **At home** (checkbox — preserve existing ticks), **Category**, kids’ likes (Andrej/Tomáš/Lukáš: Loves/OK/Dislikes), **Recipes** (dual relation).
- Naming choices already made: keep plain flour ≠ semi-coarse flour; pancetta/mangalica bacon → **Bacon**; yolks → **Eggs**; sunflower oil → **Cooking oil**. Prefer reusing rows over duplicates.
- **Auto-add** missing ingredients when creating a recipe; leave **At home** unticked for new ones.

### Appliances DB (exactly six — ask before adding)

| Name | Key | Czech |
|---|---|---|
| Gas stove | gas-stove | Plynový sporák |
| Air fryer | air-fryer | Horkovzdušná fritéza |
| Rice cooker | rice-cooker | Rýžovar |
| Microwave | microwave | Mikrovlnka |
| Oven (grill + steam) | oven | Trouba (gril + pára) |
| Meat probe | meat-probe | Sonda do masa (jen v troubě) |

**Meat probe is wired to the oven and works only there.** Never suggest it for pan, pot, or air fryer. Extra tools (grater, whisk, ladle, pans…) may appear in original recipe text; do **not** add them as Appliances without Braňo's confirmation — report them instead.

## Repo layout

```
index.html                 # GENERATED by sync from tools/index.template.html — edit the template
recipes/<slug>.html        # one cooking page per recipe (inline CSS/JS + base64 photos)
recipes/fonts/*.woff2      # Fraunces + Atkinson (relative url("fonts/…"); index rewrites to recipes/fonts/)
images/thumbs/<slug>.jpg   # index cards 480×360
images/covers/<slug>.jpg   # Notion covers ≤1200
tools/
  content/<slug>.json      # verbatim source text + our tip boxes (input to render)
  content/_make.py         # one-off generator that wrote the four JSONs
  img/                     # source photos as downloaded
  style/                   # fonts.css tints.css icons.css design.css official.css index.css script.js
  index.template.html      # index skeleton (Notion link lives HERE so sync keeps it)
  render.py                # content JSON → page + thumb + cover
  sync.py                  # Notion dump/API → patch pages + rebuild index + commit/push
  mcp_to_input.py          # Notion MCP SQL exports → notion.json for sync --input
cookbook/cookbook.md       # canonical Smalt + official O1–O9 (component truth)
designs/                   # FROZEN A/B/C previews on Pages — do not touch unless asked
docs/AGENT.md              # this file
AGENTS.md                  # short pointer
robots.txt, .nojekyll
```

Working sources for the three design proposals also exist on the agent box at `/workspace/designs/` (smalt, len, sesit + `_src/`). The published copies under `designs/` in the repo are what Pages serves; keep them as they are.

## Curation rules (non-negotiable)

1. Human-written, popular, well-rated **Czech/Slovak** sources only. Beginner- and kid-friendly.
2. Copy **original text verbatim** (ingredients, steps, author tips). No rewriting, no translating Slovak → Czech, no “fixing”.
3. Our additions only in marked boxes: „Náš tip“, „náš doplněk“, sidenote, warning (`cookbook.md` §7.17–7.21 / O2).
4. Credit source + author **top and bottom**; credit photos.
5. Our tips may use only the six appliances; meat probe = oven only.
6. Page weight ~150–300 KB (hero 720 q86, step photos 720 q70). Slightly under 150 KB is OK if the source photo is small.
7. Keep `noindex` + `robots.txt`. This is a private family site on a public host.

## How to add a recipe end-to-end

1. **Pick a source** (Toprecepty, Varecha, …). Save photos into `tools/img/`.
2. **Write** `tools/content/<slug>.json` — see existing files and `cookbook.md` §O8 for fields. Put our tips only in the marked tip structures. Set `tint` from Main ingredient (§O3); document any deliberate deviation (carbonara → pasta-rice).
3. **Render:** `python3 tools/render.py <slug>` → `recipes/<slug>.html`, thumb, cover. Keeps family meta if the page already has a `notion_id`.
4. **Notion row** in Recipes:
   - Fill Title, Total time, Difficulty, Labels, Main ingredient, Source URL, Page URL, cover.
   - Relate Appliances (only from the six) and Ingredients (auto-create missing ingredient pages with English Name + Czech name; At home unticked).
   - Leave Overall / person ratings / Last prepared / Notes **empty**.
   - Body = Cooking view embed + full-screen link (syntax above).
   - Icon optional (🍗 🧀 🍝 🥞 style).
5. **Sync** (below). Confirm live URL 200, no horizontal scroll at 375/393 and iPad 820×1180 / 1180×820.
6. If Gallery cards look wrong: manually set Card preview → Page cover.

## Sync

### Modes

```bash
# A) From a Notion dump (what the assistant does via Notion MCP — no token on the box yet)
python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json
python3 tools/sync.py --input notion.json [--report out.json] [--no-push] [--dry-run]

# B) Direct Notion API (untested by the assistant so far)
NOTION_TOKEN=secret_… NOTION_RECIPES_DB=f8d3a6ad1aee4910ac9e467957aa884f \
  python3 tools/sync.py
```

Options: `--repo PATH` · `--no-push` · `--dry-run` (lists page files that would change, writes nothing) · `--report FILE`.

### What MCP export looks like

Use Notion MCP `notion-query-data-sources` SQL against the three collection:// URLs:

- Recipes: `Title, Overall, Braňo, Zuzka, Andrej, Tomáš, Lukáš, date:Last prepared:start, Labels, Total time, Difficulty, Main ingredient, Appliances, Ingredients, Notes, Page, Source`
- Ingredients: `Name, Czech name` (+ url)
- Appliances: `Name, Czech name, Key` (+ url)

Then `mcp_to_input.py`. A sample dump often lives on the agent box under `/workspace/kucharka-sync/` (not in the repo).

### What sync touches

- `data-sync` regions: `title total_time difficulty labels appliances rating_overall rating_brano|zuzka|andrej|tomas|lukas last_prepared notes`
- `<script type="application/json" id="recipe-meta">` (sort_keys, indent 1, ensure_ascii False, `</` escaped)
- `body` tint from Main ingredient
- Regenerates **`index.html` from `tools/index.template.html`** (so put durable UI like the Notion link in the **template**, not only in the generated file)
- On title-slug rename: new page + redirect stub at old URL (`meta name="kucharka-redirect"`), `git mv` thumbs/covers, report Notion Page/cover URLs to update
- Stages only `recipes/ images/thumbs images/covers index.html`; commits only if staged; pushes with retries
- Idempotent: same input twice → “No changes — nothing committed.”

Recipe body text is **never** modified by sync.

### Daily plan (intended)

Run sync ~**04:00 Europe/Prague** so overnight Notion edits land on Pages before breakfast. Implement as a routine/cron that exports Notion → `sync.py --input`. Until a token is on the box, the assistant (or a routine with Notion MCP) must produce `notion.json`.

### Rating inheritance on the page

Blank person rating → shows Overall with `data-inherited` (dashed rim + „· jako rodina“). Both blank → „Zatím nehodnotil“ (Zuzka: „nehodnotila“). Overall blank → „Zatím nehodnoceno“. Notes blank → „Zatím bez poznámek.“

## Design previews

| Letter | Name | Path |
|---|---|---|
| A | Smalt & puntík (**official**) | `designs/smalt/` + live recipes |
| B | Len | `designs/len/` |
| C | Babiččin sešit | `designs/sesit/` |

Index: https://branovaclav.github.io/kucharka-recepty/designs/  
Braňo chose A for now; keep B/C on Pages as they are. Box sources: `/workspace/designs/`.

## Verification checklist

```bash
# after push
gh api repos/branovaclav/kucharka-recepty/pages/builds/latest --jq '.status,.commit'
curl -sI https://branovaclav.github.io/kucharka-recepty/ | head -1
# recipes, fonts, thumbs, covers, designs/ — expect 200
# Playwright: 375, 393, 820×1180, 1180×820 — no horizontal overflow (see /workspace/official/check.py pattern)
```

GitHub Pages 5xx → retry. Prefer `authorized_by` for pushes when the host requires it.

## What NOT to do

- **Do not** rewrite, translate, or “improve” author recipe text.
- **Do not** invent ratings / last prepared / notes — leave empty until real.
- **Do not** add appliances beyond the six without asking Braňo.
- **Do not** touch `designs/` unless explicitly asked.
- **Do not** push to any other repository (no “kucharka app” repo, no unrelated sites).
- **Do not** remove `noindex` / `robots.txt`.
- **Do not** delete Notion pages/DBs without confirmation; restructure in place.
- **Do not** implement Markdown↔theme content/presentation split until Braňo decides (proposal pending).
- **Do not** edit `index.html` by hand for durable chrome — edit `tools/index.template.html` then run sync (or at least rebuild the index).

## Key file pointers

- Component CSS order on a recipe page: `fonts.css` + `tints.css` + `icons.css` + `design.css` + `official.css` (inlined by render).
- Shared checklist script: `tools/style/script.js` — keys localStorage by `#recipe[data-recipe-id]`; group `<li class="checklist-group">` without a button is safe.
- Redirect stub template is inside `sync.py` (`REDIRECT`).
- Vocabularies (LABELS_CS, APPLIANCES, DIFFICULTY, RATING, MAIN_TINT) live at the top of `sync.py` — keep Notion option names in sync (especially **Pasta / rice / potatoes**, no commas).

## Current recipes (seed)

| Slug | Source | Author | Tint |
|---|---|---|---|
| kureci-rizek | Toprecepty.cz | blazena.blazkova | chicken |
| bryndzove-halusky | Varecha.sk | Jana Štrbková | pasta-rice |
| spagety-carbonara | Toprecepty.cz | Eliza | pasta-rice (bacon is flavouring) |
| palacinky | Toprecepty.cz | lnk-lnk (photo ivulinka) | veg |

When in doubt: read `cookbook/cookbook.md` O-sections, then the matching `@c:…` component, then an existing `tools/content/*.json` + its rendered HTML.
