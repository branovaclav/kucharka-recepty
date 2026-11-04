#!/usr/bin/env python3
"""Rodinná kuchařka — Notion → GitHub Pages sync.

Deterministic and idempotent: running it twice with the same Notion data changes nothing the second time.

  python3 tools/sync.py --input notion.json            # data exported from Notion (e.g. by the assistant via MCP)
  NOTION_TOKEN=... NOTION_RECIPES_DB=... python3 tools/sync.py   # direct Notion API fetch (plain HTTP)

Options: --repo PATH (default: repo root next to this file) · --no-push (write + commit locally) · --dry-run (write nothing)
         --report FILE (write JSON report: changed files + Notion updates needed)

What it touches (and nothing else):
  * the [data-sync="…"] regions, <title>, body[data-tint] and <script id="recipe-meta"> of recipes/<slug>.html
  * renames recipes/<slug>.html (+ images/thumbs, images/covers) when the Notion title's slug changes,
    leaving a small redirect page at the old address, and lists the Notion "Page" / cover updates required
  * regenerates index.html from the recipe-meta blocks of all recipe pages
Recipe text (ingredients, steps, tips) is never touched: it is the original source text, see tools/content/*.json.
"""
import argparse, datetime as dt, html, json, os, re, subprocess, sys, time, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://branovaclav.github.io/kucharka-recepty/'

# ---------- vocabularies (Notion English → page Czech) ----------
LABELS_CS = {"Quick": "Rychlé", "Beginner": "Pro začátečníky", "Kids' favourite candidate": "Tip pro děti", "Sweet": "Sladké",
             "Meatless": "Bez masa", "Weekend": "Na víkend", "To try": "Vyzkoušet", "Classic": "Klasika", "Fried": "Smažené",
             "Slovak": "Slovenské", "Italian": "Italské"}
APPLIANCES = {  # Notion name → (key used for the icon, Czech text)
    "Gas stove": ("gas-stove", "Plynový sporák"), "Air fryer": ("air-fryer", "Horkovzdušná fritéza"),
    "Rice cooker": ("rice-cooker", "Rýžovar"), "Microwave": ("microwave", "Mikrovlnka"),
    "Oven (grill + steam)": ("oven", "Trouba (gril + pára)"), "Meat probe": ("meat-probe", "Sonda do masa (jen v troubě)")}
DIFFICULTY = {"Easy": ("easy", "Snadné"), "Medium": ("medium", "Střední"), "Hard": ("hard", "Náročné")}
RATING = {"Loved": "loved", "OK": "ok", "Disliked": "disliked"}
RATING_CS = {"loved": "Chutná", "ok": "Ujde", "disliked": "Nechutná"}
PEOPLE = [("brano", "Braňo", "Braňo"), ("zuzka", "Zuzka", "Zuzka"), ("andrej", "Andrej", "Andrej"), ("tomas", "Tomáš", "Tomáš"), ("lukas", "Lukáš", "Lukáš")]
MAIN_TINT = {"Poultry": "chicken", "Pork & beef": "pork-beef", "Minced meat": "minced", "Pasta / rice / potatoes": "pasta-rice",
             "Fish & seafood": "fish", "Vegetarian": "veg"}
TINTS = set(MAIN_TINT.values())

def esc(s): return html.escape(s or '', quote=True)

def slugify(title):
    s = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'recept'

def fmt_minutes(m):
    if m in (None, ''): return '—'
    m = int(round(float(m)))
    if m < 60: return f'{m} min'
    h, r = divmod(m, 60)
    return f'{h} h {r} min' if r else f'{h} h'

def fmt_date(iso):
    d = dt.date.fromisoformat(iso[:10]); return f'{d.day}. {d.month}. {d.year}'

# ---------- canonical record (what the page shows) ----------
def normalize(rec):
    """Notion record (export/API shape) → canonical dict used for rendering and for recipe-meta."""
    ratings = {k: RATING.get((rec.get('ratings') or {}).get(k) or '', '') for k, _, _ in PEOPLE}
    apps = []
    for a in rec.get('appliances') or []:
        name = a['name'] if isinstance(a, dict) else a
        key, cs = APPLIANCES.get(name, ((a.get('key') if isinstance(a, dict) else '') or slugify(name), name))
        apps.append({"name": name, "key": key, "cs": cs})
    ingr = []
    for i in rec.get('ingredients') or []:
        if isinstance(i, str): i = {"name": i}
        ingr.append({"name": i['name'], "cs": i.get('czech') or i.get('cs') or i['name']})
    main = rec.get('main_ingredient') or ''
    return {
        "title": (rec.get('title') or '').strip(),
        "notion_id": rec.get('notion_id') or '', "notion_url": rec.get('notion_url') or '',
        "total_time": int(rec['total_time']) if rec.get('total_time') not in (None, '') else None,
        "difficulty": DIFFICULTY.get(rec.get('difficulty') or '', ('', ''))[0],
        "labels": [{"name": l, "cs": LABELS_CS.get(l, l)} for l in (rec.get('labels') or [])],
        "appliances": apps,
        "ingredients": sorted(ingr, key=lambda x: x['name'].lower()),
        "rating_overall": RATING.get(rec.get('overall') or '', ''),
        "ratings": ratings,
        "last_prepared": (rec.get('last_prepared') or '')[:10],
        "notes": (rec.get('notes') or '').strip(),
        "main_ingredient": main, "tint": MAIN_TINT.get(main, ''),
    }

# ---------- region renderers (shared with render.py) ----------
def r_title(m): return f'<h1 data-sync="title">{esc(m["title"])}</h1>'
def r_total_time(m): return f'<span class="v" data-sync="total_time">{fmt_minutes(m["total_time"])}</span>'
def r_difficulty(m):
    v = m['difficulty']; t = {"easy": "Snadné", "medium": "Střední", "hard": "Náročné"}.get(v, '—')
    return (f'<span class="difficulty" data-sync="difficulty" data-value="{v}"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="difficulty-text">{t}</span></span>')
def r_labels(m):
    lis = ''.join(f'\n        <li class="label-chip" data-value="{esc(l["name"])}">{esc(l["cs"])}</li>' for l in m['labels'])
    return f'<ul class="labels" data-sync="labels" aria-label="Štítky">{lis}\n      </ul>'
def r_appliances(m):
    lis = ''.join(f'\n        <li class="appliance" data-value="{esc(a["key"])}">{esc(a["cs"])}</li>' for a in m['appliances'])
    return f'<ul class="appliances" data-sync="appliances">{lis}\n      </ul>'
def r_rating_overall(m):
    v = m['rating_overall']
    return f'<span class="rating" data-sync="rating_overall" data-value="{v}">{RATING_CS.get(v, "Zatím nehodnoceno")}</span>'
def r_person(key, fem):
    def f(m):
        own = m['ratings'].get(key, ''); v = own or m['rating_overall']
        if not v: return f'<span class="rating" data-sync="rating_{key}" data-value="">{"Zatím nehodnotila" if fem else "Zatím nehodnotil"}</span>'
        inh = '' if own else ' data-inherited title="Stejně jako celé rodině"'
        return f'<span class="rating" data-sync="rating_{key}" data-value="{v}"{inh}>{RATING_CS[v]}</span>'
    return f
def r_last_prepared(m):
    d = m['last_prepared']
    if not d: return '<time data-sync="last_prepared">zatím ne</time>'
    return f'<time data-sync="last_prepared" datetime="{d}">{fmt_date(d)}</time>'
def r_notes(m):
    paras = [p.strip() for p in re.split(r'\n\s*\n|\n', m['notes']) if p.strip()]
    inner = ''.join(f'\n          <p>{esc(p)}</p>' for p in paras) or '\n          <p class="notes-empty">Zatím bez poznámek.</p>'
    return f'<div class="notes" data-sync="notes">{inner}\n        </div>'

REGIONS = {"title": r_title, "total_time": r_total_time, "difficulty": r_difficulty, "labels": r_labels, "appliances": r_appliances,
           "rating_overall": r_rating_overall, "last_prepared": r_last_prepared, "notes": r_notes}
for k, _, _n in PEOPLE: REGIONS['rating_' + k] = r_person(k, k == 'zuzka')

# ---------- HTML surgery ----------
def replace_region(doc, key, new):
    m = re.search(r'<([a-z0-9]+)\b[^>]*\bdata-sync="%s"' % re.escape(key), doc)
    if not m: raise ValueError(f'region {key} not found')
    tag, start = m.group(1), m.start()
    tok = re.compile(r'<(/?)%s\b[^>]*>' % tag)
    depth, pos = 0, start
    for t in tok.finditer(doc, start):
        depth += -1 if t.group(1) else 1
        if depth == 0: return doc[:start] + new + doc[t.end():]
    raise ValueError(f'region {key} not closed')

META_RE = re.compile(r'(<script type="application/json" id="recipe-meta">)(.*?)(</script>)', re.S)
def read_meta(doc):
    m = META_RE.search(doc); return json.loads(m.group(2)) if m else None
def meta_json(meta): return '\n' + json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True).replace('</', '<\\/') + '\n  '
def write_meta(doc, meta): return META_RE.sub(lambda m: m.group(1) + meta_json(meta) + m.group(3), doc, count=1)

def apply(doc, canon, page_meta):
    """Return (new_doc, new_meta) with all synced parts updated from the canonical record."""
    for key, fn in REGIONS.items(): doc = replace_region(doc, key, fn(canon))
    doc = re.sub(r'<title>.*?</title>', f'<title>{esc(canon["title"])} · Rodinná kuchařka</title>', doc, count=1, flags=re.S)
    tint = canon['tint'] or page_meta.get('tint') or 'veg'
    doc = re.sub(r'(<body data-tint=")[a-z-]+(")', lambda m: m.group(1) + tint + m.group(2), doc, count=1)
    meta = dict(page_meta)
    for k in ("title", "notion_id", "notion_url", "total_time", "difficulty", "labels", "appliances", "ingredients",
              "rating_overall", "ratings", "last_prepared", "notes", "main_ingredient"):
        meta[k] = canon[k]
    meta['tint'] = tint
    return write_meta(doc, meta), meta

REDIRECT = '''<!doctype html>
<html lang="cs"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="kucharka-redirect" content="{new}">
<meta http-equiv="refresh" content="0; url={new}"><title>Recept se přestěhoval</title></head>
<body><p>Recept se přestěhoval: <a href="{new}">{title}</a></p></body></html>
'''

# ---------- index ----------
def collect(repo):
    out = []
    rd = os.path.join(repo, 'recipes')
    for f in sorted(os.listdir(rd)):
        if not f.endswith('.html'): continue
        doc = open(os.path.join(rd, f), encoding='utf-8').read()
        if 'name="kucharka-redirect"' in doc: continue
        m = read_meta(doc)
        if m: out.append(m)
    return out

def build_index(repo):
    tpl = open(os.path.join(repo, 'tools', 'index.template.html'), encoding='utf-8').read()
    recs = sorted(collect(repo), key=lambda r: r['title'].lower())
    data = [{k: r.get(k) for k in ("slug", "title", "url", "thumb", "total_time", "difficulty", "labels", "appliances",
                                    "ingredients", "rating_overall", "last_prepared", "tint")} for r in recs]
    cards = '\n'.join(card(r) for r in recs)
    css = '\n'.join(open(os.path.join(repo, 'tools', 'style', f), encoding='utf-8').read()
                    for f in ('fonts.css', 'tints.css', 'icons.css', 'index.css')).replace('url("fonts/', 'url("recipes/fonts/')
    return (tpl.replace('{{CSS}}', css).replace('{{CARDS}}', cards).replace('{{COUNT}}', str(len(recs)))
               .replace('{{DATA}}', json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).replace('</', '<\\/')))

def card(r):
    diff = {"easy": "Snadné", "medium": "Střední", "hard": "Náročné"}.get(r.get('difficulty') or '', '—')
    v = r.get('rating_overall') or ''
    return f'''      <li class="rcard" data-slug="{esc(r['slug'])}" data-tint="{esc(r.get('tint') or 'veg')}">
        <a href="{esc(r['url'])}">
          <img src="{esc(r['thumb'])}" alt="" width="480" height="360" loading="lazy">
          <span class="rcard-body">
            <span class="rcard-title">{esc(r['title'])}</span>
            <span class="rcard-facts"><span class="fact-time">{fmt_minutes(r.get('total_time'))}</span><span class="difficulty" data-value="{esc(r.get('difficulty') or '')}"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span><span class="difficulty-text">{diff}</span></span></span>
            <span class="rating" data-value="{v}">{RATING_CS.get(v, 'Zatím nehodnoceno')}</span>
          </span>
        </a>
      </li>'''

# ---------- Notion input ----------
def load_input(path):
    d = json.load(open(path, encoding='utf-8')); return d['recipes'] if isinstance(d, dict) else d

def fetch_notion():  # Direct API mode (plain HTTP). Needs NOTION_TOKEN and NOTION_RECIPES_DB. Not exercised by the assistant's run.
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
            name = next(text(v) for v in pr.values() if v['type'] == 'title')
            out.append({"name": name, "czech": text(pr['Czech name']) if 'Czech name' in pr else '',
                        "key": text(pr['Key']) if 'Key' in pr else ''})
        return out
    recs, cursor = [], None
    while True:
        res = call(f'https://api.notion.com/v1/databases/{db}/query', {"start_cursor": cursor} if cursor else {})
        for pg in res['results']:
            P = pg['properties']; sel = lambda n: (P.get(n, {}).get('select') or {}).get('name', '')
            recs.append({"notion_id": pg['id'].replace('-', ''), "notion_url": pg['url'], "title": text(P['Title']),
                         "overall": sel('Overall'), "ratings": {k: sel(n) for k, n, _ in PEOPLE},
                         "last_prepared": ((P.get('Last prepared') or {}).get('date') or {}).get('start') or '',
                         "labels": [o['name'] for o in P.get('Labels', {}).get('multi_select', [])],
                         "total_time": P.get('Total time', {}).get('number'), "difficulty": sel('Difficulty'),
                         "main_ingredient": sel('Main ingredient'), "appliances": related(P.get('Appliances', {})),
                         "ingredients": related(P.get('Ingredients', {})), "notes": text(P.get('Notes', {})),
                         "page_url": P.get('Page', {}).get('url') or ''})
        if not res.get('has_more'): break
        cursor = res['next_cursor']
    return recs

# ---------- main ----------
def git(repo, *a, check=True): return subprocess.run(['git', '-C', repo, *a], check=check, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input'); ap.add_argument('--repo', default=ROOT); ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--report')
    a = ap.parse_args(); repo = a.repo
    recs = load_input(a.input) if a.input else fetch_notion()
    pages = {}
    for f in sorted(os.listdir(os.path.join(repo, 'recipes'))):
        if f.endswith('.html'):
            doc = open(os.path.join(repo, 'recipes', f), encoding='utf-8').read()
            if 'name="kucharka-redirect"' not in doc and read_meta(doc): pages[f[:-5]] = doc
    writes, moves, updates, warnings, seen = {}, [], [], [], set()
    for rec in sorted(recs, key=lambda r: r.get('notion_id') or r.get('title')):
        canon = normalize(rec)
        slug = next((s for s, d in pages.items() if canon['notion_id'] and read_meta(d).get('notion_id') == canon['notion_id']), None)
        if not slug:
            pu = re.search(r'recipes/([a-z0-9-]+)\.html', rec.get('page_url') or '')
            slug = next((s for s in ([pu.group(1)] if pu else []) + [slugify(canon['title'])] if s in pages), None)
        if not slug:
            warnings.append(f'No page for Notion recipe "{canon["title"]}" — render it first from tools/content/<slug>.json (original text needed).'); continue
        seen.add(slug)
        doc, meta = apply(pages[slug], canon, read_meta(pages[slug]))
        new_slug = slugify(canon['title'])
        if new_slug != slug and new_slug not in pages:
            moves.append((slug, new_slug))
            meta.update(slug=new_slug, url=f'recipes/{new_slug}.html', thumb=f'images/thumbs/{new_slug}.jpg', cover=f'images/covers/{new_slug}.jpg')
            doc = write_meta(doc, meta)
            doc = doc.replace(f'href="{slug}.html"', f'href="{new_slug}.html"')
            writes[f'recipes/{slug}.html'] = REDIRECT.format(new=f'{new_slug}.html', title=esc(canon['title']))
            writes[f'recipes/{new_slug}.html'] = doc; slug = new_slug
        else:
            writes[f'recipes/{slug}.html'] = doc
        want = {"Page": SITE + meta['url'], "cover": SITE + meta['cover']}
        if (rec.get('page_url') or '') != want['Page'] or (rec.get('cover') is not None and rec.get('cover') != want['cover']):
            updates.append({"notion_url": canon['notion_url'], "title": canon['title'], "set": want})
    for s in pages:
        if s not in seen: warnings.append(f'Page recipes/{s}.html has no Notion recipe (left unchanged).')
    changed = []
    if not a.dry_run:
        for old, new in moves:
            for d, ext in (('images/thumbs', 'jpg'), ('images/covers', 'jpg')):
                if os.path.exists(os.path.join(repo, d, f'{old}.{ext}')): git(repo, 'mv', f'{d}/{old}.{ext}', f'{d}/{new}.{ext}')
    for rel, content in writes.items():
        p = os.path.join(repo, rel)
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != content:
            changed.append(rel)
            if not a.dry_run: open(p, 'w', encoding='utf-8').write(content)
    if a.dry_run:  # index from the would-be pages is not computed in dry-run; report the page changes only
        pass
    else:
        idx = build_index(repo); p = os.path.join(repo, 'index.html')
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != idx:
            open(p, 'w', encoding='utf-8').write(idx); changed.append('index.html')
    if not a.dry_run: git(repo, 'add', '-A', '--', 'recipes', 'images/thumbs', 'images/covers', 'index.html')
    staged = [] if a.dry_run else git(repo, 'diff', '--cached', '--name-only').stdout.split()
    pushed = None
    if staged and not a.dry_run:
        ident = [] if git(repo, 'config', 'user.email', check=False).stdout.strip() else \
            ['-c', 'user.name=kucharka-sync', '-c', 'user.email=kucharka-sync@users.noreply.github.com']
        r = git(repo, *ident, 'commit', '-m', f'Sync from Notion ({len(staged)} files)', '-m', '\n'.join(staged), check=False)
        if r.returncode: sys.exit('git commit failed: ' + r.stderr.strip())
        pushed = False
        if not a.no_push:
            for i in range(5):
                r = git(repo, 'push', 'origin', 'HEAD', check=False)
                if r.returncode == 0: pushed = True; break
                time.sleep(5 * (i + 1))
    report = {"changed_files": sorted(set(changed) | set(staged)), "renamed": moves, "committed": bool(staged and not a.dry_run),
              "pushed": pushed, "notion_updates_needed": updates, "warnings": warnings}
    js = json.dumps(report, ensure_ascii=False, indent=1)
    if a.report: open(a.report, 'w', encoding='utf-8').write(js)
    print(js)
    if not staged: print('No changes — nothing committed.', file=sys.stderr)

if __name__ == '__main__': main()
