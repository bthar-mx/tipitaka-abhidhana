# Tipiṭaka Pāḷi-Myanmā Abhidhāna — digitised

**တိပိဋက ပါဠိ-မြန်မာ အဘိဓာန်** is a Pāḷi → Burmese dictionary of the whole Tipiṭaka in
**25 volumes, bound as 29 books**, with about 215,000 headwords. It was compiled from the
1950s to 2023 by five teams of scholar-monks, each taking part of the alphabet (vol. 17,
pp. 6–7), among them မစိုးရိမ် (Masoeyein) monastery in Mandalay, which wrote vols. 5–6 and
15–16; vol. 1 was published in 1964 by the Union of Burma Buddha Sāsana Council, the later
volumes by the Department for the Promotion and Propagation of the Sāsana, Ministry of
Religious Affairs, Union of Myanmar. Its history is in [`docs/history.md`](docs/history.md).

**All 29 books are now digitised**: 221,154 index headwords over 25,700 pages; 94.1% of the
articles are located in the OCR and 88.1% have both their grammatical label and their definition.
**Nothing is proofread.** Read and search it at **[abhidhana.buddha-dhamma.net](https://abhidhana.buddha-dhamma.net)**,
article by article beside the printed page (the site's source is in [`site/`](site/)); the data
are in [`ocr/`](ocr/).

## En español

Este repositorio convierte en datos el *Tipiṭaka Pāḷi-Myanmā Abhidhāna*, el diccionario
pāḷi–birmano del Tipiṭaka en 25 volúmenes (29 libros), compilado entre los años cincuenta y 2023
por cinco equipos de monjes eruditos (entre ellos el del monasterio de Masoeyein, vols. 5–6 y
15–16) y publicado por el Consejo del Buddha Sāsana y el Ministerio de Asuntos Religiosos de Myanmar. Los 29
libros están digitalizados: cada artículo se ancla en la entrada correcta (tomada del índice del
diccionario), se divide en sus campos (categoría gramatical, análisis, definición, citas) y la
entrada se romaniza (IAST). **Nada está revisado**: el birmano es una lectura automática (OCR) y
contiene errores; compare siempre con la imagen de la página. La traducción al español, hecha
desde el birmano y nunca a través del inglés, está en borrador para los vols. 1–3, 4/1, 4/2, 5 y 6, sin revisar
([`docs/spanish-method.md`](docs/spanish-method.md), `docs/translation/`). Consulta y búsqueda en
**[abhidhana.buddha-dhamma.net](https://abhidhana.buddha-dhamma.net)**, en español e inglés. Proyecto del
[Instituto de Estudios Budistas Hispano](https://iebh.org).

## What this repository does

1. **OCR** of the scanned volumes (tesseract 5, Pn Daza's `myap` model). The two-column page is cut
   at the gutter first, so that the columns are not interleaved.
2. **Articles**, each anchored on the correct headword. For every page the headwords are already
   known, correctly spelled, from the index compiled for the *Tipiṭaka Abidan* app, so OCR only has
   to find them. Each article is split into its fields: headword · grammatical label `( )` ·
   compound analysis `[ ]` · Burmese definition · citations. The labels are normalised to the
   dictionary's own set, as its front matter explains them
   ([`docs/labels.md`](docs/labels.md), [`docs/abbreviations.md`](docs/abbreviations.md)).
3. **Romanised Pāḷi** (Aksharamukha, Burmese → IAST), headwords and quoted Pāḷi, checked against the
   Sixth Council Tipiṭaka vocabulary of [OSBCT](https://github.com/bthar-mx/OSBCT).
4. **Spanish**, translated **from the Burmese**, never through English. Drafted, not reviewed, for vols. 1–3,
   4/1, 4/2, 5 and 6 (`docs/translation/meanings/`); see [`docs/spanish-method.md`](docs/spanish-method.md).

## Read this before using the data

**Nothing here is proofread.** Every row carries a status, and you should treat it as meaning exactly what it says:

| status | meaning |
|---|---|
| `ocr` | Machine-read Burmese, untouched. The headword itself is correct: it comes from the index, not the OCR. Everything around it can contain OCR errors. |
| `drafted` | A machine-assisted Spanish rendering that no one has checked. **Not a reading.** |
| `reviewed` | Checked by a reader of Burmese and Pāḷi. |
| `corrected` | Changed after review. |

Every row is `ocr` today. Always compare against the page image before quoting an article. Every
row gives its `book` and `pdf_page`.

## Progress

All 29 books, 25 September 2026. *Located*: the article's headword was found in the OCR text and the
article cut out. *Label + definition*: both were read. Each volume's reports give the figures in full,
with a spot check against the page images.

| vol. | range | PDF pages | index headwords | read at | located | label + definition | reports |
|---|---|---:|---:|---|---:|---:|---|
| 1 | အ – အနီဠက <br>*a – anīḷaka* | 913 | 8,150 | 72 dpi | 94.4% | 89.0% | [ocr](ocr/01/ocr-report.md) · [articles](ocr/01/articles-report.md) |
| 2 | အနု – အဗ္ဘောက္ကိရဏ <br>*anu – abbhokkiraṇa* | 898 | 7,189 | 72 dpi | 93.6% | 88.4% | [ocr](ocr/02/ocr-report.md) · [articles](ocr/02/articles-report.md) |
| 3 | အဗျဂ္ဂ – အဠာရပမှ <br>*abyagga – aḷārapamha* | 1,177 | 11,726 | 75 dpi | 94.8% | 89.6% | [ocr](ocr/03/ocr-report.md) · [articles](ocr/03/articles-report.md) |
| 4/1 | အာ – ဥတြာသေယျုံ <br>*ā – utrāseyyuṁ* | 863 | 7,524 | 96 dpi | 92.2% | 85.0% | [ocr](ocr/4a/ocr-report.md) · [articles](ocr/4a/articles-report.md) |
| 4/2 | ဥဒ – ဥဠုရာဇ <br>*uda – uḷurāja* | 681 | 6,655 | 72 dpi | 96.7% | 91.1% | [ocr](ocr/4b/ocr-report.md) · [articles](ocr/4b/articles-report.md) |
| 4/3 | ဦ – ဩဠုမ္ပိက <br>*ū – oḷumpika* | 736 | 5,230 | 72 dpi | 92.5% | 86.8% | [ocr](ocr/4c/ocr-report.md) · [articles](ocr/4c/articles-report.md) |
| 5 | က – ကိလေဒေတွာ <br>*ka – kiledetvā* | 883 | 8,015 | 72 dpi | 93.6% | 87.7% | [ocr](ocr/05/ocr-report.md) · [articles](ocr/05/articles-report.md) |
| 6 | ကိလေသ – ငကာရ <br>*kilesa – ṅakāra* | 1,039 | 11,429 | 75 dpi | 92.0% | 86.3% | [ocr](ocr/06/ocr-report.md) · [articles](ocr/06/articles-report.md) |
| 7 | စ – ဆိဒ္ဒေယျုံ <br>*ca – chiddeyyuṁ* | 861 | 6,877 | 72 dpi | 93.1% | 87.3% | [ocr](ocr/07/ocr-report.md) · [articles](ocr/07/articles-report.md) |
| 8 | ဆိဒ္ဒ – ဏျပစ္စယတ္ထ <br>*chidda – ṇyapaccayattha* | 849 | 6,448 | 72 dpi | 92.1% | 87.8% | [ocr](ocr/08/ocr-report.md) · [articles](ocr/08/articles-report.md) |
| 9 | တ – ထောမေဿာမိ <br>*ta – thomessāmi* | 893 | 6,805 | 75 dpi | 92.5% | 86.0% | [ocr](ocr/09/ocr-report.md) · [articles](ocr/09/articles-report.md) |
| 10 | ဒ – ဒွေဠှကပုစ္ဆာ <br>*da – dveḷhakapucchā* | 981 | 7,366 | 75 dpi | 90.8% | 84.3% | [ocr](ocr/10/ocr-report.md) · [articles](ocr/10/articles-report.md) |
| 11 | ဓ – နိက္ခာမေသုံ <br>*dha – nikkhāmesuṁ* | 769 | 5,663 | 72 dpi | 93.0% | 86.2% | [ocr](ocr/11/ocr-report.md) · [articles](ocr/11/articles-report.md) |
| 12 | နိက္ခိတ္တ – နှာရုသုတ္တနိဗန္ဓန <br>*nikkhitta – nhārusuttanibandhana* | 1,123 | 7,022 | 72 dpi | 96.9% | 91.8% | [ocr](ocr/12/ocr-report.md) · [articles](ocr/12/articles-report.md) |
| 13 | ပ – ပဋိဗြူဟန <br>*pa – paṭibrūhana* | 896 | 7,279 | 73 dpi | 89.5% | 83.8% | [ocr](ocr/13/ocr-report.md) · [articles](ocr/13/articles-report.md) |
| 14/1 | ပဋိဘံသု – ပမဇ္ဇေယျ <br>*paṭibhaṁsu – pamajjeyya* | 821 | 5,219 | 70 dpi | 96.6% | 92.4% | [ocr](ocr/14/ocr-report.md) · [articles](ocr/14/articles-report.md) |
| 14/2 | ပမတ္တ – ပလ္လောမ <br>*pamatta – palloma* | 949 | 6,942 | text layer | 98.2% | 97.6% | [extract](ocr/14b/extract-report.md) · [articles](ocr/14b/articles-report.md) |
| 14/3 | ပဝ – ပ္လုတ <br>*pava – pluta* | 1,107 | 10,390 | 72 dpi | 91.7% | 85.4% | [ocr](ocr/14c/ocr-report.md) · [articles](ocr/14c/articles-report.md) |
| 15 | ဖ – ဘောဝါဒီ <br>*pha – bhovādī* | 853 | 9,342 | 74 dpi | 93.4% | 87.6% | [ocr](ocr/15/ocr-report.md) · [articles](ocr/15/articles-report.md) |
| 16 | မ – မှိတပုဗ္ဗ <br>*ma – mhitapubba* | 890 | 10,394 | 73 dpi | 92.8% | 86.6% | [ocr](ocr/16/ocr-report.md) · [articles](ocr/16/articles-report.md) |
| 17 | ယ – ရောဟိသ <br>*ya – rohisa* | 879 | 6,520 | 69 dpi | 93.4% | 84.9% | [ocr](ocr/17/ocr-report.md) · [articles](ocr/17/articles-report.md) |
| 18 | လ – ဝဠာဝါရထ <br>*la – vaḷāvāratha* | 890 | 7,829 | 72 dpi | 92.4% | 84.5% | [ocr](ocr/18/ocr-report.md) · [articles](ocr/18/articles-report.md) |
| 19 | ဝါ – ဝိဝေကောဓိမုတ္တိ <br>*vā – vivekodhimutti* | 982 | 9,251 | 72 dpi | 96.3% | 89.7% | [ocr](ocr/19/ocr-report.md) · [articles](ocr/19/articles-report.md) |
| 20 | ဝိဝေကာနိသံသ – သံဝေါဟာရ <br>*vivekānisaṁsa – saṁvohāra* | 945 | 7,366 | 72 dpi | 95.7% | 87.1% | [ocr](ocr/20/ocr-report.md) · [articles](ocr/20/articles-report.md) |
| 21 | သံသ – သန္နာဟယာမသေ <br>*saṁsa – sannāhayāmase* | 925 | 8,129 | 70 dpi | 97.4% | 89.8% | [ocr](ocr/21/ocr-report.md) · [articles](ocr/21/articles-report.md) |
| 22 | သန္နိကဋ္ဌ – သမ္ဘောန္တိ <br>*sannikaṭṭha – sambhonti* | 933 | 8,078 | 72 dpi | 96.4% | 90.2% | [ocr](ocr/22/ocr-report.md) · [articles](ocr/22/articles-report.md) |
| 23 | သမ္မ – သိဟလ <br>*samma – sihala* | 780 | 7,182 | 323 dpi | 97.7% | 92.7% | [ocr](ocr/23/ocr-report.md) · [articles](ocr/23/articles-report.md) |
| 24 | သီကတိ – သူသူ <br>*sīkati – sūsū* | 718 | 7,088 | 72 dpi | 96.4% | 90.0% | [ocr](ocr/24/ocr-report.md) · [articles](ocr/24/articles-report.md) |
| 25 | သော – ဠကာရ <br>*so – ḷakāra* | 466 | 4,046 | 200 dpi | 95.3% | 87.4% | [ocr](ocr/25/ocr-report.md) · [articles](ocr/25/articles-report.md) |
| **all** | | **25,700** | **221,154** | | **94.1%** | **88.1%** | |

Vol. 14/2 is typeset text, not a scan: it was converted from its legacy WinInnwa fonts, not OCR'd.
Vol. 4/3 includes supplements to vols. 15, 4/2 and 16 (PDF pp. 713–735).

## The index, and its errors

The app's index (`db/tipitaka_abidan.db`, 221,154 rows of headword, book and page) is the ground
truth for *which* headwords there are, but not always for their spelling or their page: some are
filed a page early or late, a printed page is missing from vol. 22's scan, vol. 13 carries 232 of
vol. 15's headwords, and book 21's index gives p. 962 for 692. All are listed, with how they were
checked, in [`docs/index-errata.md`](docs/index-errata.md). The pipeline corrects the page errors
(`PAGE_FIX`, `ID_PAGE_FIX` in `tools/abhidhana_articles.py`); the index itself is never edited.

## Typed witnesses

Two typed copies of the dictionary exist. Both were first used only to check our reading; since
26 September 2026 PCED's text is also used (the editor's decision), see below:

- **PCED** (Pali Canon E-Dictionary 1.94, the data behind dictionary.sutta.org; `siongui/data`): its
  "Tipiṭaka Pāḷi-Myanmar Dictionary", typed in Zawgyi, covering vols. 1–19. Converted to Unicode
  and joined to our articles: labels agree on 98–99% ([`docs/witness.md`](docs/witness.md),
  [`docs/witness-join.md`](docs/witness-join.md)).
- **Pn Daza's `dict.db`**, the database of his Android app *Pali-Myanmar Dictionary*
  ([pndaza/pali-myanmar-dictionary](https://github.com/pndaza/pali-myanmar-dictionary)), which holds
  this dictionary's typed text by book and page, with two other dictionaries
  ([`docs/witness-pndaza.md`](docs/witness-pndaza.md)).

Neither states a licence. **Pn Daza's text is not in this repository or on the website**, and may be
added later, if he agrees. **PCED's text is used, credited, in two places** (decided 26 Sep 2026):
the compound analysis [ ] of vols. 1–19 is taken from it wherever it has one
(`tools/abhidhana_witness_analysis.py`; the row keeps our OCR reading as `analysis_read` and
carries `analysis_source: "pced"`), because our OCR's analysis differed from it in 50.9% of
articles and spelled the headword worse in most of those; and the Meaning boxes are drafted from
its definitions (`docs/translation/`, `source` on every row). The witness files themselves stay
local (`witness/`, gitignored).

## Layout

```
ocr/<book>/articles.jsonl      one article per line: fields, placement, status
ocr/<book>/pali.jsonl          romanised Pāḷi for each article, with its OSBCT attestation
ocr/<book>/*-report.md         OCR and article reports, spot checks
tools/abhidhana_ocr.py         OCR a book (cut at the gutter), score recall against the index
tools/run_volumes.sh           OCR → articles → romanisation, book after book, unattended
tools/abhidhana_articles.py    cut the OCR into articles, parse the fields, apply the index errata
tools/abhidhana_romanise.py    romanise and check against OSBCT
tools/abhidhana_labels.py      the label table of docs/labels.md, shared by pipeline and site
tools/abhidhana_fold.py        spellings print, index and OCR disagree on (for matching only)
tools/abhidhana_recut.py       find and re-read pages cut through a column
tools/abhidhana_winburmese.py  vol. 14/2: text layer from WinInnwa fonts to Unicode
tools/abhidhana_witness*.py    the typed witnesses (checking only; outputs gitignored)
tools/abhidhana_ocr_stats.py   figures for an OCR report
tools/abhidhana_reader_data.py data for the private Reader
tools/abhidhana_site.py        builds the website from ocr/ and site/ (Cloudflare Pages)
tools/abhidhana_pages_r2.py    page images: PDF → WebP → Cloudflare R2
tools/fetch_sources.sh         download and verify the source PDFs and index from the release
site/                          the website's pages, scripts and volume list
docs/                          project brief, labels, abbreviations, index errata, witnesses, Spanish method
pdfs/SHA256SUMS, db/SHA256SUMS checksums of the release assets
```

The PDFs and the index database are **release assets** (`sources-v1`), not files in git: 1 GB of
fixed inputs. Run `tools/fetch_sources.sh` to download and verify them. The per-page OCR records are
there too, as `ocr-NN-pages.tar.gz`.

OCR uses tesseract 5 with the `myap` Burmese-Pāḷi model by Pn Daza
([pndaza](https://github.com/pndaza)). It has to be placed in a `tessdata/` directory (set with
`ABHIDHANA_TESSDATA`). How to run a volume: [`RUNBOOK.md`](RUNBOOK.md).

## Sources and credits

The dictionary is the work of **five teams of scholar-monks**, 1950s–2023, among which the
alphabet was divided (vol. 17, pp. 6–7; [`docs/history.md`](docs/history.md)); **မစိုးရိမ်**
(Masoeyein) monastery, Mandalay, wrote vols. 5–6 and 15–16. Vol. 1 was published by the Union
of Burma Buddha Sāsana Council (1964), the later volumes by the **Department for the Promotion
and Propagation of the Sāsana, Ministry of Religious Affairs**, Union of Myanmar. We claim nothing in its
text. The licences below cover only what this project adds.

The page scans and the headword index come from the **Tipiṭaka Abidan** app, developed
by **Pn Daza**. According to the app's own provenance note ([`docs/app-info.html`](docs/app-info.html)):

- Volumes 1–19 (20 books) came from the Tipiṭaka Pāḷi-Myanmā Abhidhāna iOS app released by the **ဗုဒ္ဓစေတမန်အဖွဲ့** (Buddhasetaman group).
- Volumes 20, 21, 22 and volume 4 part 3 were prepared with the help of the monks of **မစိုးရိမ်တိုက်သစ်** (Masoeyein Taik-thit): ဦးဝိမလ၊ ဦးကိတ္တိသာရ၊ ဦးပညာဓိက၊ ဦးဩဘာသ၊ ဦးခေမာစာရ၊ ဦးဩသဓ၊ ဦးစိန္တိတ. They were joined by ဦးနန္ဒမာလာ၊ ဦးနန္ဒ၊ ဦးသီရိန္ဒ၊ ဦးဇောတိက၊ ဦးခေမာသီရိ၊ ဦးနန္ဒိယ and ဦးပညာဓဇ of other monasteries. Volume 22 was scanned by ဦးကိတ္တိသာရ၊ ဦးခေမာဝံသ၊ ဦးသာသန၊ ဦးဇဋိလ၊ ဦးဉာဏိက and ဦးပညာဓိက.
- The remaining PDFs came from the **ကမ္ဘာအေးစာကြည့်တိုက်** (Kaba-Aye library).
- Volume 23: the book was donated by အရှင်ခေမာသီရိ, the headwords were typed by အရှင်နန္ဒိယ, and ဦးမော်ဒယ် scanned it.
- Volume 14 parts 2 and 3 and volume 24 were scanned and their headwords typed by ဦးဝိမလ၊ ဦးဓမ္မာနန္ဒ၊ ဦးအာဒိစ္စ၊ ဦးသုမန၊ ဦးကုမာရ၊ ဦးခေမာစာရ and ဦးကဝိနန္ဒ.
- Volume 25 was supplied by **မြင်းဝန်ကျောင်းတိုက်** (Myinwun monastery).

The monks' names are given as the app prints them. Romanised forms will be added once a
Burmese reader has checked them.

## Licences

- **Code** (`tools/`): MIT, see [`LICENSE`](LICENSE).
- **What this project adds** (article structure, romanisations, reports, Spanish renderings): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See [`LICENSE-DATA.md`](LICENSE-DATA.md).
- **The dictionary text and the scans** belong to their makers, credited above. The OCR'd Burmese is a reading of their work and is not relicensed by us.

## Related

- [OSBCT](https://github.com/bthar-mx/OSBCT): the Sixth Council Tipiṭaka corpus that the romanised headwords are checked against, and that the citations will resolve to.
- `bthar-mx/nissaya` (private for now): Burmese nissayas. This dictionary is the reference that makes their Burmese glosses checkable.

A project of the Instituto de Estudios Budistas Hispano ([iebh.org](https://iebh.org)) and Buddhismo Theravāda Hispano A.R.
