# Vol. 1 — articles

*24 September 2026. `tools/abhidhana_articles.py 01` over the column-cut OCR. See `ocr-report.md` for the OCR itself. Labels normalised and articles re-located this day; the figures before are at the end.*

8,150 index headwords on 763 OCR'd indexed pages (of 763 indexed).

| | |
|---|---:|
| located verbatim (line start or before ( / [ ) | 5,509 = 67.6% |
| located verbatim, inline only | 26 = 0.3% |
| located by bounded fuzzy match | 2,112 = 25.9% |
| **located, any** | **7,647 = 93.8%** |
| unlocated | 503 = 6.2% |
| label ( ) read | 7,182 = 88.1% |
| label normalised to the closed set (docs/labels.md) | 7,144 = 87.7% |
| of which read exactly as printed / mapped / inferred from the ending | 5,867 / 1,274 / 3 |
| label read but left unnormalised | 38 = 0.5% |
| compound analysis [ ] recovered | 5,813 = 71.3% |
| of which + signs repaired (normalise_analysis) | 1,546 = 19.0% |
| non-empty body | 7,597 = 93.2% |
| at least one citation parsed | 4,934 = 60.5% |
| label + body (the article is usable) | 7,119 = 87.3% |

**Romanised headwords against OSBCT** (682,010 canonical words):

| | |
|---|---:|
| a canonical word | 1,745 = 21.4% |
| inside a canonical word | 3,923 = 48.1% |
| neither | 2,482 = 30.5% |

Labels, normalised: (တိ) 2,998 · (ပု) 1,458 · (န) 1,283 · (ထီ) 808 · (ကြိ) 236 · (ကြိ၊ဝိ) 174 · (ပု၊န) 70 · (ဗျ) 41 · (န၊ထီ) 30 · (န၊တိ) 9 · (ကာ၊ကြိ) 9 · (ပု၊တိ) 7 · (ပု၊ထီ) 7 · (န၊ပု) 5 · (တိ၊န) 4 · (ပုံ-ဗဟု) 2 · (စတုတ္ထန္တ) 1 · (တတိယန္တ-ဗျ) 1 · (နာမ-ကြိ) 1

Readings left unnormalised: (၂) 9 · (တံ) 4 · (၅) 3 · (၃) 3 · (၁) 2 · (ဿိ) 1 · (=မူလျေ) 1 · (= ပါပကရဏေ) 1 · (ဆံ) 1 · (သီ၊က) 1 · (မူလဋီ။ ၁။၁၁ ။) 1 · (.) 1 · (ရီ) 1 · (တ္တ) 1 · (ဂ) 1 · (တ္ထူ) 1 · (န ” ၂) 1 · (မူ) 1 · (ယီ) 1 · (နီ) 1 · (တ္တူ) 1 · (ခ) 1

## What these figures mean, and what they do not

- **"Located"** means the article's start was found in the text. The headword stored in each
  row is always the index's, correctly spelled; `headword_ocr` is what the OCR printed.
- **How articles are located (revised 24 Sep).** A verbatim pass places every headword it can,
  in printed order. The headwords it leaves, run by run between placed neighbours, are then
  *aligned* in order to the article starts in that span (a line whose head, of about the
  headword's length and without punctuation, is followed by ( or [), scoring similarity ≥ 0.70.
  Before, each was matched on its own at ≥ 0.80, and neighbouring compounds — which in this
  dictionary are all alike — took each other's lines. A headword broken across a line with a
  hyphen is now joined.
- **Checked against the page images and the analysis each article carries:** of 12 sampled
  newly located articles, 12 start at the right entry; of 16 sampled in the new 0.70–0.80 band,
  15 (the 16th, a two-letter headword, could not be decided); of 10 articles whose start moved,
  9 moved to the right entry (the 10th has since been fixed). Of 8 articles the old matcher
  placed and the new one first dropped, 5 had been wrong entries; 2 of the other 3 are placed
  again. Together 36 of 38: read the fuzzy placements as roughly 95% right, not as proofread.
- **Unlocated (6.2%)**: the headword is too damaged for a 0.70 match, sits in running text, or
  shares its line with a neighbour. The article's text then stays inside its predecessor's
  `raw`/`body`.
- **Labels are normalised** to the printed label (`label`); `label_ocr` keeps the reading and
  `label_how` says `exact`, `mapped`, or `inferred` (the ending decided it; 3 rows). The map,
  the image checks behind it, and the labels this volume uses beyond `docs/spanish-method.md`
  §2 are in `docs/labels.md`. 38 readings are left unnormalised (`label` None), mostly digits
  that stand for a lost label. On a blind sample of 32 rows checked against the images, 30
  were right; both errors came from rules since removed. Against the typed text of this
  dictionary in PCED 1.94 (dictionary.sutta.org's data; `docs/labels.md` §4), the normalised
  label agrees on **98.5%** of the 6,836 articles both have, against 81.3% for the raw readings.
- **+ signs in the compound analysis are repaired** (`normalise_analysis`): OCR reads + as ၂ or
  drops it, e.g. p. 300 အစ္စာဝဒတိ came out "အတိ ၂ အာ ဝဒ အ တိ" and now reads
  "အတိ + အာ + ဝဒ + အ + တိ", as printed (checked by Angel). Only analyses made wholly of Pāḷi
  elements are rejoined. The OCR text is kept in `analysis_ocr`. Word formations can be
  cross-checked at https://dictionary.sutta.org/ (Pāḷi-Burmese, from PCED 1.94).
- **`analysis_bracket_damaged`**: the closing `]` was misread and the analysis was taken as
  the run of `+`-joined tokens. Check these against the page.
- **Citations** are parsed only in their full form (abbreviation ၊ vol ။ para ။). Cross-reference
  articles (`X-ကြည့်`) have none by design.
- **OSBCT**: 69.5% of headwords attested whole or inside a canonical word (vol. 25 sample:
  64.1%). The residual is lemmata the canon never inflects that way and compounds formed for
  the entry, not romanisation failure.
- Every row is `status: "ocr"`. Nothing is proofread.
- This prose is hand-written; `abhidhana_articles.py` regenerates only the tables above it.

## Before and after, 24 September 2026

| | commit 40e6be1 | now |
|---|---:|---:|
| located, any | 87.0% | **93.8%** |
| unlocated | 13.0% | 6.2% |
| label | 81.6% read, 125 distinct readings | **87.7% normalised**, 19 labels |
| compound analysis recovered | 66.1% | 71.3% |
| non-empty body | 86.3% | 93.2% |
| at least one citation | 57.6% | 60.5% |
| **label + body** | 81.3% (raw readings) | **87.3%** (normalised labels) |
