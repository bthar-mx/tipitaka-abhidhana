# Rendering the Abhidhāna into Spanish

*21 September 2026. Method, a worked sample, and the things that will go wrong. Nothing
here has been reviewed by a Burmese reader; every line of Spanish below is **drafted**.*

## 1. The rule that governs everything else

**Spanish is translated from the Burmese, never relayed through English.** This is the
Nissayas project's rule and it applies here for the same reason: the Burmese definition is
the thing being translated, and an English intermediate loses the compiler's own
distinctions — above all his alternatives, §3 below.

And the second rule: **translate by stem, not by row.** The lexicon is what compounds; a
row-by-row translation of 215,447 articles is a project that never finishes and leaves
nothing reusable behind.

## 2. The four fields, and what happens to each

| field | example | what to do |
|---|---|---|
| headword | **ဟီနာဒိဘေဒ** | romanise: `hīnādibheda`. Never translated. |
| label | (တိ) | expand, do not translate: `tiliṅga` → adjective |
| analysis | [ဟီန + အာဒိ + ဘေဒ] | keep as printed, romanised: `hīna + ādi + bheda` |
| definition | ယုတ်ညံ့ခြင်းအစရှိသော … | **this is what is translated** |
| citations | ထေရ၊ဋ္ဌ၊ ၂။ ၂၇၁။ | parse, never translate; resolve against OSBCT |

The labels are a closed set and should be fixed once:

| | Pāḷi | what it means | Spanish entry shows |
|---|---|---|---|
| (ပု) | pulliṅga | masculine noun | m. |
| (ထီ) | itthiliṅga | feminine noun | f. |
| (န) | napuṁsaka | neuter noun | n. |
| (တိ) | tiliṅga | adjective, all three genders | adj. |
| (ကြိ) | kriyā | verb | v. |
| (၁)(၂)(၃) | | numbered senses | 1. 2. 3. |
| (က)(ခ) | | lettered sub-senses | a. b. |

**Do not carry Pāḷi gender onto the Spanish noun.** `hīnādisabhāva` is (ပု), masculine in
Pāḷi; its Spanish rendering is *la naturaleza*, feminine, because Spanish gender follows
Spanish. The label describes the Pāḷi word, not the translation.

## 3. The hyphens are alternatives, and running them together is the first mistake

A TPMA definition writes alternative renderings of one Pāḷi element separated by hyphens:

> ဟီနအစရှိသော-အထူး-အပြားအားဖြင့်-**ကွဲပြား-ခြားနား**-သည်၏အဖြစ်ကို-**မြင်-ပြ**-ခြင်း

`ကွဲပြား-ခြားနား` is not "split-and-differ"; it is *differentiated*, **or** *distinct* —
two renderings of the one Pāḷi word. `မြင်-ပြ` is *seeing*, **or** *showing* — the compiler
declining to choose between two senses of `dassana`. This is the same device as the
nissaya's `, ဝါ-`, and the same discipline applies: **extract the alternatives into their
own field; a single Spanish phrase that merges them drops a reading.**

## 4. The definition language is formulaic, which is the whole opportunity

A first count over the OCR of vol. 25 (952,339 characters, 429 article pages — note this
text still contains the Pāḷi citations, so it understates the density in the definitions
proper):

| | |
|---|---:|
| ခြင်း — nominaliser, *-ción / el hecho de* | 1,201 |
| သူ — *el que…* | 611 |
| ရှိသော — *que tiene…* | 514 |
| တို့ — plural | 505 |
| အပ်သော — passive participle, *que es …-do* | 248 |
| အစရှိသော — `ādi-`, *que comienza por…* | 84 |
| ၏အဖြစ် — `bhāva`, *el hecho de ser…* | 50 |

The 500 commonest four-character clause endings cover 57.3% of clauses. So a few hundred
**formula-stems**, translated once and agreed, carry the bulk of the corpus — which is the
compounding asset, exactly as the gloss lexicon is in the Nissayas project. Build that
before translating a single article at scale.

## 5. Worked sample — vol. 25, printed p. 366

Seven consecutive articles. The Burmese is as printed; the Spanish is **drafted, unreviewed**.

---

**ဟီနာဒိဘေဒ** · `hīnādibheda` · adj. · [`hīna + ādi + bheda`]
ယုတ်ညံ့ခြင်းအစရှိသော အထူးအပြားရှိသော
→ *que tiene las diferencias que comienzan por la inferioridad*
⚠ the article has a second, masculine sense numbered (၂) which the whole-page OCR broke
across the column boundary. Re-read it from the `--columns` run before filing.

**ဟီနာဒိဘေဒဘိန္န** · `hīnādibhedabhinna` · adj. · [`hīnādibheda + bhinna`]
ဟီနအစရှိသော-အထူးအပြားအားဖြင့်-ကွဲပြား-ခြားနား-သော
→ *diferenciado* / *distinto* — por las diferencias que comienzan por lo inferior
(two renderings, kept apart)

**ဟီနာဒိဘေဒဘိန္နတာဒဿန** · `hīnādibhedabhinnatādassana` · n. ·
[`hīnādi + bheda + bhinna + tā + dassana`]
ဟီနအစရှိသော-အထူး-အပြားအားဖြင့်-ကွဲပြား-ခြားနား-သည်၏အဖြစ်ကို-မြင်-ပြ-ခြင်း
→ *el ver* / *el mostrar* el hecho de estar diferenciado por las diferencias que comienzan
por lo inferior

**ဟီနာဒိသဘာဝ** · `hīnādisabhāva` · m. · [`hīnādi + sabhāva`]
ဟီနအစရှိသောသဘော
→ *la naturaleza que comienza por lo inferior*

**ဟီနာဒိဝိဘာဂ** · `hīnādivibhāga` · m. · [`hīnādi + vibhāga`]
ဟီနအစရှိသည်ကို ဝေဘန်ခြင်း
→ *la división de aquello que comienza por lo inferior*

**ဟီနာဓိကဇနသေဝိတ** · `hīnādhikajanasevita` · adj. · [`hīna + adhika + jana + sevita`]
ယုတ်ညံ့သူ-မြင့်မြတ်သူ-တို့သည် မှီဝဲအပ်သော
→ *frecuentado por gentes humildes y encumbradas*

**ဟီနာဓိကဇနသေဝိတဝုတ္တိ** · `hīnādhikajanasevitavutti` · f. ·
[`hīna + adhika + jana + sevita + vutti`]
ယုတ်ညံ့သူ-မြင့်မြတ်သူ-တို့သည် မှီဝဲအပ်သော အသက်မွေးမှု
→ *el modo de vida frecuentado por gentes humildes y encumbradas*

---

**What this sample already shows.** Six of the seven share the element `hīnādi-`, and its
Burmese formula `ဟီနအစရှိသော` is translated once. Four share `-bhinna` / `-bheda`. The whole
run is one alphabetical neighbourhood and one stem family. That is what translating by stem
means in practice, and it is why the corpus is tractable at all.

**Uncertainties in this sample, named.** `အသက်မွေးမှု` for `vutti` is rendered *modo de
vida*; *sustento* is also defensible and the glossary should fix one. `ဝေဘန်` is given as
*dividir*; *analizar* is closer in some contexts. `မှီဝဲ` covers *frecuentar*, *recurrir a*
and *asociarse con*; *frecuentar* is chosen here and should be fixed or rejected by a
reader, not by me.

## 6. Review status, on every row

`drafted` → `reviewed` → `corrected`, the Nissayas project's three states. Nothing is ever
shown without one, and **nothing drafted is presented as a reading**. The interface says so,
the data carries it, and a count of each state is reported per page.

## 7. Scope: what not to promise

215,447 articles is not a translation project that finishes. What is tractable, in order:

1. **Romanise every headword.** Mechanical, checkable, and useful on its own — it makes the
   dictionary searchable from a romanised Pāḷi text for the first time.
2. **Parse and resolve the citations** against OSBCT. Also mechanical, and it ties the
   dictionary to the same canonical spine as the nissaya bridge.
3. **Build the formula lexicon** — a few hundred Burmese definitional stems with agreed
   Spanish renderings, reviewed once.
4. **Translate a prioritised slice**: the headwords the Therīgāthā nissaya and the typed
   corpus actually use. That is where the Abhidhāna pays the Nissayas project back, and it
   is a few thousand articles, not two hundred thousand.

Everything beyond that is a decision to take later, with a Burmese reader in the room.
