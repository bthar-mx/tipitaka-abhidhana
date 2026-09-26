# Vol. 18 (လ – ဝဠာဝါရထ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (the editor's batch, natively on the Mac):
`abhidhana_ocr.py 18 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/18/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

890 PDF pages: 18 of front matter, 792 carrying index entries, 78 inside the body that the
index does not cover, and 2 of back matter. **7,829 index headwords**, 7,449 distinct. Index
`start_page` 18.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 886 at 72 ppi, 4 others.
- Column cut + one whole-page psm 6 pass. Gutter median 0.503, sd 0.016; 8 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 84.8%.

## Result

| | vol. 18 |
|---|---:|
| headwords found verbatim, either pass | **6,981 / 7,829 = 89.2%** |
| … with the spelling folds | 89.9% |
| column pass alone | 86.5% |
| whole-page pass alone | 70.1% |
| **in printed order, column pass** | **74.3%** |
| in printed order, whole-page pass | 41.9% |
| pages where every headword came out | 385 of 792 = 48.6% |
| pages at or above 90% | 66.4% |
| pages at or above 80% | 84.3% |
| pages below 50% | 13 |

By hundred pages: 90, 95, 88, 92, 86, 85, 89, 90, 89%. The median missed headword is 12 characters.

**Worst pages**: p. 727 (0 of 2), p. 886 (3 of 17), p. 487 (1 of 5), p. 80 (4 of 16), p. 662 (4 of 12), p. 497 (2 of 6), p. 633 (8 of 22), p. 540 (2 of 5). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
