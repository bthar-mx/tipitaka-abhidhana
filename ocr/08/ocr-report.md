# Vol. 8 (ဆိဒ္ဒ – ဏျပစ္စယတ္ထ) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 08
--columns --dpi 72 --passes page.psm6 --workers 10 --budget 100000`, run natively on the editor's Mac.
Figures measured from `ocr/08/pages/` with `--score`.*

849 PDF pages: 40 of front matter, 687 carrying index entries, 119 inside the body that the index
does not cover, and 3 of back matter. **6,448 index headwords**, 6,262 distinct. Index
`start_page` 40.

## Settings

- **72 dpi.** The page images are mixed: 376 at 72 ppi, 146 at 71, 212 at 70, 94 at 69 and 21 at
  57–58. Rendered at 72, the highest, so nothing is downsampled. The 57–58 ppi pages are pp. 2–21
  (front matter) and p. 818, which the index does not cover, so none of them is scored.
- Column cut + one whole-page psm 6 pass. The gutter was found inside 0.44–0.555 of the width on
  every indexed page (median 0.497, sd 0.015); but see below.

## Result

| | vol. 8 | vol. 7 | vol. 6 | vol. 5 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **5,901 / 6,448 = 91.5%** | 91.5% | 92.4% | 90.2% |
| … with the spelling folds | 92.2% | 91.9% | 93.1% | 91.4% |
| column pass alone | 87.3% | 86.3% | 87.4% | 84.9% |
| whole-page pass alone | 72.0% | 72.3% | 76.5% | 71.3% |
| **in printed order, column pass** | **75.2%** | 73.8% | 75.3% | 74.6% |
| in printed order, whole-page pass | 43.3% | 43.9% | 44.5% | 43.4% |
| pages where every headword came out | 400 of 687 = 58.2% | 50.4% | 48.3% | 46.8% |
| pages at or above 90% | 72.9% | 69.7% | 72.7% | 67.6% |
| pages at or above 80% | 86.6% | 88.7% | 92.3% | 85.7% |
| pages below 50% | 13 | 3 | 4 | 9 |

By hundred pages: 94, 91, 94, 90, 90, 92, 96, 94, 82%. The last hundred is the ဍ section
(pp. 804–818 at about 50%), where the bold ဍ of a headword is read as ဒ. The median missed
headword is 11 characters.

**Worst pages**: p. 810 (0 of 8), pp. 241 and 601 (0 of 1), p. 413 (1/8), p. 807 (4/16), p. 383 (3/11),
p. 434 (1/3), p. 112 (3/8). Each was tested against its neighbours' index lists (with the folds),
and pp. 780–849 each against the four pages either side. A neighbour's list scores higher on two
indexed pages only, p. 810 (4 of p. 809's against 0 of its own) and p. 804 (3 against 2), and both
are shared ဍ… stems quoted in running text, not pages out of order.

**Gutters at the upper edge of the accepted range.** Ten indexed pages have a gutter ≥ 0.54; their
column pass reads 68.6% of their headwords against 87.6% on the rest. P. 500 (0.554) was checked:
the cut runs through the right column's first letters. See `articles-report.md` and brief §22.
