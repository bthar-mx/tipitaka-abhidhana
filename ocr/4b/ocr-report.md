# Vol. 4b (ဥဒ – ဥဠုရာဇ) — OCR report

*25 September 2026. `tools/abhidhana_ocr.py 4b --columns --dpi 72 --passes page.psm6 --workers 10`,
run natively on the editor's Mac. Figures measured from `ocr/4b/pages/` with `--score`.*

Book 4b is vol. 4, part 2. 681 PDF pages: 16 of front matter, 631 carrying index entries, 33 inside
the body that the index does not cover (a long article fills them), and 1 of back matter (p. 681).
**6,655 index headwords.** Index `start_page` 16.

## Settings

- **72 dpi.** The page images are 72–77 ppi: 554 at 72, 11 at 73, 115 at 74, 1 at 77
  (`pdfimages -list`). Rendering at 72 reduces the 74 ppi pages by 3%; the effect was not measured.
- Column cut + one whole-page psm 6 pass. A gutter was found on every indexed page.
- The book is set in a different, cleaner typeface from vols. 1–4/1 (bold headwords, light labels).

## Result

| | vol. 4/2 | vol. 4/1 | vol. 3 |
|---|---:|---:|---:|
| headwords found verbatim, either pass | **6,211 / 6,655 = 93.3%** | 88.9% | 92.9% |
| column pass alone | 91.1% | 84.8% | 88.5% |
| whole-page pass alone | 86.0% | 69.6% | 73.1% |
| **in printed order, column pass** | **76.0%** | 73.1% | 77.3% |
| in printed order, whole-page pass | 50.1% | 43.0% | 42.9% |
| pages where every headword came out | 379 of 631 = 60.1% | 50.4% | 56.1% |
| pages at or above 90% | 79.2% | 64.9% | 74.9% |
| pages at or above 80% | 93.3% | 82.0% | 92.0% |
| pages below 50% | 6 | 9 | 6 |

The median missed headword is 12 characters. Recall is even through the book (92–96% per hundred pages).

**Worst pages**: p. 74 (0 of 7), p. 415 (3/12), p. 416 (7/17), p. 563 (7/15), p. 417 (8/17),
p. 252 (10/21). Each was tested against its neighbours' index lists, and none is out of order.
Pp. 74 and 416 were examined against the images: in both the OCR is right and the index spells
differently from the print (see `articles-report.md`).
