// The Introduction page (/introduction/): views, contents links, the abbreviations search.
// Built by tools/abhidhana_intro.py; needs common.js (t, fold, langHooks).
(function () {
  const main = document.getElementById('intro');
  if (!main) return;

  // --- views: the translation, the Burmese original, or both side by side (remembered)
  function setView(v, save) {
    if (!['tr', 'my', 'both'].includes(v)) v = 'tr';
    main.dataset.view = v;
    document.querySelectorAll('.viewsw button').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === v));
    if (save) { try { localStorage.setItem('introView', v); } catch (e) {} }
  }
  let saved = null;
  try { saved = localStorage.getItem('introView'); } catch (e) {}
  setView(saved || 'tr', false);
  document.addEventListener('click', e => {
    const b = e.target.closest('.viewsw button');
    if (b) setView(b.dataset.view, true);
  });

  // --- contents: a heading exists in the single view and again in the side-by-side view;
  // go to the copy that is shown
  const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  function go(id, smooth) {
    const all = [...document.querySelectorAll(`[data-a="${CSS.escape(id)}"]`)];
    const el = all.find(visible) || document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('.toc a[href^="#"]');
    if (!a) return;
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    if (!document.querySelector(`[data-a="${CSS.escape(id)}"]`)) return;   // chapters: default behaviour
    e.preventDefault(); history.replaceState(null, '', '#' + id); go(id, true);
  });
  if (location.hash) setTimeout(() => go(decodeURIComponent(location.hash.slice(1)), false), 50);

  // --- the abbreviations: filter as you type, over every column
  const q = document.getElementById('abbr-q'), n = document.getElementById('abbr-n');
  const rows = [...document.querySelectorAll('#abbr-table tbody tr')];
  const keys = rows.map(r => fold(r.textContent.replace(/\s+/g, ' ')));
  function filter() {
    if (!q) return;
    const s = fold(q.value.trim()); let k = 0;
    rows.forEach((r, i) => { const on = !s || keys[i].includes(s); r.hidden = !on; k += on; });
    if (n) n.textContent = t('abbr_n', k, rows.length);
  }
  if (q) { q.addEventListener('input', filter); filter(); langHooks.push(filter); }
})();
