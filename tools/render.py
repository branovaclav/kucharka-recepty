#!/usr/bin/env python3
"""Build recipes/<slug>.html (full page) + images/thumbs + images/covers from tools/content/<slug>.json.

  python3 tools/render.py [slug ...]

Use this only when a recipe's TEXT is added or changed (it rewrites the whole page). Family data
(ratings, labels, time, notes …) are kept from the existing page's recipe-meta and are then maintained by sync.py.
Design: cookbook/cookbook.md (Smalt). Styles: tools/style/*.css. Fonts: recipes/fonts/ (relative).
"""
import base64, io, json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync
from sync import esc
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)

def rd(p): return open(os.path.join(T, p), encoding='utf-8').read()
def jpeg(path, width, q):
    im = Image.open(path).convert('RGB')
    if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True); return b.getvalue(), im.size
def thumb(path, out, w=480, h=360):
    im = Image.open(path).convert('RGB'); r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im.crop((l, t, l + w, t + h)).save(out, 'JPEG', quality=74, optimize=True, progressive=True)
def datauri(b): return 'data:image/jpeg;base64,' + base64.b64encode(b).decode()

def ingredient(i):
    if isinstance(i, dict): return f'          <li class="checklist-group"><span>{esc(i["group"])}</span></li>'
    q = f'<span class="qty">{esc(i[0])}</span> ' if i[0] else ''
    return f'          <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">{q}{esc(i[1])}</span></button></li>'

def extra(e):
    if e['kind'] == 'sidenote':
        return (f'          <!-- @c:sidenote -->\n          <aside class="sidenote" data-origin="ours" lang="cs">\n            <span class="sidenote-label">Na okraj · náš doplněk</span>\n'
                f'            <p>{e["html"]}</p>\n          </aside>\n          <!-- /@c:sidenote -->')
    if e['kind'] == 'our-inline':
        return f'          <!-- @c:our-inline -->\n          <p class="our-inline" lang="cs"><span class="our-mark">Náš tip</span> {e["html"]}</p>\n          <!-- /@c:our-inline -->'
    if e['kind'] == 'warning':
        return (f'          <!-- @c:warning -->\n          <div class="warning" role="note" lang="cs">\n            <span class="warning-label">Pozor · náš doplněk</span>\n'
                f'            <p>{e["html"]}</p>\n          </div>\n          <!-- /@c:warning -->')
    raise ValueError(e['kind'])

def step(s, imgs):
    out = ['        <li class="step"><div class="step-body">']
    if s.get('h'): out.append(f'          <h3>{esc(s["h"])}</h3>')
    out += [f'          <p>{esc(p)}</p>' for p in s['p']]
    if s.get('photo'):
        ph = s['photo']; b, (w, h) = imgs(ph['file'], 720, 70)
        out.append(f'          <figure class="step-photo">\n            <img src="{datauri(b)}" alt="{esc(ph["alt"])}" loading="lazy" width="{w}" height="{h}">\n'
                   f'            <figcaption>{esc(ph["caption"])}</figcaption>\n          </figure>')
    out += [extra(e) for e in s.get('extras', [])]
    out.append('          <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>\n        </div></li>')
    return '\n'.join(out)

def tip(t, src_lang):
    facts = ''.join(f'<span class="fact"><b>{esc(a)}</b>{esc(b)}</span>' for a, b in t.get('facts', []))
    facts = f'\n      <div class="facts">{facts}</div>' if facts else ''
    if t['kind'] == 'source':
        ps = ''.join(f'\n      <p>{esc(p)}</p>' for p in t['p'])
        return (f'    <!-- @c:tip-source -->\n    <aside class="tip tip--source" lang="{src_lang}">\n      <span class="tip-label" lang="cs">Tip ze zdroje</span>\n'
                f'      <h3 lang="cs">{esc(t["h"])}</h3>{facts}{ps}\n      <p class="tip-source" lang="cs">{t["src_html"]}</p>\n    </aside>\n    <!-- /@c:tip-source -->')
    big = f'\n      <p class="big">{esc(t["big"])}</p>' if t.get('big') else ''
    ps = ''.join(f'\n      <p>{p}</p>' for p in t['p_html'])
    return (f'    <!-- @c:tip-ours -->\n    <aside class="tip tip--ours" lang="cs">\n      <span class="tip-label">Náš tip</span>\n      <h3>{esc(t["h"])}</h3>{big}{facts}{ps}\n'
            f'      <p class="tip-source">Doplněno námi — není součástí původního receptu.</p>\n    </aside>\n    <!-- /@c:tip-ours -->')

def build(slug):
    c = json.load(open(os.path.join(T, 'content', slug + '.json'), encoding='utf-8'))
    imgdir = os.path.join(T, 'img'); src = c['source']; L = c['lang']
    def imgs(f, w, q): return jpeg(os.path.join(imgdir, f), w, q)
    out = os.path.join(ROOT, 'recipes', slug + '.html')
    old = sync.read_meta(open(out, encoding='utf-8').read()) if os.path.exists(out) else None
    meta = {"slug": slug, "recipe_id": c['recipe_id'], "url": f"recipes/{slug}.html", "thumb": f"images/thumbs/{slug}.jpg",
            "cover": f"images/covers/{slug}.jpg", "lang": L, "source": {k: src[k] for k in ('site', 'url', 'title', 'author')},
            "title": c.get('title', src['title']), "notion_id": "", "notion_url": "", "total_time": None, "difficulty": "",
            "labels": [], "appliances": [], "ingredients": [], "rating_overall": "", "ratings": {k: "" for k, _, _ in sync.PEOPLE},
            "last_prepared": "", "notes": "", "main_ingredient": "", "tint": c['tint']}
    if old and old.get('notion_id'):  # keep family data already synced
        for k in ("title", "notion_id", "notion_url", "total_time", "difficulty", "labels", "appliances", "ingredients",
                  "rating_overall", "ratings", "last_prepared", "notes", "main_ingredient", "tint"): meta[k] = old.get(k, meta[k])
    R = {k: fn(meta) for k, fn in sync.REGIONS.items()}
    hero_b, (hw, hh) = imgs(c['hero']['file'], 720, 86)
    thumb(os.path.join(imgdir, c['hero']['file']), os.path.join(ROOT, 'images', 'thumbs', slug + '.jpg'))
    cov, _ = imgs(c['hero']['file'], 1200, 80); open(os.path.join(ROOT, 'images', 'covers', slug + '.jpg'), 'wb').write(cov)
    rating = (f'\n        <p class="src-rating"><span class="stars" aria-hidden="true">★★★★★</span> {src["rating"]} <small>({src["rating_count"]}× hodnoceno na {src["site"]})</small></p>'
              if src.get('rating') else f'\n        <p class="src-rating"><small>Recept z {src["site"]} — bez hodnocení čtenářů</small></p>')
    people = '\n'.join(f'          <li><span class="who">{n}</span>{R["rating_" + k]}</li>' for k, n, _ in sync.PEOPLE)
    credit = f'<a href="{esc(src["url"])}" rel="noopener">{esc(src["site"])} — {esc(src["title"])}</a> · autor {esc(src["author"])}'
    foot_extra = ''.join(f'\n    <p>{x}</p>' for x in c.get('foot_extra', []))
    ingr = '\n'.join(ingredient(i) for i in c['ingredients'])
    steps = '\n'.join(step(s, imgs) for s in c['steps'])
    tips = '\n'.join(tip(t, L) for t in c['tips'])
    serv_k = 'Porcie' if L == 'sk' else 'Porce'
    body = f'''<!-- @c:frame -->
<div class="frame-open" role="region" aria-label="Vložená stránka">
  <a class="btn-fullscreen" href="{slug}.html" target="_blank" rel="noopener" data-fullscreen-link>⤢ Otevřít na celou obrazovku</a>
</div>
<!-- /@c:frame -->
<!-- @c:topbar -->
<header class="topbar">
  <div class="wrap">
    <a class="backlink" href="../index.html">Všechny recepty</a>
    <p class="credit">Zdroj: {credit}</p>
  </div>
</header>
<!-- /@c:topbar -->

<main class="wrap" id="recipe" data-recipe-id="{c['recipe_id']}">
  <!-- @c:hero -->
  <section class="hero">
    <figure class="hero-photo">
      <img src="{datauri(hero_b)}" alt="{esc(c['hero']['alt'])}" width="{hw}" height="{hh}">
    </figure>
    <div class="hero-text">
      <!-- @c:labels -->
      {R['labels']}
      <!-- /@c:labels -->
      {R['title']}
      <p class="lede" lang="{L}">{esc(c['lede'])}</p>
      <div class="hero-ratings">
        <p class="overall"><span class="overall-k">Rodina</span> {R['rating_overall']}</p>{rating}
      </div>
    </div>
  </section>
  <!-- /@c:hero -->

  <!-- @c:meta -->
  <ul class="meta" aria-label="Základní údaje">
    <li><span class="k">Čas</span>{R['total_time']}<span class="sub" lang="{L}">{esc(c['time_sub'])}</span></li>
    <li><span class="k">{serv_k}</span><span class="v">{esc(c['servings'][0])}</span><span class="sub" lang="{L}">{esc(c['servings'][1])}</span></li>
    <li><span class="k">Obtížnost</span>
      <!-- @c:difficulty -->
      {R['difficulty']}
      <!-- /@c:difficulty -->
    </li>
    <li class="meta-appliances"><span class="k">Spotřebiče</span>
      <!-- @c:appliances -->
      {R['appliances']}
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
        <p class="last-prepared">Naposledy vařeno {R['last_prepared']}</p>
      </div>
      <!-- /@c:ratings -->
      <!-- @c:notes -->
      <div class="card notes-card">
        <h3 class="card-title">Poznámky</h3>
        {R['notes']}
      </div>
      <!-- /@c:notes -->
    </div>
  </section>
  <!-- /@c:family -->

  <div class="cook">
    <!-- @c:ingredients -->
    <section class="ingredients" aria-labelledby="h-ingr">
      <h2 class="section-title" id="h-ingr">Suroviny <small lang="{L}">{esc(c['ingr_small'])}</small></h2>
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
    <p><strong>Zdroj receptu:</strong> <a href="{esc(src['url'])}" rel="noopener">{esc(src['title'])} na {esc(src['site'])}</a> (autor {esc(src['author'])}). {esc(src['photo'])}</p>{foot_extra}
    <p class="foot-ours">Části označené <b>Náš tip</b> / <b>náš doplněk</b> jsme doplnili sami, v původním receptu nejsou. Text receptu je převzatý beze změn.</p>
    <p><a class="foot-back" href="../index.html">← Zpět na všechny recepty</a></p>
  </div>
</footer>
<!-- /@c:source-foot -->'''
    body = '\n'.join('  ' + l if l.strip() else '' for l in body.splitlines())
    css = '\n'.join(rd('style/' + f) for f in ('fonts.css', 'tints.css', 'icons.css', 'design.css', 'official.css'))
    doc = f'''<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex,nofollow">
  <meta name="theme-color" content="#183a74">
  <title>{esc(meta['title'])} · Rodinná kuchařka</title>
  <!-- DESIGN: smalt (Smalt & puntík) · cookbook/cookbook.md · built by tools/render.py from tools/content/{slug}.json; family data by tools/sync.py -->
  <script>/* Embedded (e.g. Notion iframe)? Mark early to avoid layout flash. */
  (function(){{var f;try{{f=window.self!==window.top}}catch(e){{f=true}}if(f)document.documentElement.classList.add('is-framed');}})();</script>
  <script type="application/json" id="recipe-meta">{sync.meta_json(meta)}</script>
  <style>
{css}
  </style>
</head>
<body data-tint="{meta['tint']}" data-design="smalt">
{body}
  <script>
{rd('style/script.js')}  </script>
</body>
</html>
'''
    open(out, 'w', encoding='utf-8').write(doc)
    print(slug, os.path.getsize(out))

if __name__ == '__main__':
    for s in sys.argv[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(T, 'content')) if f.endswith('.json')): build(s)
