# Agent entry point

You are taking over **Rodinná kuchařka**, a family cookbook. It is a static site on GitHub Pages, built by a GitHub Action from Markdown and themes, with an English Notion admin as the source of family data.

**Waterfall:** Notion → `tools/sync.py` (assistant's box) → `data/<slug>.json` → push → Action: `apply_json.py` (json → md front matter) → `build.py` (md + theme → `recipes/*.html`) → `build_index.py` (`index.html`) → one commit `build: json → md → html [skip ci]`.

Read first, in this order:

1. [`docs/AGENT.md`](docs/AGENT.md): the full handover (architecture, Notion schema, sync, adding a recipe, themes, constraints).
2. [`docs/CONTENT-FORMAT.md`](docs/CONTENT-FORMAT.md): the format of `content/<slug>.md`.
3. [`themes/smalt/cookbook.md`](themes/smalt/cookbook.md): the component catalogue plus the official-site O-sections.
4. [`README.md`](README.md): a short overview.

Hard rules:
- Edit `content/*.md` and `themes/`, never the generated HTML.
- Never hand-edit `data/*.json` or the synced front-matter keys; Notion owns them.
- Never rewrite the author's recipe text.
- Do not touch `designs/`.
- Do not push to any other repo.
- Ask before adding appliances beyond the six. The meat probe works only in the oven.
- Keep ratings, last prepared and notes real data only.
- Keep `noindex` and `robots.txt`.
