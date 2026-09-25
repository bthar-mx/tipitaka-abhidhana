# Grammatical labels: what the dictionary prints, and how OCR readings are mapped

*24 September 2026, from vol. 1. `tools/abhidhana_articles.py` applies this (`LABEL_SET`,
`_LABEL_READINGS`). Every row carries `label` (the printed label, or None), `label_ocr` (what the
OCR read) and `label_how` (`exact`, `mapped`, `inferred`).*

## 1. The labels vol. 1 prints

`docs/spanish-method.md` §2 lists five labels. The page images show more. The first five come
from §2. The rest are **observed, not yet agreed**: the Pāḷi expansion and the Spanish
abbreviation are Angel's to fix (IEBH glossary), and the "reading" column says how firm each one is.

| label | vol. 1 rows | Pāḷi | what it marks | how firm |
|---|---:|---|---|---|
| (တိ) | 2,998 | tiliṅga | adjective | §2 |
| (ပု) | 1,458 | pulliṅga | masculine noun | §2 |
| (န) | 1,283 | napuṁsaka | neuter noun | §2 |
| (ထီ) | 808 | itthiliṅga | feminine noun | §2 |
| (ကြိ) | 236 | kriyā | verb, incl. the aorists and optatives listed as cross-references | §2 |
| (ကြိ၊ဝိ) | 174 | kriyā-visesana? | on -tvā (95), -tuṁ (26), -ya (17), -tvāna (7) forms: absolutives and infinitives | the class is certain from the headwords; **the expansion is my guess**, not checked |
| (ပု၊န) | 70 | pulliṅga-napuṁsaka | noun of either gender | printed with ၊ (pp. 210, 803); OCR usually loses it |
| (ဗျ) | 41 | abyaya? | indeclinables and adverbs: ajja, aññathā, ati, aṭṭhakkhattuṁ, ativiya | class certain; **expansion a guess** |
| (န၊ထီ) | 30 | | neuter or feminine | image, p. 159 |
| (န၊တိ) (ပု၊တိ) (တိ၊န) | 9 · 7 · 4 | | noun and adjective | images, pp. 152, 228 |
| (ပု၊ထီ) | 7 | | masculine or feminine | images, pp. 362, 670, 733 |
| (ကာ၊ကြိ) | 9 | kārita-kriyā? | causative verb: agghāpeti, and -āpeti in 5 of 9 | image, p. 249; expansion a guess |
| (န၊ပု) | 5 | | neuter or masculine | not image-checked |
| (ပုံ-ဗဟု) | 2 | pulliṅga bahuvacana | masculine, plural only: aṅguttarāpa (a people) | image, p. 272, and the typed witness (§4) prints it so |
| (နာမ-ကြိ) | 1 | nāmadhātu? | denominative verb: aticirāyati | image, p. 500 |
| (စတုတ္ထန္တ) | 1 | catutthanta | aññā, "ending in the 4th case" | image, p. 407; meaning a guess |
| (တတိယန္တ-ဗျ) | 1 | tatiyanta abyaya? | | not image-checked |

Numbered and lettered senses, (၁)(၂) and (က)(ခ), are not labels and are not normalised. A sense
can carry its own label inside the body, e.g. anindā p. 876: (ထီ) … (က) … (တိ) (၁).

## 2. How OCR misreads them, and what was checked

Each mapping below was checked against the page image on a sample. The ids are word ids from
`db/tipitaka_abidan.db`, and the article's PDF page is in `articles.jsonl`.

| printed | read as | checked on |
|---|---|---|
| (ပု) | (ပ) 333, (၇) 241, (ပြ), (ပူ), (မ), (ု) … | ပ: 1658 7027 812 2874 1417, 4651 1820 539 6992 6604 2556 7498 2344 2545 274 3114; ၇: 6614 3919 4145 5591 3361 6950, 1327 7825 1392; ပြ: 182 1671; ပူ: 5479 7971; မ: 1111; ု: 7372 |
| (ထီ) | (ထိ) 86, (ထံ) 56, (ထ) 30, (တီ) 11, (သီ), (၊ထီ) | 2677 1205 6601 469 6736 7794 2614 5629 417 7296, 2558 2766 3694 6562; တီ: 3777 2098 (and all 11 are feminine words); သီ: 6246 6530 |
| (တိ) | (တ), (တ်), (ဘိ) | တ: 5298 2115; ဘိ: 7744 7943 |
| (ကြိ) | (က) 70, (ကြု) 51, (ကြံ) 20, (ကြ်), (ကြ), (ကကြ), (ဤ), (၍) … | 5738 5882 26 5892 4519 5735 664 2407 342 7349 153 5883 6370 3725 5884 4583 4472, 5881 2429 4320 6831 |
| (ကြိ၊ဝိ) | (ကြ၊ ဝိ), (ကြိ၊ဒိ), (ကြ၊), (ကြင်), (ကြပ်), (ကြိုငိ) … | 3039 5663 8014 2002 3146 4557 2710 3861 3008 |
| (ဗျ) | (ဗ) | 5626 6678 4235; ဗ: 5931 |
| (ပု၊န) (ပု၊ထီ) (ပု၊တိ) (န၊တိ) | (ပုန), (ပန); (ပုထ), (ပုသ); (ပတိ); (နတိ) | 1413 6252 1035 7185 5025; 2933 4296 6540 |

**Inferred (3 rows):** a verb reading on a -tvā / -tvāna / -tuṁ headword is taken as (ကြိ၊ဝိ)
with the ၊ဝိ lost. Five of five checked were so (711, 2002, 2710, 3146, 4557), and 711 had been
read as a clean (ကြိ). -ya absolutives are **not** inferred: 5662 adaṇḍiya is printed (ကြိ).

**Deliberately not mapped** (label left None, reading kept):
- (တံ): (တိ) on 455, but (ထီ) on 7901 and on 4572, atibuddhi, an -i stem. The ending cannot decide it.
- (ယီ): on 2906 it is a spelling variant printed in the headword, အဇ္ဈာယိ (ယီ) (တိ).
- Digits (၁)(၂)(၃)(၅) in the label slot: the image shows a lost label, e.g. 2796 is (ပု) and 1670 is (န).
  They cannot be recovered from the reading.

**Two parentheses in a row.** A spelling variant can sit inside the printed headword, e.g.
အကာလုသိ(ဿိ)ယ (န), အဇ္ဈာရု(ရူ) (တိ), အနိက္ခိတ္တစ္ဆ(ဆ)န္ဒ (တိ). The variant goes to
`headword_variant`, and the parenthesis that follows is taken as the label. Debris before a label,
e.g. အဋ္ဌိသင်ာတ (ဋ) (တိ), goes to `label_debris`.

## 3. Blind check

After the map was built, 32 rows not used to build it were drawn at random: 24 mapped, 2
inferred and 6 exact. Each was checked against its page image, and 30 were right. The two errors
were 4572 (an inferred (တံ) → (တိ) that should be (ထီ)) and 2906 (ယီ, a headword variant). Both
rules were removed. That check was run before the article-location change of the same day,
which added about 500 labels read by the same map.

## 4. The typed witness: PCED's "Tipiṭaka Pāḷi-Myanmar Dictionary"

dictionary.sutta.org is built from Pali Canon E-Dictionary 1.94. Its data, in the public repo
`siongui/data` (`dictionary/dict_words_{1,2}.csv`), holds a dictionary with id `K` titled
"Tipiṭaka Pāḷi-Myanmar Dictionary တိပိဋက-ပါဠိမြန်မာ အဘိဓာန်". It has 157,271 entries, typed in
**Zawgyi**, not Unicode. It is this dictionary's text: for p. 300, accāvadati reads
(ကြိ) [အတိ+အာ+ဝဒ+အ+တိ] လွန်၍ပြောဆို၏။ (က) … (ခ) … (ဂ) …, as printed. It appears to omit the Pāḷi
quotations and their citations: 158 of the 7,714 vol. 1 entries have a reference numeral.

It has an entry for **7,714 of vol. 1's 8,150 headwords (94.7%)**, matched on the romanised
headword. Its first label, converted from Zawgyi (ႀကိ → ကြိ, ဗ် → ဗျ, ကမၼ → ကမ္မ) and set against
ours on the 6,836 articles where both exist:

| | agree with the witness |
|---|---:|
| OCR readings before this map (commit 40e6be1) | 81.3% |
| **normalised labels** | **98.5%** (6,735 / 6,836) |
| of which `exact` / `mapped` / `inferred` | 99.3% / 97.5% / 3 of 3 |

Most of the remaining disagreement is (ထီ)↔(တိ) and (န)↔(တိ). These words carry two labels
(a noun sense and an adjective sense), and the witness's first label is not always the one
printed first. The witness also uses labels vol. 1 does not: (ကမ္မ၊ကြိ) 507 (passive verb?),
(ကာ၊ကြိ၊ဝိ) 418, (ထီ၊န) 678, (ထီ၊ပု) 266. Expect them from vol. 2 on.

A second witness, not ground truth: the index is still the authority for headwords, and the
printed page is the authority for everything else.

## 5. For vol. 2 onwards

Re-run the census: `label_ocr` values with `label` None are listed at the foot of each
`articles-report.md`. Add a reading to `_LABEL_READINGS` only after checking it on the image.
