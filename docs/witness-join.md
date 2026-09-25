# The typed witness joined to the articles

*25 September 2026. `tools/abhidhana_witness_join.py 01 02 03 4a 4b 05 06`. The per-article output,
`witness/join-NN.jsonl`, stays in the gitignored `witness/` until the witness's licence is known
(`docs/witness.md` §5). This page carries figures only, none of the witness's text.*

## 1. How the two are paired

For each headword, the index rows carrying it (every book, in index id order) are paired in
order with the witness entries carrying it (in the witness's own order): the k-th homonym with
the k-th. The headword is looked up as the index spells it, then with the spelling folds of
`tools/abhidhana_fold.py` (ါ/ာ, ဉ/ည and the stacked-letter confusions). Where the two counts
differ the pairing is still made, in order, and marked `count_mismatch`.

Compared, per article:

- **label**: ours, normalised (`docs/labels.md`), against the witness's, spaces removed.
- **analysis**: the first clause of each, to the first ။. The witness's analysis field runs on
  past the ] into the grammarians' derivation (ကစ+ဆ။ ကစ ဗန္ဓနေ။ ဓာန်၊ ဋီ။ ၂၄၆။ …), and so does the
  print's bracket (vol. 5 p. 63, ကကစ¹: `[က + ကစ + အ။ က ဣတိ … ဓာန်၊ဋီ။ ၅၂၈။]`). Comparing the whole
  field against our bracket made 4% of vol. 5's analyses look different when they were not.
  Similarity is difflib's ratio, + signs and spaces removed; below 0.4 is flagged, the threshold
  of brief §13.
- **body**: the witness's definition (with the rest of its analysis field) against the head of
  our body, as long as it. The witness omits the Pāḷi quotations and lightly edits, so this ratio
  measures little beyond "same article": it is not a proofreading score.

## 2. Figures

*Books 01–19, re-run 25 Sep 2026 after the analysis rule of brief §33 (earlier versions of this
table covered 01–06).*

| vol. | rows | paired | of which by fold | homonym count differs | labels: both / agree | analyses: both / ≥ 0.8 / < 0.4 | < 0.4 verbatim / fuzzy / folded | bodies: both / ≥ 0.8 / < 0.4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | 8,150 | 8,148 (100.0%) | 3 | 0 | 7,274 / **98.8%** | 5,969 / 85.1% / 1.5% | 1.6% / 0.9% / 2.7% | 7,639 / 55.4% / 9.0% |
| 02 | 7,189 | 7,189 (100.0%) | 7 | 5 | 6,354 / **99.0%** | 5,741 / 90.8% / 0.6% | 0.7% / 0.3% / 0.0% | 6,714 / 58.8% / 8.4% |
| 03 | 11,726 | 11,722 (100.0%) | 26 | 0 | 10,513 / **98.7%** | 9,198 / 90.8% / 0.8% | 0.7% / 1.0% / 2.1% | 11,092 / 66.3% / 6.7% |
| 4a | 7,524 | 7,516 (99.9%) | 5 | 0 | 6,392 / **99.0%** | 5,446 / 87.2% / 0.6% | 0.7% / 0.6% / 0.0% | 6,886 / 63.7% / 8.4% |
| 4b | 6,655 | 6,653 (100.0%) | 23 | 23 | 6,063 / **99.0%** | 5,385 / 95.4% / 0.2% | 0.2% / 0.1% / 1.5% | 6,432 / 72.3% / 6.5% |
| 05 | 8,015 | 8,010 (99.9%) | 7 | 0 | 7,031 / **99.4%** | 6,125 / 91.5% / 0.7% | 0.6% / 0.7% / 0.7% | 7,489 / 64.7% / 7.9% |
| 06 | 11,429 | 11,421 (99.9%) | 11 | 4 | 9,865 / **99.4%** | 8,806 / 90.6% / 0.4% | 0.4% / 0.5% / 0.0% | 10,499 / 65.7% / 8.0% |
| 07 | 6,877 | 6,874 (100.0%) | 10 | 0 | 6,005 / **98.9%** | 5,289 / 91.7% / 0.5% | 0.4% / 0.8% / 0.0% | 6,392 / 64.7% / 7.0% |
| 08 | 6,448 | 6,447 (100.0%) | 5 | 0 | 5,660 / **99.1%** | 4,980 / 90.4% / 0.7% | 0.6% / 0.9% / 1.1% | 5,932 / 67.9% / 6.7% |
| 09 | 6,805 | 6,804 (100.0%) | 5 | 0 | 5,851 / **98.6%** | 5,185 / 90.0% / 0.5% | 0.4% / 1.0% / 2.8% | 6,286 / 62.1% / 7.4% |
| 10 | 7,366 | 7,358 (99.9%) | 2 | 6 | 6,210 / **99.0%** | 5,474 / 90.4% / 0.5% | 0.5% / 0.7% / 0.0% | 6,679 / 62.0% / 8.1% |
| 11 | 5,663 | 5,663 (100.0%) | 2 | 0 | 4,882 / **98.5%** | 4,277 / 87.0% / 0.7% | 0.5% / 1.2% / 0.0% | 5,259 / 62.4% / 8.6% |
| 12 | 7,022 | 7,021 (100.0%) | 9 | 2 | 6,447 / **98.7%** | 5,936 / 97.3% / 0.2% | 0.3% / 0.0% / 0.0% | 6,789 / 78.3% / 6.3% |
| 13 | 7,279 | 7,279 (100.0%) | 6 | 0 | 6,097 / **99.3%** | 5,369 / 89.4% / 0.3% | 0.3% / 0.3% / 0.7% | 6,506 / 65.1% / 6.7% |
| 14 | 5,219 | 5,218 (100.0%) | 2 | 6 | 4,822 / **99.5%** | 3,715 / 96.0% / 0.2% | 0.2% / 0.2% / 0.0% | 5,039 / 67.5% / 5.7% |
| 15 | 9,342 | 9,340 (100.0%) | 8 | 1 | 8,187 / **99.4%** | 7,134 / 87.8% / 0.4% | 0.4% / 0.5% / 0.0% | 8,707 / 64.1% / 7.9% |
| 16 | 10,394 | 10,393 (100.0%) | 8 | 17 | 9,000 / **99.0%** | 7,483 / 91.0% / 0.3% | 0.2% / 0.5% / 0.9% | 9,632 / 64.0% / 8.3% |
| 17 | 6,520 | 6,514 (99.9%) | 3 | 0 | 5,526 / **98.1%** | 4,662 / 85.8% / 1.1% | 1.1% / 1.2% / 0.9% | 6,068 / 56.6% / 8.5% |
| 18 | 7,829 | 7,827 (100.0%) | 10 | 0 | 6,615 / **98.4%** | 5,660 / 83.0% / 1.0% | 0.9% / 1.2% / 3.3% | 7,219 / 56.3% / 9.4% |
| 19 | 9,251 | 9,248 (100.0%) | 16 | 0 | 8,299 / **99.2%** | 7,795 / 92.5% / 0.2% | 0.2% / 0.4% / 0.0% | 8,878 / 69.1% / 7.2% |

Columns: *paired*, index rows given a witness entry; *homonym count differs*, rows whose headword
has a different number of entries in the two; *labels*, rows where both have one, and the share
that agree; *analyses*, rows where both have one, the share ≥ 0.8 similar and the share < 0.4;
then the < 0.4 share by how the article was located (`verbatim`, `fuzzy`, `folded`).

Vol. 4/3 and its supplements (book 4c) have no witness.

## 3. What it found

- **Homonyms taken one line late.** On vol. 5 p. 63 the first index row for ကကစ carried the
  second entry's article, and the second was unlocated: the superscript ¹ was read as a glued ာ
  ("ကကစာ (ပုန) ["), which the homonym pass does not accept, since အာ is a word. The witness pairing
  showed it (label ပု against ပု၊န, analysis 0.15). `abhidhana_articles.py` now looks, for two
  identical headwords in a row with the first placed and the second not, for an entry line of the
  same headword before the first's position, with at most two characters of superscript debris.
  In vols. 1–5 it moved 50 verbatim placements (and 9 inline ones) to the earlier line, and placed
  45 headwords that had been unlocated. Of the moved and newly placed rows in the books the witness
  covers, labels agree on 67 of the 70 where both have one, and the analyses are ≥ 0.8 similar in
  51 of 60 and < 0.4 in 3.
- **Placements hold.** Analyses under 0.4 are 0.4–1.6% of verbatim placements and 0.1–1.0% of
  fuzzy ones: the fuzzy alignment does not place articles worse than the verbatim pass.
- **Labels: 511 disagreements in 60,000 pairs** where both have one (98.7–99.4% agreement per
  volume). 195 of them are (တိ) on one side and a single gender on the other, the double-labelled
  words of `docs/labels.md` §4. Then (ပု) where the witness has (ပု၊န), 31 (OCR is known to lose ၊န:
  labels.md §1); (ကြိ) against (တိ), 44 both ways; (ကြိ၊ဝိ) against (ကြိ), 13. Which side is right
  is not settled without the images.
- **The witness has a label where we read none: 7,002 rows.** It could fill them, privately,
  until §5 of `docs/witness.md` is settled; the Reader does not use it.
- **Correction to the vol. 5 report**: the witness has **7,887 of vol. 5's 7,899 distinct
  headwords (99.8%)** as the index spells them, 7,894 with the folds. The report's "7,786 (98.6%)"
  does not reproduce and was a slip. Its "labels agree 6,904 of 6,949 (99.4%)" was counted on
  distinct headwords; the join, pairing homonyms, gives 99.4% of 7,031.

## 4. Next

- Check a sample of each disagreement class on the image: (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ).
- Flag in the Reader, privately, the rows where label and analysis both disagree (10 in vols. 1–6):
  those are the likeliest misplacements left.
