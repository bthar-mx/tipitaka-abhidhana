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
