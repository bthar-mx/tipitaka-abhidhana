// Every /api/admin/ request: the Access token must verify (functions/_lib/access.js), and a write must
// come from this site's own pages (same Origin, and a header a cross-site form cannot send).
import { verifyAccess } from '../../_lib/access.js';
import { json } from '../../_lib/edits.js';

export async function onRequest(ctx) {
  const { request, env } = ctx;
  try { ctx.data.editor = await verifyAccess(request, env); }
  catch (e) {
    if (e && e.status) return json({ error: e.message }, e.status);
    return json({ error: 'the Access keys could not be read' }, 503);
  }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    const origin = request.headers.get('Origin'), self = new URL(request.url).origin;
    if (origin !== self || request.headers.get('X-Abhidhana-Editor') !== '1') return json({ error: 'cross-site write refused' }, 403);
  }
  return ctx.next();
}
