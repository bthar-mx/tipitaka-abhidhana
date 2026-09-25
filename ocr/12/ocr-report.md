# Vol. 12 (နိက္ခိတ္တ – နှာရုသုတ္တနိဗန္ဓန) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 12 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/12/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

1,123 PDF pages: 37 of front matter, 936 carrying index entries, 148 inside the body that the
index does not cover, and 2 of back matter. **7,022 index headwords**, 6,885 distinct. Index
`start_page` 37.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 961 at 72 ppi, 156 at 70, 6 at 71–75.
- Column cut + one whole-page psm 6 pass. Gutter median 0.504, sd 0.012; 3 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 96.7%.

## Result

| | vol. 12 |
|---|---:|
| headwords found verbatim, either pass | **6,604 / 7,022 = 94.0%** |
| … with the spelling folds | 94.5% |
| column pass alone | 91.9% |
| whole-page pass alone | 89.5% |
| **in printed order, column pass** | **77.9%** |
| in printed order, whole-page pass | 53.8% |
| pages where every headword came out | 671 of 936 = 71.7% |
| pages at or above 90% | 78.6% |
| pages at or above 80% | 92.8% |
| pages below 50% | 10 |

By hundred pages: 87, 94, 96, 95, 93, 95, 95, 94, 97, 93, 95, 82%. The median missed headword is 12 characters.

**Worst pages**: p. 67 (2 of 10), p. 770 (1 of 4), p. 742 (2 of 6), p. 975 (1 of 3), p. 514 (3 of 8), p. 690 (3 of 8), p. 922 (2 of 5), p. 1112 (5 of 12). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
