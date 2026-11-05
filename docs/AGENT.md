# Agent handover — Rodinná kuchařka

This file has everything a new agent needs, given **only this repo, a Notion connector and `gh` logged in as branovaclav**.
Read it top to bottom once. The Markdown format is in [CONTENT-FORMAT.md](CONTENT-FORMAT.md), and the visual components are in
[`themes/smalt/cookbook.md`](../themes/smalt/cookbook.md).

## Purpose

A private family cookbook (Braňo, Zuzka and the boys Andrej, Tomáš, Lukáš):

- **Cooking view.** Standalone static HTML pages on GitHub Pages, made for iPad and iPhone and embeddable in Notion. Inside a
  Notion frame the page detects it is framed and shows the „⤢ Otevřít na celou obrazovku“ button.
- **Admin, and the source of truth for family data.** An English Notion workspace holds ratings, last prepared, notes,
  labels, time, difficulty, appliances, ingredients, "at home" and theme.
- **Recipe text.** The original Czech/Slovak source text, verbatim, in `content/<slug>.md`, plus clearly marked tips of our own.

Live site: https://branovaclav.github.io/kucharka-recepty/ · Repo: https://github.com/branovaclav/kucharka-recepty

## Architecture: the waterfall

```
 Notion (English admin)                     humans / agents
   │  tools/sync.py  (assistant's box, daily ~04:00 Europe/Prague or on demand)
   ▼                                            │ edit
 data/<slug>.json  ── commit "sync: notion → json" ──┐        content/<slug>.md  (front matter + verbatim body)
                                                      │        themes/<id>/       (CSS, fonts, components)
                                                      ▼                │
                        GitHub Action .github/workflows/build.yml  (every push to main)
                          1. tools/apply_json.py   data/*.json  → front matter of content/*.md   (Notion wins for synced keys)
                          2. tools/build.py        content/*.md + themes/<theme>/ → recipes/<slug>.html, themes/*/preview.html, recipes/fonts/
                          3. tools/build_index.py  front matter → index.html
                          → at most ONE commit "build: json → md → html [skip ci]" (only if something changed)
                          → asks GitHub Pages to rebuild
                                                      ▼
                         GitHub Pages (legacy "deploy from branch": main /)
```

| Layer | Owner | Edited by |
|---|---|---|
| `data/<slug>.json` | **Notion**. `tools/sync.py` writes it and nothing else does. | sync only. Never edit by hand except for a test. |
| `content/<slug>.md` front matter, **synced keys** | Notion, via the JSON | `apply_json.py`. Hand edits are overwritten. |
| `content/<slug>.md` front matter, other keys + body | the Markdown | humans and agents |
| `themes/<id>/` | presentation | humans and agents |
| `recipes/*.html`, `index.html`, `themes/*/preview.html`, `recipes/fonts/` | **generated** | build only. Never hand-edit. |
| `designs/` | frozen design proposals A/B/C | nobody (Braňo asked to keep them as they are) |

Loop guard: the job runs only when `github.actor != 'github-actions[bot]'`, the bot commit carries `[skip ci]`, and pushes
made with `GITHUB_TOKEN` never start workflows anyway. All builds are deterministic: the same input gives the same bytes, so
an unchanged input gives no commit.

## Repo layout

```
.github/workflows/build.yml   the waterfall Action
data/<slug>.json              Notion snapshot per recipe (sync output)
content/<slug>.md             recipe: YAML front matter + verbatim body  (format: docs/CONTENT-FORMAT.md)
content/img/<file>.jpg        web-ready photos embedded by build.py
content/img/originals/        photos as downloaded from the credited source (input of tools/images.py)
themes/
  _shared/                    tints.css icons.css official.css script.js (used by every theme)
  smalt/                      DEFAULT. theme.json fonts.css design.css fonts/ cookbook.md (component catalogue + O-sections)
                              index.css index.template.html (the index is always Smalt; the „Správa v Notion“ link lives here)
  len/  sesit/                alternative themes: theme.json fonts.css design.css fonts/ cookbook.md
  <id>/preview.html           GENERATED: the reference recipe (kureci-rizek) rendered in that theme
recipes/<slug>.html           GENERATED cooking pages (inline CSS/JS, base64 photos)
recipes/fonts/*.woff2         GENERATED copy of every theme's fonts
index.html                    GENERATED recipe list + filters
images/thumbs/<slug>.jpg      index cards 480×360 (tools/images.py)
images/covers/<slug>.jpg      Notion covers ≤1200 px (tools/images.py)
tools/
  vocab.py                    vocabularies: labels CS, the twelve appliances, difficulty, ratings, people, tints, site URL
  recipe_md.py                Markdown + front-matter parser/writer
  apply_json.py  build.py  build_index.py   the three Action steps
  sync.py                     Notion → data/*.json, commit + push
  mcp_to_input.py             Notion MCP SQL exports → notion.json for sync --input
  images.py                   photo preparation (Pillow, run by hand)
designs/                      FROZEN previews A Smalt, B Len, C Sešit (served at /designs/) — do not touch
docs/AGENT.md  docs/CONTENT-FORMAT.md  AGENTS.md  README.md
robots.txt  .nojekyll
assets/, images/kureci-rizek-*.jpg   leftovers of the very first sample, unused; harmless
```

Every HTML page has `<meta name="robots" content="noindex,nofollow">`, and the root `robots.txt` is `Disallow: /`. Keep both.

## Live URLs

| What | URL |
|---|---|
| Index | https://branovaclav.github.io/kucharka-recepty/ |
| Recipes | …/recipes/kureci-rizek.html · bryndzove-halusky.html · spagety-carbonara.html · palacinky.html · hamburger.html |
| Theme previews | …/themes/smalt/preview.html · …/themes/len/preview.html · …/themes/sesit/preview.html |
| Frozen design proposals | …/designs/ (A Smalt, B Len, C Sešit) |
| Assets | …/recipes/fonts/*.woff2 · …/images/thumbs/<slug>.jpg · …/images/covers/<slug>.jpg |

## Notion (English admin)

| Page / DB | URL / id |
|---|---|
| Top page **Family Cookbook** | https://app.notion.com/p/40e3c877b172818686f5d1fe12709436 |
| **Recipes** | https://app.notion.com/p/f8d3a6ad1aee4910ac9e467957aa884f · `collection://9b68c9d5-1b02-4da1-93e6-2f8f7ca09fec` |
| **Ingredients** | https://app.notion.com/p/e1f1a5becfd84653a38314ddb4587679 · `collection://149886f0-356c-4c6e-9ea9-7dd23726f825` |
| **Appliances** | https://app.notion.com/p/617f1856c64c4419a602eb73084a0dd6 · `collection://989e8ee4-75b8-4a27-ac47-2bc880709ef2` |

The same links work for the owner and for guests the pages are shared with. The index links to the top page as „Správa v Notion“.

### Recipes DB properties

| Property | Type | → data/front matter key |
|---|---|---|
| Title | title | `title` (Czech recipe name) |
| Theme | select `smalt · len · sesit` | `theme`. Empty = keep the Markdown value. |
| Overall, Braňo, Zuzka, Andrej, Tomáš, Lukáš | select **Loved / OK / Disliked** | `ratings.*`. Empty until real data. A blank person shows the Overall value as „jako rodina“. |
| Last prepared | date | `last_prepared` (empty until cooked) |
| Labels | multi-select (Beginner, Classic, Fried, Kids' favourite candidate, Sweet, Meatless, To try, Slovak, Italian, Quick, Weekend) | `labels`. **No commas in option names.** A new label needs a Czech name in `vocab.LABELS_CS`. |
| Total time | number (minutes) | `total_time` |
| Difficulty | select Easy / Medium / Hard | `difficulty` → Snadné / Střední / Náročné |
| Main ingredient | select Poultry · Pork & beef · Minced meat · Pasta / rice / potatoes · Fish & seafood · Vegetarian | `main_ingredient` → `tint` |
| Appliances | relation → Appliances | `appliances` (English names) |
| Ingredients | relation → Ingredients | `ingredients` `{name, cs}` (index filter only; the checklist text comes from the Markdown) |
| Notes | text | `notes` (empty until real notes) |
| Page | url | `page_url` = `…/recipes/<slug>.html`. **This fixes the slug for a new row.** |
| Source | url | `source_url` |
| At home count / Have at home | rollup / formula | not synced (pantry helper) |

Views: Gallery, Under 45 min, Table. **A manual step that tools cannot do:** Gallery → Layout → Card preview → **Page cover**.

Each recipe page in Notion has a cover `…/images/covers/<slug>.jpg`, and a body that contains only:
```
## 📱 Cooking view
<embed source="https://branovaclav.github.io/kucharka-recepty/recipes/<slug>.html"></embed>
⤢ [Open full screen](https://branovaclav.github.io/kucharka-recepty/recipes/<slug>.html)
```

### Ingredients DB
Name (English title), Czech name (shown in the index filter), At home (checkbox; keep existing ticks), Category, kids' likes
(Andrej/Tomáš/Lukáš: Loves/OK/Dislikes), Recipes (dual relation). Reuse rows instead of making duplicates. Choices already
made: plain flour ≠ semi-coarse flour; pancetta/mangalica → Bacon; yolks → Eggs; sunflower oil → Cooking oil. When you add a
recipe, create the missing ingredient rows and leave At home unticked.

### Appliances DB: exactly twelve. Ask Braňo before adding any.

| Name | key | Czech |
|---|---|---|
| Gas stove | gas-stove | Plynový sporák |
| Air fryer | air-fryer | Horkovzdušná fritéza |
| Rice cooker | rice-cooker | Rýžovar |
| Microwave | microwave | Mikrovlnka |
| Oven (grill + steam) | oven | Trouba (gril + pára) |
| Meat probe | meat-probe | Sonda do masa (jen v troubě) |
| Halušky grater | halusky-grater | Haluškár |
| KitchenAid stand mixer | kitchenaid | Kuchyňský robot KitchenAid (with interchangeable attachments / nástavce) |
| Pressure cooker | pressure-cooker | Tlakový hrnec |
| Immersion blender | immersion-blender | Ponorný mixer |
| Outdoor grill | outdoor-grill | Vonkajší gril |
| Contact grill | contact-grill | Kontaktný gril (Braňo's "grill" = the contact grill) |

**The meat probe is wired to the oven and works only there.** Never suggest it for a pan, a pot or the air fryer. Other tools
(whisk, ladle, …) may appear in the original text, but they are not Appliances. The mapping and its order live in `tools/vocab.py APPLIANCES`.
To add an appliance (only after Braňo asks): create the Notion row (Name, Czech name, Key), add it to `tools/vocab.py APPLIANCES`,
and add an icon `--i-<key>` plus `.appliance[data-value="<key>"]` in `themes/_shared/icons.css`. An unknown key falls back to the pot icon.
Link a recipe to an appliance only when the recipe text actually uses it (e.g. bryndzové halušky → Halušky grater, „sitko na halušky“).

## Sync: Notion → data/*.json

**Ownership.** The assistant (Grok Bot) runs the sync on its box, through the Notion MCP connector. The box has no Notion
token. Intended schedule: daily ~**04:00 Europe/Prague**, plus on demand after Braňo edits Notion. Nothing on GitHub reads
Notion. The sync touches **only `data/`** and pushes at most one commit, `sync: notion → json`. The Action does the rest.

```bash
# A) MCP mode (what the assistant does). Export the three DBs with notion-query-data-sources, save each result to a file:
#   Recipes:     SELECT url, "Title", "Theme", "Overall", "Braňo", "Zuzka", "Andrej", "Tomáš", "Lukáš", "date:Last prepared:start",
#                "Labels", "Total time", "Difficulty", "Main ingredient", "Appliances", "Ingredients", "Notes", "Page", "Source"
#                FROM "collection://9b68c9d5-1b02-4da1-93e6-2f8f7ca09fec"
#   Ingredients: SELECT url, "Name", "Czech name" FROM "collection://149886f0-356c-4c6e-9ea9-7dd23726f825"
#   Appliances:  SELECT url, "Name", "Czech name", "Key" FROM "collection://989e8ee4-75b8-4a27-ac47-2bc880709ef2"
python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json
python3 tools/sync.py --input notion.json --report last-report.json

# B) Notion API mode (needs an integration token shared with the Recipes DB; never tried yet)
NOTION_TOKEN=secret_… NOTION_RECIPES_DB=f8d3a6ad1aee4910ac9e467957aa884f python3 tools/sync.py
```

Options: `--repo PATH` · `--no-pull` (skip the initial `git pull --rebase --autostash`) · `--no-commit` (write files only) ·
`--no-push` · `--dry-run` (list the files that would change; writes nothing) · `--report FILE`.
Output: "No changes — nothing committed." when Notion is unchanged. Warnings cover a missing Page URL, a data file without
Markdown, appliances that are not among the twelve, and a Notion row that was deleted (its data file is left in place, never auto-deleted).
On the assistant's box, the working copy is `/workspace/kucharka-recepty` and the dumps live in `/workspace/kucharka-sync/`.

Slug matching: an existing data file is matched by `notion_id`, else by the slug in Notion's `Page` URL, else a new slug is
made from the title. A **title change in Notion changes only the displayed title, never the URL.**

## Running the build locally

```bash
pip install pyyaml            # only dependency of the build (images.py additionally needs Pillow)
python3 tools/apply_json.py && python3 tools/build.py && python3 tools/build_index.py
```
Each step prints JSON listing the files it changed. A second run must print empty `changed` lists. Commit the outputs or let
the Action do it; both give identical bytes.

## How to add a recipe end-to-end

1. **Pick a source** that follows the curation rules below. Save its photos to `content/img/originals/`.
2. **Write `content/<slug>.md`.** Copy an existing file. Fill in the non-synced front matter (slug, lang, source, hero,
   servings, time_note, ingredients_note) and paste the source text **verbatim** into the body
   ([CONTENT-FORMAT.md](CONTENT-FORMAT.md)). Our additions go only into `::: our-tip`, `::: note` or `::: warning`.
   You may leave the synced keys empty; they fill in from Notion.
3. **Photos:** `python3 tools/images.py <slug>` → `content/img/…`, thumb, cover.
4. **Notion row** in Recipes: Title, Theme (smalt), Total time, Difficulty, Labels, Main ingredient, Source, and
   **Page = `https://branovaclav.github.io/kucharka-recepty/recipes/<slug>.html`**. Relate Appliances (from the twelve only) and
   Ingredients (create the missing ones). Set the cover to `…/images/covers/<slug>.jpg`. The body is the embed + link above.
   **Leave Overall, the person ratings, Last prepared and Notes empty.**
5. **Data JSON:** run the sync (it creates `data/<slug>.json`). Or commit everything together: run the sync with `--no-commit`,
   then commit md + images + data in one go.
6. **Push.** The Action builds the page and the index. Verify: the live URL returns 200, there is no horizontal scroll at
   375/393 px and iPad 820×1180 / 1180×820, the Notion embed shows the page, and „⤢“ opens it.

## Switching a theme

Set **Theme** on the recipe's Notion row (`smalt`, `len` or `sesit`) and run the sync. Or, if the Notion Theme is empty, set
`theme:` in the Markdown front matter and push. The Notion value wins when it is set. Compare the themes first at
`…/themes/<id>/preview.html`. Braňo chose **smalt** as the official look, and the index always uses smalt (`vocab.INDEX_THEME`).

To **add a theme**, create `themes/<id>/` with `theme.json`
(`{"name","letter","theme_color","css":["fonts.css","design.css"],"fonts":[…],"status"}`), `fonts.css` (`url("fonts/…")`),
`design.css` and `fonts/`. Font file names must be unique across themes, because they all land in `recipes/fonts/`. Every
theme styles the same markup. The components are listed in `themes/smalt/cookbook.md` §7 and the O-sections. CSS order on a
page: theme fonts.css → `_shared/tints.css` → `_shared/icons.css` → theme design.css → `_shared/official.css`. If you add an
option to the Notion Theme select, you need the matching folder.

## Renaming a slug (manual)

Slugs are stable on purpose: Notion embeds, covers and bookmarks point at them. If a rename is really needed:
`git mv content/<old>.md content/<new>.md` (and change `slug:` inside), `git mv data/<old>.json data/<new>.json`, and do the
same for thumbs and covers. Update the Notion `Page`, the embed, the link and the cover URL. Delete `recipes/<old>.html` or
replace it with a meta-refresh stub. Push.

## Own recipes („Náš recept“)

Family recipes of our own (first: **hamburger**, Braňo's) are flagged `own: true` in the Markdown front matter. The flag is
**Markdown-only** (not a Notion field, the sync never touches it). Effect, in every theme (`smalt`, `len`, `sesit`): the
„Náš recept“ badge `@c:own-badge` in the hero, in the footer and on the index card; the top credit reads „náš rodinný recept ·
<author>“; no source-rating line; `Náš tip` boxes lose the „není součástí původního receptu“ line. Rules:
- Write own recipes in **Slovak** (`lang: "sk"`), cleanly, as the author. The verbatim rule does not apply.
- Credit the photo in `## Zdroj` with a link and licence (free photo, e.g. Unsplash License).
- Times we add are marked as approximate („orientačné“). Minced meat for kids: well done (a `::: warning`).
- Ratings only as Braňo reports them (the hamburger ratings came from him).
Format details: [CONTENT-FORMAT.md § 2a](CONTENT-FORMAT.md#2a-own-recipes-own-true).

## Curation rules (non-negotiable)

1. Use only human-written, popular, well-rated **Czech/Slovak** sources that suit beginners and kids. (Exception: our own recipes, below.)
2. Copy the **original text verbatim**: ingredients, steps and the author's tips. No rewriting, no translating Slovak, no "fixing".
3. Put our additions only in the marked boxes (Náš tip / náš doplněk / Na okraj / Pozor).
4. Credit the source and author **at the top and the bottom** of the page, and credit the photos.
5. Our tips may use only the twelve appliances. The meat probe is oven-only.
6. Keep the page weight around 150–300 KB (hero 720 px q86, step photos 720 px q70).
7. Keep `noindex` and `robots.txt`. This is a private family site on a public host.
8. Ratings, last prepared and notes hold **real data only**. Never invent them.

## GitHub settings

- Pages: **Deploy from a branch → main / (root)**.
- The workflow sets its own `permissions: contents: write, pages: write`, so the repo default "read" is fine. If the build
  step's push ever fails with 403, set Settings → Actions → General → Workflow permissions → **Read and write permissions**.
- `gh` on the assistant's box is logged in as branovaclav, with the `repo` and `workflow` scopes.

## Verification checklist

```bash
gh run list --workflow build.yml -L 3          # last runs: expect "completed success"
gh api repos/branovaclav/kucharka-recepty/pages/builds/latest --jq '.status,.commit'
for u in "" recipes/kureci-rizek.html themes/len/preview.html designs/ recipes/fonts/fraunces.woff2 images/thumbs/palacinky.jpg; do
  curl -s -o /dev/null -w "%{http_code} $u\n" "https://branovaclav.github.io/kucharka-recepty/$u"; done
```
Use Playwright for layout: no horizontal overflow at 375, 393, 820×1180 and 1180×820, and no JS errors. GitHub 5xx → retry.

## What NOT to do

- Do not rewrite, translate or “improve” author text.
- Do not invent ratings, last prepared or notes.
- Do not add appliances beyond the twelve without asking Braňo.
- Do not hand-edit generated files (`recipes/*.html`, `index.html`, `themes/*/preview.html`) or the synced front-matter keys.
- Do not touch `designs/`.
- Do not push to any other repository.
- Do not delete Notion pages or DBs without confirmation; restructure them in place.
- Do not remove `noindex` or `robots.txt`.

## Current recipes

| Slug | Source | Author | Tint | Theme |
|---|---|---|---|---|
| kureci-rizek | Toprecepty.cz | blazena.blazkova | chicken | smalt |
| bryndzove-halusky | Varecha.sk (sk) | Jana Štrbková | pasta-rice | smalt |
| spagety-carbonara | Toprecepty.cz | Eliza | pasta-rice (the bacon is a flavouring) | smalt |
| palacinky | Toprecepty.cz | lnk-lnk (photo ivulinka) | veg | smalt |
| hamburger | **own recipe** (`own: true`, sk) | Braňo (photo Stanley Kustamin / Unsplash) | minced | smalt |
