# Claude Project setup — "Tipiṭaka Pāḷi Myanmā Abhidhāna"

*The exact text of the project's Description and Instructions fields, kept here so a session
can check that the fields still match what the project actually does. If they diverge,
this file is the record of what was agreed; fix the fields, not this file, unless the change
was deliberate. Revised 24 September 2026: licence decided, repository public, OCR placement
measured. Paste the Instructions below into the project's field.*

## Description

Tipiṭaka Pāḷi-Myanmā Abhidhāna — the 25-volume Pāḷi-Burmese dictionary of the Myanmar
Ministry of Religious Affairs, compiled by the Masoeyein Board of Scholar-Elders —
digitised from scans, its Pāḷi headwords romanised, its Burmese definitions rendered into
Spanish. 29 PDFs, 25,700 pages, 215,447 headwords, anchored to the app's own index and to
the Chaṭṭha Saṅgāyana Tipiṭaka. Public repository: github.com/bthar-mx/tipitaka-abhidhana.

## Instructions

This project digitises the Tipiṭaka Pāḷi-Myanmā Abhidhāna: a Pāḷi → Burmese dictionary in
25 volumes, bound as 29 books. The goal is the dictionary as data — romanised Pāḷi
headwords, structured articles, and Burmese definitions rendered into Spanish.

Read `abhidhana-project-brief.md` before advising, then `NEXT-SESSION.md`. The brief records
what is on disk, what has been measured, and what is blocked. Do not re-derive figures it
carries; if a new one is needed, measure it rather than estimating.

The material is at `~/Documents/abhidhana` — also the git working copy of the public repo
`bthar-mx/tipitaka-abhidhana` — and must be connected each session; the OCR models are at
`~/Tipitaka/nissaya/tessdata`.

Method:
- **The app's index is ground truth.** `db/tipitaka_abidan.db` holds 221,154
  (headword, book, page) rows, and `words.page_number + books.start_page` is the PDF page.
  For every page the correct headwords are known, in correct spelling, before OCR runs. Score
  OCR as RECALL against that list, per page, and report it. This is not the nissaya's
  attestation rate and should not be called one.
- **The page is two columns and OCR interleaves them.** Cut at the gutter first, and report
  the share of headwords appearing in the order the dictionary prints them, not recall alone.
- **Render at each book's native resolution** — check `pdfimages -list` first; upsampling a
  1-bit scan lowers recall.
- **The Pāḷi side is self-validating, but more weakly than in a nissaya.** A romanised
  headword can be checked against OSBCT; about two thirds are attested whole or inside a
  canonical word. Say so; do not promise the nissaya's standard of proof.
- **The Burmese side has no anchor.** Nothing validates a definition or its translation but
  Angel. Carry a status — ocr / drafted / reviewed / corrected — on every row, and never
  present a drafted rendering as a reading.

Spanish is translated **from the Burmese, never relayed through English**, and **by stem,
not by row**: the definition language is formulaic, and a few hundred agreed formula-stems
carry the bulk of the corpus. The hyphens inside a definition are **alternative renderings
of one Pāḷi element** — the same device as the nissaya's `, ဝါ-` — and merging them into one
Spanish phrase drops a reading. Pāḷi gender belongs to the Pāḷi word and is not carried onto
the Spanish noun. See `docs/spanish-method.md`.

Terminology is fixed by IEBH's glossary, not decided per session. Once a Pāḷi term has an
agreed English and Spanish rendering, use it without variation. Propose additions; do not
improvise.

Publication is decided: the work is public. Credit the compilers, the Ministry, and every
person and library named in `docs/app-info.html`; code is MIT, the project's additions are
CC BY-SA 4.0, and the dictionary text itself is not relicensed.

Run OCR in the session's cloud container (about 10 pages a minute) or natively in Terminal on
a Mac — never in the Cowork desktop VM, where tesseract is about 7× slower. Helpers follow
`RUNBOOK.md` and claim a volume through its GitHub issue.

Flag uncertainty rather than guessing, and be ready to cite sources. Converse in English
even when the work itself is Spanish.
