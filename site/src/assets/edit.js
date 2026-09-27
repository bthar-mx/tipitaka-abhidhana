// /edit/ (behind Cloudflare Access; docs/editor-mode.md): signs this browser into editor mode and lists
// the history of edits. Browse then loads assets/editor.js, which adds the Edit buttons.
'use strict';
(function () {
Object.assign(T.en, { e_as: e => `Signed in as ${e}. Editor mode is on in this browser.`, e_no: m => `Not signed in, or the editor API is not set up (${m}). Editor mode is off.`,
  e_left: 'Editor mode is off in this browser.', e_none: 'No edits yet.', e_cols: ['date', 'book', 'id', 'headword', 'field', 'sense', 'value', 'before', 'state'] });
Object.assign(T.es, { e_as: e => `Sesión iniciada como ${e}. El modo editor está activo en este navegador.`, e_no: m => `No ha iniciado sesión, o la API del editor no está configurada (${m}). El modo editor está desactivado.`,
  e_left: 'El modo editor está desactivado en este navegador.', e_none: 'Aún no hay ediciones.', e_cols: ['fecha', 'libro', 'id', 'entrada', 'campo', 'sentido', 'valor', 'antes', 'estado'] });
const set = on => { try { if (on) localStorage.setItem('abhidhana-editor', '1'); else localStorage.removeItem('abhidhana-editor'); } catch (e) {} };
let who = null, rows = [];

async function get(path) {
  const r = await fetch(path, { credentials: 'same-origin', redirect: 'manual' });
  if (r.type === 'opaqueredirect' || r.status === 0) throw new Error('Access');
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || r.status);
  return j;
}
function whoLine() { $('who').textContent = who ? t('e_as', who) : $('who').dataset.err ? t('e_no', $('who').dataset.err) : '…'; }

async function history() {
  const f = new FormData($('filt')), q = new URLSearchParams();
  for (const k of ['book', 'id', 'limit']) if ((f.get(k) || '').trim()) q.set(k, f.get(k).trim());
  rows = (await get('/api/admin/edits?' + q)).edits;
  draw();
  // the headword and a link to the article's page, from the search list (the same file the header search uses)
  searchIndex().then(() => draw()).catch(() => {});
}
function draw() {
  if (!rows.length) { $('hist').innerHTML = `<p class="muted">${esc(t('e_none'))}</p>`; return; }
  const find = (b, i) => S ? S.find(r => r[0] === b && r[1] === i) : null;
  $('hist').innerHTML = `<table class="ed-table"><tr>${t('e_cols').map(c => `<th>${esc(c)}</th>`).join('')}</tr>` + rows.map(e => {
    const s = find(e.book, e.id), my = /[က-႟]/.test(e.value + e.old) ? ' class="v my" lang="my"' : ' class="v"';
    const hw = s ? `<a href="/v/${esc(e.book)}/${s[2]}#a${e.id}"><span class="pl" lang="pi">${esc(s[4])}</span></a>` : '';
    return `<tr class="${e.status === 'reverted' ? 'rev' : ''}"><td>${esc(e.date.replace('T', ' ').slice(0, 16))}</td><td>${esc(e.book)}</td><td>${e.id}</td><td>${hw}</td>` +
      `<td>${esc(e.field)}</td><td>${esc(e.sense)}</td><td${my}>${esc(e.value)}</td><td${my}>${esc(e.old)}</td><td>${esc(e.status)}</td></tr>`;
  }).join('') + '</table>';
}

$('leave').addEventListener('click', () => { set(false); who = null; $('acts').hidden = true; $('who').textContent = t('e_left'); });
$('filt').addEventListener('submit', e => { e.preventDefault(); history().catch(err => { $('hist').textContent = err.message; }); });
langHooks.push(() => { whoLine(); if (rows.length) draw(); });
get('/api/admin/whoami').then(j => {
  who = j.email || '?'; set(true); $('acts').hidden = false; whoLine();
  return history();
}).catch(err => { set(false); $('who').dataset.err = err.message; whoLine(); });
})();
