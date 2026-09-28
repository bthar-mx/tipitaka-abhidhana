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
  ok(m.includes('quitar / arrancar (prueba).') && m.includes('corregido'), 'visitor: overlaid Spanish, marked corregido: ' + m.slice(0, 120));
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
  ok(m.includes('quitar / arrancar.') && m.includes('revisado'), 'after save: new text, revisado: ' + m.slice(0, 80));
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
  await browser.close();
  console.log(`pass ${pass} fail ${fail}`);
  process.exitCode = fail ? 1 : 0;
})();
