# Vol. 13 (ပ – ပဋိဗြူဟန) — OCR report

*25 September 2026. `tools/run_volumes.sh` (the editor's batch, natively on the Mac):
`abhidhana_ocr.py 13 --columns --dpi 73 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/13/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

896 PDF pages: 30 of front matter, 795 carrying index entries, 70 inside the body that the
index does not cover, and 1 of back matter. **7,279 index headwords**, 7,128 distinct. Index
`start_page` 30.

## Settings

- **73 dpi**, chosen by the batch as the median of three sampled pages. The page images: 720 at 73 ppi, 139 at 72, 34 at 75, 3 others.
- Column cut + one whole-page psm 6 pass. Gutter median 0.501, sd 0.013; 2 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 72.7%.

## Result

| | vol. 13 |
|---|---:|
| headwords found verbatim, either pass | **6,245 / 7,279 = 85.8%** |
| … with the spelling folds | 86.3% |
| column pass alone | 82.3% |
| whole-page pass alone | 58.3% |
| **in printed order, column pass** | **70.9%** |
| in printed order, whole-page pass | 35.9% |
| pages where every headword came out | 366 of 795 = 46.0% |
| pages at or above 90% | 60.8% |
| pages at or above 80% | 80.3% |
| pages below 50% | 27 |

By hundred pages: 93, 71, 92, 88, 85, 86, 88, 89, 86%. The median missed headword is 12 characters.

**Worst pages**: p. 187 (0 of 19), p. 177 (0 of 18), p. 185 (0 of 17), p. 184 (0 of 16), p. 186 (0 of 16), p. 175 (0 of 15), p. 176 (0 of 15), p. 181 (0 of 15). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
