# Translation, batch 1: formulas and the commonest stems of vol. 1

*25 September 2026. For Angel to review. Every rendering below is **proposed**; nothing is applied
until you approve it. Translated from the Burmese, English and Spanish each from the Burmese (the
Pāḷi column is the word the Burmese glosses, for disambiguation, not the source). The machine-readable
copy is `docs/translation/stems.tsv`; your decisions go in its `status` column (`approved`, or a
corrected rendering), or reply in chat.*

## How to read this

- **Formulas** (F) are the grammar of the definitions: rendered once, applied by rule. Approving
  F001–F005 alone fills **390 vol. 1 articles (4.8%)** exactly: their whole definition is "see X",
  "see also X" or "same meaning as X". X is always a headword, so it is linked and romanised from
  the index, not from the text.
- **Lexical stems** (L) are words, with the grammatical ending taken off. A stem's rendering is used
  wherever it occurs, **but a stem is not a sentence**: an article whose definition has three
  stems still needs its sentence composed. With batch 1 approved, 253 more vol. 1 articles (3.1%)
  have every stem approved; the 100 stems cover 15.3% of stem occurrences in vol. 1.
- **Alternatives** (the hyphens) are shown as `a / b`, never merged; a long dash (–) separates groups.
- **Flags**: `glossary` = a doctrinal term the IEBH glossary should fix (proposal only, not an
  improvisation); `homograph` = two different words in one spelling; `review` = a choice I am not sure of.
- Counts are over vol. 1: `occ` stem occurrences, `art` articles.

## Decisions needed before any Meaning box is filled

1. **Which Burmese text to translate from.** Our OCR of the definitions carries debris and split
   words (vol. 1: "မကြမ်း ထမ်း" for မကြမ်းထမ်း, stray "ရျ ချူ ဝ"), and sometimes stops early
   (*aṇḍaka*: senses (ဂ), (၂), (၃) missing). The PCED typed text of the same dictionary is clean and
   complete for vols. 1–19. Translating from it would publish a translation of the dictionary, not
   PCED's text, but it derives from a source whose licence is unknown. **Your call.** The counts here
   are from PCED; with the OCR the figures are lower and the list is polluted by OCR fragments.
2. **Mechanical fill vs composed drafts.** The formulas and one-stem definitions can be filled by rule.
   The rest (two-thirds of vol. 1) need a sentence per article. My proposal: I draft those in
   alphabetical runs, using only approved renderings, each marked **drafted**; stems met that are not
   yet approved go into the next batch instead of being improvised.
3. **Where the IEBH glossary is.** The only IEBH-normative glossary I found is grammatical
   (`~/Tipitaka/nissaya/anchor/glosario-gramaticas.md`, with Nandisena's IEBH 2013 glossary). The
   doctrinal terms flagged `glossary` below need your rendering; if a doctrinal glossary exists
   elsewhere, point me to it.

## Formulas

| id | Burmese | Pāḷi | English | Español | flag | note |
|---|---|---|---|---|---|---|
| F001 | X-ကြည့် | — | See X. | Véase X. |  | X is a headword: linked, and romanised from the index, not from the text |
| F002 | X-လည်းကြည့် | — | See also X. | Véase también X. |  |  |
| F003 | X, Y-တို့ကြည့် / တို့လည်းကြည့် | — | See X, Y. / See also X, Y. | Véanse X, Y. / Véanse también X, Y. |  |  |
| F004 | X-နှင့် အနက်တူ | — | Same meaning as X. | Mismo significado que X. |  |  |
| F005 | အထက်ပုဒ်နှင့် အနက်တူ | — | Same meaning as the preceding headword. | Mismo significado que la entrada anterior. |  |  |
| F006 | (၁) (၂) … / (က) (ခ) … | — | 1. 2. … / a. b. … | 1. 2. … / a. b. … |  | as docs/spanish-method.md §2 |
| F007 | a-b-c (hyphen) | — | a / b / c | a / b / c |  | alternatives of one Pāḷi element, kept apart; a long dash (–) separates groups (vol. 1 p. 92) |
| F008 | …သော၊ သူ၊ သည် | tiliṅga | … (said of a person; of a thing) | … (dicho de una persona; de una cosa) | review | the adjective used as a noun: သူ a person, သည် a thing or state. Alternative: "one who …; that which …" / "el que …; lo que …" |
| F009 | -ခြင်း | -na, -tā, bhāva | the …-ing; the act of …-ing | el … (infinitivo sustantivado); el hecho de … |  | verbal noun |
| F010 | -မှု | -na, kamma | …-ing (as a deed) | el …; la acción de … |  |  |
| F011 | -သော | relative, adjectival | that …; …-ing | que … |  |  |
| F012 | -အပ်သော | -ta, -tabba, -anīya | …-ed; to be …-ed | …-do; que ha de ser …-do | review | past and future passive share the form; the Pāḷi suffix decides, where the analysis gives it |
| F013 | -(သည်)၏ အဖြစ် | -tā, -tta, bhāva | the state of being … | el hecho de ser … |  | as docs/spanish-method.md §4 |
| F014 | -ရှိသော | -vant, -ika, bahubbīhi | having … | que tiene … |  |  |
| F015 | -တတ်သော / -လေ့ရှိသော | -sīla, -ī, -ka | apt to …; in the habit of … | que suele …; acostumbrado a … |  |  |
| F016 | -ခြင်းငှါ | -tuṁ | in order to …; to … | para … |  |  |
| F017 | -၍ | -tvā | having … | habiendo …; tras … |  |  |
| F018 | -၏ (verb) | -ti | … (3rd sing., present) | … (3.ª sing., presente) |  | a verb headword is glossed in the 3rd person: သွား၏ goes / va |
| F019 | -လတ္တံ့သော | -ssanta (future) | that will … | que …-rá |  |  |
| F020 | မ-… | a-, na- | not …; un- | no …; in- |  | negation |
| F021 | -ရာ | -ṭhāna, locative | the place where …; that in which … | el lugar donde …; aquello en que … |  |  |
| F022 | -စေ- | causative | to cause to …; to make … | hacer … |  |  |
| F023 | X-ဟု ဆိုအပ်သော / ခေါ်သော | saṅkhāta | called X; reckoned as X | llamado X; considerado X |  |  |
| F024 | X-ဟူသော | appositive | X, namely …; which is X | es decir X; que es X |  |  |
| F025 | X-စသော / အစရှိသော | -ādi | X and so on; beginning with X | X, etc.; que comienza por X |  | as docs/spanish-method.md §5 |
| F026 | X-ကဲ့သို့ | viya, iva | like X | como X |  |  |
| F027 | X-နှင့် တူသော | sadisa | like X; resembling X | semejante a X |  |  |

## Lexical stems, commonest first

| id | Burmese | Pāḷi | English | Español | occ | art | flag | note |
|---|---|---|---|---|---:|---:|---|---|
| L004 | တပါး / တစ်ပါး | añña | another | otro | 235 | 175 |  | usually an alternative to အခြား: "other / another" |
| L001 | တရား | dhamma | state; phenomenon; the Teaching | estado; fenómeno; la Enseñanza | 232 | 185 | glossary | dhamma: which rendering where is a glossary decision; in definitions it is mostly "a state / phenomenon" after an adjective |
| L002 | မိမိ | atta- (reflexive), ajjhatta | oneself; one's own | uno mismo; propio | 195 | 137 |  |  |
| L003 | အခြား | añña | other | otro | 188 | 148 |  |  |
| L005 | အကြောင်း | kāraṇa, hetu; vatthu | cause, reason; account | causa, razón; relato | 181 | 157 | review | X၏ အကြောင်း in a sutta or jātaka title is "the account of X" |
| L006 | အလွန် | ati-, adhi- | exceedingly; very | sumamente; muy | 149 | 140 |  |  |
| L007 | လွန် | ati-, atikkama | to pass beyond; to exceed | pasar más allá; exceder | 135 | 112 |  |  |
| L008 | သဘော | sabhāva, bhāva | nature | naturaleza | 131 | 109 | glossary | sabhāva |
| L010 | စိတ် | citta | mind | mente | 125 | 104 | glossary | citta: mente / conciencia / consciencia; IEBH to fix |
| L011 | ပြု | karoti | to do; to make | hacer | 122 | 110 |  |  |
| L009 | သိ | jānāti, ñā | to know | conocer; saber | 121 | 96 |  |  |
| L012 | အနက် | attha | meaning | significado | 117 | 98 |  |  |
| L013 | စကား | vacana, vācā, kathā | speech; words | palabras; habla | 109 | 94 |  |  |
| L014 | အကျိုး | phala; attha | fruit, result; benefit | fruto, resultado; beneficio | 98 | 77 | review | two senses: phala (result) and attha (benefit); the Pāḷi of the headword decides |
| L015 | ပြည့်စုံ | sampanna, samaṅgī | endowed with; complete | dotado de; completo | 94 | 78 |  |  |
| L016 | မဟုတ် | na (… hoti) | not (being) … | no (ser) … | 93 | 83 |  |  |
| L017 | အကျိုးစီးပွါး | attha, hita | welfare; benefit | bienestar; provecho | 93 | 74 |  |  |
| L018 | လွန်ကဲ | adhika, ati- | excessive | excesivo | 90 | 75 |  |  |
| L019 | မြတ် | agga, uttama, ariya | excellent; noble | excelente; noble | 86 | 62 |  |  |
| L021 | ရောက် | patta, gacchati | to reach; to arrive at | llegar a; alcanzar | 82 | 71 |  |  |
| L022 | အပိုင်းအခြား | pariccheda, pariyanta | limit; boundary | límite | 80 | 68 |  |  |
| L023 | နိဗ္ဗာန် | nibbāna | Nibbāna | Nibbāna | 74 | 57 | glossary | kept in Pāḷi, as IEBH keeps Buddha |
| L024 | ပြ | dasseti | to show | mostrar | 71 | 63 |  |  |
| L025 | ဆုံးဖြတ် | vinicchaya | to decide; to judge | decidir; juzgar | 71 | 55 |  |  |
| L027 | စင်စစ် | accanta, ekanta | absolutely; utterly | absolutamente | 70 | 65 |  |  |
| L026 | အဆုံး | anta, pariyosāna | end | fin | 68 | 56 |  |  |
| L028 | မှီ | nissaya, nissita | to depend on; to rest on | depender de; apoyarse en | 67 | 47 |  |  |
| L029 | ရ | labhati | to obtain | obtener | 67 | 55 |  |  |
| L030 | လွှမ်းမိုး | abhibhavati | to overpower | dominar; vencer | 65 | 57 |  |  |
| L031 | ကျော်လွန် | atikkamati | to go beyond; to transgress | sobrepasar; traspasar | 65 | 55 |  |  |
| L032 | အချင်းချင်း | aññamañña | one another; mutually | unos a otros; mutuamente | 63 | 61 |  |  |
| L033 | တူ | sadisa, sama | alike; similar | semejante; igual | 60 | 54 |  |  |
| L034 | ဆို | vadati, vuccati | to say | decir | 59 | 55 |  | ဟု ဆိုအပ်သော is formula F023 |
| L035 | တည် | tiṭṭhati, ṭhita | to stand; to abide | permanecer; estar asentado | 57 | 45 |  |  |
| L036 | မီး | aggi | fire | fuego | 57 | 49 |  |  |
| L037 | လွန်ကျူး | vītikkama | to transgress | transgredir | 56 | 47 |  |  |
| L038 | အကျင့် | paṭipatti, cariyā | practice; conduct | práctica; conducta | 56 | 49 |  |  |
| L039 | အလို | icchā, chanda, kāma | wish; desire | deseo | 55 | 41 | glossary | not "craving" (taṇhā) |
| L041 | အင်္ဂါ | aṅga | limb; factor | miembro; factor | 55 | 34 |  |  |
| L040 | သက်ဝင် | ogāhati, pavisati | to enter into | adentrarse en; entrar en | 54 | 36 |  |  |
| L042 | မိမိကိုယ် | attānaṁ | oneself | a sí mismo | 53 | 44 |  |  |
| L043 | ဟော | deseti, bhāsati | to teach; to preach | enseñar; exponer | 53 | 50 |  |  |
| L044 | ကင်း | rahita, vigata | free from; without | libre de; sin | 52 | 48 |  |  |
| L045 | ဆောင် | vahati, āvaha | to bring; to carry | traer; llevar | 52 | 38 |  |  |
| L046 | ဖြစ်စေ | janeti, uppādeti | to produce; to cause | producir; causar | 52 | 42 |  |  |
| L077 | အခြင်းအရာ | ākāra | mode; manner | modo; aspecto | 52 | 49 |  |  |
| L047 | ထား | ṭhapeti, nikkhitta | to place; to set | poner; colocar | 49 | 30 |  |  |
| L048 | ဝတ္ထု | vatthu | story; object; basis | relato; objeto; base | 48 | 43 | review | three senses; the headword decides |
| L049 | အမှတ် | saññā | perception; notion | percepción; noción | 48 | 44 | glossary | saññā |
| L050 | အဋ္ဌကထာ | aṭṭhakathā | commentary | comentario | 48 | 47 |  |  |
| L052 | နှိပ်စက် | pīḷeti | to oppress; to afflict | oprimir; afligir | 47 | 43 |  |  |
| L055 | သုတ် | sutta | sutta | sutta | 47 | 41 |  |  |
| L056 | ပြောဆို | katheti, vadati | to speak | hablar | 45 | 37 |  |  |
| L057 | ယှဉ် | sampayutta, yutta | associated with | asociado con | 45 | 43 |  |  |
| L058 | သွား | gacchati / danta | to go / tooth | ir / diente | 45 | 38 | homograph | aggadanta: ရှေ့သွား "front tooth" |
| L059 | အာရုံ | ārammaṇa | object (of the mind) | objeto (de la mente) | 44 | 36 | glossary | ārammaṇa |
| L060 | အနက်သဘော | attha | meaning; sense | significado; sentido | 44 | 41 |  |  |
| L061 | လွန်ပြီး | atīta, atikkanta | past; gone by | pasado | 44 | 32 |  |  |
| L062 | ဆင်းရဲ | dukkha | suffering; pain | sufrimiento; dolor | 43 | 34 | glossary | dukkha |
| L063 | အနက်အဓိပ္ပါယ် | attha | meaning | significado | 43 | 39 |  |  |
| L064 | တပ်မက် | rāga, rajjati | passion; to be attached | pasión; apegarse | 42 | 32 | glossary | rāga |
| L065 | သင့် | yutta, arahati | fitting; proper | conveniente; apropiado | 42 | 38 |  |  |
| L066 | စွဲယူ | gāha, parāmasati | to cling to; to grasp | aferrarse a | 42 | 28 |  |  |
| L100 | နေရာ | ṭhāna, āsana | place; seat | lugar; asiento | 42 | 35 |  |  |
| L067 | အကုသိုလ် | akusala | unwholesome | no saludable (akusala) | 41 | 38 | glossary | akusala: IEBH to fix (inhábil / insano / perjudicial …) |
| L068 | ဧကန် | ekanta | certainly; wholly | ciertamente; enteramente | 41 | 38 |  |  |
| L069 | ကျင့် | carati, paṭipajjati | to practise | practicar | 41 | 32 |  |  |
| L070 | အကျိုးမဲ့ | anattha | harm; what is useless | daño; lo inútil | 41 | 36 |  |  |
| L071 | မမြဲ | anicca | impermanent | impermanente | 41 | 24 | glossary | anicca |
| L020 | နေ | vasati, viharati / sūriya | to dwell / the sun | morar / el sol | 40 | 36 | homograph | two words: the verb, and နေ "the sun" (aṁsumālī: နေ။) |
| L072 | အမြတ်ဆုံး | agga, seṭṭha | foremost; highest | el más excelso; supremo | 40 | 34 |  |  |
| L073 | အပေါင်း | samūha, piṇḍa | collection; group | conjunto; agrupación | 39 | 38 |  |  |
| L074 | မတရား | adhamma | unrighteous; improper | injusto; indebido | 39 | 27 |  |  |
| L075 | အယူ | diṭṭhi, laddhi, gāha | view; belief | opinión; creencia | 39 | 32 | glossary | diṭṭhi |
| L076 | အက္ခရာ | akkhara | letter; syllable | letra; sílaba | 38 | 29 |  |  |
| L078 | ယူ | gaṇhāti | to take | tomar | 38 | 35 |  |  |
| L079 | သဒ္ဒါ | sadda | word; grammar | palabra; gramática | 38 | 25 |  |  |
| L080 | ထက်ဝက် | aḍḍha | half | mitad | 38 | 36 |  |  |
| L081 | လူ | manussa | human being | ser humano | 37 | 15 |  |  |
| L082 | ကိုယ် | kāya | body | cuerpo | 37 | 28 |  |  |
| L083 | ပျက်စီး | vinassati, bhaṅga | to perish; to be destroyed | perecer; destruirse | 37 | 32 |  |  |
| L051 | အပြစ် | dosa, vajja | fault | falta; defecto | 36 | 31 |  |  |
| L084 | အတ္တဘော | attabhāva | individual existence; body | existencia individual; cuerpo | 36 | 31 | glossary | attabhāva |
| L085 | ထိုက် | araha | worthy of; deserving | digno de | 36 | 31 |  |  |
| L086 | ပိုင်းခြား | paricchindati | to delimit; to discern | delimitar; discernir | 36 | 28 |  |  |
| L088 | အင်္ဂါကြီးငယ် | aṅgapaccaṅga | the limbs, major and minor | los miembros mayores y menores | 34 | 33 |  |  |
| L089 | မျက်စိ | cakkhu, akkhi | eye | ojo | 34 | 29 |  |  |
| L090 | သင်္ကန်း | cīvara | robe | hábito | 33 | 26 | glossary | cīvara: hábito / túnica |
| L091 | အရပ် | ṭhāna, padesa, disā | place; region | lugar; región | 33 | 31 |  |  |
| L092 | အခြားမဲ့ | anantara | immediately following | inmediatamente siguiente | 33 | 30 |  |  |
| L095 | နှစ်သက် | ruci, abhinandati | to delight in; to like | deleitarse en; gustar de | 33 | 23 |  |  |
| L094 | နင်း | akkamati | to tread on | pisar | 32 | 27 |  |  |
| L096 | အမည် | nāma | name | nombre | 32 | 21 |  |  |
| L097 | အတိုင်းအရှည် | pamāṇa | measure; extent | medida; extensión | 32 | 27 |  |  |
| L099 | ဉာဏ် | ñāṇa | knowledge | conocimiento | 27 | 27 | glossary | ñāṇa: conocimiento / sabiduría |
| L087 | မြင် | passati, dassana | to see | ver | 20 | 15 |  |  |
| L053 | မကောင်းမှု | pāpa | evil deed | mala acción | 16 | 15 | glossary | pāpa |
| L093 | တုန်လှုပ် | kampati | to tremble; to be shaken | temblar; estremecerse | 13 | 11 |  |  |
| L054 | ကောင်းမှု | puñña, kusala | good deed; merit | buena acción; mérito | 12 | 10 | glossary | puñña |
| L098 | ကျေးဇူး | upakāra | kindness done; favour | favor; beneficio recibido | 11 | 11 |  |  |

## Spanish abbreviations for the labels (decision 2 of the site design)

Proposed for `docs/labels.md` §0, column `abbr. es`; until you confirm them the site shows the full
Spanish word. They follow Spanish dictionary practice (the noun class first, then the qualifier:
*v. caus.*, not *caus. v.*).

| label | Español | abbr. en | abbr. es (proposed) |
|---|---|---|---|
| (ပု) | nombre masculino | m. | m. |
| (ထီ) | nombre femenino | f. | f. |
| (န) | nombre neutro | n. | n. |
| (တိ) | adjetivo (los tres géneros) | adj. | adj. |
| (ကြိ) | verbo | v. | v. |
| (ကြိ၊ဝိ) | calificativo verbal: absolutivo, infinitivo | abs./inf. | abs./inf. |
| (ကာ၊ကြိ) | verbo causativo | caus. v. | v. caus. |
| (နာမ-ကြိ) | verbo denominativo | denom. v. | v. denom. |
| (ဗျ) | indeclinable | indecl. | indecl. |
| (ပု၊န) (ပု၊ထီ) (ပု၊တိ) | masculino o neutro / femenino / adjetivo | m./n. … | m./n., m./f., m./adj. |
| (န၊ပု) (န၊ထီ) (န၊တိ) | neutro o masculino / femenino / adjetivo | n./m. … | n./m., n./f., n./adj. |
| (ထီ၊ပု) (ထီ၊န) (တိ၊န) | | f./m., f./n., adj./n. | f./m., f./n., adj./n. |
| (ပုံ-ဗဟု) | masculino, solo en plural | m. pl. | m. pl. |
| (ကမ္မ၊ကြိ) | verbo pasivo | pass. v. | v. pas. |
| (ကာ၊ကမ္မ၊ကြိ) | verbo causativo pasivo | caus. pass. v. | v. caus. pas. |
| (ကာ၊ကြိ၊ဝိ) | absolutivo causativo | caus. abs. | abs. caus. |
| (စတုတ္ထန္တ) | terminado en el cuarto caso (dativo) | — | dat. |
| (တတိယန္တ-ဗျ) | indeclinable en el tercer caso (instrumental) | — | indecl. instr. |
| (အ-လိင်) | sin género | — | sin gén. |

