# Vol. 4c (ဦ – ဩဠုမ္ပိက) — OCR report

*25 September 2026. `ABHIDHANA_TESSDATA=~/Tipitaka/nissaya/tessdata python3 tools/abhidhana_ocr.py 4c
--columns --dpi 72 --passes page.psm6 --workers 10 --budget 100000`, run natively on Angel's Mac.
Figures measured from `ocr/4c/pages/` with `--score`.*

Book 4c is vol. 4, part 3. 736 PDF pages: 27 of front matter, 677 carrying index entries, 31 inside
the body that the index does not cover (a long article fills them), and 1 at the end (p. 736).
**5,230 index headwords**, 5,008 distinct. Index `start_page` 27.

**The PDF ends with three supplements, not part of vol. 4/3** (PDF pp. 713–735; index pp. 686–708).
Each is headed "တိပိဋက ပါဠိ-မြန်မာအဘိဓာန် … ၌ ဖြည့်စွက်အပ်သောပုဒ်များ", "entries added to …":

| PDF pp. | supplement to | index headwords | also indexed in that book |
|---|---|---:|---:|
| 713–720 | vol. 15 (ဘိဇ္ဇ … ဘိဇ္ဇေယျုံ) | 53 | 0 |
| 721–730 | vol. 4/2 (ဥဒဝါ … ဥဠုဂ္ဂဟယုဒ္ဓ) | 114 | 19 in 4b |
| 731–735 | vol. 16 (မံသကာရဏ … မောဟိတဗ္ဗ) | 56 | 16 in 16 |

So 5,007 index headwords belong to vol. 4/3 itself and 223 to the supplements. The index files the
supplements under book 4c, and so do `articles.jsonl` and the Reader. The title page's 5,163 (brief
§3) matches neither 5,007 nor 5,230; that is still unexplained.

## Settings

- **72 dpi.** The page images are 69–73 ppi: 401 at 69, 93 at 70, 118 at 71, 122 at 72, 2 at 73
  (`pdfimages -list`). Rendering at 72 enlarges the 69 ppi pages by 4%; the effect was not measured.
- Column cut + one whole-page psm 6 pass. A gutter was found on every indexed page.

## Result

| | vol. 4/3 | vol. 4/2 | vol. 4/1 | vol. 3 |
|---|---:|---:|---:|---:|
| headwords found verbatim, either pass | **4,732 / 5,230 = 90.5%** | 93.3% | 88.9% | 92.9% |
| column pass alone | 88.1% | 91.1% | 84.8% | 88.5% |
| whole-page pass alone | 84.5% | 86.0% | 69.6% | 73.1% |
| **in printed order, column pass** | **72.3%** | 76.0% | 73.1% | 77.3% |
| in printed order, whole-page pass | 50.4% | 50.1% | 43.0% | 42.9% |
| pages where every headword came out | 371 of 677 = 54.8% | 60.1% | 50.4% | 56.1% |
| pages at or above 90% | 63.2% | 79.2% | 64.9% | 74.9% |
| pages at or above 80% | 85.2% | 93.3% | 82.0% | 92.0% |
| pages below 50% | 5 | 6 | 9 | 6 |

The median missed headword is 10 characters, as for the volume. Vol. 4/3 itself (PDF pp. 1–712):
90.7%; the supplements: 86.1%. By hundred pages: 92–93% to p. 399, then 89, 92, 86 and 85%.

**Worst pages**: p. 138 (0 of 1), p. 615 (5/17), p. 634 (1/3), p. 487 (3/8), p. 438 (2/5). Each was
tested against its neighbours' index lists, and none is out of order. **P. 615 is an index error**,
not an OCR one: 10 of its 17 index headwords (ဩလမ္ဗနဟေတု … ဩလမ္ဗမာနသီသ, ids 176418–176427) are
printed on pp. 613–614; the index gives page 588 for them instead of 586–587. See `articles-report.md`.
