"""Read/write content/<slug>.md: YAML front matter (synced + recipe fields) + Markdown body (verbatim recipe text).

Body format: see docs/CONTENT-FORMAT.md. Parsed into a plain dict that tools/build.py renders with a theme.
"""
import html, json, re
import yaml

# Canonical front matter key order. Keys marked SYNCED are overwritten from data/<slug>.json by apply_json.py (Notion wins).
FRONT_KEYS = [
    "slug", "title", "theme", "tint", "lang",                                   # title, theme, tint: SYNCED (tint derived from main_ingredient)
    "total_time", "difficulty", "main_ingredient", "labels", "appliances", "ingredients",  # SYNCED
    "ratings", "last_prepared", "notes",                                        # SYNCED
    "notion_id", "notion_url", "page_url",                                      # SYNCED
    "source", "hero", "servings", "time_note", "ingredients_note"]             # md-owned (never touched by sync)
SYNCED = ["title", "theme", "tint", "total_time", "difficulty", "main_ingredient", "labels", "appliances", "ingredients",
          "ratings", "last_prepared", "notes", "notion_id", "notion_url", "page_url"]
RATING_KEYS = ["overall", "brano", "zuzka", "andrej", "tomas", "lukas"]

def split(text):
    if not text.startswith('---\n'): raise ValueError('missing front matter')
    end = text.index('\n---\n', 4)
    return yaml.safe_load(text[4:end]) or {}, text[end + 5:]

def _s(v):  # scalar → YAML (JSON-style strings are valid YAML and never ambiguous)
    if v is None or v == '': return '""'
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, (int, float)): return str(v)
    return json.dumps(str(v), ensure_ascii=False)

def _v(v, ind):
    pad = ' ' * ind
    if isinstance(v, dict):
        if not v: return ' {}'
        return ''.join(f'\n{pad}  {k}:{_v(x, ind + 2)}' for k, x in v.items())
    if isinstance(v, list):
        if not v: return ' []'
        if all(not isinstance(x, (dict, list)) for x in v): return ' [' + ', '.join(_s(x) for x in v) + ']'
        return ''.join(f'\n{pad}  - {{' + ', '.join(f'{k}: {_s(y)}' for k, y in x.items()) + '}' for x in v)
    return ' ' + _s(v)

def dump_front(fm):
    keys = [k for k in FRONT_KEYS if k in fm] + sorted(k for k in fm if k not in FRONT_KEYS)
    return '---\n' + ''.join(f'{k}:{_v(fm[k], 0)}\n' for k in keys) + '---\n'

def normalize_front(fm):
    fm = dict(fm)
    r = fm.get('ratings') or {}
    fm['ratings'] = {k: (r.get(k) or '') for k in RATING_KEYS}
    for k in ('labels', 'appliances', 'ingredients'): fm[k] = list(fm.get(k) or [])
    fm['ingredients'] = [i if isinstance(i, dict) else {"name": i, "cs": i} for i in fm['ingredients']]
    fm['ingredients'] = [{"name": i.get('name', ''), "cs": i.get('cs') or i.get('czech') or i.get('name', '')} for i in fm['ingredients']]
    for k in ('title', 'theme', 'tint', 'difficulty', 'main_ingredient', 'last_prepared', 'notes', 'notion_id', 'notion_url', 'page_url'):
        fm[k] = '' if fm.get(k) is None else fm.get(k)
    if fm['last_prepared']: fm['last_prepared'] = str(fm['last_prepared'])[:10]
    tt = fm.get('total_time'); fm['total_time'] = int(tt) if tt not in (None, '') else ''
    return fm

# ---------- inline Markdown (deliberately tiny: **bold**, *italic*, [text](url)) ----------
def inline(s):
    s = html.escape(s, quote=True)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{m.group(2)}" rel="noopener">{m.group(1)}</a>', s)
    return s

# ---------- block parser ----------
IMG = re.compile(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)\s*$')
def blocks(lines):
    out, para, i = [], [], 0
    def flush():
        if para: out.append(('p', ' '.join(x.strip() for x in para))); para.clear()
    while i < len(lines):
        ln = lines[i]; st = ln.strip()
        if st.startswith('<!--'):
            flush()
            while '-->' not in lines[i]: i += 1
            i += 1; continue
        if not st: flush(); i += 1; continue
        if st.startswith(':::') and st != ':::':
            flush(); head = st[3:].strip(); kind, _, title = head.partition(' ')
            j = i + 1
            while j < len(lines) and lines[j].strip() != ':::': j += 1
            if j >= len(lines): raise ValueError(f'unclosed ::: {kind} (line {i + 1})')
            out.append(('box', kind, title.strip(), blocks(lines[i + 1:j]))); i = j + 1; continue
        if st.startswith('### '): flush(); out.append(('h3', st[4:].strip())); i += 1; continue
        if st.startswith(('- ', '* ')): flush(); out.append(('li', st[2:].strip())); i += 1; continue
        if st.startswith('> '): flush(); out.append(('quote', st[2:].strip())); i += 1; continue
        m = IMG.match(st)
        if m: flush(); out.append(('img', m.group(1), m.group(2), m.group(3) or '')); i += 1; continue
        para.append(ln); i += 1
    flush(); return out

SECTIONS = {"suroviny": "ingredients", "ingredience": "ingredients", "postup": "steps", "postup přípravy": "steps",
            "tipy": "tips", "zdroj": "foot", "ke zdroji": "foot"}
QTY = re.compile(r'^\*\*(.+?)\*\*\s+(.*)$')

def parse_body(body):
    secs, cur = {"lede": []}, "lede"
    for ln in body.splitlines():
        if ln.startswith('## '):
            name = ln[3:].strip().lower()
            if name not in SECTIONS: raise ValueError(f'unknown section "## {ln[3:].strip()}" (allowed: Suroviny, Postup, Tipy, Zdroj)')
            cur = SECTIONS[name]; secs[cur] = []; continue
        secs.setdefault(cur, []).append(ln)
    R = {"lede": [b[1] for b in blocks(secs["lede"]) if b[0] == 'p'], "ingredients": [], "steps": [], "tips": [], "foot": []}
    for b in blocks(secs.get("ingredients", [])):
        if b[0] == 'h3': R["ingredients"].append({"group": b[1]})
        elif b[0] == 'li':
            m = QTY.match(b[1]); R["ingredients"].append({"qty": m.group(1), "text": m.group(2)} if m else {"qty": "", "text": b[1]})
    step = None
    for b in blocks(secs.get("steps", [])):
        if b[0] == 'h3':
            h = re.sub(r'^\d+\.\s*', '', b[1]); step = {"h": h, "items": []}; R["steps"].append(step); continue
        if step is None: raise ValueError('step content before the first "### 1." heading')
        if b[0] == 'p': step["items"].append(("p", b[1]))
        elif b[0] == 'img': step["items"].append(("img", b[1], b[2], b[3]))
        elif b[0] == 'box':
            kind = {"our-tip": "our-inline", "note": "sidenote", "warning": "warning"}.get(b[1])
            if not kind: raise ValueError(f'::: {b[1]} not allowed inside a step (use our-tip, note, warning)')
            step["items"].append((kind, [x[1] for x in b[3] if x[0] == 'p']))
    for b in blocks(secs.get("tips", [])):
        if b[0] != 'box' or b[1] not in ('tip', 'our-tip'):
            raise ValueError(f'## Tipy may contain only "::: tip Title" / "::: our-tip Title" boxes, found {b[0]} {b[1] if len(b) > 1 else ""!r}')
        t = {"kind": "source" if b[1] == 'tip' else "ours", "h": b[2], "facts": [], "big": "", "p": [], "source": ""}
        for x in b[3]:
            if x[0] == 'li':
                m = QTY.match(x[1]); t["facts"].append((m.group(1), m.group(2)) if m else (x[1], ''))
            elif x[0] == 'quote': t["big"] = x[1]
            elif x[0] == 'p' and x[1].startswith('— '): t["source"] = x[1][2:]
            elif x[0] == 'p': t["p"].append(x[1])
        R["tips"].append(t)
    R["foot"] = [b[1] for b in blocks(secs.get("foot", [])) if b[0] == 'p']
    return R
