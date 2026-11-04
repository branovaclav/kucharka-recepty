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
