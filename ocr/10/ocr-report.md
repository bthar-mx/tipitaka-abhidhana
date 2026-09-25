# Vol. 10 (ဒ – ဒွေဠှကပုစ္ဆာ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 10 --columns --dpi 75 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/10/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

981 PDF pages: 48 of front matter, 786 carrying index entries, 144 inside the body that the
index does not cover, and 3 of back matter. **7,366 index headwords**, 7,176 distinct. Index
`start_page` 48.

## Settings

- **75 dpi**, chosen by the batch as the median of three sampled pages. The page images: 84 at 71 ppi, 271 at 73, 331 at 74, 294 at 75, 1 at 82.
- Column cut + one whole-page psm 6 pass. Gutter median 0.499, sd 0.014; 11 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 73.4%.

## Result

| | vol. 10 |
|---|---:|
| headwords found verbatim, either pass | **6,635 / 7,366 = 90.1%** |
| … with the spelling folds | 90.3% |
| column pass alone | 85.8% |
| whole-page pass alone | 70.5% |
| **in printed order, column pass** | **74.0%** |
| in printed order, whole-page pass | 42.9% |
| pages where every headword came out | 408 of 786 = 51.9% |
| pages at or above 90% | 66.7% |
| pages at or above 80% | 83.3% |
| pages below 50% | 12 |

By hundred pages: 86, 91, 94, 92, 92, 92, 90, 87, 93, 84%. The median missed headword is 12 characters.

**Worst pages**: p. 633 (1 of 5), p. 936 (2 of 8), p. 932 (4 of 12), p. 85 (1 of 3), p. 520 (1 of 3), p. 786 (4 of 10), p. 78 (3 of 7), p. 970 (7 of 16). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
