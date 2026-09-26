// Shared by every page: interface language (es / en), and search across all volumes.
'use strict';
const REPO = 'https://github.com/bthar-mx/tipitaka-abhidhana';
const RELEASE = REPO + '/releases/download/sources-v1/';
const IMG = 'https://abhidhana-img.buddha-dhamma.net/';

const T = {
  en: {
    about: 'About', home: 'Volumes', intro: 'Introduction', browse: 'Browse', abbrs: 'Abbreviations', search_short: 'Search a Pāḷi word', v_tr: 'Translation', v_my: 'Burmese original', v_both: 'Side by side',
    abbr_ph: 'Search the abbreviations: ဒီ, dī, Dīgha…', abbr_n: (k, n) => k === n ? `${n} abbreviations` : `${k} of ${n} abbreviations`, to_dark: 'Switch to dark mode', to_light: 'Switch to light mode',
    search_ph: 'Search all volumes: အကုသလ or akusala',
    search_loading: 'Loading the headword list…',
    search_fail: 'The headword list did not load. Reload the page to try again.',
    matches: n => `${n.toLocaleString('en')} headword${n === 1 ? '' : 's'} match`,
    first60: 'Showing the first 60. Type more of the word to narrow it.',
    nothing: 'Nothing matches. Burmese is matched as typed; roman letters ignore diacritics (akusala finds akusala, ākāsa finds akasa).',
    vol: 'vol.', page: 'p.',
    st_done: 'digitised', st_coming: 'coming',
    prev: '‹ Prev', next: 'Next ›', pdfp: 'PDF p.', printed: 'printed p.', headwords: 'headwords',
    show: 'Show', show_all: 'all articles', show_f: 'fuzzy matches', show_u: 'not located',
    roman: 'Pāḷi in roman',
    located: 'located', fuzzy: 'fuzzy match', unlocated: 'not located',
    in_canon: 'in canon', inside: 'inside a canon word', not_canon: 'not in canon',
    unproofed: 'unproofed OCR', status: 'status',
    st_ocr: 'ocr', st_drafted: 'drafted', st_reviewed: 'reviewed', st_corrected: 'corrected',
    report: 'Report an error', misfiled: 'the index files this headword on another page',
    no_def: 'No definition text recovered.',
    not_found: 'Headword not found in the OCR text. The article is probably inside the previous one; check the page image.',
    no_rows: 'No articles of this kind on this page.',
    scan: 'Page image', fit: 'Fit width', actual: 'Actual size', hide: 'Hide', showimg: 'Show',
    newtab: 'Open image', pdf: 'Download the volume (PDF)',
    img_missing: 'The page image is not available yet. The PDF of the whole volume is in the release sources-v1.',
    loading_vol: v => `Loading vol. ${v}…`,
    load_fail: v => `Vol. ${v} did not load. Reload the page to try again.`,
    not_digitised: v => `Vol. ${v} is not digitised yet.`,
    s_headwords: 'headwords', s_pages: 'pages', s_located: 'located', s_usable: 'with label and definition',
    provisional: 'provisional', ocr_read: 'OCR read', labelhelp: 'Explain labels', all_labels: 'All labels',
    notice: '<strong>Unproofed OCR.</strong> Each headword comes from the dictionary’s index and is spelled as the index spells it. Everything after it (label, analysis, definition, citations) is machine-read Burmese and contains errors. Check the page image before quoting an article.',
  },
  es: {
    about: 'Acerca de', home: 'Volúmenes', intro: 'Introducción', browse: 'Consultar', abbrs: 'Abreviaturas', search_short: 'Buscar una palabra pāḷi', v_tr: 'Traducción', v_my: 'Original birmano', v_both: 'En paralelo',
    abbr_ph: 'Buscar en las abreviaturas: ဒီ, dī, Dīgha…', abbr_n: (k, n) => k === n ? `${n} abreviaturas` : `${k} de ${n} abreviaturas`, to_dark: 'Cambiar al modo oscuro', to_light: 'Cambiar al modo claro',
    search_ph: 'Buscar en todos los volúmenes: အကုသလ o akusala',
    search_loading: 'Cargando la lista de entradas…',
    search_fail: 'La lista de entradas no se cargó. Recargue la página para intentarlo de nuevo.',
    matches: n => `${n.toLocaleString('es')} entrada${n === 1 ? '' : 's'} coincide${n === 1 ? '' : 'n'}`,
    first60: 'Se muestran las primeras 60. Escriba más de la palabra para acotar.',
    nothing: 'No hay coincidencias. El birmano se busca tal como se escribe; en letras latinas no cuentan los diacríticos (akasa encuentra ākāsa).',
    vol: 'vol.', page: 'p.',
    st_done: 'digitalizado', st_coming: 'próximamente',
    prev: '‹ Anterior', next: 'Siguiente ›', pdfp: 'p. del PDF', printed: 'p. impresa', headwords: 'entradas',
    show: 'Mostrar', show_all: 'todos los artículos', show_f: 'coincidencias aproximadas', show_u: 'no localizados',
    roman: 'Pāḷi en caracteres latinos',
    located: 'localizado', fuzzy: 'coincidencia aproximada', unlocated: 'no localizado',
    in_canon: 'en el canon', inside: 'dentro de una palabra del canon', not_canon: 'no está en el canon',
    unproofed: 'OCR sin revisar', status: 'estado',
    st_ocr: 'ocr', st_drafted: 'borrador', st_reviewed: 'revisado', st_corrected: 'corregido',
    report: 'Informar de un error', misfiled: 'el índice registra esta entrada en otra página',
    no_def: 'No se recuperó el texto de la definición.',
    not_found: 'La entrada no se encontró en el texto del OCR. Probablemente el artículo está dentro del anterior; consulte la imagen de la página.',
    no_rows: 'No hay artículos de este tipo en esta página.',
    scan: 'Imagen de la página', fit: 'Ajustar al ancho', actual: 'Tamaño real', hide: 'Ocultar', showimg: 'Mostrar',
    newtab: 'Abrir imagen', pdf: 'Descargar el volumen (PDF)',
    img_missing: 'La imagen de la página aún no está disponible. El PDF del volumen completo está en la publicación sources-v1.',
    loading_vol: v => `Cargando el vol. ${v}…`,
    load_fail: v => `El vol. ${v} no se cargó. Recargue la página para intentarlo de nuevo.`,
    not_digitised: v => `El vol. ${v} aún no está digitalizado.`,
    s_headwords: 'entradas', s_pages: 'páginas', s_located: 'localizadas', s_usable: 'con categoría y definición',
    provisional: 'provisional', ocr_read: 'El OCR leyó', labelhelp: 'Explicar categorías', all_labels: 'Todas las categorías',
    notice: '<strong>OCR sin revisar.</strong> Cada entrada procede del índice del diccionario y se escribe como la escribe el índice. Todo lo que sigue (categoría gramatical, análisis, definición, citas) es birmano leído por máquina y contiene errores. Consulte la imagen de la página antes de citar un artículo.',
  },
};

function pickLang() {
  try { const s = localStorage.getItem('lang'); if (s === 'es' || s === 'en') return s; } catch (e) {}
  return (navigator.language || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
}
let LANG = pickLang();
const t = (k, ...a) => { const v = T[LANG][k] ?? T.en[k] ?? k; return typeof v === 'function' ? v(...a) : v; };
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const my2 = n => String(n).replace(/\d/g, d => '၀၁၂၃၄၅၆၇၈၉'[d]);
const fold = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const langHooks = [];

function applyLang() {
  document.documentElement.lang = LANG; document.documentElement.dataset.lang = LANG;
  document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll('[data-i18n-html]').forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  document.querySelectorAll('.lang button').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === LANG));
  langHooks.forEach(f => f());
  const path = location.pathname, home = !/^\/(volumes|introduction|abbreviations|about|v)\b/.test(path.slice(0));
  document.querySelectorAll('.menu a[data-nav]').forEach(a => { const n = a.dataset.nav; const on = n === '/' ? home : path.startsWith(n); if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
}
function setLang(l) { LANG = l; try { localStorage.setItem('lang', l); } catch (e) {} applyLang(); }
document.addEventListener('click', e => { const b = e.target.closest('.lang button'); if (b) setLang(b.dataset.lang); });

// --- light / dark: the system's choice until the button is used, then the viewer's (remembered)
const darkMQ = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
const theme = () => document.documentElement.dataset.theme || (darkMQ && darkMQ.matches ? 'dark' : 'light');
function themeButton() {
  document.querySelectorAll('button.theme').forEach(b => {
    const l = t(theme() === 'dark' ? 'to_light' : 'to_dark'); b.title = l; b.setAttribute('aria-label', l);
  });
}
document.addEventListener('click', e => {
  if (!e.target.closest('button.theme')) return;
  const n = theme() === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = n;
  try { localStorage.setItem('theme', n); } catch (err) {}
  themeButton();
});
if (darkMQ && darkMQ.addEventListener) darkMQ.addEventListener('change', themeButton);
langHooks.push(themeButton);

// --- volumes and search ------------------------------------------------------------------
let VOLS = null, VOLS_P = null;
function volumes() {
  return VOLS_P || (VOLS_P = fetch('/data/volumes.json').then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(v => (VOLS = v)));
}
const volOf = id => (VOLS || []).find(v => v.id === id);

let S = null, S_P = null;
function searchIndex() {
  return S_P || (S_P = fetch('/data/search.json').then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(x => (S = x.map(row => row.concat(fold(row[4]))))));
}
function runSearch(q, box) {
  q = q.trim();
  if (!q) { box.hidden = true; return; }
  box.hidden = false;
  if (!S) {
    box.innerHTML = `<div class="more">${esc(t('search_loading'))}</div>`;
    searchIndex().then(() => runSearch(q, box)).catch(() => { box.innerHTML = `<div class="more">${esc(t('search_fail'))}</div>`; });
    return;
  }
  const isMy = /[က-႟]/.test(q), fq = fold(q), out = [];
  const ord = Object.fromEntries((VOLS || []).map((v, k) => [v.id, k]));
  for (const row of S) {
    const hay = isMy ? row[3] : row[5];
    const pos = hay.indexOf(isMy ? q : fq); if (pos < 0) continue;
    out.push([pos === 0 ? 0 : 1, hay.length, ord[row[0]] ?? 99, row[1], row]);
  }
  out.sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2] || a[3] - b[3]);
  const vn = id => (volOf(id) || { n: id }).n;
  box.innerHTML = `<h3>${esc(t('matches', out.length))}</h3>` +
    out.slice(0, 60).map(x => {
      const [b, i, p, h, r] = x[4];
      return `<a class="res" href="/v/${b}/${p}#a${i}"><span><span class="my" lang="my">${esc(h)}</span><span class="ro" lang="pi">${esc(r)}</span></span><span class="pg">${t('vol')} ${esc(vn(b))} · ${t('page')} ${p}</span></a>`;
    }).join('') +
    (out.length > 60 ? `<div class="more">${esc(t('first60'))}</div>` : '') +
    (out.length ? '' : `<div class="more">${esc(t('nothing'))}</div>`);
}
function wireSearch(input, box) {
  let tm;
  input.addEventListener('input', () => { clearTimeout(tm); tm = setTimeout(() => runSearch(input.value, box), 150); });
  input.addEventListener('focus', () => { searchIndex().catch(() => {}); }, { once: true });
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { const a = box.querySelector('a.res'); if (a) location.href = a.href; }
    if (e.key === 'Escape') { input.value = ''; box.hidden = true; }
  });
  document.addEventListener('keydown', e => {
    if (e.key === '/' && !e.target.matches('input,select,textarea')) { e.preventDefault(); input.focus(); }
  });
  langHooks.push(() => { if (input.value.trim() && !box.hidden) runSearch(input.value, box); });
}

// --- the IEBH footer and the back-to-top button (every page). The footer block is appended to each
// <footer class="site-foot">; Browse adds one at the end of every article. The version comes from the
// <meta name="version"> that tools/abhidhana_site.py writes from VERSION (brief §42).
Object.assign(T.en, { to_top: 'Back to the top' });
Object.assign(T.es, { to_top: 'Volver arriba' });
function footHTML() {
  const m = document.querySelector('meta[name="version"]'), v = m ? m.content : '';
  const ver = v ? ` · <a href="${REPO}/blob/main/CHANGELOG.md" title="CHANGELOG">v${esc(v)}</a>` : '';
  return '<div class="iebh-foot"><a class="iebh-logo" href="https://iebh.org" aria-label="Instituto de Estudios Buddhistas Hispano (IEBH)"></a>' +
    '<p><span class="tr" lang="es">Un proyecto del <a href="https://iebh.org">Instituto de Estudios Buddhistas Hispano</a> (IEBH). ' +
    'Textos relacionados: el Tipiṭaka del Sexto Concilio en <a href="https://buddha-dhamma.net">buddha-dhamma.net</a>; las gramáticas pāḷi en <a href="https://gramaticas.buddha-dhamma.net">gramaticas.buddha-dhamma.net</a>. ' +
    `Datos y código: <a href="${REPO}">github.com/bthar-mx/tipitaka-abhidhana</a>.</span>` +
    '<span class="tr" lang="en">A project of the <a href="https://iebh.org">Instituto de Estudios Buddhistas Hispano</a> (IEBH). ' +
    'Related texts: the Sixth Council Tipiṭaka at <a href="https://buddha-dhamma.net">buddha-dhamma.net</a>; the Pāḷi grammars at <a href="https://gramaticas.buddha-dhamma.net">gramaticas.buddha-dhamma.net</a>. ' +
    `Data and code: <a href="${REPO}">github.com/bthar-mx/tipitaka-abhidhana</a>.</span></p>` +
    '<p class="iebh-lic"><span class="tr" lang="es">© 2026 IEBH. Código bajo licencia <a href="' + REPO + '/blob/main/LICENSE">MIT</a>; lo que añade el proyecto (estructura, romanizaciones, traducciones), bajo <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.es">CC BY-SA 4.0</a>. El texto del diccionario pertenece a sus autores y editores y no se relicencia; créditos en <a href="/about/">Acerca de</a>.</span>' +
    '<span class="tr" lang="en">© 2026 IEBH. Code under the <a href="' + REPO + '/blob/main/LICENSE">MIT</a> licence; what the project adds (structure, romanisations, translations) under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. The dictionary’s text belongs to its authors and publishers and is not relicensed; credits on the <a href="/about/">About</a> page.</span>' +
    ver + '</p></div>';
}
function fillFoot(root) {
  (root || document).querySelectorAll('footer.site-foot:not([data-iebh])').forEach(f => { f.dataset.iebh = '1'; f.insertAdjacentHTML('beforeend', footHTML()); });
}
fillFoot();
(function () {
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'totop'; b.hidden = true; b.innerHTML = '<span aria-hidden="true">↑</span>';
  const label = () => { b.title = t('to_top'); b.setAttribute('aria-label', t('to_top')); };
  label(); langHooks.push(label);
  const scrollers = () => [document.scrollingElement, ...document.querySelectorAll('.art')].filter(Boolean);
  const update = () => { b.hidden = !scrollers().some(e => e.scrollTop > 400); };
  document.addEventListener('scroll', update, { capture: true, passive: true });
  b.addEventListener('click', () => scrollers().forEach(e => { if (e.scrollTop > 0) e.scrollTo({ top: 0, behavior: 'smooth' }); }));
  document.body.appendChild(b);
})();
