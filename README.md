# Tipiṭaka Pāḷi-Myanmā Abhidhāna — digitised

**တိပိဋက ပါဠိ-မြန်မာ အဘိဓာန်** is a Pāḷi → Burmese dictionary of the whole Tipiṭaka in
**25 volumes, bound as 29 books**. It holds about 215,000 headwords. It was compiled by the
မစိုးရိမ် (Masoeyein) Board of Scholar-Elders in Mandalay and published by the Department
for the Promotion and Propagation of the Sāsana, Ministry of Religious Affairs, Union of
Myanmar.

This repository turns the printed dictionary into data:

1. **OCR** of the scanned volumes. The two-column page is cut at the gutter first.
2. **Articles**, each anchored on the correct headword. For every page, the headwords are already known, correctly spelled, from the index compiled for the *Tipiṭaka Abidan* app. Each article is split into its fields: headword · grammatical label `( )` · compound analysis `[ ]` · Burmese definition · citations.
3. **Romanised Pāḷi headwords** (Aksharamukha, Burmese → IAST). These are checked against the Sixth Council Tipiṭaka vocabulary of [OSBCT](https://github.com/bthar-mx/OSBCT).
4. **Spanish**, translated **from the Burmese**, never through English. This part has not started; see [`docs/spanish-method.md`](docs/spanish-method.md).

## Read this before using the data

**Nothing here is proofread.** Every row carries a status, and you should treat it as meaning exactly what it says:

| status | meaning |
|---|---|
| `ocr` | Machine-read Burmese, untouched. The headword itself is correct: it comes from the index, not the OCR. Everything around it can contain OCR errors. |
| `drafted` | A machine-assisted Spanish rendering that no one has checked. **Not a reading.** |
| `reviewed` | Checked by a reader of Burmese and Pāḷi. |
| `corrected` | Changed after review. |

Always compare against the page image before quoting an article. Every row gives its
`book` and `pdf_page`.

## Progress

| volume | pages | index headwords | OCR | articles | report |
|---|---:|---:|---|---|---|
| 1 (အ – အနီဠက) | 913 | 8,150 | done | done | [`ocr/01/articles-report.md`](ocr/01/articles-report.md) |
| 25 | 466 | 4,046 | pilot, whole-page | — | [`ocr/25/pilot-report.md`](ocr/25/pilot-report.md) |

## Layout

```
tools/abhidhana_ocr.py        OCR a book, cut at the gutter, score recall against the index
tools/abhidhana_articles.py   cut the OCR into articles, parse the fields, romanise, check against OSBCT
tools/fetch_sources.sh        download and verify the source PDFs and index from the release
pdfs/SHA256SUMS               checksums of the 29 source PDFs (the files are in the release)
db/SHA256SUMS                 checksum of the app's index database (in the release)
ocr/<book>/articles.jsonl     one article per line
ocr/<book>/articles-report.md what was recovered, measured
docs/                         project brief, Spanish method, provenance of the scans
```

The PDFs and the index database are **release assets**, not files in git. They are
1 GB of fixed inputs. Run `tools/fetch_sources.sh` to download and verify them.

OCR uses tesseract 5 with the `myap` Burmese-Pāḷi model by Pn Daza
([pndaza](https://github.com/pndaza)). It has to be placed in a `tessdata/` directory
(set with `ABHIDHANA_TESSDATA`).

## Sources and credits

The dictionary is the work of the **မစိုးရိမ် Board of Scholar-Elders** (Masoeyein
Monastery, Mandalay), published by the **Department for the Promotion and Propagation of
the Sāsana, Ministry of Religious Affairs**, Union of Myanmar. We claim nothing in its
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
