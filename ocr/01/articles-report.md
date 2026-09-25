# Vol. 1 — articles

*24 September 2026. `tools/abhidhana_articles.py 01` over the column-cut OCR. See `ocr-report.md` for the OCR itself.*

8,150 index headwords on 763 OCR'd indexed pages (of 763 indexed).

| | |
|---|---:|
| located verbatim (line start or before ( / [ ) | 5,409 = 66.4% |
| located verbatim, inline only | 67 = 0.8% |
| located by bounded fuzzy match | 1,615 = 19.8% |
| **located, any** | **7,091 = 87.0%** |
| unlocated | 1,059 = 13.0% |
| label ( ) recovered | 6,648 = 81.6% |
| compound analysis [ ] recovered | 5,386 = 66.1% |
| of which + signs repaired (normalise_analysis) | 1,445 = 17.7% |
| non-empty body | 7,033 = 86.3% |
| at least one citation parsed | 4,695 = 57.6% |
| label + body (the article is usable) | 6,623 = 81.3% |

**Romanised headwords against OSBCT** (682,010 canonical words):

| | |
|---|---:|
| a canonical word | 1,745 = 21.4% |
| inside a canonical word | 3,923 = 48.1% |
| neither | 2,482 = 30.5% |

Labels: (တိ) 2,753 · (န) 1,210 · (ပု) 733 · (ထီ) 555 · (ပ) 333 · (၇) 241 · (ထိ) 86 · (က) 70 · (ကြိ၊ဝိ) 59 · (ထံ) 56 · (ကြိ) 54 · (ကြ၊ ဝိ) 52 · (ကြု) 51 · (ပုန) 49 · (ဗျ) 37

## What these figures mean, and what they do not

- **"Located"** means the article's start was found in the text. The headword stored in each
  row is always the index's, correctly spelled; `headword_ocr` is what the OCR printed.
- **Unlocated (13.0%)**: the OCR damaged the headword past a ≥0.80 match, or split it across
  a line. The article's text then stays inside its predecessor's `raw`/`body`. Most are
  recoverable by hand from the neighbouring row.
- **Labels are read, not normalised.** A spot check of p. 300 against the image: (ကြိ) came
  out as (က); `+` in the analysis as ၂. The long tail above — (၇), (က), (ကြု), (ထိ), (ပ) — is
  mostly such confusions of (ကြိ), (ထီ), (ပု). A normalisation table against the label set the
  dictionary actually uses is the next step; until then treat `label` as a reading.
- **+ signs in the compound analysis are repaired** (`normalise_analysis`, 17.7% of articles): OCR
  reads + as ၂ or drops it, e.g. p. 300 အစ္စာဝဒတိ came out "အတိ ၂ အာ ဝဒ အ တိ" and now reads
  "အတိ + အာ + ဝဒ + အ + တိ", as printed (checked by Angel). Only analyses made wholly of Pāḷi
  elements are rejoined; ones holding a derivation note or Burmese are left as read. The OCR
  text is kept in `analysis_ocr`. Word formations can be cross-checked at
  https://dictionary.sutta.org/ (Pāḷi-Burmese, from PCED 1.94).
- **`analysis_bracket_damaged`**: the closing `]` was misread and the analysis was taken as
  the run of `+`-joined tokens. Check these against the page.
- **Citations** are parsed only in their full form (abbreviation ၊ vol ။ para ။). 57% of
  articles have one; cross-reference articles (`X-ကြည့်`) have none by design.
- **OSBCT**: 69.5% of headwords attested whole or inside a canonical word (vol. 25 sample:
  64.1%). The residual is lemmata the canon never inflects that way and compounds formed for
  the entry, not romanisation failure.
- Every row is `status: "ocr"`. Nothing is proofread.
