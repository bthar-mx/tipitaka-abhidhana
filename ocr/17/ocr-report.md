# Vol. 17 (ယ – ရောဟိသ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (the editor's batch, natively on the Mac):
`abhidhana_ocr.py 17 --columns --dpi 69 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/17/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

879 PDF pages: 22 of front matter, 736 carrying index entries, 85 inside the body that the
index does not cover, and 36 of back matter. **6,520 index headwords**, 6,247 distinct. Index
`start_page` 22.

## Settings

- **69 dpi**, chosen by the batch as the median of three sampled pages. The page images: 502 at 72 ppi, 210 at 69, 158 at 68, 9 others.
- Column cut + one whole-page psm 6 pass. Gutter median 0.496, sd 0.011; 1 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 75.0%.

## Result

| | vol. 17 |
|---|---:|
| headwords found verbatim, either pass | **5,956 / 6,520 = 91.3%** |
| … with the spelling folds | 91.7% |
| column pass alone | 88.6% |
| whole-page pass alone | 74.0% |
| **in printed order, column pass** | **75.2%** |
| in printed order, whole-page pass | 44.7% |
| pages where every headword came out | 401 of 736 = 54.5% |
| pages at or above 90% | 67.8% |
| pages at or above 80% | 88.2% |
| pages below 50% | 3 |

By hundred pages: 93, 92, 89, 90, 89, 90, 93, 93, 97%. The median missed headword is 11 characters.

**Worst pages**: p. 459 (3 of 9), p. 395 (4 of 10), p. 429 (4 of 9), p. 458 (4 of 8), p. 357 (3 of 6), p. 352 (2 of 4), p. 263 (1 of 2), p. 294 (6 of 10). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
