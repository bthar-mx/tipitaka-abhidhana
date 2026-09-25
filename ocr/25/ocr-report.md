# Vol. 25 (သော – ဠကာရ) — OCR report

*25 September 2026. `tools/run_volumes.sh 25` (natively on the Mac):
`abhidhana_ocr.py 25 --columns --dpi 200 --passes page.psm6 --workers 10`, then the articles and
romanisation steps. Figures from `python3 tools/abhidhana_ocr_stats.py 25` over `ocr/25/pages/`.
The pilot of 21 Sep (whole page, no column cut) is described in `pilot-report.md`; its records are
in `tmp/ocr-25-pilot-pages/` (gitignored).*

466 PDF pages: 34 of front matter, 429 carrying index entries, 3 inside the body that the index
does not cover. **4,046 index headwords**, 3,953 distinct. Index `start_page` 34.

## Settings: 200 dpi, not the native 300

The scan is 300 ppi (three pages sampled). The batch first rendered it at 300, as it does every
book, and recall fell to 88.2% (column pass 79.3%). On the same 16 pages, the worst of that run,
300 dpi read 57.8% of the headwords and 200 dpi 88.3% (brief §29). The pilot had found the same in
September ("200 dpi, not 300", brief §5). Vol. 23 at 323 ppi was not hurt, so the cause is this
book's type size, not resolution as such. The 300-dpi run is kept in `tmp/ocr-25-300dpi/`.

Column cut + one whole-page psm 6 pass. The gutter is found at 0.499 on 431 of the 466 pages: the scan is aligned, its rule in one place
throughout.

## Result

| | vol. 25, 200 dpi | 300 dpi (discarded) | pilot, whole page, 2 passes |
|---|---:|---:|---:|
| headwords found verbatim, either pass | **3,838 / 4,046 = 94.9%** | 88.2% | 94.0% |
| … with the spelling folds | 95.0% | 88.4% | |
| column pass alone | 89.4% | 79.3% | |
| whole-page pass alone | 88.8% | 78.2% | 88.6% (psm 6) |
| **in printed order, column pass** | **83.4%** | 73.3% | |
| in printed order, whole-page pass | 55.7% | 49.8% | |
| pages where every headword came out | 288 of 429 = 67.1% | 45.5% | 63% |
| pages at or above 90% | 82.1% | 61.8% | 79% |
| pages at or above 80% | 95.3% | 82.1% | 92% |
| pages below 50% | 2 | 12 | 0 |

By hundred pages: 96, 94, 94, 94, 97%. The median missed headword is 13 characters. The best
verbatim recall and the best in-order share of any scanned book.

**Worst pages**: p. 159 (2 of 11), p. 158 (3 of 7), p. 301 (6 of 11), p. 160 (4 of 7), p. 221 (6 of
10), p. 179 (3 of 5), p. 292 (3 of 5), p. 192 (5 of 8). Pp. 158–160 are the headwords in သ္နေ
(sneha…), a stacked consonant the OCR does not read; the fuzzy alignment places them
(`articles-report.md`).
