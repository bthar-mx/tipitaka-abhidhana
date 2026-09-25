# Grammatical labels: what the dictionary prints, and how OCR readings are mapped

*24 September 2026, from vol. 1. `tools/abhidhana_articles.py` applies this (`LABEL_SET`,
`_LABEL_READINGS`). Every row carries `label` (the printed label, or None), `label_ocr` (what the
OCR read) and `label_how` (`exact`, `mapped`, `inferred`).*

## 0. The label table

*25 September 2026. **This table is read by the pipeline and the website**
(`tools/abhidhana_labels.py` parses it; `tools/abhidhana_articles.py` maps OCR readings with it;
the site's label pop-ups and its Labels page show it). Edit it here and nowhere else.*

- **status**: `confirmed` once Angel has agreed the label and its Pāḷi; otherwise `provisional`,
  and the site says so. Confirmed so far: the five of `docs/spanish-method.md` §2, (ဗျ) and (ကာ၊ကြိ)
  (Angel, 25 Sep 2026).
- **English, Spanish**: what the label marks, as the pop-up shows it. The Spanish is a draft
  (`es` = `draft`) until Angel confirms it; the site marks a draft as provisional in the Spanish
  interface.
- **abbr. en / abbr. es**: the short gloss beside the label. The Spanish abbreviations are
  Angel's to fix (IEBH glossary); until then none is shown in Spanish.
- **OCR readings**: every reading mapped to the label (spaces removed). Add one only after
  checking it on the page image (§2, §5).
- The row order is the order the pipeline tries them; it matters only for the "junk tail" rule.

<!-- labels:begin -->
| label | Pāḷi | English | Spanish | abbr. en | abbr. es | status | es | OCR readings |
|---|---|---|---|---|---|---|---|---|
| (ပု) | pulliṅga | masculine noun | sustantivo masculino | m. |  | confirmed | draft | ပု ပ ၇ ပြ ပူ ပုံ ဖု ြု ၇ု ု ပ၇ ပြု မ ပု၊ ပု။ |
| (ထီ) | itthiliṅga | feminine noun | sustantivo femenino | f. |  | confirmed | draft | ထီ ထိ ထံ ထ တီ သီ ၊ထီ |
| (န) | napuṁsaka | neuter noun | sustantivo neutro | n. |  | confirmed | draft | န နံ |
| (တိ) | tiliṅga | adjective | adjetivo | adj. |  | confirmed | draft | တိ တ တ် ဘိ |
| (ကြိ) | kriyā | verb | verbo | v. |  | confirmed | draft | ကြိ က ကြ ကြု ကြံ ကြ် ကကြ ကြို ကြီ ကြါ ကြပ် ကြရ ကိ ဤ ၍ |
| (ကြိ၊ဝိ) | kriyā-visesana? | absolutive or infinitive (-tvā, -tvāna, -tuṁ, -ya) | absolutivo o infinitivo (-tvā, -tvāna, -tuṁ, -ya) | abs./inf. |  | provisional | draft | ကြိ၊ဝိ ကြ၊ဝိ ကြ်၊ဝိ ကြံ၊ဝိ ကြို၊ဝိ ကြါ၊ဝိ ကြီ၊ဝိ ကဝိ ၉ြိ၊ဝိ ကြိးဝိ ကြိ[ဝိ ကြု၊ဝိ ကြ၊ဒိ ကိ၊ဝိ ကြိ၊ဒိ ကြိုဝိ ကြိုငိ ကြုဝိ ကြ၊ပိ ကြါဝိ ကြိဝိ ကြ၊ဝ ကြ၊ ကြင် ကြံးဝိ ကြ်းဝိ ကြီးဝိ ကြိ၊ိ ိ၊ဝိ ကြဝိ |
| (ကာ၊ကြိ) | kārita-kriyā | causative verb | verbo causativo | caus. v. |  | confirmed | draft | ကာ၊ကြို ကာ၊ကြ ကာ၊ကြ် |
| (နာမ-ကြိ) | nāmadhātu? | denominative verb | verbo denominativo | denom. v. |  | provisional | draft | နာမ-ကြ |
| (ဗျ) | abyaya | indeclinable | indeclinable | indecl. |  | confirmed | draft | ဗျ ဗ |
| (ပု၊န) | pulliṅga-napuṁsaka | masculine or neuter noun | sustantivo masculino o neutro | m./n. |  | provisional | draft | ပုန ပု၊န ပန ပု၊နု ပုန၊ |
| (ပု၊ထီ) | pulliṅga-itthiliṅga | masculine or feminine noun | sustantivo masculino o femenino | m./f. |  | provisional | draft | ပု၊ထီ ပုထ ပုသ ပု၊ထီ? |
| (ပု၊တိ) | pulliṅga-tiliṅga | masculine noun or adjective | sustantivo masculino o adjetivo | m./adj. |  | provisional | draft | ပု၊တိ ပတိ |
| (န၊ပု) | napuṁsaka-pulliṅga | neuter or masculine noun | sustantivo neutro o masculino | n./m. |  | provisional | draft | န၊ပု န၊၇ |
| (န၊ထီ) | napuṁsaka-itthiliṅga | neuter or feminine noun | sustantivo neutro o femenino | n./f. |  | provisional | draft | န၊ထီ န၊ထံ န၊ထိ န၊သီ နု၊သီ န၊တီ |
| (န၊တိ) | napuṁsaka-tiliṅga | neuter noun or adjective | sustantivo neutro o adjetivo | n./adj. |  | provisional | draft | န၊တိ နတိ |
| (တိ၊န) | tiliṅga-napuṁsaka | adjective or neuter noun | adjetivo o sustantivo neutro | adj./n. |  | provisional | draft | တိ၊န |
| (ပုံ-ဗဟု) | pulliṅga bahuvacana | masculine, plural only | masculino, solo en plural | m. pl. |  | provisional | draft | ပုဗဟု ပုံဗဟု ပုံ-ဗဟု ပု-ဗဟု |
| (စတုတ္ထန္တ) | catutthanta | ending in the fourth case (meaning a guess) | terminado en el cuarto caso (significado supuesto) |  |  | provisional | draft | စတုတ္ထန္တ |
| (တတိယန္တ-ဗျ) | tatiyanta abyaya? | indeclinable ending in the third case (not image-checked) | indeclinable terminado en el tercer caso (no comprobado en la imagen) |  |  | provisional | draft | တတိယန္တ-ဗျ |
| (ကမ္မ၊ကြိ) | kamma-kriyā? | passive verb | verbo pasivo | pass. v. |  | provisional | draft | ကမ္မ၊ကြိ ကမ္မ၊ကြို ကမ္မ၊ကြ် ကမ္မကြို ကမ္မကြိ ကမ္ပကြိ ကမ္ပ၊ကြိ |
| (ထီ၊န) | itthiliṅga-napuṁsaka | feminine or neuter noun | sustantivo femenino o neutro | f./n. |  | provisional | draft | ထီ၊န ထံ၊န |
| (ထီ၊ပု) | itthiliṅga-pulliṅga | feminine or masculine noun | sustantivo femenino o masculino | f./m. |  | provisional | draft | ထီ၊ပု ထိ၊ပု ထိ၊ပူ |
| (အ-လိင်) | aliṅga | without gender | sin género |  |  | provisional | draft | အ-လိင် အလိင် |
| (ကာ၊ကြိ၊ဝိ) | kārita-kriyā-visesana? | causative absolutive | absolutivo causativo | caus. abs. |  | provisional | draft | ကာ၊ကြိ၊ဝိ ကာ၊ကြ၊ဝိ ကာ၊ကြိံဝိ ကာ၊ကြိဝိ ကာကြိဝိ ကာ၊ကြ၊ဝိ၊ ကာ၊ကြါ၊ဝိ ကာ၊ကြးဝိ |
| (ကာ၊ကမ္မ၊ကြိ) | kārita-kamma-kriyā? | causative passive verb | verbo causativo pasivo | caus. pass. v. |  | provisional | draft | ကာ၊ကမ္မ၊ကြိ ကာ၊ကမ္မ၊ကြို ကာ၊ကမ္မ၊ကြ |
<!-- labels:end -->

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
| (ဗျ) | 41 | abyaya | indeclinables and adverbs: ajja, aññathā, ati, aṭṭhakkhattuṁ, ativiya | **confirmed by Angel, 25 Sep 2026** |
| (န၊ထီ) | 30 | | neuter or feminine | image, p. 159 |
| (န၊တိ) (ပု၊တိ) (တိ၊န) | 9 · 7 · 4 | | noun and adjective | images, pp. 152, 228 |
| (ပု၊ထီ) | 7 | | masculine or feminine | images, pp. 362, 670, 733 |
| (ကာ၊ကြိ) | 9 | kārita-kriyā | causative verb: agghāpeti, and -āpeti in 5 of 9 | image, p. 249; **confirmed by Angel, 25 Sep 2026** |
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
headword. *(25 Sep: matched on the converted Burmese instead, it has 99.9% of vol. 1's headwords; see `docs/witness.md`.)* Its first label, converted from Zawgyi (ႀကိ → ကြိ, ဗ် → ဗျ, ကမၼ → ကမ္မ) and set against
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

## 6. Added from vols. 2–3 (24 September 2026)

Each of these is a label the typed witness prints, so it was added without an image check.

| label | vol. 2 | vol. 3 | read as | what it marks (as far as the headwords show) |
|---|---:|---:|---|---|
| (ကမ္မ၊ကြိ) | 11 | 24 | (ကမ္မ၊ကြို), (ကမ္မ၊ကြ်), (ကမ္မ ကြို) | passive verb? (kamma-kriyā); the witness has 507 |
| (ထီ၊န) | 2 | 1 | | feminine or neuter |
| (ထီ၊ပု) | 3 | 2 | (ထိ၊ပု), (ထိ၊ ပူ) | feminine or masculine |
| (အ-လိင်) | – | yes | (အလိင်) | aliṅga, "without gender"; the witness has 20 |

Readings also mapped: (န၊တီ) → (န၊ထီ); (ပုန၊) → (ပု၊န); (ကြီးဝိ), (ကြိ၊ိ), (ိ၊ဝိ), (ကြ။ ဝိ) → (ကြိ၊ဝိ).
A sense number run into the label, (ပု ၂), is read as the label. Against the witness, the
normalised labels agree on 99.0% (vol. 1), 99.2% (vol. 2) and 98.8% (vol. 3) of the articles
normalised. The raw readings agree on 81.2%, 83.0% and 86.4%.

## 7. Added from vol. 6 (25 September 2026)

| label | rows, vols. 3–6 | Pāḷi | what it marks | how firm |
|---|---:|---|---|---|
| (ကာ၊ကြိ၊ဝိ) | 35 | kārita-kriyā-visesana? | causative absolutive: every row is a -tvā / -tvāna form (ဂါဟေတွာ, ခါဒါပေတွာ, ဥပ္ပါဒယိတွာန) | image, vol. 6 p. 852 (ဂါဟေတွာ); the witness prints it 418 times; **expansion a guess**, from the other two |

Until now the reading fell to the "junk tail after a valid combination" rule and was cut to
(ကာ၊ကြိ), dropping the ၊ဝိ. Readings mapped: (ကာ၊ကြိ၊ဝိ), (ကာ၊ကြ၊ဝိ), (ကာ၊ကြိံဝိ), (ကာ၊ကြိဝိ),
(ကာကြိဝိ), (ကာ၊ကြ၊ဝိ၊), (ကာ၊ကြါ၊ဝိ), (ကာ၊ကြးဝိ). Only the first was checked on the image; the
others are the same misreadings of ကြိ and ၊ already mapped for (ကြိ၊ဝိ) and (ကာ၊ကြိ).

**Readings seen in vol. 6 and not mapped**, because not image-checked: (ထိန) 8, (ထီ၊၇) 4, (ထိ၊ ၇) 3,
(ထိ၊န) 3, (ထီ၊ ၇) 2, (ထိ၊ န) 2. They look like (ထီ၊န) and (ထီ၊ပု) (၇ is the usual misreading of
ပု), but that is a guess. Examples to check: ids 51227 (p. 211), 51941 (p. 294), 54340 (p. 527).

**Against the typed witness**, with the join of `docs/witness-join.md` (homonyms paired in order),
the normalised labels agree on 98.7–99.2% per volume. About half the remaining disagreements are
(တိ) against a single gender, (ထီ)/(န)/(ပု), as §4 found; a sample has not yet been checked on the
image to say which side is right.
