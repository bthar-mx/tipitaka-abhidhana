# Vol. 6 (ကိလေသ – ငကာရ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 06
--columns --dpi 75 --passes page.psm6 …`, run natively on the editor's Mac (the dpi and passes are those
recorded in the page records; the worker count is not recorded). Figures measured from
`ocr/06/pages/` with `--score`.*

1,039 PDF pages: 22 of front matter, 960 carrying index entries, 55 inside the body that the index
does not cover, and 2 of back matter (pp. 1038–1039). **11,429 index headwords**, 11,232 distinct.
Index `start_page` 22. The pages were written between 12:41 and 13:06 UTC, about 41 a minute
(while other work ran in the Cowork VM on the same Mac).

## Settings

- **75 dpi.** Every page image is 74–77 ppi (`pdfimages -list`), as NEXT-SESSION expected; vol. 3
  was rendered at 75 for the same reason.
- Column cut + one whole-page psm 6 pass. The gutter was found inside 0.44–0.555 of the width on
  every indexed page but p. 762 (0.557), where the white-channel fallback applies.

## Result

| | vol. 6 | vol. 5 | vol. 4/2 | vol. 3 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **10,560 / 11,429 = 92.4%** | 90.2% | 93.3% | 92.9% |
| … with the spelling folds (`tools/abhidhana_fold.py`) | 93.1% | 91.4% | 94.0% | 93.5% |
| column pass alone | 87.4% | 84.9% | 91.1% | 88.5% |
| whole-page pass alone | 76.5% | 71.3% | 86.0% | 73.1% |
| **in printed order, column pass** | **75.3%** | 74.6% | 76.0% | 77.3% |
| in printed order, whole-page pass | 44.5% | 43.4% | 50.1% | 42.9% |
| pages where every headword came out | 464 of 960 = 48.3% | 46.8% | 60.1% | 56.1% |
| pages at or above 90% | 72.7% | 67.6% | 79.2% | 74.9% |
| pages at or above 80% | 92.3% | 85.7% | 93.3% | 92.0% |
| pages below 50% | 4 | 9 | 6 | 6 |

The folded figures for vols. 3–5 were measured the same way, over their page records, on 25 Sep.

By hundred pages: 93, 89, 92, 94, 92, 93, 93, 93, 93, 92, 91%. The median missed headword is 11
characters.

**Worst pages**: p. 140 (1 of 3), p. 110 (4/10), p. 744 (5/11), p. 1011 (7/15), p. 139 (4/8), p. 154
(4/8), p. 718 (2/4), p. 312 (1/2). Each was tested against its neighbours' index lists (with the
folds): on every one its own list scores best, so no page is bound out of order. P. 110 is ါ/ာ and
ဋ read ဌ/ဠ; see `articles-report.md`.

**P. 851 scores 20 of 34 because the index files 14 of its headwords a page early**: they are
printed on p. 852, which the index gives no headwords. The recall figures above count them as
missed on p. 851; `abhidhana_articles.py` reads them on p. 852 (`ID_PAGE_FIX`).
