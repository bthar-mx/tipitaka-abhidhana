# Brief: drafting the Meaning box of the Tipiṭaka Pāḷi-Myanmā Abhidhāna, vol. 1

You translate the **Burmese explanations** of a Pāḷi → Burmese dictionary into **Spanish and English**. Each draft is marked *drafted* and will be reviewed by a human reader of Burmese. Accuracy matters more than elegance. Consistency across thousands of articles matters more than variety.

## Input

Each shard line has these fields:

```
{"id": 123, "iast": "headword romanised", "label": "တိ", "text": "the Burmese definition"}
```

- **label** is the Pāḷi word class: တိ = adjective, ပု = masculine noun, န = neuter noun, ထီ = feminine noun, ကြိ = verb.
- Use the label and the headword to understand the definition. **Never translate the headword.**
- `«S1»`, `«S2»` … are placeholders for "see X" / "same meaning as X" formulas. Another step renders them. Copy each one **unchanged** to the same place in both translations.

## Output

Write one JSON line per input line, in the same order, to the output file you are given:

```
{"id": 123, "es": "…", "en": "…", "terms": ["kusala"], "flag": ""}
```

- **terms**: the IAST of every Buddhist technical term you kept as Pāḷi (see rule 6).
- **flag**: a short English note when you are unsure (an unclear or garbled Burmese word, or two plausible readings). Otherwise use "".

## Rules

1. **Translate from the Burmese.** Write the Spanish directly from the Burmese, not from your English. Spanish is the primary output; English is its companion.
2. **Hyphens mark alternatives.** A hyphen separates alternative renderings of one Pāḷi element.
   - `ကွဲပြား-ခြားနား-သော` → `diferenciado / distinto` · `differentiated / distinct`.
   - Keep every alternative and join them with ` / `. Never merge two alternatives into one word.
   - When the hyphens chain a phrase (`A-B-C-သော D`), render it as `A / B / C D`, keeping the order.
3. **Punctuation.**
   - `၊` separates alternative definitions → `; `.
   - `။` ends a sentence → `.`.
   - A Burmese `,` inside a list → `, `.
4. **Sense markers.** `(၁) (၂)` → `(1) (2)`; `(က) (ခ)` → `(a) (b)`.
   - A label inside the definition becomes the full word, in parentheses:

     | Burmese | Spanish | English |
     |---|---|---|
     | (တိ) | (adjetivo) | (adjective) |
     | (ပု) | (masculino) | (masculine) |
     | (န) | (neutro) | (neuter) |
     | (ထီ) | (femenino) | (feminine) |
     | (ကြိ) | (verbo) | (verb) |

   - A bracketed Burmese gloss such as `(အသားမရှိသည်ဖြစ်၍)` is translated, with its brackets kept.
5. **Do not translate Pāḷi.** Pāḷi written in Burmese script — a Pāḷi word, a compound, or a quoted phrase or sentence given as an example — is copied exactly, wrapped in `⟦ ⟧`.
   - Example: `⟦အဂ္ဂိဋ္ဌာ⟧`.
   - A later step romanises it. Do not romanise it yourself, and do not translate it.
   - Pāḷi-in-Burmese has none of these marks: asat ် (except in kinzi), း, ့, ဲ, ို, ၌ ၍ ၏.
   - Drop citation references such as `တိပိ၊၁၊၁` or `ဝိ၊၂။၃၄၅။`. They are shown elsewhere.
6. **Buddhist technical terms and the glossary.**
   - Use the renderings in `stems.tsv` (columns `en`, `es`) **exactly**. When a row offers several renderings, choose the one that fits the context.
   - For a doctrinal term the table lacks, keep the Pāḷi, romanised by you as `⟦=iast⟧`. Examples: `ကုသိုလ်` → `⟦=kusala⟧`, `ဈာန်` → `⟦=jhāna⟧`, `ဝိပဿနာ` → `⟦=vipassanā⟧`, `ပစ္စေကဗုဒ္ဓါ` → `⟦=paccekabuddha⟧`.
   - Add a Spanish or English gloss after it only when the Burmese itself explains it.
   - List each such term in `terms`.
   - Ordinary words are translated normally.
7. **Pāḷi gender stays with the Pāḷi.** Spanish nouns take their own Spanish gender. The Pāḷi label says nothing about the Spanish noun.
8. **The recurring formulas.** Follow the F-rows of `stems.tsv`:

   | Burmese | Spanish | English |
   |---|---|---|
   | -ခြင်း | el/la + noun (-ción, -miento) or el + infinitive | …-ing / the act of … |
   | -သော | que … / participle | that … / …-ing |
   | -အပ်သော | participle -do (the passive) | …-ed |
   | -သည်၏အဖြစ် / ၏အဖြစ် | el hecho de ser … | the state of being … |
   | -ရှိသော | que tiene … | having … |
   | …သော၊ သူ။ | … (dicho de una persona) | … (said of a person) |
   | …သော၊ သည်။ | … (dicho de una cosa) | … (said of a thing) |
   | …သော၊ သူ၊ သည်။ | … (dicho de una persona o de una cosa) | … (said of a person or a thing) |
   | -စသော / အစရှိသော | … y demás / que comienza por … | … and so on / beginning with … |
   | -ကဲ့သို့ | como | like |
   | မ- | no … / in- | not … / un- |
   | -၏ on a verb | 3rd person present: `va`, `conoce` | `goes`, `knows` |

   - For the rows with သူ / သည်, do NOT write "el que es tal" or "lo que es tal". Write, for example, `que no tiene duda (dicho de una persona o de una cosa)`.
   - Glosses start in lower case, as in a dictionary, and each sentence ends with a full stop.
   - A definition with nothing to translate (for example only `။`) gets `"es": "", "en": ""` and a flag.

9. **Be literal but readable.** Keep the compiler's structure and every alternative. Do not add explanations the Burmese does not give.
   - Numbers of things stay numbers.
   - Proper names of people and places, written in Burmese script, are Pāḷi: wrap them in `⟦ ⟧`.
10. **When the Burmese looks garbled or truncated**, translate what is clear, and say what is not in `flag`.

## How to work

- Read `stems.tsv` first.
- Process the shard **in blocks of about 40 lines**. Translate a block, then append it to the output file with a small Python snippet (`json.dumps(..., ensure_ascii=False)`, one object per line).
- Do not rewrite earlier blocks. If you are interrupted, the file must still hold every finished line.
- Finish the whole shard.
- At the end, check that the output has exactly one line per input id, all valid JSON, and that every `«Sn»` placeholder survives in both `es` and `en`. Fix what fails.
- Reply with the counts only: lines written, lines flagged, and the ten commonest `terms`.
