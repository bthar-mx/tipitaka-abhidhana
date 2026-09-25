# A second copy of the typed text: Pn Daza's `dict.db`

*25 September 2026. Examined by the first Cowork chat. The file is kept at
`witness/pndaza-dict.db` (gitignored; SHA-256
`0ecd56a941ba872aa60f2556580ed74b4de153043004e64e7c9a0b7f2b056812`, 101,799,936 bytes).*

## 1. Where it comes from

The database of Pn Daza's Android app **Pali-Myanmar Dictionary**,
[github.com/pndaza/pali-myanmar-dictionary](https://github.com/pndaza/pali-myanmar-dictionary),
downloaded by Angel from the Google Drive link in its README
(`drive.google.com/open?id=1xAAMVPrIBPpmb7VeI1k_Zl9WiTgwoVY8`). The README says the app combines the
Tipiṭaka dictionary, U Hut Sein's dictionary and Merit Sharer's Pali Myanmar Dictionary, credits
**ဆရာတော် ဦးဣန္ဒောဘာသ** for the iOS dictionary and **Merit Sharer** for theirs, and uses MDetect and
Rabbit Converter. **No licence is stated anywhere**: the repo has no LICENSE file and no
licence in its metadata, and the database itself has no metadata table and no credit or
copyright text in any entry (checked 25 Sep 2026). There are only the names above. Without a
licence, nothing grants permission to reuse the text, so permission has to be asked.

## 2. What is in it

One table, `define(_id, zword, uword, content, book)`: `zword` is the headword in Zawgyi, `uword`
the headword in Unicode (Pn Daza's conversion), `content` the whole entry in **Zawgyi**.

| `book` | entries | what it is (from the content) |
|---|---:|---|
| 1 | **158,542** | the **Tipiṭaka Pāḷi-Myanmā Abhidhāna**: headword (label) / [analysis] / definition / `တိပိ၊vol၊page` |
| 2 | 60,774 | U Hut Sein's Pāḷi-Myanmar dictionary (Burmese with English glosses) |
| 3 | 11,085 | a roots dictionary (entries of the form `[√root+suffix]`, citing Dhātvatthadīpanī-ṭīkā) |
| 4 | 1,893 | a verb-root list (`ဘူ = …`); probably Merit Sharer's |

## 3. Book 1 is the same typing as PCED's dictionary K

Matched on the Unicode headword against `witness/pced_k.jsonl` (the new chat's conversion of
PCED 1.94, dictionary K), then compared on the Zawgyi source text with whitespace, punctuation,
brackets and the trailing page reference removed:

| | |
|---|---:|
| book-1 entries | 158,542 |
| headword also in PCED K | 156,122 |
| **source text identical** | **153,636 = 98.4%** |
| not identical | 2,486, median similarity 0.98 (2,286 at ≥ 0.95) |

So `dict.db` and PCED are **one typing, not two**. It is not an independent witness to PCED:
where they agree, that confirms the copying, not the text. The small differences are edits or
corruption in one copy or the other, not a second reading.

## 4. What it adds that PCED does not: the page reference

**156,679 of 158,542 book-1 entries (98.8%) end with a reference `တိပိ၊vol၊page`** (e.g.
`တိပိ၊၁၊၁၈၀` for accāvadati, vol. 1 printed p. 180 = PDF p. 300). PCED keeps it on only 370
entries. Checked against the app's index (`db/tipitaka_abidan.db`):

| book | typed entries with a ref | headword in the index for that book | on the **same page** | index headwords covered |
|---|---:|---:|---:|---:|
| 01 | 8,149 | 99.8% | 100.0% | 99.8% |
| 02 | 7,189 | 99.7% | 100.0% | 99.6% |
| 03 | 11,726 | 99.6% | 100.0% | 99.6% |
| 4a | 7,520 | 99.6% | 100.0% | 99.6% |
| 4b | 6,654 | 99.2% | 100.0% | 99.2% |
| 05–19 | 5,218–11,425 each | 97.5–99.8% | 100.0% | 97.4–99.8% |

(The vol. field reads 4က and 4ခ for 4a and 4b. Some refs span pages: `၂+၃+၄`.)

- **Coverage** is vols 1–19 without 4c, 14b, 14c, the same as PCED, and the same as the split in
  `docs/app-info.html` between the Buddhasetaman iOS app (vols 1–19) and the volumes added later.
  This supports the new chat's inference that the typed text came from that iOS app.
- **The index and the typed text share an origin.** The typed entry counts match the index row
  counts almost exactly (vol. 1: 8,149 typed, 8,150 index rows), and every matched headword sits on
  the same page. The index was very likely built from this typed data. So for vols 1–19 the typed
  headwords are **not independent of the index**; the typed definitions **are** independent of
  our OCR.
- **What the page reference makes possible:** every typed article can be tied to its volume and
  page directly, so joining it to our OCR'd page records, and to the PDF page for checking, no
  longer depends on headword matching alone. Homographs (several entries with one headword, e.g.
  the five အ) can be told apart by page.

## 5. Headwords not in PCED

2,420 book-1 headwords (Pn Daza's Unicode) are not among PCED K's converted headwords, e.g.
ကတ္တုသဋ္ဌေ, ကမ္မသဋ္ဌေ. Many look like **conversion differences** in the ṭṭh + e cluster, which the
new chat's `tools/zawgyi.py` treats differently. Not checked: they may be spelling differences,
not extra entries.

## 6. What to do with it

1. Use `dict.db` book 1 **in place of or beside PCED K** as the typed witness: same text, plus
   page references and Pn Daza's Unicode headwords.
2. Join typed articles to OCR articles **by (book, page, headword)**, not headword alone.
3. Check the 2,420 unmatched headwords and the 2,486 non-identical texts: which copy is right?
   The page decides.
4. Books 2–4 are other dictionaries (U Hut Sein, roots). Useful for cross-checking meanings, not
   as witnesses to this dictionary.
5. **Provenance and permission:** ask Pn Daza who typed the text (Sayadaw U Indobhāsa? the
   Buddhasetaman group? Merit Sharer?) and on what terms it can be reused, before publishing text
   taken from it. Credit it in the README as the scans are credited.

## 7. Other places the typed text appears (searched 25 September 2026)

- **PCED 1.94** in `siongui/data`, behind dictionary.sutta.org: see `docs/witness.md`.
- **tipitakapali.org** lists a "Tipiṭaka Pāḷi–Myanmar Abhidhān, adapted from Ven. Pn Daza's
  Tipiṭaka App" (https://tipitakapali.org/info). Probably the same text; not checked.
- **iPaliMM Dictionary** by Merit Sharer (iOS, 2019, Zawgyi): a Pali-Myanmar dictionary app;
  contents not downloadable.
- **dxcore35/massive_Pali-dictionary** lists the dictionary but holds no data; its list of four
  Myanmar dictionaries matches PCED's.
- **Pāḷi-English Ultimate (PEU)**, in the Digital Pāḷi Dictionary's "other dictionaries" and in
  Tipitaka Pali Reader: an English version based on the "Pali Myanmar Abhidhan" ("23 volumes, more
  than 200,000 words"). English, so not a witness to the Burmese; possibly useful for meaning.
- **Official English translation** by the International Theravada Buddhist Missionary University
  for the Ministry of Religious Affairs (Ministry of Information news, 25 Nov 2024): vols 1–4
  published (7,236 entries), later volumes in progress; print only, and apparently a selection.

No born-digital edition from the Ministry was found. **14b.pdf** is the one volume whose PDF is
typeset text (legacy Win-Burmese fonts), not a scan.

## 8. Joined to the articles, and the unmatched headwords checked (25 September 2026, second chat)

`tools/abhidhana_witness_pndaza.py` converts book 1 with `tools/zawgyi.py` (the converter used for
PCED, so the two witnesses are spelled alike) into `witness/pndaza_k.jsonl` (gitignored): id,
headword (our conversion of `zword`), `uword` (Pn Daza's), label, analysis, definition, and the
reference as book and index page. 156,670 of 158,542 entries carry a usable reference.

**The join is by book, index page and headword**: an index row is paired with the typed entries
filed under the same book and page with the same headword, homographs on one page in order; the
headword is compared as our conversion, then as `uword`, then folded. Output:
`witness/pjoin-NN.jsonl`, and these figures (vols. 1–15, as far as the OCR has gone):

| vol. | index rows | paired by book, page, headword | of which by uword / folded | labels: both / agree | analyses: both / ≥ 0.8 / < 0.4 | bodies: both / ≥ 0.8 | unlocated articles with a typed text |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 | 8,150 | 8,148 (100.0%) | 0 / 3 | 7,272 / **98.8%** | 5,947 / 85.0% / 1.5% | 7,637 / 55.0% | 457 |
| 02 | 7,189 | 7,188 (100.0%) | 0 / 7 | 6,350 / **99.0%** | 5,705 / 90.8% / 0.6% | 6,712 / 58.3% | 461 |
| 03 | 11,726 | 11,726 (100.0%) | 0 / 26 | 10,505 / **98.7%** | 9,168 / 90.8% / 0.8% | 11,097 / 65.6% | 612 |
| 4a | 7,524 | 7,519 (99.9%) | 0 / 5 | 6,392 / **99.0%** | 5,425 / 87.2% / 0.6% | 6,888 / 62.9% | 581 |
| 4b | 6,655 | 6,653 (100.0%) | 0 / 23 | 6,063 / **99.0%** | 5,369 / 95.3% / 0.2% | 6,428 / 72.5% | 218 |
| 05 | 8,015 | 8,012 (100.0%) | 0 / 7 | 7,031 / **99.4%** | 6,095 / 91.6% / 0.6% | 7,490 / 63.1% | 513 |
| 06 | 11,429 | 11,424 (100.0%) | 0 / 11 | 9,862 / **99.4%** | 8,776 / 90.6% / 0.4% | 10,500 / 64.7% | 911 |
| 07 | 6,877 | 6,876 (100.0%) | 0 / 10 | 6,003 / **98.9%** | 5,229 / 91.7% / 0.6% | 6,394 / 64.0% | 477 |
| 08 | 6,448 | 6,443 (99.9%) | 0 / 5 | 5,655 / **99.1%** | 4,948 / 90.3% / 0.7% | 5,931 / 67.4% | 507 |
| 09 | 6,805 | 6,804 (100.0%) | 0 / 5 | 5,850 / **98.6%** | 5,177 / 90.0% / 0.5% | 6,285 / 61.7% | 510 |
| 10 | 7,366 | 7,362 (99.9%) | 0 / 2 | 6,204 / **99.0%** | 5,450 / 90.4% / 0.5% | 6,677 / 62.8% | 677 |
| 11 | 5,663 | 5,662 (100.0%) | 0 / 2 | 4,882 / **98.5%** | 4,253 / 86.9% / 0.7% | 5,257 / 64.5% | 399 |
| 12 | 7,022 | 7,020 (100.0%) | 0 / 9 | 6,440 / **98.7%** | 5,658 / 97.2% / 0.2% | 6,784 / 76.7% | 220 |
| 13 | 7,279 | 7,279 (100.0%) | 0 / 6 | 6,095 / **99.3%** | 5,324 / 89.4% / 0.3% | 6,504 / 64.0% | 767 |
| 14 | 5,219 | 5,218 (100.0%) | 0 / 2 | 4,814 / **99.4%** | 3,131 / 95.3% / 0.2% | 5,036 / 54.8% | 175 |
| 15 | 9,342 | 9,342 (100.0%) | 0 / 8 | 8,182 / **99.4%** | 7,092 / 87.8% / 0.5% | 8,701 / 64.6% | 616 |

- It pairs 99.9–100% of index rows, and **agrees with the headword-only join to PCED**
  (`docs/witness-join.md`) on 122,639 rows; 37 rows are paired only here, 24 only there, 9 by
  neither. Where both pair, the label verdict differs on 9 rows and the analysis ratio by more
  than 0.3 on 12. So the page reference confirms the earlier pairing rather than changing it; its
  value is that it no longer depends on headword order among homographs.
- **The last column is what the witness adds**: an unlocated article (the OCR could not place
  its headword) with a typed text on the right page, 175–911 per volume, 8,101 in vols. 1–15.
  Their text can be offered privately, marked as typed, not read.
- Labels agree on 98.5–99.4%, as against PCED.

**The 2,406 distinct `uword`s not among PCED K's headwords** (2,420 counted on entries in §5) are:

| | `uword`s | what they are |
|---|---:|---|
| entries for **books 14c, 21, 22, 23, 24, 25**, without a page reference | ≈ 1,550 | 375 in vol. 24, 363 in 22, 348 in 23, 255 in 14c, 166 in 21, 40 in 25 (by the index's book for the headword). They are index headwords; PCED has none of them. The 1,871 book-1 entries without a reference are nearly all these. A partial typing of the later volumes, then: not a witness to those books' pages, but to some of their headwords and texts |
| **Pn Daza's conversion** differs, ours does not | 582 | e before a ligature: `ကတ္တုသဋ္ဌေ` for ကတ္တုသေဋ္ဌ (423), `ဿ` misplaced (156). In 581 of the 582 our conversion is the index's spelling and `uword` is not: **the index and PCED side agree; Pn Daza's Unicode headword is wrong** |
| PCED's headword glued to what follows it | ≈ 30 | a label typed without its "(" (`ခန္တိဉာဏ န)`), or a note run on, which `abhidhana_witness.py` read as part of the PCED headword; the entries are there |
| in neither PCED nor the index | 241 | several headwords typed as one (`ဂုလာ,ဂုလာဂဏ္ဌိက,…`), a variant in brackets (`ကာမဂုဏူပ(သဉှိတ)`), damaged text, and some later-volume headwords spelled otherwise |

So the unmatched headwords are not conversion errors of ours: they are mostly entries PCED never
had, for volumes neither witness covers by page.

