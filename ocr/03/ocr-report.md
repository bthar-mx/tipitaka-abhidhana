# Vol. 3 (အဗျဂ္ဂ – အဠာရပမှ) — OCR report

*24 September 2026. `tools/abhidhana_ocr.py 03 --columns --dpi 75 --passes page.psm6 --workers 10`,
run natively on the editor's Mac. Figures measured from `ocr/03/pages/`.*

1,177 PDF pages: 8 of front matter, 1,124 carrying index entries, 43 inside the body that the
index does not cover (a long article fills them), and 2 of back matter (pp. 1176–1177). **11,726
index headwords.**

## Settings

- **75 dpi, native for most pages.** Pages are declared 2132 × 3254 pt. 919 of the 1,177 images are
  2206 × 3379 px at 75 ppi, and the rest are 72–75 ppi (p. 50 is 72). Rendering at 75 upsamples
  the 72 ppi pages by 4%; the effect was not measured.
- Column cut + one whole-page psm 6 pass. The printed rule was found on all but 4 pages.

## Result

| | vol. 3 | vol. 2 | vol. 1 |
|---|---:|---:|---:|
| headwords found verbatim, either pass | **10,895 / 11,726 = 92.9%** | 92.7% | 92.0% |
| column pass alone | 88.5% | 87.7% | 88.5% |
| whole-page pass alone | 73.1% | 75.5% | 72.0% |
| **in printed order, column pass** | **77.3%** | 75.5% | 76.1% |
| in printed order, whole-page pass | 42.9% | 46.9% | 42.3% |
| pages where every headword came out | 631 of 1,124 = 56.1% | 61.8% | 53.5% |
| pages at or above 90% | 74.9% | 74.7% | 72.0% |
| pages at or above 80% | 92.0% | 91.3% | 90.0% |
| pages below 50% | 6 | 5 | 7 |

The median missed headword is 12 characters, against 10 for the volume.

**Worst pages**: p. 654 (0 of 4), pp. 1007–1009 (5/15, 6/13, 6/12), p. 232 (4/10), p. 997 (4/10),
p. 637 (5/12). Each was tested against its neighbours' index lists, and none is out of order.
They have not been examined against the images.
