# Vol. 16 (မ – မှိတပုဗ္ဗ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 16 --columns --dpi 73 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/16/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

890 PDF pages: 26 of front matter, 838 carrying index entries, 24 inside the body that the
index does not cover, and 2 of back matter. **10,394 index headwords**, 10,280 distinct. Index
`start_page` 26.

## Settings

- **73 dpi**, chosen by the batch as the median of three sampled pages. The page images: 650 at 73 ppi, 226 at 72, 14 others.
- Column cut + one whole-page psm 6 pass. Gutter median 0.497, sd 0.011; 4 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 76.9%.

## Result

| | vol. 16 |
|---|---:|
| headwords found verbatim, either pass | **9,218 / 10,394 = 88.7%** |
| … with the spelling folds | 89.4% |
| column pass alone | 85.3% |
| whole-page pass alone | 67.4% |
| **in printed order, column pass** | **75.5%** |
| in printed order, whole-page pass | 40.0% |
| pages where every headword came out | 279 of 838 = 33.3% |
| pages at or above 90% | 60.3% |
| pages at or above 80% | 83.9% |
| pages below 50% | 11 |

By hundred pages: 90, 85, 85, 89, 88, 93, 92, 86, 92%. The median missed headword is 12 characters.

**Worst pages**: p. 741 (6 of 21), p. 742 (6 of 17), p. 169 (4 of 10), p. 280 (4 of 10), p. 872 (5 of 12), p. 298 (6 of 14), p. 714 (3 of 7), p. 784 (7 of 16). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
