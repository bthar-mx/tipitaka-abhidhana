# Vol. 7 (စ – ဆိဒ္ဒေယျုံ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 07
--columns --dpi 72 --passes page.psm6 --workers 10 --budget 100000`, run natively on Angel's Mac.
Figures measured from `ocr/07/pages/` with `--score`.*

861 PDF pages: 60 of front matter, 714 carrying index entries, 74 inside the body that the index
does not cover, and 13 of back matter. **6,877 index headwords**, 6,702 distinct. Index
`start_page` 60. About 42 pages a minute.

## Settings

- **72 dpi.** 858 of the 861 page images are 72 ppi, 3 are 73 (`pdfimages -list`).
- Column cut + one whole-page psm 6 pass. The gutter was found inside 0.44–0.555 of the width on
  every indexed page (median 0.496, sd 0.012); see p. 527 in `articles-report.md` for a cut that
  was in range and still wrong.

## Result

| | vol. 7 | vol. 6 | vol. 5 | vol. 3 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **6,293 / 6,877 = 91.5%** | 92.4% | 90.2% | 92.9% |
| … with the spelling folds | 91.9% | 93.1% | 91.4% | 93.5% |
| column pass alone | 86.3% | 87.4% | 84.9% | 88.5% |
| whole-page pass alone | 72.3% | 76.5% | 71.3% | 73.1% |
| **in printed order, column pass** | **73.8%** | 75.3% | 74.6% | 77.3% |
| in printed order, whole-page pass | 43.9% | 44.5% | 43.4% | 42.9% |
| pages where every headword came out | 360 of 714 = 50.4% | 48.3% | 46.8% | 56.1% |
| pages at or above 90% | 69.7% | 72.7% | 67.6% | 74.9% |
| pages at or above 80% | 88.7% | 92.3% | 85.7% | 92.0% |
| pages below 50% | 3 | 4 | 9 | 6 |

By hundred pages: 90, 89, 92, 93, 91, 91, 94, 91, 94%. The median missed headword is 14 characters,
longer than in vol. 6 (11).

**Worst pages**: p. 759 (3 of 14), p. 527 (4/12), p. 508 (2/6), p. 306 (5/10), pp. 85, 142, 229, 398
(2 of 4 each). Each was tested against its neighbours' index lists (with the folds): on every one
its own list scores best, so no page is bound out of order. P. 759 is ဒွ read as ဒ္ဒ throughout;
p. 527 a gutter cut left of the channel. Both are examined in `articles-report.md`.
