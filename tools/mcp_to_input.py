#!/usr/bin/env python3
"""Turn three Notion SQL exports (Recipes, Ingredients, Appliances — e.g. from the Notion MCP tool
notion-query-data-sources, which is how the assistant reads Notion) into the notion.json that sync.py --input reads.

  python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json

Recipes query:     SELECT url, "Title", "Theme", "Overall", "Braňo", "Zuzka", "Andrej", "Tomáš", "Lukáš", "date:Last prepared:start",
                   "Labels", "Total time", "Difficulty", "Main ingredient", "Appliances", "Ingredients", "Notes", "Page", "Source"
Ingredients query: SELECT url, "Name", "Czech name"      Appliances query: SELECT url, "Name", "Czech name", "Key"
"""
import json, re, sys
def rows(p):
    s = open(p, encoding='utf-8').read(); return json.loads(s[s.index('{'):s.rindex('}') + 1])['results']
def pid(u): return re.search(r'([0-9a-f]{32})', u.replace('-', '')).group(1)
def arr(v): return json.loads(v) if isinstance(v, str) and v.startswith('[') else (v or [])
R, I, A = (rows(p) for p in sys.argv[1:4])
ing = {pid(r['url']): {"name": r['Name'], "czech": r.get('Czech name') or ''} for r in I}
app = {pid(r['url']): {"name": r['Name'], "czech": r.get('Czech name') or '', "key": r.get('Key') or ''} for r in A}
out = []
for r in sorted(R, key=lambda r: pid(r['url'])):
    out.append({"notion_id": pid(r['url']), "notion_url": "https://app.notion.com/p/" + pid(r['url']), "title": r['Title'], "theme": r.get('Theme') or '',
                "overall": r.get('Overall') or '', "ratings": {k: r.get(n) or '' for k, n in
                    (("brano", "Braňo"), ("zuzka", "Zuzka"), ("andrej", "Andrej"), ("tomas", "Tomáš"), ("lukas", "Lukáš"))},
                "last_prepared": r.get('date:Last prepared:start') or '', "labels": arr(r.get('Labels')),
                "total_time": r.get('Total time'), "difficulty": r.get('Difficulty') or '', "main_ingredient": r.get('Main ingredient') or '',
                "appliances": [app[pid(u)] for u in arr(r.get('Appliances')) if pid(u) in app],
                "ingredients": [ing[pid(u)] for u in arr(r.get('Ingredients')) if pid(u) in ing],
                "notes": r.get('Notes') or '', "page_url": r.get('Page') or '', "source": r.get('Source') or ''})
print(json.dumps({"recipes": out}, ensure_ascii=False, indent=1, sort_keys=True))
