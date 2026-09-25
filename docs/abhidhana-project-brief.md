# Tipiṭaka Pāḷi-Myanmā Abhidhāna — project brief

*Written 21 September 2026, at the end of the volume-25 pilot; §10–12 revised 24 September
2026, after volume 1 was done end to end and the repository was made public. Everything in
this file was measured. Do not re-derive a figure it carries; if a new one is needed,
measure it rather than estimating.*

## 1. What the work is

The Tipiṭaka Pāḷi-Myanmā Abhidhāna is a Pāḷi → Burmese dictionary in **25 volumes, bound as
29 books**, compiled by the မစိုးရိမ် (Masoeyein) Board of Scholar-Elders in Mandalay and
published by the Department for the Promotion and Propagation of the Sāsana, Ministry of
Religious Affairs, Union of Myanmar. The imprint of vol. 4 part 3 reads Sāsana 2553 /
Kawza 1372 / 2010, printed at the Ministry's own press.

The aim: digitise it, romanise the Pāḷi headwords, and render the Burmese into Spanish.

**Why it belongs beside the Nissayas project.** That project's one structurally blocked
layer is the Burmese gloss: the Pāḷi side is self-validating against OSBCT, and the gloss
side has no anchor at all — nothing validates it but Angel. A Pāḷi → Burmese dictionary of
215,447 headwords, digitised and translated, is the reference that turns gloss translation
from guessing into checking. It is not a competing project; it is the other half.

## 2. What is on disk

`~/Documents/abhidhana/` — also the working copy of the public repository
`bthar-mx/tipitaka-abhidhana` (iCloud Desktop & Documents sync is **off** on this Mac,
checked 24 Sep 2026, so a git repo here is safe).

```
pdfs/      29 PDFs, 25,700 pages, 1,012 MB — copied out of the app bundle (release asset, not in git)
db/        tipitaka_abidan.db, the app's own index (release asset, not in git)
ocr/01/    volume 1: 913 page records, articles.jsonl, ocr-report.md, articles-report.md
ocr/25/    the pilot: 466 page records (whole-page)
tools/     abhidhana_ocr.py, abhidhana_articles.py, fetch_sources.sh, create_volume_issues.sh
docs/      app-info.html (the app's provenance note), spanish-method.md, this brief
```

Source: `/Applications/Tipiṭaka/Tipitaka Abidan.app`, a Flutter app from the Mac App Store.
`docs/app-info.html` records how it was assembled: vols 1–19 from the Buddhasetaman iOS
app, vols 20–24 and 4/3 scanned by named monks of မစိုးရိမ်တိုက်သစ်, the rest from
ကမ္ဘာအေးစာကြည့်တိုက်; vol. 25 from မြင်းဝန်ကျောင်းတိုက်; the app is by Pn Daza.

**There is no text layer in these PDFs.** Vols 1–24 were produced by
`ocrmypdf 13.6.0 / Tesseract OCR-PDF 5.2.0` and vol. 25 assembled with pdftk, but
`pdffonts` reports no fonts and `pdftotext` returns nothing on every page sampled. The
layer was stripped, or never written into the copies the app ships.

## 3. The index is ground truth, and it is what makes this cheap

`db/tipitaka_abidan.db` has two tables that matter:

- `books` — 29 rows: id (text: `01`…`25`, `4a` `4b` `4c`, `14b` `14c`), the Burmese
  alphabetical range each book covers, and `start_page`.
- `words` — **221,154 rows of (headword, book, page), 215,447 of them distinct.**

**The page identity: `words.page_number + books.start_page` = the PDF page.** Verified on
vol. 1 PDF p. 300 → index p. 180, `start_page` 120; the index lists eight headwords for
that page and they are exactly the eight bold entries printed on it.

So for all 25,700 pages **the correct headwords are already known, in correct spelling,
before a pixel is read**. This is the asset the Nissayas project does not have, and it
changes what OCR has to achieve: it does not have to read the headword correctly, only well
enough to locate it.

**One anomaly, unexplained**: book 21's highest index page plus its `start_page` is 990
against 925 PDF pages. Every other book's index fits inside its PDF. Do not use book 21's
offset until this is understood.

**A second check exists and has not been used**: each volume's title page states its own
entry count. Vol. 4 part 3 says 5,163; the index holds 5,230 for that book. The 67
difference should be explained per volume before the index is called complete.

## 4. Are the pages legible? Yes

Pages read as images before any OCR: vol. 1 pp. 205, 254, 300, 700, vol. 4a p. 250 and
vol. 25 p. 400. Clean, high-contrast two-column type. Vol. 25 is the crispest; 4a has
slight degradation at the foot of a column; vol. 1 is slightly skewed on some pages and its
column rule is thin, broken, or absent (p. 254).

Every article has the same four-field shape, with unambiguous delimiters:

> **အစ္စာဝဒတိ** (ကြိ) [အတိ + အာ + ဝဒ + အ + တိ] လွန်ရှုံ့ပြောဆိုခြင်း။ … ဝိ၊၂၊၃၄၅။

headword — grammatical label in round brackets — compound analysis in square brackets —
Burmese definition — Pāḷi citations with references in Burmese numerals. A nissaya has one
separator whose convention changes per file and sometimes per run of lines; this has four
fields that never move.

## 5. The volume-25 pilot, in full

`tools/abhidhana_ocr.py`, tesseract 5 with pndaza's `myap` and tessdata_best's `myab` from
`~/Tipitaka/nissaya/tessdata`. All **466 pages** of vol. 25 — 429 carrying index entries,
37 of front and back matter — at 200 dpi, two passes (psm 6 and psm 3), union scored
against the index.

| | |
|---|---:|
| headwords in the index for this volume | 4,046 |
| **found verbatim in the OCR (union)** | **3,802 = 94.0%** |
| psm 6 alone | 88.6% |
| psm 3 alone | 82.3% |
| pages where every headword came out | 271 of 429 = **63%** |
| pages at or above 90% | 79% |
| pages at or above 80% | 92% |
| pages below 50% | 0 |

**The 244 misses are one class: long compounds.** Median length 13 Burmese characters
against 10 for headwords generally. 182 of them (75%) lie between two headwords that *were*
found, so their position on the page is bounded; of those, 104 have a ≥0.80 fuzzy match
inside that bounded span. **Verbatim or bounded-fuzzy: 3,906 / 4,046 = 96.5%.**

**200 dpi, not 300**, on vol. 25 — but see §12: dpi is per book, and on vol. 1 the native
72 beat 200.

`myab` is a distant second on this material — 37–60% against `myap`'s 55–90% on the first
probe — and is worth keeping only as a rescue pass.

## 6. The page is two columns

Recall alone cannot see this. Run whole, tesseract **interleaves the two columns**. Measured
as the longest run of headwords appearing in the order the dictionary prints them:

| | headwords found | in printed order |
|---|---:|---:|
| vol. 25, 12 pages, whole page psm 6 | 86.8% | 56.6% |
| vol. 25, 12 pages, whole page psm 3 | 85.8% | 67.0% |
| vol. 25, 12 pages, cut at the gutter | 90.6% | 79.2% |
| **vol. 1, all 763 pages, whole page psm 6** | 72.0% | **42.3%** |
| **vol. 1, all 763 pages, cut at the gutter** | 88.5% | **76.1%** |

`--columns` in `tools/abhidhana_ocr.py` does this. The vol. 25 pilot was OCR'd before it
was found and must be re-run before any article extraction.

## 7. Romanising the Pāḷi

Aksharamukha Burmese → IAST (`ṃ` normalised to OSBCT's `ṁ`). Correct on inspection:
`ဝိဟေဌယတိ` → `viheṭhayati`, `ကင်္ခါပဝတ္တိ` → `kaṅkhāpavatti`, `အခေတ္တညူ` → `akhettaññū`.

Checked against the OSBCT vocabulary — 682,010 distinct canonical words over 118 volumes,
now also kept as `ocr/osbct_vocab.txt`:

| | vol. 25 sample (4,000) | vol. 1, all 8,150 |
|---|---:|---:|
| a canonical word | 18.7% | 21.4% |
| inside a canonical word | 45.5% | 48.1% |
| neither | 35.9% | 30.5% |

The residual is not a romanisation failure: a dictionary headword is often an uninflected
lemma the canon never uses in that form, or a compound the lexicographers formed for the
entry. The Pāḷi-side self-validation is weaker than in a nissaya. Say so.

## 8. Where the OCR work should run

- **The session's cloud container**: tesseract 5.3.4; ~10 pages a minute on 2 cores for vol. 1
  (column pass + one whole-page pass, 72 dpi). A volume in 1.5–2 hours. Stage one PDF and the
  traineddata in, bring the page records back as a tarball.
- **Not the Cowork VM on the Mac**: 37 s a page, ~7× slower than native. It is not a helper.
- **Natively on a Mac, in Terminal** (Homebrew tesseract): not yet measured; this is the path for
  Winston or anyone else helping. See `RUNBOOK.md`.

## 9. The other copies: 23 volumes in Google Drive — tested, and not the better set

`https://drive.google.com/drive/folders/1ZnO5VLkJneJ8fCGzV7hvLTFTOv59BocK`, owned by
admin@iebh.org, downloaded to `pdfs-drive/` on 21 September: 23 PDFs, 20,730 pages, 972 MB,
volumes 1–21 (vol. 4 in three parts). No text layer; page images ~718 × 1071 px against the
app's ~2051 × 3061; on the four headword-densest pages of vol. 1, 69.3% against the app's
76.1%. **OCR the app's PDFs.** `pdfs-drive/` is a fallback for a damaged page; its
pagination differs from the app's in several books (4b, VII, VIII, XVII–XXI), so check the
offset per volume before using it.

## 10. Publication (decided 24 September 2026)

**Angel's decision: publish.** The volumes are freely distributed in several places for free
distribution, and IEBH will not treat the licence as a blocker. The project is now a
**public** repository, `bthar-mx/tipitaka-abhidhana`. What follows from that:

- **Credit, not ownership.** The dictionary text belongs to the Masoeyein Board of Scholar-Elders and
  the Ministry. The scans belong to the people named in `docs/app-info.html`: the Buddhasetaman group,
  the monks of မစိုးရိမ်တိုက်သစ်, the Kaba-Aye library, the Myinwun monastery, and Pn Daza, who built
  the app and the `myap` OCR model. The README credits all of them by name. Monks' names are given in
  Burmese as the app prints them, until a Burmese reader has romanised them.
- **Licences are split.** Code under MIT. What the project adds (structure, romanisations, reports,
  Spanish) under CC BY-SA 4.0. The OCR'd Burmese is not relicensed.
- **Status is carried on the data itself.** Every row says `ocr`, `drafted`, `reviewed` or `corrected`. Being
  public makes this matter more, not less.
- **PDFs and the index are release assets** (`sources-v1`), not files in git. `pdfs/SHA256SUMS` and
  `db/SHA256SUMS` are in the repo, and `tools/fetch_sources.sh` downloads and checks them.

## 11. What has not been done (revised 24 September 2026)

- Vol. 25 pilot is still whole-page. Re-run with `--columns` at its native resolution.
- ~~Labels are not normalised; the unlocated 13% not recovered.~~ Done 24 Sep (§12, `docs/labels.md`).
- The typed PCED copy of this dictionary (`docs/labels.md` §4) is not yet converted from Zawgyi or used.
- ~~Vol. 3 is not yet spot-checked; the Reader does not show vols. 2–3.~~ Done 25 Sep (§13).
- Citations are parsed but not resolved against OSBCT.
- No Spanish exists beyond the drafted sample in `docs/spanish-method.md`.
- Book 21's offset and the per-volume entry counts are unchecked.
- Nothing whatever has been reviewed by a Burmese reader.

## 12. Volume 1, end to end (24 September 2026)

913 pages, 8,150 index headwords, OCR'd in the cloud container in about 2 hours (2 cores,
~10 pages a minute). Full figures are in `ocr/01/ocr-report.md` and `ocr/01/articles-report.md`.

| | |
|---|---:|
| headwords verbatim, column pass + whole-page psm 6 | **92.0%** |
| column pass alone | 88.5% |
| **in printed order, column pass** | **76.1%** (whole-page: 42.3%) |
| pages with every headword | 53.5% |
| pages ≥ 80% | 90.0% |
| articles located in the text | 87.0% → **94.1%** (24 Sep) |
| articles with label + body | 80.3% → **87.7%** (normalised label) |
| compound analysis recovered | 68.6% → 72.0% |
| at least one citation parsed | 57.2% → 60.8% |
| labels agreeing with the typed PCED witness | 81.2% raw → **99.0%** of those normalised |
| headwords attested in OSBCT, whole or inside | 69.5% |

**Three things vol. 1 taught that the pilot could not:**

1. **DPI is per book.** Vol. 1's pages are declared 2014 × 3142 pt, so the 1-bit scan sits at 72 ppi.
   `-r 200` upsampled it 2.8×, and that *cost* recall: 87.8% against 92.1% at native, on 15 pages,
   and it was 2.6× slower. Check `pdfimages -list` before choosing, every book.
2. **Some pages have no printed rule.** On 14 indexed pages the darkest-column finder landed at
   0.56–0.61, inside the right column. The gutter is now accepted only inside 0.44–0.555 of the
   width; outside that range the cut goes in the white channel between the columns. Re-reading
   those pages gained 22 headwords. A "3× median ink" test was tried and dropped, because it rejected
   the faint rule on ~120 good pages.
3. **The Cowork VM on the Mac is useless for tesseract.** It took 37 s a page, against ~5 s natively in
   the container. Anyone helping (e.g. Winston) must run natively in Terminal; see `RUNBOOK.md`.

**Known weaknesses of the article layer**, from a spot check of p. 300 against the image:
labels were read, not normalised, and `+` in the analysis came out as ၂. All three were fixed on
24 Sep: `normalise_analysis` for the + signs; the label map (`docs/labels.md`: 125 readings → 19
printed labels, image-checked, 98.5% agreement with the typed witness); and an ordered alignment
of the headwords between placed neighbours, which cut unlocated articles from 13.0% to 6.2%.

**A typed copy exists.** Pali Canon E-Dictionary 1.94, the data behind dictionary.sutta.org, holds
this dictionary as its "Tipiṭaka Pāḷi-Myanmar Dictionary" (157,271 entries, Zawgyi encoding,
repo `siongui/data`). It has 94.7% of vol. 1's headwords, and gives the label, analysis and
definition but apparently not the quotations. It is the Burmese side's first witness other than
Angel.

## 13. Volumes 2 and 3 (24 September 2026)

Both were OCR'd natively on Angel's Mac, at about 45 pages a minute with 10 workers. That makes
the Mac, not the container, the place to run volumes. The full figures are in `ocr/0N/*-report.md`.

| | vol. 1 | vol. 2 | vol. 3 |
|---|---:|---:|---:|
| PDF pages / index headwords | 913 / 8,150 | 898 / 7,189 | 1,177 / 11,726 |
| dpi (native) | 72 | 72 | 75 |
| headwords verbatim, either pass | 92.0% | 92.7% (92.9% with the page fix) | 92.9% |
| in printed order, column pass | 76.1% | 75.5% | 77.3% |
| articles located | 94.1% | 93.5% | 94.6% |
| normalised label + body | 87.7% | 87.1% | 88.5% |
| labels agreeing with the typed witness (of those normalised) | 99.0% | 99.2% | 98.8% |
| typed witness has the headword | 94.7% | 96.0% | 94.5% |

**What they added to the method.**
- **Scans can be bound out of order.** In vol. 2, PDF pp. 241/242 are printed pp. 224/223.
  `PAGE_FIX` in `abhidhana_articles.py` records such cases per book. To find them, test each page
  scoring below 50% against its neighbours' index lists; vol. 3 has none.
- **Spelling-variant entries**, e.g. အနုပါဒိဏ္ဏ(န္န)ကဇာတိ, are one printed article for two index
  headwords. Both spellings are read, and the second headword shares the article (`variant_of`).
- **Pages the index skips** (22 in vol. 1, 24 in vol. 2, 43 in vol. 3) lie inside a long article
  and are now read into it (`runs_through`).
- **Placements checked without images.** Against the typed witness, the analysis we read disagrees
  (similarity < 0.4) about as often for fuzzy placements as for verbatim ones: 5.7 vs 5.5%, 3.7 vs
  2.9%, and 3.6 vs 2.1% in vols. 1–3. A misplaced article would carry a neighbour's analysis.
- **Image spot checks, vol. 2.** P. 500: 11 of 11 placed right. Pp. 241–242: 15 of 15. P. 115 (the
  variant page, the worst): 7 right, 1 wrong, 6 unlocated.
- **Image spot checks, vol. 3** (25 Sep). P. 600: 13 of 14 at the right entry, 1 unlocated (a variant
  twin). P. 654, the "worst page": 4 of 4 right. P. 1008: 13 of 13. No wrong entry and no wrong label
  on the three pages; 2 labels not read.
- **The print writes ာ where the index writes ါ, after a stacked consonant** (အလမ္ပာန as printed, အလမ္ပါန
  in the index). That, not the OCR, is why p. 654 scored 0 of 4. Of the headwords with a stacked
  consonant + ါ that recall missed, 1 of 17 (vol. 1), 6 of 26 (vol. 2) and 26 of 48 (vol. 3) are
  present verbatim with ာ. Folding the two when matching is not yet implemented. A stacked ဖ read as ဗ
  (အသမ္ဖ…) is the other cause on pp. 1007–1009.
- **The Reader shows vols. 1–3** with a volume switch (25 Sep); `#v03p654` links to a page.
