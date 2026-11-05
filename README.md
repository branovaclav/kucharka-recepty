# Rodinná kuchařka

Private family cookbook: **standalone Smalt HTML** on GitHub Pages for cooking on iPad/iPhone, plus an **English Notion admin** for ratings, notes, and pantry state. A small Python sync keeps the two in step.

**Live:** https://branovaclav.github.io/kucharka-recepty/  
**Notion admin:** [Family Cookbook](https://app.notion.com/p/40e3c877b172818686f5d1fe12709436) (same link for owner and shared guests)  
**Agents taking over:** start at [`AGENTS.md`](AGENTS.md) → [`docs/AGENT.md`](docs/AGENT.md). Visual components: [`cookbook/cookbook.md`](cookbook/cookbook.md).

## What’s here

| Path | Role |
|---|---|
| `index.html` | Recipe list + filters (**generated** from `tools/index.template.html`) |
| `recipes/<slug>.html` | One cooking page per recipe (inline CSS/JS, base64 photos) |
| `recipes/fonts/` | Shared Fraunces + Atkinson Hyperlegible |
| `images/thumbs/`, `images/covers/` | Index cards and Notion covers |
| `tools/` | Content JSON, render, sync, Smalt CSS/JS |
| `cookbook/cookbook.md` | Canonical Smalt catalogue + official-site rules |
| `designs/` | Frozen design previews A (Smalt, official), B (Len), C (Sesit) — do not edit unless asked |
| `docs/AGENT.md` | Full agent handover |

Every page is `noindex`; `robots.txt` disallows all crawlers. Relative paths — works from Pages and from Notion embeds.

## Architecture (short)

1. **Content** — human Czech/Slovak recipe text, copied **verbatim** into `tools/content/<slug>.json`. Our tips only in marked boxes.
2. **Presentation** — Smalt components (`tools/style/*`, documented in `cookbook/`). `tools/render.py` builds the HTML page + thumb + cover.
3. **Family data** — Notion Recipes / Ingredients / Appliances DBs (English UI). Ratings use Loved / OK / Disliked; leave blank until real.
4. **Sync** — `tools/sync.py` patches only `data-sync` regions + `recipe-meta`, regenerates the index, commits/pushes when something changed. Idempotent.

```bash
python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json
python3 tools/sync.py --input notion.json          # or NOTION_TOKEN=… NOTION_RECIPES_DB=f8d3a6ad1aee4910ac9e467957aa884f
```

## Kitchen

Owned appliances only: gas stove, air fryer, rice cooker, microwave, oven (grill + steam), **meat probe (oven-only — wired to the oven)**. Ask before adding more.

## Adding a recipe

See [`docs/AGENT.md`](docs/AGENT.md#how-to-add-a-recipe-end-to-end). In one line: pick a CZ/SK source → write content JSON (verbatim) → `render.py` → Notion row with embed + cover → `sync.py` → verify on phone/iPad.

## Credits

- Kuřecí řízek — Toprecepty.cz (blazena.blazkova)
- Bryndzové halušky — Varecha.sk (Jana Štrbková / Medové motúzy)
- Špagety carbonara — Toprecepty.cz (Eliza)
- Palačinky — Toprecepty.cz (lnk-lnk; photo ivulinka)
- Fonts: Fraunces, Atkinson Hyperlegible (SIL OFL)
