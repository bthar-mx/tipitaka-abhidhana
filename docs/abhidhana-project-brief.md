# Tipiṭaka Pāḷi-Myanmā Abhidhāna — project brief

*Written 21 September 2026, at the end of the volume-25 pilot; §10–12 revised 24 September
2026, after volume 1 was done end to end and the repository was made public; §18–26 added
25 September 2026 (spelling folds, the witness join, vols. 6–9, re-cutting gutters, vol. 14/2's text layer, the batch of vols. 10–22); §27 the same evening (vols. 23, 24 and 14/2 finished, the index's page errors applied, book 21 explained, the Reader in binary); §28 the public website, the page images and the label table; §29 vol. 21 finished, vol. 25's resolution, the dictionary's own account of its labels; §30 vol. 25 done, all 29 books; §31 (later on 25 Sep) the page-image tool's bitmap test; §32 the weak page corrections, image-checked; §33 the compound analysis with its [ lost; §34 the dictionary's history on the site; §35 all page images live, a light/dark switch, the Introduction page; §36 citations keep their whole abbreviation; §37 translation, batch 1; §38–41 (26 Sep) the redesign, vol. 1–2 drafts, PCED analyses, versioned assets; §42 (27 Sep) the live check, vol. 3's drafts, version numbers; §43 vols. 4/1–4/2 drafts, the IEBH footer, citation tooltips, cross-reference links, labels reviewed. Everything in
this file was measured. Do not re-derive a figure it carries; if a new one is needed,
measure it rather than estimating.*

## 1. What the work is

The Tipiṭaka Pāḷi-Myanmā Abhidhāna is a Pāḷi → Burmese dictionary in **25 volumes, bound as
29 books**, compiled from the 1950s to 2023 by five teams of scholar-monks among which the
alphabet was divided — the Masoeyein (မစိုးရိမ်) monastery in Mandalay wrote vols. 5–6 and 15–16
(vol. 17, pp. 6–7; `docs/history.md`; *corrected 25 Sep 2026: this line used to credit the whole
work to the Masoeyein board*) — and published by the Union of Burma Buddha Sāsana Council (vol. 1,
1964), then by the Department for the Promotion and Propagation of the Sāsana, Ministry of
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

**Book 21's anomaly, explained 25 Sep 2026 (§27)**: its highest index page plus its
`start_page` is 990 against 925 PDF pages, but only because ten headwords carry p. 962 for 692.
The offset holds; `ID_PAGE_FIX` corrects the ten.

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

- Vol. 25 pilot is still whole-page. Re-run with `--columns` at its native resolution (300 ppi); the pilot's pages were moved to `tmp/ocr-25-pilot-pages` on 25 Sep (§27).
- ~~Labels are not normalised; the unlocated 13% not recovered.~~ Done 24 Sep (§12, `docs/labels.md`).
- ~~The typed PCED copy is not yet converted from Zawgyi.~~ Converted 25 Sep (§14, `docs/witness.md`); joined to the articles 25 Sep (§19).
- ~~Vol. 3 is not yet spot-checked; the Reader does not show vols. 2–3.~~ Done 25 Sep (§13).
- Citations are parsed but not resolved against OSBCT.
- No Spanish exists beyond the drafted sample in `docs/spanish-method.md`.
- ~~Book 21's offset~~ explained 25 Sep (§27). The per-volume entry counts are unchecked.
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

## 22. Vol. 8, and gutters cut inside the right column (25 September 2026)

849 PDF pages, 6,448 index headwords (6,262 distinct), rendered at 72 dpi (images mixed, 57–72
ppi; the low ones are front matter). `ocr/08/ocr-report.md`, `ocr/08/articles-report.md`.

| | vol. 8 |
|---|---:|
| headwords verbatim, either pass (with the folds) | 91.5% (92.2%) |
| in printed order, column pass | 75.2% |
| pages with every headword / ≥ 80% / < 50% | 58.2% / 86.6% / 13 |
| articles located | 92.1% |
| normalised label + body | 87.7% |
| witness has the headword (distinct) | 99.9% |
| labels agreeing with the witness | 99.1% |

No page out of order, no misfiled headwords. The ဍ section (pp. 804–818) is weak: a headword's
bold ဍ is read as ဒ, and short forms fall below the fuzzy threshold.

Spot check (pp. 500, 810, 413): 13 of 28 at the right entry, **1 wrong**, 14 unlocated; no label
wrong, 3 not read. The wrong one (ဇေဋ္ဌရာဇ, p. 500, placed at the analysis of ဇေဋ္ဌရာဇဓီတု¹) is the
first in a spot check since vol. 2, and it comes from the gutter.

**Gutters at the upper edge.** The accepted range 0.44–0.555 is too wide on the right. On p. 500
the cut at 0.554 ran through the right column's first letters, and every head there lost its
opening syllable. Column-pass recall on pages whose gutter is ≥ 0.54, against the rest of the book:

| | vol. 2 | vol. 3 | vol. 6 | vol. 8 |
|---|---:|---:|---:|---:|
| pages ≥ 0.54 | 19 | 24 | 25 | 10 |
| their column recall | 74.3% | 89.2% | 78.5% | 68.6% |
| the rest | 88.0% | 88.4% | 87.7% | 87.6% |

Vols. 1, 4/2, 5 and 7 have none, 4/1 and 4/3 one each. Vol. 3's are unaffected, so a high value is
not wrong by itself; where the rule is printed off-centre, it is right. The fix is to check the
cut, not to narrow the range: a cut that leaves many of the right column's lines starting with a
dependent vowel or medial (U+102B–103E) has gone through the letters. Vol. 7 p. 527 (0.467,
brief §21) is the same failure on the left.

## 23. Vol. 9 (25 September 2026)

893 PDF pages, 6,805 index headwords (6,652 distinct), 75 dpi. `ocr/09/ocr-report.md`,
`ocr/09/articles-report.md`.

| | vol. 9 |
|---|---:|
| headwords verbatim, either pass (with the folds) | 89.5% (90.1%) |
| in printed order, column pass | 73.8% |
| pages with every headword / ≥ 80% / < 50% | 51.6% / 84.5% / 8 |
| articles located | 92.5% |
| normalised label + body | 86.0% |
| witness has the headword (distinct) | 99.9% |
| labels agreeing with the witness | 98.6% |

No page out of order, no misfiled headwords. The print sets the anusvāra of ိံ apart (တာဝတိ˙သ), which
recall misses and the fuzzy alignment mostly recovers. Spot check (pp. 500, 422, 823): 21 of 35 at the
right entry, none wrong, 14 unlocated, 12 of them on p. 823.

**P. 823 was a failed reading.** A clean page, read on the Mac as fragments in both passes (1 and 3
of 12); the same code on the same page in the cloud container read 11 of 12. The cause is unknown.
Other pages under 30% (vol. 8 pp. 112, 413, 718, 806, 807, 810; vol. 9 pp. 422, 423, 436, 437) re-read
there came out as before, so such failures are rare; p. 823 is the one found.

## 24. Re-cutting gutters: `tools/abhidhana_recut.py` (25 September 2026)

A separate tool, so that `abhidhana_ocr.py` need not change while a book is being read. It finds
the column channel with a **band count**: the page (rows 12–95%) is split into 100 horizontal
bands, and a pixel column is white if it carries ink in at most one. A mean over the whole height
cannot tell the gutter from the hanging indent of the right-hand column, which only the headwords
cross; a band count can. White runs between 0.40 and 0.60 of the width, separated only by a rule
(≤ 1.5%), form the channel. A page is flagged when either edge of its old crops (cut ± 8 px) is
not white: *cut through text*, or *rule in a crop*.

**Vol. 8, all 687 indexed pages scanned** (in the cloud container): ok 288, rule in a crop 368,
cut through text 25, no channel 6. Vol. 8 p. 329 is an example recall cannot see: cut at 0.448,
inside the left column, it read 8 of 8 headwords, because the headwords sit at the line starts
and only the ends of the left column's lines went to the wrong image.

**Re-read, 37 vol. 8 pages** (cloud container, tesseract 5.3.4):

| | pages | column recall before | after | worse on |
|---|---:|---:|---:|---:|
| cut through text | 25 | 78.4% | 88.9% | 4 |
| rule in a crop (a sample) | 12 | 87.6% | 86.5% | 2 |

So `--run` re-reads only pages cut through text, and keeps a new reading only when it finds at
least as many headwords as the old one (the rejected cut is recorded as `_cut_rejected`). That
choice between two readings of a page uses the index, as the rest of the pipeline does. These
cloud readings are not in the folder: the re-run is to be done natively, for consistency with the
rest of the OCR. After it, each book's articles, romanisation, witness join and Reader are re-run.

## 25. Vol. 14/2 (book 14b) is text, not a scan (25 September 2026)

Found by Angel: 14b.pdf is typeset text in the legacy WinInnwa font family (WinResearcher,
WinHaka, WinPinya, …), 480 × 713 pt pages, made by iText. `tools/abhidhana_winburmese.py` reads the
text layer (pymupdf), converts it with python-myanmar's `wininnwa` converter plus the corrections
listed in `ocr/14b/extract-report.md` (ဝ versus the digit ၀, which share one code; stacked ta under
na; truncated ligatures; marks in drawing order; marks set as separate spans; punctuation glyphs
identified on the page image), and writes page records in the OCR records' shape, `source: "text
layer"`, so the rest of the pipeline runs on them unchanged.

| | vol. 14/2, text layer |
|---|---:|
| index headwords verbatim | 93.7% |
| with the folds, and variants printed inside a headword | 96.6% |
| pages with every headword | 73.3% |
| articles located (a trial run in the cloud container, not in the folder) | 98.2% |
| normalised label + body (same trial) | 97.5% |

The misses are print against index, not conversion: this book's index was typed separately and
has more typos (ပရတီိိရ, ဇ္စျ for ဇ္ဈ) and headwords filed on a neighbouring page. Checked against the
image on p. 300: word for word. No typed witness covers the book; the text layer is its text.
(ကာ၊ကမ္မ၊ကြိ) occurs 7 times, cleanly: a label to add to the map (the witness prints it 43 times).

**Vol. 23** is scanned at about 323 ppi on A4 pages (Angel); `tools/run_volumes.sh` renders it at that.

## 26. Vols. 10–20 and 22: Angel's batch (25 September 2026)

`tools/run_volumes.sh` (written by the other chat) ran OCR, articles and romanisation for one book
after another, natively, 09:20–13:14 for these (vol. 21 skipped by rule, 14/2 not a scan, 23 and 24
after). Reports in `ocr/NN/`, the Reader has them all.

| vol. | PDF pages | index headwords | dpi | verbatim (folded) | in order | located | label + body |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 | 981 | 7,366 | 75 | 90.1% (90.3%) | 74.0% | 90.8% | 84.3% |
| 11 | 769 | 5,663 | 72 | 89.1% (89.5%) | 74.7% | 93.0% | 86.2% |
| 12 | 1,123 | 7,022 | 72 | 94.0% (94.5%) | 77.9% | 96.9% | 91.7% |
| 13 | 896 | 7,279 | 73 | 85.8% (86.3%) | 70.9% | 89.5% | 83.7% |
| 14/1 | 821 | 5,219 | 70 | 93.8% (94.3%) | 77.0% | 96.6% | 92.3% |
| 14/3 | 1,107 | 10,390 | 72 | 91.9% (92.2%) | 75.7% | 91.1% | 84.8% |
| 15 | 853 | 9,342 | 74 | 91.0% (91.3%) | 76.2% | 93.4% | 87.6% |
| 16 | 890 | 10,394 | 73 | 88.7% (89.4%) | 75.5% | 92.8% | 86.6% |
| 17 | 879 | 6,520 | 69 | 91.3% (91.7%) | 75.2% | 93.4% | 84.9% |
| 18 | 890 | 7,829 | 72 | 89.2% (89.9%) | 74.3% | 92.4% | 84.4% |
| 19 | 982 | 9,251 | 72 | 96.3% (96.6%) | 78.5% | 96.3% | 89.5% |
| 20 | 945 | 7,366 | 72 | 91.5% (91.7%) | 76.6% | 95.7% | 87.1% |
| 22 | 933 | 8,075 | 72 | 88.5% (90.4%) | 80.6% | 95.1% | 89.0% |

Against the typed witnesses (vols. 10–19): labels agree on 98.1–99.5%, and Pn Daza's page-referenced
copy supplies a typed text for 175–767 unplaced articles per book. **Spot checks this time are one
page per book**: on the image for the three books no witness covers (14/3 p. 580: 9 of 10 right, 1
unlocated; 20 p. 465: 12 of 12; 22 p. 419: 9 of 9), and in the text and against the witness for the
rest (every placed row right, every label as the witness). No wrong placement was found.

**What the batch turned up**
- **Vol. 13: the index files vol. 15's ဗ headwords under vol. 13.** Index pages 145–160 of book 13
  (PDF pp. 175–190) list 232 ဗ headwords (ဗလိ … ဗဟိဒ္ဓါသမုဋ္ဌာန) for pages that print ပဂ္ဂဏှာထ … ပဂ္ဃရဏ-
  လက္ခဏ. Pn Daza's typed text has the same ဗ entries under vol. 13 pp. 145–160: the error is in the
  typing the index was built from (§4 of `docs/witness-pndaza.md`). Those sixteen pages' real
  headwords are in no source but our OCR.
- **Vol. 22: one printed page is missing from the scan near PDF p. 919.** From p. 920 to the end,
  each page's index headwords are found on the page before; the index's last page implies PDF
  p. 934 and the PDF has 933. A page-offset correction for pp. 920–933 after the batch; the missing
  page's headwords are lost with it. (Compare book 21, whose index runs 65 pages past its PDF.)
- **Vol. 14/3: eight small runs of headwords printed a page later than the index files them**
  (unindexed pp. 402, 565, 625, 930, 936, 962, and weaker 605, 976), besides three pages where the
  next page's list scores higher (564, 607, 620). Smaller cases in vols. 10 (p. 219), 18 (p. 815)
  and 22 (pp. 169, 184, 253, 894). All for `ID_PAGE_FIX` after the batch.
- **Vol. 17 was rendered at 69 dpi** (the median of three sampled pages, 72/68/69), though 502 of its
  879 page images are 72 ppi. Its recall (91.3%) is ordinary; a re-read at 72 would be a test.
- **Vol. 22** prints ညာ and ာ where the index writes ဉာ and ါ on whole runs (pp. 171–175, 828–837):
  the folds recover most (90.4% with them, against 88.5%).
- **The Reader's data is at 63.5 MB** of the 64 MB an artifact version may hold. Vols. 23 and 24
  will not fit as base64 text; they need a binary container or a lighter record (NEXT-SESSION). *Done in §27.*

## 27. After the batch: vols. 23, 24, 14/2; the index's page errors; book 21 (25 September 2026, evening)

**Vols. 23 and 24** (reports in `ocr/23/`, `ocr/24/`; OCR by the batch, 12:58–13:26):

| | vol. 23 | vol. 24 |
|---|---:|---:|
| PDF pages / index headwords | 780 / 7,182 | 718 / 7,088 |
| dpi (native) | **323** | 72 |
| headwords verbatim, either pass (with the folds) | 91.0% (91.2%) | 91.5% (91.9%) |
| **in printed order, column pass** | **83.2%** | **84.1%** |
| pages with every headword / ≥ 80% / < 50% | 53.8% / 88.1% / 10 | 49.5% / 88.4% / 4 |
| articles located | **97.7%** | 96.4% |
| normalised label + body | **92.7%** | 90.0% |
| compound analysis recovered | 59.3% | 72.8% |

Vol. 23 is the only high-resolution scan in the set (323 ppi, A4). It did not raise recall above
the 72-dpi books, and cost no more time (14 minutes for 780 pages); its in-order share and its
located share are the best of the scanned books, but whether that is resolution or print is not
separated. Its analysis recovery (59.3%, like 14/3's 59.6%) is low and not yet looked into. No
typed witness covers either book.

Spot checks, on the image (two pages each, a middle page and the worst): vol. 23 pp. 400 and 100,
16 of 18 at the right entry, 2 unlocated, none wrong; vol. 24 pp. 360 and 540, 8 of 9 right on the
page and **1 wrong** (သုတ္တန္တိကဒေသနာ, placed at a quotation line inside its own article: its label
and definition are lost), plus the eight misfiled headwords below. Both worst pages were index
errors, not OCR.

**Vol. 14/2 (book 14b)**, articles on the text-layer records of §25: located **98.2%**, label + body
**97.6%**, analysis 97.3%, the best of any book. One page checked in the text (p. 600): 13 of 13.
The text was extracted on 25 Sep (§25) and did not need extracting again.

**The index's page errors, applied** (`docs/index-errata.md` lists them all, with the spelling
errors and the vol. 13 / vol. 15 mix-up):
- `PAGE_FIX['22']`: index pp. 880–894 read one PDF page back. The scan lacks a printed page before
  PDF p. 920; its own headwords (11 on the index's list for PDF 919) stay unlocated.
- `ID_PAGE_FIX`: six runs in 14/3, four in 22, five in 23, two in 24 (one of them, ids
  208187–208194, found by the vol. 24 spot check: p. 540 prints only the long article သုမန²), and
  book 21's ten. Weaker candidates (14/3 pp. 605, 976; 18 p. 815; 10 p. 219) wait for an image check.
- Gains in located: 14/3 91.1 → 91.7%, 22 95.1 → 96.4%, 23 97.0 → 97.7%, 24 96.2 → 96.4%.
- `abhidhana_ocr.py`'s `index()` now applies the same corrections, so a page is scored against the
  headwords printed on it. Pages already on disk keep their old scores until re-scored.

**The label (ကာ၊ကမ္မ၊ကြိ)**, causative passive, is in the label map (readings from vols. 8–24;
clean in 14b). It now normalises 50 rows across 15 books; label + body rose by 0.1 point in vols.
8, 12, 13, 14/1, 18, 19.

**Book 21 explained.** Its index is not offset. Ten headwords (ids 170346–170355,
သတ္ထုဝဏ္ဏာဘတ … သတ္ထုဝိဿာသိက) carry p. **962** for **692**, and index p. 692 is otherwise empty; with
them corrected the highest page is 896, PDF p. 924 of 925. Checked on the image: PDF p. 720 prints
၆၉၂ with exactly those ten headwords, and PDF p. 924 prints ၈၉၆ with the index's last seven. Book
21's scan is 70–72 ppi. `tools/run_volumes.sh` no longer skips it.

**Vol. 25**: the pilot's page records (484, whole-page, 200 dpi) were moved from `ocr/25/pages/` to
`tmp/ocr-25-pilot-pages/`, so the OCR starts clean. The scan is 300 ppi (three pages sampled).
`ocr/25/pages-container.tar.gz` also unpacks into `pages/`: do not unpack it there.

**Every book re-run** (articles, romanisation) with the above, then the PCED and Pn Daza witness
joins for books 01–19 (figures in `docs/witness-join.md`, `docs/witness-pndaza.md`):

| | 01 | 02 | 03 | 4a | 4b | 4c | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| located | 94.4 | 93.6 | 94.8 | 92.2 | 96.7 | 92.5 | 93.6 | 92.0 | 93.1 | 92.1 | 92.5 | 90.8 | 93.0 | 96.9 |
| label + body | 89.0 | 88.4 | 89.6 | 85.0 | 91.1 | 86.8 | 87.7 | 86.3 | 87.3 | 87.8 | 86.0 | 84.3 | 86.2 | 91.8 |

| | 13 | 14/1 | 14/2 | 14/3 | 15 | 16 | 17 | 18 | 19 | 20 | 22 | 23 | 24 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| located | 89.5 | 96.6 | 98.2 | 91.7 | 93.4 | 92.8 | 93.4 | 92.4 | 96.3 | 95.7 | 96.4 | 97.7 | 96.4 |
| label + body | 83.8 | 92.4 | 97.6 | 85.4 | 87.6 | 86.6 | 84.9 | 84.5 | 89.7 | 87.1 | 90.2 | 92.7 | 90.0 |

**All 27 books together: 208,979 index rows** (every row of the index but books 21 and 25),
**94.0% located, 88.0% with label + body.** Vol. 13's 232 rows of vol. 15 headwords are among the
unlocated.

**The Reader** now has all 27 books. Its data moved from base64 text (`.gz.txt`) to gzip bytes
published under a `.wasm` name, which the artifact serves as `application/wasm`: 52.5 MB for the
27 books and the search index, against 63.5 MB for 24 as base64. The page reads the bytes with
`fetch().arrayBuffer()` and inflates them with `DecompressionStream`; if a server ever sends them
already inflated, it parses them as JSON directly. Verified in Node on the published bytes; not
yet opened in a browser by this session (the Cowork browser is not signed in to claude.ai).
Books 21 and 25 will add about 4 MB.

## 28. The public website, the page images, one label table (25 September 2026, night)

**Decided with Angel** (the other chat and this one): a public site on Cloudflare Pages at
**abhidhana.buddha-dhamma.net**, built from the repo on every push; page images in Cloudflare R2
(bucket `abhidhana-pages`) at **abhidhana-img.buddha-dhamma.net**; the PDFs stay in `sources-v1`.
One level of subdomain only: Cloudflare's Universal SSL does not cover `a.b.buddha-dhamma.net`.
Content rule: only our OCR and our additions; nothing of PCED or Pn Daza's `dict.db` until he
agrees.

**The site** (`site/`, built by `tools/abhidhana_site.py`, standard library only, into the
gitignored `site/dist/`): home with search and the volume list; `/v/<book>/<page>` with the
articles beside the page image; `/about/` (the dictionary, credits as in the README, licences,
reporting an error through a pre-filled GitHub issue); `/labels/`. Spanish and English, following
the browser, with a switch. A book is published when its `articles.jsonl` and `pali.jsonl` are
committed; the others show as "coming". Built over all books: 43 files, 250 MB, the largest data
file 12 MB (vol. 3; Pages allows 25 MiB a file, 20,000 files), 217,108 headwords in the search
file. Tested in a headless browser (desktop and phone widths, both languages), not yet deployed.

**Page images: native-resolution, 1-bit, lossless WebP.** Asked to compare 1,200 and 1,600 px, I
measured on the densest pages (vol. 3 p. 641, 23 headwords; vol. 24 p. 681; vol. 23 p. 300):

| | vol. 3 p. 641 | vol. 24 p. 681 | vol. 23 p. 300 |
|---|---:|---:|---:|
| 1,200 px, lossy WebP q70 | 211 KB | 157 KB | 165 KB |
| 1,600 px, lossy WebP q70 | 299 KB | 219 KB | 235 KB |
| native bitmap (pdfimages), lossless WebP | **99 KB** | **60 KB** | **91 KB** |

The scans are 1-bit; any downscale turns them grey, which lossy WebP then stores worse than the
original bits. At 1,200 px the stacked marks (ဂ္ဂ, ဗ္ဗ) are legible but soft; at 1,600 better; the
native bitmap is the print itself, and smaller than either. On 20 sample pages of vols. 1, 13, 23
and 4/3 it averaged 96 KB (0.2 s a page to encode): **about 2.5 GB for the whole set**, not the
1–1.5 GB first guessed, within R2's free 10 GB. No separate "view larger" is needed: the viewer
has fit-width and actual-size. Pages that are not one 1-bit image (covers, front matter, all of
14b's typeset text) are rendered with pdftoppm at up to 1,800 px, lossy WebP q80 (14b: ~190 KB a
page). `tools/abhidhana_pages_r2.py` does it (render, check, upload); tried in the cloud container
on 40 pages each of vols. 24 and 14b.

**One label table.** `docs/labels.md` §0 is now the only place the labels live: label, Pāḷi,
English, Spanish, abbreviations, status, Spanish status (`draft` / `confirmed`), and the OCR
readings. `tools/abhidhana_labels.py` parses it; `abhidhana_articles.py` builds its map from it
(checked: identical to the old dict, so no re-run was needed); the site's pop-ups and Labels page
read it. Confirmed: the five of `spanish-method.md` §2, (ဗျ) abyaya and (ကာ၊ကြိ) kārita-kriyā
(Angel, 25 Sep). Every Spanish meaning is my draft. The pop-up opens only on a click or tap on
the label (dotted underline), one at a time, floats just below the label's line, and can be
turned off (remembered per browser). (§29 adds the printed expansions and a third status.)

**Repo size.** Committed data: `articles.jsonl` 395 MB and `pali.jsonl` 308 MB over 28 books;
`.git` is 309 MB, all loose objects (no pack). About 40% of each file repeats another field
(`raw` in articles, `body_joined` in pali). Proposal in NEXT-SESSION.

## 29. Vol. 21 finished; vol. 25 at the wrong resolution; the labels as the dictionary explains them (25 September 2026, night)

**Vol. 21**: reports in `ocr/21/`. 925 pages, 8,129 headwords, 70 dpi; verbatim 91.8% (92.3%
folded), in printed order 75.9%, **located 97.4%**, label + body 89.8%, analysis 80.7%. Spot check
on the image (pp. 500, 318, 720): 31 of 32 at the right entry, 1 unlocated, none wrong, every label
right. In the Reader.

**Vol. 25 must be re-read at 200 dpi.** The batch rendered it at its native 300 ppi, and recall
fell to 88.2% (column pass 79.3%) against the pilot's 94.0% at 200 dpi (§5, which already said
"200 dpi, not 300" for this book). Measured on the same 16 pages (chosen among the worst of the
300-dpi run, so the gap is exaggerated): **300 dpi 57.8%, 200 dpi with the column cut 88.3%**, the
pilot's whole-page 200 dpi 89.0% (cloud container, tesseract 5.3.4). Vol. 23 at 323 ppi was not
hurt, so it is this book's type size, not resolution as such. The 300-dpi pages, articles and
reports were moved to `tmp/ocr-25-300dpi/`; `run_volumes.sh` now renders 25 at 200. **"Render at
native" is a default, not a rule: measure a sample per book.**

**The dictionary explains its labels.** Besides the tables of abbreviations (vol. 1 p. 120, vol. 4/1
p. 42; vol. 2 p. 14 now checked on the image: 12 entries, adding (ကမ္မ၊ကြိ) ကံဟောကြိယာ and ဗု၊သံ
ဗုဒ္ဓဘာသာသက္ကတ), vol. 5 p. 48 describes the brackets in prose: (ထီ၊ပု) (ပု၊န) (ထီ၊န) are "two
genders mixed", (တိ) "all three genders, i.e. an adjective", (ကြိ) the active verb against (ကမ္မ၊ကြိ)
the passive, (ဗျ) indeclinables "such as upasagga and nipāta"; and the same brackets have seven
other uses, so not every ( ) is a label. Vol. 4/1 pp. 31–36 and vol. 15 pp. 17–22 hold the table of
citation abbreviations (the key for resolving citations later). `docs/abbreviations.md` has it all.

`docs/labels.md` §0 now carries, for each label, the printed expansion and where it is printed, and
a third status: `confirmed` (Angel: the five genders/verb labels, (ဗျ), (ကာ၊ကြိ)), `printed` (the
dictionary gives the meaning: (ကြိ၊ဝိ), (ကမ္မ၊ကြိ), (ကာ၊ကမ္မ၊ကြိ) by composition, (ပု၊န) (ထီ၊ပု)
(ထီ၊န), (ပုံ-ဗဟု)), `provisional` (the rest). The OCR readings are unchanged, so no re-run.
`tools/abhidhana_labels.py` now finds columns by their header. The site's pop-up shows the printed
expansion too, and says "provisional" only for provisional labels (and, in Spanish, while the
Spanish is a draft).

## 30. Vol. 25 at 200 dpi: all 29 books done (25 September 2026, night)

Re-read natively at 200 dpi (8 minutes). Reports in `ocr/25/`.

| | vol. 25, 200 dpi | 300 dpi (discarded) | pilot (§5) |
|---|---:|---:|---:|
| headwords verbatim, either pass (with the folds) | **94.9%** (95.0%) | 88.2% | 94.0% |
| column pass alone | 89.4% | 79.3% | |
| **in printed order, column pass** | **83.4%** | 73.3% | |
| pages with every headword / ≥ 80% / < 50% | 67.1% / 95.3% / 2 | 45.5% / 82.1% / 12 | 63% / 92% / 0 |
| articles located | **95.3%** | 93.3% | |
| normalised label + body | 87.4% | 86.5% | |

The best recall and in-order share of any scanned book. Its worst pages (pp. 158–160) are the
headwords in သ္နေ, a stacked consonant the OCR does not read; the fuzzy alignment places them.
Spot check on the image (pp. 400, 159): 19 of 20 index rows at the right entry, 1 unlocated (the
index gives one printed entry, သ္နေဟယတိ၊ သ္နေဟေတိ, two rows), none wrong; 3 labels not read.

**All 29 books: 221,154 index rows, 94.1% located, 88.1% with label + body.** Every book is in
the Reader. The README now has the progress of all 29, the layout, the typed witnesses and the
index errata, and a section in Spanish.

## 31. The page images: the bitmap test was too strict (25 September 2026, afternoon, Mexico time)

Angel's first run of `tools/abhidhana_pages_r2.py render` (all books) was stopped in 4a: **522 of
vol. 1's 913 pages and 479 of vol. 2's 898** had been stored as 1,800 px lossy WebP (~430 KB) rather
than as the native bitmap (~90 KB). The test for storing a page's own bitmap compared its aspect ratio
with the page box's, within 0.03; but on many pages the scan sits in a page box with a blank margin
(vol. 1 p. 500: 2051 × 3002 px at 73 ppi, i.e. 2,961 pt tall, on a 3,142 pt page), so they fell to the
render. At that rate the set would have been ~6 GB, not ~2.5 GB.

The test is now: one 1-bit image, **undistorted** (x-ppi = y-ppi within 3%, from `pdfimages -list`),
covering **≥ 85% of the page each way** (and ≤ 103%). Measured over all 29 books with `pdfimages -list`:
it accepts every page the old test accepted and ~3,500 more (vol. 1 391 → 912, vol. 2 419 → 897, vol. 6
627 → 1,038, vol. 12 626 → 1,122, vol. 15 651 → 849; lowest coverage accepted 0.887). What it still
renders: 14b's typeset pages, covers and front matter, and one vol. 13 page (p. 28, 84% high). The bitmap
is stored without the page box's blank margin. Vol. 1 pp. 495–505 re-rendered with the fix: all native,
84–92 KB; p. 500 viewed, upright and whole.

A plain re-run now **redoes a stored page only when it should be the bitmap and is not** (its width
differs from the bitmap's): after the stop, 521 in vol. 1, 478 in vol. 2, 48 in vol. 3, none in 4a.

**`check` could not see a flipped page.** Its mean-difference score was ~21 for right pages and 32.5 for
the same page flipped, under its threshold of 35. It now blurs both images at 300 px wide and takes the
correlation at the best offset (the bitmap may sit inside the page box): right pages 0.95–0.98, flipped
0.53, rotated 180° 0.35; flagged under 0.80.

**Vol. 1, the trial (Angel, on the Mac).** `render 01`: 521 pages redone as native bitmaps, 392 kept,
28 s; 81.9 MB, **88 KB a page**. `check 01`: 12 sample pages, correlation 0.938–0.999, none flagged.
`upload 01`: 863 uploaded (76.7 MB) in 37 s, 50 already in the bucket. On the live site (in-app browser):
`/v/01/500` shows the page beside its articles at 2051 × 3002; pp. 49, 50, 120, 300, 505, 700 and 913
load at native size and p. 1 (the cover) at 1,800 px, as intended. The dark theme shows the page
inverted on purpose (`--page-filter` in `site/src/assets/style.css`). The image host sends no CORS header:
`<img>` does not need one, but a script that `fetch()`es an image would.

## 32. The weak page corrections, checked on the image (25 September 2026, afternoon)

NEXT-SESSION item 5. Every candidate was read on the page image (`docs/index-errata.md` §1, §3):

| candidate | on the image | applied |
|---|---|---|
| 14/3 201781–201786 → PDF 976 | p. 976 (printed ၉၄၉) begins with exactly these six | `ID_PAGE_FIX` |
| 14/3 198069–198070 → PDF 605 | p. 605 (၅၇၈) begins with **seven**: 198064–198070 | `ID_PAGE_FIX`, 198064–198070 |
| 14/3 p. 607 | the list for p. 607 runs on to the unindexed p. 608 (၅၈၁): 198090–198096 | `ID_PAGE_FIX` |
| 14/3 p. 620 | the same, p. 621 (၅၉၄): 198166–198168 | `ID_PAGE_FIX` |
| 14/3 p. 564 | already covered by 197721–197732 → 565 (§27) | — |
| 18 146728–146731 → PDF 815 | p. 815 is wholly inside ဝသ¹; p. 816 prints ဝသ²⁻⁵: **the index is right** | none |
| 10 81975–81976 → PDF 219 | p. 219 (၁၇၁) prints only ဒသ²; ဒသ¹ is on 218, ဒသ³⁻⁵ on 220 | `ID_PAGE_FIX`, 81975 only |

Re-run: articles and romanisation for books 10 and 14c, both witness joins (01–19), Reader data. 14/3:
located 91.7 → **91.9%**, label + body 85.4 → 85.6%; the 23 rows placed, with labels as on the image,
and four neighbours lost the following articles they had swallowed. Vol. 10: 81975 placed at ဒသ²
(analysis 1.0 against the witness); vol. 10's witness figures rise by one row. All 29 books: still
94.1% located, 88.1% with label + body (194,857 of 221,154).

Six index typos read on these pages: 14/3 198058 ပိဏ္ဍစရဏဝီရိယ (ပိဏ္ဍပါတ…), 198068 …နီဟရဏ (…နီဟရက), 198083
ပိဏ္ဍပလိဗောဓ (ပိဏ္ဍပါတ…), 198088 …ဘောဇန (…ဘာဇန), 198164 ပိဟာမဟဒွန္ဒ (ပိတာ…); vol. 10 81979
ဒသအကုလလကမ္မပထ (ဒသအကုသလ(ဒသာကုသလ)ကမ္မပထ).

**Homonyms paired one entry late, the other way round.** On vol. 10 p. 220 the first ဒသ of three is
unplaced and the second and third hold the articles of ဒသ³ and ဒသ⁴ (the typed witness: body ratios 0.36
and 0.24). §18's rule handles the case where the first of two is placed and the second not; this is the
converse. Across all 29 books there are **177 runs of identical headwords where an earlier one is
unplaced and a later one placed on the same page**. Not all are wrong (the earlier head may simply be
unread), and none was changed: for books 01–19 the witness joins can sort them, elsewhere the image.

## 33. The compound analysis when its opening bracket is lost (25 September 2026, evening)

NEXT-SESSION item 7: why vols. 23 and 14/3 recovered the analysis for only ~59% of articles.
Among the labelled articles with no analysis, measured on the 70 characters after the label:

| | vol. 23 | 14/3 | 14/1 | 24 | 22 | 12 |
|---|---:|---:|---:|---:|---:|---:|
| labelled, no analysis | 36.8% | 31.0% | 35.5% | 20.4% | 19.9% | 12.9% |
| of those: no `[`, but `+` | **81.9%** | 20.7% | **75.2%** | 69.6% | 51.0% | 54.2% |
| `[`, no `+` | 7.1% | **56.1%** | 10.0% | 12.0% | 24.1% | 19.1% |

**Vol. 23 sets its brackets apart**, `[ သမ္မဇ္ဇနီ + ဒဏ္ဍ ]` (image, PDF p. 40), and OCR drops the
free-standing `[` (1,673 rows) or reads it as `]` (322), keeping the `+` signs and usually the `]`.
`abhidhana_articles.py` now takes, after the two existing attempts and only where they fail,
elements joined by `+` straight after the label, optionally led by a `]` or `|`, **when a `]` follows**
(allowing a derivation note after `။`, up to 60 characters, as the print's bracket does). Flagged
`analysis_bracket_damaged` and `analysis_open_lost`.

Re-run on all 29 books (articles, romanisation, witness joins, Reader data): **analysis 75.0% →
77.2%** (+4,907 rows); vol. 23 59.3 → **74.1%**, 14/1 60.0 → 71.2%, 24 72.8 → 81.2%, 22 73.2 →
78.3%, 12 80.6 → 84.5%. **No analysis already read changed**, nor any placement or label. Against the
typed witness (books 01–19) the 1,758 gained analyses it can check are ≥ 0.8 similar in **97.2%**,
< 0.4 in 0.2%, against 90.1% / 0.6% for the rest. Vol. 23 (no witness): on PDF p. 40 the one gained
row (185537, သမ္ပဇ္ဇနံ + ဒဏ္ဍ for the printed သမ္မဇ္ဇနီ + ဒဏ္ဍ) is right in structure, with ordinary
letter errors. `docs/witness-join.md` §2 and `docs/witness-pndaza.md` now show all of books 01–19.

**14/3 is a different failure and is not fixed**: the `[` is read and the `+` signs are lost
(`[ပါစိတ္တိယဒိဋ္ဌိ …`, `[ပဟာရ ဌာန …`), and its `]` is usually read as ု, ျု or ါ glued to the last
element (`…ဒါယကု`). Without either the `+` or the `]`, where the analysis ends cannot be told from the
text alone; the headword, which the elements spell out, could delimit it (NEXT-SESSION item 7b).
14/3 stays at 60.0%.

## 34. The dictionary's history on the About page (25 September 2026, evening)

Angel's `docs/history.md` (EN/ES, from the dictionary's own front matter) is built into the About
page as a **History / Historia** section by `tools/abhidhana_site.py` (a small Markdown subset,
standard library; Burmese runs set in the site's Burmese face). **It is not yet published**: the
build includes it only when the file's status line reads `<!-- site: publish -->`; it now reads
`site: draft`, because the romanised names of people and monasteries are mine and need Angel's
review. `ABHIDHANA_SITE_DRAFTS=1` includes it in a local build, marked as a draft. Checked in a
headless browser at 1,200 and 390 px, both languages.

**The attribution is corrected** on the About, home and Reader pages, in the README and in §1:
by vol. 17 pp. 6–7 the dictionary was written by five teams among which the alphabet was divided,
Masoeyein monastery writing vols. 5–6 and 15–16, not by "the Masoeyein Board of Scholar-Elders".
The corrected line names no one but Masoeyein, so it is live on the next push. The Project's own
description and instructions still carry the old line (Angel's to edit).

## 35. All page images live; a light/dark switch; the Introduction page (25 September 2026, night)

**Page images.** Angel ran `abhidhana_pages_r2.py all` on the Mac: **25,700 pages, 2,509 MB** in R2
(`abhidhana-pages`), 19–49 s a book to upload. The scans average **87 KB a page**; 14/2's typeset pages,
rendered, **377 KB** (the §28 estimate was ~190 KB), 357 MB of the total. In the in-app browser, the
first, middle and last page of every book load from abhidhana-img.buddha-dhamma.net (87 images, none
failed). `check` on all 29 books: no page flagged. Vols. 14/1 and 19 score 0.85–0.88 throughout (and
three vol. 10 pages 0.87) against 0.94–0.99 elsewhere: book-wide, so the scan's type and not a page stored
wrong (a flipped page scores ≤ 0.53); not looked into further.

**Light / dark.** A button in every page's header switches the theme; the choice is remembered per browser
(`localStorage.theme`), and until it is used the system's setting decides, as before. A small script in each
page's head applies a remembered choice before the page is drawn. *Its first version declared a global `t`,
which collides with `common.js`'s `const t` and stopped common.js on every page; caught in a headless-browser
test before any push and fixed (the script is now wrapped in a function).*

**The Introduction page, `/introduction/`**, built by `tools/abhidhana_intro.py` (standard library) from
`docs/introduction/`, which another chat is filling chapter by chapter. The contract it reads, stated in the
module's docstring: one `chN-*.md` a chapter, with `## 1. Burmese transcription`, `## 2. English`,
`## 3. Español` and `## Notes for review …`; a status table before the first `##` (per part, or per batch);
page markers `` `[p. N]` ``; headings as lines wholly in bold. The page has:
- a table of contents from the chapter titles (each language's from its own section) and the headings in
  each section, and a line saying which chapters (by `README.md`'s table) are not yet transcribed;
- three views, remembered: the translation (EN/ES by the site's switch), the Burmese original, or side by
  side, which pairs the Burmese and the translation page by page where the translation carries the page
  markers (ch. 4) and shows the two whole sections where it does not (ch. 5);
- every page marker a link to that page's image (vol. 1, PDF page N);
- each file's status table as labels (drafted / reviewed / corrected / not yet done), and a draft banner
  while anything is unreviewed; the notes for review folded under each chapter;
- `citation-abbreviations.tsv` (100 rows) as a table with a search that ignores diacritics (dīgha = digha)
  and reads Burmese; the Burmese entry as printed shows in the Burmese and side-by-side views.
Linked from the home and About headers and from About's first section. Tested in a headless browser at
1,200 and 390 px, both languages, all three views, light and dark: no script errors, no horizontal scroll.
**Unlike the About page's History (§34), it publishes drafts**, under the banner, as Angel asked; ch. 4 holds
the same romanised names that keep the History back.

## 36. Citations keep their whole abbreviation (25 September 2026, night)

The citation pattern in `abhidhana_articles.py` allowed one run of letters before the numbers, so
`ဒီ၊ ဋ္ဌ၊ ၂။၃၉၆။` (Dīgha Aṭṭhakathā 2.396) was stored as `ဋ္ဌ၊၂။၃၉၆။`: the work was lost on every
commentary and subcommentary citation. Measured against vol. 1's 100 citation abbreviations
(`docs/introduction/citation-abbreviations.tsv`), only **28%** of the 530,971 citations matched one.
The pattern now takes up to three parts joined by ၊; a leading part that carries asat, visarga or
dot below is a Burmese word, not abbreviation, and is dropped (`cite_trim`). On vols. 5, 14/3 and 23,
before the re-run: the same 47,541 citations, matched 30.1% → **71.4%**; all books, measured with the
preceding words restored, 77.8%. All 29 books re-run (articles, romanisation): the same 530,971
citations, **no other field changed in any row**. What still does not match is mostly OCR forms of the
commentary marks (ဌ, ္ဌ, ဋ for ဋ္ဌ; ဋံ, ဋိ for ဋီ), `သစ်` glued on (probably "new [edition]", unchecked),
and works absent from vol. 1's table: 14/3, 4/2 and 4/3 match 57–60%, vol. 24 65%. Vol. 4/1 pp. 31–36
and vol. 15 pp. 17–22 print fuller tables (NEXT-SESSION 3b). Matching for the site is to fold the
commentary marks and stay silent where nothing matches.

## 37. Translation: batch 1 of the stem lexicon (25 September 2026, night)

Angel's decisions (site design): the Meaning box shows drafted translations marked drafted, and
stays visible, "not yet translated", until filled; Spanish label abbreviations proposed for him to
confirm. Then: translate from the Burmese into Spanish and English, by stem, vol. 1 first.

**Measured on vol. 1.** Our OCR of the definitions is too noisy to build stems from (debris, split
words, early stops); the PCED typed text is clean for vols. 1–19. On PCED (8,148 definitions,
40,877 stem occurrences, 12,510 distinct stems): the top 100 stems cover 32% of occurrences and 1.7%
of articles wholly; top 1,000 59% / 16.6%; top 5,000 82% / 50%. By shape: **390 articles (4.8%) are
pure formula** ("see X", "see also X", "same meaning as X"), 1,003 (12.3%) one stem, 1,398 two,
5,356 (66%) three or more. So stems fix the vocabulary; most articles still need a composed sentence.
A stem is a hyphen alternative with its grammatical ending removed (`~/tr` scripts in the VM; the
Burmese mark order ့် / ့် must be normalised first: PCED and my patterns differ, invisibly).

**Batch 1** (`docs/translation/stems.tsv`, `docs/translation/batch01-review.md`, also in the Project):
27 formulas and the 100 commonest lexical stems, EN and ES each from the Burmese, all `proposed`;
flags for glossary terms (dhamma, citta, saññā, akusala, dukkha …), homographs (နေ, သွား) and doubtful
choices. Approved, it fills 390 vol. 1 articles by rule and gives 253 more (3.1%) all their stems;
the 100 stems cover 15.3% of stem occurrences. Also proposed: Spanish abbreviations for the labels.

**Open, for Angel**: translate from PCED or from our OCR (licence); mechanical fill plus composed
drafts for the rest; where the doctrinal IEBH glossary is (only the grammatical one was found,
`~/Tipitaka/nissaya/anchor/glosario-gramaticas.md`).


## 38. The site redesign built: Browse is the home page (26 September 2026, early morning)

Built from `docs/site-design.md` and the mockup artifact "Abhidhāna site mockup" (a reference, not
code). **Browse** (`site/src/index.html`, `assets/browse.js`, data from `tools/abhidhana_browse.py`)
is the home page:
- a mode bar with two reading modes (Pāḷi reader / as printed), a settings panel (script,
  definitions, labels, printed page) and the printed-page switch, off by default;
- the alphabet in the dictionary's order with the two-level thumb index (group, syllable);
- the headword list and the article: labels, analysis, "see" links, the **Meaning box**, the Burmese
  definition, quoted passages and expandable citations;
- the page image beside it on demand;
- addresses `/w/<headword>` and `/browse/…`, and a header search with no diacritics, across all volumes;
- a phone layout (the alphabet in a drawer).

The old home page is now `/volumes/`. Labels and citation abbreviations are one page, `/abbreviations/`
(`/labels` redirects there). Every page has the same header, with the warm palette from the mockup
and the light/dark button.

Tested with Playwright on a vol. 1 build (desktop and phone, light and dark, ES and EN): no script
errors. The only failures were the external fonts and images, which the container cannot reach. The
full build in the VM gives 950 files, 540 MB (largest chunk 1.5 MB), 221,154 entries in 385 groups
and 820 chunks, 8,467 see-links and 84.7% of citations matched. **`site/src/labels/` is obsolete**:
Angel removes it with `git rm -r`, and the build already drops it from `dist`.

## 39. The Meaning box filled for vol. 1: drafts, not readings (26 September 2026, early morning)

Angel's scope rule: **only the Burmese explanations are translated**, never the Pāḷi or the Pāḷi
passages quoted as examples. He asked for the boxes to be filled while he was away. Nothing here
is reviewed: every row is `drafted` in both languages, and the site says so in the box.

**Source.** The PCED definition line for 8,148 articles, and our OCR for one. The PCED text is clean;
its licence is unknown (§31), so the source is recorded per row (`source`).

**Method** (`tools/abhidhana_meanings.py`, `docs/translation/drafting-brief.md`):
1. `prep` replaces "X-ကြည့်", "X-လည်းကြည့်", "X-နှင့် အနက်တူ", "X,တူ" and "အထက်ပုဒ်နှင့် အနက်တူ"
   with placeholders, rendered by rule: *Véase X.* / *Véase también X.* / *Mismo significado que X.*,
   X romanised and linked to its headword.
2. The rest was drafted from the Burmese in 16 parallel shards. Spanish was written directly from the
   Burmese, and English alongside it, following the brief:
   - hyphen alternatives kept apart as "a / b";
   - ၊ → "; ";
   - …သော၊ သူ၊ သည် → "(dicho de una persona o de una cosa)";
   - the batch-1 renderings of `stems.tsv`, still *proposed*.
3. Pāḷi was not translated. The drafts mark it and `merge` transliterates it (Aksharamukha, as
   `abhidhana_romanise.py`). A doctrinal term missing from the table was kept in Pāḷi (*kusala*,
   *jhāna*, *magga* …), because the IEBH doctrinal glossary was not found.

**Counts.**
- `docs/translation/meanings/01.jsonl` has 8,144 rows (5 have nothing to translate): 384 by formula
  and 7,760 drafted.
- 816 rows carry a flag: an unclear Burmese word, a likely misprint, or a "see X (n)" left inline.
  They are listed in `meanings/01-flags.tsv`.
- 555 Pāḷi terms were kept, in 1,636 articles. They are counted in `meanings/01-terms.tsv`, the
  glossary proposals.
- 1,523 links to other headwords resolve in the build.

**Known weaknesses.**
- Batch 1 is not approved. Two of its stems were rendered both ways: *akusala* (L067, "no saludable
  (akusala)") and *anicca* (L071, "impermanente") sometimes appear rendered and sometimes kept in Pāḷi.
  Once Angel approves or changes a stem, re-render the rows that use it and reset their status.
- Proper names came out in lower case (*ajita*): the transliteration keeps the index's convention.
- Sentences start in lower case, as dictionary glosses do.
- The drafts are by article, constrained by the stem table, not composed stem by stem. The method's
  "by stem" is kept at the level of the table, not of the sentence.

## 40. After the redesign went live: site fixes, PCED analyses, sano / insano (26 September 2026, night)

**The live site was checked after Angel's push** (in-app browser): Browse at `/`, `/w/<headword>`,
`/volumes/` (29 of 29 books), `/abbreviations/` (labels and 100 citation abbreviations), `/labels`
redirecting, the 404 page, the phone layout at 375 px (no horizontal scroll, the alphabet drawer).
The vol. 1 Meaning boxes: 8,143 of 8,150 rows carry ES and EN, all `drafted`. **Six rows have none,
not five as §39 says** (ids 21, 2190, 3938, 3988, 5435, 7881): no PCED line, and at least 21 and 3988
have a translatable OCR definition. Row 2767 (the one drafted from OCR) keeps Burmese tree names and a
Pāḷi quotation inside the Meaning. The Pāḷi-span finder reads Burmese words as Pāḷi (အစ "beginning"
romanised *aca-* on `/w/a` and listed as a quoted passage); how often is not measured.

**Fixes asked for by Angel, built and tested with Playwright on a full local build** (desktop 1,000 /
1,440 px, phone 390 px; no script errors):
- The header search list overlapped the headword and "vol. · p." in a narrow box: the list is now at
  least 440 px wide and puts the page line under the headword. 0 overlaps in the first 15 results.
- **Hide index / Mostrar índice** (modebar button, key `\`, desktop only): hides the alphabet and the
  headword list; the article, and the printed page if on, take the width. Remembered per browser
  (`localStorage['browse-panes']`), kept apart from the reading mode.
- **The label as the dictionary prints it, romanised**: *akuppa* (ti). `docs/labels.md` §0 has a new
  column `roman` (Aksharamukha, ၊ written ", "; mechanical, for Angel to confirm, e.g. (a-liṅ) for
  (အ-လိင်)); the table is otherwise identical (checked field by field). The Pāḷi reader mode now shows
  labels "as printed" in the chosen script: (ti) in roman, (တိ) in Burmese, both in both; the pop-up
  still gives the meaning. A saved named mode takes its current defaults. `/abbreviations/` shows the
  roman form under each label. Spanish abbreviations (`abbr. es`) are all still empty.
- The ES/EN switch was clipped at ~1,000 px: the header keeps to one line only from 1,180 px, and the
  switch no longer shrinks. The modebar's description is hidden below 1,180 px.
- The alphabet in the left pane shows roman letters only in roman mode, Burmese only in Burmese mode.

**Hand corrections** (`docs/corrections.tsv`, `tools/abhidhana_corrections.py`): one row per corrected
field (label, analysis or body), with the OCR reading at the time, who and when. Applied last in
`abhidhana_articles.py`, so re-runs keep them; the row keeps status `ocr` and gains `corrected`; the site
marks the field "corrected". First entry: akusala (505) [န + ကုသလ], OCR ကုသလျ (Angel). A corrected **headword** (an index
typo) is shown, romanised and filed under its printed spelling, with the index's kept as
`headword_index` and shown on the page: 4c id 172639, index စကစတုက္ကာဒိကဆတ္တိက, printed
ဧကစတုက္ကာဒိကဆတ္တိက [ဧကစတုက္ကာ + ဒ + ဆတ္တက] (Angel), now under *e*, not *c*. Re-run of vol. 1:
exactly that row changed in `articles.jsonl` and `pali.jsonl`.

**The compound analysis from PCED** (Angel's decision; `tools/abhidhana_witness_analysis.py`). Measured
first, books 01–19 with 4a, 4b: of 119,627 articles where both have an analysis, **60,859 (50.9%)
differ** after spaces and + are evened out; PCED's elements spell the headword more closely in 50,431,
ours in 3,402, 7,026 tie; PCED has one for 35,445 articles where we read none. Angel's checks: akusala,
akuppa [န + ကုပ္ပ] (OCR ကပ္ပါ), akusaladhātu [အကုသလ + ဓာတု] (OCR ဓာတျ): PCED right each time. So
`abhidhana_articles.py` now takes PCED's analysis (whole, as its field runs past ။ like the print's
bracket) wherever the join pairs a PCED entry that has one; the OCR reading stays as `analysis_read`,
the row carries `analysis_source: "pced"`, hand corrections still win. The witness joins and the
report's "recovered by the OCR" line measure `analysis_read`, not PCED's text. Re-run for all 21 books
with a join: 155,072 rows take PCED's analysis; **no field other than the analysis changed in any row**
(checked by a per-row digest). Romanisation re-run. The site marks such analyses "PCED". Books 4/3's
own text, 14/2, 14/3 and 20–25 keep the OCR. README and About now credit PCED and say where its text
is used (they had said nothing of it was published, which the vol. 1 drafts had already made untrue).

**sano / insano** (Angel): kusala = *sano*, akusala = *insano* in Spanish. `docs/translation/glossary.tsv`
records it (the first entries of the doctrinal glossary; English open); `stems.tsv` L067 is
`confirmed-es`. In `meanings/01.jsonl` 134 rows changed, Spanish only: "no saludable (akusala)" and
kept *kusala* / *akusala* became *sano/sana/sanos* agreeing with the noun, *lo sano / lo insano* as a
noun or a hyphen alternative, "y" → "e" before *insano*; *akusala* kept where the word itself is meant
(544, 587); compounds (*akusalavipāka* …) untouched. Status stays `drafted`. Batch 1's other stems are
still not reviewed (Angel: "I don't know").

## 41. Assets versioned; vol. 2's Meaning boxes drafted (26 September 2026, night)

**Assets.** Cloudflare served `/assets/*` with `Cache-Control: public, max-age=14400` (4 hours) although
`site/src/_headers` says `no-cache`; `/data/*` did follow `_headers`. After the push of §40 the live
`browse.js` was new but the in-app browser ran its cached old copy against the new label table. The
cause is probably the zone's *Browser Cache TTL* (its default is 4 hours); not confirmed in the dashboard.
`tools/abhidhana_site.py` now ends with `version_assets()`: every `/assets/` link in the built pages gets
`?v=<first 10 hex of the file's SHA-256>`, so a changed file has a new URL (7 pages rewritten). Tested
in a headless browser: pages load, no script errors.

**Vol. 2 drafted** (the method of §39; `docs/translation/drafting-brief.md`, which now carries the
glossary rule: kusala = *sano*, akusala = *insano*, agreeing with the noun). `abhidhana_meanings.py`'s
working folder moved from `work/meanings` (not gitignored) to `tmp/meanings`. `prep 02`: 7,189
explanations, 303 formula-only, 6,886 drafted in 16 shards by 16 agents, each with its own scratch
folder, told to translate every line itself (no scripts or MT). Checked after: every shard one line per
input id in order, valid JSON, every «Sn» in both languages. `merge 02`: **7,189 rows (every article of
vol. 2), all `drafted`, all from PCED; 517 flagged** (`meanings/02-flags.tsv`, with the Burmese), 615 Pāḷi
terms kept (`meanings/02-terms.tsv`; commonest apāya 87, kilesa 65, appanā 53, kamma 50). *sano/insano*
used 108 times; no "no saludable" left.

**Known weaknesses the agents reported** (nothing reviewed):
- Pāḷi already in Pāḷi form was sometimes written ⟦=iast⟧ rather than copied (both romanise the same;
  shards 00, 04 and 11 fixed their own; the brief's own vipassanā example invites it).
- ပယ် rendered *rechazar* / *reject* up to id 11625, then mostly *abandonar* / *abandon* (shard 07): a stem
  for the table.
- "see X" sentences that `prep` did not turn into placeholders (a sense number or "(က) အနက်" after X) were
  rendered by hand and flagged (shards 12, 14).
- 11 rows keep Burmese plant or mineral names outside ⟦ ⟧ (flagged); a Burmese month romanised as
  *Tazaungmon* (11741).
- Shard 15 flagged 37 rows only because their label is empty.
- Doubtful glosses flagged, e.g. 8481 anuttama "not highest", 10217 anesamāna, 11548 apatthaddha.


## 42. The live site after `5db316f`; vol. 3's Meaning boxes drafted; version numbers (27 September 2026)

**The live site, checked in the in-app browser** (neither the cloud container nor the Cowork VM can reach
it: both proxies refuse the host). `/w/anu` shows vol. 2's Meaning box (ES, marked *borrador*), the PCED
analysis mark ("Análisis PCED", `[ana + u]`) and the label as printed, romanised: (bya). `/w/akuppa`:
(ti), "Análisis PCED" `[na + kuppa]`, the Meaning box. `/w/akusala`: "Análisis corregido" `[na + kusala]`
(the hand correction of §40) and *sano / insano* in its Meaning. The pages load `favicon.svg?v=28348bf395`,
`style.css?v=b80a64a9cf`, `common.js?v=c79f868708`, `browse.js?v=7df226c490`, and these are the first ten hex
of the SHA-256 of `site/src/assets/*` in the folder, all four. Cloudflare still sends
`Cache-Control: public, max-age=14400` for `/assets/*`; with versioned URLs that no longer matters. The
console shows three `ERR_BLOCKED_BY_CLIENT` loads, not identified (a blocker in the in-app browser, most
likely; every request to the site itself returned 200). Seen on the page, not measured: vol. 2's anu has
senses (11) and (12) both "lo menor" (the Burmese has အငယ် twice), and the quoted-passage finder still lists
OCR debris as Pāḷi (§40).

**Vol. 3 drafted**, by §41's method, from PCED, with glossary.tsv (kusala = *sano*, akusala = *insano*).
`prep` was run with **24 shards, not 16** (`prep('03', 24)` from Python; the CLI has no shard argument),
so that each shard (474 lines) is about the size of vol. 2's (430); vol. 2's working files were moved to
`tmp/meanings/v02/`. 24 agents in the cloud container (at most 20 at once), each with its own scratch
folder, told to translate every line itself and to copy Pāḷi already in Pāḷi form as ⟦Burmese⟧, keeping
⟦=iast⟧ for Burmese loanword forms (ကိလေသာ, ဈာန်, မဂ်). Checked after, over all shards: one line per input
id in order, valid JSON, every «Sn» in both languages, brackets balanced, no empty field; 16 rows keep
Burmese words outside ⟦ ⟧ (plant and other names), all flagged. `merge 03`: **11,726 rows (every article of
vol. 3), 372 by formula, 11,354 drafted, all `drafted`; 11,722 from PCED, 4 from our OCR; 1,076 flagged**
(`meanings/03-flags.tsv`, with the Burmese). *sano/insano* in 65 rows' Spanish, no "no saludable". Links:
2,001 of 2,157 "see X" targets (92.8%) match a romanised index headword (vol. 2: 94.0%), measured on
`headword_iast`, not on the site's build.

`meanings/03-terms.tsv` (933 terms) is **not comparable with 02's** (615): the agents listed in `terms`
the Pāḷi-form terms they copied as well as the ⟦=iast⟧ ones, so vol. 3's list includes headword stems
(avijjā 151, arahattaphala 149, ariyamagga 149, ariya 140, nāma 87, abhiññā 86). Shard 07 listed only ⟦=⟧
terms in its first four blocks.

**Known weaknesses the agents reported** (nothing reviewed):
- "See X" sentences that `prep` left inline (a sense number after X, or a misprint such as ကြည် for
  ကြည့်) were rendered by hand, "Véase ⟦X⟧", and flagged, in most shards.
- "မူရင်းကြည့်ပါ" ("see the original") ends several PCED definitions (shards 00, 02, 09, 15, 18, 21): an
  editor's note in the witness, translated literally; whether the print has it is not checked.
- Definitions that look shifted by one row: 26094/26095 (asuddhahetu / asuddhāsaya), 19815
  (arahattamaggadiṭṭhi repeats -paññā), 23043 and 24328 run on into the next headword. For the image.
- Readings chosen through misprints and flagged: 17261 (မာန် for Māra?), 18641 (စေတနာ for စောဒနာ?), 21443
  (သံ read သဲ), 16270 (ပရိသတ် read ပရိယတ်), and missing negations (22854, 24277, 24354).
- ဟော rendered *expresar* / *express* where it means "denotes" (shard 02), against the stem's *enseñar*.
- Counts of things are mostly written as words ("los tres géneros"): the brief's "numbers stay numbers"
  is read differently by different shards.
- Seen in a sample: 15392 abyākata (2)(a) "no declarado como sano, insano" for ကုသိုလ်,အကုသိုလ်: *o* is
  wanted.

**Version numbers** (Angel: "we should put version numbers to the different iterations"). Proposed in
`CHANGELOG.md`: one `vMAJOR.MINOR.PATCH` for the repository, in `VERSION`, an annotated tag and the
changelog; 0.x while nothing is reviewed; minor for a milestone (a volume's Meaning boxes, a data layer),
patch for fixes; 1.0.0 at the first reviewed volume with the licence settled. Retroactive tags proposed:
v0.1.0 `9d5203d`, v0.2.0 `e2e32b5`, v0.3.0 `493b459`, v0.4.0 `571f566`, v0.5.0 `b7881c4`, v0.6.0 `5db316f`;
this push v0.7.0. None created: tags are Angel's (git runs in his Terminal). The site does not yet show
the version.

*This session ran one read-only `git log -1` in the Cowork VM by mistake (against the rule); no
`index.lock` was left.*


## 43. Vols. 4/1 and 4/2 drafted; the site's footer, citations and cross-references; labels reviewed (27 September 2026, later)

**Angel pushed §42 and created the tags v0.1.0–v0.7.0.** The scheme of `CHANGELOG.md` is in use; this
work is v0.8.0 (`VERSION`). The live site showed vol. 3's Meaning boxes (`/w/abyākata`, checked in the
in-app browser).

**`abhidhana_meanings.py prep` catches more "see X".** From vol. 4/1 (`LEGACY = {'01', '02', '03'}` keeps
the first pattern, so `prep 01–03` reproduce their working files byte for byte; checked on 03): a sense
marker or label before the formula ("(စ) X-ကြည့်"), a sense after X ("X-(၂)-ကြည့်", "X-(၁-က)-ကြည့်",
rendered *Véase X (2)*, *(1-a)*), the whole formula in brackets, and "လည်း-ကြည့်". In 4/1 the formulas rose
from 1,180 to 1,290 and the residual "ကြည့်" rows fell from 218 to 126; in 4/2 from 942 to 1,232 and from
464 to 217. What remains is mostly X with a variant in brackets ("X(ယ)-ကြည့်"), "see the preceding
headword", and "see the original"; the drafts render those by hand, flagged. A `report` step now writes
`<book>-flags.tsv` and `<book>-terms.tsv` (the code used by hand for vol. 3).

**`drafting-brief.md` clarified**: rule 6 now says what the vol. 3 prompt said (Pāḷi already in Pāḷi form is
copied as ⟦Burmese⟧; ⟦=iast⟧ only for a Burmese loanword form such as ဈာန်, မဂ်, ကိလေသာ, ကံ); `terms` lists
both kinds (as vol. 3 did); a list "ကုသိုလ်,အကုသိုလ်" takes *o* (*sano o insano*).

**Vols. 4/1 and 4/2 drafted**, from PCED, 16 + 14 shards of ~446 / ~474 lines, one agent and one scratch
folder each (20 at once, then 10). Checked after: one line per id in order, valid JSON, every «Sn» in both
languages, brackets balanced; 30 rows keep Burmese outside ⟦ ⟧ (plant and other names, and the source tag
(သျ)), all flagged.

| | vol. 4/1 (4a) | vol. 4/2 (4b) |
|---|---:|---:|
| rows (every article with a definition) | 7,519 | 6,654 |
| by formula / drafted | 397 / 7,122 | 25 / 6,629 |
| from PCED / from our OCR | 7,515 / 4 | 6,652 / 2 |
| flagged (`meanings/NN-flags.tsv`) | 409 | 872 |
| terms kept in Pāḷi | 751 | 575 |
| "see X" links matching a romanised headword | 1,355 of 1,404 (96.5%) | 1,228 of 1,315 (93.4%) |
| *sano/insano* rows; "no saludable" | 53; 0 | 47; 0 |

One explanation per book has no row (both languages empty: a definition that is only citations, e.g. 27730
ācayagāmisutta). 4/2 is flagged twice as often: its shards flagged every row whose verb person was taken from
the Pāḷi ending, (သျ) tags (an abbreviation in neither table; dropped as a citation, a guess), and more
"see the original" notes.

**What the agents reported for the reviewer** (nothing reviewed):
- **Colloquial ကုသိုလ်**: 27529 āgantukāgāra, "a guest house built as a work of merit", came out *sano*: the
  glossary rule reads wrongly where ကုသိုလ်ဖြစ် means "meritorious". A rule for Angel. 28891
  āpattikusalatā (kusala = skilled) was rendered by sense.
- **Recurring choices to fix as stems**: ဥတု kept Pāḷi where it means temperature, *estación* for seasons
  (shard 4a/14, ~60 rows); လုံ့လဝီရိယ *esfuerzo (vīriya)*; နတ် *deidad* in some shards, ⟦=deva⟧ in others;
  ရဟန်း *monje*; ပယ် and သုံးသပ် (*palpar* / *considerar*); plant names identified tentatively (သျှစ်သျှား
  *mirobálano*, အာလူး *patata* for āluva) or left in Burmese.
- **Definitions that look shifted or wrong** (for the image): 35125/35127 (udayabbaya(ā)manasikāra glosses
  swapped), 35655, 35672, 35780, 36386, 37845, 38313, 38337, 38638, 41050 ussāsa "excrement", 40165 (a missing
  negation), 31346 āsava glossed as the deity Āsā, 33026 uggacchati "subsides".
- **Truncated articles with "see the original"**: 29995 ārammaṇa, 35075 udaya, 39125 uposatha, 31730 āḷavaka.
- **Verb person**: the Burmese does not mark it; 4/2's shards took it from the Pāḷi ending and are not all
  consistent (အံ့ 1st vs 3rd person in 38094 / 38119).

**The site** (asked by Angel; built on vols. 1 and 4/1 in the cloud container and tested with Playwright at
1,440 and 390 px, light and dark, ES: no script errors, no horizontal scroll):
- **IEBH footer on every page** (`common.js` `footHTML()`, appended to each `footer.site-foot`; Browse adds one
  at the end of each article): the IEBH imagotype (the SVGs of gramaticas.buddha-dhamma.net, from
  `bthar-mx/gramaticas-pali-es/site/assets`, granate and white for dark mode), related sites
  (buddha-dhamma.net, gramaticas.buddha-dhamma.net), repository, licences (MIT; CC BY-SA 4.0 for the
  additions; the dictionary's text not relicensed), and the version from `<meta name="version">`, linked to
  the changelog. `stamp_version()` now writes only the meta and `data/version.json`. The old footers of
  Volumes, About and Abbreviations are replaced; the reader keeps its own credit line above the block.
  *The logo reads "Instituto de Estudios Buddhistas Hispano", as gramaticas does; the rest of this site
  (About, README) writes "Budistas". The footer follows the logo; Angel to say which is right.*
- **Back-to-top button** (↑, bottom right) on every page, shown after 400 px of scroll in the window or in
  Browse's article pane.
- **"Análisis"**, without the "PCED" chip: it is the dictionary's own analysis (Angel). PCED is now described
  where it belongs, in a new **Typed witnesses / Testigos mecanografiados** section of About (what it is, how
  it was joined and measured, what the site takes from it, its unstated licence), with Pn Daza's typed text.
- **Cross-references in the Burmese definition are links**: a "see X" span links to X's article, in all three
  scripts (vol. 4/1 test: iṭṭhamajjhattārammaṇa → iṭṭha).
- **Citation tooltips**: hovering a citation shows the work and the location, *Abhidhamma Aṭṭhakathā · tomo 1,
  página 314* (EN *vol. 1, p. 314*), the format of gramaticas' Kaccāyana pages (`generar_capitulo.py`,
  "{obra} · tomo {tomo}, página {pag}"); the click note shows the same. The first number is taken as the
  volume and the second as the page (brief §36); one number is shown as a page; other shapes as printed.
  Abbreviations not in vol. 1's table get no tooltip (e.g. မဏိမဉ္စူ).
- **Mode bar**: "Modo de lectura:" is a label (it was taken for a button); the page switch reads
  *Mostrar / Ocultar la página impresa*. It is not redundant with "Como está impreso": that mode is a preset
  (Burmese script, definition shown, page on); the switch shows the page in any mode.

**Labels (Angel, 27 Sep)**: *sustantivo* → *nombre* in every Spanish label (and in the Introduction ch. 5
and `batch01-review.md`); (ကြိ၊ဝိ) without "infinitivo"; (နာမ-ကြိ) *nāmadhātu*, *verbo denominativo, verbo
nominal*; (စတုတ္ထန္တ) *voz terminada en la cuarta inflexión*; (တတိယန္တ-ဗျ) *tatiyanta abyaya*, *indeclinable
terminado en la tercera inflexión*. Those rows (16) are `confirmed` with their Spanish; the others keep their
status. The (ကြိ၊ဝိ) Spanish still lists *-tuṁ* among its forms: Angel removed only the word.
