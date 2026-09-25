# Vol. 2 (အနု – အဗ္ဘောက္ကိရဏ) — OCR report

*24 September 2026. `tools/abhidhana_ocr.py 02 --columns --dpi 72 --passes page.psm6 --workers 10`,
run natively on Angel's Mac (Homebrew tesseract, `myap`), about 45 pages a minute. Figures
measured from `ocr/02/pages/`.*

898 PDF pages: 18 of front matter, 855 carrying index entries, 24 inside the body that the
index does not cover (a long article fills them), and the colophon (p. 898). **7,189 index
headwords.**

## Settings

- **72 dpi, native.** Pages are declared 2000 × 3158 pt. The 1-bit JBIG2 images are 2000 px wide
  at 72 ppi (heights 2958–3224 px; 34 pages at 73–74 ppi). `-r 72` is 1:1.
- Column cut + one whole-page psm 6 pass, as for vol. 1. The printed rule was found on all but
  8 pages, where the cut went in the white channel.

## Result

| | vol. 2 | vol. 1 |
|---|---:|---:|
| headwords found verbatim, either pass | **6,662 / 7,189 = 92.7%** | 92.0% |
| column pass alone | 87.7% | 88.5% |
| whole-page pass alone | 75.5% | 72.0% |
| **in printed order, column pass** | **75.5%** | 76.1% |
| in printed order, whole-page pass | 46.9% | 42.3% |
| pages where every headword came out | 528 of 855 = 61.8% | 53.5% |
| pages at or above 90% | 74.7% | 72.0% |
| pages at or above 80% | 91.3% | 90.0% |
| pages below 50% | 5 | 7 |

As in vol. 1, the misses are mostly long compounds: the median missed headword is 12 characters,
against 11 for the volume.

**Worst pages**
- **Pp. 241 and 242 (0 of 5, 0 of 10) are bound in the wrong order.** The running heads print
  ၂၂၄ on p. 241 and 223 on p. 242, and each page carries the other's index headwords (10 of 10 of
  242's list are on 241). The OCR is fine. Recall is scored against the index's order, so the
  table above counts these 15 as missed. `PAGE_FIX` in `abhidhana_articles.py` corrects the order.
  Corrected, recall is 6,675 / 7,189 = 92.9%.
- **Pp. 114–115 (4 of 9, 4 of 14)** are pages of spelling-variant entries, အနုပါဒိဏ္ဏ(န္န)က…: one
  printed entry for two index headwords, neither of which appears verbatim.
- P. 700 (4 of 9) was not examined.

## Front and back matter

Pages 1–18 are the title pages and preface, in one column. The index does not cover them, so
nothing measures their accuracy; read the `page.psm6` text. P. 898 is the colophon.
