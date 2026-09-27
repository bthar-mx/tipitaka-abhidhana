# Tipiṭaka Pāḷi-Myanmā Abhidhāna — notes for Claude Code

Read first, every session: `docs/abhidhana-project-brief.md` (what has been done and measured; the latest
section is the current state) and `docs/NEXT-SESSION.md` (what to do next, in order).

Rules of the project:

- Never write the editor's personal name in the repo: write "the editor" in prose, `IEBH` in data columns.
- Every push that changes data or the site: bump `VERSION` and add a section to `CHANGELOG.md`
  (scheme at the top of that file). The editor creates the git tag.
- Do not edit `.gitignore`; the editor maintains it.
- Record what you did and measured as a new numbered section of the brief, and update NEXT-SESSION.
  Do not re-derive a figure the brief already carries; measure a new one rather than estimating.
- Flag uncertainty rather than guessing. Converse in English, even when the work is Spanish.
- Every Meaning row stays `drafted` until the editor reviews it; never present a draft as a reading.
- Translation: Spanish from the Burmese, never through English. Follow `docs/translation/drafting-brief.md`,
  `docs/translation/stems.tsv` and `docs/translation/glossary.tsv` (the glossary overrides everything).
  Drafting agents get `docs/translation/drafting-prompt.md`, one agent and one scratch folder per shard.
- `abhidhana_meanings.py merge` needs `pip install aksharamukha`.
- End every session with a final message headed **Report for the Cowork chat**, in this order:
  1. Branch, commit(s) pushed, VERSION.
  2. What was done, with counts.
  3. Checks run and their results (and any check that could not be run in the cloud and must be run on the Mac).
  4. Tokens used (per agent and total), if known.
  5. Decisions taken without asking, and anything left undone.
  6. Questions for the editor, numbered.
  7. Files to review, with paths.
  Keep it under 60 lines; details go in the brief.

What is not in this repository (gitignored or release assets): `pdfs/`, `db/`, `witness/` (the PCED
typed witness and its joins), `tmp/`, the OCR models. Work that needs them (OCR, the witness joins)
is done on the editor's Mac, not in a cloud session.
