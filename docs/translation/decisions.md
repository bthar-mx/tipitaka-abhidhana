# Decision sheet for the final revision (plan step 2.1)

*Written 29 Sep 2026 (Cowork), after v0.28.0. Nothing in the data was changed and nothing redrafted. Every count was
measured by script (`tmp/dec21/flags.py`, `gather.py`, `extra.py`, `spec*.tsv`; outputs `gather.json`, `flags-by-kind.tsv`);
none is estimated. The recommendations are Claude's and are marked as such; where Claude is unsure it says so.*

**How the counts were made.** *Rows* are Meaning rows (217,450). Where a question is about a Burmese word, the count is
the rows whose Burmese source text (the text the drafts were made from: `tmp/meanings/vNN/workNN.json`, 209,678 rows)
contains it as a substring; **vol. 1 (no work file) and the 238 split rows of v0.28.0 are not in those counts**, and a
short word over-counts (it is found inside longer ones). *Current Spanish* counts are rows among those whose `es` matches
the rendering (a row can match two). Verb-person counts use the verb label (ကြိ…) of the work file. Flag counts come from
the 29 `-flags.tsv` files (41,042 rows). Links open the headword on the site (all homonyms); the id picks the row.

**How to answer.** Write the option letter (or your own wording) after each **Decision:**. Decisions go to `stems.tsv`,
`glossary.tsv` and `drafting-prompt.md` as on 27 Sep, and are applied in step 2.3 (by script where lexical, by agents where
the sense or person decides), every changed row staying `drafted` with `revised: <question id>`.

---

## A. Verb person

The rule of 27 Sep: the person follows the Pāḷi ending (paṭhama 3rd, majjhima 2nd, uttama 1st). What it leaves open is the
endings that are two forms at once. The Burmese gloss nearly always shows which one the lexicographers meant: ပြီ marks a
past (aorist), ရာ၏ an optative, လော့ an imperative, ကုန် a plural.

**A1. -esi headwords** — the present 2nd sg of an e-stem (*desesi* "you teach") and the aorist 3rd sg (*desesi* "he taught")
are the same word. **545 verb rows; 396 have ပြီ in the Burmese; 125 flagged.** The drafts split: most shards 3rd person, some
2nd (brief §54, §57, §60, §63). Examples: [36737](https://abhidhana.buddha-dhamma.net/w/upa%E1%B9%AD%E1%B9%ADhesi) upaṭṭhesi (4/2) [177654](https://abhidhana.buddha-dhamma.net/w/sanniv%C4%81resi) sannivāresi (22) [219765](https://abhidhana.buddha-dhamma.net/w/h%C4%81resi) hāresi (25); 14/2 [213807](https://abhidhana.buddha-dhamma.net/w/parip%C4%81tesi) paripātesi (14/2) (2nd) vs [215427](https://abhidhana.buddha-dhamma.net/w/pariva%E1%B9%AD%E1%B9%ADesi) parivaṭṭesi (14/2) (3rd).
Options: (a) always aorist 3rd sg; (b) always present 2nd sg (the -si rule read literally); (c) **by the Burmese**: ပြီ → aorist
3rd sg, otherwise present 2nd sg.
*Recommended: (c).* The Burmese is the dictionary's own parse; (a) and (b) are each wrong for part of the set. R2 (§51) left
-si out of the revision queue for this reason.
**Decision:**

**A2. Other -si headwords** (-asi, -isi, -āsi, -osi …; not -ssasi) — **533 verb rows; 104 with ပြီ; 128 flagged.** Mostly present
2nd sg ([35305](https://abhidhana.buddha-dhamma.net/w/udikkhasi) udikkhasi (4/2) udikkhasi, [130763](https://abhidhana.buddha-dhamma.net/w/mil%C4%81yasi) milāyasi (16) milāyasi); a few are aorists ([219860](https://abhidhana.buddha-dhamma.net/w/hi%E1%B9%81si) hiṁsi (25) hiṁsi). Options as A1. *Recommended: (c)*, same reason.
**Decision:**

**A3. -ttha / -ittha** — aorist 2nd pl (parassapada) or aorist 3rd sg (attanopada). **173 verb rows; 152 with ပြီ; 29 flagged.**
Examples: [72899](https://abhidhana.buddha-dhamma.net/w/%E1%B9%ADhapayittha) ṭhapayittha (8) [176536](https://abhidhana.buddha-dhamma.net/w/olokayittha) olokayittha (4/3) [218386](https://abhidhana.buddha-dhamma.net/w/ha%C3%B1%C3%B1ittha) haññittha (25); [193484](https://abhidhana.buddha-dhamma.net/w/pavassittha) pavassittha (14/3) rendered *llovisteis* (2nd), [167879](https://abhidhana.buddha-dhamma.net/w/sa%C3%B1carittha) sañcarittha (21) 3rd.
Options: (a) 3rd sg; (b) 2nd pl; (c) **by the Burmese**: a 2nd-person plural gloss (သင်တို့, ကုန်) → 2nd pl, otherwise 3rd sg.
*Recommended: (c)*, with low confidence on how often the Burmese marks the plural (not counted); rows with neither mark
stay flagged.
**Decision:**

**A4. -etha** — optative 3rd sg attanopada (*labhetha*) or present / imperative 2nd pl of an e-stem (*desetha*). **269 verb rows;
51 flagged.** Examples: [17478](https://abhidhana.buddha-dhamma.net/w/abhisambhavetha) abhisambhavetha (3) [164298](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81s%C4%81detha) saṁsādetha (21) [210773](https://abhidhana.buddha-dhamma.net/w/payojetha) payojetha (14/2); [189075](https://abhidhana.buddha-dhamma.net/w/sahetha) sahetha (23) sahetha, [163912](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81vibhajetha) saṁvibhajetha (20) (-etha with …လော: imperative).
Options: (a) optative 3rd sg; (b) 2nd pl; (c) **by the Burmese ending**: ရာ၏ → optative 3rd sg, လော့ → imperative 2nd pl, ၏ with
a 2nd-person plural → present 2nd pl. *Recommended: (c).*
**Decision:**

**A5. Other -tha** (-atha, -eyyātha …) — 2nd pl by R2 already. **472 verb rows; 119 flagged.** Examples: [35512](https://abhidhana.buddha-dhamma.net/w/uddiseyy%C4%81tha) uddiseyyātha (4/2) [130756](https://abhidhana.buddha-dhamma.net/w/mil%C4%81yatha) milāyatha (16) [214633](https://abhidhana.buddha-dhamma.net/w/parimajjatha) parimajjatha (14/2).
*Recommended: keep R2 (2nd pl)*; nothing new to decide except A7.
**Decision:**

**A6. Verb headwords in -aṁ** — -eyyaṁ, -issaṁ and the aorist -aṁ are 1st sg; -taṁ is the 3rd sg imperative attanopada.
**388 verb rows; 141 flagged.** Examples: [50110](https://abhidhana.buddha-dhamma.net/w/k%C4%ABl%CC%A4eyya%E1%B9%81) kīl̤eyyaṁ (6) kīḷeyyaṁ, [114244](https://abhidhana.buddha-dhamma.net/w/phusissa%E1%B9%81) phusissaṁ (15) phusissaṁ, [219351](https://abhidhana.buddha-dhamma.net/w/har%C4%81peyya%E1%B9%81) harāpeyyaṁ (25) harāpeyyaṁ; 14/3 [196508](https://abhidhana.buddha-dhamma.net/w/p%C4%81pata%E1%B9%81) pāpataṁ (14/3) [196512](https://abhidhana.buddha-dhamma.net/w/p%C4%81patta%E1%B9%81) pāpattaṁ (14/3)
[196513](https://abhidhana.buddha-dhamma.net/w/p%C4%81pattha%E1%B9%81) pāpatthaṁ (14/3) (pāpataṁ … taken as 1st sg, flagged: probably not verbs).
Options: (a) by the ending as listed; (b) leave as drafted. *Recommended: (a)*; the three 14/3 rows to the page check (F6).
**Decision:**

**A7. vosotros or ustedes** for the 2nd person plural — **295 rows have vosotros forms, 14 ustedes** (vol. 4/2 9). Examples:
[160867](https://abhidhana.buddha-dhamma.net/w/ve%E1%B9%ADhetha) veṭhetha (20) [221132](https://abhidhana.buddha-dhamma.net/w/hotha) hotha (25) [36025](https://abhidhana.buddha-dhamma.net/w/upakappetha) upakappetha (4/2) (ustedes); [176432](https://abhidhana.buddha-dhamma.net/w/olamb%C4%81petha) olambāpetha (4/3) olambāpetha (§70).
Options: (a) *vosotros*; (b) *ustedes*; (c) *ustedes*, with (2.ª pl.) after the verb.
*Recommended: (a) vosotros, low confidence — a house-style question.* With *ustedes* the verb is 3rd-person plural, so a
2nd-person headword and a 3rd-person one gloss the same, and the dictionary exists to show that difference. IEBH writes for
Mexican readers, who say *ustedes*: if that weighs more, (c).
**Decision:**

**A8. Future headwords whose Burmese has a past (ပြီ)** — **57 verb rows; 5 flagged.** Examples: [94896](https://abhidhana.buddha-dhamma.net/w/ni%E1%B9%AD%E1%B9%ADh%C4%81pess%C4%81mi) niṭṭhāpessāmi (12) [96114](https://abhidhana.buddha-dhamma.net/w/nipph%C4%81dess%C4%81mi) nipphādessāmi (12) [162218](https://abhidhana.buddha-dhamma.net/w/voropessatha) voropessatha (20);
[158190](https://abhidhana.buddha-dhamma.net/w/vissajjissanti) vissajjissanti (20) [158221](https://abhidhana.buddha-dhamma.net/w/vissajjessanti) vissajjessanti (20) [162215](https://abhidhana.buddha-dhamma.net/w/voropessati) voropessati (20). Options: (a) follow the Pāḷi (future), flag the Burmese; (b) follow the Burmese.
*Recommended: (a)*: the 27 Sep rule (the Pāḷi ending decides) extends to tense.
**Decision:**

**A9. The Burmese pronoun against the Pāḷi ending, passives glossed as actives, negatives** — flags naming a pronoun **24**,
a passive **141**, a negation **115**, -ssu **7**. Examples: pronoun [170811](https://abhidhana.buddha-dhamma.net/w/saddahi) saddahi (21) [170829](https://abhidhana.buddha-dhamma.net/w/saddaheyya) saddaheyya (21) [164276](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81sari%E1%B9%81) saṁsariṁ (21) [220333](https://abhidhana.buddha-dhamma.net/w/hiss%C4%81mi) hissāmi (25); passive [220177](https://abhidhana.buddha-dhamma.net/w/hiyyati) hiyyati (25) [220489](https://abhidhana.buddha-dhamma.net/w/h%C4%AByare) hīyare (25)
[141320](https://abhidhana.buddha-dhamma.net/w/li%E1%B9%85g%C4%AByati) liṅgīyati (18); negative [220556](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%ADhayeyyu%E1%B9%81) heṭhayeyyuṁ (25); -ssu [191505](https://abhidhana.buddha-dhamma.net/w/sikkhassu) sikkhassu (23) [146891](https://abhidhana.buddha-dhamma.net/w/vasassu) vasassu (18). Options: (a) the Pāḷi form decides person, voice and polarity, the
disagreement flagged; (b) the Burmese decides. *Recommended: (a)*, as A8.
**Decision:**

---

## B. Stems and renderings

### B1. How to apply the revision queue's rules (decided 27 Sep; `revision-queue.tsv`, 3,382 rows)

The rules are settled; what is open is how each is applied in step 2.3.

| rule | rows | books with most | examples | options | recommended |
|---|---:|---|---|---|---|
| R2 person | 1,684 | 12 231, 13 211, 06 180, 14/2 154 | [5570](https://abhidhana.buddha-dhamma.net/w/atthi) atthi (1) [95806](https://abhidhana.buddha-dhamma.net/w/nip%C4%81tess%C4%81mi) nipātessāmi (12) [217050](https://abhidhana.buddha-dhamma.net/w/palobhehi) palobhehi (14/2) | agents (per-row prompt) / script | **agents**, after A1–A9 (the person needs the sense) |
| R3 ပယ် | 565 | 13 97, 19 79, 03 60 | [1353](https://abhidhana.buddha-dhamma.net/w/aggahitada%E1%B9%87%E1%B8%8Da) aggahitadaṇḍa (1) [106483](https://abhidhana.buddha-dhamma.net/w/pa%E1%B9%ADikkhip%C4%81pesi) paṭikkhipāpesi (13) [216838](https://abhidhana.buddha-dhamma.net/w/palikhananakha%E1%B9%87itti) palikhananakhaṇitti (14/2) | agents / editor | **agents** (by sense, L103); the other 2,477 rows with ပယ် not in the queue are left |
| R4 -attha | 182 | 08 28, 13 26 | [650](https://abhidhana.buddha-dhamma.net/w/akkamanattha) akkamanattha (1) [100308](https://abhidhana.buddha-dhamma.net/w/n%C4%ABhara%E1%B9%87attha) nīharaṇattha (12) [217017](https://abhidhana.buddha-dhamma.net/w/palobhanattha) palobhanattha (14/2) | script / agents | **script** (lexical), diff for the editor |
| R5 ပရိသတ် | 24 | 15 4, 03 4 | [2788](https://abhidhana.buddha-dhamma.net/w/ajjhatta) ajjhatta (1) [86951](https://abhidhana.buddha-dhamma.net/w/desakaparis%C4%81padesa) desakaparisāpadesa (10) [135073](https://abhidhana.buddha-dhamma.net/w/yuttasevaka) yuttasevaka (17) | script | **script** |
| R6 pariveṇa / parikamma / parikkhāra | 184 | 14/2 124 | [177](https://abhidhana.buddha-dhamma.net/w/akappiyaparikkh%C4%81ra) akappiyaparikkhāra (1) [212107](https://abhidhana.buddha-dhamma.net/w/parikammavisesa) parikammavisesa (14/2) [216251](https://abhidhana.buddha-dhamma.net/w/parihara%E1%B9%87%C4%AByaparikkh%C4%81ra) pariharaṇīyaparikkhāra (14/2) | script | **script** |
| R7 three futures | 9 | 19 6, 18 3 | [140147](https://abhidhana.buddha-dhamma.net/w/lajjissanti) lajjissanti (18) [149267](https://abhidhana.buddha-dhamma.net/w/vikki%E1%B9%87issati) vikkiṇissati (19) [153185](https://abhidhana.buddha-dhamma.net/w/vipaccissanti) vipaccissanti (19) | script / by hand | **by hand** (9 rows) |
| R8 ငရဲ | 58 | 12 16, 09 13 | [42045](https://abhidhana.buddha-dhamma.net/w/ka%E1%B9%87%E1%B9%ADakasimbaliniraya) kaṇṭakasimbaliniraya (5) [97565](https://abhidhana.buddha-dhamma.net/w/niyatamicch%C4%81dassana) niyatamicchādassana (12) [210977](https://abhidhana.buddha-dhamma.net/w/parad%C4%81rakamma) paradārakamma (14/2) | script | **script** |
| R9 ဖောက်ပြန် | 437 | 19 178, 03 65 | [4286](https://abhidhana.buddha-dhamma.net/w/atikkamati) atikkamati (1) [131012](https://abhidhana.buddha-dhamma.net/w/mukhavik%C4%81ra) mukhavikāra (16) [215932](https://abhidhana.buddha-dhamma.net/w/paris%C4%81) parisā (14/2) | agents | **agents** (by sense, L109) |
| R10 maṅgala | 128 | 16 104 | [16886](https://abhidhana.buddha-dhamma.net/w/abhima%E1%B9%85galar%C5%ABpadassana) abhimaṅgalarūpadassana (3) [123680](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galapokkhara%E1%B9%87ip%C4%81k%C4%81ramatthaka) maṅgalapokkharaṇipākāramatthaka (16) [211433](https://abhidhana.buddha-dhamma.net/w/paramama%E1%B9%85gala) paramamaṅgala (14/2) | script (proper names excluded) | **script** |
| R11 ají | 7 | 16 7 | [126568](https://abhidhana.buddha-dhamma.net/w/marica) marica (16) [126571](https://abhidhana.buddha-dhamma.net/w/maricapakka) maricapakka (16) [126640](https://abhidhana.buddha-dhamma.net/w/mar%C4%ABca) marīca (16) | script | **script** |
| R12 လေ | 119 | 19 101 | [17345](https://abhidhana.buddha-dhamma.net/w/abhisanna) abhisanna (3) [147774](https://abhidhana.buddha-dhamma.net/w/v%C4%81tabbh%C4%81hata) vātabbhāhata (19) [148328](https://abhidhana.buddha-dhamma.net/w/v%C4%81yodh%C4%81tu) vāyodhātu (19) | agents | **agents** (element vs weather) |

`tmp/dec0927/mech.py` already writes the script diff for R4–R8, R10, R11 (§51).
**Decision (the method column, or "as recommended"):**

### B2. Renderings the drafts disagree on

For each: rows whose Burmese has the word, and how the current Spanish renders it. *Recommended* is Claude's proposal;
several are house-style calls for IEBH.

| id | word | rows | current Spanish | examples | options | recommended |
|---|---|---:|---|---|---|---|
| B2.1 | soka (စိုးရိမ်) | 243 | pena / pesar / aflicción … 115; ⟦soka⟧ 25 (vol. 25 kept it throughout) | [8460](https://abhidhana.buddha-dhamma.net/w/anutappati) anutappati (2) [104006](https://abhidhana.buddha-dhamma.net/w/pacch%C4%81t%C4%81pa) pacchātāpa (13) [219630](https://abhidhana.buddha-dhamma.net/w/h%C4%81) hā (25) | *pesar*; *pena*; *aflicción*; keep ⟦soka⟧ | ***pesar*** (one word; *aflicción* is free for domanassa). Low confidence |
| B2.2 | sāsana (သာသနာ) | 496 | ⟦sāsana⟧ 313; *Enseñanza / doctrina* 77 | [9396](https://abhidhana.buddha-dhamma.net/w/anur%C4%81dha) anurādha (2) [165100](https://abhidhana.buddha-dhamma.net/w/sakalanava%E1%B9%85gasatthus%C4%81sana) sakalanavaṅgasatthusāsana (21) [221034](https://abhidhana.buddha-dhamma.net/w/hemakatthera) hemakatthera (25) | keep; *la Enseñanza*; by sense | **keep ⟦sāsana⟧** for the dispensation (as Nibbāna); *enseñanza* where it is plain instruction |
| B2.3 | saṁsāra (သံသရာ) | 368 | kept 218; *ciclo* 19 | [9476](https://abhidhana.buddha-dhamma.net/w/anuloma) anuloma (2) [160386](https://abhidhana.buddha-dhamma.net/w/vuttasa%E1%B9%81s%C4%81rava%E1%B9%AD%E1%B9%ADak%C4%81ra%E1%B9%87a) vuttasaṁsāravaṭṭakāraṇa (20) [220594](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%AD%E1%B9%ADh%C4%81gaman%C4%ABya) heṭṭhāgamanīya (25) | keep; *ciclo de renacimientos* | **keep** |
| B2.4 | cakkavāḷa (စကြဝဠာ) | 132 | kept 122; *sistema de mundos* 12 | [10694](https://abhidhana.buddha-dhamma.net/w/antocakkav%C4%81l%CC%A4a) antocakkavāl̤a (2) [82214](https://abhidhana.buddha-dhamma.net/w/dasasahassacakkav%C4%81l%CC%A4a) dasasahassacakkavāl̤a (10) [220136](https://abhidhana.buddha-dhamma.net/w/himavantacakkav%C4%81l%CC%A4apabbata) himavantacakkavāl̤apabbata (25) | keep; *sistema de mundos* | **keep** (cosmological term) |
| B2.5 | sikkhāpada (သိက္ခာပုဒ်) | 693 | kept 655; *regla de entrenamiento* 32; *precepto* 8 | [8555](https://abhidhana.buddha-dhamma.net/w/anuddesasikkh%C4%81pada) anuddesasikkhāpada (2) [122628](https://abhidhana.buddha-dhamma.net/w/bhojanavagga) bhojanavagga (15) [220688](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%AD%E1%B9%ADh%C4%81sikkh%C4%81pada) heṭṭhāsikkhāpada (25) | keep; *regla de entrenamiento*; *precepto* | ***regla de entrenamiento*** everywhere (vol. 23 shard 08's choice); *precepto* only in pañcasīla. Medium confidence |
| B2.6 | ပြာသာဒ် pāsāda | 263 | *palacio* 242; kept 17 | [10766](https://abhidhana.buddha-dhamma.net/w/antop%C4%81s%C4%81da) antopāsāda (2) [146346](https://abhidhana.buddha-dhamma.net/w/varap%C4%81s%C4%81da) varapāsāda (18) [221063](https://abhidhana.buddha-dhamma.net/w/hemap%C4%81s%C4%81dala%E1%B9%85kata) hemapāsādalaṅkata (25) | *palacio*; keep | ***palacio***; names (Lohapāsāda) kept |
| B2.7 | ကမ္ဘာ | 348 | *eón* 305; *mundo* 48; ⟦kappa⟧ 77 | [10037](https://abhidhana.buddha-dhamma.net/w/anekakappa) anekakappa (2) [117131](https://abhidhana.buddha-dhamma.net/w/buddhupp%C4%81dakappa) buddhuppādakappa (15) [218200](https://abhidhana.buddha-dhamma.net/w/sol%CC%A4as%C4%81sa%E1%B9%85khyeyya) sol̤asāsaṅkhyeyya (25); [196223](https://abhidhana.buddha-dhamma.net/w/p%C4%81dap%C4%81vara) pādapāvara (14/3) | by sense | **by sense**: *eón* for time, *mundo* for the world; never ⟦kappa⟧ for ကမ္ဘာ |
| B2.8 | ကံ as act / object | 306 (flags 264) | ⟦kamma⟧ 278; *acto* 34; *objeto* 19 | [9025](https://abhidhana.buddha-dhamma.net/w/anupokha) anupokha (2) [97554](https://abhidhana.buddha-dhamma.net/w/niyataphalak%C4%81la) niyataphalakāla (12) [220071](https://abhidhana.buddha-dhamma.net/w/hit%C4%81hit%C4%81s%C4%AB) hitāhitāsī (25); [246](https://abhidhana.buddha-dhamma.net/w/akammaka) akammaka (1) [88727](https://abhidhana.buddha-dhamma.net/w/dhammakammika) dhammakammika (11) | by sense | **by sense**: moral ⟦kamma⟧; the Saṅgha's *acto formal*; grammar *objeto* |
| B2.9 | ကြိယာ | 328 (flags 162) | kept 129; *acción* 34; *verbo* 21 | [8544](https://abhidhana.buddha-dhamma.net/w/anudd%C4%81k%C4%81ra) anuddākāra (2) [82316](https://abhidhana.buddha-dhamma.net/w/dassanakriy%C4%81) dassanakriyā (10) [221105](https://abhidhana.buddha-dhamma.net/w/hel%C4%81) helā (25) | by sense | **by sense**: grammar *verbo*; Abhidhamma kiriyā ⟦kiriyā⟧ (functional); otherwise *acción* |
| B2.10 | ဘုံ | 1,089 | ⟦bhūmi⟧ 818; *plano* 129; *mundo* 74; *piso / nivel* 63 | [10123](https://abhidhana.buddha-dhamma.net/w/anekabh%C5%ABmika) anekabhūmika (2) [109039](https://abhidhana.buddha-dhamma.net/w/pa%E1%B9%ADivedhabh%C5%ABmi) paṭivedhabhūmi (14/1) [220649](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%AD%E1%B9%ADh%C4%81bh%C5%ABmi) heṭṭhābhūmi (25) | keep; *plano*; by sense | **by sense**: *plano (de existencia)* in cosmology, *piso* of a building, ⟦bhūmi⟧ for the level of consciousness. Medium confidence |
| B2.11 | ဥတု | 258 | ⟦utu⟧ 125; *estación* 111; *menstruación* 27 | [8479](https://abhidhana.buddha-dhamma.net/w/anutuja) anutuja (2) [104257](https://abhidhana.buddha-dhamma.net/w/pacchimavassa) pacchimavassa (13) [221062](https://abhidhana.buddha-dhamma.net/w/hemantogadha) hemantogadha (25) | L104 + menses | **L104 as is, plus *menstruación*** where the Burmese means the menses (utunī) |
| B2.12 | ဟင်္သာ (haṁsa) | 59 | *cisne* 28; *ganso* 10; kept 8; ‹ › 1 | [8629](https://abhidhana.buddha-dhamma.net/w/anupakkhandaha%E1%B9%81sapotaka) anupakkhandahaṁsapotaka (2) [84233](https://abhidhana.buddha-dhamma.net/w/dibbiya) dibbiya (10) [215638](https://abhidhana.buddha-dhamma.net/w/pariv%C4%81raha%E1%B9%81sa) parivārahaṁsa (14/2) | *cisne*; *ganso*; keep ⟦haṁsa⟧ | **keep ⟦haṁsa⟧** (the bird is disputed: goose, swan, the Burmese shelduck). Low confidence |
| B2.13 | စောင်း for vīṇā | 439* | *arpa* 105; *laúd* 1; ⟦vīṇā⟧ 5 | [8372](https://abhidhana.buddha-dhamma.net/w/anucc%C4%81ritakata) anuccāritakata (2) [124278](https://abhidhana.buddha-dhamma.net/w/ma%C3%B1cap%C4%AB%E1%B9%ADharahita) mañcapīṭharahita (16) [220659](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%AD%E1%B9%ADh%C4%81ma%C3%B1ca) heṭṭhāmañca (25) | *laúd*; *arpa*; keep ⟦vīṇā⟧ | **keep ⟦vīṇā⟧** (the Pāḷi instrument is a lute, the Burmese saung a harp; *arpa* is wrong for the Pāḷi). *စောင်း also means "lean, side": the count over-counts |
| B2.14 | ဝါဒ | 1,129 | *doctrina / teoría* 551; kept 318 | [9003](https://abhidhana.buddha-dhamma.net/w/anupubbase%E1%B9%AD%E1%B9%ADhiputta) anupubbaseṭṭhiputta (2) [148019](https://abhidhana.buddha-dhamma.net/w/v%C4%81dimaddana) vādimaddana (19) [221111](https://abhidhana.buddha-dhamma.net/w/hevatthikav%C4%81da) hevatthikavāda (25) | *doctrina*; keep | ***doctrina***; kept inside school names (Theravāda) |
| B2.15 | သစ္စာ | 810 | kept 312; *verdad* 192; *voto* 9 | [8719](https://abhidhana.buddha-dhamma.net/w/anupanenta) anupanenta (2) [115779](https://abhidhana.buddha-dhamma.net/w/bahusaccaka) bahusaccaka (15) [220983](https://abhidhana.buddha-dhamma.net/w/hetusu%C3%B1%C3%B1a) hetusuñña (25) | keep; by sense | **by sense**: *verdad* (*las cuatro nobles verdades*), *veracidad*, *acto de verdad* (saccakiriyā), *voto* |
| B2.16 | သဒ္ဒါ | 2,833 | *palabra* 2,513; *gramática* 73; *sonido* 69 | [8197](https://abhidhana.buddha-dhamma.net/w/anukara%E1%B9%87asadda) anukaraṇasadda (2) [138272](https://abhidhana.buddha-dhamma.net/w/rukkhasadda) rukkhasadda (17) [221148](https://abhidhana.buddha-dhamma.net/w/l%CC%A4a) l̤a (25) | by sense | **by sense**: *palabra* by default, *gramática*, *sonido* |
| B2.17 | ခေတ် | 129 | ⟦khetta⟧ 60; *época* 29; *campo* 19 | [12789](https://abhidhana.buddha-dhamma.net/w/ap%C4%81cittiyakhetta) apācittiyakhetta (2) [69545](https://abhidhana.buddha-dhamma.net/w/j%C4%81tikkhetta) jātikkhetta (8) [216377](https://abhidhana.buddha-dhamma.net/w/parih%C4%81rakhetta) parihārakhetta (14/2) | by sense | **by sense**: khetta *campo* (buddhakkhetta *campo de un Buddha*); Burmese ခေတ် *época* |
| B2.18 | ရှုတ်ချ / ကဲ့ရဲ့ | 784 | *censurar* 707; *reprochar* 142; *denigrar* 50 | [8323](https://abhidhana.buddha-dhamma.net/w/anuggahagarahavacana) anuggahagarahavacana (2) [70266](https://abhidhana.buddha-dhamma.net/w/jigucch%C4%81vaha) jigucchāvaha (8) [220510](https://abhidhana.buddha-dhamma.net/w/h%C4%ABl%CC%A4emi) hīl̤emi (25) | one word; two | **two**: ကဲ့ရဲ့ *censurar*, ရှုတ်ချ *denigrar* |
| B2.19 | စောဒနာ | 213 | *acusar* 133; *reprender* 68 | [8558](https://abhidhana.buddha-dhamma.net/w/anuddha%E1%B9%81sana) anuddhaṁsana (2) [66227](https://abhidhana.buddha-dhamma.net/w/ced%C4%81peyya) cedāpeyya (7) [215846](https://abhidhana.buddha-dhamma.net/w/parisa%E1%B9%85kitacodan%C4%81) parisaṅkitacodanā (14/2) | by context | **by context**: Vinaya codanā *acusación / acusar*; admonition *reprender* |
| B2.20 | ဘီလူး | 359 | ⟦yakkha⟧ 267; *ogro* 61 | [10003](https://abhidhana.buddha-dhamma.net/w/an%C5%ABnan%C4%81ma) anūnanāma (2) [133138](https://abhidhana.buddha-dhamma.net/w/yakkhak%C4%81ka) yakkhakāka (17) [221075](https://abhidhana.buddha-dhamma.net/w/hemavata) hemavata (25) | keep; *ogro* | **keep ⟦yakkha⟧** (as deva, L101) |
| B2.21 | နတ်သား / နတ်သမီး | 380 | ⟦deva⟧ 234; *hijo / hija* 27; *diosa / ninfa* 9 | [9414](https://abhidhana.buddha-dhamma.net/w/anuruddhasutta) anuruddhasutta (2) [105244](https://abhidhana.buddha-dhamma.net/w/pa%C3%B1casikha) pañcasikha (13) [220271](https://abhidhana.buddha-dhamma.net/w/hir%C4%AB) hirī (25) | ⟦deva⟧ / ⟦devī⟧; *deva* / *deva femenina* | **⟦deva⟧ / ⟦devī⟧** |
| B2.22 | ထာဝရဘုရား | 3 | *Dios* 2 | [78050](https://abhidhana.buddha-dhamma.net/w/titth%C4%81yatanasutta) titthāyatanasutta (9) [167675](https://abhidhana.buddha-dhamma.net/w/sajitu) sajitu (21) [167734](https://abhidhana.buddha-dhamma.net/w/sajjitu) sajjitu (21) | accept | **accept** *Dios* (the theists' creator) |
| B2.23 | ဆွမ်း | 825 | *comida de limosna* 538 | [8731](https://abhidhana.buddha-dhamma.net/w/anupama) anupama (2) [121072](https://abhidhana.buddha-dhamma.net/w/bhikkh%C4%81c%C4%81ravel%C4%81) bhikkhācāravelā (15) [220689](https://abhidhana.buddha-dhamma.net/w/he%E1%B9%AD%E1%B9%ADh%C4%81sittha) heṭṭhāsittha (25) | confirm | **confirm** *comida de limosna* |
| B2.24 | ပူဇော် | 1,105 | *venerar* 505; *ofrecer* 237; *honrar* 186 | [8209](https://abhidhana.buddha-dhamma.net/w/anukulaya%C3%B1%C3%B1a) anukulayañña (2) [127613](https://abhidhana.buddha-dhamma.net/w/mah%C4%81th%C5%ABpamaha) mahāthūpamaha (16) [221139](https://abhidhana.buddha-dhamma.net/w/homakara%E1%B9%87a) homakaraṇa (25) | by object | **by object**: things *ofrecer (en veneración)*, persons *venerar / rendir homenaje* |
| B2.25 | ကြည်ညို | 381 | *devoción* 239; *fe / confianza* 70 | [9933](https://abhidhana.buddha-dhamma.net/w/anussavappasanna) anussavappasanna (2) [172584](https://abhidhana.buddha-dhamma.net/w/ekaggat%C4%81) ekaggatā (4/3) [214176](https://abhidhana.buddha-dhamma.net/w/pariplavapas%C4%81da) pariplavapasāda (14/2) | *devoción*; *confianza* | ***devoción***; pasāda's own rendering is a glossary item (C3) |
| B2.26 | ပါဠိ | 1,501 | *texto* 628; ⟦pāḷi⟧ 435 | [8572](https://abhidhana.buddha-dhamma.net/w/anudhamma) anudhamma (2) [166757](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%85kh%C4%81rupekkh%C4%81%C3%B1%C4%81%E1%B9%87aniddesa) saṅkhārupekkhāñāṇaniddesa (21) [220896](https://abhidhana.buddha-dhamma.net/w/hetuphalapa%E1%B9%ADip%C4%81%E1%B9%ADi) hetuphalapaṭipāṭi (25) | by sense | **by sense**: ⟦pāḷi⟧ the canonical text, *texto* a passage |
| B2.27 | ဦးချို | 63 | *cuerno* 60; *copete* 2 | [31149](https://abhidhana.buddha-dhamma.net/w/%C4%81vellitasi%E1%B9%85gika) āvellitasiṅgika (4/1) [134947](https://abhidhana.buddha-dhamma.net/w/yujjh%C4%81peti) yujjhāpeti (17) [196285](https://abhidhana.buddha-dhamma.net/w/p%C4%81davis%C4%81%E1%B9%87a) pādavisāṇa (14/3); [191722](https://abhidhana.buddha-dhamma.net/w/sikhara) sikhara (23) [191731](https://abhidhana.buddha-dhamma.net/w/sikh%C4%81) sikhā (23) | *cuerno* | ***cuerno***; fix the two *copete* |
| B2.28 | သမုတ် | 303 | *designar* 158; *convención* 58; *autorizar* 25 | [9959](https://abhidhana.buddha-dhamma.net/w/anuss%C4%81van%C4%81naya) anussāvanānaya (2) [139189](https://abhidhana.buddha-dhamma.net/w/r%C5%ABpiyacha%E1%B8%8D%E1%B8%8Dakasammata) rūpiyachaḍḍakasammata (17) [221028](https://abhidhana.buddha-dhamma.net/w/hetusammata) hetusammata (25) | by sense | **by sense**: sammuti *convención*; Vinaya sammata *designado / autorizado* |
| B2.29 | သရုပ် sarūpa | 94 | translated 59; kept 23 | [8694](https://abhidhana.buddha-dhamma.net/w/anupadadhammavipassan%C4%81) anupadadhammavipassanā (2) [138674](https://abhidhana.buddha-dhamma.net/w/r%C5%ABpadassanapaccaya) rūpadassanapaccaya (17) [219736](https://abhidhana.buddha-dhamma.net/w/h%C4%81rasar%C5%ABpamattadassanatta) hārasarūpamattadassanatta (25) | translate | ***naturaleza propia*** |
| B2.30 | သရဏဂုံ | 60 | kept 57 | [8577](https://abhidhana.buddha-dhamma.net/w/anudhammappa%E1%B9%ADipatti) anudhammappaṭipatti (2) [186704](https://abhidhana.buddha-dhamma.net/w/sara%E1%B9%87agamanapasiddhi) saraṇagamanapasiddhi (23) [213545](https://abhidhana.buddha-dhamma.net/w/parini%E1%B9%AD%E1%B9%ADhitasara%E1%B9%87agamana) pariniṭṭhitasaraṇagamana (14/2) | translate | ***toma de refugio*** |
| B2.31 | အသပြာ kahāpaṇa | 144 | kept 83; *moneda* 62 | [10666](https://abhidhana.buddha-dhamma.net/w/antoko%E1%B9%ADisanth%C4%81ra) antokoṭisanthāra (2) [93290](https://abhidhana.buddha-dhamma.net/w/n%C4%81vutiya) nāvutiya (11) [221100](https://abhidhana.buddha-dhamma.net/w/hera%C3%B1%C3%B1ikakah%C4%81pa%E1%B9%87adassanasadisa) heraññikakahāpaṇadassanasadisa (25) | keep | **keep ⟦kahāpaṇa⟧** (a coin; as kyat) |
| B2.32 | မြင့်မိုရ် meru | 50 | *Meru* 48 | [10850](https://abhidhana.buddha-dhamma.net/w/antosineru) antosineru (2) [192134](https://abhidhana.buddha-dhamma.net/w/sinerupabbatamuddha) sinerupabbatamuddha (23) [208970](https://abhidhana.buddha-dhamma.net/w/suva%E1%B9%87%E1%B9%87amah%C4%81meru) suvaṇṇamahāmeru (24) | keep | **keep** (a name) |
| B2.33 | "Véase el original" | 1,371 | the drafts' wording (vols. 17 306, 10 240); which Burmese it renders was not checked | [2711](https://abhidhana.buddha-dhamma.net/w/aj%C4%ABva) ajīva (1) [84485](https://abhidhana.buddha-dhamma.net/w/dissati) dissati (10) [155872](https://abhidhana.buddha-dhamma.net/w/virodhidosa) virodhidosa (19) | keep; drop; link the citation | **read three rows' Burmese first**, then fix it as a formula (F029) |

**Decision (a column of letters or "as recommended", with exceptions):**

### B3. Choices single agents made, for approval as a batch

Rows = Burmese has the word; *drafts* = rows whose Spanish has the agent's choice. *Recommended*: approve unless marked.

| word | agent's choice | rows / drafts | examples | recommended |
|---|---|---|---|---|
| ဂုဏ်ကျေးဇူး | *virtudes* | 351 / 245 | [9820](https://abhidhana.buddha-dhamma.net/w/anus%C4%81sanigu%E1%B9%87%C4%81bhirata) anusāsaniguṇābhirata (2) [116794](https://abhidhana.buddha-dhamma.net/w/buddhadhamma) buddhadhamma (15) | approve |
| ပူပန် | *angustia* | 624 / 224 | [8459](https://abhidhana.buddha-dhamma.net/w/anutappa) anutappa (2) [104017](https://abhidhana.buddha-dhamma.net/w/pacch%C4%81nut%C4%81pacariya) pacchānutāpacariya (13) | approve |
| ငြိမ်းအေး | *aquietamiento* | 736 / 8 | [8565](https://abhidhana.buddha-dhamma.net/w/anuddha%E1%B9%ADa) anuddhaṭa (2) [216480](https://abhidhana.buddha-dhamma.net/w/paril%CC%A4%C4%81h%C5%ABpasama) paril̤āhūpasama (14/2) | *serenidad*, *apaciguamiento* (Claude; low confidence) |
| ကောင်းစွာ (sam-) | *completamente* | 3,639 / 84 | [8522](https://abhidhana.buddha-dhamma.net/w/anudassita) anudassita (2) [182377](https://abhidhana.buddha-dhamma.net/w/sam%C4%81lapati) samālapati (22) | *bien / debidamente* by default; *completamente* only for sam- intensive |
| ကျမ်းတက် | *nexo textual* | 1 / 1 | [185002](https://abhidhana.buddha-dhamma.net/w/sambandha) sambandha (22) | approve |
| ဒြဗ် | *cosa* | 62 / 19 | [17771](https://abhidhana.buddha-dhamma.net/w/abh%C5%ABta) abhūta (3) [81780](https://abhidhana.buddha-dhamma.net/w/dabya) dabya (10) | *sustancia* (dravya), medium confidence |
| ချမ်းသာ | *felicidad* | 1,267 / 647 | [8181](https://abhidhana.buddha-dhamma.net/w/anukampam%C4%81na) anukampamāna (2) [166103](https://abhidhana.buddha-dhamma.net/w/saggasukha) saggasukha (21) | approve; *placentero* of touch |
| သိမ်မွေ့ | *sutil* | 446 / 173 | [9707](https://abhidhana.buddha-dhamma.net/w/anusadd%C4%81yati) anusaddāyati (2) [168857](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%87hasukhumagu%E1%B9%87a) saṇhasukhumaguṇa (21) | approve |
| အဆောက်အဦ (upakaraṇa) | *equipamiento* | 345 / 18 | [8651](https://abhidhana.buddha-dhamma.net/w/anupacitakusalasambh%C4%81ra) anupacitakusalasambhāra (2) [214537](https://abhidhana.buddha-dhamma.net/w/paribhutt%C5%ABpakara%E1%B9%87a) paribhuttūpakaraṇa (14/2) | *enseres / utensilios* |
| သုသာန် | *osario* | 85 / 41 | [8385](https://abhidhana.buddha-dhamma.net/w/anucchi%E1%B9%AD%E1%B9%ADhasus%C4%81na) anucchiṭṭhasusāna (2) [203189](https://abhidhana.buddha-dhamma.net/w/s%C4%ABtavana) sītavana (24) | *cementerio / lugar de cremación*: osario is a bone store |
| သံဂါယနာ | *saṅgāyanā* | 93 / 48 | [26345](https://abhidhana.buddha-dhamma.net/w/asoka) asoka (3) [167059](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%85g%C4%81yanak%C4%81ra) saṅgāyanakāra (21) | *concilio (⟦saṅgāyanā⟧)* |
| robes: ဒုကုဋ် / သင်းပိုင် / ကိုယ်ရုံ | *hábito doble / inferior / superior* | 34 / 30; 61 / 45; 30 / 2 | [65215](https://abhidhana.buddha-dhamma.net/w/c%C4%ABvaraniyama) cīvaraniyama (7) [98993](https://abhidhana.buddha-dhamma.net/w/niv%C4%81sanavatta) nivāsanavatta (12) [90205](https://abhidhana.buddha-dhamma.net/w/dh%C4%81resi) dhāresi (11) | approve (saṅghāṭi, antaravāsaka, uttarāsaṅga) |
| သီတင်းတစ်ပတ် | *semana de observancia* | 2 / 2 | [170023](https://abhidhana.buddha-dhamma.net/w/satt%C4%81ha) sattāha (21) [170024](https://abhidhana.buddha-dhamma.net/w/satt%C4%81hakara%E1%B9%87%C4%ABya) sattāhakaraṇīya (21) | *semana* (sattāha) |
| သူတော်ကောင်းတရား | *la Enseñanza de los buenos* | 95 / 48 | [9858](https://abhidhana.buddha-dhamma.net/w/anusi%E1%B9%AD%E1%B9%ADhipada) anusiṭṭhipada (2) [170908](https://abhidhana.buddha-dhamma.net/w/saddhammacakk%C4%81nupavattaka) saddhammacakkānupavattaka (21) | approve (saddhamma) |
| သပြေ | *jambolán* | 72 / 57 | [18762](https://abhidhana.buddha-dhamma.net/w/ambajamb%C4%81dipa%E1%B9%87%E1%B9%87a) ambajambādipaṇṇa (3) [68640](https://abhidhana.buddha-dhamma.net/w/jambusadisa) jambusadisa (8) | approve (jambu, Syzygium cumini) |
| ပဟိုရ် | *vigilia* | 12 / 8 | [60146](https://abhidhana.buddha-dhamma.net/w/gha%E1%B9%87%E1%B9%ADika) ghaṇṭika (6) [195232](https://abhidhana.buddha-dhamma.net/w/pah%C4%81rasa%C3%B1%C3%B1ita) pahārasaññita (14/3) | approve |
| ဝိဘတ် / ပုထုဇဉ် | ⟦vibhatti⟧ / ⟦puthujjana⟧ | 233 / 152; 106 / 105 | [15378](https://abhidhana.buddha-dhamma.net/w/abyaya) abyaya (3) [200252](https://abhidhana.buddha-dhamma.net/w/puthujjanakaly%C4%81%E1%B9%87aka) puthujjanakalyāṇaka (14/3) | ⟦vibhatti⟧ approve; puthujjana *persona común* is possible: glossary (C3) |
| ကောင်းမှုကုသိုလ် | *buena acción meritoria* | 94 / 81 | [32074](https://abhidhana.buddha-dhamma.net/w/itthid%C4%81na) itthidāna (4/1) [199798](https://abhidhana.buddha-dhamma.net/w/pu%C3%B1%C3%B1appabh%C4%81v%C4%81nuggahitasar%C4%ABra) puññappabhāvānuggahitasarīra (14/3) | approve |
| ပုဂ္ဂိုလ် | *persona* | 1,563 / 1,448 | [8379](https://abhidhana.buddha-dhamma.net/w/anucchavikapuggala) anucchavikapuggala (2) [119347](https://abhidhana.buddha-dhamma.net/w/bhabbapuggalapariggaha) bhabbapuggalapariggaha (15) | approve |
| ပုစ္ဆာ | kept ⟦ပုစ္ဆာ⟧ | 448 / 119 | [8296](https://abhidhana.buddha-dhamma.net/w/anug%C4%ABti) anugīti (2) [115873](https://abhidhana.buddha-dhamma.net/w/b%C4%81tti%E1%B9%81sasatapa%C3%B1ha) bāttiṁsasatapañha (15) | *pregunta* |
| သုံးသပ် (āmasana) | *tocar* | 619 / 102 | [8321](https://abhidhana.buddha-dhamma.net/w/anuggaha) anuggaha (2) [150195](https://abhidhana.buddha-dhamma.net/w/vicin%C4%AB) vicinī (19) | by sense: *examinar* (reflect) / *tocar* (touch) |
| ဆုတ်နစ် | *hundirse* | 488 / 48 | [10257](https://abhidhana.buddha-dhamma.net/w/ano%E1%B9%87amana) anoṇamana (2) [220473](https://abhidhana.buddha-dhamma.net/w/h%C4%ABn%C4%81y%C4%81vattanti) hīnāyāvattanti (25) | *retroceder / decaer* where of effort; medium confidence |
| သဗ္ဗညု | kept | 298 / 269 | [8572](https://abhidhana.buddha-dhamma.net/w/anudhamma) anudhamma (2) [178692](https://abhidhana.buddha-dhamma.net/w/sabba%C3%B1%C3%B1uta%C3%B1%C4%81%E1%B9%87ak%C4%81ra%E1%B9%87a) sabbaññutañāṇakāraṇa (22) | approve (sabbaññū, *omnisciente* in the adjective) |
| ရဟန်းတရား | ⟦=dhamma⟧ | 40 / 20 | [29859](https://abhidhana.buddha-dhamma.net/w/%C4%81rakkhavipatti) ārakkhavipatti (4/1) [180350](https://abhidhana.buddha-dhamma.net/w/sama%E1%B9%87adhammakara%E1%B9%87ak%C4%81la) samaṇadhammakaraṇakāla (22) | *la práctica del asceta (samaṇadhamma)* |
| ပယ်နုတ်-ပယ်ဖျက်… | *erradicar / eliminar / extirpar / abandonar* | 83 / 25 | [10902](https://abhidhana.buddha-dhamma.net/w/andhak%C4%81ratamonuda) andhakāratamonuda (2) [133001](https://abhidhana.buddha-dhamma.net/w/mohapa%E1%B9%ADalasamupp%C4%81%E1%B9%ADana) mohapaṭalasamuppāṭana (16) | approve (hyphens kept apart, F007) |
| အကြွင်းမဲ့ | *sin residuo* | 348 / 272 | [9779](https://abhidhana.buddha-dhamma.net/w/anusayasamuggh%C4%81ta) anusayasamugghāta (2) [149519](https://abhidhana.buddha-dhamma.net/w/vigatakatha%E1%B9%81katha) vigatakathaṁkatha (19) | approve |
| ဆုတ်ယုတ် / ယုတ်လျော့ | *decaer* / *menguar* | 392 / 223; 389 / 92 | [8373](https://abhidhana.buddha-dhamma.net/w/anucc%C4%81vaca) anuccāvaca (2) [9993](https://abhidhana.buddha-dhamma.net/w/an%C5%ABna) anūna (2) | approve |
| အစီးအပွား | *provecho* | 117 / 102 | [162429](https://abhidhana.buddha-dhamma.net/w/sa) sa (20) [219942](https://abhidhana.buddha-dhamma.net/w/hitajjh%C4%81sayappavattita) hitajjhāsayappavattita (25) | approve |
| သဘောလက္ခဏာ | ⟦lakkhaṇa⟧ variants | 69 / 6 | [24309](https://abhidhana.buddha-dhamma.net/w/asa%E1%B9%81g%C4%81han%C4%81) asaṁgāhanā (3) [139861](https://abhidhana.buddha-dhamma.net/w/lakkha%E1%B9%87%C5%ABpanijjh%C4%81na) lakkhaṇūpanijjhāna (18) | *característica intrínseca* |
| သူငယ်ချင်း | *amigo* / *camarada* | 61 / 52 | [11529](https://abhidhana.buddha-dhamma.net/w/apatir%C5%ABpasah%C4%81ya) apatirūpasahāya (2) [185507](https://abhidhana.buddha-dhamma.net/w/samma) samma (23) | *amigo* |

**Decision:**

### B4. Names, measures, dates

**B4.1 Burmese left in ‹ ›** (plant, animal, tool, measure names the agents would not guess) — **3,804 rows** (05 375, 16 364,
06 353, 09 269). Examples: [4154](https://abhidhana.buddha-dhamma.net/w/a%E1%B9%87%E1%B8%8Davu%E1%B8%8D%E1%B8%8Dhiroga) aṇḍavuḍḍhiroga (1) [123388](https://abhidhana.buddha-dhamma.net/w/maggar%C5%ABp%C4%AB) maggarūpī (16) [221099](https://abhidhana.buddha-dhamma.net/w/hera%C3%B1%C3%B1ika) heraññika (25). **Tentative identifications in flags** (a species or a Latin name, with
"probably" / "?"): **1,264 rows**. Examples: [1030](https://abhidhana.buddha-dhamma.net/w/agada%E1%B9%85g%C4%81ra) agadaṅgāra (1) [114275](https://abhidhana.buddha-dhamma.net/w/phussavel%CC%A4uvala%E1%B9%AD%E1%B9%ADhi) phussavel̤uvalaṭṭhi (15) [220774](https://abhidhana.buddha-dhamma.net/w/hetugocchaka) hetugocchaka (25).
Options: (a) ‹Burmese› plus a tentative name in a note; (b) a name only when sure, else ‹Burmese›; (c) the Pāḷi name kept
(⟦pāṭali⟧) with the Burmese in a note. *Recommended: (c) where the headword gives the Pāḷi, else (a)*; the botanical names
need a reference (not checked here), so none goes into the text on an agent's guess.
**Decision:**

**B4.2 Burmese months** — **443 rows** mention one (22 66, 23 47, 18 44); romanised in 161, in ‹ › in 27, the rest rendered
otherwise (Pāḷi month, season). Examples: [8537](https://abhidhana.buddha-dhamma.net/w/anudeva) anudeva (2) [147256](https://abhidhana.buddha-dhamma.net/w/vass%C4%81v%C4%81sika%E1%B9%AD%E1%B9%ADhitik%C4%81) vassāvāsikaṭṭhitikā (18) [221052](https://abhidhana.buddha-dhamma.net/w/hemanta) hemanta (25).
Options: (a) romanised (Kason); (b) ‹ ›; (c) the Pāḷi month (Vesākha) with the Burmese romanised in brackets.
*Recommended: (c)*: the Pāḷi month is what the Spanish reader can look up.
**Decision:**

**B4.3 Coins and measures** (kyat, pya, viss, ရွေး, တင်း, ပယ် as land) — **202 rows** (vol. 20 89). Examples: [3595](https://abhidhana.buddha-dhamma.net/w/a%E1%B9%AD%E1%B9%ADhakah%C4%81pa%E1%B9%87a) aṭṭhakahāpaṇa (1) [158163](https://abhidhana.buddha-dhamma.net/w/vissajji) vissajji (20)
[218116](https://abhidhana.buddha-dhamma.net/w/sol%CC%A4asakah%C4%81pa%E1%B9%87aparibbaya) sol̤asakahāpaṇaparibbaya (25). Options: (a) romanised (*kyat*); (b) ‹ ›; (c) romanised + equivalent in a note. *Recommended: (a)*, as the drafts mostly
do; (c) only where the text depends on the amount.
**Decision:**

**B4.4 Place names** — romanised by vol. 20 shard 10 (Bihar, Muzaffarpur, Basarh, Minbu); not counted across books (no reliable
test). *Recommended*: Pāḷi places in Pāḷi (Vesālī), modern places in their usual Spanish or English spelling.
**Decision:**

### B5. R10 maṅgala: the cases a word swap does not settle (added 29 Sep, brief §72–73)

The rule of 27 Sep renders *\*maṅgala\** as *bendición* where it is not a name (R10). Read against the Burmese (brief §72), some of
R10's 127 proposed changes use maṅgala in a way *bendición* may not fit: 9, 29 and 30 rows of the three kinds below, counted in
`tmp/dec0927/diffs/R10.tsv` by pattern (a row can fall under two kinds, so they are not 68 distinct rows). Nothing is changed; the current drafts keep *\*maṅgala\**.

| kind | rows | examples (current draft → the rule's proposal) |
|---|---:|---|
| a ceremony or festival (Burmese မင်္ဂလာပြု / ဆောင် / ပွဲ) | 9 | [123642](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galakiriy%C4%81divasa) maṅgalakiriyādivasa (16): el día en que se realiza *maṅgalā*. → *el día en que se realiza bendición.*; [123635](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galakamyat%C4%81) maṅgalakamyatā (16): el hecho de desear para realizar *maṅgalā*; el desear realizar *maṅgalā*.… |
| an attribute, "auspicious / of state" (*elefante, jardín, espada, caballo … de bendición*) | 29 | [123628](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galaasi) maṅgalaasi (16): espada que tiene *maṅgalā*; espada de *maṅgalā*. → *espada de bendición*; [123630](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galaassanh%C4%81natittha) maṅgalaassanhānatittha (16): lugar de baño del caballo de *maṅgalā*. → *caballo de bendición* |
| a bare *bendición* after a verb, without article | 30 | [123639](https://abhidhana.buddha-dhamma.net/w/ma%E1%B9%85galak%C4%81la) maṅgalakāla (16): el momento en que se realiza *maṅgalā*. → *se realiza bendición*; [83532](https://abhidhana.buddha-dhamma.net/w/di%E1%B9%AD%E1%B9%ADhama%E1%B9%85galika) diṭṭhamaṅgalika (10): (1) que suele decir / considerar que el *rūpārammaṇa* visto es *maṅgalā* (causa de prosper… → *… es bendición* |

Options: (a) *bendición* everywhere, as the rule says; (b) by sense: a ceremony *ceremonia / festividad*, an attribute *auspicioso / de
estado* (or *ceremonial*), *bendición* elsewhere, with the article supplied; (c) keep ⟦maṅgala⟧ in these rows. *No recommendation here*;
Claude's reading of the kinds is by pattern and may misclass a row (low to medium confidence).
**Decision:**

---

## C. Glossary terms

**C1. English for the eleven confirmed entries of `glossary.tsv`** (Spanish confirmed, English open). Rows whose Spanish has the
term: *sano* 1,028, *insano* 728, *requisitos* 404, *asamblea* 371, *infierno* 287, *bendición* 66, *recinto monástico* 23,
*trabajo preparatorio* 19, *pimienta negra* 2; vaṭṭa kept 864, vassa 346.
*Proposed English*: kusala *wholesome*, akusala *unwholesome*, pariveṇa *monastic precinct*, parikamma *preparatory work*,
parikkhāra *requisites*, maṅgala *blessing*, niraya *hell*, marica *black pepper*, parisā *assembly*; vaṭṭa, vassa kept.
**Decision:**

**C2. The stems marked `glossary`** (their Spanish is a glossary decision): L001 တရား dhamma (8,384 rows: *estado* 5,640,
*Enseñanza* 1,459, ⟦dhamma⟧ 490, *fenómeno* 164, *norma* 71), L010 စိတ် citta (6,034: *mente* 4,349, ⟦citta⟧ 284), L099 ဉာဏ်
ñāṇa (3,402: *conocimiento* 2,664, ⟦ñāṇa⟧ 970, *sabiduría* 22), L090 သင်္ကန်း cīvara (989: *hábito* 983), and L008 sabhāva,
L023 nibbāna, L039 အလို, L049 saññā, L053 pāpa, L054 puñña, L059 ārammaṇa, L062 dukkha, L064 rāga, L071 anicca, L075 diṭṭhi,
L084 attabhāva (counts in Appendix A). Examples: [8184](https://abhidhana.buddha-dhamma.net/w/anukampasutta) anukampasutta (2) [102932](https://abhidhana.buddha-dhamma.net/w/paccayadhammadassanapubbaka) paccayadhammadassanapubbaka (13) [221027](https://abhidhana.buddha-dhamma.net/w/hetusambh%C4%81ra) hetusambhāra (25) (တရား); [8177](https://abhidhana.buddha-dhamma.net/w/anukampati) anukampati (2) [102027](https://abhidhana.buddha-dhamma.net/w/pagu%E1%B9%87a) paguṇa (13) (စိတ်); [8155](https://abhidhana.buddha-dhamma.net/w/anuaya) anuaya (2) [100581](https://abhidhana.buddha-dhamma.net/w/neyya) neyya (12) (ဉာဏ်).
*Recommended*: confirm the proposed Spanish of each (dhamma by sense: *estado* / *la Enseñanza* / *fenómeno*; citta *mente*;
ñāṇa *conocimiento*, paññā *sabiduría*), and enter them in `glossary.tsv`.
**Decision:**

**C3. Pāḷi terms kept in the drafts** — 5,716 distinct, 89,888 row-occurrences (the `-terms.tsv` files). The forty commonest:
kilesa 1,971, deva 1,873, thera 1,847, kamma 1,641, paññā 1,454, nibbāna 1,261, jhāna 1,240, sīla 1,213, magga 1,195, taṇhā 1,158,
rūpa 934, khandha 797, paṭisandhi 738, āpatti 728, rāga 708, vipassanā 693, bhūmi 683, lakkhaṇa 661, sikkhāpada 659, saññā 650,
samādhi 616, vaṭṭa 613, phala 568, cetanā 555, arahattaphala 525, vīriya 506, arahant 500, ariyamagga 496, saṅgha 491, dosa 490,
sāsana 488, kāmaguṇa 467, jātaka 461, sati 460, kammaṭṭhāna 454, bhava 448, saddhā 437, saṅkhāra 432, vedanā 431, māna 419.
Options: (a) keep the whole list in Pāḷi until IEBH's glossary exists; (b) decide the forty now, one line each; (c) decide by
stem, as the editor reviews (2.5). *Recommended: (c), starting with the forty*: they carry 35.6% of the occurrences (31,961). A proposal table with one Spanish rendering each is a separate short job if wanted; Claude does not propose
renderings here, per the rule "propose additions; do not improvise" and because no IEBH doctrinal glossary was found.
**Decision:**

---

## D. Labels, the History and the site's wording

**D1. Labels still in draft** (`docs/labels.md` §0; counts are articles carrying the label, all 29 books):

| label | articles | open | examples | recommended |
|---|---:|---|---|---|
| (တိ) adjective | 63,644 | Spanish *adjetivo (los tres géneros)* draft | [17](https://abhidhana.buddha-dhamma.net/w/a%E1%B9%81savantu) aṁsavantu (1) [112796](https://abhidhana.buddha-dhamma.net/w/padh%C4%81nasa%E1%B9%85kh%C4%81rabh%C4%81vita) padhānasaṅkhārabhāvita (14/1) [221133](https://abhidhana.buddha-dhamma.net/w/honta) honta (25) | confirm |
| (ကြိ) verb | 12,380 | Spanish *verbo* draft | [25](https://abhidhana.buddha-dhamma.net/w/aka%E1%B9%81) akaṁ (1) [118059](https://abhidhana.buddha-dhamma.net/w/by%C4%81yati) byāyati (15) [221146](https://abhidhana.buddha-dhamma.net/w/hohisi) hohisi (25) | confirm |
| (ကာ၊ကြိ) causative verb | 3,389 | Spanish draft | [1557](https://abhidhana.buddha-dhamma.net/w/aggh%C4%81peti) agghāpeti (1) [132800](https://abhidhana.buddha-dhamma.net/w/mocehi) mocehi (16) [219824](https://abhidhana.buddha-dhamma.net/w/h%C4%81sess%C4%81ma) hāsessāma (25) | confirm |
| (ဗျ) indeclinable | 1,141 | Spanish draft | [400](https://abhidhana.buddha-dhamma.net/w/aki%C3%B1ci) akiñci (1) [133967](https://abhidhana.buddha-dhamma.net/w/yath%C4%81hi) yathāhi (17) [221124](https://abhidhana.buddha-dhamma.net/w/hehe) hehe (25) | confirm |
| (ကမ္မ၊ကြိ) passive verb | 597 | Pāḷi *kammavācaka-kriyā?*; Spanish draft | [8780](https://abhidhana.buddha-dhamma.net/w/anuparivattiyati) anuparivattiyati (2) [135821](https://abhidhana.buddha-dhamma.net/w/rakkh%C4%AByate) rakkhīyate (17) [219868](https://abhidhana.buddha-dhamma.net/w/hi%E1%B9%81s%C4%AByati) hiṁsīyati (25) | confirm kammavācaka-kriyā (ကံဟောကြိယာ, "verb that states the object") |
| (ကာ၊ကြိ၊ဝိ) causative absolutive | 541 | status provisional; Pāḷi *kārita-kriyāvisesana?* | [17536](https://abhidhana.buddha-dhamma.net/w/abhisi%C3%B1c%C4%81petv%C4%81) abhisiñcāpetvā (3) [137075](https://abhidhana.buddha-dhamma.net/w/rametv%C4%81) rametvā (17) [219817](https://abhidhana.buddha-dhamma.net/w/h%C4%81setv%C4%81) hāsetvā (25) | confirm |
| (ကာ၊ကမ္မ၊ကြိ) causative passive | 52 | Pāḷi *?*; Spanish draft | [68494](https://abhidhana.buddha-dhamma.net/w/jan%C4%AByate) janīyate (8) [150953](https://abhidhana.buddha-dhamma.net/w/vijjh%C4%81piyanti) vijjhāpiyanti (19) [215223](https://abhidhana.buddha-dhamma.net/w/pariyodap%C4%AByati) pariyodapīyati (14/2) | confirm |
| (အ-လိင်) without gender | 15 | provisional | [19012](https://abhidhana.buddha-dhamma.net/w/amhasu) amhasu (3) [26413](https://abhidhana.buddha-dhamma.net/w/asm%C4%81su) asmāsu (3) [132238](https://abhidhana.buddha-dhamma.net/w/me) me (16) | confirm *sin género* |
| (ပုံ-ဗဟု) masc. plural only | 2 | Spanish draft | [1645](https://abhidhana.buddha-dhamma.net/w/a%E1%B9%85ga) aṅga (1) [1862](https://abhidhana.buddha-dhamma.net/w/a%E1%B9%85guttar%C4%81pa) aṅguttarāpa (1) | confirm |

Also in item 3: *sakkata / pākata* (ဗု၊သံ, "Buddhist Sanskrit", vol. 2 p. 14) — **no article carries them as a label** (0): a
note in `abbreviations.md`, not a label. *Recommended*: confirm all nine as they stand. The label disagreements with the
witness (item 8) wait for their image check.
**Decision:**

**D2. The History (item 7c)** — `docs/history.md` is `site: draft`. Open: (1) every romanised name of people and monasteries
and the Spanish names of institutions (34 bold spans in the two languages); (2) vol. 25's completion year, printed 1384 BE for
20 Nov 2023, which falls in 1385: check the image of vol. 25 p. 15; (3) which parts of vol. 4 the Jambudīpa team wrote
(vol. 17, OCR unclear); (4) who compiled vol. 14. Also: whether the Introduction's ch. 4 names should wait too.
Options: (a) publish now with (2)–(4) marked "not established"; (b) wait for the image checks. *Recommended: (a)* after the
editor reads the names; (2) is one page for 2.4.
**Decision:**

**D3. "Budistas" or "Buddhistas"** (logo and footer say Buddhistas; About and README Budistas; item 00c). *Recommended:
Budistas*, the institute's own name (Instituto de Estudios Budistas Hispano) and standard Spanish spelling.
**Decision:** **Buddhistas** (the editor, 1 Oct 2026). Applied in About, README and LICENSE, v0.29.5, brief §96.

---

## E. Grammar notes

**E1. Grammarians' notes inside the definition** (ဒါ-၏ အာ-ကို ဣယ-ပြု, X-ပစ္စည်း, case senses) — **220 flagged rows**; most were
put in `omitted` (brief §55). Examples: [3230](https://abhidhana.buddha-dhamma.net/w/a%C3%B1%C3%B1adatthika) aññadatthika (1) [150341](https://abhidhana.buddha-dhamma.net/w/vija%E1%B9%AD%C4%81pessatha) vijaṭāpessatha (19) [221148](https://abhidhana.buddha-dhamma.net/w/l%CC%A4a) l̤a (25); 14/2 [210324](https://abhidhana.buddha-dhamma.net/w/pam%C4%81davat%C4%81) pamādavatā (14/2).
Options: (a) leave them out of the Meaning (the analysis field carries the derivation); (b) translate them as a note after the
definition; (c) a separate field later. *Recommended: (a) now, (c) later* with the case abbreviations (item 3b).
**Decision:**

**E2. Formula stems marked `review`**: F008 …သော / သူ / သည် (the adjective as a noun: *dicho de una persona; de una cosa*) and
F012 -အပ်သော (past and future passive share the form; the Pāḷi suffix decides). Counts: F008 0 as written (its pattern is a
schema), F012 18,997 rows contain အပ်သော. *Recommended*: approve both as written.
**Decision:**

**E3. The source tag ထောမ and (သျ)** (vol. 5's agents) — flags naming ထောမ: **103**. Examples: [8151](https://abhidhana.buddha-dhamma.net/w/anu) anu (2) [158926](https://abhidhana.buddha-dhamma.net/w/v%C4%ABta%E1%B9%81sa) vītaṁsa (20) [219451](https://abhidhana.buddha-dhamma.net/w/harit%C4%81lamanosil%C4%81) haritālamanosilā (25).
*Recommended*: treat as a source abbreviation for `abbreviations.md` (item 3b), not translated. Low confidence on what ထောမ
abbreviates; not checked.
**Decision:**

**E4. Honorific verbs** (ဘုဉ်းပေး "eat" of monks, etc.) — **86 flagged**. Examples: [12268](https://abhidhana.buddha-dhamma.net/w/aparibhu%C3%B1jitv%C4%81) aparibhuñjitvā (2) [145105](https://abhidhana.buddha-dhamma.net/w/vattu) vattu (18) [214447](https://abhidhana.buddha-dhamma.net/w/paribhu%C3%B1jati) paribhuñjati (14/2). Options: (a) plain
Spanish verb; (b) a respectful Spanish verb (*tomar*); *Recommended: (a)*, with the honorific noted only where the Pāḷi
headword is itself honorific.
**Decision:**

**E5. The tall ā in roman input** (item 00m (a)): Aksharamukha writes ္ပာ where most volumes print ္ပါ; **354 of 221,154
headwords** differ. It matters only for a field typed anew in *Latín*. *Recommended*: keep Aksharamukha's form (no work);
the *se guarda* line shows the Burmese before saving.
**Decision:**

---

## F. Source defects

The dictionary's print or our OCR is at fault; the question is who looks and when.

| id | kind | rows | examples | options | recommended |
|---|---|---:|---|---|---|
| F1 | numbers lost or misread (totals, dates, counts) | 393 flagged | [4210](https://abhidhana.buddha-dhamma.net/w/ati) ati (1) [179519](https://abhidhana.buddha-dhamma.net/w/sabb%C4%81k%C4%81ravar%C5%ABpeta) sabbākāravarūpeta (22) [221148](https://abhidhana.buddha-dhamma.net/w/l%CC%A4a) l̤a (25); [159512](https://abhidhana.buddha-dhamma.net/w/v%C4%ABsativassika) vīsativassika (20) [180718](https://abhidhana.buddha-dhamma.net/w/samadhisattav%C4%ABsatisatasahassamatta) samadhisattavīsatisatasahassamatta (22) [163323](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81yuttanik%C4%81ya) saṁyuttanikāya (20) | (a) image check by Claude (2.4, ~3 k tokens a row); (b) the editor in the page pane; (c) accept, flagged | **(a)**: mechanical |
| F2 | headword and text disagree | 59 (strict test); 1,860 flags name the headword | [512](https://abhidhana.buddha-dhamma.net/w/akusalakammabh%C4%81va) akusalakammabhāva (1) [167023](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%85g%C4%81mappabheda) saṅgāmappabheda (21) [220139](https://abhidhana.buddha-dhamma.net/w/himavantadesabh%C4%81ga) himavantadesabhāga (25); [157122](https://abhidhana.buddha-dhamma.net/w/visamacakkala) visamacakkala (20) [160369](https://abhidhana.buddha-dhamma.net/w/vuttavisa) vuttavisa (20) [203619](https://abhidhana.buddha-dhamma.net/w/s%C4%ABlamada) sīlamada (24) | (a); (b); (c) | **(a)** for the 59; the rest stay flagged |
| F3 | truncated glosses | 1,293 flagged | [682](https://abhidhana.buddha-dhamma.net/w/akkodha) akkodha (1) [178641](https://abhidhana.buddha-dhamma.net/w/sabbajan%C4%81nanda) sabbajanānanda (22) [220788](https://abhidhana.buddha-dhamma.net/w/hetutthav%C4%81caka) hetutthavācaka (25); [203784](https://abhidhana.buddha-dhamma.net/w/s%C4%ABlasam%C4%81dhipa%C3%B1%C3%B1%C4%81vimuttik%C4%81ra%E1%B9%87aj%C4%81nanasamattha) sīlasamādhipaññāvimuttikāraṇajānanasamattha (24)–[203800](https://abhidhana.buddha-dhamma.net/w/s%C4%ABlasam%C4%81dhipa%C3%B1%C3%B1%C4%81s%C4%81ra) sīlasamādhipaññāsāra (24) run | (a); (b); (c) | **(c)**: the start is not on our page text; to (b) when the editor reviews the stem |
| F4 | garbled beyond reading | 1,880 flagged (22 280, 25 275, 4/3 215) | [183](https://abhidhana.buddha-dhamma.net/w/akappiyabhisibimbohana) akappiyabhisibimbohana (1) [177441](https://abhidhana.buddha-dhamma.net/w/sannicita) sannicita (22) [221105](https://abhidhana.buddha-dhamma.net/w/hel%C4%81) helā (25) | (b); (c) | **(c)** now, *borrador* with the page pane; (b) for doctrinal rows |
| F5 | rows the agents asked to check on the page | 44 (strict phrase) | [11548](https://abhidhana.buddha-dhamma.net/w/apatthaddha) apatthaddha (2) [181396](https://abhidhana.buddha-dhamma.net/w/sam%C4%81dapetabba) samādapetabba (22) [218962](https://abhidhana.buddha-dhamma.net/w/hatthip%C4%81la) hatthipāla (25); vol. 23 shard 00's 20 ids (brief §55) | (a); (b) | **(a)** |
| F6 | misromanised or misprinted headwords | 6 | 14/3: pāpatara, pāparāgī, pāpabhikkhamānā, pāpintave, pāvikatara (brief §63); [216840](https://abhidhana.buddha-dhamma.net/w/paligijcyeyya) paligijcyeyya (14/2) | index-errata; image | **image, then `index-errata.md`** |
| F7 | spelling marks after "see X" | 2 | [176231](https://abhidhana.buddha-dhamma.net/w/oramana) oramana (4/3) [193595](https://abhidhana.buddha-dhamma.net/w/pav%C4%81la) pavāla (14/3) | render *(también con ṇ / ḷ)*; drop | ***(también …)*** as a note |
| F8 | "see X" targets with a stray mark (§65) | 14 | 14/3 3, 21 6, 22 1, 23 2, 24 2 | re-merge those rows from their old drafts | **re-merge** (mechanical, no redraft) |
| F9 | the index spells differently from the print | 4 | [212175](https://abhidhana.buddha-dhamma.net/w/parik%C4%ABl%CC%A4in%C4%81) parikīl̤inā (14/2) [210262](https://abhidhana.buddha-dhamma.net/w/pam%C4%81%E1%B9%87avatth%C4%81na) pamāṇavatthāna (14/2) [163326](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81yuttanik%C4%81yavarala%C3%B1jaka) saṁyuttanikāyavaralañjaka (20) [190856](https://abhidhana.buddha-dhamma.net/w/s%C4%81lakiya) sālakiya (23) | `index-errata.md` | **errata** |
| F10 | lost sense numbers / skips | in 1,518 "source" flags | [171365](https://abhidhana.buddha-dhamma.net/w/santa) santa (21) [171730](https://abhidhana.buddha-dhamma.net/w/santi) santi (21); `/w/vedanā` (vol. 20, 1c (w)) | (a); (c) | **(a)** only where a sense is missing |

**Decision (a letter per row, or "as recommended"):**

---

## G. Run-ons and homonyms

**G1. The seven unsure splits** (brief §69; `docs/splits-checked.tsv` column 5; a `wrong` removes the split at the next article
run and its Meaning row at the next `merge --ids`):

| id | book | the page | note | recommended |
|---|---|---|---|---|
| [157108](https://abhidhana.buddha-dhamma.net/w/visama) visama (20) | 20 | [PDF 74](https://abhidhana.buddha-dhamma.net/v/20/74) | the line is ဝိသမ⁴; five ဝိသမ rows | **right**: the text is a ဝိသမ entry; numbering to G6 |
| [162430](https://abhidhana.buddha-dhamma.net/w/sa) sa (20) | 20 | [PDF 740](https://abhidhana.buddha-dhamma.net/v/20/740) | the line is သ⁶; seven သ rows | **right**, as above |
| [166027](https://abhidhana.buddha-dhamma.net/w/sagga) sagga (21) | 21 | [PDF 228](https://abhidhana.buddha-dhamma.net/v/21/228) | sagga's text, split inside its analysis | **right**: the text is the article's |
| [168888](https://abhidhana.buddha-dhamma.net/w/sata) sata (21) | 21 | [PDF 553](https://abhidhana.buddha-dhamma.net/v/21/553) | the line is သတ⁸; nine သတ rows | **right**, numbering to G6 |
| [180718](https://abhidhana.buddha-dhamma.net/w/samadhisattav%C4%ABsatisatasahassamatta) samadhisattavīsatisatasahassamatta (22) | 22 | [PDF 364](https://abhidhana.buddha-dhamma.net/v/22/364) | its text; split at the analysis's second line | **right** |
| [181875](https://abhidhana.buddha-dhamma.net/w/sam%C4%81na) samāna (22) | 22 | [PDF 487](https://abhidhana.buddha-dhamma.net/v/22/487) | the line is သမာန²; host reads like two entries | **right**, numbering to G6 |
| [204389](https://abhidhana.buddha-dhamma.net/w/su) su (24) | 24 | [PDF 158](https://abhidhana.buddha-dhamma.net/v/24/158) | the line is သု² (ဗျ); five သု rows | **right**, numbering to G6 |

*Why*: each split gives a real entry of the same headword a body; "wrong" would put the text back into a neighbour. Which
homonym number the row is belongs to the homonym pass (G6). Claude has not seen these pages this session.
**Decision (right / wrong per id):**

**G2. Run-on text still inside a host** — **2,355 rows** flagged run-on (22 385, 20 331, 14/3 321, 21 303, 4/3 301, 24 295).
Examples: [156719](https://abhidhana.buddha-dhamma.net/w/vivec%C4%81petabba) vivecāpetabba (20) [182453](https://abhidhana.buddha-dhamma.net/w/sam%C4%81hitindriya) samāhitindriya (22) [221143](https://abhidhana.buddha-dhamma.net/w/hosi) hosi (25). Only the row's own text is translated; the neighbour's is in `omitted`.
Options: (a) accept as drafted until step 1.8; (b) split more now. *Recommended: (a)*: §67 showed the split rule reaches few of
these.
**Decision:**

**G3. Rows where an agent translated the neighbour's text as the row's own definition** (the departures of 1c (d), (k), (o), (s),
(ab)): vol. 23 [187500](https://abhidhana.buddha-dhamma.net/w/salla) salla (23) [187501](https://abhidhana.buddha-dhamma.net/w/salla) salla (23) [187506](https://abhidhana.buddha-dhamma.net/w/sallakatta) sallakatta (23) [187608](https://abhidhana.buddha-dhamma.net/w/sallapi) sallapi (23) [187609](https://abhidhana.buddha-dhamma.net/w/sallapita) sallapita (23) [187611](https://abhidhana.buddha-dhamma.net/w/sallapitu%E1%B9%81) sallapituṁ (23); vol. 24 [207949](https://abhidhana.buddha-dhamma.net/w/subhaka) subhaka (24) [208154](https://abhidhana.buddha-dhamma.net/w/suma%E1%B9%85gala) sumaṅgala (24) [209515](https://abhidhana.buddha-dhamma.net/w/susamucchinna) susamucchinna (24) [209651](https://abhidhana.buddha-dhamma.net/w/susukkakhandha) susukkakhandha (24); vol. 20 [163650](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81vara%E1%B9%87a) saṁvaraṇa (20)
[163859](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%81vidahi%E1%B9%81su) saṁvidahiṁsu (20) [156817](https://abhidhana.buddha-dhamma.net/w/visakkiyad%C5%ABta) visakkiyadūta (20) [157106](https://abhidhana.buddha-dhamma.net/w/visama) visama (20); vol. 21 [171012](https://abhidhana.buddha-dhamma.net/w/saddh%C4%81) saddhā (21) [171074](https://abhidhana.buddha-dhamma.net/w/saddh%C4%81dhipateyya) saddhādhipateyya (21); 14/3 [198085](https://abhidhana.buddha-dhamma.net/w/pi%E1%B9%87%E1%B8%8Dap%C4%81tap%C4%81risuddhi) piṇḍapātapārisuddhi (14/3) (the 17 ids the brief names; the set was not counted).
Options: (a) keep where the translated text is that headword's own definition (what a split would give), flag kept; (b) blank
them to `omitted`. *Recommended: (a)*, each checked against the host at 2.3.
**Decision:**

**G4. Senses printed twice, translated once** — **830 rows** flagged (14/2 118, 21 83, 22 79, 20 79). Examples: [2083](https://abhidhana.buddha-dhamma.net/w/acorisa%C3%B1%C3%B1a) acorisañña (1) [173950](https://abhidhana.buddha-dhamma.net/w/ek%C4%81baddha) ekābaddha (4/3)
[221075](https://abhidhana.buddha-dhamma.net/w/hemavata) hemavata (25). Rows where both copies were translated (flags "both copies / passes / parts"): **8** — [166545](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%85kh%C4%81ta) saṅkhāta (21) [184462](https://abhidhana.buddha-dhamma.net/w/sampayoga) sampayoga (22) [220334](https://abhidhana.buddha-dhamma.net/w/h%C4%ABna) hīna (25), and
satti [170052](https://abhidhana.buddha-dhamma.net/w/satti) satti (21), sattha [170159](https://abhidhana.buddha-dhamma.net/w/sattha) sattha (21), satthaka [170167](https://abhidhana.buddha-dhamma.net/w/satthaka) satthaka (21), satthu [170259](https://abhidhana.buddha-dhamma.net/w/satthu) satthu (21), pāḷi [197689](https://abhidhana.buddha-dhamma.net/w/p%C4%81l%CC%A4i) pāl̤i (14/3).
Options: (a) confirm "once", and cut the second copy in those 8; (b) translate both. *Recommended: (a)*; for saṅkhāra
[166574](https://abhidhana.buddha-dhamma.net/w/sa%E1%B9%85kh%C4%81ra) saṅkhāra (21), whose copies disagree, the page decides (F5).
**Decision:**

**G5. «Sn» of a run-on article kept in its host row** — **213 rows** (14/3 64, 4/3 60, 20 33). Examples: [157540](https://abhidhana.buddha-dhamma.net/w/visibbati) visibbati (20) [177520](https://abhidhana.buddha-dhamma.net/w/sannidhik%C4%81raka) sannidhikāraka (22)
[218553](https://abhidhana.buddha-dhamma.net/w/hatthacchinn%C4%81dibheda) hatthacchinnādibheda (25). *Recommended*: leave; they move when their article is split (1.8).
**Decision:**

**G6. Homonyms placed one entry late** (item 5b): 177 runs, 311 swaps measured (§67), plus the five numbering cases of G1 and
the five wrong splits of §69. Options: (a) step 1.8 after Phase 2; (b) before 2.3. For (b): the revision would not touch text that later moves to
another id. For (a): 1.8 needs image checks and is not sized, and Phase 2 need not wait for it. **Claude is unsure; the editor's call.**
**Decision:**

**G7. Headwords with no text at all** — 4,601 unlocated headwords not in their page's text (§67), and rows with no Meaning:
[186261](https://abhidhana.buddha-dhamma.net/w/sammukh%C4%ABbh%C5%ABta) sammukhībhūta (23) (lost its text in v0.28.0), [175181](https://abhidhana.buddha-dhamma.net/w/ogha) ogha (4/3) ogha¹, [208591](https://abhidhana.buddha-dhamma.net/w/sulabhad%C4%81ru) sulabhadāru (24), [205117](https://abhidhana.buddha-dhamma.net/w/sukh%C4%81disabh%C4%81va) sukhādisabhāva (24). Options: (a) accept "not yet translated" with the page
image; (b) the `page.psm6` fallback (1.7, Mac OCR + ~300 k tokens). *Recommended: (a) now, (b) optional later.*
**Decision:**

---

## H. The flag files by kind (plan step 2.2)

41,042 flag rows in 29 files, each given **one** kind: the first of the list below its text matches (a regex over the flag
text; `tmp/dec21/flags.py`). *Any* counts a row under every kind it mentions. The proposed action: **accept** (stays
`drafted` with its flag), **rule** (2.3, after this sheet), **image** (2.4), **editor** (2.5).

| kind | the test (substring, case-insensitive) | rows | any | proposed action |
|---|---|---:|---:|---|
| nothing to translate | nothing to translate / left empty | 41 | 41 | accept |
| run-on | run-on, wrong / previous line, belongs to the next … | 2,514 | 2,519 | accept (G2), later 1.8 |
| printed twice | twice, second copy, two passes | 1,070 | 1,144 | accept (G4) |
| person | person, aorist, optative, imperative, 1st/2nd/3rd | 2,402 | 2,522 | rule (A) |
| headword / text | headword | 1,860 | 3,681 | image for the strict 59 (F2); else accept |
| see X | see, cross-ref, ကြည့်, véase | 4,382 | 5,471 | accept (links checked by `report`) |
| OCR reading | OCR, "read X as Y", misread, typo | 14,697 | 17,965 | accept (the reading is flagged; sample in 2.4) |
| source defect | stray, as printed, sense numbering, skips | 1,518 | 3,147 | accept; image where a sense is missing (F10) |
| truncated | truncated, lost, missing, cut off | 1,586 | 3,750 | accept (F3) |
| garbled | garbled, illegible, debris, damaged | 1,268 | 4,056 | accept; editor for doctrinal rows (F4) |
| dropped | dropped, left out, omitted | 636 | 1,669 | accept (citations, quotations) |
| check on the page | check, verify, on the page, image | 225 | 600 | image (F5) |
| sense choice | could equally, may mean, rather than, by context | 450 | 815 | editor (by stem) |
| tentative | tentative, identified, perhaps, probably, ? | 2,632 | 7,241 | editor; names by B4.1 |
| rendering | kept in Pāḷi, ‹ ›, rendered, term, name, measure, Vinaya | 2,312 | 9,986 | rule (B, C) |
| hyphen | hyphen | 230 | 1,715 | accept (F007) |
| label / analysis | label, analysis, bracket, grammar, quotation | 1,916 | 5,992 | accept (E1) |
| other | none of the above | 1,303 | 1,303 | editor (sample) |
| **all** | | **41,042** | | |

The first-match order puts a row under its most specific kind; "OCR reading" is large because most OCR-book flags name a
reading first. Per book: Appendix B. Summed by proposed action (primary kind): **accept 31,718**, rule 4,714, image 225, editor 4,385 (= 41,042). The
stricter image lists of F1 (393) and F2 (59) are drawn from the accepted rows.

---

## Appendix A. The open stems of `stems.tsv` (status `proposed`, 131)

*Rows* = rows whose Burmese source contains the stem (substring; vols. 2–25 without the split rows; a short stem such as ရ
or ပြ over-counts). *Flag* is the file's own column. *Recommended*: approve the 108 without a flag as written (they are the
drafts' practice since vol. 1); the 23 flagged ones are C2 (`glossary`), E2 (F008, F012) or below (`review`, `homograph`).

| id | Burmese | proposed Spanish | flag | rows |
|---|---|---|---|---:|
| F001 | X-ကြည့် | Véase X. |  | 7,685 |
| F002 | X-လည်းကြည့် | Véase también X. |  | 716 |
| F003 | X, Y-တို့ကြည့် / တို့လည်းကြည့် | Véanse X, Y. / Véanse también X, Y. |  | 169 |
| F004 | X-နှင့် အနက်တူ | Mismo significado que X. |  | 15 |
| F005 | အထက်ပုဒ်နှင့် အနက်တူ | Mismo significado que la entrada anterior. |  | 0 |
| F006 | (၁) (၂) … / (က) (ခ) … | 1. 2. … / a. b. … |  | 24,952 |
| F007 | a-b-c (hyphen) | a / b / c |  | — |
| F008 | …သော၊ သူ၊ သည် | … (dicho de una persona; de una cosa) | review | 0 |
| F009 | -ခြင်း | el … (infinitivo sustantivado); el hecho de … |  | 53,929 |
| F010 | -မှု | el …; la acción de … |  | 6,785 |
| F011 | -သော | que … |  | 122,826 |
| F012 | -အပ်သော | …-do; que ha de ser …-do | review | 18,997 |
| F013 | -(သည်)၏ အဖြစ် | el hecho de ser … |  | 2 |
| F014 | -ရှိသော | que tiene … |  | 31,741 |
| F015 | -တတ်သော / -လေ့ရှိသော | que suele …; acostumbrado a … |  | 11,050 |
| F016 | -ခြင်းငှါ | para … |  | 2,308 |
| F017 | -၍ | habiendo …; tras … |  | 11,991 |
| F018 | -၏ (verb) | … (3.ª sing., presente) |  | 45,854 |
| F019 | -လတ္တံ့သော | que …-rá |  | 277 |
| F020 | မ-… | no …; in- |  | 113,295 |
| F021 | -ရာ | el lugar donde …; aquello en que … |  | 32,899 |
| F022 | -စေ- | hacer … |  | 22,469 |
| F023 | X-ဟု ဆိုအပ်သော / ခေါ်သော | llamado X; considerado X |  | 363 |
| F024 | X-ဟူသော | es decir X; que es X |  | 10,398 |
| F025 | X-စသော / အစရှိသော | X, etc.; que comienza por X |  | 3,044 |
| F026 | X-ကဲ့သို့ | como X |  | 1,111 |
| F027 | X-နှင့် တူသော | semejante a X |  | 692 |
| L001 | တရား | estado; fenómeno; la Enseñanza | glossary | 8,388 |
| L002 | မိမိ | uno mismo; propio |  | 1,315 |
| L003 | အခြား | otro |  | 1,731 |
| L004 | တပါး / တစ်ပါး | otro |  | 1,762 |
| L005 | အကြောင်း | causa, razón; relato | review | 7,121 |
| L006 | အလွန် | sumamente; muy |  | 1,973 |
| L007 | လွန် | pasar más allá; exceder |  | 4,490 |
| L008 | သဘော | naturaleza | glossary | 4,642 |
| L009 | သိ | conocer; saber |  | 23,215 |
| L010 | စိတ် | mente | glossary | 6,043 |
| L011 | ပြု | hacer |  | 13,185 |
| L012 | အနက် | significado |  | 3,551 |
| L013 | စကား | palabras; habla |  | 4,364 |
| L014 | အကျိုး | fruto, resultado; beneficio | review | 3,797 |
| L015 | ပြည့်စုံ | dotado de; completo |  | 3,220 |
| L016 | မဟုတ် | no (ser) … |  | 1,207 |
| L017 | အကျိုးစီးပွါး | bienestar; provecho |  | 83 |
| L018 | လွန်ကဲ | excesivo |  | 531 |
| L019 | မြတ် | excelente; noble |  | 4,854 |
| L020 | နေ | morar / el sol | homograph | 10,836 |
| L021 | ရောက် | llegar a; alcanzar |  | 6,512 |
| L022 | အပိုင်းအခြား | límite |  | 909 |
| L023 | နိဗ္ဗာန် | Nibbāna | glossary | 1,767 |
| L024 | ပြ | mostrar |  | 47,874 |
| L025 | ဆုံးဖြတ် | decidir; juzgar |  | 744 |
| L026 | အဆုံး | fin |  | 1,619 |
| L027 | စင်စစ် | absolutamente |  | 229 |
| L028 | မှီ | depender de; apoyarse en |  | 3,113 |
| L029 | ရ | obtener |  | 117,693 |
| L030 | လွှမ်းမိုး | dominar; vencer |  | 580 |
| L031 | ကျော်လွန် | sobrepasar; traspasar |  | 296 |
| L032 | အချင်းချင်း | unos a otros; mutuamente |  | 124 |
| L033 | တူ | semejante; igual |  | 6,353 |
| L034 | ဆို | decir |  | 9,298 |
| L035 | တည် | permanecer; estar asentado |  | 7,374 |
| L036 | မီး | fuego |  | 1,796 |
| L037 | လွန်ကျူး | transgredir |  | 238 |
| L038 | အကျင့် | práctica; conducta |  | 2,039 |
| L039 | အလို | deseo | glossary | 2,775 |
| L040 | သက်ဝင် | adentrarse en; entrar en |  | 669 |
| L041 | အင်္ဂါ | miembro; factor |  | 739 |
| L042 | မိမိကိုယ် | a sí mismo |  | 80 |
| L043 | ဟော | enseñar; exponer |  | 4,737 |
| L044 | ကင်း | libre de; sin |  | 4,169 |
| L045 | ဆောင် | traer; llevar |  | 5,772 |
| L046 | ဖြစ်စေ | producir; causar |  | 2,939 |
| L047 | ထား | poner; colocar |  | 4,385 |
| L048 | ဝတ္ထု | relato; objeto; base | review | 1,868 |
| L049 | အမှတ် | percepción; noción | glossary | 1,271 |
| L050 | အဋ္ဌကထာ | comentario |  | 640 |
| L051 | အပြစ် | falta; defecto |  | 1,409 |
| L052 | နှိပ်စက် | oprimir; afligir |  | 1,699 |
| L053 | မကောင်းမှု | mala acción | glossary | 335 |
| L054 | ကောင်းမှု | buena acción; mérito | glossary | 850 |
| L055 | သုတ် | sutta |  | 3,130 |
| L056 | ပြောဆို | hablar |  | 2,173 |
| L057 | ယှဉ် | asociado con |  | 3,639 |
| L058 | သွား | ir / diente | homograph | 4,017 |
| L059 | အာရုံ | objeto (de la mente) | glossary | 2,367 |
| L060 | အနက်သဘော | significado; sentido |  | 451 |
| L061 | လွန်ပြီး | pasado |  | 41 |
| L062 | ဆင်းရဲ | sufrimiento; dolor | glossary | 1,542 |
| L063 | အနက်အဓိပ္ပါယ် | significado |  | 40 |
| L064 | တပ်မက် | pasión; apegarse | glossary | 761 |
| L065 | သင့် | conveniente; apropiado |  | 3,131 |
| L066 | စွဲယူ | aferrarse a |  | 98 |
| L068 | ဧကန် | ciertamente; enteramente |  | 109 |
| L069 | ကျင့် | practicar |  | 3,742 |
| L070 | အကျိုးမဲ့ | daño; lo inútil |  | 95 |
| L071 | မမြဲ | impermanente | glossary | 52 |
| L072 | အမြတ်ဆုံး | el más excelso; supremo |  | 146 |
| L073 | အပေါင်း | conjunto; agrupación |  | 3,016 |
| L074 | မတရား | injusto; indebido |  | 50 |
| L075 | အယူ | opinión; creencia | glossary | 1,610 |
| L076 | အက္ခရာ | letra; sílaba |  | 363 |
| L077 | အခြင်းအရာ | modo; aspecto |  | 1,469 |
| L078 | ယူ | tomar |  | 6,861 |
| L079 | သဒ္ဒါ | palabra; gramática |  | 2,837 |
| L080 | ထက်ဝက် | mitad |  | 119 |
| L081 | လူ | ser humano |  | 2,585 |
| L082 | ကိုယ် | cuerpo |  | 3,576 |
| L083 | ပျက်စီး | perecer; destruirse |  | 2,033 |
| L084 | အတ္တဘော | existencia individual; cuerpo | glossary | 252 |
| L085 | ထိုက် | digno de |  | 2,343 |
| L086 | ပိုင်းခြား | delimitar; discernir |  | 1,185 |
| L087 | မြင် | ver |  | 3,150 |
| L088 | အင်္ဂါကြီးငယ် | los miembros mayores y menores |  | 46 |
| L089 | မျက်စိ | ojo |  | 549 |
| L090 | သင်္ကန်း | hábito | glossary | 989 |
| L091 | အရပ် | lugar; región |  | 3,711 |
| L092 | အခြားမဲ့ | inmediatamente siguiente |  | 291 |
| L093 | တုန်လှုပ် | temblar; estremecerse |  | 805 |
| L094 | နင်း | pisar |  | 576 |
| L095 | နှစ်သက် | deleitarse en; gustar de |  | 1,896 |
| L096 | အမည် | nombre |  | 1,969 |
| L097 | အတိုင်းအရှည် | medida; extensión |  | 1,137 |
| L098 | ကျေးဇူး | favor; beneficio recibido |  | 808 |
| L099 | ဉာဏ် | conocimiento | glossary | 3,403 |
| L100 | နေရာ | lugar; asiento |  | 1,213 |
| L101 | နတ် | deva (se mantiene en pāḷi) |  | 2,411 |
| L102 | ရဟန်း | monje |  | 2,184 |
| L104 | ဥတု | utu (temperatura, se mantiene en pāḷi); estación |  | 259 |
| L105 | ဂုဏ် | cualidad; virtud |  | 2,077 |
| L106 | လူ (of the gihi- compounds) | laico |  | 2,585 |

**Flagged `review` / `homograph`** (besides C2 and E2): L005 အကြောင်း *causa, razón; relato* (the account of X in titles),
L014 အကျိုး (revised 27 Sep for -attha: approve), L020 နေ *morar / el sol*, L048 ဝတ္ထု *relato; objeto; base* (and *caso* in the
Vinaya, a flag in vol. 1), L058 သွား *ir / diente*. *Recommended*: approve, the sense decided per row as the note says.

**Decision (approve all / exceptions):**

## Appendix B. Flag rows by book and kind (primary kind)

| book | nothing | runon | twice | person | hw_text | seex | ocr_read | source | truncated | garbled | dropped | check | sense | tentative | rendering | hyphen | label_an | other | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 15 | 5 | 28 | 92 | 241 | 109 | 26 | 50 | 3 | 7 | 20 | 74 | 47 | 16 | 35 | 47 | 816 |
| 2 | 2 | 1 | 16 | 2 | 24 | 47 | 178 | 46 | 52 | 26 | 8 | 10 | 15 | 32 | 25 | 5 | 14 | 14 | 517 |
| 3 | 0 | 5 | 70 | 8 | 62 | 151 | 299 | 90 | 51 | 40 | 8 | 19 | 26 | 61 | 54 | 12 | 75 | 45 | 1,076 |
| 5 | 2 | 0 | 17 | 16 | 50 | 161 | 287 | 61 | 8 | 62 | 14 | 16 | 26 | 190 | 233 | 7 | 82 | 43 | 1,275 |
| 6 | 1 | 0 | 9 | 129 | 19 | 60 | 297 | 85 | 9 | 77 | 8 | 6 | 20 | 313 | 59 | 8 | 20 | 34 | 1,154 |
| 7 | 3 | 0 | 8 | 53 | 6 | 151 | 145 | 31 | 44 | 22 | 3 | 5 | 9 | 103 | 61 | 2 | 13 | 24 | 683 |
| 8 | 0 | 3 | 6 | 105 | 14 | 53 | 123 | 71 | 7 | 43 | 2 | 5 | 26 | 107 | 47 | 0 | 7 | 17 | 636 |
| 9 | 1 | 0 | 9 | 55 | 17 | 125 | 174 | 29 | 21 | 32 | 2 | 3 | 8 | 215 | 71 | 1 | 14 | 21 | 798 |
| 10 | 0 | 0 | 22 | 95 | 14 | 293 | 148 | 41 | 9 | 40 | 63 | 3 | 2 | 72 | 63 | 3 | 23 | 28 | 919 |
| 11 | 1 | 1 | 6 | 44 | 15 | 31 | 137 | 27 | 10 | 28 | 1 | 10 | 12 | 87 | 60 | 0 | 15 | 12 | 497 |
| 12 | 1 | 2 | 41 | 181 | 45 | 66 | 362 | 92 | 36 | 62 | 36 | 5 | 9 | 65 | 43 | 10 | 50 | 43 | 1,149 |
| 13 | 1 | 0 | 4 | 190 | 20 | 23 | 165 | 26 | 95 | 29 | 0 | 11 | 20 | 59 | 155 | 3 | 26 | 29 | 856 |
| 14/1 | 0 | 0 | 4 | 94 | 7 | 49 | 89 | 45 | 5 | 18 | 1 | 2 | 5 | 48 | 31 | 3 | 4 | 63 | 468 |
| 15 | 0 | 1 | 3 | 169 | 69 | 85 | 361 | 25 | 20 | 55 | 38 | 11 | 29 | 151 | 107 | 15 | 73 | 78 | 1,290 |
| 16 | 0 | 2 | 18 | 121 | 67 | 188 | 582 | 105 | 35 | 73 | 83 | 3 | 27 | 186 | 181 | 24 | 103 | 132 | 1,930 |
| 17 | 0 | 4 | 35 | 61 | 44 | 354 | 466 | 78 | 25 | 47 | 21 | 0 | 23 | 105 | 127 | 30 | 135 | 105 | 1,660 |
| 18 | 0 | 1 | 18 | 130 | 31 | 160 | 409 | 52 | 18 | 68 | 16 | 3 | 25 | 105 | 196 | 25 | 630 | 108 | 1,995 |
| 19 | 1 | 4 | 53 | 206 | 152 | 190 | 426 | 73 | 40 | 44 | 22 | 0 | 21 | 71 | 149 | 28 | 257 | 83 | 1,820 |
| 20 | 5 | 345 | 87 | 70 | 165 | 277 | 896 | 31 | 98 | 27 | 22 | 12 | 9 | 40 | 61 | 7 | 34 | 46 | 2,232 |
| 21 | 1 | 318 | 102 | 62 | 147 | 220 | 1,134 | 71 | 145 | 32 | 26 | 14 | 10 | 63 | 67 | 3 | 39 | 46 | 2,500 |
| 22 | 0 | 405 | 84 | 74 | 135 | 270 | 1,386 | 47 | 155 | 84 | 10 | 13 | 11 | 29 | 31 | 6 | 24 | 39 | 2,803 |
| 23 | 9 | 244 | 49 | 38 | 117 | 202 | 899 | 34 | 77 | 40 | 20 | 7 | 13 | 103 | 80 | 1 | 60 | 49 | 2,042 |
| 24 | 1 | 326 | 57 | 13 | 119 | 256 | 1,360 | 18 | 135 | 32 | 8 | 11 | 10 | 62 | 34 | 0 | 77 | 19 | 2,538 |
| 25 | 1 | 181 | 50 | 30 | 46 | 167 | 1,061 | 9 | 66 | 57 | 4 | 2 | 7 | 39 | 52 | 2 | 8 | 19 | 1,801 |
| 4/1 | 2 | 2 | 14 | 5 | 27 | 45 | 109 | 37 | 9 | 24 | 7 | 19 | 10 | 42 | 24 | 0 | 13 | 20 | 409 |
| 4/2 | 1 | 0 | 34 | 57 | 46 | 116 | 290 | 48 | 29 | 22 | 58 | 7 | 12 | 42 | 32 | 8 | 27 | 43 | 872 |
| 4/3 | 4 | 306 | 52 | 108 | 142 | 278 | 1,085 | 16 | 60 | 28 | 12 | 7 | 6 | 24 | 67 | 4 | 7 | 23 | 2,229 |
| 14/2 | 0 | 29 | 120 | 174 | 78 | 70 | 232 | 50 | 46 | 40 | 100 | 8 | 23 | 31 | 66 | 3 | 17 | 35 | 1,122 |
| 14/3 | 4 | 333 | 67 | 107 | 154 | 202 | 1,356 | 71 | 255 | 66 | 40 | 6 | 16 | 113 | 89 | 4 | 34 | 38 | 2,955 |
| **all** | 41 | 2,514 | 1,070 | 2,402 | 1,860 | 4,382 | 14,697 | 1,518 | 1,586 | 1,268 | 636 | 225 | 450 | 2,632 | 2,312 | 230 | 1,916 | 1,303 | 41,042 |

