# Vol. 5 (က – ကိလေဒေတွာ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 05
--columns --dpi 72 --passes page.psm6 --workers 10 --budget 100000`, run natively on the editor's Mac.
Figures measured from `ocr/05/pages/` with `--score`.*

883 PDF pages: 54 of front matter, 756 carrying index entries, 68 inside the body that the index
does not cover (a long article fills them), and 5 of back matter (pp. 879–883). **8,015 index
headwords**, 7,899 distinct. Index `start_page` 54.

## Settings

- **72 dpi.** 800 of the 883 page images are 72 ppi, the rest 73–79 (`pdfimages -list`).
- Column cut + one whole-page psm 6 pass. A gutter was found on every indexed page.

## Result

| | vol. 5 | vol. 4/3 | vol. 4/2 | vol. 3 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **7,230 / 8,015 = 90.2%** | 90.5% | 93.3% | 92.9% |
| column pass alone | 84.9% | 88.1% | 91.1% | 88.5% |
| whole-page pass alone | 71.3% | 84.5% | 86.0% | 73.1% |
| **in printed order, column pass** | **74.6%** | 72.3% | 76.0% | 77.3% |
| in printed order, whole-page pass | 43.4% | 50.4% | 50.1% | 42.9% |
| pages where every headword came out | 354 of 756 = 46.8% | 54.8% | 60.1% | 56.1% |
| pages at or above 90% | 67.6% | 63.2% | 79.2% | 74.9% |
| pages at or above 80% | 85.7% | 85.2% | 93.3% | 92.0% |
| pages below 50% | 9 | 5 | 6 | 6 |

The median missed headword is 13 characters. By hundred pages: 82, 86, 91, 88, 92, 94, 91, 92, 91%:
the first 200 pages are the weakest.

**The misses are mostly three stacked letters read as their neighbours**, measured over the page
records by writing the confusion into each missed headword and looking for it in the page text:
ဉ္ဇ read as ဉ္စ (27 of the 47 missed headwords with ဉ္ဇ: ကဉ္ဇိက… p. 106), ဏ္ဌ read as ဏ္ဍ or ဏ္ဏ
(20 of 20: ကဏ္ဌ… p. 142), ဋ read as ဌ or ဠ (14 of 141: ကဝါဋ… p. 500). The same test on vols. 3–4/3
finds the ဉ္ဇ confusion in each (10/18, 17/23, 3/5, 6/7). Vol. 5 is the first book with many of them,
because က-words with these clusters are common.

**Worst pages**: p. 331 (0 of 1), p. 106 (2/10), p. 142 (4/13), p. 497 (2/6), p. 81 (3/8), p. 98
(6/15). Each was tested against its neighbours' index lists, and none is out of order. Pp. 106 and
142 were examined against the images: see `articles-report.md`.
