# Vol. 9 (တ – ထောမေဿာမိ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 09
--columns --dpi 75 --passes page.psm6 --workers 10 --budget 100000`, run natively on the editor's Mac.
Figures measured from `ocr/09/pages/` with `--score`.*

893 PDF pages: 52 of front matter, 772 carrying index entries, 65 inside the body that the index
does not cover, and 4 of back matter. **6,805 index headwords**, 6,652 distinct. Index
`start_page` 52.

## Settings

- **75 dpi.** The page images are 75 ppi (672), 76 (220) and 77 (1).
- Column cut + one whole-page psm 6 pass. Gutter median 0.503, sd 0.020; 15 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22).

## Result

| | vol. 9 | vol. 8 | vol. 7 | vol. 6 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **6,093 / 6,805 = 89.5%** | 91.5% | 91.5% | 92.4% |
| … with the spelling folds | 90.1% | 92.2% | 91.9% | 93.1% |
| column pass alone | 85.9% | 87.3% | 86.3% | 87.4% |
| whole-page pass alone | 68.0% | 72.0% | 72.3% | 76.5% |
| **in printed order, column pass** | **73.8%** | 75.2% | 73.8% | 75.3% |
| in printed order, whole-page pass | 41.8% | 43.3% | 43.9% | 44.5% |
| pages where every headword came out | 398 of 772 = 51.6% | 58.2% | 50.4% | 48.3% |
| pages at or above 90% | 64.8% | 72.9% | 69.7% | 72.7% |
| pages at or above 80% | 84.5% | 86.6% | 88.7% | 92.3% |
| pages below 50% | 8 | 13 | 3 | 4 |

By hundred pages: 86, 88, 92, 89, 89, 87, 90, 92, 92%. The median missed headword is 12 characters.

**Worst pages**: p. 422 (1 of 11), pp. 436–437 (2 of 14, 2 of 11), p. 423 (2/9), p. 823 (3/12), p. 580
(4/12), p. 343 (2/6), p. 421 (1/3). Each was tested against its neighbours' index lists (with the
folds); on every one its own list scores best, so no page is bound out of order. Pp. 421–423 and
436–437 are ိံ printed with the anusvāra set apart (တာဝတိ˙သ). **P. 823 is a failed reading**, not a
bad page: re-read with the same code in the cloud container, its column pass found 11 of 12. Pp.
422, 423, 436, 437 re-read there came out as before.
