# Vol. 14/2 (book 14b, ပမတ္တ – ပလ္လောမ) — text-layer extraction report

*25 September 2026. `tools/abhidhana_winburmese.py 14b` (pymupdf + python-myanmar), run in the
session's cloud container; the page records it wrote are in `ocr/14b/pages/` (and
`release/ocr-14b-pages.tar.gz`). Nothing in this book was OCR'd.*

## What the book is

949 pages, 480 × 713 pt (not the scans' ~2000 pt pages), made by iText and pdftk. **It is not a
scan.** Every page carries text in the WinInnwa family of legacy fonts: WinResearcher (1.4 million
characters), Win---Researcher2, WinHaka (the bold headwords), WinPinya, WinKalaw, WinInnwa and
WinInnwa070A. These share one encoding, a Latin-1 keyboard layout drawn with Burmese glyphs and
typed in visual order. Besides them: SanskritKavyaNormal (Sanskrit quotations, 9,634 characters),
Mahar4 and Pinny9 (an ornament between headword and label), and ArtHouse (a title page).

864 pages carry index entries (PDF pp. 25–948), **6,942 index headwords**, 6,787 distinct. Index
`start_page` 24, and the offset holds: PDF p. 300 is index p. 276 and its running head says ၂၇၆.

## How

python-myanmar's `wininnwa` converter does the syllable reordering. What this book needed beyond
it, each found by converting the whole book and looking at what was left unconverted or at the
headwords that did not match the index:

| problem | fix |
|---|---|
| ဝ and the digit ၀ are both `0` in the encoding; the converter makes every one a digit, and a vowel after it is then left unconverted (`0d`) | `0` not among digits is read as ဝ |
| stacked ta under na, `Å` (2,324 times), and `É` (stacked ta + wa-hswe) are not in its table | read as `å`, `åG` |
| ligatures it truncates: i + anusvara `ð`, kinzi + i/ii/anusvara `Ø Ð ø`, ya-yit + u `û ê`, ဉ + ာ `Ó` | spelt out before converting |
| two-consonant ligatures `| ¥ × ¹ @` (ဋ္ဌ ဋ္ဋ ဍ္ဍ ဍ္ဎ ဏ္ဍ) block a following vowel | split into consonant + stacked consonant |
| marks typed in drawing order, not in the converter's (`EdÅ` for န္တိ, `EdI` for နှိ) | each run of marks sorted into the converter's order, never across a consonant |
| a mark set as its own span (ံ, ဲ: 202 times) | put after the last character to its left on its baseline |
| « » round the analysis, `]]` `}}` round a quotation | [ ], “ ” |
| `ç ¿ µ Þ` | , ? ! — (identified on the page image, pp. 26, 32, 40, 625) |

A page is written as an OCR page record, `text['col.psm6']` = the left column's lines then the
right column's, so the articles step and the reports run on it unchanged. Records carry
`source: "text layer"` and `dpi: null`. Sanskrit spans are kept raw inside ⟨ ⟩, unconverted.

Checked against the page image on p. 300 (the first thirteen lines of the left column): word for
word, including the print's own spellings (ကင်္ခါ).

## Result

| | vol. 14/2, text layer | vol. 9, OCR |
|---|---:|---:|
| index headwords verbatim | **6,508 / 6,942 = 93.7%** | 89.5% |
| … with the spelling folds | 96.3% | 90.1% |
| … and a spelling variant printed inside the headword, ပရဒုက္ခပဋိ(တိ)ကာရ | 96.6% | |
| pages where every headword came out | 633 of 864 = 73.3% | 51.6% |
| pages below 50% | 14 | 8 |

**What the remaining 3.4% are** is not the conversion. Sampled misses are the print and the index
spelling a headword differently: ါ/ာ beyond the fold's reach (ဓါ/ဓာ), index typos (ပရတီိိရ,
ပရစိိတ္တဇာနနက, ဇ္စျ typed for ဇ္ဈ in ပရိတ္တဇ္စျာန, ပရိပုဏ္ဏဇ္စျာသယ), headwords the index files on a
neighbouring page (62 are on one within two pages), and a handful of stray marks
(ပရိဒဍ္ဎုဂတ္တ). This book's index was typed separately (`docs/app-info.html`), and it shows.

**In printed order** (the column pass's measure) comes out at 77.0%, but the measure takes each
headword's first occurrence on the page, and clean text quotes headwords (running heads,
cross-references) before their entries. Here it says little: the lines are in reading order by
construction.

## A trial of the articles step (not in the folder)

To see what the text layer gives, `abhidhana_articles.py 14b` was run on these records in the cloud
container, on a copy; its output is not written to the folder, since articles are not to be run
during the batch. Figures to expect when it is run there:

| | vol. 14/2 (trial) | vol. 9 (OCR) |
|---|---:|---:|
| articles located | **98.2%** | 92.5% |
| normalised label + body | **97.5%** | 86.0% |
| compound analysis recovered | 97.3% | 76.1% |

Readings left unnormalised include **(ကာ၊ကမ္မ၊ကြိ) 7 times**, clean here, so a real label (the
typed witness prints it 43 times): add it to the label map after the batch.

No typed witness covers this book (`docs/witness.md` §3), so the text layer is its only text; it
is a far better one than OCR. Its licence is the dictionary's, as for the scans.
