#!/usr/bin/env python3
"""Waterfall step 2: content/<slug>.md + themes/<theme>/ → recipes/<slug>.html (+ theme previews).

  python3 tools/build.py [slug ...]

* Theme = front matter `theme:` (default smalt). Each theme supplies CSS + fonts (themes/<id>/theme.json);
  the markup is shared, components are documented in themes/smalt/cookbook.md.
* Pages are standalone: all CSS/JS inline, photos base64 from content/img/<file>; fonts relative (recipes/fonts/).
* Also writes themes/<id>/preview.html for every theme (the first recipe rendered in that theme).
* Pure text processing (needs only PyYAML) → deterministic: same input, same bytes. Writes only files that changed.
"""
import base64, datetime as dt, html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vocab as V
from recipe_md import split, normalize_front, parse_body, inline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TH = os.path.join(ROOT, 'themes')
PREVIEW_SLUG = 'kureci-rizek'

def esc(s): return html.escape('' if s is None else str(s), quote=True)
def rd(*p): return open(os.path.join(*p), encoding='utf-8').read()
def themes(): return sorted(d for d in os.listdir(TH) if os.path.isfile(os.path.join(TH, d, 'theme.json')))
def theme_meta(t): return json.load(open(os.path.join(TH, t, 'theme.json'), encoding='utf-8'))
def theme_css(t):
    m = theme_meta(t)
    parts = [rd(TH, t, m['css'][0]), rd(TH, '_shared', 'tints.css'), rd(TH, '_shared', 'icons.css')] + \
            [rd(TH, t, f) for f in m['css'][1:]] + [rd(TH, '_shared', 'official.css')]
    return '\n'.join(parts)
def datauri(path): return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
def jpeg_size(path):
    b = open(path, 'rb').read(); i = 2
    while i < len(b):
        if b[i] != 0xFF: i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2): return int.from_bytes(b[i + 7:i + 9], 'big'), int.from_bytes(b[i + 5:i + 7], 'big')
        i += 2 + int.from_bytes(b[i + 2:i + 4], 'big')
    return 0, 0

def fmt_minutes(m):
    if m in (None, ''): return '—'
    m = int(m)
    if m < 60: return f'{m} min'
    h, r = divmod(m, 60); return f'{h} h {r} min' if r else f'{h} h'
def fmt_date(iso): d = dt.date.fromisoformat(iso[:10]); return f'{d.day}. {d.month}. {d.year}'

# ---------- canonical view of the front matter (what the page and the index show) ----------
def canon(fm):
    apps = []
    for a in sorted(fm['appliances'], key=V.appliance_order):
        key, cs = V.APPLIANCES.get(a, (V.slugify(a), a)); apps.append({"name": a, "key": key, "cs": cs})
    r = fm['ratings']
    return {"slug": fm['slug'], "recipe_id": fm['slug'], "title": fm['title'], "theme": fm.get('theme') or V.DEFAULT_THEME,
            "tint": fm.get('tint') or V.MAIN_TINT.get(fm['main_ingredient'], 'veg'),
            "url": f"recipes/{fm['slug']}.html", "thumb": f"images/thumbs/{fm['slug']}.jpg", "cover": f"images/covers/{fm['slug']}.jpg",
            "total_time": fm['total_time'] if fm['total_time'] != '' else None,
            "difficulty": V.DIFFICULTY.get(fm['difficulty'], ('', ''))[0],
            "labels": [{"name": l, "cs": V.LABELS_CS.get(l, l)} for l in fm['labels']],
            "appliances": apps, "ingredients": sorted(fm['ingredients'], key=lambda x: x['name'].lower()),
            "rating_overall": V.RATING.get(r['overall'], ''), "ratings": {k: V.RATING.get(r[k], '') for k, _ in V.PEOPLE},
            "last_prepared": fm['last_prepared'], "notes": (fm['notes'] or '').strip(), "main_ingredient": fm['main_ingredient'],
            "notion_id": fm['notion_id'], "notion_url": fm['notion_url'], "lang": fm.get('lang', 'cs'),
            "source": {k: (fm.get('source') or {}).get(k, '') for k in ('site', 'url', 'title', 'author')}}

# ---------- family regions (data-sync attributes kept as stable hooks) ----------
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
def r_overall(m):
    v = m['rating_overall']
    return f'<span class="rating" data-sync="rating_overall" data-value="{v}">{V.RATING_CS.get(v, "Zatím nehodnoceno")}</span>'
def r_person(m, key):
    own = m['ratings'].get(key, ''); v = own or m['rating_overall']
    if not v: return f'<span class="rating" data-sync="rating_{key}" data-value="">{"Zatím nehodnotila" if key in V.FEMININE else "Zatím nehodnotil"}</span>'
    inh = '' if own else ' data-inherited title="Stejně jako celé rodině"'
    return f'<span class="rating" data-sync="rating_{key}" data-value="{v}"{inh}>{V.RATING_CS[v]}</span>'
def r_last(m):
    d = m['last_prepared']
    return f'<time data-sync="last_prepared" datetime="{d}">{fmt_date(d)}</time>' if d else '<time data-sync="last_prepared">zatím ne</time>'
def r_notes(m):
    paras = [p.strip() for p in re.split(r'\n', m['notes']) if p.strip()]
    inner = ''.join(f'\n          <p>{esc(p)}</p>' for p in paras) or '\n          <p class="notes-empty">Zatím bez poznámek.</p>'
    return f'<div class="notes" data-sync="notes">{inner}\n        </div>'

# ---------- recipe body components ----------
def ingredient(i):
    if 'group' in i: return f'          <li class="checklist-group"><span>{esc(i["group"])}</span></li>'
    q = f'<span class="qty">{inline(i["qty"])}</span> ' if i['qty'] else ''
    return f'          <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">{q}{inline(i["text"])}</span></button></li>'

def step(s):
    out = ['        <li class="step"><div class="step-body">']
    if s['h']: out.append(f'          <h3>{esc(s["h"])}</h3>')
    for it in s['items']:
        k = it[0]
        if k == 'p': out.append(f'          <p>{inline(it[1])}</p>')
        elif k == 'img':
            path = os.path.join(ROOT, 'content', it[2]); w, h = jpeg_size(path)
            out.append(f'          <figure class="step-photo">\n            <img src="{datauri(path)}" alt="{esc(it[1])}" loading="lazy" width="{w}" height="{h}">\n'
                       f'            <figcaption>{esc(it[3])}</figcaption>\n          </figure>')
        elif k == 'our-inline':
            out.append(f'          <!-- @c:our-inline -->\n          <p class="our-inline" lang="cs"><span class="our-mark">Náš tip</span> {" ".join(inline(p) for p in it[1])}</p>\n          <!-- /@c:our-inline -->')
        elif k == 'sidenote':
            ps = ''.join(f'\n            <p>{inline(p)}</p>' for p in it[1])
            out.append(f'          <!-- @c:sidenote -->\n          <aside class="sidenote" data-origin="ours" lang="cs">\n            <span class="sidenote-label">Na okraj · náš doplněk</span>{ps}\n          </aside>\n          <!-- /@c:sidenote -->')
        elif k == 'warning':
            ps = ''.join(f'\n            <p>{inline(p)}</p>' for p in it[1])
            out.append(f'          <!-- @c:warning -->\n          <div class="warning" role="note" lang="cs">\n            <span class="warning-label">Pozor · náš doplněk</span>{ps}\n          </div>\n          <!-- /@c:warning -->')
    out.append('          <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>\n        </div></li>')
    return '\n'.join(out)

def tip(t, L):
    facts = ''.join(f'<span class="fact"><b>{inline(a)}</b>{inline(b)}</span>' for a, b in t['facts'])
    facts = f'\n      <div class="facts">{facts}</div>' if facts else ''
    ps = ''.join(f'\n      <p>{inline(p)}</p>' for p in t['p'])
    big = f'\n      <p class="big">{inline(t["big"])}</p>' if t['big'] else ''
    if t['kind'] == 'source':
        return (f'    <!-- @c:tip-source -->\n    <aside class="tip tip--source" lang="{L}">\n      <span class="tip-label" lang="cs">Tip ze zdroje</span>\n'
                f'      <h3 lang="cs">{esc(t["h"])}</h3>{big}{facts}{ps}\n      <p class="tip-source" lang="cs">{inline(t["source"])}</p>\n    </aside>\n    <!-- /@c:tip-source -->')
    return (f'    <!-- @c:tip-ours -->\n    <aside class="tip tip--ours" lang="cs">\n      <span class="tip-label">Náš tip</span>\n      <h3>{esc(t["h"])}</h3>{big}{facts}{ps}\n'
            f'      <p class="tip-source">Doplněno námi — není součástí původního receptu.</p>\n    </aside>\n    <!-- /@c:tip-ours -->')

def meta_json(meta): return '\n' + json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True).replace('</', '<\\/') + '\n  '

def load(slug):
    fm, body = split(rd(ROOT, 'content', slug + '.md'))
    fm = normalize_front(fm)
    if fm.get('slug') != slug: raise ValueError(f'content/{slug}.md: front matter slug "{fm.get("slug")}" must equal the file name')
    return fm, parse_body(body)

def page(slug, theme=None, self_href=None):
    fm, B = load(slug); m = canon(fm); t = theme or m['theme']; tm = theme_meta(t)
    src = fm['source']; L = m['lang']
    hero = os.path.join(ROOT, 'content', fm['hero']['image']); hw, hh = jpeg_size(hero)
    rating = (f'\n        <p class="src-rating"><span class="stars" aria-hidden="true">★★★★★</span> {esc(src["rating"])} <small>({esc(src["rating_count"])}× hodnoceno na {esc(src["site"])})</small></p>'
              if src.get('rating') else f'\n        <p class="src-rating"><small>Recept z {esc(src["site"])} — bez hodnocení čtenářů</small></p>')
    people = '\n'.join(f'          <li><span class="who">{n}</span>{r_person(m, k)}</li>' for k, n in V.PEOPLE)
    credit = f'<a href="{esc(src["url"])}" rel="noopener">{esc(src["site"])} — {esc(src["title"])}</a> · autor {esc(src["author"])}'
    foot_extra = ''.join(f'\n    <p>{inline(x)}</p>' for x in B['foot'])
    lede = '\n      '.join(f'<p class="lede" lang="{L}">{inline(p)}</p>' for p in B['lede'])
    sv = fm.get('servings') or {}
    serv_k = 'Porcie' if L == 'sk' else 'Porce'
    serv = (f'\n    <li><span class="k">{serv_k}</span><span class="v">{esc(sv.get("count"))}</span><span class="sub" lang="{L}">{esc(sv.get("unit"))}</span></li>'
            if sv.get('count') else '')
    ingr = '\n'.join(ingredient(i) for i in B['ingredients'])
    steps = '\n'.join(step(s) for s in B['steps'])
    tips = '\n'.join(tip(x, L) for x in B['tips'])
    href = self_href or f'{slug}.html'
    back = '../index.html' if not theme else '../../index.html'
    body = f'''<!-- @c:frame -->
<div class="frame-open" role="region" aria-label="Vložená stránka">
  <a class="btn-fullscreen" href="{href}" target="_blank" rel="noopener" data-fullscreen-link>⤢ Otevřít na celou obrazovku</a>
</div>
<!-- /@c:frame -->
<!-- @c:topbar -->
<header class="topbar">
  <div class="wrap">
    <a class="backlink" href="{back}">Všechny recepty</a>
    <p class="credit">Zdroj: {credit}</p>
  </div>
</header>
<!-- /@c:topbar -->

<main class="wrap" id="recipe" data-recipe-id="{esc(slug)}">
  <!-- @c:hero -->
  <section class="hero">
    <figure class="hero-photo">
      <img src="{datauri(hero)}" alt="{esc(fm['hero'].get('alt'))}" width="{hw}" height="{hh}">
    </figure>
    <div class="hero-text">
      <!-- @c:labels -->
      {r_labels(m)}
      <!-- /@c:labels -->
      <h1 data-sync="title">{esc(m['title'])}</h1>
      {lede}
      <div class="hero-ratings">
        <p class="overall"><span class="overall-k">Rodina</span> {r_overall(m)}</p>{rating}
      </div>
    </div>
  </section>
  <!-- /@c:hero -->

  <!-- @c:meta -->
  <ul class="meta" aria-label="Základní údaje">
    <li><span class="k">Čas</span><span class="v" data-sync="total_time">{fmt_minutes(m['total_time'])}</span><span class="sub" lang="{L}">{esc(fm.get('time_note'))}</span></li>{serv}
    <li><span class="k">Obtížnost</span>
      <!-- @c:difficulty -->
      {r_difficulty(m)}
      <!-- /@c:difficulty -->
    </li>
    <li class="meta-appliances"><span class="k">Spotřebiče</span>
      <!-- @c:appliances -->
      {r_appliances(m)}
      <!-- /@c:appliances -->
    </li>
  </ul>
  <!-- /@c:meta -->

  <!-- @c:family -->
  <section class="family" aria-labelledby="h-family">
    <h2 class="section-title" id="h-family">U nás doma</h2>
    <div class="family-grid">
      <!-- @c:ratings -->
      <div class="card ratings-card">
        <h3 class="card-title">Jak komu chutná</h3>
        <ul class="ratings">
{people}
        </ul>
        <p class="last-prepared">Naposledy vařeno {r_last(m)}</p>
      </div>
      <!-- /@c:ratings -->
      <!-- @c:notes -->
      <div class="card notes-card">
        <h3 class="card-title">Poznámky</h3>
        {r_notes(m)}
      </div>
      <!-- /@c:notes -->
    </div>
  </section>
  <!-- /@c:family -->

  <div class="cook">
    <!-- @c:ingredients -->
    <section class="ingredients" aria-labelledby="h-ingr">
      <h2 class="section-title" id="h-ingr">Suroviny <small lang="{L}">{esc(fm.get('ingredients_note'))}</small></h2>
      <div class="card">
        <ul class="checklist" data-checklist lang="{L}">
{ingr}
        </ul>
        <div class="list-tools">
          <span>Ťukněte na surovinu, kterou máte připravenou.</span>
          <button type="button" class="btn" data-reset>Odškrtnout vše</button>
        </div>
      </div>
    </section>
    <!-- /@c:ingredients -->

    <!-- @c:steps -->
    <section class="method" aria-labelledby="h-steps">
      <h2 class="section-title" id="h-steps">Postup přípravy</h2>
      <ol class="steps" data-steps lang="{L}">
{steps}
      </ol>
    </section>
    <!-- /@c:steps -->
  </div>

  <section class="tips" aria-label="Tipy">
{tips}
  </section>

  <!-- @c:toolbar -->
  <div class="toolbar">
    <button type="button" class="btn" data-wakelock hidden aria-pressed="false">☀ Nezhasínat displej</button>
    <button type="button" class="btn" data-reset-all>↺ Začít znovu</button>
  </div>
  <!-- /@c:toolbar -->
</main>

<!-- @c:source-foot -->
<footer class="source-foot">
  <div class="wrap">
    <p><strong>Zdroj receptu:</strong> <a href="{esc(src['url'])}" rel="noopener">{esc(src['title'])} na {esc(src['site'])}</a> (autor {esc(src['author'])}). {esc(src.get('photo'))}</p>{foot_extra}
    <p class="foot-ours">Části označené <b>Náš tip</b> / <b>náš doplněk</b> jsme doplnili sami, v původním receptu nejsou. Text receptu je převzatý beze změn.</p>
    <p><a class="foot-back" href="{back}">← Zpět na všechny recepty</a></p>
  </div>
</footer>
<!-- /@c:source-foot -->'''
    body = '\n'.join('  ' + l if l.strip() else '' for l in body.splitlines())
    meta = dict(m, theme=t)
    return f'''<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex,nofollow">
  <meta name="theme-color" content="{tm['theme_color']}">
  <title>{esc(m['title'])} · Rodinná kuchařka</title>
  <!-- GENERATED by tools/build.py from content/{slug}.md with theme "{t}" ({tm['name']}) — do not edit; edit the Markdown or the theme -->
  <script>/* Embedded (e.g. Notion iframe)? Mark early to avoid layout flash. */
  (function(){{var f;try{{f=window.self!==window.top}}catch(e){{f=true}}if(f)document.documentElement.classList.add('is-framed');}})();</script>
  <script type="application/json" id="recipe-meta">{meta_json(meta)}</script>
  <style>
{theme_css(t)}
  </style>
</head>
<body data-tint="{m['tint']}" data-design="{t}">
{body}
  <script>
{rd(TH, '_shared', 'script.js')}  </script>
</body>
</html>
'''

def write(path, content, changed, binary=False):
    old = open(path, 'rb' if binary else 'r', **({} if binary else {'encoding': 'utf-8'})).read() if os.path.exists(path) else None
    if old == content: return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb' if binary else 'w', **({} if binary else {'encoding': 'utf-8'})).write(content); changed.append(os.path.relpath(path, ROOT))

def slugs(): return sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, 'content')) if f.endswith('.md'))

def main(argv):
    changed = []
    todo = [a for a in argv if not a.startswith('-')] or slugs()
    used = set()
    for s in todo:
        doc = page(s); used.add(re.search(r'data-design="([a-z0-9-]+)"', doc).group(1))
        write(os.path.join(ROOT, 'recipes', s + '.html'), doc, changed)
    # fonts of every theme go to recipes/fonts/ (file names are unique per theme), so any recipe can switch theme
    for t in themes():
        for f in theme_meta(t)['fonts']:
            write(os.path.join(ROOT, 'recipes', 'fonts', f), open(os.path.join(TH, t, 'fonts', f), 'rb').read(), changed, binary=True)
        if PREVIEW_SLUG in slugs():  # theme preview page: the reference recipe rendered in this theme
            write(os.path.join(TH, t, 'preview.html'), page(PREVIEW_SLUG, theme=t, self_href='preview.html'), changed)
    print(json.dumps({"built": todo, "changed": changed}, ensure_ascii=False))
    return changed

if __name__ == '__main__': main(sys.argv[1:])
