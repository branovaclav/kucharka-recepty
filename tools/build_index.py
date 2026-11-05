#!/usr/bin/env python3
"""Waterfall step 3: front matter of content/*.md → index.html (theme vocab.INDEX_THEME, template themes/<id>/index.template.html).

  python3 tools/build_index.py
Deterministic; writes index.html only when it changes. The "Správa v Notion" link lives in the template.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vocab as V
from build import ROOT, TH, esc, rd, canon, load, slugs, fmt_minutes, write

def card(r):
    diff = {"easy": "Snadné", "medium": "Střední", "hard": "Náročné"}.get(r.get('difficulty') or '', '—')
    v = r.get('rating_overall') or ''
    return f'''      <li class="rcard" data-slug="{esc(r['slug'])}" data-tint="{esc(r.get('tint') or 'veg')}">
        <a href="{esc(r['url'])}">
          <img src="{esc(r['thumb'])}" alt="" width="480" height="360" loading="lazy">
          <span class="rcard-body">
            <span class="rcard-title">{esc(r['title'])}</span>
            <span class="rcard-facts"><span class="fact-time">{fmt_minutes(r.get('total_time'))}</span><span class="difficulty" data-value="{esc(r.get('difficulty') or '')}"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span><span class="difficulty-text">{diff}</span></span></span>
            <span class="rating" data-value="{v}">{V.RATING_CS.get(v, 'Zatím nehodnoceno')}</span>
          </span>
        </a>
      </li>'''

def build():
    recs = sorted((canon(load(s)[0]) for s in slugs()), key=lambda r: r['title'].lower())
    for r in recs:
        if not os.path.exists(os.path.join(ROOT, r['thumb'])): print(f'warning: missing {r["thumb"]} — run tools/images.py {r["slug"]}', file=sys.stderr)
    t = V.INDEX_THEME
    data = [{k: r.get(k) for k in ("slug", "title", "url", "thumb", "total_time", "difficulty", "labels", "appliances",
                                    "ingredients", "rating_overall", "last_prepared", "tint", "theme")} for r in recs]
    css = '\n'.join([rd(TH, t, 'fonts.css'), rd(TH, '_shared', 'tints.css'), rd(TH, '_shared', 'icons.css'), rd(TH, t, 'index.css')]
                    ).replace('url("fonts/', 'url("recipes/fonts/')
    tpl = rd(TH, t, 'index.template.html')
    return (tpl.replace('{{CSS}}', css).replace('{{CARDS}}', '\n'.join(card(r) for r in recs)).replace('{{COUNT}}', str(len(recs)))
               .replace('{{DATA}}', json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).replace('</', '<\\/')))

def main():
    changed = []; write(os.path.join(ROOT, 'index.html'), build(), changed)
    print(json.dumps({"changed": changed})); return changed

if __name__ == '__main__': main()
