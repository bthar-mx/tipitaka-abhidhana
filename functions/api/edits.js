// GET /api/edits?book=NN — public: the latest saved edit per id + field + sense of a book, which Browse
// lays over the static data (site/src/assets/browse.js). ?book=all gives every book (for
// tools/abhidhana_edits_export.py). Kept 60 s in the edge cache; a write clears its book's entry.
import { BOOK, json, latest } from '../_lib/edits.js';

export async function onRequestGet({ request, env, waitUntil }) {
  const url = new URL(request.url), book = url.searchParams.get('book') || '';
  if (book !== 'all' && !BOOK.test(book)) return json({ error: 'book=NN (01–25, 4a–4c, 14b, 14c) or book=all' }, 400);
  if (!env.DB) return json({ error: 'no database bound' }, 503);
  const key = new Request(`${url.origin}/api/edits?book=${book}`), cache = caches.default;
  const hit = await cache.match(key);
  if (hit) return hit;
  const edits = await latest(env.DB, book === 'all' ? null : book);
  const res = json({ book, n: edits.length, edits }, 200, { 'Cache-Control': 'public, max-age=0, s-maxage=60' });
  waitUntil(cache.put(key, res.clone()));
  return res;
}
