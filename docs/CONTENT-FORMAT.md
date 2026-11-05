# Recipe Markdown format — `content/<slug>.md`

One file per recipe. **The file name is the slug and the page URL** (`recipes/<slug>.html`). Never rename it casually; see
[AGENT.md § Renaming a slug](AGENT.md#renaming-a-slug-manual).
Parser: `tools/recipe_md.py`. It accepts only the constructs below and **fails loudly** on anything it does not know, so
the GitHub Action goes red instead of silently dropping text.

```
---                      ← YAML front matter (metadata)
…
---
<!-- comment -->          ← optional; HTML comments are ignored everywhere
Lede paragraph(s)        ← text before the first "## " = intro under the title (verbatim from the source)
## Suroviny              ← ingredients
## Postup                ← steps
## Tipy                  ← tip boxes
## Zdroj                 ← optional extra lines for the source footer
```

## 1. Front matter

Two kinds of keys. **Synced keys are owned by Notion.** `tools/apply_json.py` overwrites them from `data/<slug>.json` on
every build, so a hand edit to them is lost on the next build. Change them in Notion instead. The other keys belong to the
Markdown, and Notion never touches them.

| key | owner | meaning |
|---|---|---|
| `slug` | md | must equal the file name |
| `title` | **Notion** Title | page `<h1>` and `<title>` |
| `theme` | **Notion** Theme (if set) else md | `smalt` (default) · `len` · `sesit` (`themes/<id>/`) |
| `tint` | derived from `main_ingredient` | `chicken · pork-beef · minced · pasta-rice · fish · veg` |
| `lang` | md | `cs` or `sk` (the source's language; Slovak shows „Porcie“) |
| `total_time` | **Notion** Total time | minutes (int) |
| `difficulty` | **Notion** | `Easy · Medium · Hard` |
| `main_ingredient` | **Notion** | `Poultry · Pork & beef · Minced meat · Pasta / rice / potatoes · Fish & seafood · Vegetarian` |
| `labels` | **Notion** Labels | English option names (Czech display names are in `tools/vocab.py LABELS_CS`) |
| `appliances` | **Notion** Appliances | English names of the owned appliances (`tools/vocab.py APPLIANCES`) |
| `ingredients` | **Notion** Ingredients | `{name: English, cs: Czech}`; drives the index ingredient filter only |
| `ratings` | **Notion** Overall, Braňo, Zuzka, Andrej, Tomáš, Lukáš | `Loved · OK · Disliked · ""` |
| `last_prepared` | **Notion** Last prepared | `YYYY-MM-DD` or `""` |
| `notes` | **Notion** Notes | free text, one paragraph per line |
| `notion_id`, `notion_url`, `page_url` | **Notion** | identity / links |
| `source` | md | `{site, url, title, author, rating, rating_count, photo}`; credited at the top and the bottom of the page |
| `hero` | md | `{image: "img/<file>.jpg", alt}` |
| `servings` | md | `{count, unit}` (both shown verbatim) |
| `time_note` | md | small text under the time, e.g. „15 min příprava + 25 min tepelná úprava“ |
| `ingredients_note` | md | small text after „Suroviny“, e.g. „pro 4 porce“ |

The writer is canonical: double-quoted strings, flow lists, fixed key order (`recipe_md.FRONT_KEYS`). The first
`apply_json.py` run may reformat hand-written YAML. After that it is a no-op.

## 2. Body

Everything in the body is **copied verbatim from the credited source**, except the marked boxes we add ourselves
(`::: our-tip`, `::: note`, `::: warning`). Never rewrite, translate or “fix” the source text.

Inline: `**bold**`, `*italic*`, `[text](https://url)`. Text is HTML-escaped, so raw HTML is not allowed.

### Lede
Paragraph(s) before `## Suroviny`.

### `## Suroviny`
```
- **500 g** kuřecího masa      ← "**qty** text" → quantity column + text
- sůl                          ← no quantity
### Ozdobenie:                 ← group heading inside the checklist (not clickable)
- **100 g** slaniny
```

### `## Postup`
```
### 1. Příprava masa           ← one step; the "1." is stripped (steps are numbered by CSS)
Paragraph text…

![alt text](img/rizek-step1.jpg "caption / photo credit")     ← step photo from content/img/

::: our-tip                    ← „Náš tip“ inline line (ours)
…
:::
::: note                       ← side note „Na okraj · náš doplněk“ (ours)
…
:::
::: warning                    ← „Pozor · náš doplněk“ (ours, safety)
…
:::
```

### `## Tipy`
Only boxes:
```
::: tip Title from the source      ← „Tip ze zdroje“ (author's tip, verbatim)
- **180 °C** teplota               ← fact tiles (bold part = big value)
> big line                         ← optional highlighted line
Paragraphs…
— Zdroj: [Site — page](https://…) (author)     ← line starting with "— " = credit line of the tip
:::

::: our-tip Title                  ← „Náš tip“ box (ours); gets „Doplněno námi — není součástí původního receptu.“
…
:::
```

### `## Zdroj` (optional)
Extra paragraphs appended to the source footer (e.g. a credit for the source of a variant).
The main credit line is generated from `source:` in the front matter.

## 3. Our tips: kitchen rules

Tips we add may use only the family kitchen: gas stove, air fryer, rice cooker, microwave, oven (grill + steam), meat probe, halušky grater, KitchenAid stand mixer (with attachments), pressure cooker, immersion blender.
**The meat probe is wired to the oven and works only for oven cooking.** Never suggest it for a pan, a pot or the air fryer.
Ask Braňo before introducing any other equipment.

## 4. Images

Put the original photo in `content/img/originals/`, then run `python3 tools/images.py <slug>` (needs Pillow; run it locally,
the Action never does). It writes the web-ready `content/img/<file>` (hero ≤720 px q86, step photos ≤720 px q70),
`images/thumbs/<slug>.jpg` (480×360) and `images/covers/<slug>.jpg` (≤1200 px, the Notion cover). Existing outputs are kept
unless you pass `--force`. `build.py` only base64-embeds the prepared bytes, so builds stay deterministic.
