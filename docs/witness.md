# The typed witness: PCED's "Tipiṭaka Pāḷi-Myanmar Dictionary" in Unicode

*25 September 2026. Built by `tools/abhidhana_witness.py`, converted by `tools/zawgyi.py`. The
output, `witness/pced_k.jsonl`, is gitignored: see §5.*

## 1. Source

Pali Canon E-Dictionary 1.94 (PCED) is the data behind dictionary.sutta.org, whose About page
says only that "the source of the dictionaries come from Pali Canon E-Dictionary Version 1.94
(PCED)". The data is in the public repo `siongui/data`, `dictionary/dict_words_{1,2}.csv`.
Dictionary `K` is "Tipiṭaka Pāḷi-Myanmar Dictionary တိပိဋက-ပါဠိမြန်မာ အဘိဓာန်": **157,271 entries,
153,529 distinct headwords**, typed in Zawgyi. Each cell reads
`key：headword（label）<br>[analysis]<br>definition`, with full-width punctuation in place of ASCII.

## 2. Conversion

`tools/zawgyi.py` uses python-myanmar's converter (`pip install python-myanmar`) and corrects it
where it loses what the source typed. Each correction was found by comparing converted headwords
with the index, and checked against PCED's own romanised key:

| what the converter does | correction | example |
|---|---|---|
| re-derives tall vs round aa by its own spelling rule | keep the source's ါ or ာ | ပွါး stays ပွါး (not ပွား) |
| drops ံ from ႎ (i + anusvara) | split before converting | ဥပနိဇ္ဈာယိံသု |
| drops the vowel from kinzi + i / ii | split before converting | ပဉ္စင်္ဂိက, သမင်္ဂီ |
| gives an e typed before a ligature (ṇḍ ṭṭh ṭṭ ḍḍ ḍḍh) to the consonant before it | carry it to the ligature | ပဋိဃဋ္ဋေတိ |
| leaves stacked ၲ ႓ ႅ ႖, kinzi ၤ, ၽ ႈ ႕, tall u ဳ ဴ, and ႆ unconverted | place them after the base consonant | အန္တေဝါသိက, အဗ္ဘ, ဿ |
| — | ဥ + ီ → ဦ; စျ → ဈ (Zawgyi typists write jha as ca + ya-pin) | ဈာန |

The definitions also get two normalisations: full-width punctuation → ASCII, and a ဝ standing for
zero inside a number → ၀. Four entries keep a Zawgyi-only character (unclear source typing). The
source cell is kept in `zg` on every row.

## 3. Checks

**Against the index's spelling.** 152,653 of the 153,529 distinct converted headwords (**99.4%**)
are index headwords letter for letter; 156,375 of 157,271 entries. Before the corrections in §2 it
was 98.0%. The residue is mostly the witness's own spelling, not the conversion: ာ where the index
has ါ after a stacked consonant (158, the print's spelling too; see `ocr/03/articles-report.md`),
a space inside a compound (108, ကိံ ပဘုတိက), and different verb forms (ပဗ္ဗဇန္တိ for ပဗ္ဗာဇေန္တိ).

**Which volumes it has.** Share of each book's index headwords present in the witness:

| books | coverage |
|---|---:|
| 01, 02, 03, 4a, 4b, 05–14, 15–19 | 98.7–100% each; 152,913 of 153,231 = **99.8%** |
| 4c, 14b, 14c, 20–25 | 0–0.7% |

So the witness is the dictionary as far as vol. 19, without the three "second parts" (4/3, 14/2,
14/3). That is also the app's split between the Buddhasetaman iOS scans (vols 1–19) and the rest
(`docs/app-info.html`), which suggests the typed text came from the same source. That is an
inference, not a finding. This replaces the per-volume 94.5–96.0% in the brief, which matched on
the romanised key rather than on the converted Burmese.

**Against the page images.** Every entry on vol. 3 pp. 600 and 1008 (27 index headwords; 25 in
the witness under the index spelling, the other 2 under the print's ာ):

- labels 25 of 25 and compound analyses 25 of 25 agree with the print;
- definitions agree word for word in 24 of 25. In one, အရူပပဋိသံယုတ္တ, the source has
  `နာမ္တရား，စပ္ယွဉ္ေသာ` where the print has နာမ်တရားနှင့် စပ်ယှဉ်သော: a typing omission in PCED, not a
  conversion error;
- spacing around the dashes between alternative renderings is not kept (နှင့်-တူသော for နှင့် – တူသော);
- the witness writes ဖ in အသမ္ဖ… as the index does, which settles the reading of p. 1008.

And vol. 1 pp. 121–122 (the five entries for အ): the witness has them, but edited. It
modernises (တစ်လုံး for the print's တလုံး), turns the running text "ပကတိ နိပါတ် –" into an
analysis `[ပကတိနိပါတ်]`, and gives the numbered senses without their Pāḷi glosses
("(၁) ဆန့်ကျင်ဖက်" for the print's "(၁) ပဋိပက္ခ=ဝိရုဒ္ဓ (ဆန့်ကျင်ဖက်)").

## 4. What it is good for, and what not

- **Good for**: the label, the compound analysis, and the Burmese definition, as clean text
  with no OCR noise, for 99.8% of vols 1–19. That is a second witness beside the OCR, per article.
- **Not for**: the Pāḷi quotations and their citations (it omits them: 158 of vol. 1's entries
  carry a reference numeral), the Pāḷi glosses inside a definition, and the print's exact wording
  (it is lightly edited). **The page stays the authority**, and the index for headwords.
- Vols 20–25 and 4c, 14b, 14c have no witness: the OCR is all there is.

## 5. Licence

Not stated. `siongui/data`'s README lists sources and licences for its other files, but not for
the dictionaries, and dictionary.sutta.org says nothing either. PCED's own terms were not found.
Until they are, **`witness/` stays out of git** and nothing derived from it (the Reader column,
merged articles) is published. Using it to *check* our own OCR, and reporting agreement figures,
publishes nothing of its text.

## 6. Next

1. ~~Join it to `ocr/NN/articles.jsonl` by headword (and homonym order), and flag label and
   analysis disagreements per article.~~ Done 25 Sep: `docs/witness-join.md`,
   `tools/abhidhana_witness_join.py`. It found homonyms placed one entry late, now fixed.
2. Offer its definition beside the OCR one in the Reader, only after §5 is settled (or privately).
3. Where our article is unlocated (e.g. the short headwords such as အ¹–⁵), its text is the only
   clean one we have; say so in the Reader rather than silently substituting it.
