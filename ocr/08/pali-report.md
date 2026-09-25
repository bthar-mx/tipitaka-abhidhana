# Vol. 08 — romanised Pāḷi

*`tools/abhidhana_romanise.py 08` over `articles.jsonl`. Aksharamukha Burmese → IAST, ṃ written ṁ.
Output: `pali.jsonl`, one row per article, keyed by `id`.*

| | |
|---|---:|
| headwords romanised | 6,448 (all) |
| compound analyses romanised | 4,949 |
| of which every element Pāḷi-shaped | 4,572 = 92.4% (the rest keep Burmese parts in ⟨ ⟩) |
| articles with Pāḷi found in the definition | 5,557 = 86.2% |
| Pāḷi spans | 20,900 |
| tokens in those spans | 78,764, of which **87.9% attested in OSBCT** |
| citations romanised (mechanically, abbreviations not expanded) | 23,701 |

What is and is not claimed:

- The **headword** romanisation rests on the index spelling, so it is as good as Aksharamukha.
- **Analyses and quoted Pāḷi** are romanised from OCR text. An OCR error becomes a romanisation
  error; the OSBCT attestation rate above is the measure of how much of it is clean.
- **Which text is Pāḷi** is decided by script shape plus OSBCT attestation (see the tool's
  docstring). Short Burmese words that look like Pāḷi can slip in when they sit next to
  attested Pāḷi, and a badly OCR'd quotation can be missed. Each span carries `tokens` and
  `attested` so its strength is visible.
- Nothing is reviewed. Every row is `status: "ocr"`.
