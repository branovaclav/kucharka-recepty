#!/usr/bin/env python3
"""Waterfall step 1: data/<slug>.json (written from Notion by tools/sync.py) → YAML front matter of content/<slug>.md.

  python3 tools/apply_json.py
Notion wins for the SYNCED fields (recipe_md.SYNCED); everything else in the Markdown is left alone.
Empty "theme" in JSON keeps the Markdown's theme. tint is derived from main_ingredient (vocab.MAIN_TINT).
A data file without a matching content/<slug>.md is reported (a human/agent must write the recipe body first).
Front matter is re-emitted in canonical form, so the first run may reformat hand-written YAML; later runs are no-ops.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vocab as V
from recipe_md import split, dump_front, normalize_front, RATING_KEYS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def merge(fm, d):
    fm = dict(fm)
    for k in ("title", "total_time", "difficulty", "main_ingredient", "labels", "appliances", "last_prepared", "notes",
              "notion_id", "notion_url", "page_url"):
        if k in d: fm[k] = d[k]
    if 'ingredients' in d: fm['ingredients'] = sorted(({"name": i['name'], "cs": i.get('cs') or i.get('czech') or i['name']} for i in d['ingredients']), key=lambda x: x['name'].lower())
    if 'ratings' in d: fm['ratings'] = {k: d['ratings'].get(k) or '' for k in RATING_KEYS}
    if d.get('theme'): fm['theme'] = d['theme']
    if fm.get('main_ingredient') in V.MAIN_TINT: fm['tint'] = V.MAIN_TINT[fm['main_ingredient']]
    return normalize_front(fm)

def main():
    changed, warnings = [], []
    dd = os.path.join(ROOT, 'data')
    for f in sorted(os.listdir(dd)) if os.path.isdir(dd) else []:
        if not f.endswith('.json'): continue
        slug = f[:-5]; md = os.path.join(ROOT, 'content', slug + '.md')
        if not os.path.exists(md): warnings.append(f'data/{f} has no content/{slug}.md yet — write the recipe Markdown'); continue
        text = open(md, encoding='utf-8').read(); fm, body = split(text)
        unknown = [a for a in json.load(open(os.path.join(dd, f), encoding='utf-8')).get('appliances', []) if a not in V.APPLIANCES]
        if unknown: warnings.append(f'{slug}: appliances not in vocab.APPLIANCES: {unknown} (ask Braňo before adding)')
        new = dump_front(merge(normalize_front(fm), json.load(open(os.path.join(dd, f), encoding='utf-8')))) + body
        if new != text: open(md, 'w', encoding='utf-8').write(new); changed.append(f'content/{slug}.md')
    for w in warnings: print('warning:', w, file=sys.stderr)
    print(json.dumps({"changed": changed, "warnings": warnings}, ensure_ascii=False)); return changed

if __name__ == '__main__': main()
