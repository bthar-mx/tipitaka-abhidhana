# Vol. 24 (သီကတိ – သူသူ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 24 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/24/pages/` and from `logs/run-20260925-0920.log`.*

718 PDF pages: 34 of front matter, 666 carrying index entries, 15 inside the body that the
index does not cover, and 3 of back matter. **7,088 index headwords**, 6,954 distinct. Index
`start_page` 34.

## Settings

- **72 dpi**, the scan's own resolution (72 ppi on all three sampled pages). OCR took 11 minutes.
- Column cut + one whole-page psm 6 pass. Gutter median 0.500, sd 0.014; 15 indexed pages at
  ≥ 0.54, whose column pass reads 80.8% against 88.3% for the book: candidates for
  `tools/abhidhana_recut.py` (brief §22, §24).

## Result

| | vol. 24 |
|---|---:|
| headwords found verbatim, either pass | **6,486 / 7,088 = 91.5%** |
| … with the spelling folds | 91.9% |
| column pass alone | 88.3% |
| whole-page pass alone | 86.4% |
| **in printed order, column pass** | **84.1%** (the highest so far) |
| in printed order, whole-page pass | 54.7% |
| pages where every headword came out | 330 of 666 = 49.5% |
| pages at or above 90% | 71.3% |
| pages at or above 80% | 88.4% |
| pages below 50% | 4 |

By hundred pages: 90, 92, 92, 93, 92, 92, 90, 87%. The median missed headword is 13 characters.

**Worst pages**: p. 540 (2 of 10), p. 441 (4 of 11), p. 681 (10 of 22), p. 586 (5 of 11), p. 712
(6 of 12), p. 328 (3 of 6), p. 551 (1 of 2), p. 55 (7 of 13). P. 540 is the index, not the OCR:
eight of its ten headwords are printed on p. 542 (`articles-report.md`).
