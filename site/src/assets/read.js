// The reader: /v/<book>/<pdf page>, optionally #a<article id>. Articles on the left, the page
// image (from R2) on the right. Everything shown is our OCR and what the project adds.
'use strict';
// The label table (docs/labels.md §0, published by the build as /data/labels.json).
let LAB = new Map();   // label -> {pali, en, es, abbr_en, abbr_es, status, es_status, k}
let labelHelp = true;
try { labelHelp = localStorage.getItem('labelHelp') !== '0'; } catch (e) {}
const LOC = { v: ['c-v', 'located'], f: ['c-f', 'fuzzy'], u: ['c-u', 'unlocated'] };
const OS = { word: 'in_canon', inside: 'inside', none: 'not_canon' };

let V = null, D = [], pages = [], byPage = new Map(), cur = 0, hit = null, seq = 0, roman = true;
const cache = new Map();

function route() {
  const m = /^\/v\/(\w+)(?:\/(\d+))?/.exec(location.pathname);
  const h = /^#a(\d+)$/.exec(location.hash);
  return { id: m ? m[1] : '01', page: m && m[2] ? +m[2] : 0, art: h ? +h[1] : null };
}

function bodyHTML(d) {
  if (!d.sp || !roman) return esc(d.b);
  let out = '', k = 0;
  for (const [a, b, r] of d.sp) { out += esc(d.b.slice(k, a)) + `<span class="pali" lang="pi" title="${esc(d.b.slice(a, b))}">${esc(r)}</span>`; k = b; }
  return out + esc(d.b.slice(k));
}
function chip(cls, txt) { return `<span class="chip ${cls}">${esc(txt)}</span>`; }
function reportURL(d) {
  const link = `${location.origin}/v/${V.id}/${d.p}#a${d.i}`;
  const title = `Error: vol. ${V.n}, PDF p. ${d.p}, ${d.h} (id ${d.i})`;
  const body = `**Volume:** ${V.n} (book \`${V.id}\`)\n**PDF page:** ${d.p} · **printed page:** ${d.q}\n**Headword:** ${d.h} (${d.r})\n**Article id:** ${d.i}\n**Link:** ${link}\n\n**What is wrong** (and, if you can, what the printed page says):\n\n`;
  return `${REPO}/issues/new?labels=error-report&title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}
function card(d) {
  const [lc, lk] = LOC[d.x];
  const L = d.l && LAB.get(d.l), ab = L && L['abbr_' + LANG];
  const gl = ab ? `<span class="gl">${esc(ab)}</span>` : '';
  const lab = d.l
    ? (labelHelp && L ? `<span class="label"><button type="button" class="lb" data-l="${esc(d.l)}"${d.lo ? ` data-lo="${esc(d.lo)}"` : ''} aria-haspopup="dialog">(${esc(d.l)})</button>${gl}</span>`
                      : `<span class="label">(${esc(d.l)})${gl}</span>`)
    : (d.lo ? `<span class="label" style="opacity:.6">(${esc(d.lo)}?)</span>` : '');
  const an = d.a ? `<span class="analysis">${esc(d.a)}</span>${roman && d.ai ? `<span class="an-ro" lang="pi">[${esc(d.ai)}]</span>` : ''}` : '';
  const body = d.b ? `<p class="def" lang="my">${bodyHTML(d)}</p>` : `<p class="empty">${esc(t(d.x === 'u' ? 'not_found' : 'no_def'))}</p>`;
  const ci = d.c && d.c.length ? `<div class="cites">${d.c.map((c, j) => `<span class="cite">${roman && d.ci ? `<span class="ro">${esc(d.ci[j])}</span>` : esc(c)}</span>`).join('')}</div>` : '';
  return `<article id="a${d.i}" class="${d.i === hit ? 'hit' : ''}">
    <div class="hw"><span class="my" lang="my">${esc(d.h)}</span><span class="ro" lang="pi">${esc(d.r)}</span></div>
    <div class="line1">${lab}${an}</div>${body}${ci}
    <div class="meta">${chip(lc, t(lk))}${d.o ? chip('c-o', t(OS[d.o])) : ''}${chip('c-s', `${t('unproofed')} · ${t('status')}: ${t('st_' + d.s)}`)}${d.m ? chip('c-o', t('misfiled')) : ''}
      <a href="${reportURL(d)}" target="_blank" rel="noopener">${esc(t('report'))}</a></div></article>`;
}

function setImage(p) {
  const url = `${IMG}${V.id}/${String(p).padStart(4, '0')}.webp`;
  const img = $('img');
  $('imgmiss').hidden = true; $('view').hidden = $('scan').classList.contains('collapsed');
  img.onerror = () => { $('view').hidden = true; $('imgmiss').hidden = false; };
  img.onload = () => { $('imgmiss').hidden = true; };
  img.alt = `${V.title_my}, PDF p. ${p}`;
  if (img.getAttribute('src') !== url) img.src = url;
  $('imgopen').href = url;
  $('pdf').href = `${RELEASE}${V.id}.pdf`;
  // warm the neighbours
  for (const q of [p - 1, p + 1]) if (q > 0 && q <= V.pdf_pages) { const i = new Image(); i.src = `${IMG}${V.id}/${String(q).padStart(4, '0')}.webp`; }
}

function render(p, scroll) {
  closePop();
  if (!pages.length) return;
  if (!byPage.has(p)) p = pages.find(x => x >= p) ?? pages[pages.length - 1];
  cur = p; $('pg').value = p;
  const url = `/v/${V.id}/${p}${hit != null ? '#a' + hit : ''}`;
  if (location.pathname + location.hash !== url) history.replaceState(null, '', url);
  document.title = `${V.title_my} · ${t('pdfp')} ${p} — Tipiṭaka Pāḷi-Myanmā Abhidhāna`;
  const idx = byPage.get(p) || [], f = $('show').value;
  const rows = idx.filter(i => f === 'all' || D[i].x === f);
  const c = { v: 0, f: 0, u: 0 }; idx.forEach(i => c[D[i].x]++);
  const d0 = D[idx[0]];
  $('pagehead').innerHTML = `<h2>${esc(t('pdfp'))} <b>${p}</b> · ${esc(t('printed'))} <b>${d0 ? my2(d0.q) : '–'}</b> · ${idx.length} ${esc(t('headwords'))}</h2>
    <div>${chip('c-v', c.v + ' ' + t('located'))}${c.f ? chip('c-f', c.f + ' ' + t('fuzzy')) : ''}${c.u ? chip('c-u', c.u + ' ' + t('unlocated')) : ''}</div>`;
  $('list').innerHTML = rows.length ? rows.map(i => card(D[i])).join('') : `<div class="loading">${esc(t('no_rows'))}</div>`;
  const k = pages.indexOf(p); $('prev').disabled = k <= 0; $('next').disabled = k >= pages.length - 1;
  setImage(p);
  if (scroll && hit != null) { const el = $('a' + hit); if (el) el.scrollIntoView({ block: 'start' }); }
}
function step(dir) {
  const f = $('show').value; let k = pages.indexOf(cur);
  do { k += dir; } while (k >= 0 && k < pages.length && f !== 'all' && !(byPage.get(pages[k]) || []).some(i => D[i].x === f));
  if (k >= 0 && k < pages.length) { hit = null; render(pages[k]); window.scrollTo({ top: 0 }); }
}

function header() {
  $('vmy').textContent = `${V.title_my} · ${V.range_my}`;
  const note = V['note_' + LANG] ? ` (${V['note_' + LANG]})` : '';
  $('vro').textContent = `${t('vol')} ${V.n} · ${V.range_ro}${note}`;
  const ghd = `${REPO}/blob/main/ocr/${V.id}/`;
  for (const [a, b] of [['fdata', 'articles.jsonl'], ['fdata2', 'articles.jsonl'], ['frep', 'articles-report.md'], ['frep2', 'articles-report.md']]) $(a).href = ghd + b;
  $('stats').innerHTML = V.status === 'done'
    ? `<span><b>${V.records.toLocaleString(LANG)}</b> ${esc(t('s_headwords'))}</span><span><b>${V.pages}</b> ${esc(t('s_pages'))}</span><span><b>${V.located.toLocaleString(LANG)}%</b> ${esc(t('s_located'))}</span><span><b>${V.usable.toLocaleString(LANG)}%</b> ${esc(t('s_usable'))}</span>` : '';
}

function load(id, page, art) {
  V = volOf(id) || VOLS.find(v => v.status === 'done');
  $('vol').value = V.id; hit = art; header();
  const my = ++seq;
  if (V.status !== 'done') {
    D = []; pages = []; $('pagehead').innerHTML = ''; $('list').innerHTML = `<div class="loading">${esc(t('not_digitised', V.n))}</div>`;
    $('pg').value = page || ''; setImage(page || V.start); return;
  }
  const show = data => {
    if (my !== seq) return;
    D = data; byPage = new Map();
    D.forEach((d, i) => { if (!byPage.has(d.p)) byPage.set(d.p, []); byPage.get(d.p).push(i); });
    pages = [...byPage.keys()].sort((a, b) => a - b);
    if (art != null && !page) { const d = D.find(x => x.i === art); if (d) page = d.p; }
    render(page || V.start, true);
  };
  if (cache.has(V.id)) return show(cache.get(V.id));
  $('list').innerHTML = `<div class="loading">${esc(t('loading_vol', V.n))}</div>`; $('pagehead').innerHTML = '';
  fetch(`/data/v${V.id}.json`).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(data => { cache.set(V.id, data); show(data); })
    .catch(() => { if (my === seq) $('list').innerHTML = `<div class="loading">${esc(t('load_fail', V.n))}</div>`; });
}

function volOptions() {
  $('vol').innerHTML = VOLS.map(v => `<option value="${v.id}">${esc(v.n)} · ${esc(v.range_ro)}${v.status === 'done' ? '' : ' — ' + esc(t('st_coming'))}</option>`).join('');
  if (V) $('vol').value = V.id;
}

// --- label pop-up: opens only on a click or tap on the label; one at a time; closes on a click
// elsewhere, Esc, or the label again. It floats just below the label's line (above it when there
// is no room), so the text does not move.
let pop = null, popFor = null;
function closePop() { if (pop) { pop.remove(); pop = null; } if (popFor) popFor.setAttribute('aria-expanded', 'false'); popFor = null; }
function openPop(btn) {
  const L = LAB.get(btn.dataset.l); if (!L) return;
  closePop();
  const meaning = L[LANG] || L.en;
  const prov = L.status === 'provisional' || (LANG === 'es' && L.es_status !== 'confirmed');
  pop = document.createElement('div'); pop.className = 'pop'; pop.setAttribute('role', 'dialog');
  pop.innerHTML = `<div class="l1"><span class="my" lang="my">(${esc(btn.dataset.l)})</span><span>·</span>${L.printed ? `<span class="my" lang="my">${esc(L.printed)}</span><span>·</span>` : ''}${L.pali ? `<span class="pl" lang="pi">${esc(L.pali)}</span><span>·</span>` : ''}<span>${esc(meaning)}</span>${prov ? `<span class="prov">${esc(t('provisional'))}</span>` : ''}<a href="/abbreviations/#l${L.k}" title="${esc(t('all_labels'))}" aria-label="${esc(t('all_labels'))}">↗</a></div>` +
    (btn.dataset.lo ? `<div class="l2">${esc(t('ocr_read'))}: <span class="my" lang="my">(${esc(btn.dataset.lo)})</span></div>` : '');
  document.body.appendChild(pop);
  const r = btn.getBoundingClientRect(), line = parseFloat(getComputedStyle(btn).lineHeight) || r.height;
  const w = pop.offsetWidth, h = pop.offsetHeight, gap = 4;
  const lineBottom = r.top + Math.max(r.height, line) - (Math.max(r.height, line) - r.height) / 2;
  let top = lineBottom + gap;
  if (top + h > window.innerHeight - 8 && r.top - h - gap > 8) top = r.top - h - gap;
  const left = Math.max(8, Math.min(r.left, document.documentElement.clientWidth - w - 8));
  pop.style.top = `${top + window.scrollY}px`; pop.style.left = `${left + window.scrollX}px`;
  popFor = btn; btn.setAttribute('aria-expanded', 'true');
}
document.addEventListener('click', e => {
  const b = e.target.closest('.lb');
  if (b) { e.preventDefault(); if (popFor === b) closePop(); else openPop(b); return; }
  if (pop && !pop.contains(e.target)) closePop();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape' && pop) { const f = popFor; closePop(); if (f) f.focus(); } });
window.addEventListener('resize', closePop);

wireSearch($('q'), $('results'));
$('prev').onclick = () => step(-1); $('next').onclick = () => step(1);
$('pg').addEventListener('change', e => { const n = parseInt(e.target.value, 10); if (n) { hit = null; render(n); } });
$('pg').addEventListener('keydown', e => { if (e.key === 'Enter') e.target.dispatchEvent(new Event('change')); });
$('show').addEventListener('change', () => { const f = $('show').value; if (f !== 'all' && !(byPage.get(cur) || []).some(i => D[i].x === f)) step(1); else render(cur); });
$('rom').addEventListener('change', e => { roman = e.target.checked; render(cur); });
$('lhelp').checked = labelHelp;
$('lhelp').addEventListener('change', e => { labelHelp = e.target.checked; try { localStorage.setItem('labelHelp', labelHelp ? '1' : '0'); } catch (x) {} render(cur); });
$('vol').addEventListener('change', e => { $('show').value = 'all'; window.scrollTo({ top: 0 }); history.pushState(null, '', `/v/${e.target.value}`); load(e.target.value, 0, null); });
$('zoom').onclick = () => { const s = $('scan'); s.classList.toggle('full'); $('zoom').dataset.i18n = s.classList.contains('full') ? 'fit' : 'actual'; $('zoom').textContent = t($('zoom').dataset.i18n); };
$('imgtoggle').onclick = () => { const s = $('scan'); s.classList.toggle('collapsed'); const c = s.classList.contains('collapsed'); $('view').hidden = c; $('imgtoggle').dataset.i18n = c ? 'showimg' : 'hide'; $('imgtoggle').textContent = t($('imgtoggle').dataset.i18n); };
document.addEventListener('keydown', e => {
  if (e.target.matches('input,select,textarea')) return;
  if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1);
});
window.addEventListener('popstate', () => { const r = route(); load(r.id, r.page, r.art); });
window.addEventListener('hashchange', () => { const r = route(); if (r.art != null && V && r.id === V.id) { hit = r.art; const d = D.find(x => x.i === hit); render(d ? d.p : cur, true); } });
langHooks.push(() => { if (VOLS) { volOptions(); if (V) { header(); if (pages.length) render(cur); } } });

applyLang();
const labelsP = fetch('/data/labels.json').then(r => r.ok ? r.json() : []).catch(() => [])
  .then(ls => { LAB = new Map(ls.map((d, k) => [d.label, { ...d, k }])); });
Promise.all([volumes(), labelsP]).then(() => { volOptions(); const r = route(); load(r.id, r.page, r.art); })
  .catch(() => { $('list').innerHTML = '<div class="loading">volumes.json did not load.</div>'; });
