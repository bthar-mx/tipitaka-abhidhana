# Vol. 22 (သန္နိကဋ္ဌ – သမ္ဘောန္တိ) — OCR report

*25 September 2026. `tools/run_volumes.sh` (Angel's batch, natively on the Mac):
`abhidhana_ocr.py 22 --columns --dpi 72 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures measured from `ocr/22/pages/` with `--score` and from `logs/run-20260925-0920.log`.*

933 PDF pages: 40 of front matter, 861 carrying index entries, 32 inside the body that the
index does not cover, and 0 of back matter. **8,075 index headwords**, 7,929 distinct. Index
`start_page` 40.

## Settings

- **72 dpi**, chosen by the batch as the median of three sampled pages. The page images: 758 at 72 ppi, the rest 73–95.
- Column cut + one whole-page psm 6 pass. Gutter median 0.501, sd 0.011; 9 indexed pages at ≥ 0.54,
  the range where cuts have gone through the right-hand column in other books (brief §22), whose column pass reads 90.7%.

## Result

| | vol. 22 |
|---|---:|
| headwords found verbatim, either pass | **7,143 / 8,075 = 88.5%** |
| … with the spelling folds | 90.4% |
| column pass alone | 85.8% |
| whole-page pass alone | 82.4% |
| **in printed order, column pass** | **80.6%** |
| in printed order, whole-page pass | 52.9% |
| pages where every headword came out | 464 of 861 = 53.9% |
| pages at or above 90% | 69.5% |
| pages at or above 80% | 85.4% |
| pages below 50% | 42 |

By hundred pages: 95, 87, 89, 91, 91, 93, 94, 92, 75, 46%. The median missed headword is 12 characters.

**Worst pages**: p. 173 (0 of 15), p. 828 (0 of 12), p. 927 (0 of 11), p. 174 (0 of 10), p. 175 (0 of 10), p. 837 (0 of 10), p. 933 (0 of 10), p. 829 (0 of 9). Each indexed page's list was scored
on its own page and on its neighbours (with the folds); see `articles-report.md` for what was found.
