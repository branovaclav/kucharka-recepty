> **Theme `len` (design B „Len“) in the official build.** This catalogue is the design-phase document, ported unchanged.
> In production the theme is `themes/len/theme.json` + `fonts.css` + `design.css` + `fonts/`. The markup is shared with every
> theme and produced by `tools/build.py`. The rules that win are in `themes/smalt/cookbook.md` (O-sections) and `docs/AGENT.md`.
> Live preview: `themes/len/preview.html`. To use it for a recipe, set Notion Theme = `len` (or front matter `theme: len`).

# Design cookbook B — „Len“

*Calm Scandinavian editorial: linen-white page, near-black ink, hairline rules, a big quiet serif title on one wide band of the page tint.*
No shadows and no heavy borders — hierarchy comes from type size, whitespace and thin rules.

Sample: [`kureci-rizek.html`](kureci-rizek.html) · Screenshots: `preview.png` (full page, chicken), `tints.png` (all 6 tints).

## 1. Look & tokens

| token | value | use |
|---|---|---|
| `--tint` | from `data-tint` (§3) | full-width hero band + top bar, notes card, source-tip panel |
| `--tint-ink` | from `data-tint` | kicker labels, step numerals 01–05, icons |
| `--bg` / `--surface` | `#faf8f3` / `#ffffff` | page / cards |
| `--ink` / `--muted` | `#1e2522` / `#555d58` | text / secondary text (6.4:1) |
| `--line` / `--line-strong` | `#e2ded4` / `#c9c3b6` | hairlines, chip outlines |
| `--pine` | `#2f4a3f` | primary buttons, ticks, **our additions** (dashed pine outline) |
| `--red` | `#a8321f` | warnings, "Chutná" heart |
| `--radius` | `14px` | cards, panels |

Typography: **Newsreader** 400–700 (display optical size baked in) for title, section heads, values, numerals and notes;
**Figtree** 300–900 (body at weight 430) for text and UI. Labels: 0.8–0.9 rem uppercase, letter-spacing .14em.
Section heads sit under a 1 px ink rule. Step numbers are leading-zero serif numerals in `--tint-ink`.

**Our-addition rule:** dashed pine outline + pine "＋ Náš tip" tag. Source tips are solid tint panels without outline.

## 2. Page skeleton (every recipe page)

One recipe = one standalone file `recipes/<slug>.html`. Everything is inline: one `<style>` block (copy the
**complete** block from this design's `kureci-rizek.html` — it is the canonical stylesheet; the snippets below
are the same CSS split per component), images as `data:` URIs, icons as inline SVG (CSS mask data URIs),
one `<script>` at the end. Only the fonts are separate files (`fonts/*.woff2`, same folder level as
referenced by `url("fonts/…")` — on GitHub Pages put them in `recipes/fonts/` or change the `url()` paths
to `../fonts/`). If a font fails to load, the system fallback in the font stack is used — nothing breaks.

```html
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex,nofollow">
  <meta name="theme-color" content="#2f4a3f">
  <title>Kuřecí řízek · Rodinná kuchařka</title>   <!-- sync: title + " · Rodinná kuchařka" -->
  <!-- DESIGN: len · RECIPE: <slug> | source: <url> | notion-page: <id> -->
  <script>/* Embedded (e.g. Notion iframe)? Mark early to avoid layout flash. */
  (function(){var f;try{f=window.self!==window.top}catch(e){f=true}if(f)document.documentElement.classList.add('is-framed');})();</script>
  <style>/* fonts → tints → icons → base → components (copy whole block) */</style>
</head>
<body data-tint="chicken" data-design="len">
  [frame] [topbar]
  <main class="wrap" id="recipe" data-recipe-id="<slug>">   <!-- data-recipe-id keys localStorage; must be unique -->
    [hero (+labels, overall rating)] [meta (+difficulty, appliances)] [family (ratings + notes)]
    <div class="cook"> [ingredients] [steps (+our-inline, sidenote, warning inside steps)] </div>
    <section class="tips" aria-label="Tipy"> [tip-source] [tip-ours] </section>
    [toolbar]
  </main>
  [source-foot]
  <script>/* shared behaviour — copy unchanged, see §6 */</script>
</body>
</html>
```

Content rules (all designs):
- **Original text stays verbatim** (Czech/Slovak as published; light formatting only — no rewording, no translation).
- **Anything we add is visibly marked as ours**: use only `our-inline`, `tip--ours`, `sidenote[data-origin="ours"]`
  or `warning` (label "… · náš doplněk"). Never add our words into an original `<p>`.
- Source credit **twice**: `.credit` in the top bar and `.source-foot` at the bottom. Tips taken from another source
  page go in `tip--source` with their own `.tip-source` link.
- Omit what the source does not have (no rating → drop `.src-rating`; no photo for a step → no `<figure>`).

## 3. Tint system — main ingredient

`<body data-tint="…">` is the only per-recipe colour decision. Six keys, identical hex in all three designs:

| key | meaning (Hlavní surovina) | `--tint` | `--tint-strong` | `--tint-ink` |
|---|---|---|---|---|
| `chicken` | drůbež (kuře, krůta, kachna) — teplá žlutá | `#FCEDBE` | `#E9C153` | `#684D00` |
| `pork-beef` | vepřové, hovězí, zvěřina, uzené — světlá terakota | `#F6DACD` | `#D98A6B` | `#7A3820` |
| `minced` | mleté maso (karbanátky, sekaná, boloňská) — broskvová | `#FFE3CF` | `#F3A576` | `#80421A` |
| `pasta-rice` | těstoviny, rýže, brambory, knedlíky bez masa jako základ — krémová | `#F5EEDC` | `#D5C192` | `#5E4F2C` |
| `fish` | ryby a mořské plody — jemná modrá | `#DCEAF5` | `#8CB5D4` | `#1F4E76` |
| `veg` | vegetariánské (zelenina, luštěniny, vejce, sýr) — šalvějová | `#E0ECDA` | `#99BB8E` | `#36592F` |

Contrast: `--tint-ink` is ≥ 6.3:1 on `--tint` and ≥ 7.7:1 on white; body ink is ≥ 11.9:1 on every `--tint`.
`--tint-strong` is decorative only (borders, tape, gingham, highlighter) — never put text on it.

**Deterministic rule (for the sync script)** — pick the first that matches, from the recipe's labels / main ingredient:
1. fish or seafood → `fish`  2. poultry → `chicken`  3. minced meat → `minced`  4. any other meat → `pork-beef`
5. no meat and the base is pasta / rice / potatoes / dumplings → `pasta-rice`  6. otherwise → `veg`.
Recommended: an explicit Notion select "Hlavní surovina" (6 options) so the rule never has to guess.
Difficulty is **not** a tint — it is the small `.difficulty` badge.

## 4. Notion sync contract (`data-sync`)

The sync script only touches elements carrying `data-sync`; everything else on the page is static.
Replace the element's **content** (and `data-value` / `datetime` where noted). Never remove the element — if a value
is empty, write the empty-state text shown below.

| `data-sync` | element | how to write it |
|---|---|---|
| `title` | `<h1>` | plain text; also update `<title>` (`<title>{title} · Rodinná kuchařka</title>`). On rename also rename the file + links. |
| `total_time` | `.meta .v` | `"40 min"` / `"1 h 15 min"` |
| `difficulty` | `.difficulty` | `data-value="easy|medium|hard"` + `.difficulty-text` = `Snadné` / `Střední` / `Náročné` (keep the `.pips` span) |
| `labels` | `ul.labels` | one `<li class="label-chip">štítek</li>` per Notion label, in Notion order |
| `appliances` | `ul.appliances` | one `<li class="appliance" data-value="KEY">Název</li>`; keys: `gas-stove` Plynový sporák, `induction` Indukční deska, `oven` Trouba, `air-fryer` Horkovzdušná fritéza, `microwave` Mikrovlnka, `blender` Mixér; unknown key → pot icon |
| `rating_overall` | `.overall .rating` | `data-value` + text, see below |
| `rating_brano`, `rating_zuzka`, `rating_andrej`, `rating_tomas`, `rating_lukas` | `.ratings .rating` | `data-value="loved"` → `Chutná`, `"ok"` → `Ujde`, `"disliked"` → `Nechutná`, `""` → `Zatím nehodnotil` (Zuzka: `Zatím nehodnotila`) |
| `last_prepared` | `<time>` | `datetime="YYYY-MM-DD"` + text `D. M. YYYY`; empty → `datetime=""`, text `zatím ne` |
| `notes` | `div.notes` | Notion text → `<p>` per paragraph (HTML-escaped); empty → `<p>Zatím bez poznámek.</p>` |

All writes are plain string/attribute replacements on tagged elements → the sync can be a deterministic script
(parse with an HTML parser, replace, write back, commit only if the file changed).

## 5. Interaction & accessibility rules

- Tap targets ≥ 44 px (ingredient rows 56–60 px, toolbar 56 px). Body text 19–23 px, steps 21–26 px.
- State is never shown by colour alone: ticked ingredients are also struck through; ratings always show the word.
- Ingredient ticks and "Hotovo" steps persist in `localStorage` under `kucharka:<recipe-id>:ingr|steps`.
- **Framed (Notion embed)**: the `<head>` script adds `html.is-framed` → sticky **⤢ Otevřít na celou obrazovku** bar
  appears (link rewritten by the script to the page's own URL, `target="_blank"`), wake-lock button stays hidden,
  sticky ingredient column is disabled, hero photo is height-capped.
- Wake lock button is `hidden` by default and only revealed where `navigator.wakeLock` exists and the page is not framed.
- Layout: single column up to 999 px (iPad portrait; ingredients in 2 columns from 640 px); from 1000 px
  (iPad landscape) ingredients become a sticky left column beside the steps.

## 5a. iPhone & responsive layout

The same page must work on iPhone (375–430 px wide), iPad portrait (820 px) and iPad landscape (1180 px).

**Breakpoints** (CSS px, `max-width`/`min-width` media queries only — no JS layout):

| width | device | layout |
|---|---|---|
| < 560 | iPhone portrait | single column; info strip = **Čas full width**, then Porce · Obtížnost side by side, then Spotřebiče; ingredients 1 column; tip facts shrink to 1.6rem |
| 560–639 | iPhone landscape / small | single column; info strip 3 columns |
| 640–999 | iPad portrait | single column; ingredients 2 columns |
| ≥ 1000 | iPad landscape / desktop | hero photo beside text; info strip 4 columns; ingredients sticky left column beside steps (sticky off when height < 760) |

**Rules**

- `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` — never add `maximum-scale`/`user-scalable=no` (pinch-zoom must stay possible).
- `html { -webkit-text-size-adjust: 100%; text-size-adjust: 100% }` — stops iOS inflating text in landscape.
- Safe areas: `body` is padded with `env(safe-area-inset-top|right|bottom|left)` (notch / Dynamic Island / home indicator, matters in landscape and when added to the Home Screen); the sticky fullscreen bar uses `max(.5rem, env(safe-area-inset-top))`.
- **No horizontal scroll, ever**: `html, body { overflow-x: clip }`; grid columns are `minmax(0, 1fr)` (plain `1fr` lets a long word widen the page and iOS then zooms the whole page out); big values (`40 min`, `180 °C`) are `white-space: nowrap` and the layout gives them room instead of breaking them. Use `&nbsp;` between a number and its unit in our own texts.
- Tap targets ≥ 44 × 44 px on phone too: buttons, chips and the bottom back link (`.foot-back`) have `min-height: 44px`; inline text links get `padding-block: .35em` for a larger hit area without changing the layout.
- Nothing sticky on phones except the fullscreen bar when framed; it is ~50 px and never covers the checklist (ingredients are only sticky ≥ 1000 px).
- Long Czech words: headings use `text-wrap: balance` where supported; never set fixed widths on text containers.
- Check before publishing: `document.documentElement.scrollWidth === innerWidth` at 375, 393 and 1180 px (Playwright `is_mobile=True`, DPR 3).

## 6. Shared script (copy unchanged to every page, all designs)

```html
<script>
/* Shared recipe behaviour — identical on every recipe page, in every design. Do not edit per recipe. */
(function () {
  var root = document.getElementById('recipe'), id = root.dataset.recipeId;
  var KEY_I = 'kucharka:' + id + ':ingr', KEY_S = 'kucharka:' + id + ':steps';
  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || []; } catch (e) { return []; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function wire(btns, key, onSet) {
    var state = load(key);
    btns.forEach(function (b, i) {
      var set = function (on) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); if (onSet) onSet(b, on); };
      set(state.indexOf(i) > -1);
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true'; set(on);
        state = btns.map(function (x, j) { return x.getAttribute('aria-pressed') === 'true' ? j : -1; }).filter(function (j) { return j > -1; });
        save(key, state);
      });
    });
    return function () { btns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); if (onSet) onSet(b, false); }); save(key, []); };
  }
  var resetI = wire([].slice.call(root.querySelectorAll('[data-checklist] button')), KEY_I);
  var resetS = wire([].slice.call(root.querySelectorAll('.step-done')), KEY_S, function (b, on) {
    b.closest('.step').classList.toggle('is-done', on); b.textContent = on ? 'Hotovo ✓' : 'Hotovo';
  });
  var r = root.querySelector('[data-reset]'); if (r) r.addEventListener('click', resetI);
  var ra = root.querySelector('[data-reset-all]'); if (ra) ra.addEventListener('click', function () { resetI(); resetS(); window.scrollTo(0, 0); });
  /* Embedded (Notion iframe): the full-screen link opens this exact page in a new tab; wake lock is usually blocked in frames, so it stays hidden. */
  var framed = document.documentElement.classList.contains('is-framed');
  var fl = document.querySelector('[data-fullscreen-link]'); if (fl) fl.href = location.href.split('#')[0];
  /* Keep the iPad screen on while cooking (Screen Wake Lock API, iPadOS 16.4+). */
  var wl = root.querySelector('[data-wakelock]'), lock = null;
  if (wl && 'wakeLock' in navigator && !framed) {
    wl.hidden = false;
    var req = function () { return navigator.wakeLock.request('screen').then(function (l) { lock = l; wl.setAttribute('aria-pressed', 'true');
      l.addEventListener('release', function () { wl.setAttribute('aria-pressed', 'false'); }); }).catch(function () {}); };
    wl.addEventListener('click', function () { if (lock && !lock.released) { lock.release(); lock = null; } else { req(); } });
    document.addEventListener('visibilitychange', function () { if (lock && document.visibilityState === 'visible' && wl.getAttribute('aria-pressed') === 'true') req(); });
  }
})();
</script>
```


## 7. Component catalogue

Each component = HTML (copy into the page) + CSS (already contained in the page's full `<style>`; shown here so a component can be understood, adjusted or reused alone). Components marked *nested* live inside another one.

### 7.1 Fonts  `@c:fonts`

@font-face declarations (self-hosted woff2).

```css
/* Self-hosted, subset (Latin + Czech/Slovak), SIL OFL. Files live next to the page in fonts/. */
@font-face { font-family: "Newsreader"; src: url("fonts/newsreader.woff2") format("woff2"); font-weight: 400 700; font-display: swap; }
@font-face { font-family: "Figtree"; src: url("fonts/figtree.woff2") format("woff2"); font-weight: 300 900; font-display: swap; }
```

### 7.2 Tint variables  `@c:tints`

Shared by all designs — do not edit per page; choose the tint with `data-tint` on `<body>`.

```css
/* Pastel tint by MAIN INGREDIENT — set once per page: <body data-tint="chicken">.
   --tint = pastel surface, --tint-strong = mid accent (borders, tape, dots; never under text),
   --tint-ink = dark tint-coloured text (>= 6.3:1 on --tint and >= 7.7:1 on white). Same hex in every design. */
body, body[data-tint="chicken"] { --tint: #FCEDBE; --tint-strong: #E9C153; --tint-ink: #684D00; }  /* drůbež — teplá žlutá */
body[data-tint="pork-beef"]     { --tint: #F6DACD; --tint-strong: #D98A6B; --tint-ink: #7A3820; }  /* vepřové, hovězí — světlá terakota */
body[data-tint="minced"]        { --tint: #FFE3CF; --tint-strong: #F3A576; --tint-ink: #80421A; }  /* mleté maso — broskvová */
body[data-tint="pasta-rice"]    { --tint: #F5EEDC; --tint-strong: #D5C192; --tint-ink: #5E4F2C; }  /* těstoviny, rýže, přílohy — krémová */
body[data-tint="fish"]          { --tint: #DCEAF5; --tint-strong: #8CB5D4; --tint-ink: #1F4E76; }  /* ryby — jemná modrá */
body[data-tint="veg"]           { --tint: #E0ECDA; --tint-strong: #99BB8E; --tint-ink: #36592F; }  /* vegetariánské — šalvějová */
```

### 7.3 Icon set  `@c:icons`

Inline SVG icons as CSS mask variables + data-value mappings for appliances and ratings. Shared by all designs.

```css
/* Inline SVG icons as CSS mask images (no files, no requests). Colour = currentColor of the element.
   Appliances and ratings pick their icon from data-value, so the Notion sync only writes data-value + text. */
:root {
  --i-gas-stove: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M12 2.5c.8 3.2 5.5 5.6 5.5 11a5.5 5.5 0 0 1-11 0c0-2.6 1.3-4.4 2.6-5.6.2 2.1 1.3 3.3 2.6 3.6-.6-3.2-.6-6 .3-9z%22/></svg>");
  --i-induction: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><rect x=%223%22 y=%223%22 width=%2218%22 height=%2218%22 rx=%223%22/><circle cx=%2212%22 cy=%2212%22 r=%225.5%22/><circle cx=%2212%22 cy=%2212%22 r=%222%22/></svg>");
  --i-oven: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><rect x=%223%22 y=%223%22 width=%2218%22 height=%2218%22 rx=%222.5%22/><path d=%22M3 8h18M7 5.5h.01M10 5.5h.01%22/><rect x=%226.5%22 y=%2211%22 width=%2211%22 height=%227%22 rx=%221.2%22/></svg>");
  --i-air-fryer: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M3 8h10.5a3 3 0 1 0-3-3M3 12.5h15a3 3 0 1 1-3 3M3 17h7%22/></svg>");
  --i-microwave: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><rect x=%222%22 y=%225%22 width=%2220%22 height=%2214%22 rx=%222.5%22/><rect x=%225%22 y=%228%22 width=%2210%22 height=%228%22 rx=%221%22/><path d=%22M18.5 9v.01M18.5 12v.01M18.5 15v.01%22/></svg>");
  --i-blender: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M7 3h10l-2 10H9z%22/><path d=%22M8 13h8l.5 4a2 2 0 0 1-2 2.2h-5A2 2 0 0 1 7.5 17z%22/><path d=%22M12 16h.01%22/></svg>");
  --i-pot: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M4.5 10h15v6a4 4 0 0 1-4 4h-7a4 4 0 0 1-4-4z%22/><path d=%22M2 10h20M9 6.5c0-1.2 1-1.2 1-2.5M14 6.5c0-1.2 1-1.2 1-2.5%22/></svg>");
  --i-loved: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22><path d=%22M12 21s-8-4.9-10-10A5.3 5.3 0 0 1 12 7.2 5.3 5.3 0 0 1 22 11c-2 5.1-10 10-10 10z%22/></svg>");
  --i-ok: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><circle cx=%2212%22 cy=%2212%22 r=%229.5%22/><path d=%22M8 15h8%22/><circle cx=%229%22 cy=%229.5%22 r=%22.6%22 fill=%22%23000%22/><circle cx=%2215%22 cy=%229.5%22 r=%22.6%22 fill=%22%23000%22/></svg>");
  --i-disliked: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><circle cx=%2212%22 cy=%2212%22 r=%229.5%22/><path d=%22M8 16.5c2.2-2 5.8-2 8 0%22/><circle cx=%229%22 cy=%229.5%22 r=%22.6%22 fill=%22%23000%22/><circle cx=%2215%22 cy=%229.5%22 r=%22.6%22 fill=%22%23000%22/></svg>");
  --i-unrated: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><circle cx=%2212%22 cy=%2212%22 r=%229.5%22 stroke-dasharray=%223 3.2%22/></svg>");
  --i-check: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%223%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M5 12.5l4.5 4.5L19 7%22/></svg>");
  --i-warning: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M12 3 2 20.5h20z%22/><path d=%22M12 9.5v5M12 17.6v.01%22/></svg>");
  --i-plus: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%223%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M12 5v14M5 12h14%22/></svg>");
  --i-expand: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7%22/></svg>");
  --i-sun: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23000%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><circle cx=%2212%22 cy=%2212%22 r=%224%22/><path d=%22M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4%22/></svg>");
}
/* appliance keys (data-value) → icon. Unknown key falls back to a pot. */
.appliance { --icon: var(--i-pot); }
.appliance[data-value="gas-stove"] { --icon: var(--i-gas-stove); }
.appliance[data-value="induction"] { --icon: var(--i-induction); }
.appliance[data-value="oven"] { --icon: var(--i-oven); }
.appliance[data-value="air-fryer"] { --icon: var(--i-air-fryer); }
.appliance[data-value="microwave"] { --icon: var(--i-microwave); }
.appliance[data-value="blender"] { --icon: var(--i-blender); }
/* rating values: loved | ok | disliked | "" (unrated) */
.rating { --icon: var(--i-unrated); }
.rating[data-value="loved"] { --icon: var(--i-loved); }
.rating[data-value="ok"] { --icon: var(--i-ok); }
.rating[data-value="disliked"] { --icon: var(--i-disliked); }
.ico, .appliance::before, .rating::before { content: ""; display: inline-block; flex: none; width: 1.15em; height: 1.15em; background: currentColor;
  -webkit-mask: var(--icon) center / contain no-repeat; mask: var(--icon) center / contain no-repeat; }
```

### 7.4 Tokens, base & layout  `@c:base`

Design tokens, reset, typography, `.card`, `.btn`, `.section-title`, two-column `.cook` layout.

```css
/* ==== Len — calm Scandinavian editorial: warm white linen, near-black ink, hairline rules, big quiet serif,
   the pastel tint as one wide band behind the title and as soft panels. No shadows, no heavy borders. ==== */
:root {
  --bg: #faf8f3;       /* linen white page */
  --surface: #ffffff;  /* cards */
  --ink: #1e2522;      /* body text (15.6:1 on --bg) */
  --muted: #555d58;    /* secondary text (6.4:1 on --bg) */
  --line: #e2ded4;     /* hairlines */
  --line-strong: #c9c3b6;
  --pine: #2f4a3f;     /* primary: buttons, checks, OUR additions (9.6:1 on white) */
  --pine-soft: #e6ede9;
  --red: #a8321f;      /* warnings, loved (5.9:1 on white) */
  --font-display: "Newsreader", "Iowan Old Style", Georgia, serif;
  --font-body: "Figtree", "Avenir Next", "Segoe UI", system-ui, -apple-system, sans-serif;
  --fs-body: clamp(1.2rem, 0.95rem + 0.9vw, 1.42rem);
  --fs-step: clamp(1.3rem, 1rem + 1.05vw, 1.6rem);
  --fs-h1: clamp(3rem, 1.8rem + 4.6vw, 5.2rem);
  --fs-h2: clamp(1.9rem, 1.4rem + 1.6vw, 2.6rem);
  --radius: 14px;
  --gap: clamp(1.1rem, 0.6rem + 1.8vw, 2.2rem);
  --maxw: 1180px;
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: var(--fs-body); font-weight: 430; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; display: block; }
a { color: var(--pine); text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
:focus-visible { outline: 3px solid var(--pine); outline-offset: 3px; border-radius: 6px; }
.wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 var(--gap); }
h1, h2, h3 { font-family: var(--font-display); font-weight: 500; color: var(--ink); line-height: 1.08; margin: 0; letter-spacing: -.01em; }
.section-title { font-size: var(--fs-h2); display: flex; align-items: baseline; gap: .8rem; flex-wrap: wrap; margin-bottom: 1.1rem; padding-top: 1rem; border-top: 1px solid var(--ink); }
.section-title small { font-family: var(--font-body); font-size: .95rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(1rem, .7rem + 1vw, 1.6rem); }
.card-title { font-family: var(--font-body); font-size: .9rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin-bottom: .6rem; }
.btn { font: inherit; font-size: 1.05rem; font-weight: 600; cursor: pointer; color: var(--ink); background: var(--surface);
  border: 1.5px solid var(--ink); border-radius: 999px; padding: .6rem 1.3rem; min-height: 48px; transition: background .15s, color .15s; }
.btn:active { background: var(--pine-soft); }
.btn[aria-pressed="true"] { background: var(--pine); border-color: var(--pine); color: #fff; }
.cook { display: grid; gap: calc(var(--gap) * 1.6); margin-top: calc(var(--gap) * 1.8); }
@media (min-width: 1000px) { .cook { grid-template-columns: minmax(320px, .85fr) 1.6fr; align-items: start; } .cook .ingredients { position: sticky; top: 1rem; } }
@media (max-height: 760px) { .cook .ingredients { position: static; } }
```

### 7.5 Fullscreen button (Notion embed)  `@c:frame`

Visible only when framed (`html.is-framed`). Put it first in `<body>`.

```html
<div class="frame-open" role="region" aria-label="Vložená stránka">
  <a class="btn-fullscreen" href="kureci-rizek.html" target="_blank" rel="noopener" data-fullscreen-link>⤢ Otevřít na celou obrazovku</a>
</div>
```

```css
/* Sticky "open full screen" bar, visible only inside an iframe (Notion embed). Needs the tiny <head> script that sets html.is-framed. */
.frame-open { display: none; }
html.is-framed .frame-open { display: flex; justify-content: center; padding: .5rem var(--gap); background: var(--pine); position: sticky; top: 0; z-index: 10; }
.btn-fullscreen { display: inline-flex; align-items: center; gap: .5rem; min-height: 48px; padding: .45rem 1.4rem; border-radius: 999px; background: #fff; color: var(--pine);
  font-weight: 700; font-size: 1.1rem; text-decoration: none; }
html.is-framed [data-wakelock] { display: none !important; }
html.is-framed .cook .ingredients { position: static; }
html.is-framed .hero-photo { aspect-ratio: auto; height: clamp(180px, 50vh, 460px); }
```

### 7.6 Top bar + source credit (top)  `@c:topbar`

Back link and the first source credit. Keep author + link.

```html
<header class="topbar">
  <div class="wrap">
    <a class="backlink" href="../index.html">Všechny recepty</a>
    <p class="credit">Zdroj: <a href="https://www.toprecepty.cz/recept/23122-kureci-rizek/" rel="noopener">Toprecepty.cz — Kuřecí řízek</a> · autor blazena.blazkova</p>
  </div>
</header>
```

```css
.topbar { background: var(--tint); }
.topbar .wrap { display: flex; align-items: center; justify-content: space-between; gap: .5rem 1.2rem; flex-wrap: wrap; padding-block: .9rem; border-bottom: 1px solid color-mix(in srgb, var(--tint-ink) 25%, transparent); }
.backlink { display: inline-flex; align-items: center; gap: .55rem; min-height: 44px; font-weight: 700; font-size: 1.05rem; color: var(--ink); text-decoration: none; letter-spacing: .02em; }
.backlink::before { content: "←"; font-size: 1.2em; }
.credit { margin: 0; font-size: .95rem; color: var(--ink); }
.credit a { color: var(--ink); font-weight: 600; }
```

### 7.7 Hero  `@c:hero`

Photo (base64 JPEG, ~4:3, ≤ 1000 px wide, q≈75), labels, title, lede (source perex verbatim), family overall rating, source rating.

```html
<section class="hero">
  <figure class="hero-photo">
    <img src="data:image/jpeg;base64,…" alt="Kuřecí řízek s bramborovou kaší" width="677" height="508">
  </figure>
  <div class="hero-text">
    <!-- @c:labels -->
    <ul class="labels" data-sync="labels" aria-label="Štítky">
      <li class="label-chip">kuře</li>
      <li class="label-chip">pro začátečníky</li>
      <li class="label-chip">klasika</li>
      <li class="label-chip">smažené</li>
    </ul>
    <!-- /@c:labels -->
    <h1 data-sync="title">Kuřecí řízek</h1>
    <p class="lede">Klasikou českých Vánoc a nedělních obědů je křupavý kuřecí řízek v trojobalu. Pokud s vařením teprve začínáte a nejste si s postupem přípravy jistí, vyzkoušejte tento jednoduchý recept, podle kterého se vám řízky jistě povedou.</p>
    <div class="hero-ratings">
      <p class="overall"><span class="overall-k">Rodina</span> <span class="rating" data-sync="rating_overall" data-value="loved">Chutná</span></p>
      <p class="src-rating"><span class="stars" aria-hidden="true">★★★★★</span> 4,6 <small>(33× hodnoceno na Toprecepty.cz)</small></p>
    </div>
  </div>
</section>
```

```css
/* The tint band: the hero text sits on --tint, spanning the full window width; the photo straddles the band edge. */
.hero { display: grid; gap: calc(var(--gap) * 1.1); padding-top: calc(var(--gap) * 1.2); background: var(--tint);
  box-shadow: 0 0 0 100vmax var(--tint); clip-path: inset(0 -100vmax); position: relative; }
.hero::after { content: ""; position: absolute; left: -100vmax; right: -100vmax; bottom: 0; height: 34%; background: var(--bg); z-index: 0; }
.hero-text { order: -1; position: relative; z-index: 1; }
.hero-photo { margin: 0; border-radius: var(--radius); overflow: hidden; aspect-ratio: 3 / 2; position: relative; z-index: 1; background: var(--surface); }
.hero-photo img { width: 100%; height: 100%; object-fit: cover; }
.hero h1 { font-size: var(--fs-h1); font-weight: 400; letter-spacing: -.025em; margin-top: .7rem; color: var(--ink); }
.lede { margin: 1rem 0 0; max-width: 36ch; font-family: var(--font-display); font-size: clamp(1.3rem, 1rem + 1vw, 1.65rem); line-height: 1.45; color: var(--ink); }
.hero-ratings { display: flex; flex-wrap: wrap; align-items: center; gap: .6rem 1.4rem; margin-top: 1.2rem; }
.hero-ratings p { margin: 0; }
.overall { display: inline-flex; align-items: center; gap: .6rem; }
.overall-k { font-size: .85rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tint-ink); }
.src-rating { font-size: 1rem; color: var(--ink); }
.stars { color: var(--tint-ink); letter-spacing: .08em; }
@media (min-width: 1000px) { .hero { grid-template-columns: 1fr 1.1fr; align-items: end; padding-bottom: 0; } .hero-text { order: 0; padding-bottom: 2rem; } .hero::after { height: 18%; } }
```

### 7.8 Labels chips  `@c:labels`

`data-sync="labels"`.

```html
<ul class="labels" data-sync="labels" aria-label="Štítky">
  <li class="label-chip">kuře</li>
  <li class="label-chip">pro začátečníky</li>
  <li class="label-chip">klasika</li>
  <li class="label-chip">smažené</li>
</ul>
```

```css
/* Notion "Štítky" → one <li class="label-chip"> each. Rendered as a quiet kicker line with dot separators. */
.labels { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .3rem 0; }
.label-chip { font-size: .9rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tint-ink); }
.label-chip + .label-chip::before { content: "·"; margin: 0 .6rem; }
```

### 7.9 Info strip  `@c:meta`

Čas / Porce / Obtížnost / Spotřebiče. Drop an item the recipe does not have.

```html
<ul class="meta" aria-label="Základní údaje">
  <li><span class="k">Čas</span><span class="v" data-sync="total_time">40 min</span><span class="sub">15 min příprava + 25 min tepelná úprava</span></li>
  <li><span class="k">Porce</span><span class="v">4</span><span class="sub">porce</span></li>
  <li><span class="k">Obtížnost</span>
    <!-- @c:difficulty -->
    <span class="difficulty" data-sync="difficulty" data-value="easy"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span><span class="difficulty-text">Snadné</span></span>
    <!-- /@c:difficulty -->
  </li>
  <li class="meta-appliances"><span class="k">Spotřebiče</span>
    <!-- @c:appliances -->
    <ul class="appliances" data-sync="appliances">
      <li class="appliance" data-value="gas-stove">Plynový sporák</li>
      <li class="appliance" data-value="air-fryer">Horkovzdušná fritéza</li>
    </ul>
    <!-- /@c:appliances -->
  </li>
</ul>
```

```css
.meta { list-style: none; margin: calc(var(--gap) * 1.2) 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--ink); border-bottom: 1px solid var(--line); }
.meta > li { padding: 1rem 1rem 1.1rem 0; }
.meta > li + li { padding-left: 1rem; border-left: 1px solid var(--line); }
.meta .k { display: block; font-size: .85rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.meta .v { display: block; font-family: var(--font-display); font-size: 2.1rem; line-height: 1.15; }
.meta .sub { display: block; font-size: .95rem; line-height: 1.35; color: var(--muted); }
.meta .meta-appliances { grid-column: 1 / -1; border-left: 0; padding-left: 0; border-top: 1px solid var(--line); display: flex; flex-wrap: wrap; align-items: center; gap: .5rem 1.2rem; }
@media (min-width: 1000px) { .meta { grid-template-columns: 1fr 1fr 1fr 2fr; } .meta .meta-appliances { grid-column: auto; border-top: 0; padding-left: 1rem; border-left: 1px solid var(--line); display: block; } }
```

### 7.10 Difficulty badge  `@c:difficulty`

`data-sync="difficulty"` with `data-value="easy|medium|hard"`.

```html
<span class="difficulty" data-sync="difficulty" data-value="easy"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span><span class="difficulty-text">Snadné</span></span>
```

```css
/* data-value: easy | medium | hard → 1 / 2 / 3 filled bars. Text: Snadné / Střední / Náročné. */
.difficulty { display: inline-flex; align-items: center; gap: .6rem; margin-top: .35rem; font-family: var(--font-display); font-size: 1.6rem; line-height: 1.1; }
.pips { display: inline-flex; align-items: flex-end; gap: 3px; }
.pips i { width: 7px; border-radius: 2px; background: var(--line-strong); }
.pips i:nth-child(1) { height: 10px; } .pips i:nth-child(2) { height: 16px; } .pips i:nth-child(3) { height: 22px; }
.difficulty[data-value="easy"] .pips i:nth-child(-n+1), .difficulty[data-value="medium"] .pips i:nth-child(-n+2), .difficulty[data-value="hard"] .pips i { background: var(--ink); }
```

### 7.11 Appliance badges  `@c:appliances`

`data-sync="appliances"`; icon picked by `data-value`.

```html
<ul class="appliances" data-sync="appliances">
  <li class="appliance" data-value="gas-stove">Plynový sporák</li>
  <li class="appliance" data-value="air-fryer">Horkovzdušná fritéza</li>
</ul>
```

```css
/* data-value keys: gas-stove | induction | oven | air-fryer | microwave | blender (icon from the icons block). */
.appliances { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .5rem; }
.appliance { display: inline-flex; align-items: center; gap: .5rem; min-height: 44px; padding: .35rem 1rem .35rem .75rem; border: 1px solid var(--line-strong); border-radius: 999px; background: var(--surface); font-size: 1.05rem; font-weight: 600; }
.appliance::before { width: 1.35em; height: 1.35em; color: var(--tint-ink); }
.meta-appliances .k { margin-right: .2rem; }
```

### 7.12 Family block ("U nás doma")  `@c:family`

Wrapper for ratings + notes, placed between the info strip and the ingredients.

```html
<section class="family" aria-labelledby="h-family">
  <h2 class="section-title" id="h-family">U nás doma</h2>
  <div class="family-grid">
    <!-- @c:ratings -->
    <div class="card ratings-card">
      <h3 class="card-title">Jak komu chutná</h3>
      <ul class="ratings">
        <li><span class="who">Braňo</span><span class="rating" data-sync="rating_brano" data-value="loved">Chutná</span></li>
        <li><span class="who">Zuzka</span><span class="rating" data-sync="rating_zuzka" data-value="ok">Ujde</span></li>
        <li><span class="who">Andrej</span><span class="rating" data-sync="rating_andrej" data-value="loved">Chutná</span></li>
        <li><span class="who">Tomáš</span><span class="rating" data-sync="rating_tomas" data-value="disliked">Nechutná</span></li>
        <li><span class="who">Lukáš</span><span class="rating" data-sync="rating_lukas" data-value="">Zatím nehodnotil</span></li>
      </ul>
      <p class="last-prepared">Naposledy vařeno <time data-sync="last_prepared" datetime="2026-10-18">18. 10. 2026</time></p>
    </div>
    <!-- /@c:ratings -->
    <!-- @c:notes -->
    <div class="card notes-card">
      <h3 class="card-title">Poznámky</h3>
      <div class="notes" data-sync="notes">
        <p>Ukázková poznámka z Notionu: příště dvojitou dávku — řízky zmizely za 10 minut. Tomášovi bez pepře.</p>
      </div>
    </div>
    <!-- /@c:notes -->
  </div>
</section>
```

```css
.family { margin-top: calc(var(--gap) * 1.8); }
.family-grid { display: grid; gap: var(--gap); }
@media (min-width: 760px) { .family-grid { grid-template-columns: 1.1fr 1fr; } }
```

### 7.13 Ratings block  `@c:ratings`

Five people + last prepared. Loved / OK / Disliked → Chutná / Ujde / Nechutná.

```html
<div class="card ratings-card">
  <h3 class="card-title">Jak komu chutná</h3>
  <ul class="ratings">
    <li><span class="who">Braňo</span><span class="rating" data-sync="rating_brano" data-value="loved">Chutná</span></li>
    <li><span class="who">Zuzka</span><span class="rating" data-sync="rating_zuzka" data-value="ok">Ujde</span></li>
    <li><span class="who">Andrej</span><span class="rating" data-sync="rating_andrej" data-value="loved">Chutná</span></li>
    <li><span class="who">Tomáš</span><span class="rating" data-sync="rating_tomas" data-value="disliked">Nechutná</span></li>
    <li><span class="who">Lukáš</span><span class="rating" data-sync="rating_lukas" data-value="">Zatím nehodnotil</span></li>
  </ul>
  <p class="last-prepared">Naposledy vařeno <time data-sync="last_prepared" datetime="2026-10-18">18. 10. 2026</time></p>
</div>
```

```css
/* data-value: loved (Chutná) | ok (Ujde) | disliked (Nechutná) | "" (Zatím nehodnotil/a). The word is always shown — never colour only. */
.ratings { list-style: none; margin: 0; padding: 0; }
.ratings li { display: flex; justify-content: space-between; align-items: center; gap: .8rem; min-height: 52px; border-bottom: 1px solid var(--line); }
.ratings li:last-child { border-bottom: 0; }
.who { font-family: var(--font-display); font-size: 1.4rem; }
.rating { display: inline-flex; align-items: center; gap: .45rem; font-size: 1.05rem; font-weight: 650; color: var(--muted); }
.rating::before { width: 1.3em; height: 1.3em; }
.rating[data-value="loved"] { color: var(--red); }
.rating[data-value="ok"] { color: #6c5400; }
.rating[data-value="disliked"] { color: #3c4a57; }
.overall .rating { padding: .3rem .9rem .3rem .65rem; border-radius: 999px; background: var(--surface); }
.last-prepared { margin: .9rem 0 0; font-size: 1rem; color: var(--muted); }
.last-prepared time { color: var(--ink); font-weight: 700; }
```

### 7.14 Notes block  `@c:notes`

`data-sync="notes"` — Notion "Poznámky".

```html
<div class="card notes-card">
  <h3 class="card-title">Poznámky</h3>
  <div class="notes" data-sync="notes">
    <p>Ukázková poznámka z Notionu: příště dvojitou dávku — řízky zmizely za 10 minut. Tomášovi bez pepře.</p>
  </div>
</div>
```

```css
/* Free text from Notion "Poznámky"; the sync writes <p> paragraphs inside [data-sync="notes"]. */
.notes-card { background: var(--tint); border-color: transparent; }
.notes-card .card-title { color: var(--tint-ink); }
.notes { font-family: var(--font-display); font-size: clamp(1.3rem, 1.05rem + .8vw, 1.55rem); line-height: 1.45; }
.notes p { margin: 0 0 .6rem; } .notes p:last-child { margin: 0; }
```

### 7.15 Ingredient checklist  `@c:ingredients`

One `<li><button aria-pressed="false">` per source line, quantity wrapped in `.qty`. Text verbatim.

```html
<section class="ingredients" aria-labelledby="h-ingr">
  <h2 class="section-title" id="h-ingr">Suroviny <small>pro 4 porce</small></h2>
  <div class="card">
    <ul class="checklist" data-checklist>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text"><span class="qty">500 g</span> kuřecího masa (prsní nebo stehenní)</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">sůl</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">mletý pepř</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">hladká mouka</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">strouhanka</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text"><span class="qty">2</span> vejce</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text"><span class="qty">100 ml</span> mléka</span></button></li>
      <li><button type="button" aria-pressed="false"><span class="box"></span><span class="text">olej na smažení</span></button></li>
    </ul>
    <div class="list-tools">
      <span>Ťukněte na surovinu, kterou máte připravenou.</span>
      <button type="button" class="btn" data-reset>Odškrtnout vše</button>
    </div>
  </div>
</section>
```

```css
.checklist { list-style: none; margin: 0; padding: 0; display: grid; }
@media (min-width: 640px) and (max-width: 999px) { .checklist { grid-template-columns: 1fr 1fr; column-gap: 1.6rem; } }
.checklist li { border-bottom: 1px solid var(--line); }
.checklist button { all: unset; box-sizing: border-box; cursor: pointer; width: 100%; display: flex; align-items: center; gap: .9rem; padding: .7rem .2rem; min-height: 60px;
  font-size: var(--fs-body); line-height: 1.3; -webkit-tap-highlight-color: transparent; }
.checklist button:focus-visible { outline: 3px solid var(--pine); border-radius: 8px; }
.checklist .box { flex: none; width: 32px; height: 32px; border-radius: 9px; border: 2px solid var(--ink); display: grid; place-items: center; background: var(--surface); transition: background .15s; }
.checklist .box::after { content: ""; width: 20px; height: 20px; background: #fff; -webkit-mask: var(--i-check) center / contain no-repeat; mask: var(--i-check) center / contain no-repeat; opacity: 0; }
.checklist .qty { font-weight: 750; font-variant-numeric: tabular-nums; white-space: nowrap; }
.checklist [aria-pressed="true"] .box { background: var(--pine); border-color: var(--pine); }
.checklist [aria-pressed="true"] .box::after { opacity: 1; }
.checklist [aria-pressed="true"] .text { color: var(--muted); text-decoration: line-through; text-decoration-thickness: 1.5px; }
.list-tools { display: flex; justify-content: space-between; align-items: center; gap: .6rem; flex-wrap: wrap; margin-top: 1rem; font-size: 1rem; color: var(--muted); }
```

### 7.16 Steps with "Hotovo" buttons  `@c:steps`

One `<li class="step">` per source step; numbering is automatic. Optional `<h3>`, optional `<figure class="step-photo">`, keep the `.step-done` button last.

```html
<section class="method" aria-labelledby="h-steps">
  <h2 class="section-title" id="h-steps">Postup přípravy</h2>
  <ol class="steps" data-steps>
    <li class="step"><div class="step-body">
      <h3>Příprava masa</h3>
      <p>Maso nakrájíme na plátky. Poté ho z obou stran osolíme a opepříme.</p>
      <figure class="step-photo">
        <img src="data:image/jpeg;base64,…" alt="Naklepané plátky masa a palička na maso" loading="lazy" width="960" height="640">
        <figcaption>Náhled videa ze zdroje: „Jak krájet maso na řízky“</figcaption>
      </figure>
      <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>
    </div></li>
    <li class="step"><div class="step-body">
      <h3>Příprava obalovacích směsí</h3>
      <p>Připravíme 3 hluboké talíře. Do prvního vsypeme hladkou mouku, do druhého rozklepneme dvě nevařená vajíčka bez skořápky, přidáme mléko, špetku soli, trochu pepře a pořádně promícháme. Do třetího talíře nasypeme strouhanku.</p>
      <!-- @c:sidenote -->
      <aside class="sidenote" data-origin="ours">
        <span class="sidenote-label">Na okraj · náš doplněk</span>
        <p>Tomuhle pořadí (mouka → vejce → strouhanka) se říká <b>trojobal</b>.</p>
      </aside>
      <!-- /@c:sidenote -->
      <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>
    </div></li>
    <li class="step"><div class="step-body">
      <h3>Obalování řízků</h3>
      <p>Maso důkladně obalíme z obou stran v prvním talíři, pak ve druhém a nakonec ve třetím.</p>
      <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>
    </div></li>
    <li class="step"><div class="step-body">
      <h3>Dvojité obalování</h3>
      <p>Pro lepší konzistenci obalu je dobré postupovat tak, že obalíme v prvním, pak v druhém, pak zase prvním, zase v druhém a nakonec ve třetím talíři.</p>
      <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>
    </div></li>
    <li class="step"><div class="step-body">
      <h3>Smažení</h3>
      <p>Na pánev nalijeme dostatečné množství oleje, rozpálíme ho a řízky osmažíme.</p>
      <!-- @c:our-inline -->
      <p class="our-inline"><span class="our-mark">Náš tip</span> Bez pánve to jde i v horkovzdušné fritéze — postup je níže v tipu „Varianta · horkovzdušná fritéza“.</p>
      <!-- /@c:our-inline -->
      <!-- @c:warning -->
      <div class="warning" role="note">
        <span class="warning-label">Pozor · náš doplněk</span>
        <p>Rozpálený olej může vzplanout. Nikdy ho nehaste vodou — pánev přikryjte pokličkou a vypněte plyn.</p>
      </div>
      <!-- /@c:warning -->
      <button type="button" class="btn step-done" aria-pressed="false">Hotovo</button>
    </div></li>
  </ol>
</section>
```

```css
.steps { list-style: none; margin: 0; padding: 0; counter-reset: step; }
.step { counter-increment: step; display: grid; grid-template-columns: clamp(3.4rem, 2.6rem + 2.4vw, 5rem) 1fr; gap: 0 clamp(.8rem, .4rem + 1.4vw, 1.6rem); padding: 1.4rem 0 1.6rem; border-bottom: 1px solid var(--line); }
.step:first-child { padding-top: .4rem; }
.step::before { content: counter(step, decimal-leading-zero); font-family: var(--font-display); font-size: clamp(2.4rem, 1.8rem + 2vw, 3.4rem); line-height: .95; color: var(--tint-ink);
  font-variant-numeric: lining-nums; }
.step-body { min-width: 0; }
.step h3 { font-size: clamp(1.45rem, 1.15rem + 1vw, 1.9rem); margin-bottom: .4rem; }
.step p { font-size: var(--fs-step); line-height: 1.55; margin: 0; max-width: 42ch; }
.step-photo { margin: 1.1rem 0 0; max-width: 560px; }
.step-photo img { width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; border-radius: 10px; }
.step-photo figcaption { font-size: .92rem; color: var(--muted); padding-top: .45rem; }
.step-done { margin-top: 1rem; min-width: 8.5rem; }
.step.is-done::before { content: "✓"; color: var(--pine); }
.step.is-done h3, .step.is-done p, .step.is-done aside, .step.is-done .warning { opacity: .45; }
```

### 7.17 Our inline note (inside a step)  `@c:our-inline`

Short addition of ours placed right after the original paragraph it relates to.

```html
<p class="our-inline"><span class="our-mark">Náš tip</span> Bez pánve to jde i v horkovzdušné fritéze — postup je níže v tipu „Varianta · horkovzdušná fritéza“.</p>
```

```css
/* OUR addition inside the original text flow. Rule for the whole design: our additions = DASHED pine outline + "Náš tip" tag with a plus. */
.step p.our-inline, .our-inline { margin: 1rem 0 0; padding: .7rem 1rem; border: 1.5px dashed var(--pine); border-radius: 12px; background: var(--surface); font-size: 1.15rem; line-height: 1.5; max-width: 48ch; }
.our-mark { display: inline-flex; align-items: center; gap: .3rem; margin-right: .4rem; padding: .1rem .6rem .1rem .45rem; border-radius: 6px; background: var(--pine); color: #fff;
  font-size: .78rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; vertical-align: .12em; }
.our-mark::before { content: ""; width: .9em; height: .9em; background: currentColor; -webkit-mask: var(--i-plus) center / contain no-repeat; mask: var(--i-plus) center / contain no-repeat; }
```

### 7.18 Warning  `@c:warning`

Safety note. If it is ours, the label says "Pozor · náš doplněk"; if from the source: "Pozor".

```html
<div class="warning" role="note">
  <span class="warning-label">Pozor · náš doplněk</span>
  <p>Rozpálený olej může vzplanout. Nikdy ho nehaste vodou — pánev přikryjte pokličkou a vypněte plyn.</p>
</div>
```

```css
.warning { margin: 1rem 0 0; padding: .75rem 1rem .8rem 3.3rem; position: relative; border-left: 4px solid var(--red); border-radius: 0 12px 12px 0; background: #fbeeec; max-width: 48ch; }
.warning::before { content: ""; position: absolute; left: .95rem; top: .9rem; width: 1.55rem; height: 1.55rem; background: var(--red); -webkit-mask: var(--i-warning) center / contain no-repeat; mask: var(--i-warning) center / contain no-repeat; }
.warning-label { display: block; font-size: .8rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; color: var(--red); }
.step .warning p, .warning p { margin: .15rem 0 0; font-size: 1.15rem; line-height: 1.5; }
```

### 7.19 Side note  `@c:sidenote`

Neutral explanation. `data-origin="ours"` (label "Na okraj · náš doplněk") or `data-origin="source"` (label "Na okraj").

```html
<aside class="sidenote" data-origin="ours">
  <span class="sidenote-label">Na okraj · náš doplněk</span>
  <p>Tomuhle pořadí (mouka → vejce → strouhanka) se říká <b>trojobal</b>.</p>
</aside>
```

```css
/* Neutral explanation, margin-note style. data-origin="ours" → dashed pine outline; "source" → plain hairline. */
.sidenote { margin: 1rem 0 0; padding: .6rem 1rem; border-left: 1px solid var(--ink); max-width: 48ch; }
.sidenote[data-origin="ours"] { border: 1.5px dashed var(--pine); border-radius: 12px; background: var(--surface); }
.sidenote-label { display: block; font-size: .8rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; color: var(--pine); }
.step .sidenote p, .sidenote p { margin: .1rem 0 0; font-size: 1.15rem; line-height: 1.5; color: var(--ink); }
```

### 7.20 Original-author / source tip  `@c:tip-source`

Tip copied verbatim from the source (or a linked page of the same site); always with `.tip-source` link. `.facts` is optional.

```html
<aside class="tip tip--source">
  <span class="tip-label">Tip ze zdroje</span>
  <h3>Varianta · horkovzdušná fritéza</h3>
  <div class="facts">
    <span class="fact"><b>180 °C</b>teplota</span>
    <span class="fact"><b>20 min</b>doba</span>
    <span class="fact"><b>v ½</b>obrátit</span>
  </div>
  <p>Připravené, již obalené řízky nejprve potřete z obou stran olejem – použít můžete mašlovačku nebo olej ve spreji přímo k tomuto určený.</p>
  <p>Omaštěné řízky vložte do horkovzdušné fritézy a smažte při 180 °C po dobu 20 minut. V polovině doby je obraťte, aby byly zlatavé a křupavé z obou stran.</p>
  <p class="tip-source">Zdroj: <a href="https://www.toprecepty.cz/tipy-triky/jak-pripravit-rizek-v-horkovzdusne-friteze/" rel="noopener">Toprecepty.cz — Jak udělat řízek v horkovzdušné fritéze?</a> (Kristýna Anna Vondálová)</p>
</aside>
```

```css
.tips { display: grid; gap: var(--gap); margin-top: calc(var(--gap) * 2); }
@media (min-width: 1000px) { .tips { grid-template-columns: 1fr 1fr; align-items: start; } }
.tip { background: var(--tint); border-radius: var(--radius); padding: clamp(1.2rem, .8rem + 1.2vw, 2rem); }
.tip-label { display: flex; align-items: center; gap: .6rem; font-size: .85rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tint-ink); margin-bottom: .6rem; }
.tip-label::after { content: ""; flex: 1; height: 1px; background: currentColor; opacity: .35; }
.tip h3 { font-size: clamp(1.6rem, 1.25rem + 1.1vw, 2.1rem); margin-bottom: .8rem; }
.tip p { margin: 0 0 .7rem; }
.tip .facts { display: grid; grid-template-columns: repeat(3, 1fr); margin: .2rem 0 1.1rem; border-top: 1px solid color-mix(in srgb, var(--tint-ink) 30%, transparent); border-bottom: 1px solid color-mix(in srgb, var(--tint-ink) 30%, transparent); }
.tip .fact { padding: .6rem .2rem; font-size: .95rem; color: var(--ink); }
.tip .fact + .fact { padding-left: .9rem; border-left: 1px solid color-mix(in srgb, var(--tint-ink) 30%, transparent); }
.tip .fact b { display: block; font-family: var(--font-display); font-weight: 500; font-size: 1.9rem; line-height: 1.1; }
.tip .tip-source { font-size: .95rem; color: var(--ink); margin: 1rem 0 0; }
```

### 7.21 OUR added tip ("Náš tip")  `@c:tip-ours`

Appliance substitutions, temperatures, etc. Always ends with "Doplněno námi — není součástí původního receptu." `.big` is optional.

```html
<aside class="tip tip--ours">
  <span class="tip-label">Náš tip</span>
  <h3>Teploměr do středu řízku</h3>
  <p class="big">74&nbsp;°C</p>
  <p>Kuřecí maso je hotové, když jádro (nejsilnější místo) dosáhne <strong>74&nbsp;°C</strong>. Teploměr zapíchněte z boku do středu plátku.</p>
  <p class="tip-source">Doplněno námi — není součástí původního receptu.</p>
</aside>
```

```css
.tip--ours { background: var(--surface); border: 1.5px dashed var(--pine); }
.tip--ours .tip-label { color: var(--pine); }
.tip--ours .tip-label::before { content: ""; width: 1.1em; height: 1.1em; background: currentColor; -webkit-mask: var(--i-plus) center / contain no-repeat; mask: var(--i-plus) center / contain no-repeat; }
.tip .big { font-family: var(--font-display); font-size: clamp(3rem, 2.2rem + 3vw, 4.4rem); line-height: 1; margin-bottom: .6rem; color: var(--pine); }
.tip--ours .tip-source { color: var(--pine); font-weight: 650; padding-top: .8rem; border-top: 1px dashed var(--pine); }
```

### 7.22 Wake lock + "Začít znovu"  `@c:toolbar`

Wake-lock button stays `hidden`; the script reveals it when supported and not framed.

```html
<div class="toolbar">
  <button type="button" class="btn" data-wakelock hidden aria-pressed="false">☀ Nezhasínat displej</button>
  <button type="button" class="btn" data-reset-all>↺ Začít znovu</button>
</div>
```

```css
.toolbar { display: flex; gap: .8rem; flex-wrap: wrap; margin-top: calc(var(--gap) * 1.5); }
.toolbar .btn { min-height: 56px; padding-inline: 1.5rem; font-size: 1.1rem; }
```

### 7.23 Source credit (bottom)  `@c:source-foot`

Second credit + the "our additions" disclaimer + back link.

```html
<footer class="source-foot">
  <div class="wrap">
    <p><strong>Zdroj receptu:</strong> <a href="https://www.toprecepty.cz/recept/23122-kureci-rizek/" rel="noopener">Kuřecí řízek na Toprecepty.cz</a> (autor blazena.blazkova). Fotografie © Toprecepty.cz.</p>
    <p><strong>Varianta pro fritézu:</strong> <a href="https://www.toprecepty.cz/tipy-triky/jak-pripravit-rizek-v-horkovzdusne-friteze/" rel="noopener">Toprecepty.cz — tipy a triky</a>.</p>
    <p class="foot-ours">Části označené <b>Náš tip</b> / <b>náš doplněk</b> jsme doplnili sami, v původním receptu nejsou.</p>
    <p><a class="foot-back" href="../index.html">← Zpět na všechny recepty</a></p>
  </div>
</footer>
```

```css
.source-foot { margin-top: calc(var(--gap) * 2.2); border-top: 1px solid var(--ink); }
.source-foot .wrap { padding-block: 1.4rem 2.6rem; font-size: 1.02rem; color: var(--muted); }
.source-foot p { margin: .35rem 0; } .source-foot strong { color: var(--ink); }
.foot-ours { color: var(--pine) !important; }
@media print { .frame-open, .toolbar, .list-tools, .step-done, .backlink { display: none !important; } .hero, .topbar { background: none; box-shadow: none; } }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
```

### 7.24 iPhone & safe-area layer  `@c:phone`

Responsive overrides for phones (< 560 px) plus safe-area insets and overflow guard. Always paste it **last** in `<style>`; it has no markup of its own. See §5a.

```css
/* iPhone + safe-area layer — keep it LAST in the <style> so it wins */
html, body { overflow-x: clip; }   /* nothing may ever cause sideways scroll */
h1, h2, h3 { text-wrap: balance; }
body { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }
html.is-framed .frame-open { padding-top: max(.5rem, env(safe-area-inset-top)); }
@media (max-width: 999px) { .meta { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (min-width: 1000px) { .meta { grid-template-columns: repeat(3, minmax(0, 1fr)) minmax(0, 2fr); } }
.meta .v, .tip .fact b { white-space: nowrap; }
.credit a, .source-foot a, .tip-source a { padding-block: .35em; }        /* bigger hit area, same layout */
.foot-back { display: inline-flex; align-items: center; min-height: 44px; }
@media (max-width: 559px) {                    /* iPhone portrait (375–430 px) */
  .meta { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
  .meta > li:first-child { grid-column: 1 / -1; }
  .rating { white-space: nowrap; }
  .tip .fact b { font-size: 1.6rem; }
  .credit { font-size: .9rem; }
}
@media (max-width: 559px) {
  .meta > li:first-child { border-bottom: 1px solid var(--line); }
  .meta > li:nth-child(2) { border-left: 0; padding-left: 0; }
  .tip .fact + .fact { padding-left: .6rem; }
}
```

## 8. New recipe page — checklist

1. Copy this design's `kureci-rizek.html` → `recipes/<slug>.html` (keeps the full `<style>` and `<script>`).
2. Set `<title>`, the header comment, `data-recipe-id`, `data-tint` (§3 rule).
3. Replace content component by component from §7, keeping `data-sync` attributes and `@c:` comments.
4. Images: resize to ≤ 1000 px wide, JPEG q≈75, embed as `data:image/jpeg;base64,…` (≈ 60–110 kB each). Keep total page ≲ 600 kB; if a recipe has many photos, keep the hero + at most 3 step photos.
5. Verify: open with no network → only `fonts/*.woff2` may be requested; screenshot at 820×1180 (iPad portrait), 1180×820 (iPad landscape) and 393×852 + 375×812 with mobile emulation (iPhone), check `document.documentElement.scrollWidth === innerWidth` and every tint-coloured element is legible; embed in an iframe → fullscreen bar visible, wake lock hidden.
