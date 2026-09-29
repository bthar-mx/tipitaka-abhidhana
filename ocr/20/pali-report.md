# Vol. 20 — romanised Pāḷi

*`tools/abhidhana_romanise.py 20` over `articles.jsonl`. Aksharamukha Burmese → IAST, ṃ written ṁ.
Output: `pali.jsonl`, one row per article, keyed by `id`.*

| | |
|---|---:|
| headwords romanised | 7,366 (all) |
| compound analyses romanised | 6,260 |
| of which every element Pāḷi-shaped | 6,169 = 98.5% (the rest keep Burmese parts in ⟨ ⟩) |
| articles with Pāḷi found in the definition | 6,752 = 91.7% |
| Pāḷi spans | 23,149 |
| tokens in those spans | 82,863, of which **93.3% attested in OSBCT** |
| citations romanised (mechanically, abbreviations not expanded) | 17,168 |

What is and is not claimed:

- The **headword** romanisation rests on the index spelling, so it is as good as Aksharamukha.
- **Analyses and quoted Pāḷi** are romanised from OCR text. An OCR error becomes a romanisation
  error; the OSBCT attestation rate above is the measure of how much of it is clean.
- **Which text is Pāḷi** is decided by script shape plus OSBCT attestation (see the tool's
  docstring). Short Burmese words that look like Pāḷi can slip in when they sit next to
  attested Pāḷi, and a badly OCR'd quotation can be missed. Each span carries `tokens` and
  `attested` so its strength is visible.
- Nothing is reviewed. Every row is `status: "ocr"`.
