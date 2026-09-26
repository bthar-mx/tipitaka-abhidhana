# Errata in the app's index (`db/tipitaka_abidan.db`)

*Started 25 September 2026. The index is the project's ground truth for **which** headwords there
are (brief §3), but not always for their spelling or their page. Each entry below was found by
the pipeline and checked, on the page image unless it says otherwise. The corrections the
pipeline applies are in `tools/abhidhana_articles.py` (`PAGE_FIX`, `ID_PAGE_FIX`); the index
itself is never edited. Spelling errors are not corrected anywhere yet: the fuzzy alignment
places most of those headwords, and a row keeps the index's spelling in `headword`.*

Printed page numbers are the index's (`words.page_number`); PDF pages are `page_number +
books.start_page`, unless corrected here.

## 1. Pages: the index points to the wrong page

| book | ids | index says | printed on (PDF p.) | how found / checked | applied |
|---|---|---|---|---|---|
| 21 | 170346–170355 (10) | p. **962** | p. 692 = PDF 720 | transposed digits; PDF 720 prints ၆၉၂ with exactly these ten (image) | `ID_PAGE_FIX` |
| 22 | all of index pp. 880–894 | PDF 920–934 | one PDF page earlier | a printed page is **missing from the scan** before PDF 920; PDF 919 has p. 920's list 9/9, 2/11 of its own; the PDF has 933 pages, the index implies 934 (text) | `PAGE_FIX` |
| 4c | 176418–176427 (10) | PDF 615 | PDF 613 | unindexed page, entries begin with them (text, brief §16) | `ID_PAGE_FIX` |
| 06 | 58264–58277 (14) | PDF 851 | PDF 852 | same (image) | `ID_PAGE_FIX` |
| 14c | 196222–196234, 197721–197732, 198200–198207, 201263–201269, 201325–201334, 201634–201646 | the page before | PDF 402, 565, 625, 930, 936, 962 | unindexed pages whose entries begin with a neighbour's unlocated headwords (text) | `ID_PAGE_FIX` |
| 22 | 178676–178682, 178835–178847, 179577–179585, 185264–185267 | the page before | PDF 169, 184, 253, 894 | same (text) | `ID_PAGE_FIX` |
| 23 | 187848–187857, 187871–187878, 189039–189048, 189502–189513, 190351–190359 | the page before | PDF 275, 277, 390, 436, 523 | same (text) | `ID_PAGE_FIX` |
| 24 | 206034–206036 | the page before | PDF 329 | same (text) | `ID_PAGE_FIX` |
| 24 | 208187–208194 (8) | PDF 540 | PDF 542 | p. 540 prints only the long article သုမန², which runs to p. 542 (image, spot check) | `ID_PAGE_FIX` |
| 14c | 198064–198070 (7), 198090–198096 (7), 198166–198168 (3), 201781–201786 (6) | the page before | PDF 605, 608, 621, 976 (printed ၅၇၈, ၅၈၁, ၅၉၄, ၉၄၉) | unindexed pages; each begins with exactly these headwords (image, 25 Sep 2026) | `ID_PAGE_FIX` |
| 10 | 81975 (ဒသ²) | PDF 220 | PDF 219 (printed ၁၇၁) | of the index's four ဒသ for p. 172, the first is printed on p. 171; ဒသ¹ on PDF 218, ဒသ³⁻⁵ on 220 (image, 25 Sep 2026) | `ID_PAGE_FIX` |
| 18 | 146728–146731 (ဝသ²⁻⁵) | PDF 816 | PDF 816: **the index is right** | PDF 815 is wholly inside ဝသ¹; 816 prints ဝသ²⁻⁵ (image, 25 Sep 2026) | none needed |
| 02 | — | PDF 241 / 242 | 242 / 241 | pages bound out of order in the scan, not an index error (brief §13) | `PAGE_FIX` |

**Candidates checked on the image, 25 Sep 2026.** The weak candidates (14c 201781–201786, 198069–198070;
18 146728–146731; 10 81975–81976) and 14c pp. 564, 607, 620 are resolved in the table above: 14c p. 564
was already covered by 197721–197732 → 565; the 14c run at p. 605 is seven headwords, not two; vol. 10
needs only one of its two; vol. 18 needs none.

## 2. Headwords belonging to another volume

- **Book 13, index pp. 145–160 (PDF 175–190)**: 232 headwords, ids 102092–102323, ဗလိ …
  ဗဟိဒ္ဓါသမုဋ္ဌာန, are vol. 15's ဗ headwords; these pages print ပဂ္ဂဏှာထ … ပဂ္ဃရဏလက္ခဏ. Pn Daza's
  typed text has the same error, so it was made in the typing the index was built from
  (`docs/witness-pndaza.md` §4). The real headwords of these sixteen pages are in no source but
  our OCR. Not corrected: the 232 rows stay unlocated in vol. 13.
- **Book 4c, index pp. 686–708 (PDF 713–735)**: 223 headwords of supplements to vols. 15, 4/2 and
  16, bound after vol. 4/3 and indexed under it (brief §16). Correctly placed, but **the 53 ဘိဇ္ဇ
  headwords of the vol. 15 supplement are indexed only there**.

## 3. Spelling: the index spells the headword differently from the print

| book | id(s) | index | print | checked |
|---|---|---|---|---|
| 23 | 186075–186085 (index pp. 65–66, PDF 100–101) | အမ္မဝါဒ…, အမ္မဝါယာမ… | သမ္မာဝါဒ…, သမ္မာဝါယာမ… | image, p. 100 |
| 23 | 186076 | …ပတဋ္ဌာပန | …ပတိဋ္ဌာပန | image |
| 14c | 198058 | ပိဏ္ဍစရဏဝီရိယ | ပိဏ္ဍပါတစရဏဝီရိယ | image, PDF 604 |
| 14c | 198068 | ပိဏ္ဍပါတနီဟရဏ | ပိဏ္ဍပါတနီဟရက | image, PDF 605 |
| 14c | 198083 | ပိဏ္ဍပလိဗောဓ | ပိဏ္ဍပါတပလိဗောဓ | image, PDF 607 |
| 14c | 198088 | ပိဏ္ဍပါတဘောဇန (the index has it twice; the second, 198091, is right) | ပိဏ္ဍပါတဘာဇန | image, PDF 607–608 |
| 14c | 198164 | ပိဟာမဟဒွန္ဒ | ပိတာမဟဒွန္ဒ | image, PDF 620 |
| 10 | 81979 | ဒသအကုလလကမ္မပထ | ဒသအကုသလ(ဒသာကုသလ)ကမ္မပထ | image, PDF 220 |
| 23 | 188777 | အဟဿအဿာဇာနီယ | presumably သဟဿ… | **not checked** |
| 4b | — | ဥဒယဗ္ဗကဉာကပဋိပါဋိ | ဥဒယဗ္ဗယညာဏပဋိပါဋိ | image (brief §15) |
| 4c | — | ဩလမ္ဗတကုလာဝက, ဥဒါနိ, ဥပါဃာတဘူမိ, စကစတုက္ကာဒိကဆတ္တိက (printed ဧကစတုက္ကာဒိကဆတ္တိက, id 172639, PDF p. 85: the editor 26 Sep 2026, corrected via `docs/corrections.tsv`) | the other printed forms not recorded in the brief | image (brief §16) |
| 4c | — | ဧဏိ / ဧဏီ as two bare headwords | one variant entry | image |
| 4c | — | ဥပက္ကိလေသ | no printed entry found | image |
| 05 | — | ကဉ္စိက | ကဉ္ဇိက | image (brief §17) |
| 14b | — | ပရတီိိရ, ပရစိိတ္တဇာနနက | (doubled vowel signs) | text layer |
| 14b | — | ပရိတ္တဇ္စျာန, ပရိပုဏ္ဏဇ္စျာသယ | ဇ္ဈ for ဇ္စျ | text layer |
| 14b | — | ပရိဘိန္ဒသု | ပရိဘိန္ဒိံသု | text layer, p. 600 |

**Systematic, not errors of a single row** (handled by the spelling folds, `tools/abhidhana_fold.py`):
the index writes ါ where the print writes ာ after a stacked consonant (vols. 3, 4/2, 22), and ဉာ
where 4b and 22 print ညာ.

## 4. Counts

- The title page of vol. 4/3 prints 5,163 entries; the index has 5,007 for 4/3 itself and 223 for
  the supplements. Unexplained. The other volumes' title pages are not yet compared.
- Vol. 22: the headwords of the page missing from the scan (about 11, those of the index's p. 879 /
  PDF 919 list not found there) are lost unless another copy of the page is found
  (`pdfs-drive/` has no vol. 22).
