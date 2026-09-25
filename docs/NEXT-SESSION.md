# Abhidhāna — handover, 25 September 2026 (evening)

*Vols. 1–3 and 4/1 are digitised end to end, spot-checked and in the Reader. Read `abhidhana-project-brief.md` first: §12 covers vol. 1
and §13 vols. 2–3, and every figure is there. `docs/labels.md` holds the label map and the typed
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

| | vol. 1 | vol. 2 | vol. 3 | vol. 4/1 (4a) | vol. 4/2 (4b) |
|---|---|---|---|---|---|
| OCR, articles, romanisation | done | done | done | done 25 Sep | OCR running (Angel, 25 Sep) |
| reports | done | done | done | done 25 Sep | — |
| image spot check | done | done | done | done 25 Sep (pp. 300, 478, 786) | — |
| in the Reader | yes | yes | yes | yes, 25 Sep | — |
| page records in the release | uploaded | uploaded | uploaded | `release/ocr-4a-pages.tar.gz`, to upload | — |
| GitHub issue | closed | closed | closed | close after this commit | open |

Done on 25 Sep (brief §14): vol. 3 spot check; the Reader with a volume switch and search across
all volumes; the typed witness converted and checked (`docs/witness.md`); short headwords and
homonym superscripts placed in the articles (vols. 1–3 and 4a regenerated); vol. 4/1 checked.
`abhidhana_articles.py` now keeps the hand-written notes in `articles-report.md`.

## Next, in order

1. **Vol. 4/2 (4b)** when Angel's OCR run finishes: `abhidhana_articles.py 4b`, then
   `abhidhana_romanise.py 4b`; write `ocr/4b/ocr-report.md` (run `abhidhana_ocr.py 4b --score`; test
   pages below 50% against their neighbours' lists); a 3-page spot check, written into
   `articles-report.md` under the generated tables; `abhidhana_reader_data.py 4b` and a `VOLS` entry
   in `reader/index.html` (id `4b`, n `4/2`, ranges from `books.name_info`); republish (read the
   artifact and every published file first); `tar czf release/ocr-4b-pages.tar.gz -C ocr/4b pages`.
   `pdfs-drive/`'s pagination differs from the app's in 4b; don't use it without checking.
2. **Join the witness to the articles** (`docs/witness.md` §6): per article, by headword and
   homonym order; flag label and analysis disagreements; report agreement per volume. Its text is
   not published until its licence is known (it is not stated anywhere found).
3. **Fold ါ/ာ after a stacked consonant** when matching headwords (`abhidhana_ocr.py` scoring and
   `abhidhana_articles.py`): it would recover 1, 6 and 26 missed headwords in vols. 1–3. Also
   ဉ္ဆ/ဉ္စ in 4a (27 missed). Don't edit `abhidhana_ocr.py` while an OCR run is going.
4. **Angel's review of the new labels**: `docs/labels.md` §1 and §6. There is a Pāḷi expansion and a
   Spanish abbreviation for each (ကြိ၊ဝိ, ဗျ, ကာ၊ကြိ, ကမ္မ၊ကြိ, …).
5. **Re-run vol. 25** with `--columns` at its native resolution.
6. **Next volumes**: 4c, then 05 onwards, on the Mac natively or on Winston's.
   Per volume: reports, a 3-page spot check, the Reader, then close the issue.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **The `page.psm6` fallback** for headwords the column pass lost is still not tried (5.4–6.5% of
  articles remain unlocated).
- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is
  explained; the vol. 2 page swap is a hint of what such problems look like.
- **Title-page entry counts vs the index** (vol. 4/3: 5,163 vs 5,230). Explain per volume.
- ~~The witness's coverage.~~ Answered: books 01–19 with 4a, 4b; not 4c, 14b, 14c, 20–25 (`docs/witness.md` §3).
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
