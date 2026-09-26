# Vol. 14/3 (ပဝ – ပ္လုတ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (the editor's batch, natively on the Mac):
`abhidhana_ocr.py 14c --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/14c/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

1,107 PDF pages: 27 of front matter, 1,012 carrying index entries, 65 inside the body that the
index does not cover, and 3 of back matter. **10,390 index headwords**, 9,914 distinct. Index
`start_page` 27.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 1,045 at 72 ppi, 62 at 79.
- Column cut + one whole-page psm 6 pass. Gutter median 0.501, sd 0.011; 21 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 75.6%.

## Result

| | vol. 14/3 |
|---|---:|
| headwords found verbatim, either pass | **9,549 / 10,390 = 91.9%** |
| … with the spelling folds | 92.2% |
| column pass alone | 89.5% |
| whole-page pass alone | 86.5% |
| **in printed order, column pass** | **75.7%** |
| in printed order, whole-page pass | 51.0% |
| pages where every headword came out | 568 of 1012 = 56.1% |
| pages at or above 90% | 74.1% |
| pages at or above 80% | 89.8% |
| pages below 50% | 11 |

By hundred pages: 93, 96, 96, 92, 93, 90, 83, 90, 95, 89, 96, 69%. The median missed headword is 11 characters.

**Worst pages**: p. 609 (0 of 2), p. 675 (0 of 1), p. 782 (0 of 1), p. 1104 (2 of 14), p. 783 (1 of 3), p. 564 (7 of 19), p. 607 (6 of 15), p. 611 (2 of 5). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
