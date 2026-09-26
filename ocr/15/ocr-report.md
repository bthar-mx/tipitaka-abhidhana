# Vol. 15 (ဖ – ဘောဝါဒီ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (the editor's batch, natively on the Mac):
`abhidhana_ocr.py 15 --columns --dpi 74 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/15/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

853 PDF pages: 28 of front matter, 752 carrying index entries, 68 inside the body that the
index does not cover, and 5 of back matter. **9,342 index headwords**, 9,183 distinct. Index
`start_page` 28.

## Settings

- **74 dpi**, chosen by the batch as the median of three sampled pages. The page images: 350 at 74 ppi, 237 at 75, 202 at 73, 59 at 72, 5 others.
- Column cut + one whole-page psm 6 pass. Gutter median 0.499, sd 0.011; 1 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 69.2%.

## Result

| | vol. 15 |
|---|---:|
| headwords found verbatim, either pass | **8,503 / 9,342 = 91.0%** |
| … with the spelling folds | 91.3% |
| column pass alone | 87.3% |
| whole-page pass alone | 69.4% |
| **in printed order, column pass** | **76.2%** |
| in printed order, whole-page pass | 40.9% |
| pages where every headword came out | 323 of 752 = 43.0% |
| pages at or above 90% | 66.0% |
| pages at or above 80% | 87.5% |
| pages below 50% | 4 |

By hundred pages: 94, 94, 93, 88, 88, 88, 93, 89, 93%. The median missed headword is 12 characters.

**Worst pages**: p. 448 (0 of 1), p. 473 (3 of 13), p. 533 (4 of 10), p. 393 (6 of 13), p. 719 (5 of 10), p. 594 (2 of 4), p. 528 (7 of 13), p. 452 (6 of 11). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
