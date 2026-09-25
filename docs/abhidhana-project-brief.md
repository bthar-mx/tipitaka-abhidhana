# Tipiṭaka Pāḷi-Myanmā Abhidhāna — project brief

*Written 21 September 2026, at the end of the volume-25 pilot; §10–12 revised 24 September
2026, after volume 1 was done end to end and the repository was made public; §18–21 added
25 September 2026 (spelling folds, the witness join, vols. 6 and 7). Everything in
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
- ~~The typed PCED copy is not yet converted from Zawgyi.~~ Converted 25 Sep (§14, `docs/witness.md`); joined to the articles 25 Sep (§19).
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

## 14. 25 September 2026: the witness, short headwords, vol. 4/1

**The typed witness is in Unicode** (`docs/witness.md`, `tools/abhidhana_witness.py`,
`tools/zawgyi.py`; output `witness/pced_k.jsonl`, gitignored). python-myanmar's converter needed
seven corrections, each found against the index. After them, **99.4%** of the witness's 153,529
distinct headwords are index headwords letter for letter. It covers **99.8%** of the headwords of
books 01–19 with 4a and 4b, and nothing of 4c, 14b, 14c or 20–25. The 94.5–96.0% per volume in §13
matched on the romanised key and is superseded. On vol. 3 pp. 600 and 1008 its labels (25/25) and
analyses (25/25) agree with the print, its definitions word for word in 24 of 25 (one typing
omission in the source). It omits the Pāḷi quotations and glosses and lightly modernises (တစ် for
တ). Its licence is not stated: nothing derived from it is published.

**Short headwords and homonyms.** A homonym's superscript is read as debris glued to the headword
(အါ, အဝ်, အည”, အမူလကာါ). A last pass in `abhidhana_articles.py` now places such heads, and a one-
or two-character headword on a line of its own, only for headwords still unplaced and only
between placed neighbours. It moved no earlier placement: located +11 / +1 / +7 in vols. 1–3
(vol. 1 94.1% → 94.2%), including the five entries for အ on pp. 121–122. Tried inside the verbatim
pass, it had let a homonym's first entry take the second's line; that version was discarded.
`abhidhana_articles.py` also no longer overwrites the hand-written notes of `articles-report.md`
(it did, and they were restored from GitHub).

**Vol. 4/1 (book 4a)**, OCR'd natively by Angel at 96 dpi (native):

| | vol. 4/1 | vol. 3 |
|---|---:|---:|
| PDF pages / index headwords | 863 / 7,524 | 1,177 / 11,726 |
| headwords verbatim, either pass | 88.9% | 92.9% |
| in printed order, column pass | 73.1% | 77.3% |
| articles located | 92.1% | 94.6% |
| normalised label + body | 83.8% (85.0% after §15) | 88.5% |

The shortfall is the last 160 pages, a scan of worn print (pp. 700–863: recall 79.2%, located 89.0%;
pp. 1–699: 91.5%, 92.9%), and one glyph, the stacked ဆ of ဉ္ဆ, read as ဉ္စ. Spot check (pp. 300,
478, 786): 36 of 40 at the right entry, none wrong, 4 unlocated; no label wrong, 5 not read.
No page is out of order.

**The Reader** covers vols. 1, 2, 3 and 4/1, and its search runs across all of them
(`reader/search.json`, built by `abhidhana_reader_data.py`).

## 15. Vol. 4/2 (book 4b), and labels with a lost bracket (25 September 2026, later)

**Labels with a lost bracket.** "(ကြို [" and "ထီ) [" — a label whose ( or ) was lost, with the [
of the analysis after it — are now read when the reading is in the label map
(`label_bracket_damaged`), and two image-checked readings were added (ထံ၊န → ထီ၊န, ကမ္ပကြိ →
ကမ္မ၊ကြိ). Gains: 88 / 91 / 119 / 86 / 314 labels in vols. 1, 2, 3, 4/1, 4/2; no label already read
changed. Against the typed witness, 671 of the 694 new labels it has agree (96.7%), against about
99% for the others.

**Vol. 4/2** (681 PDF pages, 6,655 headwords, 72 dpi) is the best book so far. It is set in a
cleaner typeface.

| | vol. 1 | vol. 2 | vol. 3 | vol. 4/1 | vol. 4/2 |
|---|---:|---:|---:|---:|---:|
| headwords verbatim, either pass | 92.0% | 92.7% | 92.9% | 88.9% | 93.3% |
| in printed order, column pass | 76.1% | 75.5% | 77.3% | 73.1% | 76.0% |
| articles located | 94.2% | 93.5% | 94.7% | 92.1% | **96.6%** |
| normalised label + body | 88.9% | 88.4% | 89.6% | 85.0% | **90.8%** |

Its worst page (p. 74, 0 of 7) is the index writing ဉာ where 4b prints ညာ (ဥဒယဗ္ဗယညာဏ…); the
OCR is right, and all 7 are placed right. Spot check (pp. 300, 74, 416): 33 of 35 at the right
entry, none wrong, 2 unlocated; no label wrong, 1 not read. One index typo found
(ဥဒယဗ္ဗကဉာကပဋိပါဋိ for ဥဒယဗ္ဗယညာဏပဋိပါဋိ).

**Print and index spell differently in three ways now**, each invisible to recall: ါ/ာ after a
stacked consonant (vols. 3, 4/2), ဉာ/ညာ (vol. 4/2), and the index's own typos. Folding the first
two when matching is item 3 in NEXT-SESSION.

## 16. Vol. 4/3 (book 4c) and its supplements (25 September 2026, night)

**4c's PDF is vol. 4/3 plus three supplements.** PDF pp. 713–735 are "entries added to" vols. 15
(ဘိဇ္ဇ…, 53 headwords), 4/2 (ဥဒဝါ…ဥဠုဂ္ဂဟယုဒ္ဓ, 114) and 16 (မံသကာရဏ…မောဟိတဗ္ဗ, 56), each so
headed in print. The index files all 223 under book 4c (index pp. 686–708). Vol. 4/3 itself has
5,007 index headwords. The title page's 5,163 (§3) matches neither 5,007 nor 5,230: the "67" of §3
was a coincidence of this sum, and the difference is still unexplained. **The supplement to vol. 15
is the only place its 53 ဘိဇ္ဇ headwords are indexed**; when vol. 15 is done, they belong beside it.

| | vol. 4/3 (all) | vol. 4/3 itself | the supplements |
|---|---:|---:|---:|
| index headwords | 5,230 | 5,007 | 223 |
| headwords verbatim, either pass | 90.5% | 90.7% | 86.1% |
| in printed order, column pass | 72.3% | | |
| articles located | 92.2% | 92.2% | 92.8% |
| normalised label + body | 86.4% | 86.3% | 89.2% |

Rendered at 72 dpi (pages are 69–73 ppi). **No typed witness** covers it. Spot check (pp. 300, 615,
721): 28 of 32 index headwords at the right entry (not counting the ten filed on the wrong page),
none wrong; no label wrong, 1 not read.

**The index is least reliable here.** On three pages: ten headwords filed two pages late (p. 615,
ids 176418–176427), four typos (ဩလမ္ဗတကုလာဝက, ဥဒါနိ, ဥပါဃာတဘူမိ, စကစတုက္ကာဒိကဆတ္တိက), a variant
entry split into bare ဧဏိ / ဧဏီ, and one headword (ဥပက္ကိလေသ) with no printed entry. The index is
still the authority for *which* headwords there are, but not for their spelling or their page.

## 17. Vol. 5 (25 September 2026, late)

883 PDF pages, 8,015 index headwords, 72 dpi. The typed witness covers it.

| | vol. 5 |
|---|---:|
| headwords verbatim, either pass | 90.2% |
| in printed order, column pass | 74.6% |
| articles located | 93.4% (29.1% by fuzzy match, the highest share so far) |
| normalised label + body | 87.6% |
| labels agreeing with the typed witness | 99.4% (6,904 / 6,949) |
| witness has the headword | 98.6% |

**Three stacked-letter confusions account for most misses here**: ဉ္ဇ read ဉ္စ (27 of 47 missed
headwords with ဉ္ဇ), ဏ္ဌ read ဏ္ဍ/ဏ္ဏ (20 of 20), ဋ read ဌ/ဠ (14 of 141). The ဉ္ဇ confusion is in
every book from vol. 3 on. A table of such confusions, used when matching, would join the ါ/ာ and
ဉာ/ညာ folds (NEXT-SESSION item 3). Spot check (pp. 500, 106, 142): 30 of 36 at the right entry,
none wrong, 6 unlocated; no label wrong, 1 not read. One more index typo: ကဉ္စိက for ကဉ္ဇိက.

*Correction (§19):* the vol. 5 report said the witness has 7,786 of 7,899 distinct headwords
(98.6%). Measured again it is **7,887 (99.8%)**; the earlier figure does not reproduce.

## 18. Spelling folds, homonyms placed late, headwords filed on the wrong page (25 September 2026)

**Folds.** `tools/abhidhana_fold.py` folds, one character for one, the spellings print, index and
OCR disagree on: ါ→ာ, ဉ→ည, ဌ ဠ→ဋ, ည္ဇ ည္ဆ→ည္စ, ဏ္ဍ ဏ္ဏ→ဏ္ဋ. It is used for matching only; nothing
folded is written out. Recall with the folds, over the page records:

| | 01 | 02 | 03 | 4a | 4b | 4c | 05 | 06 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| verbatim | 92.0% | 92.7% | 92.9% | 88.9% | 93.3% | 90.5% | 90.2% | 92.4% |
| with the folds | 92.4% | 93.0% | 93.5% | 89.6% | 94.0% | 90.8% | 91.4% | 93.1% |

`abhidhana_ocr.py` now records `union_folded` per page and prints both. In `abhidhana_articles.py`
the folded search runs **after** the fuzzy alignment, for headwords still unplaced, rank 2 or better
between placed neighbours. Run before it, it moved three placements in vol. 5, two of them wrongly
(a quotation line; a cross-reference "ကာသာဝကဏ္ဍ (ခ) ကြည့်"), so that version was dropped. A fuzzy
placement whose line begins with the folded headword is relabelled `folded` (868 in vols. 1–5). It
gains little on its own (15 articles in vols. 1–5): the fuzzy alignment had already placed most.

**Homonyms taken one entry late.** Found through the witness (§19): when a homonym's superscript
is read as a glued ာ ("ကကစာ (ပုန) [", vol. 5 p. 63), the verbatim pass gave the first index row the
second entry's line and left the second unplaced. For two identical headwords in a row, the first
placed and the second not, an entry line of the headword before the first's position, with at
most two characters of superscript debris (ာ ါ, a quote mark, a digit), now takes the first; the
second moves to the first's old line. In vols. 1–5: 50 verbatim placements moved, 9 inline ones,
45 unlocated headwords placed. The witness agrees with 67 of 70 of their labels; their analyses
are ≥ 0.8 similar in 51 of 60, < 0.4 in 3. (A version allowing any two characters also moved
ကတတ္တ onto the line of ကတတ္တံ and was narrowed.)

**Headwords filed on the wrong page.** `ID_PAGE_FIX` reads an id range on the page it is printed on,
keeping `index_page` and marking `index_misfiled`. Two runs, found as unindexed pages inside the
body whose entries begin with a neighbour's unlocated headwords (no other case in vols. 3, 4/3, 5):
4c ids 176418–176427 (indexed p. 615, printed p. 613: 9 of 10 now placed) and 06 ids 58264–58277
(indexed p. 851, printed p. 852: 14 of 14, image-checked).

**A label lost.** (ကာ၊ကြိ၊ဝိ), the causative absolutive, fell to the junk-tail rule and was cut to
(ကာ၊ကြိ): 35 rows in vols. 3–6. Now in the label map (`docs/labels.md` §7; image, vol. 6 p. 852).

Articles now, every volume re-run with all of the above:

| | 01 | 02 | 03 | 4a | 4b | 4c | 05 | 06 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| located | 94.4% | 93.6% | 94.8% | 92.2% | 96.7% | 92.5% | 93.6% | 92.0% |
| label + body | 89.0% | 88.4% | 89.6% | 85.0% | 91.1% | 86.8% | 87.7% | 86.3% |

## 19. The witness joined to the articles (25 September 2026)

`tools/abhidhana_witness_join.py`, `docs/witness-join.md`; per-article output in the gitignored
`witness/join-NN.jsonl`. Homonyms are paired in order, all books at once; the headword is looked up
as the index spells it, then folded. Analyses are compared on their first clause (to ။): the
witness's analysis field, like the print's bracket, runs on into the grammarians' derivation.

| | 01 | 02 | 03 | 4a | 4b | 05 | 06 |
|---|---:|---:|---:|---:|---:|---:|---:|
| index rows paired | 100.0% | 100.0% | 100.0% | 99.9% | 100.0% | 99.9% | 99.9% |
| labels agree (where both have one) | 98.8% | 99.0% | 98.7% | 99.0% | 99.0% | 99.4% | 99.4% |
| analyses ≥ 0.8 similar | 85.0% | 90.8% | 90.8% | 87.2% | 95.4% | 91.6% | 90.6% |
| analyses < 0.4 | 1.5% | 0.6% | 0.8% | 0.6% | 0.2% | 0.6% | 0.4% |

These supersede the label agreements of §12–17, which counted distinct headwords. Analyses under
0.4 are no commoner for fuzzy placements (0.1–1.0%) than for verbatim ones (0.2–1.6%). The 511 label
disagreements are mostly (တိ) against a single gender (195), (ပု) against (ပု၊န) (31) and (ကြိ)
against (တိ) (44); which side is right is not checked. The witness has a label for 7,002 rows where
we read none. The body ratio (the witness omits quotations) says little and is not a proofreading
score. Nothing of the witness's text is published.

## 20. Vol. 6 (25 September 2026)

1,039 PDF pages, 11,429 index headwords (11,232 distinct), 75 dpi (images 74–77 ppi), OCR'd
natively on Angel's Mac. `ocr/06/ocr-report.md`, `ocr/06/articles-report.md`.

| | vol. 6 |
|---|---:|
| headwords verbatim, either pass (with the folds) | 92.4% (93.1%) |
| in printed order, column pass | 75.3% |
| pages with every headword / ≥ 80% / < 50% | 48.3% / 92.3% / 4 |
| articles located | 92.0% |
| normalised label + body | 86.3% |
| witness has the headword (distinct) | 99.8% |
| labels agreeing with the witness | 99.4% |

No page is bound out of order. **The index files 14 headwords of p. 852 under p. 851** (§18).
Spot check (pp. 500, 110, 852): 43 of 46 at the right entry, none wrong, 3 unlocated; one label
wrong (ဂါဟေတွာ, the lost ၊ဝိ, since fixed). Located is below vols. 3 and 5; 710 of the 915
unlocated are in the page text but not at an entry's head, which is where the `page.psm6`
fallback (NEXT-SESSION, open questions) would be tried.

**The Reader** now has vols. 1–6. Its data are published gzipped and base64-encoded
(`reader/*.gz.txt`, 21.7 MB for eight books): as plain JSON they passed the artifact's 64 MB per
version, and artifacts do not serve `.gz`. The page inflates them with `DecompressionStream`,
which needs a 2023-or-later browser.

## 21. Vol. 7 (25 September 2026)

861 PDF pages, 6,877 index headwords (6,702 distinct), 72 dpi, OCR'd natively on Angel's Mac.
`ocr/07/ocr-report.md`, `ocr/07/articles-report.md`.

| | vol. 7 |
|---|---:|
| headwords verbatim, either pass (with the folds) | 91.5% (91.9%) |
| in printed order, column pass | 73.8% |
| pages with every headword / ≥ 80% / < 50% | 50.4% / 88.7% / 3 |
| articles located | 93.1% |
| normalised label + body | 87.3% |
| witness has the headword (distinct) | 99.8% |
| labels agreeing with the witness | 98.9% |

No page out of order, no misfiled headwords. Spot check (pp. 400, 759, 527): 28 of 35 at the right
entry, none wrong, 5 unlocated, 2 placed inside garbled text; no label wrong, 2 not read.

**Two new failure modes.** (1) ဒွ read as ဒ္ဒ: the run ဆဒွါရ… on p. 759, 14 headwords, all missed by
recall and all placed right by the fuzzy alignment. Not a one-for-one fold, so not in
`abhidhana_fold.py`. (2) A gutter taken inside the accepted range but left of the channel
(p. 527, 0.467): the right column came out as interleaved fragments. Pages where the whole-page
pass reads ≥ 3 headwords more than the column pass are the candidates: 9 in vol. 7, 23 in vol. 6.

