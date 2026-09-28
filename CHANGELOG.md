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

## v0.19.0 — 28 Sep 2026

- **Vol. 23's Meaning boxes drafted from our OCR** (brief §56): 6,906 rows in `docs/translation/meanings/23.jsonl` (206 formula,
  6,700 drafted), all `drafted`, `source: ocr`, the first book drafted from the scanned pages' OCR; 15 shards (shard 00 is §55's
  trial). 2,033 rows flagged (`23-flags.tsv`), 3,873 lines of what the drafts left out (`23-omitted.tsv`), 595 terms kept in Pāḷi
  (`23-terms.tsv`). About and README list vol. 23. Meaning rows in all: **170,351, 77.0% of the index, none reviewed**.
- NEXT-SESSION 1c: the review questions of the OCR drafts, for the final revision.

## v0.18.5 — 28 Sep 2026

- `tools/abhidhana_meanings.py prep`, books drafted from our OCR (`source: ocr`: 14/3, 20–25, 4/3): where a damaged analysis
  bracket's part up to the first `]` holds Burmese gloss words, only the analysis formulas in it (Pāḷi elements joined by +)
  are left out and the `]` becomes ။; before, the whole part went, and with it the gloss where the `]` was scan noise or a
  later bracket (vol. 23: 64 rows' text changed, vol. 22: 241). 14/2 and the PCED books unchanged (byte-identical `prep`
  output). No published data changed.
- **The OCR pilot** (brief §55): vols. 23 and 22 prepared from our OCR; vol. 23 shard 00 (451 rows) drafted as a trial, not
  merged (`docs/translation/trial/23-shard00-{in,out}.jsonl`, the prompt as given in `23-shard00-prompt.md`): 137 flagged,
  270 with `omitted`, 10 empty. Meaning rows in all unchanged: 163,445, none reviewed.
- NEXT-SESSION: 00o done (0.18.3 checked live), v0.18.4 noted (00p).

## v0.18.4 — 28 Sep 2026

- **Vol. 4/3: article step re-run** (`abhidhana_articles.py 4c`, `abhidhana_romanise.py 4c`) with the three analyses corrected
  in editor mode and exported in v0.18.2 (176136 omakapatta, 176140 omakasatta, 176144 omakkhi): each now carries the corrected
  analysis and is marked `corrected`. No other data changed by intent.

## v0.18.3 — 28 Sep 2026

- **Vol. 14/2: 497 Meaning rows redrafted** (brief §54): the rows whose Burmese now begins with the body's restored first
  words (brief §50, `docs/translation/meanings/14b-redraft.tsv`), drafted again in two shards and merged over the old rows;
  all still `drafted`. No other row changed. Flags 1,406 → 1,128 (the old ones mostly noted the lost first word), omitted
  lines 1,165 → 1,172, terms 571 → 572. Meaning rows in all: 163,445, none reviewed.
- `tools/abhidhana_meanings.py`: `prep` / `merge` take `--ids FILE` (draft and merge only those ids over the existing rows),
  `--shards N` and `--work DIR`.
- Brief §53 corrected: the weekly export workflow was added in v0.18.1 and its first run opened PR #33 (v0.18.2).

## v0.18.2 — 2026-09-28

- **Edits from editor mode exported** (weekly workflow): 0 Meaning row(s), 3 correction(s) to `docs/corrections.tsv`, 0 line(s) to `corrections-es.tsv`. Books and fields: 4c: analysis. Article step still to re-run on the Mac for: 4c.

## v0.18.1 — 28 Sep 2026

- **Weekly export of the editor's edits** (`.github/workflows/export-edits.yml`, `docs/editor-mode.md` §5): every Monday
  at 10:00 UTC (04:00 in Mexico City), and on demand from the Actions tab, GitHub reads `/api/edits?book=all`, runs
  `tools/abhidhana_edits_export.py --api --write --summary`, and if any file changed bumps the patch, adds a CHANGELOG
  section and opens a pull request on `edits/YYYY-MM-DD` listing the books whose article step must be re-run on the Mac.
  No change, no PR. Written in a Cowork chat (the cloud session's permission check had refused the file); its version
  and changelog step tested on a scratch copy, the export itself not yet run on GitHub. No data changed.

## v0.18.0 — 28 Sep 2026

- **Roman input in the editor's form** (brief §53, `docs/editor-mode.md` §3): the headword, label and analysis each have a
  switch *Birmano / Latín*; in *Latín* they are typed in IAST and converted to Burmese script by `ROMAN.burmese`
  (`site/src/assets/roman.js`, a port of Aksharamukha's IAST → Burmese; it agrees with Aksharamukha on 256,123 of 256,203
  distinct words, the 80 others being ဂြ + ā, written short as the dictionary prints it). The form shows, for each of the
  three fields, the Burmese to be stored and its roman read-back; a save needs the read-back to equal what was typed. The
  Burmese is stored, as before. The mode is remembered per field in the browser.
- **Round trip measured** (`site/test/roman/roundtrip.js`): headwords 220,623 of 221,154 (99.76%), PCED analyses without
  a derivation 139,759 of 140,281 (99.63%); the failures are malformed OCR, Burmese prose, stray characters and the tall ā.
  Browser tests `ui-test.js` 48/48 (20 new), `api-test.js` 28/28.
- `tools/abhidhana_edits_export.py`: `--summary FILE` (what changed, as JSON) and a User-Agent on `--api`. No data changed.

## v0.17.0 — 27 Sep 2026

- **Editor mode** (brief §52, `docs/editor-mode.md`): in Browse, when the editor is signed in, each article has an
  **Editar** button with a form for the Meaning (ES/EN, the status of the Spanish, whole or by sense) and the article's
  fields (headword, label, analysis, body, in Burmese, with a live roman preview). Saves go to a Cloudflare D1 database
  through Pages Functions (`functions/`); `/edit/` and `/api/admin/` are for Cloudflare Access, and the write API checks
  the Access token itself. Every edit is kept; the latest per id + field + sense counts.
- **Every visitor's Browse lays the saved edits over the published data** (`/api/edits?book=NN`), marked *corregido* /
  *revisado* (or *en parte*, by sense), with the date; if the API fails, the page shows the published data.
- `tools/abhidhana_edits_export.py` writes the edits into `docs/translation/meanings/NN.jsonl`, `corrections-es.tsv` and
  `docs/corrections.tsv`, and lists the books whose article step must be re-run on the Mac.
- The build now writes a "véase" link to a word that is not a headword as `[[x|]]` (still shown in italics), so the form
  can give back the source text. No data changed. **Not yet switched on**: the dashboard steps of `docs/editor-mode.md` §2.

## v0.16.0 — 27 Sep 2026

- **The editor's decisions of 27 Sep recorded** for new drafts (brief §51): person by the Pāḷi ending; ပယ်, ဖောက်ပြန် by sense;
  -attha *el beneficio de X*; ပရိသတ် *asamblea*; ငရဲ *infierno*; pariveṇa, parikamma, parikkhāra, maṅgala translated; one
  rendering for stacked futures; marica *pimienta negra*; လေ as element *aire* (`stems.tsv`, `glossary.tsv`, `drafting-prompt.md`).
- **Nine Meaning rows corrected** by the editor (`docs/translation/corrections-es.tsv`); three corrected in part, shown on the
  site as *corregido en parte* with the corrected sense named.
- **No re-rendering**: the rows whose draft conflicts with a rule (3,382) are listed for the final revision in
  `docs/translation/revision-queue.tsv`.
- **Vol. 4/3**: ဩ restored at the start of 393 OCR analyses read as သ or သဩ (`analysis_o_restored`); two hand corrections
  (176133, 176134).

## v0.15.0 — 27 Sep 2026

- **The body's first words restored** (brief §50): words printed on the headword's line after the analysis's ] were
  dropped as debris by the article step's noise filter. **6,003 bodies** in 29 books gained them; in books 01–19 only
  where the PCED definition begins with them (4,577 kept, 289 taken out), elsewhere by their shape (1,426; 497 in 14/2).
  No placement, label or analysis changed in any row. Rows gain `body_head_restored` and `body_head_how`. Romanisation
  re-run for all books. Vol. 14/2's 497 affected Meaning rows are listed for a redraft
  (`docs/translation/meanings/14b-redraft.tsv`); their drafts are unchanged for now.

## v0.14.0 — 27 Sep 2026

- **Vol. 14/2 Meaning boxes drafted** from the PDF's own text layer (no PCED): 6,795 rows, all `drafted`, `source` text
  layer; 1,406 flagged (`docs/translation/meanings/14b-flags.tsv`), what the drafts left out in `14b-omitted.tsv`. Drafted so
  far: 163,445 rows in 21 books (73.9% of the index), none reviewed. About and README updated.
- `prep` (books without a join) also strips citations without numbers and dash-joined lists of inflected forms (681 of
  14/2's rows changed); drafts record omissions in a field `omitted`, which `merge` keeps out of the rows. Shard 00, the
  trial, kept as drafted. Brief §49.

## v0.13.1 — 27 Sep 2026

- **`abhidhana_meanings.py prep` for books without a witness join** (14/2, 14/3, 20–25, 4/3): the Burmese comes from our
  text (`articles.jsonl` body), `source` *text layer* for 14/2, *ocr* otherwise; line-end hyphens kept outside Pāḷi and
  dropped inside it; multi-word Pāḷi quotations, citations and reference lists removed; one-word Pāḷi kept. Books with a
  join unchanged (`prep 15` byte-identical on a synthetic witness; to be confirmed on the Mac). Vol. 14/2: 6,804
  explanations in 15 shards. The drafting prompt has a section for books drafted from our own text.
- **Trial shard 00 of vol. 14/2 drafted** (454 rows, 181 flagged), kept apart in `docs/translation/trial/`, not merged.
- **No published data changed**: `meanings/` and the site are as in v0.13.0. Brief §49.

## v0.13.0 — 27 Sep 2026

- **Vols. 15, 16, 17, 18 and 19 Meaning boxes drafted** from PCED: 9,340 + 10,393 + 6,510 + 7,826 + 9,250 rows, all
  `drafted`; 8,695 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 156,650 rows in 20 books (70.8% of
  the index), none reviewed. PCED's vols. 1–19 are now all drafted. About and README updated.
- The drafting prompt is now kept in the repo, `docs/translation/drafting-prompt.md`. Brief §48.

## v0.12.0 — 26 Sep 2026, later still

- **Vols. 10, 11, 12, 13 and 14/1 Meaning boxes drafted** from PCED: 7,353 + 5,662 + 7,020 + 7,279 + 5,219 rows, all
  `drafted`; 3,889 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 113,331 rows in 15 books (51.2% of
  the index), none reviewed. About and README updated. Brief §47.

## v0.11.0 — 26 Sep 2026, later still

- **Vols. 7, 8 and 9 Meaning boxes drafted** from PCED: 6,877 + 6,448 + 6,805 rows (every article with a definition),
  all `drafted`; 683 + 636 + 798 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 80,798 rows in
  vols. 1–3, 4/1, 4/2 and 5–9, none reviewed. About and README updated.
- Stems L105 (ဂုဏ် *cualidad / virtud*) and L106 (လူ in the gihi- compounds, *laico*), the editor's. Brief §46.

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
