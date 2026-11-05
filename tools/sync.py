#!/usr/bin/env python3
"""Notion → data/<slug>.json (waterfall step 0). Runs OUTSIDE GitHub — on the assistant's box (daily ~04:00 Europe/Prague, or on demand).

  python3 tools/sync.py --input notion.json          # dump made via the Notion MCP connector + tools/mcp_to_input.py
  NOTION_TOKEN=… NOTION_RECIPES_DB=f8d3a6ad1aee4910ac9e467957aa884f python3 tools/sync.py   # direct Notion API

Options: --repo PATH · --no-pull · --no-commit (write files only) · --no-push · --dry-run (print what would change, write nothing) · --report FILE

It ONLY writes data/<slug>.json and pushes at most ONE commit "sync: notion → json". It never touches content/*.md,
recipes/*.html or index.html — the GitHub Action (.github/workflows/build.yml) does json → md → html after the push.
Deterministic: same Notion data → byte-identical JSON → "No changes", no commit.

Slug (= file name = page URL) is stable: an existing data file is matched by notion_id, else by the slug in the Notion
"Page" URL, else a new slug is made from the title. A later title change in Notion changes the page title, NOT the URL.
"""
import argparse, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vocab as V
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT_MSG = 'sync: notion → json'
PEOPLE_NOTION = [("brano", "Braňo"), ("zuzka", "Zuzka"), ("andrej", "Andrej"), ("tomas", "Tomáš"), ("lukas", "Lukáš")]

def record(rec):
    """Notion record (export/API shape) → data JSON (Notion's own English values; Czech rendering happens in build.py)."""
    r = rec.get('ratings') or {}
    tt = rec.get('total_time')
    return {
        "notion_id": (rec.get('notion_id') or '').replace('-', ''), "notion_url": rec.get('notion_url') or '',
        "title": (rec.get('title') or '').strip(), "theme": rec.get('theme') or '',
        "total_time": int(round(float(tt))) if tt not in (None, '') else '',
        "difficulty": rec.get('difficulty') or '', "main_ingredient": rec.get('main_ingredient') or '',
        "labels": list(rec.get('labels') or []),
        "appliances": sorted(((a['name'] if isinstance(a, dict) else a) for a in rec.get('appliances') or []), key=V.appliance_order),
        "ingredients": sorted(({"name": i['name'] if isinstance(i, dict) else i,
                                "cs": (i.get('czech') or i.get('cs') or i['name']) if isinstance(i, dict) else i}
                               for i in rec.get('ingredients') or []), key=lambda x: x['name'].lower()),
        "ratings": {"overall": rec.get('overall') or r.get('overall') or '', **{k: r.get(k) or '' for k, _ in PEOPLE_NOTION}},
        "last_prepared": (rec.get('last_prepared') or '')[:10], "notes": (rec.get('notes') or '').strip(),
        "page_url": rec.get('page_url') or '', "source_url": rec.get('source') or ''}

def dumps(d): return json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + '\n'

def load_input(path):
    d = json.load(open(path, encoding='utf-8')); return d['recipes'] if isinstance(d, dict) else d

def fetch_notion():  # Direct API mode (plain HTTP). Needs NOTION_TOKEN + NOTION_RECIPES_DB. Not yet exercised (no token on the box).
    import urllib.request
    tok, db = os.environ['NOTION_TOKEN'], os.environ['NOTION_RECIPES_DB']
    H = {"Authorization": f"Bearer {tok}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
    def call(url, body=None):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers=H, method='POST' if body is not None else 'GET')
        return json.load(urllib.request.urlopen(req))
    def text(p): return ''.join(t['plain_text'] for t in (p.get('title') or p.get('rich_text') or []))
    cache = {}
    def related(p):
        out = []
        for r in p.get('relation', []):
            if r['id'] not in cache: cache[r['id']] = call(f'https://api.notion.com/v1/pages/{r["id"]}')['properties']
            pr = cache[r['id']]
            out.append({"name": next(text(v) for v in pr.values() if v['type'] == 'title'),
                        "czech": text(pr['Czech name']) if 'Czech name' in pr else ''})
        return out
    recs, cursor = [], None
    while True:
        res = call(f'https://api.notion.com/v1/databases/{db}/query', {"start_cursor": cursor} if cursor else {})
        for pg in res['results']:
            P = pg['properties']; sel = lambda n: (P.get(n, {}).get('select') or {}).get('name', '')
            recs.append({"notion_id": pg['id'].replace('-', ''), "notion_url": 'https://app.notion.com/p/' + pg['id'].replace('-', ''),
                         "title": text(P['Title']), "theme": sel('Theme'), "overall": sel('Overall'),
                         "ratings": {k: sel(n) for k, n in PEOPLE_NOTION},
                         "last_prepared": ((P.get('Last prepared') or {}).get('date') or {}).get('start') or '',
                         "labels": [o['name'] for o in P.get('Labels', {}).get('multi_select', [])],
                         "total_time": P.get('Total time', {}).get('number'), "difficulty": sel('Difficulty'),
                         "main_ingredient": sel('Main ingredient'), "appliances": related(P.get('Appliances', {})),
                         "ingredients": related(P.get('Ingredients', {})), "notes": text(P.get('Notes', {})),
                         "page_url": P.get('Page', {}).get('url') or '', "source": P.get('Source', {}).get('url') or ''})
        if not res.get('has_more'): break
        cursor = res['next_cursor']
    return recs

def git(repo, *a, check=True): return subprocess.run(['git', '-C', repo, *a], check=check, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input'); ap.add_argument('--repo', default=ROOT); ap.add_argument('--report')
    ap.add_argument('--no-pull', action='store_true'); ap.add_argument('--no-push', action='store_true'); ap.add_argument('--no-commit', action='store_true'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(); repo = os.path.abspath(a.repo)
    if not (a.no_pull or a.dry_run):
        r = git(repo, 'pull', '--rebase', '--autostash', '-q', check=False)
        if r.returncode: sys.exit('git pull failed: ' + r.stderr.strip())
    recs = load_input(a.input) if a.input else fetch_notion()
    dd = os.path.join(repo, 'data'); os.makedirs(dd, exist_ok=True)
    existing = {}
    for f in sorted(os.listdir(dd)):
        if f.endswith('.json'): existing[json.load(open(os.path.join(dd, f), encoding='utf-8')).get('notion_id', '')] = f[:-5]
    changed, warnings, seen = [], [], set()
    for rec in sorted(recs, key=lambda r: (r.get('notion_id') or '').replace('-', '')):
        d = record(rec)
        if not d['title']: warnings.append(f'skipped untitled Notion row {d["notion_id"]}'); continue
        m = re.search(r'/recipes/([a-z0-9-]+)\.html', d['page_url'])
        slug = existing.get(d['notion_id']) or (m.group(1) if m else V.slugify(d['title']))
        if slug in seen: warnings.append(f'duplicate slug {slug} — fix the Notion Page URL'); continue
        seen.add(slug)
        if not d['page_url']: warnings.append(f'{slug}: Notion "Page" is empty — set it to {V.SITE}recipes/{slug}.html')
        if not os.path.exists(os.path.join(repo, 'content', slug + '.md')):
            warnings.append(f'{slug}: no content/{slug}.md yet — the page is built once the recipe Markdown exists')
        unknown = [x for x in d['appliances'] if x not in V.APPLIANCES]
        if unknown: warnings.append(f'{slug}: unknown appliances {unknown} — ask Braňo before adding to tools/vocab.py')
        p = os.path.join(dd, slug + '.json'); new = dumps(d)
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != new:
            changed.append(f'data/{slug}.json')
            if not a.dry_run: open(p, 'w', encoding='utf-8').write(new)
    for nid, slug in existing.items():
        if slug not in seen: warnings.append(f'data/{slug}.json has no Notion row any more (left in place; delete by hand if intended)')
    committed = pushed = False
    if changed and not (a.dry_run or a.no_commit):
        git(repo, 'add', '--', *changed)
        ident = [] if git(repo, 'config', 'user.email', check=False).stdout.strip() else \
            ['-c', 'user.name=kucharka-sync', '-c', 'user.email=kucharka-sync@users.noreply.github.com']
        r = git(repo, *ident, 'commit', '-m', COMMIT_MSG, '-m', '\n'.join(changed), check=False)
        if r.returncode: sys.exit('git commit failed: ' + r.stderr.strip())
        committed = True
        if not a.no_push:
            for i in range(5):
                if git(repo, 'push', '-q', check=False).returncode == 0: pushed = True; break
                git(repo, 'pull', '--rebase', '-q', check=False); time.sleep(3 * (i + 1))
    rep = {"changed_files": changed, "committed": committed, "pushed": pushed if committed and not a.no_push else None, "warnings": warnings}
    print('No changes — nothing committed.' if not changed else 'Dry run — would change:' if a.dry_run else
          'Committed: ' + COMMIT_MSG if committed else 'Wrote data files (not committed).')
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    if a.report: open(a.report, 'w', encoding='utf-8').write(json.dumps(rep, ensure_ascii=False, indent=1))

if __name__ == '__main__': main()
