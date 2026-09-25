# Vol. 4a (အာ – ဥတြာသေယျုံ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 4a
--columns --dpi 96 --passes page.psm6 --workers 10`, run natively on Angel's Mac. Figures measured
from `ocr/4a/pages/` with `--score`.*

Book 4a is vol. 4, part 1. 863 PDF pages: 42 of front matter, 791 carrying index entries, 27 inside
the body that the index does not cover (a long article fills them), and 3 of back matter
(pp. 861–863). **7,524 index headwords.** Index `start_page` 42.

## Settings

- **96 dpi, native.** Every page image is 96 ppi (`pdfimages -list`); 855 of 863 are
  2152–2154 × 3120–3172 px.
- Column cut + one whole-page psm 6 pass. A gutter was found on every indexed page.

## Result

| | vol. 4a | vol. 3 | vol. 2 | vol. 1 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **6,687 / 7,524 = 88.9%** | 92.9% | 92.7% | 92.0% |
| column pass alone | 84.8% | 88.5% | 87.7% | 88.5% |
| whole-page pass alone | 69.6% | 73.1% | 75.5% | 72.0% |
| **in printed order, column pass** | **73.1%** | 77.3% | 75.5% | 76.1% |
| in printed order, whole-page pass | 43.0% | 42.9% | 46.9% | 42.3% |
| pages where every headword came out | 399 of 791 = 50.4% | 56.1% | 61.8% | 53.5% |
| pages at or above 90% | 64.9% | 74.9% | 74.7% | 72.0% |
| pages at or above 80% | 82.0% | 92.0% | 91.3% | 90.0% |
| pages below 50% | 9 | 6 | 5 | 7 |

The median missed headword is 12 characters, against 10 for the volume.

**By part of the book**: PDF pp. 1–699, 91.5%; pp. 700–863, 79.2% (pp. 700–799 81%, 800–863 75%).
The last part is a scan of worn print, with broken and faint strokes (checked on p. 786). A second
copy of vol. 4/1 is in `pdfs-drive/`; it was not compared.

**Worst pages**: p. 478 (2 of 15), p. 847 (2/12), p. 786 (4/13), p. 523 (4/11), p. 47 (5/13),
p. 524 (7/18). Each was tested against its neighbours' index lists, and none is out of order.
P. 478's cause is one glyph: the stacked ဆ of ဉ္ဆ, read as ဉ္စ or ဉ္ဇ. Pp. 478 and 786 were
examined against the images: see `articles-report.md`.
