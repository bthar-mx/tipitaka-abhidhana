# Vol. 21 (သံသ – သန္နာဟယာမသေ) — OCR report

*25 September 2026. `tools/run_volumes.sh 21 25` (natively on the Mac):
`abhidhana_ocr.py 21 --columns --dpi 70 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures from `python3 tools/abhidhana_ocr_stats.py 21` over `ocr/21/pages/`.*

925 PDF pages: 28 of front matter, 880 carrying index entries, 16 inside the body that the index
does not cover, and 1 of back matter. **8,129 index headwords**, 7,901 distinct. Index
`start_page` 28.

**Why this book waited.** Its index seemed to run 65 pages past the PDF (index p. 962 → PDF 990 of
925). It does not: ten headwords, ids 170346–170355 (သတ္ထုဝဏ္ဏာဘတ … သတ္ထုဝိဿာသိက), carry p. 962
for 692, a transposition, and index p. 692 is otherwise empty. PDF p. 720 prints ၆၉၂ with exactly
those ten (image), and PDF p. 924 prints ၈၉၆ with the index's last seven. `ID_PAGE_FIX` reads the
ten on p. 720, and since 25 Sep `abhidhana_ocr.py` scores each page against the corrected lists
(brief §27).

## Settings

- **70 dpi**, the median of three sampled pages (72/70/70 ppi), 1-bit scans.
- Column cut + one whole-page psm 6 pass. Gutter median 0.496, sd 0.011; no page at ≥ 0.54.

## Result

| | vol. 21 |
|---|---:|
| headwords found verbatim, either pass | **7,466 / 8,129 = 91.8%** |
| … with the spelling folds | 92.3% |
| column pass alone | 90.3% |
| whole-page pass alone | 87.6% |
| **in printed order, column pass** | **75.9%** |
| in printed order, whole-page pass | 51.0% |
| pages where every headword came out | 484 of 880 = 55.0% |
| pages at or above 90% | 71.7% |
| pages at or above 80% | 89.2% |
| pages below 50% | 7 |

By hundred pages: 95, 93, 92, 87, 90, 91, 93, 93, 93, 94%. The median missed headword is 13
characters.

**Worst pages**: p. 417 (0 of 2), p. 318 (3 of 10), p. 290 (1 of 3), p. 319 (5 of 13), p. 816
(4 of 10), p. 486 (7 of 17), p. 798 (5 of 11), p. 363 (7 of 14). On p. 318 (checked on the
image) the headwords are printed with a ligature for the kinzi of သင်္ခ that the OCR does not read;
the fuzzy alignment places them (`articles-report.md`).
