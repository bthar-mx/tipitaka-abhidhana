// The editor's edits, in the D1 database bound as DB (docs/editor-mode.md for the schema).
// Every edit is kept (a history); what the site shows is the latest row per id + field + sense
// (by insertion order), unless that row withdraws the edit (status 'reverted').

export const FIELDS = ['es', 'en', 'status', 'analysis', 'label', 'body', 'headword'];
export const BOOK = /^(?:0[1-9]|1[0-9]|2[0-5]|4[abc]|14[bc])$/;
const SENSE = /^(?:[1-9][0-9]?(?:,[1-9][0-9]?)*)?$/;

export const json = (obj, status = 200, headers = {}) => new Response(JSON.stringify(obj), {
  status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers },
});

// the latest row per id + field + sense of one book, or of every book (book = null)
export async function latest(db, book) {
  const where = book ? 'WHERE book = ?1' : '';
  const q = `SELECT e.id, e.book, e.field, e.sense, e.value, e.old, e.status, e.date FROM edits e
    JOIN (SELECT MAX(rowid) AS r FROM edits ${where} GROUP BY id, field, sense) m ON e.rowid = m.r
    WHERE e.status != 'reverted' ORDER BY e.id, e.field, e.sense`;
  const st = book ? db.prepare(q).bind(book) : db.prepare(q);
  return (await st.all()).results;
}

// one edit as sent by the form -> a row, or a string saying what is wrong
export function check(book, id, e) {
  if (!BOOK.test(book)) return `book ${book}?`;
  if (!Number.isInteger(id) || id < 1) return `id ${id}?`;
  if (!FIELDS.includes(e.field)) return `field ${e.field}?`;
  const sense = String(e.sense ?? '').replace(/\s+/g, '');
  if (!SENSE.test(sense)) return `sense ${e.sense}? (blank for the whole, or 1 or 1,3)`;
  if (sense && e.field !== 'status') return 'a sense applies to the status only';
  const status = e.status || 'saved';
  if (!['saved', 'reverted'].includes(status)) return `status ${status}?`;
  let value = typeof e.value === 'string' ? e.value.normalize('NFC').trim() : '';
  if (status === 'saved') {
    if (!value) return `${e.field}: empty value (to go back to the published text, withdraw the edit)`;
    if (e.field === 'status' && !['reviewed', 'corrected', 'drafted'].includes(value)) return `status value ${value}?`;
    if (value.length > 20000) return `${e.field}: too long`;
  } else value = '';
  const old = typeof e.old === 'string' ? e.old.normalize('NFC').slice(0, 20000) : '';
  return { id, book, field: e.field, sense, value, old, status };
}
