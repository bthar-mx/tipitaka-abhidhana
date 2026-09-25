# Vol. 11 (ဓ – နိက္ခာမေသုံ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 11 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/11/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

769 PDF pages: 80 of front matter, 623 carrying index entries, 65 inside the body that the
index does not cover, and 1 of back matter. **5,663 index headwords**, 5,541 distinct. Index
`start_page` 80.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 763 at 72 ppi, 6 at 73–78.
- Column cut + one whole-page psm 6 pass. Gutter median 0.497, sd 0.011; 3 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 75.9%.

## Result

| | vol. 11 |
|---|---:|
| headwords found verbatim, either pass | **5,046 / 5,663 = 89.1%** |
| … with the spelling folds | 89.5% |
| column pass alone | 86.1% |
| whole-page pass alone | 72.2% |
| **in printed order, column pass** | **74.7%** |
| in printed order, whole-page pass | 44.5% |
| pages where every headword came out | 331 of 623 = 53.1% |
| pages at or above 90% | 66.5% |
| pages at or above 80% | 83.9% |
| pages below 50% | 9 |

By hundred pages: 78, 92, 89, 93, 85, 86, 93, 90%. The median missed headword is 11 characters.

**Worst pages**: p. 478 (0 of 18), p. 250 (2 of 23), p. 251 (3 of 15), p. 441 (2 of 7), p. 433 (3 of 10), p. 98 (3 of 9), p. 740 (3 of 9), p. 572 (2 of 5). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
