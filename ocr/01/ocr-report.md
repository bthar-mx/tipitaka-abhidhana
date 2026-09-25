# Vol. 1 (အ – အနီဠက) — OCR report

*24 September 2026. `tools/abhidhana_ocr.py 01 --columns --dpi 72 --passes page.psm6`, tesseract 5.3.4, `myap`.*

913 PDF pages: 120 of front matter (title pages and the နိဒါန်း introduction), 763 carrying
index entries, and back matter. **8,150 index headwords.**

## Settings, and why

- **72 dpi, the scan's native resolution.** Vol. 1's pages are declared 2014 × 3142 pt, and the 1-bit
  JBIG2 image in each is ~2051 × 3061 px, so `-r 72` is 1:1. The pilot's `-r 200` upsamples 2.8×.
  On 15 pages, column-cut: 72 dpi 92.1% recall / 78.7% in order; 100 dpi 91.5 / 78.7; 200 dpi
  87.8 / 77.4, at 2.6× the time. **Check `pdfimages -list` per book before choosing.**
- **Column cut + one whole-page psm 6 pass.** psm 3 dropped: the column pass is the text used
  for articles; the whole-page pass is kept only to widen headword recall.
- **Gutter.** The printed rule is taken as the darkest column of the middle third, but only
  if it falls in 0.44–0.555 of the width; otherwise the cut goes in the white channel between
  the columns. 14 indexed pages had no usable rule (the detector had landed at 0.56–0.61,
  inside the right-hand column) and were re-read: +22 headwords on those pages.

## Result

| | |
|---|---:|
| headwords found verbatim, either pass | **7,497 / 8,150 = 92.0%** |
| column pass alone | 88.5% |
| whole-page pass alone | 72.0% |
| **in printed order, column pass** | **76.1%** |
| in printed order, whole-page pass | 42.3% |
| pages where every headword came out | 408 of 763 = 53.5% |
| pages at or above 90% | 72.0% |
| pages at or above 80% | 90.0% |
| pages below 50% | 7 |

The column cut is what makes article extraction possible: whole-page OCR keeps only
42.3% of headwords in the order the dictionary prints them.

**Against vol. 25** (the pilot, whole-page, 200 dpi): 94.0% union recall there, 92.0% here.
The gap is modest, and the failures are, as in vol. 25, mostly long
compounds — median length of a missed headword 12 characters against
10 for vol. 1 headwords generally.

Worst pages: p. 220 (0/1), p. 254 (3/10), p. 625 (6/17), p. 585 (6/15), p. 253 (4/9), p. 697 (5/11).
p. 220 carries a single index entry; pp. 253–254 are rule-less pages where both passes are weak and
should be looked at against the image.

## Front matter

Pages 1–120 are set in one column (title pages and the နိဒါန်း introduction on the Pāḷi language and its literature). The column cut garbles them; the `page.psm6` text is the one to read, and
it is legible with some noise from the decorative borders. The index does not cover these
pages, so nothing measures their accuracy.
