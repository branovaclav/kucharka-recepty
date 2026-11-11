# Rodinná kuchařka

A private family cookbook. It has **cooking pages on GitHub Pages** for iPad and iPhone (they also embed in Notion), and an
**English Notion admin** for ratings, notes and pantry state.

**Live:** https://branovaclav.github.io/kucharka-recepty/ ·
**Notion:** [Family Cookbook](https://app.notion.com/p/40e3c877b172818686f5d1fe12709436) ·
**Agents:** start at [`AGENTS.md`](AGENTS.md) → [`docs/AGENT.md`](docs/AGENT.md)

## How it works

```
Notion ──sync.py──▶ data/<slug>.json ──▶ GitHub Action on every push:
                                           apply_json.py  json → content/<slug>.md front matter
                                           build.py       md + themes/<id>/ → recipes/<slug>.html
                                           build_index.py → index.html          (one "build:" commit if anything changed)
```

| Path | Role |
|---|---|
| `content/<slug>.md` | **The recipe.** Front matter (metadata) plus the original Czech/Slovak text verbatim, with our tips in marked boxes. [Format](docs/CONTENT-FORMAT.md) |
| `data/<slug>.json` | Notion snapshot written by the sync. Notion wins for those fields. |
| `themes/<id>/` | Presentation: `sesit` (default, „Babiččin sešit“), `smalt`, `len`. Chosen per recipe (`theme:` / Notion Theme). Previews: `/themes/<id>/preview.html` |
| `recipes/`, `index.html` | **Generated.** Do not edit. |
| `tools/` | sync, build steps, photo prep, vocabularies |
| `designs/` | Frozen design proposals A/B/C (kept as Braňo asked) |

Every page is `noindex`, and `robots.txt` disallows all crawlers.

```bash
# sync (the assistant runs this daily ~04:00 Europe/Prague, from a Notion MCP export)
python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json
python3 tools/sync.py --input notion.json
# build locally (the Action does the same)
pip install pyyaml && python3 tools/apply_json.py && python3 tools/build.py && python3 tools/build_index.py
```

**Add a recipe:** write `content/<slug>.md` → `tools/images.py <slug>` → Notion row (Page URL, cover, embed) → sync → push.
The details are in [docs/AGENT.md](docs/AGENT.md#how-to-add-a-recipe-end-to-end).

## Kitchen

The family owns only these appliances: gas stove, air fryer, rice cooker, microwave, oven (grill + steam), the
**meat probe (oven only, because it is wired to the oven)**, a halušky grater (haluškár), a KitchenAid stand mixer with
attachments, a pressure cooker, an immersion blender, an outdoor grill and a contact grill.

## Credits

- Kuřecí řízek: Toprecepty.cz (blazena.blazkova)
- Bryndzové halušky: Varecha.sk (Jana Štrbková / Medové motúzy)
- Špagety carbonara: Toprecepty.cz (Eliza)
- Palačinky: Toprecepty.cz (lnk-lnk; photo ivulinka)
- Fonts (SIL OFL): Fraunces, Atkinson Hyperlegible (smalt); Newsreader, Figtree (len); Caveat, Literata, Courier Prime (sesit)
