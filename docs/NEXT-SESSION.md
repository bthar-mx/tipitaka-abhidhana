# Abhidhāna — handover, 25 September 2026 (after vol. 5)

*Vols. 1–5 (vol. 4 in three parts) are digitised end to end, spot-checked and in the Reader. Read `abhidhana-project-brief.md` first: §12 covers vol. 1
§13 vols. 2–3, §14–17 the witness and vols. 4/1–5; every figure is there. `docs/labels.md` holds the label map and the typed
witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. Angel runs
  git and `gh` in Terminal; the session has no GitHub credentials.
- **Run OCR natively on the Mac** (about 45 pages a minute with `--workers 10`). Check the dpi per
  book with `pdfimages -list`. After the OCR, run `abhidhana_articles.py NN` and then
  `abhidhana_romanise.py NN`, always in that order.

## State

| | vols. 1–4/3 | vol. 5 | vol. 6 |
|---|---|---|---|
| OCR, articles, romanisation | done | done 25 Sep | OCR next (Angel) |
| reports, spot check, Reader | done | done 25 Sep | — |
| page records in the release | uploaded or to upload (`--clobber` is safe) | `release/ocr-05-pages.tar.gz`, to upload | — |
| GitHub issue | close any still open | close after this commit | open |

Done on 25 Sep (brief §14–17): vols. 4/1, 4/2, 4/3 and 5; the Reader with all seven books and
search across them; the typed witness; homonym and one-letter headwords; labels with a lost
bracket. **4c's PDF carries supplements to vols. 15, 4/2 and 16** (brief §16).

## Next, in order

1. **Vol. 6** (book 06, ကိလေသ – ငကာရ, 1,039 PDF pages, images 74–77 ppi: render at 75, as vol. 3
   was): OCR natively; then as for vol. 5.
2. **Join the witness to the articles** (`docs/witness.md` §6): per article, by headword and
   homonym order; flag label and analysis disagreements; report agreement per volume. Its text is
   not published until its licence is known (it is not stated anywhere found).
3. **Fold ါ/ာ after a stacked consonant, ဉာ/ညာ, and the stacked-letter confusions (ဉ္ဇ/ဉ္စ, ဏ္ဌ/ဏ္ဍ/ဏ္ဏ, ဋ/ဌ/ဠ, ဉ္ဆ/ဉ္စ),** when matching headwords (`abhidhana_ocr.py` scoring and
   `abhidhana_articles.py`): it would recover 1, 6 and 26 missed headwords in vols. 1–3. Also
   ဉ္ဆ/ဉ္စ in 4a (27 missed). ဉာ/ညာ: 6 of 4b's 9 misses of ဉာ-headwords. Don't edit `abhidhana_ocr.py` while an OCR run is going.
4. **Angel's review of the new labels**: `docs/labels.md` §1 and §6. There is a Pāḷi expansion and a
   Spanish abbreviation for each (ကြိ၊ဝိ, ဗျ, ကာ၊ကြိ, ကမ္မ၊ကြိ, …).
5. **Re-run vol. 25** with `--columns` at its native resolution.
6. **Next volumes**: 07 onwards, on the Mac natively or on Winston's. **Vol. 15** must be joined with
   4c's supplement to it (53 ဘိဇ္ဇ headwords indexed only there).
   Per volume: reports, a 3-page spot check, the Reader, then close the issue.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **The `page.psm6` fallback** for headwords the column pass lost is still not tried (5.4–6.5% of
  articles remain unlocated).
- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is
  explained; the vol. 2 page swap is a hint of what such problems look like.
- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **An index-errata list**: the errors found (brief §15–16) should be collected in
  `docs/index-errata.md` with the printed form, rather than corrected silently.
- ~~The witness's coverage.~~ Answered: books 01–19 with 4a, 4b; not 4c, 14b, 14c, 20–25 (`docs/witness.md` §3).
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
