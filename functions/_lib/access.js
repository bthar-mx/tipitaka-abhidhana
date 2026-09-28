// Cloudflare Access, checked by the function itself (docs/editor-mode.md). Access, when its rule covers
// /api/admin/, puts a signed JWT in the Cf-Access-Jwt-Assertion header of every request it lets through.
// The write API verifies that token (RS256 against the team's published keys; audience, issuer, expiry)
// so that a missing or misconfigured rule, or the *.pages.dev address, which Access does not cover,
// does not leave the API open. Configuration, set in the Pages project (never in the repo):
//   ACCESS_TEAM_DOMAIN  https://<team>.cloudflareaccess.com   (the token's issuer; keys at /cdn-cgi/access/certs)
//   ACCESS_AUD          the Access application's Audience (AUD) tag
//   EDITOR_EMAILS       optional: comma-separated addresses allowed to write, a second check beside the rule
// Missing configuration refuses every write (503).

let KEYS = null, KEYS_AT = 0;   // the team's public keys, kept for ten minutes per isolate

const b64url = s => {
  s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '=';
  return Uint8Array.from(atob(s), c => c.charCodeAt(0));
};
const json64 = s => JSON.parse(new TextDecoder().decode(b64url(s)));

async function keys(team, force) {
  if (KEYS && !force && Date.now() - KEYS_AT < 600000) return KEYS;
  const r = await fetch(`${team}/cdn-cgi/access/certs`);
  if (!r.ok) throw new Error(`certs ${r.status}`);
  KEYS = (await r.json()).keys || []; KEYS_AT = Date.now();
  return KEYS;
}

// -> {email} or throws {status, message}
export async function verifyAccess(request, env) {
  const team = (env.ACCESS_TEAM_DOMAIN || '').replace(/\/+$/, ''), aud = env.ACCESS_AUD || '';
  if (!team || !aud) throw { status: 503, message: 'editor mode is not configured (ACCESS_TEAM_DOMAIN, ACCESS_AUD)' };
  const token = request.headers.get('Cf-Access-Jwt-Assertion');
  if (!token) throw { status: 401, message: 'no Access token' };
  const parts = token.split('.');
  if (parts.length !== 3) throw { status: 403, message: 'malformed token' };
  let head, body;
  try { head = json64(parts[0]); body = json64(parts[1]); } catch (e) { throw { status: 403, message: 'malformed token' }; }
  if (head.alg !== 'RS256') throw { status: 403, message: 'unexpected algorithm' };
  let jwk = (await keys(team)).find(k => k.kid === head.kid);
  if (!jwk) jwk = (await keys(team, true)).find(k => k.kid === head.kid);   // keys rotate
  if (!jwk) throw { status: 403, message: 'unknown signing key' };
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64url(parts[2]),
    new TextEncoder().encode(parts[0] + '.' + parts[1]));
  if (!ok) throw { status: 403, message: 'bad signature' };
  const now = Math.floor(Date.now() / 1000), auds = [].concat(body.aud || []);
  if (!auds.includes(aud)) throw { status: 403, message: 'wrong audience' };
  if (body.iss !== team) throw { status: 403, message: 'wrong issuer' };
  if (!body.exp || body.exp < now - 30) throw { status: 403, message: 'token expired' };
  if (body.nbf && body.nbf > now + 30) throw { status: 403, message: 'token not yet valid' };
  const email = (body.email || '').toLowerCase();
  const allowed = (env.EDITOR_EMAILS || '').split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
  if (allowed.length && !allowed.includes(email)) throw { status: 403, message: 'not an editor' };
  return { email };
}
