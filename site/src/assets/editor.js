// Editor mode in Browse (docs/editor-mode.md). Loaded by browse.js only in a browser that /edit/ marked
// for editor mode; it shows nothing until /api/admin/whoami (behind Cloudflare Access) answers. Then each
// article gets an Edit button and a form for its Meaning (ES/EN, the status of the Spanish, whole or by
// sense) and its fields (headword, label, analysis, body, in Burmese). A save writes new rows to the D1
// database through /api/admin/edits; the page lays them over the static data (browse.js ov()).
'use strict';
(function () {
Object.assign(T.en, {
  ed_edit: 'Edit', ed_close: 'Close', ed_save: 'Save', ed_saving: 'Saving…', ed_saved: 'Saved.', ed_nochange: 'Nothing changed.',
  ed_meaning: 'Meaning', ed_article: 'The article (Burmese, as printed)', ed_es: 'Spanish', ed_en: 'English',
  ed_status: 'Status of the Spanish', ed_senses: 'senses', ed_senses_ph: 'all, or 1 or 1,3', ed_st_drafted: 'drafted', ed_st_reviewed: 'reviewed', ed_st_corrected: 'corrected',
  ed_hw: 'Headword', ed_label: 'Label (without brackets)', ed_an: 'Analysis (without [ ])', ed_body: 'Definition (body)',
  ed_preview: 'roman', ed_nopreview: 'No roman preview for the body: it mixes Burmese prose with Pāḷi.',
  ed_withdraw: 'withdraw the edit', ed_withdrawn: 'Edit withdrawn: the published text shows again.',
  ed_edited: d => `edited ${d}`, ed_empty: f => `${f} is empty. To go back to the published text, withdraw the edit.`,
  ed_err: m => `Not saved: ${m}`, ed_signin: 'Editor mode: not signed in.', ed_signin_a: 'Sign in', ed_as: e => `Editor mode · ${e}`,
  ed_text_corr: 'A new Spanish text counts as corrected unless a status is chosen here.',
  ed_sense_drafted: 'A status by sense must be reviewed or corrected.', ed_not_my: f => `${f}: no Burmese letters. Is the keyboard set to Myanmar (Unicode)?`,
  ed_m_my: 'Burmese', ed_m_rom: 'Roman', ed_m_title: 'Type this field in Burmese script or in roman (IAST)',
  ed_store: 'stored', ed_back: 'read back', ed_back_ok: 'matches what was typed',
  ed_back_bad: 'differs from what was typed: correct it, or type this field in Burmese',
  ed_rt: f => `${f}: the Burmese read back in roman differs from what was typed.`,
});
Object.assign(T.es, {
  ed_edit: 'Editar', ed_close: 'Cerrar', ed_save: 'Guardar', ed_saving: 'Guardando…', ed_saved: 'Guardado.', ed_nochange: 'No ha cambiado nada.',
  ed_meaning: 'Significado', ed_article: 'El artículo (en birmano, como está impreso)', ed_es: 'Español', ed_en: 'Inglés',
  ed_status: 'Estado del español', ed_senses: 'sentidos', ed_senses_ph: 'todos, o 1 o 1,3', ed_st_drafted: 'borrador', ed_st_reviewed: 'revisado', ed_st_corrected: 'corregido',
  ed_hw: 'Entrada', ed_label: 'Categoría (sin paréntesis)', ed_an: 'Análisis (sin [ ])', ed_body: 'Definición (cuerpo)',
  ed_preview: 'latín', ed_nopreview: 'Sin vista previa en caracteres latinos para el cuerpo: mezcla prosa birmana y pāḷi.',
  ed_withdraw: 'retirar la edición', ed_withdrawn: 'Edición retirada: vuelve a verse el texto publicado.',
  ed_edited: d => `editado el ${d}`, ed_empty: f => `${f} está vacío. Para volver al texto publicado, retire la edición.`,
  ed_err: m => `No se guardó: ${m}`, ed_signin: 'Modo editor: no ha iniciado sesión.', ed_signin_a: 'Iniciar sesión', ed_as: e => `Modo editor · ${e}`,
  ed_text_corr: 'Un texto español nuevo cuenta como corregido salvo que se elija aquí un estado.',
  ed_sense_drafted: 'Un estado por sentidos ha de ser revisado o corregido.', ed_not_my: f => `${f}: no hay letras birmanas. ¿Está el teclado en birmano (Unicode)?`,
  ed_m_my: 'Birmano', ed_m_rom: 'Latín', ed_m_title: 'Escribir este campo en letra birmana o en caracteres latinos (IAST)',
  ed_store: 'se guarda', ed_back: 'relectura', ed_back_ok: 'coincide con lo escrito',
  ed_back_bad: 'no coincide con lo escrito: corríjalo, o escriba este campo en birmano',
  ed_rt: f => `${f}: el birmano releído en caracteres latinos no coincide con lo escrito.`,
});

const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = window.EDITOR_CSS || '/assets/editor.css';
document.head.appendChild(css);
const badge = document.createElement('div'); badge.className = 'ed-badge'; document.body.appendChild(badge);
let who = null, openId = null, form = null, msg = '', stash = null;   // stash: what was typed, kept across a re-render

const nfc = s => (s || '').normalize('NFC').trim();

// Roman input (brief §53): headword, label and analysis can be typed in IAST; the form converts to Burmese
// (ROMAN.burmese) and shows the Burmese to be stored and its roman read-back (ROMAN.segment); a save needs
// the read-back to equal what was typed. The mode is kept per field in this browser.
const ROM_FIELDS = ['headword', 'label', 'analysis'];
const modeKey = k => 'abh-ed-mode-' + k;
function modeOf(k) { try { return localStorage.getItem(modeKey(k)) === 'rom' ? 'rom' : 'my'; } catch (e) { return 'my'; } }
function setMode(k, m) { try { localStorage.setItem(modeKey(k), m); } catch (e) { /* the mode is then kept for this page only */ } memMode[k] = m; }
const memMode = {};
const mode = k => memMode[k] || modeOf(k);
let base = {};   // per field: the roman shown when the field went roman and the Burmese it came from
function baseFor(k, b) { base[k] = { r: ROMAN.segment(b), b }; return base[k].r; }
// the Burmese a field would store, and whether its read-back matches what was typed
function reading(k) {
  const el = form.querySelector(`[data-f="${k}"]`), v = el ? el.value : '';
  if (!ROM_FIELDS.includes(k) || mode(k) !== 'rom') { const b = nfc(v); return { b, back: b ? ROMAN.segment(b) : '', ok: true, rom: false }; }
  const typed = ROMAN.canon(v), bs = base[k];
  const b = bs && typed === ROMAN.canon(bs.r) ? nfc(bs.b) : ROMAN.burmese(typed), back = b ? ROMAN.segment(b) : '';
  // a letter the conversion does not know stays Latin in the Burmese and can read back unchanged: refused too
  return { b, back, typed, ok: back === typed && !/[A-Za-z\u00C0-\u024F\u1E00-\u1EFF]/.test(b), rom: true };
}
const hasMy = s => /[က-႟]/.test(s);
const sensesOf = s => [...new Set(nfc(s).split(/[\s,;]+/).filter(Boolean).map(Number).filter(n => n > 0 && n < 100))].sort((a, b) => a - b).join(',');

async function api(path, opt) {
  const r = await fetch(path, Object.assign({ credentials: 'same-origin', redirect: 'manual' }, opt || {}));
  if (r.type === 'opaqueredirect' || r.status === 0) throw new Error(t('ed_signin'));
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || r.status);
  return j;
}

function showBadge() {
  badge.innerHTML = who ? `${esc(t('ed_as', who))} · <a href="/edit/">/edit/</a>`
    : `${esc(t('ed_signin'))} <a href="/edit/">${esc(t('ed_signin_a'))}</a>`;
}

// the values the page shows now (the static data with the saved edits over them)
// the Meaning as its source file has it: the build turned [[x]] into [[x|address]] or [[x|]]
const srcTr = x => (x || '').replace(/\[\[([^\]|]+)\|[^\]]*\]\]/g, '[[$1]]');
function current(d) {
  const es = d.t && d.t.es, st = es ? es.s : 'drafted';
  return {
    es: es ? srcTr(es.x) : '', en: d.t && d.t.en ? srcTr(d.t.en.x) : '', headword: d.h || '', label: d.l || '', analysis: d.a || '', body: d.b || '',
    status: st === 'partial' ? 'corrected' : st === 'rpartial' ? 'reviewed' : st, senses: (st === 'partial' || st === 'rpartial') ? (es.cs || []).join(',') : '',
  };
}

const langAttr = (key, v) => ROM_FIELDS.includes(key) && mode(key) === 'rom' ? 'lang="pi" class="ed-rom"'
  : hasMy(v) || ['headword', 'label', 'analysis', 'body'].includes(key) ? 'lang="my" class="my"' : `lang="${key}"`;
function field(d, key, label, kind, preview) {
  let v = current(d)[key]; const e = d.ed && d.ed[key];
  if (ROM_FIELDS.includes(key) && mode(key) === 'rom') v = baseFor(key, v);
  const input = kind === 'area'
    ? `<textarea data-f="${key}" rows="${key === 'body' ? 8 : 3}" ${langAttr(key, v)} spellcheck="${key === 'es' || key === 'en'}">${esc(v)}</textarea>`
    : `<input data-f="${key}" type="text" ${langAttr(key, v)} spellcheck="false" value="${esc(v)}">`;
  const sw = ROM_FIELDS.includes(key) ? ` <span class="ed-mode" role="group" title="${esc(t('ed_m_title'))}">` +
    ['my', 'rom'].map(m => `<button type="button" data-mode="${m}" data-mf="${key}" aria-pressed="${mode(key) === m}">${esc(t('ed_m_' + m))}</button>`).join('') + '</span>' : '';
  return `<div class="ed-f"><label><span>${esc(t(label))}</span>` +
    (e ? ` <span class="muted small">${esc(t('ed_edited', e.date.slice(0, 10)))} · <button type="button" class="ed-link" data-withdraw="${key}">${esc(t('ed_withdraw'))}</button></span>` : '') +
    `</label>${sw}${input}` + (preview ? `<div class="ed-prev" data-prev="${key}"></div>` : '') + '</div>';
}

function formHTML(d) {
  const c = current(d);
  return `<section class="ed-form" data-id="${d.i}"><h2>${esc(t('ed_edit'))} · <span class="muted small">${esc(d.k)} · id ${d.i}</span></h2>` +
    `<h3>${esc(t('ed_meaning'))}</h3>` +
    field(d, 'es', 'ed_es', 'area') +
    `<div class="ed-f ed-st"><span>${esc(t('ed_status'))}</span> ` +
    ['drafted', 'reviewed', 'corrected'].map(s => `<label class="ed-r"><input type="radio" name="ed-st" value="${s}"${c.status === s ? ' checked' : ''}> ${esc(t('ed_st_' + s))}</label>`).join('') +
    ` <label class="ed-r">${esc(t('ed_senses'))} <input data-f="senses" type="text" size="8" placeholder="${esc(t('ed_senses_ph'))}" value="${esc(c.senses)}"></label>` +
    (hasStatusEdits(d) ? ` <button type="button" class="ed-link" data-withdraw="status">${esc(t('ed_withdraw'))}</button>` : '') +
    `<div class="muted small">${esc(t('ed_text_corr'))}</div></div>` +
    field(d, 'en', 'ed_en', 'area') +
    `<h3>${esc(t('ed_article'))}</h3>` +
    field(d, 'headword', 'ed_hw', 'input', true) + field(d, 'label', 'ed_label', 'input', true) +
    field(d, 'analysis', 'ed_an', 'area', true) + field(d, 'body', 'ed_body', 'area') +
    `<div class="muted small">${esc(t('ed_nopreview'))}</div>` +
    `<div class="ed-bar"><button type="button" class="btn ed-save" data-save>${esc(t('ed_save'))}</button>` +
    `<button type="button" class="btn" data-close>${esc(t('ed_close'))}</button><span class="ed-msg" role="status">${esc(msg)}</span></div></section>`;
}
// this article's status rows as saved (ov() folds them into one status); for "withdraw"
const statusRows = d => (ABH.rows(d.k, d.i) || []).filter(e => e.field === 'status');
const hasStatusEdits = d => statusRows(d).length > 0;

// under each of headword, label, analysis: the Burmese to be stored and its roman read-back; in roman
// mode, whether the read-back equals what was typed (Save is disabled while one does not)
function preview() {
  if (!form) return;
  let bad = false;
  form.querySelectorAll('[data-prev]').forEach(p => {
    const k = p.dataset.prev, r = reading(k);
    p.classList.toggle('ed-bad', r.rom && !r.ok);
    if (!r.b) { p.innerHTML = ''; return; }
    if (r.rom && !r.ok) bad = true;
    const show = !r.rom ? (k === 'analysis' ? '[' + ROMAN.analysis(r.b) + ']' : k === 'label' ? '(' + ROMAN.segment(r.b) + ')' : ROMAN.headword(r.b)) : r.back;
    p.innerHTML = `<div><span class="ed-k">${esc(t('ed_store'))}</span> <span class="my" lang="my" data-store>${esc(r.b)}</span></div>` +
      `<div><span class="ed-k">${esc(t('ed_back'))}</span> <span class="pl" lang="pi" data-back>${esc(show)}</span>` +
      (r.rom ? ` <span class="ed-chk" data-ok="${r.ok}">${r.ok ? '✓ ' + esc(t('ed_back_ok')) : '✗ ' + esc(t('ed_back_bad'))}</span>` : '') + '</div>';
  });
  const sv = form.querySelector('[data-save]'); if (sv) sv.disabled = bad;
}
// switch a field between Burmese and roman input, converting what is in it
function switchMode(k, m) {
  if (mode(k) === m) return;
  const el = form.querySelector(`[data-f="${k}"]`);
  if (m === 'rom') el.value = baseFor(k, nfc(el.value));
  else el.value = reading(k).b;
  setMode(k, m);
  el.lang = m === 'rom' ? 'pi' : 'my'; el.className = m === 'rom' ? 'ed-rom' : 'my';
  form.querySelectorAll(`[data-mf="${k}"]`).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === m)));
  el.dispatchEvent(new Event('input', { bubbles: true }));
}

async function post(d, edits) {
  const j = await api('/api/admin/edits', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Abhidhana-Editor': '1' },
    body: JSON.stringify({ book: d.k, id: d.i, edits }) });
  ABH.setEdits(d.k, j.latest, d.i);
  return j;
}

async function save(d) {
  const c = current(d), edits = [], val = k => ROM_FIELDS.includes(k) ? reading(k).b : nfc(form.querySelector(`[data-f="${k}"]`).value);
  const names = { es: t('ed_es'), en: t('ed_en'), headword: t('ed_hw'), label: t('ed_label'), analysis: t('ed_an'), body: t('ed_body') };
  for (const k of ['es', 'en', 'headword', 'label', 'analysis', 'body']) {
    const v = val(k);
    if (v === nfc(c[k])) continue;
    if (!v) throw new Error(t('ed_empty', names[k]));
    if (ROM_FIELDS.includes(k) && !reading(k).ok) throw new Error(t('ed_rt', names[k]));
    if (['headword', 'label', 'analysis', 'body'].includes(k) && !hasMy(v)) throw new Error(t('ed_not_my', names[k]));
    edits.push({ field: k, value: v, old: c[k] });
  }
  const st = (form.querySelector('input[name="ed-st"]:checked') || {}).value || c.status, se = sensesOf(val('senses'));
  if (st !== c.status || se !== c.senses) {
    if (se && st === 'drafted') throw new Error(t('ed_sense_drafted'));
    edits.push({ field: 'status', sense: se, value: st, old: c.status + (c.senses ? ` (${c.senses})` : '') });
  }
  if (!edits.length) { msg = t('ed_nochange'); return; }
  await post(d, edits);
  msg = t('ed_saved');
}

async function withdraw(d, key) {
  const c = current(d);
  const edits = key === 'status'
    ? [...new Set(statusRows(d).map(e => e.sense))].map(s => ({ field: 'status', sense: s, status: 'reverted', old: c.status }))
    : [{ field: key, status: 'reverted', old: c[key] }];
  if (!edits.length) return;
  await post(d, edits);
  msg = t('ed_withdrawn');
}

window.EDITOR = {
  decorate(d) {
    if (!who || !d) return;
    const art = document.querySelector('#art article'); if (!art) return;
    const where = art.querySelector('.where');
    if (where) where.insertAdjacentHTML('beforeend', `<button type="button" class="btn ed-open" data-edit aria-expanded="${openId === d.i}">${esc(t('ed_edit'))}</button>`);
    if (openId !== d.i) { form = null; base = {}; return; }
    art.querySelector('.head').insertAdjacentHTML('afterend', formHTML(d));
    form = art.querySelector('.ed-form');
    if (stash && stash.id === d.i) {
      for (const [k, v] of Object.entries(stash.v)) {
        const el = form.querySelector(k); if (el) { if (el.type === 'radio') el.checked = v; else el.value = v; }
      }
      Object.assign(base, stash.base || {});
    }
    preview();
    form.addEventListener('input', () => {
      const v = {};
      form.querySelectorAll('[data-f]').forEach(el => { v[`[data-f="${el.dataset.f}"]`] = el.value; });
      form.querySelectorAll('input[name="ed-st"]').forEach(el => { v[`input[name="ed-st"][value="${el.value}"]`] = el.checked; });
      stash = { id: d.i, v, base: Object.assign({}, base) }; preview();
    });
    form.addEventListener('click', async e => {
      const b = e.target.closest('button'); if (!b) return;
      e.stopPropagation();
      if ('close' in b.dataset) { openId = null; msg = ''; stash = null; return ABH.rerender(); }
      if (b.dataset.mf) return switchMode(b.dataset.mf, b.dataset.mode);
      const bar = form.querySelector('.ed-msg');
      try {
        if ('save' in b.dataset) { b.disabled = true; bar.textContent = t('ed_saving'); await save(d); stash = null; }
        else if (b.dataset.withdraw) { b.disabled = true; await withdraw(d, b.dataset.withdraw); stash = null; }
        else return;
        ABH.rerender();
      } catch (err) { b.disabled = false; msg = t('ed_err', err.message); bar.textContent = msg; }
    });
  },
};
document.addEventListener('click', e => {
  const b = e.target.closest('#art [data-edit]'); if (!b) return;
  const d = ABH.current(); if (!d) return;
  openId = openId === d.i ? null : d.i; msg = ''; stash = null;
  ABH.rerender();
}, true);
langHooks.push(showBadge);

api('/api/admin/whoami').then(j => { who = j.email || '?'; showBadge(); ABH.rerender(); })
  .catch(() => { who = null; showBadge(); });
})();
