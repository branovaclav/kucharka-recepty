# Rodinná kuchařka — canonical cookbook (design A „Smalt & puntík“)

**This file is the single source of truth for the official recipe site.**
Live site: https://branovaclav.github.io/kucharka-recepty/ · design previews (frozen, do not edit): `/designs/`.

It is the design-A cookbook (sections 1–8 below, unchanged from `designs/smalt`, kept as the component catalogue)
**plus the "Official site" part (sections O1–O9 at the end), which wins wherever they differ.**
Production CSS/JS lives in `themes/smalt/{fonts,design,index}.css` + `themes/_shared/{tints,icons,official}.css, script.js`;
the markup is produced by `tools/build.py` from `content/<slug>.md`. If a snippet here and those files disagree, the files win.
Sections 1–8 still mention the old "sync script patching `data-sync` regions". Nothing patches HTML today: every page is
regenerated (see O1/O6), and the `data-sync` attributes remain as stable hooks for CSS and tests.

---


*Czech enamelware kitchen: a tinted enamel body, cobalt rims, tomato accents, polka dots and hard offset shadows like a printed kitchen card.*
The existing prototype look, preserved and converted to the standalone single-file format.

Sample: [`kureci-rizek.html`](kureci-rizek.html) · Screenshots: `preview.png` (full page, chicken), `tints.png` (all 6 tints).

## 1. Look & tokens

| token | value | use |
|---|---|---|
| `--tint` | from `data-tint` (§3) | page background = the colour of the enamel pot |
| `--paper` | `#fffaf0` | card faces, top bar, footer |
| `--cobalt` | `#183a74` | 3 px rims, headings, buttons, hard shadows `6px 6px 0` |
| `--ink` | `#14223d` | body text |
| `--tomato` / `--tomato-ink` | `#c8402a` / `#a8321f` | accents, **our additions** (dashed tomato rim), small red labels |
| `--mustard` | `#f0b93a` | "Tip ze zdroje" label, focus ring |
| `--sage` | `#4f7a55` | ticked / done |
| `--dot` | `#c9d6ee` | dashed dividers, sidenote dots |
| `--radius` | `22px` | cards; chips are full pills |

Typography: **Fraunces** 600–900 (SOFT 100, WONK 1 baked in) for headings, numbers and values; **Atkinson Hyperlegible**
400/700 for everything else. Labels: 0.8–0.9 rem uppercase, letter-spacing .12em.
Motifs: polka-dot band (`.source-foot::before`, or `.dots` helper), offset shadows, round step badges with a tomato shadow.

**Our-addition rule:** dashed tomato rim + tomato "＋ Náš tip" pill. Source content always has solid cobalt rims.

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
  <meta name="theme-color" content="#183a74">
  <title>Kuřecí řízek · Rodinná kuchařka</title>   <!-- sync: title + " · Rodinná kuchařka" -->
  <!-- DESIGN: smalt · RECIPE: <slug> | source: <url> | notion-page: <id> -->
  <script>/* Embedded (e.g. Notion iframe)? Mark early to avoid layout flash. */
  (function(){var f;try{f=window.self!==window.top}catch(e){f=true}if(f)document.documentElement.classList.add('is-framed');})();</script>
  <style>/* fonts → tints → icons → base → components (copy whole block) */</style>
</head>
<body data-tint="chicken" data-design="smalt">
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
@font-face { font-family: "Fraunces"; src: url("fonts/fraunces.woff2") format("woff2"); font-weight: 600 900; font-display: swap; }
@font-face { font-family: "Atkinson"; src: url("fonts/atkinson-regular.woff2") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "Atkinson"; src: url("fonts/atkinson-bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
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
/* ==== Smalt & puntík — Czech enamelware: tinted enamel body, cobalt rims, tomato accents, polka dots,
   3 px rims with hard offset shadows (no blur). ==== */
:root {
  --paper: #fffaf0;   /* card face (enamel white) */
  --cobalt: #183a74;  /* rims, headings, buttons */
  --ink: #14223d;     /* body text (>= 11.9:1 on every tint) */
  --tomato: #c8402a;  /* accent, "Náš tip" */
  --tomato-ink: #a8321f; /* tomato for small text on light (5.6:1 on paper) */
  --mustard: #f0b93a; /* source tip label, focus ring */
  --sage: #4f7a55;    /* done / checked */
  --dot: #c9d6ee;     /* dashed dividers */
  --font-display: "Fraunces", Georgia, "Times New Roman", serif;
  --font-body: "Atkinson", "Atkinson Hyperlegible", "Segoe UI", system-ui, -apple-system, sans-serif;
  --fs-body: clamp(1.2rem, 0.95rem + 0.9vw, 1.45rem);
  --fs-step: clamp(1.3rem, 1rem + 1.1vw, 1.65rem);
  --fs-h1: clamp(2.6rem, 1.6rem + 4.2vw, 4.6rem);
  --fs-h2: clamp(1.8rem, 1.3rem + 1.8vw, 2.5rem);
  --rim: 3px solid var(--cobalt);
  --radius: 22px;
  --shadow: 6px 6px 0 var(--cobalt);
  --shadow-sm: 4px 4px 0 var(--cobalt);
  --gap: clamp(1rem, 0.6rem + 1.6vw, 2rem);
  --maxw: 1240px;
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { margin: 0; background: var(--tint); color: var(--ink); font-family: var(--font-body); font-size: var(--fs-body); line-height: 1.55; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; display: block; }
a { color: var(--cobalt); text-decoration-thickness: 2px; text-underline-offset: 3px; }
:focus-visible { outline: 4px solid var(--mustard); outline-offset: 3px; border-radius: 6px; }
.wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 var(--gap); }
h1, h2, h3 { font-family: var(--font-display); color: var(--cobalt); line-height: 1.05; margin: 0; }
.section-title { font-size: var(--fs-h2); font-weight: 800; display: flex; align-items: baseline; gap: .6rem; flex-wrap: wrap; margin-bottom: 1rem; }
.section-title small { font-family: var(--font-body); font-size: 1rem; font-weight: 700; color: var(--tomato-ink); }
.card { background: var(--paper); border: var(--rim); border-radius: var(--radius); box-shadow: var(--shadow); padding: clamp(1rem, .7rem + 1vw, 1.6rem); }
.card-title { font-size: 1.45rem; font-weight: 800; margin-bottom: .7rem; }
.btn { font: inherit; font-size: 1.05rem; font-weight: 700; cursor: pointer; color: var(--cobalt); background: var(--paper);
  border: 2px solid var(--cobalt); border-radius: 999px; padding: .6rem 1.2rem; min-height: 48px; box-shadow: 3px 3px 0 var(--cobalt); }
.btn:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 var(--cobalt); }
.btn[aria-pressed="true"] { background: var(--cobalt); color: var(--paper); }
/* Polka-dot enamel band (signature motif) */
.dots { background-color: var(--cobalt);
  background-image: radial-gradient(circle, var(--paper) 0 5px, transparent 5.5px), radial-gradient(circle, var(--paper) 0 5px, transparent 5.5px);
  background-size: 34px 34px; background-position: 0 0, 17px 17px; }
.cook { display: grid; gap: calc(var(--gap) * 1.4); margin-top: calc(var(--gap) * 1.6); }
@media (min-width: 1000px) { .cook { grid-template-columns: minmax(320px, .8fr) 1.6fr; align-items: start; } .cook .ingredients { position: sticky; top: 1rem; } }
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
html.is-framed .frame-open { display: flex; justify-content: center; padding: .45rem var(--gap); background: var(--cobalt); border-bottom: var(--rim); position: sticky; top: 0; z-index: 10; }
.btn-fullscreen { display: inline-flex; align-items: center; gap: .4rem; min-height: 48px; text-decoration: none; background: var(--tomato); color: var(--paper);
  border: 3px solid var(--paper); border-radius: 999px; padding: .45rem 1.3rem; font-weight: 700; font-size: 1.1rem; box-shadow: 3px 3px 0 rgba(0,0,0,.35); }
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
.topbar { border-bottom: var(--rim); background: var(--paper); }
.topbar .wrap { display: flex; align-items: center; justify-content: space-between; gap: .75rem 1rem; flex-wrap: wrap; padding-block: .7rem; }
.backlink { font-family: var(--font-display); font-weight: 800; font-size: 1.35rem; color: var(--cobalt); text-decoration: none; display: inline-flex; align-items: center; gap: .5rem; min-height: 44px; }
.backlink::before { content: ""; width: 1.4rem; height: 1.4rem; border-radius: 50%; background: var(--tomato); box-shadow: inset 0 0 0 4px var(--paper), 0 0 0 3px var(--cobalt); }
.credit { font-size: .95rem; line-height: 1.35; background: var(--paper); border: 2px solid var(--cobalt); border-radius: 18px; padding: .4rem .95rem; margin: 0; }
.credit a { font-weight: 700; }
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
.hero { padding-top: var(--gap); display: grid; gap: var(--gap); align-items: center; }
.hero-photo { margin: 0; border: var(--rim); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); background: var(--paper); aspect-ratio: 4 / 3; }
.hero-photo img { width: 100%; height: 100%; object-fit: cover; }
.hero h1 { font-size: var(--fs-h1); font-weight: 800; letter-spacing: -.01em; margin-top: .5rem; }
.lede { margin: 1rem 0 0; max-width: 40ch; }
.hero-ratings { display: flex; flex-wrap: wrap; gap: .6rem 1.2rem; align-items: center; margin-top: 1rem; }
.hero-ratings p { margin: 0; }
.overall { display: inline-flex; align-items: center; gap: .5rem; font-weight: 700; }
.overall-k { font-size: .8rem; letter-spacing: .12em; text-transform: uppercase; color: var(--cobalt); }
.src-rating { font-weight: 700; }
.stars { color: var(--tomato); letter-spacing: .1em; font-size: 1.2em; line-height: 1; }
.src-rating small { font-weight: 400; font-size: .85em; }
@media (min-width: 1000px) { .hero { grid-template-columns: 1.1fr 1fr; } .hero-photo { transform: rotate(-1.2deg); } }
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
/* Notion "Štítky" → one <li class="label-chip"> each, lowercase as in Notion. */
.labels { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .4rem; }
.label-chip { font-size: .9rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--paper); background: var(--cobalt); padding: .25rem .8rem; border-radius: 999px; }
.label-chip:first-child { background: var(--tomato); }
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
.meta { list-style: none; margin: calc(var(--gap) * 1.3) 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr);
  border: var(--rim); border-radius: var(--radius); overflow: hidden; background: var(--paper); box-shadow: var(--shadow-sm); }
.meta > li { padding: .9rem 1.1rem; border-right: 2px dashed var(--dot); }
.meta > li:nth-child(3) { border-right: 0; }
.meta .k { display: block; font-size: .8rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--tomato-ink); }
.meta .v { display: block; font-family: var(--font-display); font-weight: 700; font-size: 1.6rem; color: var(--cobalt); line-height: 1.15; }
.meta .sub { display: block; font-size: .9rem; line-height: 1.3; }
.meta .meta-appliances { grid-column: 1 / -1; border-right: 0; border-top: 2px dashed var(--dot); display: flex; flex-wrap: wrap; align-items: center; gap: .3rem 1rem; }
@media (min-width: 1000px) { .meta { grid-template-columns: 1fr 1fr 1fr 2fr; } .meta > li:nth-child(3) { border-right: 2px dashed var(--dot); } .meta .meta-appliances { grid-column: auto; border-top: 0; display: block; } }
```

### 7.10 Difficulty badge  `@c:difficulty`

`data-sync="difficulty"` with `data-value="easy|medium|hard"`.

```html
<span class="difficulty" data-sync="difficulty" data-value="easy"><span class="pips" aria-hidden="true"><i></i><i></i><i></i></span><span class="difficulty-text">Snadné</span></span>
```

```css
/* data-value: easy | medium | hard  →  1 / 2 / 3 filled pips. Text: Snadné / Střední / Náročné. */
.difficulty { display: inline-flex; align-items: center; gap: .5rem; margin-top: .25rem; padding: .2rem .8rem .2rem .55rem; border: 2px solid var(--cobalt);
  border-radius: 999px; background: var(--paper); font-weight: 700; font-size: 1.05rem; color: var(--cobalt); }
.pips { display: inline-flex; gap: 3px; }
.pips i { width: 9px; height: 18px; border-radius: 3px; border: 2px solid var(--cobalt); }
.difficulty[data-value="easy"] .pips i:nth-child(-n+1), .difficulty[data-value="medium"] .pips i:nth-child(-n+2), .difficulty[data-value="hard"] .pips i { background: var(--cobalt); }
.difficulty[data-value="easy"] .pips i:first-child { background: var(--sage); border-color: var(--sage); }
.difficulty[data-value="hard"] .pips i { background: var(--tomato); border-color: var(--tomato); }
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
/* data-value keys: gas-stove | induction | oven | air-fryer | microwave | blender (icon comes from the icons block). */
.appliances { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .4rem; }
.appliance { display: inline-flex; align-items: center; gap: .45rem; padding: .3rem .85rem .3rem .6rem; border: 2px solid var(--cobalt); border-radius: 999px;
  background: var(--tint); font-size: 1rem; font-weight: 700; color: var(--cobalt); }
.appliance::before { width: 1.3em; height: 1.3em; }
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
.family { margin-top: calc(var(--gap) * 1.6); }
.family-grid { display: grid; gap: var(--gap); }
@media (min-width: 760px) { .family-grid { grid-template-columns: 1.15fr 1fr; align-items: stretch; } }
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
.ratings { list-style: none; margin: 0; padding: 0; display: grid; gap: .35rem; }
.ratings li { display: flex; justify-content: space-between; align-items: center; gap: .6rem; padding: .3rem 0; border-bottom: 2px dashed var(--dot); }
.ratings li:last-child { border-bottom: 0; }
.who { font-weight: 700; }
.rating { display: inline-flex; align-items: center; gap: .4rem; padding: .2rem .75rem .2rem .55rem; border-radius: 999px; font-size: 1rem; font-weight: 700;
  border: 2px solid currentColor; background: var(--paper); color: #5b6478; }
.rating[data-value="loved"] { color: var(--tomato-ink); background: #fde9e4; }
.rating[data-value="ok"] { color: #7a5600; background: #fdf1d2; }
.rating[data-value="disliked"] { color: var(--cobalt); background: #e6ecf7; }
.last-prepared { margin: .8rem 0 0; font-size: 1rem; }
.last-prepared time { font-weight: 700; color: var(--cobalt); }
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
.notes { line-height: 1.75em; min-height: 7em; background-image: linear-gradient(transparent calc(100% - 2px), var(--dot) 0); background-size: 100% 1.75em; }
.notes p { margin: 0; }
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
.checklist { list-style: none; margin: 0; padding: 0; display: grid; gap: .25rem; }
@media (min-width: 640px) and (max-width: 999px) { .checklist { grid-template-columns: 1fr 1fr; column-gap: 1rem; } }
.checklist button { all: unset; box-sizing: border-box; cursor: pointer; width: 100%; display: flex; align-items: center; gap: .85rem;
  padding: .65rem .5rem; min-height: 56px; border-radius: 14px; font-size: var(--fs-body); line-height: 1.3; -webkit-tap-highlight-color: transparent; }
.checklist button:focus-visible { outline: 4px solid var(--mustard); }
.checklist .box { flex: none; width: 34px; height: 34px; border-radius: 50%; border: 3px solid var(--cobalt); background: var(--paper); display: grid; place-items: center; transition: background .15s, transform .15s; }
.checklist .box::after { content: ""; width: 20px; height: 20px; background: var(--paper); -webkit-mask: var(--i-check) center / contain no-repeat; mask: var(--i-check) center / contain no-repeat; opacity: 0; }
.checklist .qty { font-weight: 700; color: var(--cobalt); white-space: nowrap; }
.checklist [aria-pressed="true"] .box { background: var(--sage); border-color: var(--sage); transform: scale(1.06); }
.checklist [aria-pressed="true"] .box::after { opacity: 1; }
.checklist [aria-pressed="true"] .text { text-decoration: line-through; text-decoration-thickness: 2px; opacity: .55; }
.list-tools { display: flex; justify-content: space-between; align-items: center; gap: .5rem; flex-wrap: wrap; margin-top: 1rem; font-size: 1rem; }
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
.steps { list-style: none; margin: 0; padding: 0; display: grid; gap: calc(var(--gap) * 1.1); counter-reset: step; }
.step { counter-increment: step; display: grid; grid-template-columns: auto 1fr; gap: 0 clamp(.9rem, .5rem + 1.5vw, 1.6rem); align-items: start; }
.step::before { content: counter(step); width: clamp(64px, 50px + 3vw, 88px); aspect-ratio: 1; border-radius: 50%; display: grid; place-items: center;
  font-family: var(--font-display); font-weight: 900; font-size: clamp(2rem, 1.5rem + 1.8vw, 2.9rem); color: var(--paper); background: var(--cobalt);
  box-shadow: inset 0 0 0 5px var(--cobalt), inset 0 0 0 8px var(--paper), 4px 4px 0 var(--tomato); transition: background .2s; }
.step-body { padding-top: .2rem; min-width: 0; }
.step h3 { font-size: clamp(1.35rem, 1.1rem + 1vw, 1.8rem); font-weight: 700; margin-bottom: .35rem; }
.step p { font-size: var(--fs-step); line-height: 1.5; margin: 0; max-width: 42ch; }
.step-photo { margin: 1rem 0 0; border: var(--rim); border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-sm); max-width: 520px; background: var(--paper); }
.step-photo img { width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; }
.step-photo figcaption { font-size: .9rem; padding: .45rem .8rem; border-top: 2px solid var(--cobalt); }
.step-done { margin-top: .9rem; min-width: 8rem; }
.step.is-done::before { content: "✓"; background: var(--sage); box-shadow: inset 0 0 0 5px var(--sage), inset 0 0 0 8px var(--paper), 4px 4px 0 var(--cobalt); }
.step.is-done h3, .step.is-done p, .step.is-done aside, .step.is-done .warning { opacity: .5; }
```

### 7.17 Our inline note (inside a step)  `@c:our-inline`

Short addition of ours placed right after the original paragraph it relates to.

```html
<p class="our-inline"><span class="our-mark">Náš tip</span> Bez pánve to jde i v horkovzdušné fritéze — postup je níže v tipu „Varianta · horkovzdušná fritéza“.</p>
```

```css
/* OUR addition inside original text flow. Rule for the whole design: our additions = DASHED tomato rim + "Náš tip" tag. */
.step p.our-inline, .our-inline { margin: .9rem 0 0; padding: .6rem .9rem; border: 2px dashed var(--tomato); border-radius: 14px; background: var(--paper); font-size: 1.15rem; line-height: 1.45; max-width: 46ch; }
.our-mark { display: inline-flex; align-items: center; gap: .25rem; margin-right: .35rem; padding: .05rem .6rem .05rem .45rem; border-radius: 999px; background: var(--tomato); color: var(--paper);
  font-size: .8rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; vertical-align: .12em; }
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
.warning { margin: .9rem 0 0; padding: .7rem 1rem .8rem 3.4rem; position: relative; border: 3px solid var(--tomato); border-radius: 14px; background: #fde9e4; max-width: 46ch; }
.warning::before { content: ""; position: absolute; left: .9rem; top: .85rem; width: 1.7rem; height: 1.7rem; background: var(--tomato); -webkit-mask: var(--i-warning) center / contain no-repeat; mask: var(--i-warning) center / contain no-repeat; }
.warning-label { display: block; font-size: .8rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--tomato-ink); }
.step .warning p, .warning p { margin: .15rem 0 0; font-size: 1.15rem; line-height: 1.45; }
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
/* Neutral explanation. data-origin="ours" → dashed rim + "náš doplněk" in the label; data-origin="source" → solid rim, label "Na okraj · ze zdroje". */
.sidenote { margin: .9rem 0 0; padding: .6rem 1rem; border-left: 6px solid var(--cobalt); border-radius: 0 14px 14px 0; background: var(--paper); max-width: 46ch;
  background-image: radial-gradient(circle, var(--dot) 0 2px, transparent 2.5px); background-size: 16px 16px; }
.sidenote[data-origin="ours"] { border: 2px dashed var(--tomato); border-left: 6px solid var(--tomato); }
.sidenote-label { display: block; font-size: .8rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--cobalt); }
.sidenote[data-origin="ours"] .sidenote-label { color: var(--tomato-ink); }
.step .sidenote p, .sidenote p { margin: .1rem 0 0; font-size: 1.15rem; line-height: 1.45; }
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
.tips { display: grid; gap: calc(var(--gap) * 1.4); margin-top: calc(var(--gap) * 2); }
@media (min-width: 1000px) { .tips { grid-template-columns: 1fr 1fr; align-items: start; } }
.tip { position: relative; background: var(--paper); border: var(--rim); border-radius: var(--radius); padding: 2.2rem clamp(1rem, .7rem + 1vw, 1.6rem) 1.3rem; box-shadow: var(--shadow); }
.tip-label { position: absolute; top: -1.05rem; left: 1.2rem; font-weight: 700; font-size: .9rem; letter-spacing: .1em; text-transform: uppercase;
  background: var(--mustard); color: var(--ink); border: 3px solid var(--cobalt); border-radius: 999px; padding: .25rem .9rem; }
.tip h3 { font-size: clamp(1.4rem, 1.15rem + 1vw, 1.9rem); margin-bottom: .6rem; }
.tip p { margin: 0 0 .7rem; }
.tip .facts { display: flex; gap: .6rem; flex-wrap: wrap; margin: .2rem 0 1rem; }
.tip .fact { border: 2px solid var(--cobalt); border-radius: 14px; padding: .4rem .8rem; background: var(--tint); font-weight: 700; }
.tip .fact b { display: block; font-family: var(--font-display); font-size: 1.6rem; color: var(--cobalt); line-height: 1.1; }
.tip .tip-source { font-size: .95rem; border-top: 2px dashed var(--dot); padding-top: .7rem; margin: .4rem 0 0; }
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
.tip--ours { border-style: dashed; border-color: var(--tomato); box-shadow: 6px 6px 0 var(--tomato); }
.tip--ours .tip-label { background: var(--tomato); color: var(--paper); border-color: var(--tomato); display: inline-flex; align-items: center; gap: .35rem; }
.tip--ours .tip-label::before { content: ""; width: 1em; height: 1em; background: currentColor; -webkit-mask: var(--i-plus) center / contain no-repeat; mask: var(--i-plus) center / contain no-repeat; }
.tip .big { font-family: var(--font-display); font-weight: 900; font-size: clamp(2.6rem, 2rem + 2.5vw, 3.6rem); color: var(--tomato); line-height: 1; }
.tip--ours .tip-source { color: var(--tomato-ink); font-weight: 700; }
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
.toolbar { display: flex; gap: .7rem; flex-wrap: wrap; margin-top: calc(var(--gap) * 1.4); }
.toolbar .btn { min-height: 56px; padding-inline: 1.4rem; font-size: 1.1rem; }
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
.source-foot { margin-top: calc(var(--gap) * 2); background: var(--paper); }
.source-foot::before { content: ""; display: block; height: 28px; border-top: var(--rim); border-bottom: var(--rim); background-color: var(--cobalt);
  background-image: radial-gradient(circle, var(--paper) 0 5px, transparent 5.5px), radial-gradient(circle, var(--paper) 0 5px, transparent 5.5px); background-size: 34px 34px; background-position: 0 0, 17px 17px; }
.source-foot .wrap { padding-block: 1.4rem 2.4rem; font-size: 1.05rem; }
.source-foot p { margin: .3rem 0; }
.foot-ours { color: var(--tomato-ink); }
@media print { .frame-open, .toolbar, .list-tools, .step-done, .backlink { display: none !important; } .card, .tip, .hero-photo, .meta { box-shadow: none; } }
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
  .meta > li:first-child { border-right: 0; border-bottom: 2px dashed var(--dot); }
  .meta > li:nth-child(2) { border-right: 2px dashed var(--dot); }
  .hero h1 { font-size: clamp(2.2rem, 9vw, 2.8rem); }
}
```

## 8. New recipe page — checklist (historic, design-phase; for the official site use O8)

1. Copy this design's `kureci-rizek.html` → `recipes/<slug>.html` (keeps the full `<style>` and `<script>`).
2. Set `<title>`, the header comment, `data-recipe-id`, `data-tint` (§3 rule).
3. Replace content component by component from §7, keeping `data-sync` attributes and `@c:` comments.
4. Images: resize to ≤ 1000 px wide, JPEG q≈75, embed as `data:image/jpeg;base64,…` (≈ 60–110 kB each). Keep total page ≲ 600 kB; if a recipe has many photos, keep the hero + at most 3 step photos.
5. Verify: open with no network → only `fonts/*.woff2` may be requested; screenshot at 820×1180 (iPad portrait), 1180×820 (iPad landscape) and 393×852 + 375×812 with mobile emulation (iPhone), check `document.documentElement.scrollWidth === innerWidth` and every tint-coloured element is legible; embed in an iframe → fullscreen bar visible, wake lock hidden.

---

# Official site (O-sections, authoritative)

The full handover is in `docs/AGENT.md`; the Markdown format is in `docs/CONTENT-FORMAT.md`. This part only pins the rules that the
components depend on.

## O1. Pipeline and repository layout

Waterfall: **Notion → `data/<slug>.json` (tools/sync.py, assistant's box) → GitHub Action on every push:
`apply_json.py` (json → front matter of `content/<slug>.md`) → `build.py` (md + `themes/<theme>/` → `recipes/<slug>.html`)
→ `build_index.py` (`index.html`) → one commit `build: json → md → html [skip ci]` if anything changed.**

| Path | What | Edited by |
|---|---|---|
| `content/<slug>.md` | front matter + verbatim recipe body | humans/agents (synced keys: Notion) |
| `content/img/`, `content/img/originals/` | web-ready / original photos | `tools/images.py` / human |
| `data/<slug>.json` | Notion snapshot | `tools/sync.py` only |
| `themes/_shared/` | `tints.css icons.css official.css script.js` (all themes) | human |
| `themes/<id>/` | `theme.json fonts.css design.css fonts/ cookbook.md` (+ `index.css index.template.html` for smalt) | human |
| `themes/<id>/preview.html` | the reference recipe in that theme | **generated** |
| `recipes/<slug>.html`, `recipes/fonts/` | standalone cooking pages (inline CSS/JS, base64 photos), every theme's fonts | **generated** |
| `index.html` | recipe index (always smalt) | **generated** from `themes/smalt/index.template.html` |
| `images/thumbs/<slug>.jpg`, `images/covers/<slug>.jpg` | index card 480×360 q74, Notion cover ≤1200 q80 | `tools/images.py` |
| `designs/` | frozen proposals A/B/C | nobody |

Page CSS order: theme `fonts.css` → `_shared/tints.css` → `_shared/icons.css` → theme `design.css` → `_shared/official.css`.
`<meta name="theme-color">` comes from `theme.json`, and `<body data-design="<theme>" data-tint="<tint>">`.
Every HTML file keeps `<meta name="robots" content="noindex,nofollow">`; `robots.txt` stays.

## O2. Content rules (non-negotiable)

1. Only human-written, popular, well-rated Czech/Slovak recipes. Beginner- and kid-friendly.
2. The **original text is copied verbatim**: ingredients, steps and the author's tips. No rewriting, no translation, no "fixing" Slovak.
3. Anything we add lives only in a clearly marked box. In Markdown that is `::: our-tip` (in a step → `@c:our-inline`, in Tipy → `@c:tip-ours`),
   `::: note` (`@c:sidenote`) or `::: warning` (`@c:warning`). The author's tips are `::: tip` (`@c:tip-source`).
4. The source is credited with author and link **at the top** (`@c:topbar`) **and at the bottom** (`@c:source-foot`), from front matter `source:`. Photos are credited too.
5. Our tips may use only the family kitchen: gas stove, air fryer, rice cooker, microwave, oven (grill + steam), meat probe, halušky grater, KitchenAid stand mixer (with attachments), pressure cooker, immersion blender.
   **The meat probe is wired to the oven and works only for oven cooking.** Never suggest it for a pan, a pot or the air fryer.
   Other tools may be mentioned only where the original recipe uses them. New equipment needs Braňo's confirmation.
6. Page weight is ~150–300 KB (hero 720 px q86, step photos 720 px q70).

## O3. Tint per main ingredient

Notion "Main ingredient" → front matter `tint` → `<body data-tint="…">`:

| Notion | tint |
|---|---|
| Poultry | `chicken` |
| Pork & beef | `pork-beef` |
| Minced meat | `minced` |
| Pasta / rice / potatoes | `pasta-rice` |
| Fish & seafood | `fish` |
| Vegetarian | `veg` |

Choices so far: řízek → chicken; bryndzové halušky → pasta-rice (the potato dough is the dish, the bacon is a topping);
carbonara → pasta-rice (pancetta/bacon is a flavouring); palačinky → veg.

## O4. Page skeleton additions

* `<main id="recipe" data-recipe-id="<slug>">`. `script.js` keys the localStorage checkboxes by it.
* A framing-detection script in `<head>` adds `html.is-framed` inside Notion; `@c:frame` then shows „⤢ Otevřít na celou obrazovku“.
* `<script type="application/json" id="recipe-meta">` holds a machine-readable copy of the page data (slug, theme, tint, ratings…),
  serialised with `sort_keys`, `indent=1`, `ensure_ascii=False`, and `</` escaped as `<\/`.

### `@c:checklist-group`
A non-clickable heading inside the ingredient list (Markdown `### Dále:` in `## Suroviny`):
`<li class="checklist-group"><span>Dále:</span></li>`. It has no `<button>`, so script.js's index-based keys stay stable.

### `@c:rating-inherited`
A person without their own rating shows the family (Overall) value with `data-inherited` (dashed rim + „· jako rodina“).
With no overall rating either, it shows „Zatím nehodnotil“ (Zuzka: „Zatím nehodnotila“). An empty Overall shows „Zatím nehodnoceno“.
Empty notes show `<p class="notes-empty">Zatím bez poznámek.</p>`.

### Icons
`--i-rice-cooker` and `--i-meat-probe` in `_shared/icons.css`, mapped by `.appliance[data-value="rice-cooker|meat-probe"]`.

## O5. Index (`index.html`)

Smalt header „Rodinná kuchařka“ with the „Správa v Notion“ link (in the template), a collapsible `<details id="filters">` (open by
default at ≥760 px), and a card grid of 1/2/3 columns. A card has the thumb, title, time, difficulty pips and overall rating colour.
Filters run client-side on the inline JSON `#recipes-data`: ingredients (a card must contain **all** selected), max time
(30/45/60/90), difficulty, appliances, labels, overall rating (loved/ok/disliked/unrated). Sort: title (cs collation), time,
last prepared. Chips are generated only for values that occur in at least one recipe. Tested at 375/393/820×1180/1180×820.

## O6. Data contract (Notion → JSON → front matter → page)

| Notion | data / front matter key | rendered as (`data-sync` hook) |
|---|---|---|
| Title | `title` | `<h1 data-sync="title">`, `<title>{title} · Rodinná kuchařka</title>` |
| Theme | `theme` (empty = keep md) | which `themes/<id>/` styles the page |
| Total time | `total_time` | `total_time` „40 min“ / „1 h 15 min“ |
| Difficulty Easy/Medium/Hard | `difficulty` | `difficulty` Snadné/Střední/Náročné + pips |
| Labels | `labels` | `labels`, Czech chips (`vocab.LABELS_CS`) |
| Appliances | `appliances` | `appliances` icon badges, in `vocab.APPLIANCES` order |
| Main ingredient | `main_ingredient` → `tint` | `body[data-tint]` |
| Overall / Braňo … Lukáš | `ratings.*` | `rating_overall`, `rating_brano` … `rating_lukas` |
| Last prepared | `last_prepared` | `last_prepared` „5. 11. 2026“ / „zatím ne“ |
| Notes | `notes` | `notes` paragraphs / empty state |
| Ingredients | `ingredients` | `recipe-meta` + the index ingredient filter (the checklist comes from the Markdown body) |
| Page / Source | `page_url` / `source_url` | identity; the slug is fixed by the file name |

Nothing patches HTML in place. Pages are fully regenerated, deterministically.

## O7. Running the sync and the build

```bash
python3 tools/mcp_to_input.py recipes.json ingredients.json appliances.json > notion.json   # MCP exports → input
python3 tools/sync.py --input notion.json        # writes data/*.json only; one commit "sync: notion → json"; push
python3 tools/apply_json.py && python3 tools/build.py && python3 tools/build_index.py      # what the Action runs
```

## O8. Adding a new recipe

Write `content/<slug>.md` (verbatim, see `docs/CONTENT-FORMAT.md`) → put the photos in `content/img/originals/` and run
`tools/images.py <slug>` → create the Notion row (Page URL = `…/recipes/<slug>.html`, cover, the embed + „Open full screen“
link; ratings, Last prepared and Notes left empty) → sync → push → verify the widths from §5a and a live 200.

## O9. Notion admin (English)

Top page „Family Cookbook“ → Recipes (views: Gallery, Under 45 min, Table; select **Theme** smalt/len/sesit), Ingredients
(At home, Category, Czech name, kids' likes) and Appliances (the ten in `docs/AGENT.md`; Key = icon key). The Recipes formula „Have at home“ =
at-home ingredients / all ingredients.
