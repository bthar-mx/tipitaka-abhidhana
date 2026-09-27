// The editor API against `wrangler pages dev` with an empty local D1 (run.sh). Access is simulated:
// access-mock.js serves the signing keys and mints tokens.
const { mint } = require('./access-mock.js');
const B = process.env.BASE || 'http://127.0.0.1:8788';
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
async function call(method, path, { token, body, origin = B, hdr = true } = {}) {
  const h = {};
  if (token) h['Cf-Access-Jwt-Assertion'] = token;
  if (body) { h['Content-Type'] = 'application/json'; if (hdr) h['X-Abhidhana-Editor'] = '1'; if (origin) h['Origin'] = origin; }
  const r = await fetch(B + path, { method, headers: h, body: body ? JSON.stringify(body) : undefined });
  let j = null; try { j = await r.json(); } catch (e) {}
  return { s: r.status, j };
}
(async () => {
  const good = mint({});
  const E = { book: '18', id: 140731, edits: [{ field: 'es', value: '(1) obtendrá. (2) llegará. (3) verá.', old: 'x' }] };
  // the write API refuses without a valid Access token
  let r = await call('GET', '/api/admin/whoami'); ok(r.s === 401, 'no token 401 ' + r.s);
  r = await call('POST', '/api/admin/edits', { body: E }); ok(r.s === 401, 'post no token ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: mint({}, { otherKey: true }), body: E }); ok(r.s === 403 && /signature/.test(r.j.error), 'forged ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: mint({ aud: ['other'] }), body: E }); ok(r.s === 403 && /audience/.test(r.j.error), 'aud ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: mint({ iss: 'https://evil.cloudflareaccess.com' }), body: E }); ok(r.s === 403 && /issuer/.test(r.j.error), 'iss ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: mint({ exp: Math.floor(Date.now() / 1000) - 3600 }), body: E }); ok(r.s === 403 && /expired/.test(r.j.error), 'exp ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: mint({}, { kid: 'nope' }), body: E }); ok(r.s === 403 && /key/.test(r.j.error), 'kid ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: 'abc.def', body: E }); ok(r.s === 403, 'malformed ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: good, body: E, origin: 'https://evil.example' }); ok(r.s === 403 && /cross-site/.test(r.j.error), 'origin ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: good, body: E, hdr: false }); ok(r.s === 403, 'no custom header ' + r.s);
  // validation
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '99', id: 1, edits: [{ field: 'es', value: 'a' }] } }); ok(r.s === 400, 'bad book ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 1, edits: [{ field: 'xx', value: 'a' }] } }); ok(r.s === 400, 'bad field ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 1, edits: [{ field: 'es', value: 'a', sense: '1' }] } }); ok(r.s === 400, 'sense on es ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 1, edits: [{ field: 'status', value: 'great' }] } }); ok(r.s === 400, 'bad status value ' + r.s);
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 1, edits: [{ field: 'es', value: '  ' }] } }); ok(r.s === 400, 'empty ' + r.s);
  // good writes
  r = await call('GET', '/api/admin/whoami', { token: good }); ok(r.s === 200 && r.j.email === 'editor@example.org', 'whoami ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: good, body: E }); ok(r.s === 200 && r.j.saved === 1, 'save ' + JSON.stringify(r));
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 140731, edits: [{ field: 'es', value: '(1) obtendrá. (2) llegará. (3) verá / encontrará.' }, { field: 'status', sense: '1', value: 'corrected' }] } });
  ok(r.s === 200 && r.j.saved === 2 && r.j.latest.length === 2, 'save 2 ' + JSON.stringify(r.j));
  ok(r.j.latest.find(e => e.field === 'es').value.endsWith('encontrará.'), 'latest es is the newer');
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '4c', id: 176134, edits: [{ field: 'analysis', value: 'ဩမကာ + ဒေသနာ', old: 'ဩမကာ + ဒေသနာ' }] } }); ok(r.s === 200, 'save 4c');
  // history keeps everything; the public read has the latest
  r = await call('GET', '/api/admin/edits?book=18&id=140731', { token: good }); ok(r.j.n === 3, 'history 3 rows ' + r.j.n);
  r = await call('GET', '/api/edits?book=18'); ok(r.s === 200 && r.j.n === 2, 'public latest 2 ' + JSON.stringify(r.j));
  // withdraw the es edit -> public no longer has it (after the cache entry is dropped)
  r = await call('POST', '/api/admin/edits', { token: good, body: { book: '18', id: 140731, edits: [{ field: 'es', status: 'reverted' }] } }); ok(r.s === 200 && r.j.latest.length === 1, 'withdraw ' + JSON.stringify(r.j));
  r = await call('GET', '/api/edits?book=18'); ok(r.j.n === 1 && r.j.edits[0].field === 'status', 'public after withdraw ' + JSON.stringify(r.j));
  r = await call('GET', '/api/edits?book=all'); ok(r.j.n === 2, 'all books ' + r.j.n);
  r = await call('GET', '/api/edits?book=zz'); ok(r.s === 400, 'bad book read');
  r = await call('GET', '/api/admin/edits', { token: good }); ok(r.j.n === 5, 'history all ' + r.j.n);
  r = await fetch(B + '/_lib/access'); ok(!(await r.text()).includes('verifyAccess'), 'functions/_lib is not served');
  console.log(`pass ${pass} fail ${fail}`);
  process.exitCode = fail ? 1 : 0;
})();
