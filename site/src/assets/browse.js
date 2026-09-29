// Browse: the dictionary consulted by word (the site's home, /w/<headword>, /browse/<letter>/<syllable>).
// Design: docs/site-design.md, from the mockup "Abhidhāna site mockup". Data: tools/abhidhana_browse.py.
// Nothing drafted is presented as a reading: every article and translation shows its status.
'use strict';
(function () {
const app = document.getElementById('app');
if (!app) return;

Object.assign(T.en, {
  b_mode: 'Reading mode:', m_reader: 'Pāḷi reader', m_printed: 'As printed', m_custom: 'custom',
  d_reader: 'Pāḷi in roman, labels as printed, romanised; Burmese definition folded away.',
  d_printed: 'As the book has it: Burmese script, printed labels, the printed page.',
  settings: 'Settings', done: 'Done', page_on: 'Hide the printed page', page_off: 'Show the printed page',
  s_script: 'Script for Pāḷi', s_defs: 'Burmese definition', s_labels: 'Grammatical labels', s_page: 'Printed page',
  o_ro: 'roman', o_my: 'Burmese', o_both: 'both', o_show: 'show', o_collapse: 'fold away', o_hide: 'hide',
  o_printed: 'as printed', o_abbr: 'abbreviated', o_full: 'spelled out', o_on: 'on', o_off: 'off',
  alphabet: 'Pāḷi alphabet', after: x => `After ${x}`, syll: 'Syllables', words: 'Headwords', earlier: '↑ earlier', later: '↓ later',
  open_alpha: 'Alphabet', close: 'Close', in_vols: v => `In vols. ${v}`, entries: 'entries',
  analysis: 'Analysis', see: 'See', meaning: 'Meaning', not_translated: 'not yet translated',
  trans_note: 'This definition has not been translated yet. The translation will appear here with its status (drafted, reviewed, corrected).',
  drafted_note: 'Drafted translation: not reviewed. Not a reading.',
  partial_note: s => `Corrected by the editor: sense ${s}. The rest is a draft, not reviewed.`,
  rpartial_note: s => `Reviewed by the editor: sense ${s}. The rest is a draft, not reviewed.`,
  edited_on: d => `Edited by the editor on ${d}.`,
  show_def: 'Show the Burmese definition', hide_def: 'Hide the Burmese definition', my_def: 'Burmese definition',
  ocrnote: 'Machine-read Burmese (OCR), unchecked. Compare the printed page before quoting.',
  quotes: 'Pāḷi passages quoted', quotes_note: 'Picked out of the definition by machine; their references are among the citations.',
  cit_vp: (v, p) => `vol. ${v}, p. ${p}`, cit_p: p => `p. ${p}`, cit: 'Citations', cit_unknown: 'abbreviation not yet identified', cit_list: 'in the list of works', cit_draft: 'table drafted, not reviewed',
  scan: 'Printed page', see_page: 'See the printed page', page_view: 'Page view', close_scan: 'Close the printed page',
  prev_page: 'Previous page', next_page: 'Next page', img_none: 'This page image is not available.',
  fuzzy: 'located approximately', unlocated_h: 'Not found in the machine reading',
  unlocated_p: 'The index places this headword on this page, but the OCR text did not yield its article (it is often inside the article before). The printed page shows it.',
  ocr_st: 'ocr · unchecked', loading: 'Loading…', load_fail: 'This part of the dictionary did not load. Reload the page to try again.',
  not_found_w: w => `No headword “${w}” was found.`, results_none: 'No headword matches. Roman letters ignore diacritics (nana finds ñāṇa); Burmese is matched as typed.',
  results_more: 'Type more of the word to narrow the list.', report: 'Report an error', vol_short: 'vol.', pdf_p: 'PDF p.', print_p: 'p.',
  label_unknown: 'label not yet identified', printed_as: 'printed', lab_prov: 'provisional',
  hw_fixed: 'headword corrected; the index spells it', homonym: 'homonym', misfiled: 'the index files this headword on another page',
  pced_t: 'From the typed text of this dictionary in the Pali Canon E-Dictionary (PCED), not from our OCR.',
  corrected_f: 'corrected', corrected_t: 'Corrected by hand against the printed page; the rest of the article is unchecked OCR.',
  panes_hide: 'Hide index', panes_show: 'Show index', panes_t: 'Hide or show the alphabet and the headword list',
  step_prev: 'previous', step_next: 'next', drafted_t: 'machine-drafted, not reviewed', label_nr: 'label not read', analysis_nr: 'analysis not read',
  nr_t: 'The machine reading did not yield this field. Check the printed page: the book may have it, or may not.',
  homs: 'homonyms', homs_t: (n, N) => `homonym ${n} of ${N}`,
  cits_note: 'Picked out of the definition by machine; tap one to see the work.',
  show_all_n: n => `show all (${n})`, show_fewer: 'show fewer', show_every: m => `show everything (${m} more)`, hide_noise: 'hide the fragments again',
  noise_t: 'Hidden by default: lines of one word, or mostly dashes, digits or symbols (over 30% non-letters), and citations that are only numbers.',
});
Object.assign(T.es, {
  b_mode: 'Modo de lectura:', m_reader: 'Lector de pāḷi', m_printed: 'Como está impreso', m_custom: 'personalizado',
  d_reader: 'Pāḷi en caracteres latinos, categorías como se imprimen, romanizadas; definición birmana plegada.',
  d_printed: 'Como en el libro: escritura birmana, categorías impresas, página impresa.',
  settings: 'Ajustes', done: 'Listo', page_on: 'Ocultar la página impresa', page_off: 'Mostrar la página impresa',
  s_script: 'Escritura del pāḷi', s_defs: 'Definición birmana', s_labels: 'Categorías gramaticales', s_page: 'Página impresa',
  o_ro: 'latina', o_my: 'birmana', o_both: 'ambas', o_show: 'mostrar', o_collapse: 'plegar', o_hide: 'ocultar',
  o_printed: 'como se imprimen', o_abbr: 'abreviadas', o_full: 'completas', o_on: 'sí', o_off: 'no',
  alphabet: 'Alfabeto pāḷi', after: x => `Después de ${x}`, syll: 'Sílabas', words: 'Entradas', earlier: '↑ anteriores', later: '↓ siguientes',
  open_alpha: 'Alfabeto', close: 'Cerrar', in_vols: v => `En los vols. ${v}`, entries: 'entradas',
  analysis: 'Análisis', see: 'Véase', meaning: 'Significado', not_translated: 'sin traducir',
  trans_note: 'Esta definición aún no se ha traducido. La traducción aparecerá aquí con su estado (borrador, revisada, corregida).',
  drafted_note: 'Traducción en borrador: sin revisar. No es una lectura.',
  partial_note: s => `Corregido por el editor: sentido ${s}. El resto es borrador, sin revisar.`,
  rpartial_note: s => `Revisado por el editor: sentido ${s}. El resto es borrador, sin revisar.`,
  edited_on: d => `Editado por el editor el ${d}.`,
  show_def: 'Mostrar la definición birmana', hide_def: 'Ocultar la definición birmana', my_def: 'Definición birmana',
  ocrnote: 'Birmano leído por máquina (OCR), sin revisar. Compare con la página impresa antes de citar.',
  quotes: 'Pasajes pāḷi citados', quotes_note: 'Extraídos por máquina de la definición; sus referencias están entre las citas.',
  cit_vp: (v, p) => `tomo ${v}, página ${p}`, cit_p: p => `página ${p}`, cit: 'Citas', cit_unknown: 'abreviatura aún no identificada', cit_list: 'en la lista de obras', cit_draft: 'tabla en borrador, sin revisar',
  scan: 'Página impresa', see_page: 'Ver la página impresa', page_view: 'Vista de página', close_scan: 'Cerrar la página impresa',
  prev_page: 'Página anterior', next_page: 'Página siguiente', img_none: 'La imagen de esta página no está disponible.',
  fuzzy: 'localizada aproximadamente', unlocated_h: 'No encontrada en la lectura automática',
  unlocated_p: 'El índice sitúa esta entrada en esta página, pero el texto del OCR no dio su artículo (a menudo está dentro del anterior). La página impresa lo muestra.',
  ocr_st: 'ocr · sin revisar', loading: 'Cargando…', load_fail: 'Esta parte del diccionario no se cargó. Recargue la página para intentarlo de nuevo.',
  not_found_w: w => `No se encontró la entrada «${w}».`, results_none: 'Ninguna entrada coincide. En letras latinas no cuentan los diacríticos (nana encuentra ñāṇa); el birmano se busca tal como se escribe.',
  results_more: 'Escriba más de la palabra para acotar la lista.', report: 'Informar de un error', vol_short: 'vol.', pdf_p: 'p. del PDF', print_p: 'p.',
  label_unknown: 'categoría aún no identificada', printed_as: 'impreso', lab_prov: 'provisional',
  hw_fixed: 'entrada corregida; el índice la escribe', homonym: 'homónimo', misfiled: 'el índice registra esta entrada en otra página',
  pced_t: 'Del texto mecanografiado de este diccionario en el Pali Canon E-Dictionary (PCED), no de nuestro OCR.',
  corrected_f: 'corregido', corrected_t: 'Corregido a mano sobre la página impresa; el resto del artículo es OCR sin revisar.',
  panes_hide: 'Ocultar índice', panes_show: 'Mostrar índice', panes_t: 'Ocultar o mostrar el alfabeto y la lista de entradas',
  step_prev: 'anterior', step_next: 'siguiente', drafted_t: 'borrador automático, sin revisar', label_nr: 'etiqueta no leída', analysis_nr: 'análisis no leído',
  nr_t: 'La lectura automática no dio este campo. Consulte la página impresa: puede que el libro lo tenga o que no.',
  homs: 'homónimos', homs_t: (n, N) => `homónimo ${n} de ${N}`,
  cits_note: 'Extraídas por máquina de la definición; toque una para ver la obra.',
  show_all_n: n => `mostrar todo (${n})`, show_fewer: 'mostrar menos', show_every: m => `mostrarlo todo (${m} más)`, hide_noise: 'volver a ocultar los fragmentos',
  noise_t: 'Ocultas de entrada: las líneas de una sola palabra, o que son sobre todo guiones, cifras o símbolos (más de un 30% de caracteres que no son letras), y las citas que son solo números.',
});

// --- settings (per browser) ------------------------------------------------------------------------
const MODES = { reader: { script: 'ro', defs: 'collapse', labels: 'printed', scan: false },
                printed: { script: 'my', defs: 'show', labels: 'printed', scan: true } };
let S = Object.assign({ mode: 'reader' }, MODES.reader);
try { const s = JSON.parse(localStorage.getItem('browse') || 'null');
      if (s && s.mode) S = Object.assign(S, s, MODES[s.mode] || {}); } catch (e) {}   // a named mode takes its current defaults
const phone = () => window.matchMedia('(max-width: 760px)').matches;
if (phone()) S.scan = false;
function save() { try { localStorage.setItem('browse', JSON.stringify(S)); } catch (e) {} document.documentElement.dataset.script = S.script; }
function setMode(m) { S = Object.assign({ mode: m }, MODES[m]); if (phone()) S.scan = false; save(); renderAll(); }
function setOne(k, v) { S[k] = v; S.mode = 'custom'; save(); renderAll(); }
save();
let PANES_OFF = false;   // alphabet + headword list hidden (desktop); a layout choice, kept apart from the reading mode
try { PANES_OFF = localStorage.getItem('browse-panes') === 'off'; } catch (e) {}
function setPanes(off) { PANES_OFF = off; try { localStorage.setItem('browse-panes', off ? 'off' : 'on'); } catch (e) {} modebar(); }

// --- the alphabet, as tools/abhidhana_browse.py computes it ---------------------------------------
const LETTERS = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'o', 'k', 'kh', 'g', 'gh', 'ṅ', 'c', 'ch', 'j', 'jh', 'ñ', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ',
  't', 'th', 'd', 'dh', 'n', 'p', 'ph', 'b', 'bh', 'm', 'y', 'r', 'l', 'v', 's', 'h', 'ḷ'];
const VOW = new Set(['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'o']);
const TOK = new RegExp([...LETTERS, 'ṁ'].sort((a, b) => b.length - a.length).map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
function letters(s) { return ((s || '').normalize('NFC').toLowerCase().replace(/ṃ/g, 'ṁ').match(TOK) || []); }
function keysOf(r) {
  const L = letters(r); if (!L.length) return null;
  const li = LETTERS.indexOf(L[0]); if (li < 0) return null;
  let nv = 0, k = 0;
  for (k = 0; k < L.length; k++) if (VOW.has(L[k]) && ++nv === 2) break;
  return { li, g: L.slice(0, 2).join(''), s: nv >= 2 ? L.slice(0, k + 1).join('') : L.join('') };
}
const MYL = { 'အ': [0, 1], 'ဣ': [2], 'ဤ': [3], 'ဥ': [4], 'ဦ': [5], 'ဧ': [6], 'ဩ': [7], 'က': [8], 'ခ': [9], 'ဂ': [10], 'ဃ': [11], 'င': [12],
  'စ': [13], 'ဆ': [14], 'ဇ': [15], 'ဈ': [16], 'ဉ': [17], 'ည': [17], 'ဋ': [18], 'ဌ': [19], 'ဍ': [20], 'ဎ': [21], 'ဏ': [22], 'တ': [23], 'ထ': [24],
  'ဒ': [25], 'ဓ': [26], 'န': [27], 'ပ': [28], 'ဖ': [29], 'ဗ': [30], 'ဘ': [31], 'မ': [32], 'ယ': [33], 'ရ': [34], 'လ': [35], 'ဝ': [36],
  'သ': [37], 'ဟ': [38], 'ဠ': [39] };

// --- data, loaded on demand ------------------------------------------------------------------------
const cache = new Map();
function get(url) {
  if (!cache.has(url)) cache.set(url, fetch(url).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .catch(e => { cache.delete(url); throw e; }));
  return cache.get(url);
}
let NAV = null, LABS = new Map(), ABBR = [];
const navL = li => get(`/data/nav/${li}.json`);
const chunk = c => get(`/data/c/${c}.json`);
const shard = li => get(`/data/s/${li}.json`);

// --- the editor's edits, laid over the static data (docs/editor-mode.md) ----------------------------
// /api/edits?book=NN gives the latest saved edit per id + field + sense (functions/api/edits.js). Each
// book is asked for once, when one of its articles is first shown; until the answer comes, or if the
// request fails (no API, network), the static data are shown as they are.
const EDX = new Map();   // book -> Map(id -> [edit rows]) once loaded; null while loading or failed
function editsOf(book) {
  if (EDX.has(book)) return EDX.get(book);
  EDX.set(book, null);
  fetch(`/api/edits?book=${encodeURIComponent(book)}`).then(r => r.ok ? r.json() : null).then(j => {
    if (!j || !Array.isArray(j.edits)) return;
    setEdits(book, j.edits);
    if (NAV && cur.recs.some(d => d.k === book)) { words(); article(); }
  }).catch(() => {});
  return null;
}
function setEdits(book, rows, id) {   // all of a book's rows, or (id given) the rows of one article
  const M = EDX.get(book) || new Map();
  if (id != null) M.delete(id);
  for (const e of rows) { if (!M.has(e.id)) M.set(e.id, []); M.get(e.id).push(e); }
  EDX.set(book, M);
}
// a record with its edits applied (a copy; the static record is left as it was)
function ov(d) {
  if (!d) return d;
  const M = editsOf(d.k), E = M && M.get(d.i);
  if (!E || !E.length) return d;
  const o = Object.assign({}, d), cf = new Set(d.cf || []), last = {};
  o.static = d; o.ed = {};
  for (const e of E) {
    if (e.field === 'status') continue;
    o.ed[e.field] = e; cf.add(e.field);
    if (e.field === 'headword') { if (!d.hi) o.hi = d.h; o.h = e.value; if (typeof ROMAN !== 'undefined') o.r = ROMAN.headword(e.value); }
    else if (e.field === 'label') { o.l = e.value; delete o.lo; }
    else if (e.field === 'analysis') { o.a = e.value; delete o.ad; delete o.as; o.ai = typeof ROMAN !== 'undefined' ? ROMAN.analysis(e.value) : ''; }
    else if (e.field === 'body') { o.b = e.value; delete o.sp; }   // the Pāḷi spans were offsets into the old text
    else if (e.field === 'es' || e.field === 'en') {
      o.t = Object.assign({}, o.t); o.t[e.field] = { x: e.value, s: 'corrected', date: e.date }; last[e.field] = e.date;
    }
  }
  o.cf = [...cf].filter(f => !['es', 'en'].includes(f));
  // the status of the Spanish: the newest whole-Meaning row, then any per-sense rows newer than it
  const st = E.filter(e => e.field === 'status');
  if (st.length && o.t && o.t.es) {
    const whole = st.filter(e => !e.sense).sort((a, b) => a.date < b.date ? 1 : -1)[0];
    const base = whole && (!last.es || whole.date >= last.es) ? whole : null;
    const es = Object.assign({}, o.t.es);
    if (base) { es.s = base.value; es.date = base.date; delete es.cs; }
    const since = base ? base.date : (last.es || '');
    const per = st.filter(e => e.sense && e.date >= since);
    const corr = per.filter(e => e.value === 'corrected').flatMap(e => e.sense.split(',').map(Number));
    const rev = per.filter(e => e.value === 'reviewed').flatMap(e => e.sense.split(',').map(Number));
    if (corr.length) { es.s = 'partial'; es.cs = [...new Set(corr)].sort((a, b) => a - b); es.date = per[per.length - 1].date; }
    else if (rev.length && es.s === 'drafted') { es.s = 'rpartial'; es.cs = [...new Set(rev)].sort((a, b) => a - b); es.date = per[per.length - 1].date; }
    o.t = Object.assign({}, o.t, { es });
  }
  return o;
}
window.ABH = { ov, setEdits, current: () => cur.recs[cur.k], rows: (book, id) => (EDX.get(book) || new Map()).get(id),
  rerender: () => { words(); article(); } };   // for assets/editor.js

// --- state ----------------------------------------------------------------------------------------
let cur = { li: 0, gi: 0, si: 0, recs: [], k: 0, off: 0 };   // the syllable shown and the entry in it
const FRESH = { label: false, def: false, cit: -1, scanDelta: 0, qall: false, qevery: false, call: false, cevery: false };   // per article
let open = Object.assign({ drawer: false, settings: false }, FRESH);
const W = 160;

async function subRecords(li, gi, si) {
  const G = (await navL(li))[gi]; const sub = G.subs[si];
  const parts = await Promise.all(sub.c.map(chunk));
  const out = [];
  for (const part of parts) for (const d of part) { const kk = keysOf(d.r); if (kk && kk.g === G.k && kk.s === sub.k) out.push(d); }
  out.sort((a, b) => a.g - b.g);
  return out;
}
async function show(li, gi, si, pick) {
  $('art').innerHTML = `<p class="muted">${esc(t('loading'))}</p>`;
  try {
    const recs = await subRecords(li, gi, si);
    let k = 0;
    if (typeof pick === 'string') k = Math.max(0, recs.findIndex(d => d.sl === pick));
    else if (pick === 'last') k = recs.length - 1;
    cur = { li, gi, si, recs, k, off: Math.max(0, Math.floor(k / W) * W) };
    open = Object.assign(open, FRESH, { drawer: false });
    await renderAll(true);
  } catch (e) { $('art').innerHTML = `<p class="muted">${esc(t('load_fail'))}</p>`; }
}
async function gotoSlug(slug, push) {
  const r = decodeURIComponent(slug).replace(/-\d+$/, '');
  const kk = keysOf(r);
  const tryIn = async li => {
    const rows = await shard(li); const row = rows.find(x => x[0] === decodeURIComponent(slug));
    if (!row) return false;
    const nav = await navL(li); const kk2 = keysOf(row[1]);
    const gi = nav.findIndex(G => G.k === kk2.g), si = gi >= 0 ? nav[gi].subs.findIndex(s => s.k === kk2.s) : -1;
    if (si < 0) return false;
    await show(li, gi, si, row[0]); return true;
  };
  try {
    if (kk && await tryIn(kk.li)) { if (push) route(); return; }
  } catch (e) {}
  $('art').innerHTML = `<p class="muted">${esc(t('not_found_w', decodeURIComponent(slug)))}</p>`;
}
function route(replace) {
  const d = cur.recs[cur.k]; if (!d) return;
  const url = '/w/' + encodeURIComponent(d.sl).replace(/%2F/g, '/');
  if (location.pathname !== url) history[replace ? 'replaceState' : 'pushState'](null, '', url);
  document.title = `${d.r || d.h} — Tipiṭaka Pāḷi-Myanmā Abhidhāna`;
}

// --- rendering ------------------------------------------------------------------------------------
const vn = id => (volOf(id) || { n: id }).n;
const pageStr = (id, p) => { const q = printedP(id, p); return (q ? `${t('print_p')} ${q} · ` : '') + `${t('pdf_p')} ${p}`; };
const seg = (on, label, data) => `<button type="button" ${data} aria-pressed="${on}" class="${on ? 'on' : ''}">${esc(label)}</button>`;

function modebar() {
  $('modes').innerHTML = seg(S.mode === 'reader', t('m_reader'), 'data-mode="reader"') + seg(S.mode === 'printed', t('m_printed'), 'data-mode="printed"');
  $('custom').hidden = S.mode !== 'custom'; $('custom').textContent = t('m_custom');
  $('modedesc').textContent = S.mode === 'reader' ? t('d_reader') : S.mode === 'printed' ? t('d_printed') : '';
  $('scanbtn').textContent = S.scan ? t('page_on') : t('page_off'); $('scanbtn').setAttribute('aria-pressed', S.scan);
  const opt = (k, pairs) => pairs.map(([v, l]) => seg(S[k] === v, t(l), `data-set="${k}" data-val="${v}"`)).join('');
  $('settings').innerHTML = [
    ['s_script', opt('script', [['ro', 'o_ro'], ['my', 'o_my'], ['both', 'o_both']])],
    ['s_defs', opt('defs', [['show', 'o_show'], ['collapse', 'o_collapse'], ['hide', 'o_hide']])],
    ['s_labels', opt('labels', [['printed', 'o_printed'], ['abbr', 'o_abbr'], ['full', 'o_full']])],
    ['s_page', [[true, 'o_on'], [false, 'o_off']].map(([v, l]) => seg(S.scan === v, t(l), `data-set="scan" data-val="${v}"`)).join('')],
  ].map(([l, h]) => `<div class="set"><div class="set-l">${esc(t(l))}</div><div class="set-o" role="group" aria-label="${esc(t(l))}">${h}</div></div>`).join('') +
    `<button type="button" class="done" data-done>${esc(t('done'))}</button>`;
  $('settings').hidden = !open.settings; app.classList.toggle('set-open', open.settings);   // phones: the mode bar folds behind Ajustes
  const pb = $('panesbtn'); pb.textContent = PANES_OFF ? t('panes_show') : t('panes_hide'); pb.title = t('panes_t');
  pb.setAttribute('aria-pressed', PANES_OFF); app.classList.toggle('panes-off', PANES_OFF);
  document.documentElement.dataset.script = S.script;
}

async function alpha() {
  const letters = NAV.letters;
  $('letters').innerHTML = letters.map((L, i) =>
    `<button type="button" class="lt${i === cur.li ? ' on' : ''}" data-li="${i}" title="${esc(t('in_vols', L.books.map(vn).join(', ')))} · ${L.n.toLocaleString(LANG)} ${esc(t('entries'))}">` +
    `<span class="my" lang="my">${esc(L.my)}</span><span class="pl" lang="pi">${esc(L.ro)}</span></button>`).join('');
  const L = letters[cur.li];
  $('lnote').textContent = `${t('in_vols', L.books.map(vn).join(', '))} · ${L.n.toLocaleString(LANG)} ${t('entries')}`;
  const nav = await navL(cur.li), G = nav[cur.gi];
  $('after').textContent = t('after', L.ro);
  $('groups').innerHTML = nav.map((g, i) => `<button type="button" class="ch${i === cur.gi ? ' on' : ''}" data-gi="${i}"><span class="pl" lang="pi">${esc(g.k)}-</span></button>`).join('');
  $('syll').textContent = t('syll');
  $('subs').innerHTML = G.subs.map((s, i) => `<button type="button" class="ch${i === cur.si ? ' on' : ''}" data-si="${i}"><span class="pl" lang="pi">${esc(s.k)}-</span><span class="n">${s.n}</span></button>`).join('');
}

function hwLabel(d) {
  if (S.script === 'my') return `<span class="my" lang="my">${esc(d.h)}</span>`;
  if (S.script === 'both') return `<span class="pl" lang="pi">${esc(d.r)}</span> <span class="my sub" lang="my">${esc(d.h)}</span>`;
  return `<span class="pl" lang="pi">${esc(d.r)}</span>`;
}
function words() {
  const recs = cur.recs, a = cur.off, b = Math.min(recs.length, a + W);
  $('wearlier').hidden = a <= 0; $('wlater').hidden = b >= recs.length;
  $('wlist').innerHTML = recs.slice(a, b).map((d0, j) => {
    const k = a + j, d = ov(d0);
    return `<a class="w${k === cur.k ? ' on' : ''}" href="/w/${encodeURIComponent(d.sl)}" data-k="${k}" title="${esc(d.r || d.h)}"${k === cur.k ? ' aria-current="true"' : ''}>${hwLabel(d)}${d.hn ? `<sup>${d.hn}</sup>` : ''}</a>`;
  }).join('');
  const on = $('wlist').querySelector('.on'); if (on) on.scrollIntoView({ block: 'nearest' });
}

// labels: docs/labels.md §0 (published as /data/labels.json)
function labelParts(l) { return (l || '').split(/[၊,]\s*/).filter(Boolean); }
function labelShown(d) {
  const L = LABS.get(d.l);
  if (S.labels === 'printed') {   // the printed label, in the script chosen for Pāḷi: (ti) / (တိ)
    const my = `<span class="my" lang="my">(${esc(d.l)})</span>`, ro = L && L.roman ? `<span lang="pi">${esc(L.roman)}</span>` : '';
    return S.script === 'my' || !ro ? my : S.script === 'both' ? `${ro} ${my}` : ro;
  }
  const txt = L ? (S.labels === 'full' ? (L[LANG] || L.en) : (L['abbr_' + LANG] || L[LANG] || L.en)) : `(${d.l})`;
  return `<span lang="${L ? LANG : 'my'}" class="${L ? '' : 'my'}">${esc(txt)}</span>`;
}
function labelInfo(d) {
  const L = LABS.get(d.l);
  if (!L) return `<div class="note"><span class="my" lang="my">(${esc(d.l)})</span> — ${esc(t('label_unknown'))}</div>`;
  const prov = L.status === 'provisional' || (LANG === 'es' && L.es_status !== 'confirmed');
  return `<div class="note"><strong>${esc(L[LANG] || L.en)}</strong>${L.pali ? ` — <span class="pl" lang="pi"><i>${esc(L.pali)}</i></span>` : ''} · ${esc(t('printed_as'))} <span class="my" lang="my">(${esc(d.l)})${L.printed ? ' ' + esc(L.printed) : ''}</span>` +
    `${prov ? ` <span class="chip c-warn">${esc(t('lab_prov'))}</span>` : ''} <a href="/abbreviations/#l${L.k}">↗</a>` +
    (d.lo ? `<div class="muted small">OCR: <span class="my" lang="my">(${esc(d.lo)})</span></div>` : '') + '</div>';
}
// the Burmese definition with its Pāḷi spans in the chosen script
function defHTML(d) {
  // the Pāḷi spans in the definition, romanised; a "see X" span (d.see) links to X's article
  const b = d.b || ''; if (!d.sp) return esc(b);
  const SEE = new Map((d.see || []).map(([r, sl]) => [r, sl]));
  const link = (r, inner) => SEE.has(r) ? `<a class="xref" href="/w/${encodeURIComponent(SEE.get(r))}">${inner}</a>` : inner;
  let out = '', k = 0;
  for (const [s, e, r] of d.sp) {
    out += esc(b.slice(k, s));
    const my = esc(b.slice(s, e));
    out += S.script === 'my' ? link(r, my)
      : S.script === 'both' ? link(r, `<span class="pali-my" lang="my">${my}</span> <span class="pali" lang="pi">(${esc(r)})</span>`)
      : link(r, `<span class="pali" lang="pi" title="${my}">${esc(r)}</span>`);
    k = e;
  }
  return out + esc(b.slice(k));
}
// a citation's expansion for its tooltip: the work (docs/introduction/citation-abbreviations.tsv) and,
// read from the reference, volume and page (ဒီ၊ဋီ၊၂။၁၂။ -> Dīgha Ṭīkā · vol. 2, p. 12)
function citeTip(d, j) {
  const x = d.cx ? d.cx[j] : -1, A = x >= 0 ? ABBR[x] : null;
  if (!A) return '';
  const n = (d.c[j].replace(/[၀-၉]/g, c => '၀၁၂၃၄၅၆၇၈၉'.indexOf(c)).match(/\d+(?:\s*[-–]\s*\d+)?/g) || []).map(v => v.replace(/\s+/g, ''));
  const loc = n.length === 2 ? t('cit_vp', n[0], n[1]) : n.length === 1 ? t('cit_p', n[0]) : n.join('.');
  return A.work + (loc ? ' · ' + loc : '');
}
function reportURL(d) {
  const link = `${location.origin}/w/${encodeURIComponent(d.sl)}`;
  const title = `Error: vol. ${vn(d.kb || d.k)}, PDF p. ${d.p}, ${d.h} (id ${d.i})`;
  const body = `**Volume:** ${vn(d.kb || d.k)}${d.kb ? ` (supplement bound in vol. ${vn(d.k)})` : ''} (book \`${d.k}\`)\n**PDF page:** ${d.p} · **printed page:** ${d.q}\n**Headword:** ${d.h} (${d.r})\n**Article id:** ${d.i}\n**Link:** ${link}\n\n**What is wrong** (and, if you can, what the printed page says):\n\n`;
  return `${REPO}/issues/new?labels=error-report&title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}
// --- Copy / Cite / Share (brief §81), modelled on the Reader of buddha-dhamma.net (reader2.html: icon buttons,
// navigator.clipboard, a short flash). Plain text, one field per line, built from the record as shown (edits laid over).
// The address is always the public site's, so a copy made anywhere cites the same place.
const SITE = 'https://abhidhana.buddha-dhamma.net';
let VER = (document.querySelector('meta[name="version"]') || {}).content || '';
fetch('/data/version.json').then(r => r.ok ? r.json() : null).then(j => { if (j && j.version) VER = j.version; }).catch(() => {});
const SUPN = n => String(n).replace(/\d/g, c => '⁰¹²³⁴⁵⁶⁷⁸⁹'[c]);
const wURL = d => `${SITE}/w/${d.sl}`;                                          // as read (the citation, the copy)
const wHref = d => `${SITE}/w/${encodeURIComponent(d.sl).replace(/%2F/g, '/')}`;   // as sent (share, the copied link)
const one = s => String(s || '').replace(/\s+/g, ' ').trim();
const plainTr = x => (x || '').replace(/\[\[([^\]|]+)\|[^\]]*\]\]/g, '$1').replace(/\[\[([^\]]+)\]\]/g, '$1')
  .replace(/\*([^*]+)\*/g, '$1').replace(/‹([^›]+)›/g, '$1');
function today() { const n = new Date(); return `${n.getDate()} ${t('months')[n.getMonth()]} ${n.getFullYear()}`; }
function copyText(d) {
  const hn = d.hn ? SUPN(d.hn) : '', L = [];
  L.push(d.r ? `${d.r}${hn} · ${d.h}${hn}` : `${d.h}${hn}`);
  if (d.l) {
    const B = LABS.get(d.l);
    L.push(`${t('cp_label')}: ` + (B ? `${B.roman ? B.roman.replace(/^\((.*)\)$/, '$1') + ' ' : ''}(${d.l}) — ${B[LANG] || B.en}` : `(${d.l})`));
  }
  if (d.a || d.ai) L.push(`${t('cp_analysis')}: ` + [d.ai && `[${d.ai}]`, d.a && `[${d.a}]`].filter(Boolean).join(' '));
  const tr = d.t && d.t[LANG];
  if (tr) {
    let st = t('st_' + tr.s);
    if (tr.s === 'drafted') st += ', ' + t('cp_unreviewed');
    if (tr.s === 'partial' || tr.s === 'rpartial') st += `: ${t('cp_sense', (tr.cs || []).map(n => `(${n})`).join(', '))}; ${t('cp_rest')}`;
    L.push(`${t('cp_meaning')} (${st}): ${one(plainTr(tr.x))}`);
  } else L.push(`${t('cp_meaning')}: ${t('not_translated')}`);
  if (d.b) L.push(`${t('cp_def')}; ${t((d.cf || []).includes('body') ? 'cp_def_fixed' : 'cp_def_ocr')}: ${one(d.b)}`);
  L.push(t('cp_attr', wURL(d)));
  return L.join('\n');
}
function citeText(d) {
  const q = printedP(d.k, d.p), pg = q ? `${t('print_p')} ${q} (${t('pdf_p')} ${d.p})` : `${t('pdf_p')} ${d.p}`;
  return `Tipiṭaka Pāḷi-Myanmā Abhidhāna, ${t('vol_short')} ${volLabel(d.k, d.kb)}, ${pg}, s.v. ${d.r || d.h}${d.hn ? SUPN(d.hn) : ''}. ` +
    `${t('ct_ed')}, IEBH${VER ? ', v' + VER : ''}. ${wURL(d)} (${t('ct_acc', today())}).`;
}
async function clip(s) {
  try { if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(s); return true; } } catch (e) {}
  const f = document.activeElement;   // older browsers, or a page not served over https
  try {
    const ta = document.createElement('textarea'); ta.value = s; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
    document.body.appendChild(ta); ta.select(); const r = document.execCommand('copy'); ta.remove(); if (f && f.focus) f.focus(); return r;
  } catch (e) { return false; }
}
const ICONS = {
  copy: '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false"><rect x="5" y="5" width="8" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M3 10.5V3a1 1 0 0 1 1-1h6" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>',
  cite: '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false"><path d="M6 5H3.5A1.5 1.5 0 0 0 2 6.5V9A1.5 1.5 0 0 0 3.5 10.5H5V11a2 2 0 0 1-2 2M14 5h-2.5A1.5 1.5 0 0 0 10 6.5V9a1.5 1.5 0 0 0 1.5 1.5H13V11a2 2 0 0 1-2 2" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>',
  share: '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false"><path d="M8 10V2M5 4.5 8 1.5l3 3M5 7H3.5A1.5 1.5 0 0 0 2 8.5v4A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5v-4A1.5 1.5 0 0 0 12.5 7H11" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
};
function actsHTML() {
  return `<span class="acts" role="group" aria-label="${esc(t('act_group'))}">` +
    ['copy', 'cite', 'share'].map(k => `<button type="button" class="icn" data-act="${k}" aria-label="${esc(t('act_' + k))}" title="${esc(t('act_' + k))}">${ICONS[k]}</button>`).join('') +
    '<span class="acts-msg" role="status" aria-live="polite"></span></span>';
}
function flash(b, ok, msg) {   // as the Reader: the button shows ✓ for a moment; the message is also read out
  const m = b.parentNode && b.parentNode.querySelector('.acts-msg'), k = b.dataset.act;
  b.classList.remove('ok', 'bad'); b.classList.add(ok ? 'ok' : 'bad');
  b.innerHTML = `<span aria-hidden="true">${ok ? '✓' : '✗'}</span>`;
  if (m) { m.textContent = msg; m.classList.toggle('bad', !ok); }
  clearTimeout(b._ft);
  b._ft = setTimeout(() => { b.classList.remove('ok', 'bad'); b.innerHTML = ICONS[k]; if (m) m.textContent = ''; }, 1500);
}
async function act(k, b) {
  const d = ov(cur.recs[cur.k]); if (!d) return;
  if (k === 'copy') { const r = await clip(copyText(d)); return flash(b, r, t(r ? 'act_copied' : 'act_failed')); }
  if (k === 'cite') { const r = await clip(citeText(d)); return flash(b, r, t(r ? 'act_cited' : 'act_failed')); }
  if (k === 'share') {
    if (navigator.share) {
      try { await navigator.share({ title: `${d.r || d.h} — Tipiṭaka Pāḷi-Myanmā Abhidhāna`, text: citeText(d), url: wHref(d) }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }   // dismissed; any other refusal falls back to the link
    }
    const r = await clip(wHref(d)); return flash(b, r, t(r ? 'act_linked' : 'act_failed'));
  }
}
window.ABH_ACTS = { copyText: () => { const d = ov(cur.recs[cur.k]); return d ? copyText(d) : ''; },
  citeText: () => { const d = ov(cur.recs[cur.k]); return d ? citeText(d) : ''; } };   // for the UI test

// the Meaning box's small markup: *pāḷi* in italics, [[iast|address]] a link to another headword
// ([[iast|]] and [[iast]] in italics),
// ‹…› a Burmese word the draft left untranslated
function fmtTr(x) {
  return esc(x).replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (m, r, sl) => `<a class="pl" lang="pi" href="/w/${encodeURIComponent(sl)}">${r}</a>`)
    .replace(/\[\[([^\]|]+)\|?\]\]/g, '<i class="pl" lang="pi">$1</i>')   // [[x|]]: not a headword; [[x]]: from an edit
    .replace(/\*([^*]+)\*/g, '<i class="pl" lang="pi">$1</i>')
    .replace(/‹([^›]+)›/g, '<span class="my" lang="my">$1</span>');
}
// display only: a quoted line of one word, or mostly dashes, digits or symbols (over 30% of its
// characters not letters), and a citation that is only numbers ("2.50"; "vi 1" names a work and stays),
// are hidden behind "show everything" (the editor, 28 Sep 2026). Nothing in the data changes.
const FOLD = 5;
function noiseQuote(r) {
  const x = (r || '').replace(/\s+/g, ''); if (!x) return true;
  const L = (x.match(/[\p{L}\p{M}]/gu) || []).length;
  const words = (r.match(/[\p{L}\p{M}]+/gu) || []).filter(w => w.length > 1);
  return words.length < 2 || (x.length - L) / x.length > 0.3;
}
const noiseCite = c => !/[\p{L}]/u.test((c || '').replace(/[၀-၉]/g, ''));
// the citations shown as chips wrap into rows: keep the first FOLD rows, the rest behind "show all"
function foldCits() {
  const box = document.querySelector('#art .cits'); if (!box) return;
  const btn = document.querySelector('#art [data-fold="call"]');
  const chips = [...box.children]; chips.forEach(c => c.classList.remove('cut'));
  if (open.call) return;
  const tops = []; let cut = 0;
  for (const c of chips) {
    if (c.offsetParent === null) continue;
    if (!tops.includes(c.offsetTop)) tops.push(c.offsetTop);
    if (tops.length > FOLD) { c.classList.add('cut'); cut++; }
  }
  if (btn) btn.hidden = !cut;
}
let foldTm; window.addEventListener('resize', () => { clearTimeout(foldTm); foldTm = setTimeout(foldCits, 120); });
// "show all (N)" / "show fewer", and "show everything (M more)" when lines were hidden as noise
function foldBar(k, nGood, nNoise) {
  const all = open[k + 'all'] || open[k + 'every'], every = open[k + 'every'], B = [];
  if (k === 'c' || nGood > FOLD) B.push(`<button type="button" data-fold="${k}all"${k === 'c' && !all ? ' hidden' : ''}>${esc(all ? t('show_fewer') : t('show_all_n', nGood))}</button>`);
  if (nNoise) B.push(`<button type="button" data-fold="${k}every" title="${esc(t('noise_t'))}">${esc(every ? t('hide_noise') : t('show_every', nNoise))}</button>`);
  return B.length ? `<div class="fold">${B.join('')}</div>` : '';
}
// the homonyms of this headword (same address but its -n), all in the syllable shown: "homonyms 1 2 3 4"
function homsHTML(d) {
  if (!d.hn) return '';
  const base = d.sl.replace(/-\d+$/, ''), H = cur.recs.filter(x => x.hn && x.sl.replace(/-\d+$/, '') === base);
  if (H.length < 2) return '';
  return `<span class="homs" title="${esc(t('homs_t', d.hn, H.length))}">${esc(t('homs'))}` +
    H.map(x => x.hn === d.hn ? `<b aria-current="true">${x.hn}</b>` : `<a href="/w/${encodeURIComponent(x.sl)}">${x.hn}</a>`).join('') + '</span>';
}
function article() {
  const d = ov(cur.recs[cur.k]);
  if (!d) { $('art').innerHTML = ''; return; }
  const H = [];
  H.push(`<div class="where"><span>${esc(t('vol_short'))} ${esc(volLabel(d.k, d.kb))} · ${esc(pageStr(d.k, d.p))}</span>` +
    `<span class="chip"${d.s === 'drafted' ? ` title="${esc(t('drafted_t'))}"` : ''}>${esc(d.s === 'ocr' ? t('ocr_st') : t('st_' + d.s))}</span>` +
    (d.x === 'f' ? `<span class="chip c-warn">${esc(t('fuzzy'))}</span>` : '') +
    (d.m ? `<span class="chip">${esc(t('misfiled'))}</span>` : '') +
    (d.hi ? `<span class="chip c-ok">${esc(t('hw_fixed'))} <span class="my" lang="my">${esc(d.hi)}</span></span>` : '') + '</div>');
  const ro = S.script !== 'my', my = S.script !== 'ro';
  H.push(`<div class="head">` +
    (ro ? `<h1 class="pl" lang="pi">${esc(d.r)}${d.hn ? `<sup>${d.hn}</sup>` : ''}</h1>` : '') +
    (my ? `<div class="my hw-my${ro ? ' second' : ''}" lang="my">${esc(d.h)}${!ro && d.hn ? `<sup>${d.hn}</sup>` : ''}</div>` : '') +
    actsHTML() +
    (d.l ? `<button type="button" class="lab" data-label aria-expanded="${open.label}">${labelShown(d)}</button>` : '') +
    ((d.cf || []).includes('label') ? ` <span class="chip c-ok" title="${esc(t('corrected_t'))}">${esc(t('corrected_f'))}</span>` : '') +
    homsHTML(d) +
    (d.x !== 'u' && !d.l ? `<span class="notread" title="${esc(t('nr_t'))}">${esc(t('label_nr'))}</span>` : '') +
    (d.ax && !d.a && !d.ai ? `<span class="notread" title="${esc(t('nr_t'))}">${esc(t('analysis_nr'))}</span>` : '') + '</div>');
  if (open.label && d.l) H.push(labelInfo(d));
  if (d.x === 'u') {
    H.push(`<div class="note warn"><strong>${esc(t('unlocated_h'))}</strong><p>${esc(t('unlocated_p'))}</p>` +
      (S.scan ? '' : `<button type="button" data-scan>${esc(t('see_page'))}</button>`) + '</div>');
  }
  if (d.a || d.ai) {
    const fixed = (d.cf || []).includes('analysis') ? ` <span class="chip c-ok" title="${esc(t('corrected_t'))}">${esc(t('corrected_f'))}</span>`
      : '';
    H.push(`<section><h2>${esc(t('analysis'))}${fixed}</h2>` + (ro && d.ai ? `<div class="pl an" lang="pi">[${esc(d.ai)}]</div>` : '') +
      ((my || (ro && d.ad)) && d.a ? `<div class="my an-my" lang="my">[${esc(d.a)}]</div>` : '') + '</section>');
  }
  if (d.see && d.see.length) H.push(`<div class="see"><span class="muted">${esc(t('see'))}</span> ` +
    d.see.map(([r, sl]) => `<a class="pl" lang="pi" href="/w/${encodeURIComponent(sl)}">${esc(r)}</a>`).join(', ') + '</div>');
  // Meaning: the translation with its status, or an honest "not yet translated"
  const tr = d.t && d.t[LANG];
  H.push(`<section><h2>${esc(t('meaning'))}</h2>` + (tr
    ? `<div class="meaning"><span class="chip ${tr.s === 'drafted' || tr.s === 'partial' || tr.s === 'rpartial' ? 'c-warn' : 'c-ok'}"${tr.s === 'drafted' ? ` title="${esc(t('drafted_t'))}"` : ''}>${esc(t('st_' + tr.s))}</span><div lang="${LANG}">${fmtTr(tr.x)}</div>${tr.s === 'drafted' ? `<div class="muted small">${esc(t('drafted_note'))}</div>` : ''}${tr.s === 'partial' || tr.s === 'rpartial' ? `<div class="muted small">${esc(t(tr.s === 'partial' ? 'partial_note' : 'rpartial_note', (tr.cs || []).map(n => `(${n})`).join(', ')))}</div>` : ''}${tr.date ? `<div class="muted small">${esc(t('edited_on', tr.date.slice(0, 10)))}</div>` : ''}</div>`
    : `<div class="meaning empty"><span class="chip">${esc(t('not_translated'))}</span><span>${esc(t('trans_note'))}</span></div>`));
  const showDef = d.b && (S.defs === 'show' || (S.defs === 'collapse' && open.def));
  if (d.b && S.defs === 'collapse' && !open.def) H.push(`<button type="button" class="btn" data-def="1" aria-expanded="false">${esc(t('show_def'))}</button>`);
  if (showDef) {
    H.push((S.defs === 'collapse' ? `<button type="button" class="btn small" data-def="0" aria-expanded="true">${esc(t('hide_def'))}</button>` : '') +
      `<div class="def my" lang="my">${defHTML(d)}</div>` + ((d.cf || []).includes('body')
        ? `<div class="muted small"><span class="chip c-ok">${esc(t('corrected_f'))}</span> ${esc(t('corrected_t'))}</div>`
        : `<div class="muted small">${esc(t('ocrnote'))}</div>`));
  }
  H.push('</section>');
  // Pāḷi passages quoted (when the definition is not shown)
  const seeR = new Set((d.see || []).map(x => x[0]));
  const quotes = (d.sp || []).filter(s => (s[3] || 1) >= 2 && !seeR.has(s[2]));
  if (!showDef && quotes.length) {
    const good = quotes.filter(s => !noiseQuote(s[2])), noise = quotes.length - good.length;
    const shown = open.qevery ? quotes : open.qall ? good : good.slice(0, FOLD);
    H.push(`<section><h2>${esc(t('quotes'))}</h2><div class="muted small listnote">${esc(t('quotes_note'))}</div><ol class="quotes">` +
      shown.map(s => { const n = noiseQuote(s[2]) ? ' noise' : '';
        return S.script === 'my' ? `<li class="my${n}" lang="my">${esc((d.b || '').slice(s[0], s[1]))}</li>` : `<li class="pl${n}" lang="pi">${esc(s[2])}</li>`; }).join('') +
      '</ol>' + foldBar('q', good.length, noise) + '</section>');
  }
  // citations: tap expands the abbreviation to the work (docs/introduction/citation-abbreviations.tsv)
  if (d.c && d.c.length) {
    const cn = d.c.map((c, j) => noiseCite(d.ci ? d.ci[j] : c)), noise = cn.filter(Boolean).length;
    H.push(`<section><h2>${esc(t('cit'))}</h2><div class="muted small listnote">${esc(t('cits_note'))}</div><div class="cits">` + d.c.map((c, j) => {
      if (cn[j] && !open.cevery) return '';
      const lab = S.script === 'my' || !d.ci ? `<span class="my" lang="my">${esc(c)}</span>` : `<span class="pl" lang="pi">${esc(d.ci[j])}</span>`;
      const tip = citeTip(d, j);
      return `<button type="button" class="cit${open.cit === j ? ' on' : ''}${cn[j] ? ' noise' : ''}" data-cit="${j}" aria-expanded="${open.cit === j}"${tip ? ` title="${esc(tip)}"` : ''}>${lab}</button>`;
    }).join('') + '</div>' + foldBar('c', d.c.length - noise, noise));
    if (open.cit >= 0 && open.cit < d.c.length) {
      const x = d.cx ? d.cx[open.cit] : -1, A = x >= 0 ? ABBR[x] : null;
      H.push('<div class="note">' + (A
        ? `<strong class="pl" lang="pi">${esc(A.ro)}</strong> <span class="my" lang="my">(${esc(A.my)})</span> → ${esc(citeTip(d, open.cit))}` +
          ` <span class="muted">· ${esc(t('cit_list'))}: ${esc(LANG === 'es' ? (A.list_es || A.list) : A.list)} ${esc(A.list_no)}${(LANG === 'es' ? A.note_es : A.note_en) ? ' · ' + esc(LANG === 'es' ? A.note_es : A.note_en) : ''}</span>` +
          ` <span class="chip c-warn">${esc(t('cit_draft'))}</span> <a href="/abbreviations/#abbreviations">↗</a>`
        : `<span class="my" lang="my">${esc(d.c[open.cit])}</span> — ${esc(t('cit_unknown'))}`) + '</div>');
    }
    H.push('</section>');
  }
  // previous / next, printed page, report
  const P = cur.k > 0 ? cur.recs[cur.k - 1] : null, N = cur.k < cur.recs.length - 1 ? cur.recs[cur.k + 1] : null;
  H.push(`<div class="artnav"><button type="button" class="btn step" data-step="-1">‹ ${P ? hwLabel(P) : esc(t('step_prev'))}</button>` +
    `<button type="button" class="btn step" data-step="1">${N ? hwLabel(N) : esc(t('step_next'))} ›</button>` +
    (S.scan ? '' : `<button type="button" class="btn" data-scan>${esc(t('see_page'))}</button>`) +
    `<a href="/v/${d.k}/${d.p}#a${d.i}">${esc(t('page_view'))}</a>` +
    `<a class="report" href="${reportURL(d)}" target="_blank" rel="noopener">${esc(t('report'))}</a></div>`);
  $('art').innerHTML = `<article>${H.join('')}</article><footer class="site-foot"></footer>`;
  fillFoot($('art')); foldCits();
  if (window.EDITOR) EDITOR.decorate(d);   // editor mode (assets/editor.js), only when the editor is signed in
}

function scan() {
  const d = cur.recs[cur.k];
  const on = S.scan || (d && d.x === 'u' && !phone() && open.scanForced);
  app.classList.toggle('scan-on', !!S.scan);
  $('scanpane').hidden = !S.scan;
  if (!S.scan || !d) return;
  const p = d.p + open.scanDelta, V = volOf(d.k);
  $('scanwhere').textContent = `${t('vol_short')} ${vn(d.k)} · ${pageStr(d.k, p)}`;
  const url = `${IMG}${d.k}/${String(p).padStart(4, '0')}.webp`, img = $('scanimg');
  $('scanmiss').hidden = true; img.hidden = false;
  img.onerror = () => { img.hidden = true; $('scanmiss').hidden = false; };
  img.alt = `Vol. ${vn(d.k)}, PDF page ${p}`;
  if (img.getAttribute('src') !== url) img.src = url;
  $('scanprev').disabled = p <= 1; $('scannext').disabled = V ? p >= V.pdf_pages : false;
}

async function renderAll(routeIt) {
  modebar();
  try { await alpha(); } catch (e) {}
  words(); article(); scan();
  app.classList.toggle('drawer-open', open.drawer);
  if (routeIt) route(true);
}

async function step(dir) {
  const k = cur.k + dir;
  if (k >= 0 && k < cur.recs.length) { cur.k = k; if (k < cur.off || k >= cur.off + W) cur.off = Math.floor(k / W) * W; open = Object.assign(open, FRESH); await renderAll(); route(); return; }
  // across syllables, groups and letters
  let { li, gi, si } = cur, nav = await navL(li);
  si += dir;
  if (si < 0 || si >= nav[gi].subs.length) {
    gi += dir;
    if (gi < 0 || gi >= nav.length) { li += dir; if (li < 0 || li >= NAV.letters.length) return; nav = await navL(li); gi = dir > 0 ? 0 : nav.length - 1; }
    si = dir > 0 ? 0 : nav[gi].subs.length - 1;
  }
  await show(li, gi, si, dir > 0 ? 'first' : 'last'); route();
}

// --- search: prefix first, then substring; one letter's shard at a time -------------------------
const FL = LETTERS.map(l => fold(l));
async function search(q) {
  const box = $('hresults'); q = q.trim();
  if (!q) { box.hidden = true; return; }
  box.hidden = false; box.innerHTML = `<div class="more">${esc(t('loading'))}</div>`;
  const isMy = /[က-႟]/.test(q), fq = fold(q);
  let lis = isMy ? (MYL[q[0]] || []) : FL.map((l, i) => fq.startsWith(l) ? i : -1).filter(i => i >= 0);
  const scan = async lis => {
    const rows = (await Promise.all(lis.map(shard))).flat();
    const pre = [], sub = [];
    for (const r of rows) {
      const hay = isMy ? r[2] : (r._f || (r._f = fold(r[1])));
      const pos = hay.indexOf(isMy ? q : fq);
      if (pos === 0) pre.push(r); else if (pos > 0) sub.push(r);
    }
    return [pre, sub];
  };
  try {
    let [pre, sub] = await scan(lis);
    if (pre.length < 10 && (isMy ? q.length : fq.length) >= 3) {   // substring across every letter
      const [p2, s2] = await scan(LETTERS.map((_, i) => i));
      const seen = new Set(pre.map(r => r[0]));
      sub = [...s2, ...p2].filter(r => !seen.has(r[0]));
    }
    if (!isMy) {   // among the prefix matches: the typed word itself first, then by closeness to what was typed
      const key = r => [fold(r[1]) === fq ? 0 : 1, dmiss(r[1], q)];
      pre = pre.map((r, n) => [key(r), n, r]).sort((a, b) => a[0][0] - b[0][0] || a[0][1] - b[0][1] || a[1] - b[1]).map(x => x[2]);
    }
    const out = [...pre, ...sub].slice(0, 60);
    if ($('hq').value.trim() !== q) return;
    box.innerHTML = out.map(r => `<a class="res" href="/w/${encodeURIComponent(r[0])}"><span>` +
      (S.script === 'my' ? `<span class="my" lang="my">${esc(r[2])}</span>` : `<span class="pl" lang="pi">${esc(r[1])}</span>${S.script === 'both' ? ` <span class="my sub" lang="my">${esc(r[2])}</span>` : ''}`) +
      `</span><span class="pg">${esc(t('vol_short'))} ${esc(volLabel(r[3], r[6]))} · ${esc(pageStr(r[3], r[4]))}</span></a>`).join('') +
      (out.length ? (pre.length + sub.length > 60 ? `<div class="more">${esc(t('results_more'))}</div>` : '') : `<div class="more">${esc(t('results_none'))}</div>`);
  } catch (e) { box.innerHTML = `<div class="more">${esc(t('load_fail'))}</div>`; }
}

// --- events ---------------------------------------------------------------------------------------
app.addEventListener('click', async e => {
  const el = e.target.closest('button, a'); if (!el) return;
  const ds = el.dataset;
  if (ds.act) return act(ds.act, el);
  if (ds.mode) return setMode(ds.mode);
  if (ds.set) return setOne(ds.set, ds.set === 'scan' ? ds.val === 'true' : ds.val);
  if ('done' in ds) { open.settings = false; return modebar(); }
  if (el.id === 'setbtn') { open.settings = !open.settings; el.setAttribute('aria-expanded', open.settings); return modebar(); }
  if (el.id === 'scanbtn' || 'scan' in ds) { if (phone() && !S.scan) { S.scan = true; save(); return renderAll(); } return setOne('scan', !S.scan); }
  if (el.id === 'scanclose') { if (phone()) { S.scan = false; save(); return renderAll(); } return setOne('scan', false); }
  if (el.id === 'scanprev') { open.scanDelta--; return scan(); }
  if (el.id === 'scannext') { open.scanDelta++; return scan(); }
  if (el.id === 'panesbtn') return setPanes(!PANES_OFF);
  if (el.id === 'alphabtn') { open.drawer = !open.drawer; return app.classList.toggle('drawer-open', open.drawer); }
  if (el.id === 'drawerclose') { open.drawer = false; return app.classList.remove('drawer-open'); }
  if (ds.li) { const li = +ds.li; await show(li, 0, 0, 'first'); open.drawer = phone(); app.classList.toggle('drawer-open', open.drawer); return route(); }
  if (ds.gi) { await show(cur.li, +ds.gi, 0, 'first'); open.drawer = phone(); app.classList.toggle('drawer-open', open.drawer); return route(); }
  if (ds.si) { await show(cur.li, cur.gi, +ds.si, 'first'); open.drawer = phone(); app.classList.toggle('drawer-open', open.drawer); return route(); }
  if (ds.k) { e.preventDefault(); cur.k = +ds.k; open = Object.assign(open, FRESH, { drawer: false }); await renderAll(); $('art').scrollTop = 0; return route(); }
  if (el.id === 'wearlier') { cur.off = Math.max(0, cur.off - W); return words(); }
  if (el.id === 'wlater') { cur.off += W; return words(); }
  if ('label' in ds) { open.label = !open.label; return article(); }
  if (ds.def) { open.def = ds.def === '1'; return article(); }
  if (ds.fold) {   // qall / qevery / call / cevery; "show fewer" folds both back
    const k = ds.fold[0], w = ds.fold.slice(1);
    if (w === 'all') { const was = open[k + 'all'] || open[k + 'every']; open[k + 'all'] = !was; if (was) open[k + 'every'] = false; }
    else { open[k + 'every'] = !open[k + 'every']; if (open[k + 'every']) open[k + 'all'] = true; }
    return article();
  }
  if (ds.cit) { const j = +ds.cit; open.cit = open.cit === j ? -1 : j; return article(); }
  if (ds.step) return step(+ds.step);
  if (el.matches('a[href^="/w/"]')) { e.preventDefault(); $('hresults').hidden = true; await gotoSlug(el.getAttribute('href').slice(3), true); route(); window.scrollTo({ top: 0 }); }
});
document.addEventListener('click', e => {   // search results live in the header, outside #app
  const a = e.target.closest('#hresults a.res');
  if (a) { e.preventDefault(); $('hresults').hidden = true; gotoSlug(a.getAttribute('href').slice(3), true).then(() => route()); }
  else if (!e.target.closest('#hresults, #hq')) $('hresults').hidden = true;
});
let tm;
$('hq').addEventListener('input', () => { clearTimeout(tm); tm = setTimeout(() => search($('hq').value), 180); });
$('hq').addEventListener('keydown', e => {
  if (e.key === 'Enter') { e.preventDefault(); const a = $('hresults').querySelector('a.res'); if (a) a.click(); }
  if (e.key === 'Escape') { $('hq').value = ''; $('hresults').hidden = true; }
});
$('hq').closest('form').addEventListener('submit', e => e.preventDefault());
document.addEventListener('keydown', e => {
  if (e.target.matches('input,select,textarea')) return;
  if (e.key === '/') { e.preventDefault(); $('hq').focus(); }
  if (e.key === '\\' && !phone()) { e.preventDefault(); setPanes(!PANES_OFF); }
  if (e.key === 'ArrowDown' || e.key === 'j') { e.preventDefault(); step(1); }
  if (e.key === 'ArrowUp' || e.key === 'k') { e.preventDefault(); step(-1); }
});
window.addEventListener('popstate', () => start());
langHooks.push(() => { if (NAV) renderAll(); if ($('hq').value.trim()) search($('hq').value); });

// --- start ----------------------------------------------------------------------------------------
async function start() {
  const m = /^\/w\/(.+)$/.exec(location.pathname), b = /^\/browse\/([^/]+)(?:\/([^/]+))?/.exec(location.pathname);
  const q = new URLSearchParams(location.search).get('q');
  if (m) return gotoSlug(m[1]);
  if (b) {
    const li = LETTERS.indexOf(decodeURIComponent(b[1]));
    if (li >= 0) {
      const nav = await navL(li); const sk = b[2] ? decodeURIComponent(b[2]) : null;
      let gi = 0, si = 0;
      if (sk) nav.forEach((G, i) => G.subs.forEach((s, j) => { if (s.k === sk) { gi = i; si = j; } }));
      return show(li, gi, si, 'first');
    }
  }
  await show(0, 0, 0, 'first');
  if (q) { $('hq').value = q; search(q); }
}
// editor mode: /edit/ (behind Cloudflare Access) marks this browser; the editor's script is loaded only
// then, and shows nothing unless the signed-in check (/api/admin/whoami) passes
try {
  if (localStorage.getItem('abhidhana-editor') === '1' && window.EDITOR_JS) {
    const sc = document.createElement('script'); sc.src = window.EDITOR_JS; document.body.appendChild(sc);
  }
} catch (e) {}
Promise.all([volumes(), get('/data/nav.json'), get('/data/labels.json').catch(() => []), get('/data/abbr.json').catch(() => [])])
  .then(([, nav, labs, abbr]) => { NAV = nav; LABS = new Map(labs.map((d, k) => [d.label, { ...d, k }])); ABBR = abbr; return start(); })
  .catch(() => { $('art').innerHTML = `<p class="muted">${esc(t('load_fail'))}</p>`; });
})();
