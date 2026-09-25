# Abhidhāna — handover, 25 September 2026, evening (after vols. 23, 24, 14/2)

*27 books — vols. 1–20 and 22–24, vol. 4 in three parts and 14 in three — are digitised end to end, spot-checked and in the Reader: 208,979 index rows, 94.0% located, 88.0% with label + body. Books 21 and 25 remain; both are ready to OCR. Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool, §25 vol. 14/2's text layer, §26 the batch (vols. 10–22), §27 vols. 23, 24, 14/2, the index's page errors, book 21 and the Reader in binary. Every figure is there. `docs/labels.md` holds the label map, `docs/index-errata.md` the index's errors, `docs/witness.md` and
`docs/witness-join.md` the typed witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. Angel runs
  git and `gh` in Terminal; the session has no GitHub credentials.
- **Run OCR natively on the Mac** (about 45 pages a minute with `--workers 10`; ~41 while the Cowork
  VM was busy on the same Mac). Check the dpi per book with `pdfimages -list`. After the OCR, run
  `abhidhana_articles.py NN` and then `abhidhana_romanise.py NN`, always in that order; then
  `abhidhana_reader_data.py NN` and `abhidhana_witness_join.py` with every witnessed book.
- **In the Cowork VM, a background job dies when the call returns**, and `pkill -f` with a pattern
  that appears in the command line kills the calling shell. Run the article step for up to five
  books in parallel inside one call (about 45–65 s for five).
- **The Reader's data are `reader/*.wasm`** (gzip bytes, served as application/wasm), not `.json`
  or the old `.gz.txt`: republish those with `reader/index.html`. `reader/*.wasm` is not yet in
  `.gitignore` (Angel's file): don't commit them.
- **Pipeline order per book**: `abhidhana_articles.py NN`, `abhidhana_romanise.py NN`, then
  `abhidhana_reader_data.py NN [NN ...]` (it now takes several books) and the witness joins.
  In a fresh Cowork VM, `pip install --user aksharamukha python-myanmar pymupdf` first.

## State

| | 27 books (1–20, 22–24 with 4/1–4/3, 14/1–14/3) | 21 | 25 |
|---|---|---|---|
| OCR / text, articles, romanisation | done (14/2 from its text layer) | ready: index explained (brief §27) | ready: pilot moved aside |
| reports, spot check, Reader | done | — | — |
| page records in `sources-v1` | to upload: 10–20, 14c, 22, 23, 24 (`release/ocr-NN-pages.tar.gz`) | — | — |
| GitHub issues | close 10–20, 14c, 22, 23, 24, 14b | open | open |

`tmp/_to_delete/` holds nine `*.json.gz` files from a first try at the Reader's data; delete it by
hand (`tmp/` is gitignored). `tmp/ocr-25-pilot-pages/` is the old vol. 25 pilot; keep or delete.

## Next, in order

0. **OCR books 21 and 25**, natively: `caffeinate -i tools/run_volumes.sh 21 25` (21 at ~72 dpi,
   25 at 300; the script now runs both). Then reports (the OCR report's figures:
   `python3 tools/abhidhana_ocr_stats.py 21 25`; model the text on `ocr/23/ocr-report.md`), a 3-page
   spot check, the Reader, and close the issues. Vol. 25's new figures replace the
   pilot's (brief §5), which were whole-page at 200 dpi.
1. **The public website** (Angel, 25 Sep evening): Cloudflare Pages from `site/` in the repo, page
   images in R2. Proposal first, then build; see the chat of 25 Sep evening.
2. **Weak `ID_PAGE_FIX` candidates**, on the image: 14/3 pp. 605 (198069–198070) and 976
   (201781–201786), 18 p. 815 (146728–146731), 10 p. 219 (81975–81976); and 14/3 pp. 564, 607, 620.
3. **Re-cut the gutters** with `tools/abhidhana_recut.py` (brief §24), natively, book by book, when
   no OCR is running: `python3 tools/abhidhana_recut.py NN --scan --workers 10`, then `--run
   --workers 10`. Then re-run articles, romanisation, the witness joins and the Reader for every
   book, and compare. Vol. 24 has 15 pages with a gutter ≥ 0.54 (column recall 80.8%). **Vol. 9
   p. 823** (brief §23): move `ocr/09/pages/p0823.json` aside and re-run it before that. Afterwards
   try the `page.psm6` fallback for headwords still unlocated.
4. **Why is compound analysis low in vols. 23 and 14/3** (59%) against ~72% elsewhere? Look at a
   page's [ ] in the text.
5. **Image-check the label disagreements** with the witness (`docs/witness-join.md` §3): a sample
   of (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ). And (ထိန), (ထီ၊၇), (ထိ၊န) (`docs/labels.md` §7; ids
   51227, 51941, 54340; vol. 24 has (ထီ၊ ၇) 17 and (ထိ၊ န) 11 unnormalised) before mapping them.
6. **Angel's review of the labels**: `docs/labels.md` §1, §6, §7, and now (ကာ၊ကမ္မ၊ကြိ). A Pāḷi
   expansion and a Spanish abbreviation for each.
7. **Vol. 15** must be joined with 4c's supplement to it (53 ဘိဇ္ဇ headwords indexed only there).
8. **Vol. 13's sixteen pages of vol. 15 headwords** (`docs/index-errata.md` §2): their real
   headwords can only come from our OCR; a later task.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **The witness's labels for rows we could not read** (7,002): usable privately; not published
  until its licence is known.
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
- **The Reader needs `DecompressionStream`** (Safari 16.4+, Chrome 80+, Firefox 113+). Say so if someone reports a blank page.
- **The Reader's `.wasm` data have not been opened in a browser by Claude** (brief §27). If a
  volume fails to load, check the response's Content-Type and first bytes (should be 1f 8b).
