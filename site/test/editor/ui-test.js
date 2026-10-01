// Browse and /edit/ in a headless browser against `wrangler pages dev` (run.sh; after api-test.js, whose
// rows it expects). Access is simulated by adding its header to /api/admin/ requests.
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const { mint } = require('./access-mock.js');
const B = process.env.BASE || 'http://127.0.0.1:8788';
const shots = process.env.SHOTS || '.';
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) { pass++; console.log('ok  ', m); } else { fail++; console.log('FAIL', m); } };
async function seed(token) {
  const r = await fetch(B + '/api/admin/edits', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Abhidhana-Editor': '1', Origin: B, 'Cf-Access-Jwt-Assertion': token },
    body: JSON.stringify({ book: '18', id: 141459, edits: [{ field: 'es', value: 'quitar / arrancar (prueba).', old: '' }] }) });
  return r.status;
}
(async () => {
  const token = mint({});
  ok(await seed(token) === 200, 'seeded an ES edit of luñcana (141459) through the API');
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});

  // 1. a visitor: sees the edit laid over the static data; no editor script, no admin call
  let ctx = await browser.newContext({ locale: 'es-ES' }), page = await ctx.newPage();
  const reqs = []; page.on('request', q => reqs.push(q.url()));
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('.meaning');
  await page.waitForFunction(() => document.querySelector('.meaning').textContent.includes('prueba'), null, { timeout: 5000 }).catch(() => {});
  let m = await page.textContent('.meaning');
  ok(m.includes('quitar / arrancar (prueba).') && m.includes('corregido') && m.includes('Traducción corregida por el editor.'), 'visitor: overlaid Spanish, marked corregido: ' + m.slice(0, 120));
  ok(m.includes('Editado por el editor el'), 'visitor: edit date shown');
  ok(!(await page.$('[data-edit]')), 'visitor: no Editar button');
  ok(!reqs.some(u => /editor\.js|\/api\/admin\//.test(u)), 'visitor: editor.js and /api/admin/ never requested');
  ok(reqs.some(u => u.includes('/api/edits?book=18')), 'visitor: /api/edits?book=18 requested');
  await page.screenshot({ path: `${shots}/visitor.png` });
  await ctx.close();

  // 2. the read API fails: the static data, as before
  ctx = await browser.newContext({ locale: 'es-ES' }); page = await ctx.newPage();
  await page.route('**/api/edits**', r => r.abort());
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('.meaning'); await page.waitForTimeout(500);
  m = await page.textContent('.meaning');
  ok(m.includes('quitar / arrancar.') && !m.includes('prueba'), 'API down: the static Meaning shows: ' + m.slice(0, 80));
  await ctx.close();

  // 3. the editor: /edit/ turns editor mode on; Access is simulated by adding its header to /api/admin/
  ctx = await browser.newContext({ locale: 'es-ES' }); page = await ctx.newPage();
  await ctx.route('**/api/admin/**', r => r.continue({ headers: Object.assign({}, r.request().headers(), { 'cf-access-jwt-assertion': token }) }));
  await page.goto(B + '/edit/'); await page.waitForSelector('.ed-table', { timeout: 8000 });
  ok((await page.textContent('#who')).includes('editor@example.org'), '/edit/: signed in, email shown');
  ok(await page.evaluate(() => localStorage.getItem('abhidhana-editor')) === '1', '/edit/: this browser marked for editor mode');
  await page.waitForTimeout(1500);
  const hist = await page.textContent('.ed-table');
  ok(hist.includes('141459') && hist.includes('prueba'), '/edit/: history lists the edits');
  await page.screenshot({ path: `${shots}/edit-page.png`, fullPage: true });
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('[data-edit]', { timeout: 8000 });
  ok(true, 'editor: Editar button present');
  ok((await page.textContent('.ed-badge')).includes('editor@example.org'), 'editor: badge');
  await page.click('[data-edit]'); await page.waitForSelector('.ed-form');
  ok(await page.inputValue('[data-f="es"]') === 'quitar / arrancar (prueba).', 'form: ES prefilled with the overlaid text');
  ok(await page.inputValue('[data-f="analysis"]') === 'လုဉ္စ + ယု။ (တိ) လုဉ္စန-သံ။', 'form: analysis prefilled');
  // Burmese input with the live roman preview
  await page.fill('[data-f="analysis"]', 'လုဉ္စ + အန');
  ok((await page.textContent('[data-prev="analysis"] [data-back]')) === '[luñca + ana]', 'preview: ' + await page.textContent('[data-prev="analysis"] [data-back]'));
  ok((await page.textContent('[data-prev="analysis"] [data-store]')) === 'လုဉ္စ + အန', 'preview: the Burmese to be stored shown');
  await page.fill('[data-f="headword"]', 'လုဉ္စန');
  ok((await page.textContent('[data-prev="headword"] [data-back]')) === 'luñcana', 'headword preview');
  await page.fill('[data-f="es"]', 'quitar / arrancar.');
  await page.check('input[name="ed-st"][value="reviewed"]');
  await page.screenshot({ path: `${shots}/form.png`, fullPage: true });
  await page.click('[data-save]');
  await page.waitForFunction(() => !document.querySelector('.ed-form [data-save]') || document.querySelector('.ed-msg').textContent.length > 0);
  await page.waitForTimeout(500);
  ok((await page.textContent('.ed-msg')).includes('Guardado'), 'save: ' + await page.textContent('.ed-msg'));
  m = await page.textContent('.meaning');
  ok(m.includes('quitar / arrancar.') && m.includes('revisado') && m.includes('Traducción revisada por el editor.'), 'after save: new text, revisado: ' + m.slice(0, 80));
  ok((await page.textContent('.an')).includes('luñca + ana'), 'after save: analysis in roman from the edit');
  ok((await page.textContent('section:has(.an) h2')).includes('corregido'), 'after save: analysis marked corregido');
  // per-sense status
  await page.fill('[data-f="senses"]', '1');
  await page.check('input[name="ed-st"][value="corrected"]');
  await page.click('[data-save]'); await page.waitForTimeout(800);
  m = await page.textContent('.meaning');
  ok(m.includes('corregido en parte') && m.includes('sentido (1)'), 'per-sense: corregido en parte (1): ' + m.slice(0, 160));
  // withdraw the analysis edit
  await page.click('[data-withdraw="analysis"]'); await page.waitForTimeout(800);
  ok(!(await page.textContent('.an')).includes('ana]') && (await page.textContent('.an')).includes('luñca + yu'), 'withdraw: the published analysis again');
  // a reload keeps the edits (they are in D1)
  await page.reload(); await page.waitForSelector('.meaning'); await page.waitForTimeout(800);
  m = await page.textContent('.meaning');
  ok(m.includes('corregido en parte'), 'reload: the edits persist');
  // an empty Burmese field is refused in the form
  await page.click('[data-edit]'); await page.waitForSelector('.ed-form');
  await page.fill('[data-f="body"]', 'abc'); await page.click('[data-save]'); await page.waitForTimeout(300);
  ok((await page.textContent('.ed-msg')).includes('birmanas'), 'form refuses a body without Burmese letters');
  await page.screenshot({ path: `${shots}/editor-after.png`, fullPage: true });
  await ctx.close();

  // 5. the form gives back the Meaning as its source has it ([[labhati]], not the built [[labhati|labhati]]);
  //    a phone-width page does not scroll sideways
  ctx = await browser.newContext({ locale: 'es-ES', viewport: { width: 390, height: 844 } }); page = await ctx.newPage();
  await ctx.route('**/api/admin/**', r => r.continue({ headers: Object.assign({}, r.request().headers(), { 'cf-access-jwt-assertion': token }) }));
  await page.addInitScript(() => localStorage.setItem('abhidhana-editor', '1'));
  await page.goto(B + '/w/labhissati'); await page.waitForSelector('[data-edit]', { timeout: 8000 });
  await page.click('[data-edit]'); await page.waitForSelector('.ed-form');
  const src = await page.inputValue('[data-f="es"]');
  ok(src.includes('[[labhati]]') && !src.includes('|'), 'form: links in the source markup: ' + src.slice(0, 100));
  ok(await page.evaluate(() => document.documentElement.scrollWidth) <= 390, 'phone width: no sideways scroll');
  await page.screenshot({ path: `${shots}/phone.png` });
  await ctx.close();

  // 6. roman input (brief §53): headword, label and analysis typed in IAST, converted to Burmese; the Burmese
  //    and its read-back shown; Save refused while the read-back differs; the mode remembered per field
  ctx = await browser.newContext({ locale: 'es-ES' }); page = await ctx.newPage();
  await ctx.route('**/api/admin/**', r => r.continue({ headers: Object.assign({}, r.request().headers(), { 'cf-access-jwt-assertion': token }) }));
  await page.addInitScript(() => localStorage.setItem('abhidhana-editor', '1'));
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('[data-edit]', { timeout: 8000 });
  await page.click('[data-edit]'); await page.waitForSelector('.ed-form');
  const an0 = await page.inputValue('[data-f="analysis"]');
  await page.click('[data-mf="analysis"][data-mode="rom"]');
  ok(await page.inputValue('[data-f="analysis"]') === 'luñca + yu. (ti) luñcana-saṁ.', 'roman: the analysis shown in roman: ' + await page.inputValue('[data-f="analysis"]'));
  ok(await page.evaluate(() => localStorage.getItem('abh-ed-mode-analysis')) === 'rom', 'roman: the mode kept in this browser');
  await page.click('[data-save]'); await page.waitForTimeout(400);
  ok((await page.textContent('.ed-msg')).includes('No ha cambiado'), 'roman: an untouched field is not an edit');
  await page.fill('[data-f="analysis"]', 'omaka + patta');
  ok(await page.textContent('[data-prev="analysis"] [data-store]') === 'ဩမက + ပတ္တ', 'roman: omaka + patta → ' + await page.textContent('[data-prev="analysis"] [data-store]'));
  ok(await page.textContent('[data-prev="analysis"] [data-back]') === 'omaka + patta', 'roman: read-back shown');
  ok(await page.getAttribute('[data-prev="analysis"] .ed-chk', 'data-ok') === 'true' && !(await page.isDisabled('[data-save]')), 'roman: read-back matches, Save enabled');
  await page.fill('[data-f="analysis"]', 'kṛta + ti');
  ok(await page.getAttribute('[data-prev="analysis"] .ed-chk', 'data-ok') === 'false' && await page.isDisabled('[data-save]'), 'roman: a letter it cannot convert (ṛ) → ✗, Save disabled');
  ok(await page.evaluate(() => document.querySelector('.ed-form').classList.length > 0 && !!document.querySelector('[data-prev="analysis"].ed-bad')), 'roman: the failing field marked');
  await page.fill('[data-f="analysis"]', 'Omaka + patta');
  ok(await page.isDisabled('[data-save]'), 'roman: a capital letter → Save disabled');
  await page.fill('[data-f="analysis"]', 'saṃ + gha');
  ok(await page.textContent('[data-prev="analysis"] [data-store]') === 'သံ + ဃ' && !(await page.isDisabled('[data-save]')), 'roman: ṃ read as ṁ');
  await page.fill('[data-f="analysis"]', 'na + kataludda. akata + ludda');
  ok(await page.textContent('[data-prev="analysis"] [data-store]') === 'န + ကတလုဒ္ဒ။ အကတ + လုဒ္ဒ', 'roman: . → ။ in the analysis');
  await page.click('[data-mf="label"][data-mode="rom"]');
  await page.fill('[data-f="label"]', 'ti');
  ok(await page.textContent('[data-prev="label"] [data-store]') === 'တိ', 'roman: label ti → တိ');
  await page.click('[data-mf="headword"][data-mode="rom"]');
  await page.fill('[data-f="headword"]', 'saṅkhāra');
  ok(await page.textContent('[data-prev="headword"] [data-store]') === 'သင်္ခါရ', 'roman: headword saṅkhāra → သင်္ခါရ (kinzi, tall ā)');
  await page.fill('[data-f="headword"]', 'luñcana');
  await page.fill('[data-f="analysis"]', 'omaka + patta');
  await page.screenshot({ path: `${shots}/roman.png`, fullPage: true });
  await page.click('[data-save]'); await page.waitForTimeout(900);
  ok((await page.textContent('.ed-msg')).includes('Guardado'), 'roman: saved: ' + await page.textContent('.ed-msg'));
  ok((await page.textContent('.an')).includes('omaka + patta'), 'roman: the saved analysis shows');
  const hist2 = await (await fetch(B + '/api/edits?book=18')).json();
  const rows2 = JSON.stringify(hist2);
  ok(rows2.includes('ဩမက + ပတ္တ') && !rows2.includes('omaka + patta'), 'roman: the Burmese is what is stored');
  await page.reload(); await page.waitForSelector('[data-edit]', { timeout: 8000 });
  await page.click('[data-edit]'); await page.waitForSelector('.ed-form');
  ok(await page.getAttribute('[data-mf="analysis"][data-mode="rom"]', 'aria-pressed') === 'true' && await page.inputValue('[data-f="analysis"]') === 'omaka + patta', 'reload: the roman mode remembered');
  await page.click('[data-mf="analysis"][data-mode="my"]');
  ok(await page.inputValue('[data-f="analysis"]') === 'ဩမက + ပတ္တ', 'back to Burmese: the field in Burmese');
  await page.click('[data-withdraw="analysis"]'); await page.waitForTimeout(800);
  ok((await page.textContent('.an')).includes('luñca + yu'), 'withdraw: the published analysis again (' + an0 + ')');
  await ctx.close();

  // 4. editor mode set in this browser, but not signed in: no Editar buttons
  ctx = await browser.newContext({ locale: 'en-GB' }); page = await ctx.newPage();
  await page.addInitScript(() => localStorage.setItem('abhidhana-editor', '1'));
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('.meaning'); await page.waitForTimeout(1200);
  ok(!(await page.$('[data-edit]')), 'not signed in: no Edit button');
  ok((await page.textContent('.ed-badge')).includes('not signed in'), 'not signed in: badge says so');
  await ctx.close();

  // 7. Copy / Cite / Share beside the headword (brief §81). The clipboard is read back; navigator.share is taken
  //    away for the fallback (copy the link) and replaced by a stub to see what it would be given
  const MON = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'], NOW = new Date();
  const TODAY = `${NOW.getDate()} ${MON[NOW.getMonth()]} ${NOW.getFullYear()}`;
  const VER = (await (await fetch(B + '/data/version.json')).json()).version;
  const clipAfter = async (sel) => {
    await page.evaluate(() => navigator.clipboard.writeText(''));
    await page.click(sel);
    await page.waitForFunction(() => document.querySelector('.acts-msg').textContent.length > 0, null, { timeout: 5000 }).catch(() => {});
    return [await page.evaluate(() => navigator.clipboard.readText()), await page.textContent('.acts-msg')];
  };
  ctx = await browser.newContext({ locale: 'es-ES', permissions: ['clipboard-read', 'clipboard-write'] }); page = await ctx.newPage();
  await page.addInitScript(() => { Object.defineProperty(Navigator.prototype, 'share', { value: undefined, configurable: true }); });
  await page.goto(B + '/w/bhijja'); await page.waitForSelector('.head .acts [data-act="share"]');
  const acts = await page.$$eval('.head .acts button[data-act]', bs => bs.map(b => [b.dataset.act, b.type, b.getAttribute('aria-label') || '']));
  ok(acts.map(a => a[0]).join() === 'copy,cite,share' && acts.every(a => a[1] === 'button' && a[2]), 'acts: copy, cite, share beside the headword, buttons with aria-label: ' + JSON.stringify(acts));
  await page.waitForTimeout(300);   // /data/version.json read by the page
  const WANT = `Tipiṭaka Pāḷi-Myanmā Abhidhāna, vol. 15 (suplemento, encuadernado en el vol. 4/3), p. 686 (p. del PDF 713), s.v. bhijja. Edición digital, IEBH, v${VER}. https://abhidhana.buddha-dhamma.net/w/bhijja (consultado el ${TODAY}).`;
  let [clip, msg] = await clipAfter('[data-act="cite"]');
  ok(clip === WANT, 'Cite /w/bhijja: ' + clip);
  ok(msg === 'cita copiada', 'Cite: flash "' + msg + '"');
  [clip, msg] = await clipAfter('[data-act="copy"]');
  const lines = clip.split('\n');
  const mi = lines.findIndex(l => l.startsWith('Significado'));
  ok(lines[0] === 'bhijja · ဘိဇ္ဇ' && /^Significado: \S/.test(lines[mi] || '') &&
     lines[mi + 1] === 'borrador · Traducción del birmano al español hecha con IA, sin revisar. No es una lectura.' &&
     lines.some(l => l.startsWith('Definición birmana (texto del diccionario;')) &&
     lines[lines.length - 1] === 'Tipiṭaka Pāḷi-Myanmā Abhidhāna — edición digital del IEBH (lo añadido, CC BY-SA 4.0; el texto del diccionario no se relicencia) — https://abhidhana.buddha-dhamma.net/w/bhijja',
     'Copy /w/bhijja: headword, status borrador, the Burmese marked as the dictionary\'s, attribution: ' + JSON.stringify(lines.map(l => l.slice(0, 60))));
  [clip, msg] = await clipAfter('[data-act="share"]');
  ok(clip === 'https://abhidhana.buddha-dhamma.net/w/bhijja' && msg === 'enlace copiado', 'Share without navigator.share: the link copied, "' + msg + '"');
  // the Copy of an edited article carries the edit's status (luñcana: sense 1 corrected in step 3)
  await page.goto(B + '/w/luñcana'); await page.waitForSelector('.head .acts'); await page.waitForTimeout(800);
  [clip] = await clipAfter('[data-act="copy"]');
  ok(clip.includes('\nSignificado: ') && clip.includes('\ncorregido en parte · Corregido por el editor: sentido (1). El resto es borrador, sin revisar.\n'), 'Copy /w/luñcana: the status from editor mode: ' + (clip.split('\n').find(l => l.startsWith('corregido')) || '').slice(0, 90));
  // English: the citation's words and date
  await page.evaluate(() => localStorage.setItem('lang', 'en'));
  await page.goto(B + '/w/bhijja'); await page.waitForSelector('.head .acts'); await page.waitForTimeout(300);
  [clip] = await clipAfter('[data-act="cite"]');
  const EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][NOW.getMonth()];
  ok(clip === `Tipiṭaka Pāḷi-Myanmā Abhidhāna, vol. 15 (supplement, bound in vol. 4/3), p. 686 (PDF p. 713), s.v. bhijja. Digital edition, IEBH, v${VER}. https://abhidhana.buddha-dhamma.net/w/bhijja (accessed ${NOW.getDate()} ${EN} ${NOW.getFullYear()}).`, 'Cite in English: ' + clip);
  await ctx.close();
  // navigator.share, where there is one: given the title, the citation and the address
  ctx = await browser.newContext({ locale: 'es-ES', permissions: ['clipboard-read', 'clipboard-write'] }); page = await ctx.newPage();
  await page.addInitScript(() => { window.__shared = null; Object.defineProperty(Navigator.prototype, 'share', { value: function (o) { window.__shared = o; return Promise.resolve(); }, configurable: true }); });
  await page.goto(B + '/w/bhijja'); await page.waitForSelector('.head .acts'); await page.waitForTimeout(300);
  await page.click('[data-act="share"]'); await page.waitForTimeout(200);
  const sh = await page.evaluate(() => window.__shared);
  ok(sh && sh.url === 'https://abhidhana.buddha-dhamma.net/w/bhijja' && sh.text === WANT && /bhijja/.test(sh.title), 'Share: navigator.share given ' + JSON.stringify(sh));
  // 375 px (brief §83): below 768 px the buttons sit out of the flow, above the meta line, so they never add a line to the
  // head, whatever it holds. Three articles: bhijja (a supplement row); luñcana with step 6's edits (a label and the
  // *corregido* chips); bhijjanasabhāva² (a homonym with its superscript, a supplement row, *análisis no leído*), shown
  // with both scripts and the labels in full, and given the longest label (ကြိ၊ဝိ) by an edit here, so its *corregido* chip
  // shows. Real fonts: the page's Google Fonts, or with ABH_FONTS=<folder> a local copy (fonts.css + its .woff2 files).
  if (process.env.ABH_FONTS) {
    const F = process.env.ABH_FONTS, fsp = require('fs'), pth = require('path');
    await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ path: pth.join(F, 'fonts.css'), contentType: 'text/css' }));
    await page.route(/\/__fonts\//, r => r.fulfill({ path: pth.join(F, pth.basename(new URL(r.request().url()).pathname)), contentType: 'font/woff2' }));
  }
  const lab = await fetch(B + '/api/admin/edits', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Abhidhana-Editor': '1', Origin: B, 'Cf-Access-Jwt-Assertion': token },
    body: JSON.stringify({ book: '4c', id: 177224, edits: [{ field: 'label', value: 'ကြိ၊ဝိ', old: 'တိ' }] }) });
  ok(lab.status === 200, 'seeded a label edit of bhijjanasabhāva² (4c 177224) through the API: ' + lab.status);
  await page.setViewportSize({ width: 375, height: 812 });
  const LONG = { mode: 'custom', script: 'both', defs: 'collapse', labels: 'full', scan: false };
  for (const [w, set] of [['bhijja', null], ['luñcana', null], ['bhijjanasabhāva-2', LONG]]) {
    await page.evaluate(s => s ? localStorage.setItem('browse', JSON.stringify(s)) : localStorage.removeItem('browse'), set);
    await page.goto(B + '/w/' + w); await page.waitForSelector('.meaning'); await page.waitForTimeout(800);
    await page.evaluate(() => document.fonts.ready);
    const fonts = await page.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')))].sort().join(', ') || 'none loaded');
    const g = await page.evaluate(() => {
      const q = s => document.querySelector(s), R = e => e.getBoundingClientRect(), A = R(q('.head .acts'));
      const hit = r => r.width && r.left < A.right - 0.5 && r.right > A.left + 0.5 && r.top < A.bottom - 0.5 && r.bottom > A.top + 0.5;
      const txt = []; const tw = document.createTreeWalker(q('.where'), NodeFilter.SHOW_TEXT); let n;
      while ((n = tw.nextNode())) { const rg = document.createRange(); rg.selectNodeContents(n); txt.push(...rg.getClientRects()); }
      q('.where').querySelectorAll('.chip').forEach(e => txt.push(R(e)));
      const head = [...q('.head').children].filter(e => !e.classList.contains('acts')).map(R);
      return { y: R(q('.meaning')).top, h: R(q('.head')).height, sw: document.documentElement.scrollWidth, over: txt.some(hit) || head.some(hit),
        inside: A.left >= 0 && A.right <= innerWidth, sup: !!q('.head h1 sup'), lab: !!q('.head .lab'), my: !!q('.head .hw-my'), fixed: !!q('.head .chip.c-ok'),
        homs: !!q('.head .homs'), nr: !!q('.head .notread'), supp: /suplemento/.test(q('.where').textContent) };
    });
    await page.screenshot({ path: `${shots}/375-${w}.png` });
    await page.addStyleTag({ content: '.acts{display:none!important}' });
    const y0 = await page.evaluate(() => document.querySelector('.meaning').getBoundingClientRect().top);
    const h0 = await page.evaluate(() => document.querySelector('.head').getBoundingClientRect().height);
    const holds = Object.entries(g).filter(([k, v]) => ['sup', 'lab', 'my', 'fixed', 'homs', 'nr', 'supp'].includes(k) && v).map(([k]) => k).join(' ');
    ok(Math.abs(g.y - y0) < 1 && Math.abs(g.h - h0) < 1 && g.sw <= 375 && !g.over && g.inside,
      `375 px /w/${w} [${holds}]: Meaning box at ${g.y.toFixed(0)} px with the buttons, ${y0.toFixed(0)} without; head ${g.h.toFixed(0)} / ${h0.toFixed(0)} px; ` +
      `buttons ${g.over ? 'OVERLAP the head or the meta line' : 'clear of the head and the meta line'}${g.inside ? '' : ', OUTSIDE the page'}; page width ${g.sw}; fonts: ${fonts}`);
    if (w === 'bhijjanasabhāva-2') ok(g.sup && g.lab && g.my && g.fixed && g.homs && g.nr && g.supp, `375 px /w/${w}: the long head holds a superscript, both scripts, a label, a corregido chip, the homonyms, a "not read" note, a supplement row: ${holds}`);
  }
  await page.evaluate(() => localStorage.removeItem('browse'));
  await ctx.close();

  // 8. a Meaning's numbered senses as a list (brief §84; display only). karoti: a lead ("hace;"), 18 senses folded to
  //    8 + "mostrar todo (18)"; bhava in English: 16 senses, (5) with (a) (b) nested; bhijja, luñcana: no numbers;
  //    kāyaggahaṇa: "(3)" printed twice; kaṁsatālakaṭṭhatālasadda: "Véase [[kaṁsatāla]] (1)": paragraphs as before. The
  //    marker's text clear of its sense (≥ 3 px), every line of a sense at the same x, no gap between senses, one font
  //    size; Copy the plain text; at 375 px the buttons of §81/§83 add no line; real fonts as in step 7 (ABH_FONTS).
  const geo = () => {
    const q = s => document.querySelector(s), box = q('.meaning > div[lang]'), L = box && box.querySelector(':scope > ol.senses');
    const R = e => e.getBoundingClientRect(), out = { list: !!L, sw: document.documentElement.scrollWidth, y: R(q('.meaning')).top, hh: R(q('.head')).height };
    if (!L) return out;
    const lines = li => {   // the left edge of each line of the sense's own text (not its marker, not a nested list)
      const tw = document.createTreeWalker(li, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest('.sn') || n.parentElement.closest('ol') !== li.parentElement ? 2 : 1 });
      const by = {}; let n;
      while ((n = tw.nextNode())) { const rg = document.createRange(); rg.selectNodeContents(n); for (const r of rg.getClientRects()) if (r.width) { const k = Math.round(r.top); by[k] = Math.min(by[k] ?? 1e9, r.left); } }
      return Object.values(by);
    };
    const lis = [...box.querySelectorAll('ol.senses > li')], top = [...L.children]; let hang = true, gap = 0, lineN = 0; const fs = new Set();
    for (const li of lis) {
      const cs = getComputedStyle(li), x0 = R(li).left + parseFloat(cs.paddingLeft), sn = li.querySelector(':scope > .sn');
      fs.add(cs.fontSize); fs.add(getComputedStyle(sn).fontSize);
      const ls = lines(li); lineN = Math.max(lineN, ls.length);
      const rs = document.createRange(); rs.selectNodeContents(sn);
      if (rs.getBoundingClientRect().right > x0 - 3 || ls.some(l => Math.abs(l - x0) > 1)) hang = false;
      const sub = li.querySelector(':scope > ol.senses'); if (sub && Math.abs(R(sub).left - x0) > 1) hang = false;
    }
    for (let j = 1; j < top.length; j++) gap = Math.max(gap, Math.abs(R(top[j]).top - R(top[j - 1]).bottom));
    const btn = box.querySelector('[data-fold="mall"]');
    return Object.assign(out, { n: top.length, mk: top.map(li => li.querySelector('.sn').textContent), lead: (box.querySelector(':scope > .s-lead') || {}).textContent || '',
      sub: box.querySelectorAll('ol.senses.sub').length, hang, gap, lineN, fs: [...new Set([...fs, getComputedStyle(box).fontSize])], btn: btn ? btn.textContent : '' });
  };
  for (const [W, H] of [[375, 812], [1280, 900]]) {
    ctx = await browser.newContext({ locale: 'es-ES', viewport: { width: W, height: H } }); page = await ctx.newPage();
    if (process.env.ABH_FONTS) {
      const F = process.env.ABH_FONTS, pth = require('path');
      await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ path: pth.join(F, 'fonts.css'), contentType: 'text/css' }));
      await page.route(/\/__fonts\//, r => r.fulfill({ path: pth.join(F, pth.basename(new URL(r.request().url()).pathname)), contentType: 'font/woff2' }));
    }
    const errs = []; page.on('pageerror', e => errs.push(String(e)));
    const go = async (w, lang) => {
      await page.evaluate(l => localStorage.setItem('lang', l), lang);
      await page.goto(B + '/w/' + w); await page.waitForSelector('.meaning'); await page.waitForTimeout(800);
      await page.evaluate(() => document.fonts.ready);
      return page.evaluate(geo);
    };
    await page.goto(B + '/');
    let g = await go('karoti', 'es');
    const fonts = await page.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')))].sort().join(', ') || 'none loaded');
    ok(g.list && g.lead === 'hace;' && g.n === 8 && g.mk.join('') === '(1)(2)(3)(4)(5)(6)(7)(8)' && g.btn === 'mostrar todo (18)',
      `senses ${W} px /w/karoti: lead "${g.lead}", ${g.n} shown ${g.mk.join('')}, "${g.btn}"`);
    ok(g.hang && g.gap < 0.5 && g.fs.length === 1, `senses ${W} px /w/karoti: hanging indent ${g.hang}, gap ${g.gap.toFixed(2)} px, font size ${g.fs.join(' / ')}`);
    ok(g.sw <= W, `senses ${W} px /w/karoti: page width ${g.sw}; fonts: ${fonts}`);
    await page.screenshot({ path: `${shots}/senses-${W}-karoti.png`, fullPage: W === 375 });
    if (W === 375) {
      const st = await page.addStyleTag({ content: '.acts{display:none!important}' }); const g0 = await page.evaluate(geo); await st.evaluate(e => e.remove());
      ok(Math.abs(g0.y - g.y) < 1 && Math.abs(g0.hh - g.hh) < 1, `senses 375 px /w/karoti: Meaning box at ${g.y.toFixed(0)} px with the buttons, ${g0.y.toFixed(0)} without`);
    }
    await page.click('[data-fold="mall"]'); g = await page.evaluate(geo);
    ok(g.n === 18 && g.mk[17] === '(18)' && g.btn === 'mostrar menos' && g.hang && g.gap < 0.5, `senses ${W} px /w/karoti unfolded: ${g.n}, last ${g.mk[17]}, "${g.btn}"`);
    await page.click('[data-fold="mall"]'); g = await page.evaluate(geo);
    ok(g.n === 8, `senses ${W} px /w/karoti folded back: ${g.n}`);
    const cp = await page.evaluate(() => ABH_ACTS.copyText());
    ok(cp.includes('Significado: hace; (1) produce; (2) practica. (3) pone.') && cp.includes('\nborrador · Traducción del birmano al español hecha con IA, sin revisar. No es una lectura.\n'),
      `senses ${W} px /w/karoti: Copy keeps the plain text: ` + (cp.split('\n').find(l => l.startsWith('Significado')) || '').slice(0, 90));
    g = await go('bhava', 'en');
    ok(g.list && g.n === 8 && g.btn === 'show all (16)' && g.sub === 1 && g.hang && g.gap < 0.5 && g.fs.length === 1 && g.sw <= W,
      `senses ${W} px /w/bhava (EN): ${g.n} shown, "${g.btn}", ${g.sub} nested list, hanging ${g.hang}, longest sense ${g.lineN} lines, page width ${g.sw}`);
    await page.screenshot({ path: `${shots}/senses-${W}-bhava-en.png`, fullPage: W === 375 });
    for (const [w, why] of [['bhijja', 'no numbers'], ['luñcana', 'no numbers'], ['kāyaggahaṇa', '(3) printed twice'], ['kaṁsatālakaṭṭhatālasadda', 'Véase … (1)']]) {
      g = await go(w, 'es');
      ok(!g.list && g.sw <= W, `senses ${W} px /w/${w}: a paragraph (${why}); page width ${g.sw}`);
      if (W === 375 && (w === 'bhijja' || w === 'luñcana')) {
        const st = await page.addStyleTag({ content: '.acts{display:none!important}' }); const g0 = await page.evaluate(geo); await st.evaluate(e => e.remove());
        ok(Math.abs(g0.y - g.y) < 1, `senses 375 px /w/${w}: Meaning box at ${g.y.toFixed(0)} px with the buttons, ${g0.y.toFixed(0)} without`);
      }
    }
    ok(!errs.length, `senses ${W} px: no script errors ${errs.join(' | ')}`);
    await page.evaluate(() => localStorage.removeItem('lang'));
    await ctx.close();
  }
  // 9. the Meaning's status below its text (brief §93): a small muted badge and its note on one line, ES and EN,
  //    at 375 and 1,024 px; Copy in English writes the same line
  for (const [W, H] of [[375, 812], [1024, 800]]) {
    ctx = await browser.newContext({ locale: 'es-ES', viewport: { width: W, height: H }, permissions: ['clipboard-read', 'clipboard-write'] }); page = await ctx.newPage();
    if (process.env.ABH_FONTS) {
      const F = process.env.ABH_FONTS, pth = require('path');
      await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ path: pth.join(F, 'fonts.css'), contentType: 'text/css' }));
      await page.route(/\/__fonts\//, r => r.fulfill({ path: pth.join(F, pth.basename(new URL(r.request().url()).pathname)), contentType: 'font/woff2' }));
    }
    await page.goto(B + '/');
    for (const [lang, badge, note] of [['es', 'borrador', 'Traducción del birmano al español hecha con IA, sin revisar. No es una lectura.'],
                                       ['en', 'draft', 'AI translation from the Burmese, unreviewed. Not a reading.']]) {
      await page.evaluate(l => localStorage.setItem('lang', l), lang);
      await page.goto(B + '/w/bhijja'); await page.waitForSelector('.meaning .mstat'); await page.waitForTimeout(500);
      await page.evaluate(() => document.fonts.ready);
      const g = await page.evaluate(() => {
        const q = s => document.querySelector(s), R = e => e.getBoundingClientRect(), box = q('.meaning'), st = q('.meaning .mstat'), b = st.querySelector('.mbadge');
        const nt = st.lastElementChild, rg = document.createRange(); rg.selectNodeContents(nt); const r1 = rg.getClientRects()[0];
        const css = e => getComputedStyle(e), txt = q('.meaning > div[lang]');
        return { after: st.previousElementSibling === txt && R(st).top >= R(txt).bottom - 0.5, badge: b.textContent, note: nt.textContent,
          line: Math.abs((R(b).top + R(b).bottom) / 2 - (r1.top + r1.bottom) / 2) < 4, small: parseFloat(css(b).fontSize) < parseFloat(css(txt).fontSize) && parseFloat(css(st).fontSize) < parseFloat(css(txt).fontSize),
          muted: css(b).color === css(st).color && css(st).color !== css(txt).color, chips: box.querySelectorAll('.chip').length,
          old: /Traducción en borrador|Drafted translation/.test(box.textContent), inside: R(st).right <= R(box).right + 0.5, sw: document.documentElement.scrollWidth };
      });
      await page.screenshot({ path: `${shots}/meaning-${W}-${lang}.png` });
      ok(g.after && g.badge === badge && g.note === note && g.line && g.small && g.muted && !g.chips && !g.old && g.inside && g.sw <= W,
        `status ${W} px /w/bhijja (${lang}): below the text ${g.after}, "${g.badge}" · "${g.note.slice(0, 40)}…", one line ${g.line}, smaller ${g.small}, muted ${g.muted}, chips in the box ${g.chips}, page width ${g.sw}`);
      if (W === 1024 && lang === 'en') {
        await page.evaluate(() => navigator.clipboard.writeText('')); await page.click('[data-act="copy"]'); await page.waitForTimeout(300);
        const cl = (await page.evaluate(() => navigator.clipboard.readText())).split('\n'), j = cl.findIndex(l => l.startsWith('Meaning: '));
        ok(j > 0 && cl[j + 1] === 'draft · AI translation from the Burmese, unreviewed. Not a reading.', 'Copy /w/bhijja (en): ' + JSON.stringify(cl.slice(j, j + 2).map(l => l.slice(0, 70))));
      }
    }
    await page.evaluate(() => localStorage.removeItem('lang'));
    await ctx.close();
  }
  await browser.close();
  console.log(`pass ${pass} fail ${fail}`);
  process.exitCode = fail ? 1 : 0;
})();
