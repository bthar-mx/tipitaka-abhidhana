// /api/admin/edits — the editor's writes (behind Access; functions/api/admin/_middleware.js).
//   GET  ?book=NN&id=N&limit=N   the history, newest first (every row, withdrawn ones too)
//   POST {book, id, edits: [{field, sense, value, old, status}]}   saves the rows, all or none;
//        answers with the book's latest edits for that id
import { check, json, latest } from '../../_lib/edits.js';

export async function onRequestGet({ request, env }) {
  if (!env.DB) return json({ error: 'no database bound' }, 503);
  const u = new URL(request.url).searchParams, where = [], args = [];
  if (u.get('book')) { where.push(`book = ?${args.length + 1}`); args.push(u.get('book')); }
  if (u.get('id')) { where.push(`id = ?${args.length + 1}`); args.push(parseInt(u.get('id'), 10) || 0); }
  const limit = Math.min(Math.max(parseInt(u.get('limit') || '200', 10) || 200, 1), 5000);
  const q = `SELECT rowid AS n, id, book, field, sense, value, old, status, date FROM edits
    ${where.length ? 'WHERE ' + where.join(' AND ') : ''} ORDER BY rowid DESC LIMIT ${limit}`;
  const rows = (await env.DB.prepare(q).bind(...args).all()).results;
  return json({ n: rows.length, edits: rows });
}

export async function onRequestPost({ request, env, waitUntil }) {
  if (!env.DB) return json({ error: 'no database bound' }, 503);
  if (!(request.headers.get('Content-Type') || '').startsWith('application/json')) return json({ error: 'JSON only' }, 415);
  const text = await request.text();
  if (text.length > 200000) return json({ error: 'too large' }, 413);
  let body; try { body = JSON.parse(text); } catch (e) { return json({ error: 'bad JSON' }, 400); }
  const book = String(body.book || ''), id = body.id;
  if (!Array.isArray(body.edits) || !body.edits.length || body.edits.length > 20) return json({ error: 'edits: 1 to 20 rows' }, 400);
  const rows = [];
  for (const e of body.edits) {
    const r = check(book, id, e || {});
    if (typeof r === 'string') return json({ error: r }, 400);
    rows.push(r);
  }
  const date = new Date().toISOString();
  const ins = env.DB.prepare('INSERT INTO edits (id, book, field, sense, value, old, status, date) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)');
  await env.DB.batch(rows.map(r => ins.bind(r.id, r.book, r.field, r.sense, r.value, r.old, r.status, date)));
  // the public read of this book is cached for 60 s: drop it so the edit shows at once
  const origin = new URL(request.url).origin;
  waitUntil(caches.default.delete(new Request(`${origin}/api/edits?book=${book}`)));
  const now = (await latest(env.DB, book)).filter(r => r.id === id);
  return json({ saved: rows.length, date, latest: now });
}
