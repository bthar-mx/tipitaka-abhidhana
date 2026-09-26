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

// --- state ----------------------------------------------------------------------------------------
let cur = { li: 0, gi: 0, si: 0, recs: [], k: 0, off: 0 };   // the syllable shown and the entry in it
let open = { label: false, def: false, cit: -1, scanDelta: 0, drawer: false, settings: false };
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
    open = Object.assign(open, { label: false, def: false, cit: -1, scanDelta: 0, drawer: false });
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
  $('settings').hidden = !open.settings;
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
  $('wlist').innerHTML = recs.slice(a, b).map((d, j) => {
    const k = a + j;
    return `<a class="w${k === cur.k ? ' on' : ''}" href="/w/${encodeURIComponent(d.sl)}" data-k="${k}"${k === cur.k ? ' aria-current="true"' : ''}>${hwLabel(d)}${d.hn ? `<sup>${d.hn}</sup>` : ''}</a>`;
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
  const title = `Error: vol. ${vn(d.k)}, PDF p. ${d.p}, ${d.h} (id ${d.i})`;
  const body = `**Volume:** ${vn(d.k)} (book \`${d.k}\`)\n**PDF page:** ${d.p} · **printed page:** ${d.q}\n**Headword:** ${d.h} (${d.r})\n**Article id:** ${d.i}\n**Link:** ${link}\n\n**What is wrong** (and, if you can, what the printed page says):\n\n`;
  return `${REPO}/issues/new?labels=error-report&title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}
// the Meaning box's small markup: *pāḷi* in italics, [[iast|address]] a link to another headword,
// ‹…› a Burmese word the draft left untranslated
function fmtTr(x) {
  return esc(x).replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (m, r, sl) => `<a class="pl" lang="pi" href="/w/${encodeURIComponent(sl)}">${r}</a>`)
    .replace(/\[\[([^\]]+)\]\]/g, '<i class="pl" lang="pi">$1</i>')
    .replace(/\*([^*]+)\*/g, '<i class="pl" lang="pi">$1</i>')
    .replace(/‹([^›]+)›/g, '<span class="my" lang="my">$1</span>');
}
function article() {
  const d = cur.recs[cur.k];
  if (!d) { $('art').innerHTML = ''; return; }
  const H = [];
  H.push(`<div class="where"><span>${esc(t('vol_short'))} ${esc(vn(d.k))} · ${esc(pageStr(d.k, d.p))}</span>` +
    `<span class="chip">${esc(d.s === 'ocr' ? t('ocr_st') : t('st_' + d.s))}</span>` +
    (d.x === 'f' ? `<span class="chip c-warn">${esc(t('fuzzy'))}</span>` : '') +
    (d.m ? `<span class="chip">${esc(t('misfiled'))}</span>` : '') +
    (d.hi ? `<span class="chip c-ok">${esc(t('hw_fixed'))} <span class="my" lang="my">${esc(d.hi)}</span></span>` : '') + '</div>');
  const ro = S.script !== 'my', my = S.script !== 'ro';
  H.push(`<div class="head">` +
    (ro ? `<h1 class="pl" lang="pi">${esc(d.r)}${d.hn ? `<sup>${d.hn}</sup>` : ''}</h1>` : '') +
    (my ? `<div class="my hw-my${ro ? ' second' : ''}" lang="my">${esc(d.h)}${!ro && d.hn ? `<sup>${d.hn}</sup>` : ''}</div>` : '') +
    (d.l ? `<button type="button" class="lab" data-label aria-expanded="${open.label}">${labelShown(d)}</button>` : '') + '</div>');
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
    ? `<div class="meaning"><span class="chip ${tr.s === 'drafted' ? 'c-warn' : 'c-ok'}">${esc(t('st_' + tr.s))}</span><div lang="${LANG}">${fmtTr(tr.x)}</div>${tr.s === 'drafted' ? `<div class="muted small">${esc(t('drafted_note'))}</div>` : ''}</div>`
    : `<div class="meaning empty"><span class="chip">${esc(t('not_translated'))}</span><span>${esc(t('trans_note'))}</span></div>`));
  const showDef = d.b && (S.defs === 'show' || (S.defs === 'collapse' && open.def));
  if (d.b && S.defs === 'collapse' && !open.def) H.push(`<button type="button" class="btn" data-def="1" aria-expanded="false">${esc(t('show_def'))}</button>`);
  if (showDef) {
    H.push((S.defs === 'collapse' ? `<button type="button" class="btn small" data-def="0" aria-expanded="true">${esc(t('hide_def'))}</button>` : '') +
      `<div class="def my" lang="my">${defHTML(d)}</div><div class="muted small">${esc(t('ocrnote'))}</div>`);
  }
  H.push('</section>');
  // Pāḷi passages quoted (when the definition is not shown)
  const seeR = new Set((d.see || []).map(x => x[0]));
  const quotes = (d.sp || []).filter(s => (s[3] || 1) >= 2 && !seeR.has(s[2]));
  if (!showDef && quotes.length) {
    H.push(`<section><h2>${esc(t('quotes'))}</h2><ol class="quotes">` +
      quotes.map(s => S.script === 'my' ? `<li class="my" lang="my">${esc((d.b || '').slice(s[0], s[1]))}</li>` : `<li class="pl" lang="pi">${esc(s[2])}</li>`).join('') +
      `</ol><div class="muted small">${esc(t('quotes_note'))}</div></section>`);
  }
  // citations: tap expands the abbreviation to the work (docs/introduction/citation-abbreviations.tsv)
  if (d.c && d.c.length) {
    H.push(`<section><h2>${esc(t('cit'))}</h2><div class="cits">` + d.c.map((c, j) => {
      const lab = S.script === 'my' || !d.ci ? `<span class="my" lang="my">${esc(c)}</span>` : `<span class="pl" lang="pi">${esc(d.ci[j])}</span>`;
      const tip = citeTip(d, j);
      return `<button type="button" class="cit${open.cit === j ? ' on' : ''}" data-cit="${j}" aria-expanded="${open.cit === j}"${tip ? ` title="${esc(tip)}"` : ''}>${lab}</button>`;
    }).join('') + '</div>');
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
  H.push(`<div class="artnav"><button type="button" class="btn" data-step="-1">‹ ${P ? hwLabel(P) : ''}</button>` +
    `<button type="button" class="btn" data-step="1">${N ? hwLabel(N) : ''} ›</button>` +
    (S.scan ? '' : `<button type="button" class="btn" data-scan>${esc(t('see_page'))}</button>`) +
    `<a href="/v/${d.k}/${d.p}#a${d.i}">${esc(t('page_view'))}</a>` +
    `<a class="report" href="${reportURL(d)}" target="_blank" rel="noopener">${esc(t('report'))}</a></div>`);
  $('art').innerHTML = `<article>${H.join('')}</article><footer class="site-foot"></footer>`;
  fillFoot($('art'));
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
  if (k >= 0 && k < cur.recs.length) { cur.k = k; if (k < cur.off || k >= cur.off + W) cur.off = Math.floor(k / W) * W; open = Object.assign(open, { label: false, def: false, cit: -1, scanDelta: 0 }); await renderAll(); route(); return; }
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
    const out = [...pre, ...sub].slice(0, 60);
    if ($('hq').value.trim() !== q) return;
    box.innerHTML = out.map(r => `<a class="res" href="/w/${encodeURIComponent(r[0])}"><span>` +
      (S.script === 'my' ? `<span class="my" lang="my">${esc(r[2])}</span>` : `<span class="pl" lang="pi">${esc(r[1])}</span>${S.script === 'both' ? ` <span class="my sub" lang="my">${esc(r[2])}</span>` : ''}`) +
      `</span><span class="pg">${esc(t('vol_short'))} ${esc(vn(r[3]))} · ${esc(pageStr(r[3], r[4]))}</span></a>`).join('') +
      (out.length ? (pre.length + sub.length > 60 ? `<div class="more">${esc(t('results_more'))}</div>` : '') : `<div class="more">${esc(t('results_none'))}</div>`);
  } catch (e) { box.innerHTML = `<div class="more">${esc(t('load_fail'))}</div>`; }
}

// --- events ---------------------------------------------------------------------------------------
app.addEventListener('click', async e => {
  const el = e.target.closest('button, a'); if (!el) return;
  const ds = el.dataset;
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
  if (ds.k) { e.preventDefault(); cur.k = +ds.k; open = Object.assign(open, { label: false, def: false, cit: -1, scanDelta: 0, drawer: false }); await renderAll(); $('art').scrollTop = 0; return route(); }
  if (el.id === 'wearlier') { cur.off = Math.max(0, cur.off - W); return words(); }
  if (el.id === 'wlater') { cur.off += W; return words(); }
  if ('label' in ds) { open.label = !open.label; return article(); }
  if (ds.def) { open.def = ds.def === '1'; return article(); }
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
Promise.all([volumes(), get('/data/nav.json'), get('/data/labels.json').catch(() => []), get('/data/abbr.json').catch(() => [])])
  .then(([, nav, labs, abbr]) => { NAV = nav; LABS = new Map(labs.map((d, k) => [d.label, { ...d, k }])); ABBR = abbr; return start(); })
  .catch(() => { $('art').innerHTML = `<p class="muted">${esc(t('load_fail'))}</p>`; });
})();
