# Vol. 19 (ဝါ – ဝိဝေကောဓိမုတ္တိ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 19 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/19/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

982 PDF pages: 21 of front matter, 903 carrying index entries, 57 inside the body that the
index does not cover, and 1 of back matter. **9,251 index headwords**, 8,967 distinct. Index
`start_page` 21.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 824 at 72 ppi, 142 at 71, 16 at 73–75.
- Column cut + one whole-page psm 6 pass. Gutter median 0.503, sd 0.011; 2 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 95.0%.

## Result

| | vol. 19 |
|---|---:|
| headwords found verbatim, either pass | **8,913 / 9,251 = 96.3%** |
| … with the spelling folds | 96.6% |
| column pass alone | 94.3% |
| whole-page pass alone | 94.7% |
| **in printed order, column pass** | **78.5%** |
| in printed order, whole-page pass | 54.3% |
| pages where every headword came out | 700 of 903 = 77.5% |
| pages at or above 90% | 89.4% |
| pages at or above 80% | 96.6% |
| pages below 50% | 6 |

By hundred pages: 96, 98, 96, 93, 96, 98, 97, 98, 96, 95%. The median missed headword is 12 characters.

**Worst pages**: p. 372 (2 of 18), p. 369 (2 of 12), p. 371 (2 of 11), p. 290 (4 of 10), p. 354 (2 of 5), p. 370 (5 of 11), p. 59 (6 of 10), p. 886 (3 of 5). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
