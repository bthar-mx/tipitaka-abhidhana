# Changelog

Versions of the Tipiṭaka Pāḷi-Myanmā Abhidhāna project: the data, the tools and the site together.
*Scheme proposed 26 September 2026; the editor created the tags v0.1.0–v0.7.0 the same day.*

## The scheme

`vMAJOR.MINOR.PATCH`, one number for the whole repository, recorded in three places: the file
`VERSION`, an annotated git tag on the commit, and a section of this file.

- **0.x** while nothing in the dictionary has been reviewed by a reader of Burmese. Every row is
  `ocr` or `drafted`.
- **MINOR** for a milestone a user of the data or the site would notice: a new layer of data (a
  volume's Meaning boxes, the PCED analyses), a re-run that changes figures across books, a new
  site section.
- **PATCH** for fixes that change no published figure: typos, a page's layout, the docs.
- **1.0.0** when the text layer is complete *and* reviewed work is published: proposed as the
  first volume whose Meaning boxes the editor has reviewed (status `reviewed` or `corrected`), with the
  licence question settled (brief §10). Until then, a 0.x number says "drafts".
- The source release `sources-v1` (PDFs and index) keeps its own name: it versions the inputs,
  not the project.

A release note says, per version: what changed, the brief's sections, and the headline figures
(located, label + body, Meaning rows drafted / reviewed).

## v0.10.0 — 26 Sep 2026, later still

- **Vol. 6 Meaning boxes drafted** from PCED: 11,424 rows (every article with a definition but one), all
  `drafted`; 1,154 flagged (`docs/translation/meanings/06-flags.tsv`), 397 terms kept in Pāḷi
  (`06-terms.tsv`). About and README list vols. 1–3, 4/1, 4/2, 5 and 6 as drafted.
- The live site checked after v0.9.0 (printed page numbers, the analysis and its derivation). Brief §45.

## v0.9.0 — 26 Sep 2026, later

- **Vol. 5 Meaning boxes drafted** from PCED: 8,012 rows (every article with a definition but one), all
  `drafted`; 1,275 flagged (`docs/translation/meanings/05-flags.tsv`). Vol. 4/3 deferred (no PCED text).
  Glossary: ကုသိုလ် as merit → *mérito / meritorio*; stems L101–L104 (နတ်, ရဟန်း, ပယ်, ဥတု). Brief §44.
- **The compound analysis split from its derivation** (`tools/abhidhana_romanise.py`): the romanised line
  gives the analyses and, where it is wholly Pāḷi, the derivation (ulūka); a derivation in Burmese stays
  on the Burmese line, shown below it (katvā: [kara + tvā]). 19,871 rows' `analysis_iast` changed, no
  other field.
- **Printed page numbers**: Browse, the page pane, the search list and the page view show the book's
  own page beside the PDF page (`site/volumes.json` `offset`, with vol. 2's and vol. 22's exceptions).
- Labels: (ကြိ၊ဝိ) Spanish without *-tuṁ*. Personal names removed from the repository's docs and data
  (`IEBH` in data columns). Dates of v0.7.0–v0.8.0 and brief §42–43 corrected from 27 to 26 Sep.

## v0.8.0 — 26 Sep 2026

- **Vols. 4/1 and 4/2 Meaning boxes drafted** from PCED: 7,519 and 6,654 rows, all `drafted`; 409 and 872
  flagged. `prep` links more "see X" forms; a `report` step writes the flags and terms lists. Brief §43.
- Site: the IEBH footer with logo, related sites, licences and the version on every page; a back-to-top
  button; "Análisis" without the PCED chip; PCED described as a typed witness on About; citation tooltips
  (work · volume, page); "see X" in the Burmese definition linked; mode bar wording.
- Labels: *sustantivo* → *nombre*; (ကြိ၊ဝိ), (နာမ-ကြိ), (စတုတ္ထန္တ), (တတိယန္တ-ဗျ) corrected and confirmed (the editor).

## v0.7.0 — 26 Sep 2026

- **Vol. 3 Meaning boxes drafted** from PCED: 11,726 rows (372 by formula, 11,354 drafted in 24
  shards), all `drafted`; 1,076 flagged (`docs/translation/meanings/03-flags.tsv`). Brief §42.
- This changelog and `VERSION`.

## v0.6.0 — 26 Sep 2026, night (`5db316f`)

PCED's compound analyses for books 01–19 (155,072 rows); hand corrections (`docs/corrections.tsv`);
kusala = *sano*, akusala = *insano*; Browse fixes (search list, Hide index, romanised printed labels);
`/assets/` links versioned by content hash; **vol. 2 Meaning boxes drafted** (7,189 rows). Brief §40–41.
Commits `cef941c` … `5db316f`.

## v0.5.0 — 26 Sep 2026, early morning (`b7881c4`)

Site redesign: Browse is the home page, `/volumes/`, `/abbreviations/`; **vol. 1 Meaning boxes
drafted** (8,144 rows). Brief §38–39.

## v0.4.0 — 25 Sep 2026, night (`571f566`)

Page images live (25,700 pages in R2), light/dark switch, Introduction page, compound analysis with a
lost `[` (+4,907), citations keep their whole abbreviation, translation batch 1 for review.
Brief §31–37.

## v0.3.0 — 25 Sep 2026, evening (`493b459`)

**All 29 books** digitised: 221,154 index rows, 94.1% located, 88.1% label + body; the public website
and one label table. Brief §28–30.

## v0.2.0 — 25 Sep 2026 (`e2e32b5`)

27 books (the batch of vols. 10–24), the index's page errors applied, the Reader in binary.
Brief §13–27.

## v0.1.0 — 24–25 Sep 2026 (`9d5203d`)

Vol. 1 digitised end to end; tools, runbook, docs; the repository made public. Brief §1–12.
