// A stand-in for Cloudflare Access in local tests: serves /cdn-cgi/access/certs and mints tokens.
const crypto = require('crypto'), http = require('http'), fs = require('fs'), path = require('path');
const kf = path.join(process.env.TMPDIR || require('os').tmpdir(), 'abhidhana-access-mock-key.pem');
if (!fs.existsSync(kf)) fs.writeFileSync(kf, crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs8', format: 'pem' }));
const priv = crypto.createPrivateKey(fs.readFileSync(kf)), pub = crypto.createPublicKey(priv);
const jwk = Object.assign(pub.export({ format: 'jwk' }), { kid: 'k1', alg: 'RS256', use: 'sig' });
const b64 = o => Buffer.from(typeof o === 'string' ? o : JSON.stringify(o)).toString('base64url');
function mint(claims, opt = {}) {
  const now = Math.floor(Date.now() / 1000);
  const body = Object.assign({ aud: ['test-aud'], iss: 'http://127.0.0.1:8799', email: 'editor@example.org', iat: now, exp: now + 3600 }, claims);
  const h = b64({ alg: 'RS256', kid: opt.kid || 'k1', typ: 'JWT' }), p = b64(body);
  const key = opt.otherKey ? crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey : priv;
  return `${h}.${p}.` + crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), key).toString('base64url');
}
module.exports = { mint };
if (require.main === module) {
  http.createServer((q, r) => {
    if (q.url === '/cdn-cgi/access/certs') { r.setHeader('Content-Type', 'application/json'); return r.end(JSON.stringify({ keys: [jwk] })); }
    r.statusCode = 404; r.end();
  }).listen(8799, '127.0.0.1', () => console.log('access mock on 8799'));
}
