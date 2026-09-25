# Vol. 23 (သမ္မ – သိဟလ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 23 --columns --dpi 323 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/23/pages/` and from `logs/run-20260925-0920.log`.*

780 PDF pages: 35 of front matter, 723 carrying index entries, 22 inside the body that the
index does not cover, and 0 of back matter. **7,182 index headwords**, 6,989 distinct. Index
`start_page` 35.

## Settings

- **323 dpi**, the scan's own resolution (323 ppi on all three sampled pages; A4 pages). Every
  other book so far is 69–96 ppi: this is the only high-resolution scan in the set. OCR took 14
  minutes for 780 pages, no slower than the 72-dpi books.
- Column cut + one whole-page psm 6 pass. Gutter median 0.500, sd 0.009; 9 indexed pages at
  ≥ 0.54, whose column pass reads 97.3% (not the failure of brief §22).

## Result

| | vol. 23 |
|---|---:|
| headwords found verbatim, either pass | **6,538 / 7,182 = 91.0%** |
| … with the spelling folds | 91.2% |
| column pass alone | 88.6% |
| whole-page pass alone | 86.8% |
| **in printed order, column pass** | **83.2%** (the highest so far) |
| in printed order, whole-page pass | 55.1% |
| pages where every headword came out | 389 of 723 = 53.8% |
| pages at or above 90% | 72.3% |
| pages at or above 80% | 88.1% |
| pages below 50% | 10 |

By hundred pages: 86, 90, 91, 92, 92, 91, 94, 91%. The median missed headword is 13 characters.

**Worst pages**: p. 100 (0 of 10), p. 231 (0 of 3), p. 456 (4 of 18), p. 74 (3 of 11), p. 276
(7 of 21), p. 556 (4 of 12), p. 346 (4 of 11), p. 582 (4 of 9). P. 100 is the index's spelling,
not the OCR: it writes အမ္မဝါ… for the printed သမ္မာဝါ… (`articles-report.md`).

**Higher resolution did not buy higher recall.** 91.0% is in the range of the 72-dpi books
(88.5–96.3%); the in-order share (83.2%) is the best of any book. Whether that is the
resolution or this book's print is not separated.
