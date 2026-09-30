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
| 14c | 196602 | ပါပတရ (a second row; the first, 196510, is right) | ပါပရတ | image, PDF 440 (29 Sep, brief §73) |
| 14c | 196606 | ပါပရာဂီ | ပါပရောဂီ | image, PDF 440 (§73) |
| 14c | 196644 | ပါပဘိက္ခမာနာ | ပါပသိက္ခမာနာ | image, PDF 444 (§73) |
| 14b | 216840 | ပလိဂိဇ္စျေယျ | ပလိဂိဇ္ဈေယျ | image, PDF 916 (§73) |
| 14b | 212175 | ပရိကီဠိနာ | ပရိကီဠနာ | image, PDF 298 (§69, §73) |
| 14b | 210262 | ပမာဏဝတ္ထာန | ပမာဏဝဝတ္ထာန | image, PDF 40 (§69, §73) |
| 20 | 163326 | သံယုတ္တနိကာယဝရလဉ္ဇက | သံယုတ္တနိကာယဝရလဉ္ဆက | image, PDF 860 (§69, §73) |
| 23 | 190856 | သာလကိယ | သာလာကိယ | image, PDF 582 (§69, §73) |
| 20 | 156798 | ဝိသံသဋ္ဌဘာဝ | ဝိသံသဋ္ဌာဘာဝ | image, PDF 41 (29 Sep, brief §74) |
| 20 | 158654 | ဝိဟာရဘတ္တကောဋိ | ဝိဟာရဘိတ္တိကောဋိ | image, PDF 262 (§73–74) |
| 14c | 201391 | ပုရိမကာလဘတ္တ | ပုရိမကာလတ္ထ | image, PDF 943 (§74) |
| 14c | 201598 | ပုရိမယဿ | ပုရိမယသ | image, PDF 959 (§74) |
| 16 | 124782 | မတကသတ္တသင်္ခေပ | မတကဘတ္တသင်္ခေပ | image, PDF 207 (§74) |
| 16 | 125634 | မနုဿရာမဏေယျက | မနုဿရာဟသေယျက | image, PDF 273 (§74) |
| 21 | 167023 | သင်္ဂါမပ္ပဘေဒ | သင်္ဂါမပ္ပဒေသ | image, PDF 347 (§74) |
| 22 | 178400 | သဗ္ဗကိစ္စကာရက | သဗ္ဗကိစ္စသာဓက (medium confidence: by its place between the neighbours) | image, PDF 145 (§74) |
| 22 | 179634 | သဗ္ဗာသဝဟာရ | သဗ္ဗာဟာရ | image, PDF 258 (§74) |
| 22 | 181000 | သမပညာသပုစ္ဆနာ | သမပညာသမုစ္ဆနာ | image, PDF 394 (§74) |
| 4c | 176808 | ဩသက္ကိတောသဏ္ဍိတဋ္ဌာန | ဩသက္ကိတောသက္ကိတဋ္ဌာန | image, PDF 662 (§74) |
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
| 4c | — | ဩလမ္ဗတကုလာဝက, ဥဒါနိ (177260, below), ဥပါဃာတဘူမိ (177269, below), စကစတုက္ကာဒိကဆတ္တိက (printed ဧကစတုက္ကာဒိကဆတ္တိက, id 172639, PDF p. 85: the editor 26 Sep 2026, corrected via `docs/corrections.tsv`) | the other printed forms not recorded in the brief | image (brief §16) |
| 4c | — | ဧဏိ / ဧဏီ as two bare headwords | one variant entry | image |
| 4c | 177266 | ဥပက္ကိလေသ | no printed entry found (no article of its own: below) | image |
| 05 | — | ကဉ္စိက | ကဉ္ဇိက | image (brief §17) |
| 14b | — | ပရတီိိရ, ပရစိိတ္တဇာနနက | (doubled vowel signs) | text layer |
| 14b | — | ပရိတ္တဇ္စျာန, ပရိပုဏ္ဏဇ္စျာသယ | ဇ္ဈ for ဇ္စျ | text layer |
| 14b | — | ပရိဘိန္ဒသု | ပရိဘိန္ဒိံသု | text layer, p. 600 |
| 21 | 170596 | သဒ္ဒကဏ္ဍက | သဒ္ဒကဏ္ဋက | image, PDF 747 (30 Sep, brief §85 §3) |
| 14c | 197306–197308 | ပါရေဝတက္ခိ, ပါရေဝတက္ခိ, ပါရေဝတက္ခီ | ပါရေဝတက္ခီ¹, ပါရေဝတက္ခီ², ပါရေဝတက္ခိ (the index's ခိ / ခီ in the wrong rows) | image, PDF 517 (§85 §3) |
| 20 | 161196 | ဝေဒနိယ | ဝေဒနီယ¹ (so the run of ဝေဒနီယ, 161197–, begins at ²) | image, PDF 570 (§85 §3) |

### 4c: the supplements bound after vol. 4/3 (from §79)

*From brief §79, where each was read on the page images (4c PDF pp. 721–735); copied here from `tools/abhidhana_supplements.py`
(`PRINTED`, `SAME_AS`, `NOTES`) and `docs/supplements.tsv`, not re-checked (brief §80). The script places each row by its printed
form; the data keeps the index's spelling. "Vol." is the volume the supplement belongs to. The printed form is in Burmese where §79
recorded it; otherwise in IAST only, as the script holds it.*

| id | vol. | index | print | 4c PDF p. |
|---|---|---|---|---|
| 177260 | 4/2 | ဥဒါနိ (*udāni*) | *udānita* (IAST; Burmese not recorded) | 721 |
| 177267 | 4/2 | ဥပက္ကိလေသမုစ္ဆေဒ (*upakkilesamuccheda*) | ဥပက္ကိလေသသမုစ္ဆေဒ (*upakkilesasamuccheda*) | 721 |
| 177269 | 4/2 | ဥပါဃာတဘူမိ (*upāghātabhūmi*) | ဥပဃာတဘူမိ (*upaghātabhūmi*) | 721 |
| 177277 | 4/2 | ဥပဇ္ဈယိနီ (*upajjhayinī*) | *upajjhāyinī* (IAST; Burmese not recorded) | 722 |
| 177282 | 4/2 | ဥပါနာဟက (*upānāhaka*) | ဥပနာဟက (*upanāhaka*) | 723 |
| 177287 | 4/2 | ဥပပက္ကလေသမုစ္ဆေဒ (*upapakkalesamuccheda*) | ဥပပက္ကိလေသသမုစ္ဆေဒ (*upapakkilesasamuccheda*) — a "see" entry | 723 |
| 177300 | 4/2 | ဥပနန္တ (*upananta*) | ဥပဝနန္တ (*upavananta*) | 724 |
| 177305 | 4/2 | ဥပဝိယတိ (*upaviyati*) | *upavīyati* (IAST; Burmese not recorded) | 724 |
| 177307 | 4/2 | ဥပသေဝန (*upasevana*) | ဥပဝေသန (*upavesana*) | 724 |
| 177314 | 4/2 | ဥပသမ္ပဒါဒျ (*upasampadādya*) | *upasampādya* (IAST; Burmese not recorded) | 725 |
| 177326 | 4/2 | ဥပါနာဟက (*upānāhaka*) | ဥပါန (*upāna*) — the index repeats 177282's spelling | 726 |
| 177327 | 4/2 | ဥပါဒန္တဘူ (*upādantabhū*) | ဥပါန္တဘူ (*upāntabhū*) | 726 |
| 177332 | 4/2 | ဥပါဝတ္ထ (*upāvattha*) | *upāvatta* (IAST; Burmese not recorded) | 726 |
| 177336 | 4/2 | ဥပေက္ခိယ (*upekkhiya*) | *upekkhikā* (IAST; Burmese not recorded) | 727 |
| 177337 | 4/2 | ဥပေယမာ (*upeyamā*) | *upeyamāna* (IAST; Burmese not recorded) | 727 |
| 177338 | 4/2 | ဥပ္ပဇ္ဇန္ဇိ (*uppajjanji*) | *uppajjantī* (IAST; Burmese not recorded) | 727 |
| 177343 | 4/2 | ဥဗ္ဗဋ (*ubbaṭa*) | *ubbaṭṭa* (IAST; Burmese not recorded) | 727 |
| 177344 | 4/2 | ဥဗ္ဗဋဗီဇက (*ubbaṭabījaka*) | *ubbaṭṭabījaka* (IAST; Burmese not recorded) | 727 |
| 177368 | 4/2 | ဥဿိဉ္ဇန္တိ (*ussiñjanti*) | *ussiñcanti* (IAST; Burmese not recorded) | 730 |
| 177373 | 16 | မံသကာရဏ (*maṁsakāraṇa*) | မံကာရဏ (*maṁkāraṇa*) | 731 |
| 177389 | 16 | မာဲဏိဝရ (*māaiṇivara*) | *māṇivara* (IAST; Burmese not recorded) | 732 |
| 177424 | 16 | မေဒက (*medaka*) | မောဒက (*modaka*) | 735 |

**Index rows and printed articles that do not match one to one** (from §79): four index rows have no article of their own and are
placed with the article they belong to (`SAME_AS`); one index row covers two printed articles.

| id | vol. | index | §79's note | 4c PDF p. |
|---|---|---|---|---|
| 177266 | 4/2 | ဥပက္ကိလေသ (*upakkilesa*) | no article of its own on p. 721: the page prints ဥပက္ကိလေသသမုစ္ဆေဒ (177267); placed with it | 721 |
| 177350 | 4/2 | ဥဗ္ဘံ (*ubbhaṁ*) | one printed article with 177349 (ဥဗ္ဘ၊ ဥဗ္ဘံ); placed with it | 728 |
| 177381 | 16 | မဋ္ဋက (*maṭṭaka*) | p. 731 prints one မဋ္ဋက article; the index has two rows (177381, 177382); placed with 177382 | 731 |
| 177402 | 16 | မိယမာန (*miyamāna*) | one printed article with 177401 (မီ(မိ)ယမာန¹); placed with it | 732 |
| 177412 | 16 | မေဃဇ္ဇဝမေဃလ (*meghajjavameghala*) | the index row covers two printed articles, မေဃဇ္ဇဝ and မေဃလ | 734 |

**Systematic, not errors of a single row** (handled by the spelling folds, `tools/abhidhana_fold.py`):
the index writes ါ where the print writes ာ after a stacked consonant (vols. 3, 4/2, 22), and ဉာ
where 4b and 22 print ညာ.

## 4. Counts

- The title page of vol. 4/3 prints 5,163 entries; the index has 5,007 for 4/3 itself and 223 for
  the supplements. Unexplained. The other volumes' title pages are not yet compared.
- Vol. 22: the headwords of the page missing from the scan (about 11, those of the index's p. 879 /
  PDF 919 list not found there) are lost unless another copy of the page is found
  (`pdfs-drive/` has no vol. 22).

## 5. Repeats: the same headword indexed twice, not in adjacent rows

*Added 30 Sep 2026 (plan step 1.8; docs only, nothing applied). An index row whose headword the index gives again within 40 ids, the
two not adjacent, so the homonym runs of brief §85–86 (adjacent ids) do not take them. Found in the text, **not checked on the image**
except where it says so. A repeat may be a duplicate row of one printed entry, or a homonym indexed out of its place (174421 below:
the index lists ဧဓတိ² before ¹, read on the image in §91); not decided row by row. Pages: the index's printed page, the PDF page in brackets.*

**From brief §85 §1: 78 rows** (66 unlocated, 12 stubs or rows with no label / analysis), each at a line start + label on the head line of
the other, same-headword, article (§67's test on the articles of 29 Sep; the ids are `tmp/homonym18/cands.json`'s `flag` entries
`s67x:*`, the same test as §85's `cands.py`; per book as its `s67_nongroup`). 09 80709 has no repeat within 40 ids: its twin 80349 is 360
ids earlier, on the same index page.

| book | id | headword | index p. (PDF) | the other row(s): id, index p. (PDF) | row (brief §67) | from |
|---|---|---|---|---|---|---|
| 01 | 3990 | အဍ္ဎကာသိယ | 347 (467) | 3988, p. 347 (467) | unlocated | §85 §1 |
| 4a | 30424 | အာရောဟနီယ | 372 (414) | 30433, p. 373 (415) | unlocated | §85 §1 |
| 4b | 34785 | ဥဒကဗုဗ္ဗုဠက | 17 (33) | 34808, p. 18 (34) | unlocated | §85 §1 |
| 4b | 37763 | ဥပရိဈာန | 337 (353) | 37758, p. 337 (353) | unlocated | §85 §1 |
| 4b | 39948 | ဥပ္ပိလာဝိတ | 543 (559) | 39950, p. 544 (560) | unlocated | §85 §1 |
| 4b | 40668 | ဥရုဝေဠာ | 611 (627) | 40670, p. 612 (628) | unlocated | §85 §1 |
| 06 | 54423 | ခါရိယ | 511 (533) | 54431, p. 512 (534) | unlocated | §85 §1 |
| 06 | 57960 | ဂါမပတ္တ | 810 (832) | 57957, p. 810 (832) | unlocated | §85 §1 |
| 06 | 57988 | ဂါမပ္ပဝေသန | 811 (833) | 57976, p. 811 (833) | unlocated | §85 §1 |
| 08 | 69199 | ဇဟိံသု | 191 (231) | 69215, p. 192 (232) | unlocated | §85 §1 |
| 09 | 80709 | ထုတပ္ပသတ္ထ | 775 (827) | 80349, p. 775 (827) (360 ids earlier) | unlocated | §85 §1 |
| 10 | 83678 | ဒိဋ္ဌိဂ္ဂဟဏ | 440 (488) | 83676, p. 440 (488) | unlocated | §85 §1 |
| 10 | 87127 | ဒေသနိယမန | 833 (881) | 87119, p. 833 (881) | unlocated | §85 §1 |
| 10 | 87128 | ဒေသနုပါယ | 833 (881) | 87120, p. 833 (881) | unlocated | §85 §1 |
| 10 | 87129 | ဒေသန္တရ | 833 (881) | 87121, p. 833 (881) | unlocated | §85 §1 |
| 10 | 87130 | ဒေသန္တရဂတ | 833 (881) | 87122, p. 833 (881) | unlocated | §85 §1 |
| 10 | 87131 | ဒေသန္တရဂမန | 834 (882) | 87123, p. 834 (882) | unlocated | §85 §1 |
| 10 | 87759 | ဒွါစတ္တာလီသ | 895 (943) | 87765, p. 896 (944) | unlocated | §85 §1 |
| 11 | 93313 | နာသာရဇ္ဇု | 616 (696) | 93330, p. 617 (697) | unlocated | §85 §1 |
| 13 | 106699 | ပဋိဂ္ဂဟေတုံ | 689 (719) | 106705, p. 690 (720) | unlocated | §85 §1 |
| 14 | 109098 | ပဋိသံဝေဒိယန္တိ | 119 (140) | 109087, p. 119 (140) | unlocated | §85 §1 |
| 14 | 109859 | ပဌမ | 223 (244) | 109861, p. 224 (245) | stub | §85 §1 |
| 14c | 192800 | ပဝတ္တကိစ္စ | 11 (38) | 192804, p. 11 (38) | unlocated | §85 §1 |
| 14c | 192802 | ပဝတ္တကာရဏ | 11 (38) | 192798, p. 11 (38) | unlocated | §85 §1 |
| 14c | 192803 | ပဝတ္တကာလ | 11 (38) | 192799, p. 11 (38) | unlocated | §85 §1 |
| 14c | 194655 | ပဿထ | 213 (240) | 194664, p. 213 (240) | unlocated | §85 §1 |
| 14c | 194663 | ပဿ | 213 (240) | 194647, p. 212 (239); 194648, p. 213 (240) | unlocated | §85 §1 |
| 14c | 194664 | ပဿထ | 213 (240) | 194655, p. 213 (240); 194696, p. 214 (241) | unlocated | §85 §1 |
| 14c | 194745 | ပဿမ္ဘိ | 218 (245) | 194756, p. 219 (246) | unlocated | §85 §1 |
| 14c | 195771 | ပါဌာနာရုဠှ | 322 (349) | 195767, p. 322 (349) | unlocated | §85 §1 |
| 14c | 196389 | ပါနီယဃဋ | 391 (418) | 196386, p. 391 (418) | unlocated | §85 §1 |
| 14c | 197300 | ပါရေတိ | 489 (516) | 197297, p. 489 (516) | unlocated | §85 §1 |
| 14c | 197302 | ပါရေမိ | 489 (516) | 197298, p. 489 (516) | unlocated | §85 §1 |
| 14c | 197334 | ပါလယိဿာမိ | 492 (519) | 197328, p. 492 (519) | unlocated | §85 §1 |
| 14c | 197365 | ပါလေန္တိ | 497 (524) | 197383, p. 498 (525) | no label / analysis | §85 §1 |
| 14c | 197369 | ပါလေန္တု | 497 (524) | 197384, p. 498 (525) | unlocated | §85 §1 |
| 14c | 197376 | ပါလေဿာမိ | 497 (524) | 197393, p. 498 (525) | unlocated | §85 §1 |
| 14c | 197457 | ပါဝုဿကကာလ | 506 (533) | 197449, p. 506 (533) | unlocated | §85 §1 |
| 14c | 198291 | ပိဒဟထ | 605 (632) | 198301, p. 606 (633) | unlocated | §85 §1 |
| 14c | 198297 | ပိဒဟိံ | 606 (633) | 198315, p. 607 (634) | unlocated | §85 §1 |
| 14c | 198356 | ပိဓိယျန္တိ | 610 (637) | 198353, p. 610 (637) | unlocated | §85 §1 |
| 14c | 202365 | ပေက္ခရေ | 1005 (1032) | 202383, p. 1006 (1033) | unlocated | §85 §1 |
| 14c | 202585 | ပေသယိ | 1028 (1055) | 202591, p. 1029 (1056) | unlocated | §85 §1 |
| 14c | 202836 | ပေါထေယျ | 1053 (1080) | 202846, p. 1054 (1081) | unlocated | §85 §1 |
| 14c | 202837 | ပေါထေယျုံ | 1053 (1080) | 202848, p. 1054 (1081) | unlocated | §85 §1 |
| 14c | 202840 | ပေါထေဿာမိ | 1053 (1080) | 202850, p. 1054 (1081) | stub | §85 §1 |
| 15 | 115158 | ဗဟလတ္တစ | 150 (178) | 115170, p. 151 (179) | unlocated | §85 §1 |
| 15 | 118087 | ဗျာဟရ | 413 (441) | 118085, p. 413 (441) | unlocated | §85 §1 |
| 15 | 119699 | ဘဝင်္ဂပ္ပဝါဟ | 569 (597) | 119694, p. 569 (597) | unlocated | §85 §1 |
| 15 | 120077 | ဘဝါဘိသင်္ခရဏဋ္ဌ | 604 (632) | 120080, p. 605 (633) | no label / analysis | §85 §1 |
| 16 | 125847 | မနောရမ္မ | 265 (291) | 125851, p. 266 (292) | unlocated | §85 §1 |
| 17 | 138171 | ရုက္ခဆာယာ | 642 (664) | 138176, p. 642 (664) | unlocated | §85 §1 |
| 17 | 138175 | ရုက္ခဆလ္လိ | 642 (664) | 138168, p. 642 (664) | unlocated | §85 §1 |
| 17 | 139233 | ရူပူပယ | 774 (796) | 139247, p. 775 (797) | unlocated | §85 §1 |
| 18 | 142162 | လောကိယပဋိပဒါနုတ္တရိယ | 307 (325) | 142165, p. 308 (326) | unlocated | §85 §1 |
| 20 | 158939 | ဝီတစ္စိတ | 265 (295) | 158935, p. 265 (295) | unlocated | §85 §1 |
| 20 | 160880 | ဝေဏီ | 499 (529) | 160889, p. 500 (530) | unlocated | §85 §1 |
| 20 | 162972 | သံဃာတ | 786 (816) | 162974, p. 787 (817) | stub | §85 §1 |
| 21 | 166523 | သင်္ခလိက | 257 (285) | 166520, p. 257 (285) | no label / analysis | §85 §1 |
| 21 | 168114 | သဉ္ဇာတဗလဝဒေါမနဿ | 442 (470) | 168112, p. 442 (470) | unlocated | §85 §1 |
| 21 | 168524 | သညူပယ | 488 (516) | 168533, p. 489 (517) | unlocated | §85 §1 |
| 21 | 168601 | သဋ္ဌိတူရိယသဟဿ | 495 (523) | 168598, p. 495 (523) | unlocated | §85 §1 |
| 21 | 170978 | သဒ္ဓမ္မဿဝန | 756 (784) | 170993, p. 757 (785) | unlocated | §85 §1 |
| 21 | 170986 | သဒ္ဓမ္မဿဝနာဓီန | 756 (784) | 170995, p. 757 (785) | no label / analysis | §85 §1 |
| 22 | 178096 | သပ္ပါဋိဟိရကတ | 77 (117) | 178094, p. 77 (117) | no label / analysis | §85 §1 |
| 23 | 187965 | သဝိသေသ | 251 (286) | 187960, p. 251 (286) | no label / analysis | §85 §1 |
| 24 | 205449 | သုဂတိဂါမိမဂ္ဂ | 230 (264) | 205446, p. 230 (264) | unlocated | §85 §1 |
| 24 | 206045 | သုတက္ခရသဒိသ | 296 (330) | 206042, p. 296 (330) | unlocated | §85 §1 |
| 24 | 206368 | သုတ္တပ္ပမာဏ | 328 (362) | 206388, p. 329 (363) | no label / analysis | §85 §1 |
| 25 | 219369 | ဟရိ | 250 (284) | 219371, p. 250 (284); 219372, p. 250 (284) | no label / analysis | §85 §1 |
| 25 | 219383 | ဟရိတက | 251 (285) | 219391, p. 252 (286) | unlocated | §85 §1 |
| 25 | 219387 | ဟရိတကီ | 251 (285) | 219396, p. 252 (286) | unlocated | §85 §1 |
| 4c | 175118 | ဩဂဠိတွာ | 395 (422) | 175126, p. 396 (423) | unlocated | §85 §1 |
| 4c | 175549 | ဩတ္တပန | 458 (485) | 175546, p. 458 (485) | unlocated | §85 §1 |
| 4c | 175658 | ဩဒဟိဿန္တိ | 473 (500) | 175677, p. 474 (501) | unlocated | §85 §1 |
| 4c | 175665 | ဩဒဟထ | 473 (500) | 175652, p. 473 (500) | unlocated | §85 §1 |
| 4c | 175786 | ဩဓုနာထ | 496 (523) | 175783, p. 496 (523) | unlocated | §85 §1 |
| 4c | 176410 | ဩလမ္ဗန္တိ | 585 (612) | 176420, p. 588 (615) | no label / analysis | §85 §1 |

**From plan step 1.8's farther-body measurement: 6 rows, 2 left after §91** (30 Sep 2026, the snapshot of that day; unlocated headwords found at a line start +
label inside an earlier article's body, whose headword the index repeats within 40 ids, not adjacent). None is among the 78.

| book | id | headword | index p. (PDF) | the other row: id, index p. (PDF) | note | from |
|---|---|---|---|---|---|---|
| 14c | 202368 | ပေက္ခတေ | 1005 (1032) | 202376, p. 1005 (1032) | unlocated | 1.8 farther body (`tmp/farbody18/`) |
| 4c | 174421 | ဧဓတိ | 293 (320) | 174419, p. 293 (320) | on its own printed entry since §89 (farther-body split, right on the image); image (4c p. 320 R, read in §91): its entry is printed **ဧဓတိ¹** (ကြိ) [ဧဓ+အ+တိ], and 174419's is **ဧဓတိ²** (ကာ၊ကြိ), printed last on the page (running head ဧဓတိ²): the index lists ² (174419) before ¹ (174421), with 174420 ဧဓိတ္တ between, which the page prints only as sense (3) inside ဧဓတိ¹'s quotations (no entry of its own; unlocated). Kept here for the order; the §89 measurement's "printed ²" was a misreading | 1.8 farther body (`tmp/farbody18/`); §91 |

*Re-checked 30 Sep 2026 (brief §91), after plan step 1.8 was applied (the homonym rules R, PCED and `HOMONYM_FIX`, and the
farther-body splits):*
- *Left §5: 4 rows, now each on its own printed entry* (a farther-body split, §89: read right on the image in the nine books, PCED-gated in
  01–19). Both rows of each pair then have a printed entry, so the repeat is two printed articles of one headword, not a misfiled index row:
  14c 196387 ပါနီယကူပ (twin 196384, p. 391 (418); image), 15 118320 ဗြဟ္မလောကူပပတ္တိ (118317, p. 441 (469); PCED), 19 150247 ဝိစ္စေဿတိ
  (150245, p. 290 (311); PCED), 24 204839 သုခပ္ပဋိသံဝေဒီ (204879, p. 173 (207); image). 174421 is on its own entry too, and stays for the order (above).
- *The 78 rows of §85 §1*: none is now placed by `HOMONYM_FIX`, R or the PCED pass, none is `same_as`, none was split out, and none of their
  twins changed: all 78 stay. **§88's finding** (the index repeats a headword for each page a long entry runs over; those rows are `same_as`,
  not errors) explains none of them: in 41 the twin's article stands on the repeat's own index page (PDF), in 37 on a later page (the
  repeat is indexed before its twin), never on an earlier page it runs on from. One looked at apart: 14c 194663 ပဿ (p. 213 (240)); 194647
  (p. 239) runs on to p. 240, but that page's continuation row is 194648, adjacent to 194647 (a homonym run), and 194663 is 15 ids further.
- 202368 ပေက္ခတေ stays (still unlocated).
