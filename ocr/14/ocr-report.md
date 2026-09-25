# Vol. 14 (ပဋိဘံသု – ပမဇ္ဇေယျ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 14 --columns --dpi 70 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/14/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

821 PDF pages: 21 of front matter, 668 carrying index entries, 131 inside the body that the
index does not cover, and 1 of back matter. **5,219 index headwords**, 5,086 distinct. Index
`start_page` 21.

## Settings

- **70 dpi**, chosen by the batch as the median of three sampled pages. The page images: 634 at 70 ppi, 160 at 72, 26 at 73, 1 at 69.
- Column cut + one whole-page psm 6 pass. Gutter median 0.501, sd 0.013; 0 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22).

## Result

| | vol. 14 |
|---|---:|
| headwords found verbatim, either pass | **4,897 / 5,219 = 93.8%** |
| … with the spelling folds | 94.3% |
| column pass alone | 92.3% |
| whole-page pass alone | 89.3% |
| **in printed order, column pass** | **77.0%** |
| in printed order, whole-page pass | 53.5% |
| pages where every headword came out | 486 of 668 = 72.8% |
| pages at or above 90% | 78.3% |
| pages at or above 80% | 91.9% |
| pages below 50% | 7 |

By hundred pages: 96, 92, 94, 92, 96, 92, 93, 98, 98%. The median missed headword is 12 characters.

**Worst pages**: p. 448 (0 of 9), p. 637 (0 of 7), p. 229 (1 of 6), p. 174 (5 of 12), p. 549 (6 of 14), p. 173 (3 of 7), p. 557 (8 of 18), p. 151 (4 of 8). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
