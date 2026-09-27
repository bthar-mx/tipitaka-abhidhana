-- The editor's edits (docs/editor-mode.md). Apply once:
--   npx wrangler d1 execute abhidhana-edits --remote --file site/d1/schema.sql
-- Every edit is a new row; nothing is updated or deleted. The site shows the latest row (highest rowid)
-- per id + field + sense; a row with status 'reverted' withdraws the edit (the published data shows again).
CREATE TABLE IF NOT EXISTS edits (
  id     INTEGER NOT NULL,             -- the article (index row) id
  book   TEXT    NOT NULL,             -- its book: 01 … 25, 4a, 4b, 4c, 14b, 14c
  field  TEXT    NOT NULL,             -- es | en | status | analysis | label | body | headword
  sense  TEXT    NOT NULL DEFAULT '',  -- status only: '' the whole Meaning, or the senses, '1' or '1,3'
  value  TEXT    NOT NULL DEFAULT '',  -- the new text (Burmese for the article's fields); for status:
                                       -- reviewed | corrected | drafted; '' when reverted
  old    TEXT    NOT NULL DEFAULT '',  -- what the page showed before this edit
  status TEXT    NOT NULL DEFAULT 'saved',   -- saved | reverted
  date   TEXT    NOT NULL              -- UTC, ISO 8601 with milliseconds, set by the server
);
CREATE INDEX IF NOT EXISTS edits_book ON edits (book, id, field, sense);
