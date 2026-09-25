# Abhidhāna — handover, 25 September 2026 (after the batch of vols. 10–22)

*Vols. 1–20 and 22 (vol. 4 in three parts, 14 in three) — all but 14/2's articles, 21, 23, 24, 25 — are digitised end to end, spot-checked and in the Reader. Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool, §25 vol. 14/2's text layer, §26 the batch (vols. 10–22). Every figure is there. `docs/labels.md` holds the label map, `docs/witness.md` and
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
  that appears in the command line kills the calling shell. Run the article step for up to four
  books in parallel inside one call (about 55 s a book).
- **The Reader's data are `reader/*.gz.txt`** (gzip, base64), not `.json`: republish those.

## State

| | vols. 1–20, 22 | vols. 23, 24 | 14/2 | 21, 25 |
|---|---|---|---|---|
| OCR, articles, romanisation | done | in the batch | text layer extracted; articles after the batch | not run |
| reports, spot check, Reader | done (10–22 on 25 Sep, one-page spot checks) | after the batch | after | — |
| page records in `sources-v1` | to upload: 10–20, 14c, 22 (`release/ocr-NN-pages.tar.gz`) | — | uploaded | — |
| GitHub issues | close 10–20, 14c, 22 after this commit | open | open | open |

`tmp/_to_delete/` holds nine `*.json.gz` files from a first try at the Reader's data; the VM
cannot delete. Delete the folder by hand (`tmp/` is gitignored).

## Next, in order

00. **After the batch** (23 and 24 still running at 13:14): reports, a spot check and the Reader for
   23 and 24. **The Reader is at 63.5 MB of 64**: before adding them, move its data out of base64
   text (e.g. gzip bytes in a served binary type, or drop the romanised citations `ci`, which can be
   made in the page), and measure. Then the page-offset corrections of brief §26: vol. 22 pp. 920–933
   one page back (a page is missing from the scan), 14/3's eight runs and the small ones in 10, 18, 22
   (`ID_PAGE_FIX`), and the vol. 13 index error (pp. 175–190) recorded in `docs/index-errata.md`.
0. **The batch run** (`tools/run_volumes.sh`, started 25 Sep by Angel): OCR, articles and
   romanisation for vol. 10's articles and vols. 11–24, one after another, about 5 hours; skips
   14b, 21 and 25; logs in `logs/`. **While it runs, don't change `abhidhana_ocr.py`,
   `abhidhana_articles.py` or `abhidhana_romanise.py`, and don't run OCR or articles steps.** When it
   says `all done`: reports, spot checks, the witness join and the Reader for vols. 10–24, commits;
   then the changes held back (below), and the articles step again for every book.
   Also then: `python3 tools/abhidhana_witness_pndaza.py join` for every book 01–19 (Pn Daza's
   typed text joined by book, page and headword; `docs/witness-pndaza.md` §8), beside the PCED join.
   Held back until then: (ကာ၊ကမ္မ၊ကြိ) in the label map (clean in 14b, 7 times; the witness 43);
   `abhidhana_articles.py 14b` and `abhidhana_romanise.py 14b` on the text-layer records already in
   `ocr/14b/pages/` (brief §25; a trial gave 98.2% located, 97.5% label + body).
1. ~~Vol. 10~~: done in the batch, reports 25 Sep (brief §26).
2. **Re-cut the gutters** with `tools/abhidhana_recut.py` (brief §24), natively, book by book, when
   no OCR is running (it competes for the CPU, not for files):
   `python3 tools/abhidhana_recut.py NN --scan --workers 10`, then `--run --workers 10`. Then
   re-run articles, romanisation, the witness join and the Reader for every book, and compare
   located and label + body before and after. **Vol. 9 p. 823** (a failed reading, brief §23):
   move `ocr/09/pages/p0823.json` aside and re-run `abhidhana_ocr.py 09 ... --first 823 --last 823`
   before that. Afterwards try the `page.psm6` fallback for headwords still unlocated.
3. **Image-check the label disagreements** with the witness (`docs/witness-join.md` §3): a sample
   of (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ). And the vol. 6 readings (ထိန), (ထီ၊၇), (ထိ၊န)
   (`docs/labels.md` §7; ids 51227, 51941, 54340), and vol. 8's (ကာ၊ကမ္မ၊ကြို) (the witness has
   (ကာ၊ကမ္မ၊ကြိ) 43 times), before mapping them.
4. **Angel's review of the labels**: `docs/labels.md` §1, §6 and now §7 (ကာ၊ကြိ၊ဝိ). A Pāḷi expansion
   and a Spanish abbreviation for each.
5. **An index-errata list**, `docs/index-errata.md`, with the printed form: the typos of brief §15–17,
   the misfiled runs of §18 (4c p. 615 → 613, 06 p. 851 → 852), ကဉ္စိက.
6. **Re-run vol. 25** with `--columns` at its native resolution.
7. **Next volumes**: 11–24 are in the batch (not 14b, 21, 25). **Vol. 15** must be joined with 4c's supplement to it (53 ဘိဇ္ဇ
   headwords indexed only there). Per volume: reports, a 3-page spot check, the Reader, the witness
   join, then close the issue.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is
  explained; the misfiled runs of brief §18 and the vol. 2 page swap show what such problems look like.
- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **The witness's labels for rows we could not read** (7,002): usable privately; not published
  until its licence is known.
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
- **The Reader needs `DecompressionStream`** (Safari 16.4+, Chrome 80+, Firefox 113+). Say so if someone reports a blank page.
