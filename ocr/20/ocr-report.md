# Vol. 20 (ဝိဝေကာနိသံသ – သံဝေါဟာရ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 20 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/20/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

945 PDF pages: 30 of front matter, 832 carrying index entries, 81 inside the body that the
index does not cover, and 2 of back matter. **7,366 index headwords**, 7,113 distinct. Index
`start_page` 30.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 607 at 72 ppi, 160 at 71, 144 at 73, 34 at 74–76.
- Column cut + one whole-page psm 6 pass. Gutter median 0.495, sd 0.009; 0 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22).

## Result

| | vol. 20 |
|---|---:|
| headwords found verbatim, either pass | **6,737 / 7,366 = 91.5%** |
| … with the spelling folds | 91.7% |
| column pass alone | 90.8% |
| whole-page pass alone | 91.1% |
| **in printed order, column pass** | **76.6%** |
| in printed order, whole-page pass | 53.2% |
| pages where every headword came out | 469 of 832 = 56.4% |
| pages at or above 90% | 71.6% |
| pages at or above 80% | 89.1% |
| pages below 50% | 13 |

By hundred pages: 88, 94, 95, 93, 90, 96, 91, 88, 88, 90%. The median missed headword is 12 characters.

**Worst pages**: p. 366 (0 of 2), p. 544 (0 of 1), p. 866 (0 of 1), p. 425 (1 of 12), p. 424 (1 of 9), p. 818 (1 of 5), p. 716 (3 of 10), p. 421 (4 of 12). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
