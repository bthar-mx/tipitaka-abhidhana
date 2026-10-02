# Changelog

Versions of the Tipiṭaka Pāḷi-Myanmā Abhidhāna project: the data, the tools and the site together.
*Scheme proposed 26 September 2026; the editor created the tags v0.1.0–v0.7.0 the same day.*

## The scheme

`vMAJOR.MINOR.PATCH`, one number for the whole repository, recorded in three places: the file
`VERSION`, an annotated git tag on the commit, and a section of this file.

- **0.x** while nothing in the dictionary has been reviewed by a reader of Burmese. Every row is
  `ocr` or `drafted`.
- **MINOR** for a milestone a user of the data or the site would notice: a new layer of data (a
  volume's Meaning boxes, the PCED analyses), a re-run that changes figures across books, a new
  site section.
- **PATCH** for fixes that change no published figure: typos, a page's layout, the docs.
- **1.0.0** when the text layer is complete *and* reviewed work is published: proposed as the
  first volume whose Meaning boxes the editor has reviewed (status `reviewed` or `corrected`), with the
  licence question settled (brief §10). Until then, a 0.x number says "drafts".
- The source release `sources-v1` (PDFs and index) keeps its own name: it versions the inputs,
  not the project.

A release note says, per version: what changed, the brief's sections, and the headline figures
(located, label + body, Meaning rows drafted / reviewed).

## v0.29.5 — 1 Oct 2026

Decision D3 (item 00c): the institute's name is spelt **Instituto de Estudios Buddhistas Hispano**, as the logo and footer
already had it (the editor). About (EN and ES), README and LICENSE changed from "Budistas" (brief §96). No data or figures changed.

## v0.29.4 — 1 Oct 2026

The 39 farther-body splits that §89's image check found wrong, made from its readers' notes; the article re-run that brings §93's
*သုတ္တန်* into the citations (brief §95). Data, tools and Meaning files; no site code changed.

- **`docs/farbody-fix.tsv`** (new) and `FARBODY_FIX` in `tools/abhidhana_articles.py` (`ABH_FARBODY_FIX=0` turns it off): 43 rows, each the
  start and end line of a printed entry and the rows whose lines hold it, every one read on the page image again (42 items, 7 by a second
  reader): 36 of the 39 items made, and 7 rows moved to their own printed entry (two swaps of the ငါ and 3rd-person forms, 163760 / 163761
  and 163811 / 163812; one of ု / ူ, 186731 / 186732). 202368 ပေက္ခတေ's entry goes to 202376, the same headword in the print's order. 4 rows
  that sat on a line of a fixed entry are left unlocated, flagged (161221, 161399, 182509, 218328). **Not made, for the editor**: 198532,
  205449 (index questions) and 182509 (an unsettled homonym run).
- **Articles + romanisation re-run, 29 books** (87 `ocr/` files): 209 rows change — 43 fixed, 31 hosts cut, 4 left unlocated, and 131 rows
  whose citations gain *သုတ္တန်* (82 headed, 50 new, every new one with a tooltip; no tooltip changed or lost). With the table off the files
  are the committed tool's, and differ from v0.29.3's only in those 131 rows. Unlocated 12,106 → 12,074; label + body 196,172 → 196,210.
- **Meaning** (books 14c, 20–25): 35 new drafts and 2 formula rows for the fixed rows, 6 redrafted rows given their own entry, 6 hosts
  redrafted, 22 hosts' `flag` / `omitted` trimmed, 1 host drafted, 1 re-merged as formula, 3 withdrawn (`docs/translation/withdrawn.tsv`).
  **217,773 Meaning rows** (98.5% of the index), all drafted but 9 corrected.
- `docs/splits-checked.tsv` (notes on the 47 rows), `docs/page-checks.tsv` (217511 superseded). The `/w/` addresses: 0 of 221,154 change.

## v0.29.3 — 1 Oct 2026

The Meaning box's drafted note shortened (the editor, 1 Oct): "Traducción del birmano al español hecha con IA, sin revisar." / "AI
translation from the Burmese, unreviewed." ("No es una lectura." / "Not a reading." removed). The same in Copy and on the About page;
the UI test's expectations updated. Site only.

## v0.29.2 — 1 Oct 2026

The Meaning box's status line, and the tooltips the ။ parser lost (brief §93). Site and tools only; no article re-run.

- **The Meaning box**: the status badge (*borrador* / *draft*, *revisado* / *reviewed*, *corregido* / *corrected*) moves below the text,
  small and muted, on one line with its note: "Traducción del birmano al español hecha con IA, sin revisar. No es una lectura." / "AI
  translation from the Burmese, unreviewed. Not a reading."; "Traducción revisada / corregida por el editor." / "Translation reviewed /
  corrected by the editor."; the partial states keep their notes; *sin traducir* unchanged. Copy writes the same line after the Meaning;
  the About page's *drafted* row has the same wording.
- **`cite_how`** (`tools/abhidhana_browse.py`): when every other step fails, the head is read again with "-" dropped, ။ read as ၊, ၊ put
  before a mark ending a part and `HEADTYPO` applied. 93 of v0.29.1's 96 lost tooltips are back with their old work; no other tooltip
  changes its work or is lost; 622 more citations get one (585 inferred). Tooltips 626,130 → **626,845 of 685,834 (91.4%)**, inferred
  39,328 → 39,974.
- **`ASAT_WORKS`** (`tools/abhidhana_articles.py`) gains *သုတ္တန်*: simulated, it changes no tooltip (131 rows, 50 new citations, all with a
  tooltip). Not yet in the data: the next article run applies it.
- `site/test/editor/ui-test.js`: step 9, the status line at 375 and 1,024 px, ES and EN, and Copy in English (5 checks); the Copy checks of
  steps 7–8 and the status checks of steps 1 and 3 follow the new wording. Expect UI pass 93 fail 0.

## v0.29.1 — 30 Sep 2026

The ။ citation parser fix (brief §92). Re-run of the article step and romanisation for all 29 books; only the citation fields change.

- **`CITE` / `cite_trim` in `tools/abhidhana_articles.py`**: an abbreviation closed by ။ (*မိလိန္ဒ။ ၁၂၃။*, the form of a work in one
  volume, and the OCR's ။ for ၊), a head cut from its commentary mark by ။, a space or a line end (*ထေရ / ဌ၊*, *မူလ- / ဋီ၊*), and an
  abbreviation with an asat or a kinzi (*ဓာန်*, *ကင်္ခါ*, *မောဂ်* and its OCR readings) are read as the work; the old pattern stays as the
  fallback, so nothing it read is lost; `tools/abhidhana_witness_analysis.py` collects them with the same `cites()`. `ABH_CITE_FIX=0` restores the old reading: with it the 116 `ocr/` files are v0.29.0's byte for
  byte. With the fix, only `citations` (77,921 rows) and `citations_iast` (77,918) change; ids, order and every other field are the same.
- **Figures**: citations 530,869 → **685,834** (+154,965 parsed for the first time); with a tooltip 489,082 (92.1%) → **626,130 (91.3%)**;
  over the citations v0.29.0 had, 92.1% → **93.7%**; number-only citations 18,415 → **8,036**; of §90's 2,845 lost-head rescues, 2,084
  now read directly. 2 tooltips change their work (to the broader *ကင်္ခါ၊ ဋီ*), 96 are lost (a browse-side fold recovers 93 in
  simulation: not applied). Page images: 18 of 20 sampled citations read, 17 right.
- **`prep`** (nine OCR books): the Burmese for drafting changes in 3,569 of 61,627 rows (3,329 lose citation material only); 13 rows
  leave the list, 2 enter it. Not redrafted; the list is in `tmp/cite92/prep-changed.tsv` (gitignored).
- Meaning rows unchanged: 217,738, all `drafted` but the 9 corrected.

## v0.29.0 — 30 Sep 2026

Plan step 1.8 (brief §85–89, §91) and the citation tooltips' second pass (§90). Re-runs across all 29 books. Released with the six
local commits before it (10a6e4d … 3d4cfe9) and stage 3's.

- **Homonyms placed on their own printed entries** (§86, §88). Rule R in `tools/abhidhana_articles.py`: in a run of identical index
  headwords, row i takes the i-th printed entry line when the counts agree (R moved 668 rows; image samples 28 / 30 right in the nine
  books without PCED); in books 01–19 PCED gates R and moves 274 rows more (143 take a sibling's text; sample 19 / 20). The nine books'
  residue, 172 runs / 456 rows, read on the page image (a second reader on 159 runs): `docs/homonyms-checked.tsv`, applied as
  `HOMONYM_FIX` (420 rows; 61 index rows with no entry of their own kept as `same_as` records; 36 unsure left). 44 new split candidates
  made (right on the image). `ABH_HOMONYM=0` turns all of it off.
- **Farther-body run-ons split out** (§89): `farbody_split()`, all 29 books: 523 split rows (427 PCED-gated in 01–19, 96 read right on the
  image in the nine), 272 hosts cut, 35 chained rows on their own line, 83 left unlocated. `ABH_FARBODY=0` turns it off. With both off the
  tool reproduces v0.28.6's `ocr/` files byte for byte (116 of 116, checked again in §91).
- **The nine books' Meaning rows redrafted** (§91): of the 1,036 rows 1.8 changed, 330 drafted (new rows), 11 new formula rows, 263
  redrafted, 6 re-merged as formula rows, **53 withdrawn** ("not yet translated"; recorded in the new `docs/translation/withdrawn.tsv`),
  175 hosts kept with `flag` / `omitted` trimmed, 150 kept as they were, 48 with nothing to do or drafted empty. Every row `drafted`.
  **Meaning rows 217,450 → 217,738 (98.5% of the index).**
- **Citation tooltips** (§90): lost heads taken from the body, *အပါ* alone → အပ၊ဋ္ဌ; "leído como …" / "read as …" when the work is
  inferred (`cg` per record). Citations with a tooltip: 489,082 of 530,869 (92.1%). Not tested in Safari, on a phone or with the Mac's fonts.
- **Index errata** (`docs/index-errata.md` §5): 4 repeats left (now on their own printed entries), 174421 ဧဓတိ re-read (printed ¹; the
  index lists ² first); the 78 repeats of §85 all stay.
- **Check files re-read** (§91 §5): `page-checks.tsv` 17 rows (7 still valid, 10 superseded), `splits-checked.tsv` 24 (15 / 9),
  `revision-queue.tsv` 26 (24 / 2, new column `reread_1_8`).
- `/w/` addresses: address → id unchanged for all 221,154 records (full builds before and after).
- Headline figures: 221,154 index rows; label + body 196,172 (§89); Meaning rows 217,738 drafted / 9 corrected / 0 reviewed.

## v0.28.6 — 29 Sep 2026

- **A Meaning with numbered senses is shown as a list** (brief §84; display only: the Meaning text and the data are unchanged,
  Copy still copies the plain text). The draft's own "(1)", "(2)" are the markers, hanging to the left, no gap between senses,
  the same font size; text before (1) (karoti's "hace;") stays as a lead line; letter sub-senses (a), (b) … are nested under
  their number. A marker is "(n)" at the start or after `.` `;` `:` `,` (grammatical labels such as "(adjetivo)" before it go
  with that sense); "(n)" anywhere else (`Véase [[x]] (2)`, "veinte (20)") is text. The list is used only with ≥ 2 markers
  running 1, 2, 3 … with no gap or repeat, in a Meaning longer than 120 characters; otherwise the paragraph is as before.
  Over 8 senses: the first 8 and *mostrar todo (N)* / *show all (N)*.
- Measured over `docs/translation/meanings/*.jsonl` (217,450 rows): **9,478 ES and 8,877 EN Meanings split** (1,993 / 1,978 with
  nested letters; 314 each with more than 8 senses). Numbers but left as a paragraph (ES / EN): 120 characters or fewer 8,021 /
  8,619; numbers only inside the text (cross-references, counts) 4,308 / 4,312; one marker 840 / 844; a number repeated 1,174 /
  1,173; not starting at (1) 201 / 203; a gap 184 / 181.
- `site/src/assets/browse.js` (the senses block, `mall` in the fold state), `style.css` (one block). UI test step 8 (27 checks,
  375 and 1,280 px): expect UI pass 88 fail 0.
- No data file changed.

## v0.28.5 — 29 Sep 2026

- **Copy / Cite / Share no longer add a line on a phone** (brief §83). v0.28.4's UI test on the Mac (real fonts) failed at 375 px
  on `/w/luñcana`: with a label and the *corregido* chips, the head line wrapped once the three buttons were added (the Meaning box
  407 → 435 px). Below 768 px the buttons now sit out of the flow at the top right of the article, in the 28 px that are always
  empty above the meta line ("vol. … · p. …"); nothing reserves room for them, so the head and the meta line are laid out exactly as
  without them, whatever they hold. 26 px tall there (28 on desktop); the message flashes below them, right-aligned. The DOM order is
  unchanged (headword, buttons, label). Desktop and 768–1,023 px as they were. `site/src/assets/style.css` only.
- UI test step 7: the 375-px check covers three articles — bhijja, luñcana with step 6's edits, and bhijjanasabhāva² (homonym
  superscript, both scripts, the labels in full, a label edit for the *corregido* chip, the homonyms, *análisis no leído*, a
  supplement row) — and checks, besides the Meaning box, the head's height with and without the buttons, that the buttons overlap
  neither the head nor the meta line, and names the web fonts loaded. `ABH_FONTS=<folder>` serves a local copy of the fonts
  (`run.sh`). Expect UI pass 61 fail 0.
- No data file changed.

## v0.28.4 — 29 Sep 2026

- **Copy, Cite and Share on every article** (brief §81), beside the headword in Browse and on `/w/…`, modelled on the Reader of
  buddha-dhamma.net (icon buttons, `navigator.clipboard`, a short ✓ flash). *Copy*: the headword (IAST · Burmese), label,
  analysis, the Meaning in the page's language with its status (*borrador, sin revisar* / *revisado* / *corregido* / *corregido en
  parte: sentido (n)*), the Burmese definition marked as the dictionary's text (machine-read, unchecked, or corrected by hand), and
  one attribution line; plain text, one field per line. *Cite*: e.g. "Tipiṭaka Pāḷi-Myanmā Abhidhāna, vol. 15 (suplemento,
  encuadernado en el vol. 4/3), p. 686 (p. del PDF 713), s.v. bhijja. Edición digital, IEBH, v0.28.4.
  https://abhidhana.buddha-dhamma.net/w/bhijja (consultado el 29 sep 2026)." (EN: "PDF p.", "Digital edition", "accessed 29 Sep
  2026"). *Share*: `navigator.share` (title, the citation, the address) where the browser has it; otherwise the link is copied
  ("enlace copiado"). Buttons with `aria-label`s, a `role="status"` message; no height added at 375 px. Strings ES / EN in `common.js`.
  UI test: 10 new checks (`site/test/editor/ui-test.js` step 7).
- **Citation tooltips: a normaliser for damaged abbreviations** (brief §82; built in the advice chat, reviewed here). New
  `tools/abhidhana_citefold.py`, called at the end of `abhidhana_browse.cite_key()` when every earlier match fails; the citation text
  shown is unchanged. Citations with a tooltip **450,399 → 483,912 of 530,965 (84.8% → 91.1%)**; no citation matched before maps
  to another work (checked against a build without the fallback: 0 changed, 0 lost, 33,513 gained). 10 newly resolved citations
  checked on the page images: 10 right.
- No data file changed: `ocr/*`, `meanings/*`, D1 and editor mode as they were.

## v0.28.3 — 29 Sep 2026

- **The supplements bound in vol. 4/3 shown with the volumes they belong to** (brief §78 way (c), §79; NEXT-SESSION item 9).
  New `docs/supplements.tsv`, 223 rows (id, book 4c, belongs_to 15 / 4b / 16 — 53 / 114 / 56 —, after_id, how, note), made by
  `tools/abhidhana_supplements.py` with the Pāḷi-alphabet key; 88 anchors `checked` on the page images (4c PDF pp. 721–735, vol. 15
  p. 738), 135 `key`. 22 supplement headwords are printed otherwise than the index spells them (e.g. ဥပဝေသန, indexed ဥပသေဝန); their
  anchors use the printed form. No data file changed: the index, `ocr/4c/*`, `meanings/4c.jsonl`, D1 and editor mode as they were.
- Browse: each supplement row after its anchor in that volume's alphabet; "vol. 15 (supplement, bound in vol. 4/3)", the page,
  image, printed page and edits still 4/3's. **Addresses unchanged** (assigned before the move: 0 of 221,154 differ). Homonym
  superscripts follow the order shown: in 32 rows the superscript and the address's `-N` now differ (e.g. `/w/mata` is *mata*³).
  The bh and m letters no longer list 4/3 among their volumes. Search results name the volume the same way; the page view of
  4c pp. 713–735 names the volume it supplements.
- Volumes: 4/2, 15 and 16 show "+ N in the supplement bound in 4/3", 4/3 "5,007 + 223 in the supplements to vols. 4/2, 15, 16";
  the index figures are kept. `data/volumes.json` gains `supp` / `supp_out`; `search.json` rows and Browse shards gain a `kb`
  element for supplement rows; `v4c.json` records gain `kb`.
- No article data, Spanish or published figure changed.

## v0.28.2 — 29 Sep 2026

- **Citation abbreviations from vol. 15's key** (brief §77, item 3b): `docs/introduction/citation-abbreviations.tsv` 100 → 123 rows.
  The 23 base abbreviations of the later volumes' key (vol. 15, PDF pp. 23–28; vol. 4/1 prints the same) that vol. 1's table lacks
  (*vi nicchaya ṭī*, *netti ṭī*, *netti vi*, *vi saṅgaha*, *milinda*, *peṭako*, C.P.D., P.T.S. …), and the key's spellings *paṭisaṁ*
  and *anu ṭī* as alternatives of vol. 1's *paṭi saṁ* and *anuṭī*. All *drafted*, transcribed from the page images, not checked by
  the editor; page written `15/N`, linked to book 15's page image.
- Browse: an `A / B` row matches both forms (it matched neither before). Citations with a tooltip 449,811 → 450,399 of 530,965
  (84.7% → 84.8%). Most of the rest is OCR damage in the citations, not missing abbreviations; no normaliser yet.
- No article data, Spanish or published figure changed.

## v0.28.1 — 29 Sep 2026

- **14 "see X" links without their stray mark** (brief §71): 14/3 192706, 193589, 194844; 21 165539, 165879, 167295, 168395, 168914,
  169374; 22 180186; 23 187505, 192332; 24 209222, 209501. `merge NN --ids` over a fresh `prep` (the §65 target fix), no redraft;
  e.g. *Véase [[sakula”]]* → *Véase [[sakula]]*. No other row, `omitted` or `terms` line changed; the flags files only in these rows.
- Plan step 2.2's id lists (per book and proposed action; `tmp/dec21/lists/`, not committed): accept 31,718, rule 4,714, image 225,
  editor 4,385. Nothing applied to the Spanish.

## v0.28.0 — 29 Sep 2026

- **The split rows and their hosts redrafted** (brief §70; plan step 1.6), in the nine books without PCED. The 241 rows split out in
  v0.27.0 get Meaning boxes: 237 drafted, 2 "see X" formula rows; 208591 has nothing left after `prep`, 205117 was drafted empty. Of the
  156 hosts, **30 had translated the run-on text now split off**: 29 redrafted from what is left, and 186261 sammukhībhūta, left with
  nothing, lost its row; **126 had put it in `omitted`**: their Meaning is kept and only the parts of `flag` / `omitted` about the
  split-off text were taken out (4 of them are now a formula only and were re-merged as formula rows). Two shards (14/2's text layer, 79
  lines; the OCR books, 188), one agent each, the prompt of §55–57; hosts classified by two agents; 0.62 M agent tokens in all.
- **Meaning rows 217,212 → 217,450** (98.3% of the index), all `drafted` except the 9 corrected; flags in the nine books 20,240 → 20,222.
  Checked: no row or flag / omitted line changed outside the split rows and hosts; the usual draft checks, 0 errors.
- `tools/abhidhana_meanings.py merge --ids`: an id with no explanation left or an empty new draft now loses its row, and an id with no new
  draft keeps its `omitted` line (it was dropped); unit test in `tools/test_meanings_merge.py`.

## v0.27.0 — 28 Sep 2026

- **Run-on articles split out of their neighbour** (brief §69; plan steps 1.3 reduced and 1.4), in the nine books without PCED only
  (14/2, 14/3, 20–25, 4/3): `abhidhana_articles.py` `split_runons()`, the rule of §67 plus a homonym rule and an end at the next
  headword of the neighbourhood. Each split row carries `split_from`, `split_rule`, `split_checked`; each host `split_to` and
  `body_before_split`. **Every split checked on the page image** (the editor's decision): 248 checked, 234 right, 7 wrong (left out;
  all homonyms or double headwords), 7 unsure (kept, listed in §69); `docs/splits-checked.tsv`. **241 splits applied; 234 articles
  gained a body** (articles without a body in the nine books 2,899 → 2,665); label + body 57,786 → 58,022 in those books.
- Tested: no row outside the split rows and their 156 hosts changed (per-row digest), and books 01–19 (with 4/1, 4/2, 14/1) re-run
  byte-identical. Articles, romanisation and reports re-run for the nine books. The site maps `located: "split"` to the fuzzy mark.
- Not done: the Meaning boxes of the split rows and hosts (plan step 1.6, the redraft).

## v0.26.5 — 28 Sep 2026

- **Tooltips larger and easier to see** (the editor asked): the browser's small `title` tooltips are replaced by the site's own, in the
  theme's colours, 15 px (17 px for Burmese), shown after a short delay below the element or above it near the bottom edge; on touch
  screens a tap on a chip, note or Pāḷi word shows its tip for 4 s (`common.js`, `style.css`). Display only; no data change. Tested
  in Chrome on the live page (injected) before the push, not yet in Safari or Firefox.

## v0.26.4 — 28 Sep 2026

- **Site display only; no data change** (brief §68; the editor's decisions of 28 Sep on §66's questions). Passage lines are hidden
  behind *show everything* only when they are one word or over 30% non-letters: 279 of 504,587 (was 172,598); on sīla 1 of 59 (was 24),
  in vol. 24 1 of 13,640 (was 4,038). Citations: unchanged, only all-digit ones hidden (16,953); "vi 1", "ma 1" stay visible.
  *Analysis not read* only where an analysis is likely printed (PCED books: where PCED has one; other books: `[` or `+` in the raw
  head line): 7,878 articles (was 11,873; none now in books 01–19). *Label not read* unchanged (13,127). NEXT-SESSION: Phase 1 reduced
  to the split pass in the nine books without PCED (~200 articles), per the editor.

## v0.26.3 — 28 Sep 2026

- **Site display only; no data change** (brief §66). Phones (below 768 px): the five tabs and ES / EN fold behind a ☰ button, and
  the mode bar (reading modes, *personalizado*, printed page, settings) behind one *Ajustes* button: on `/w/sīla` at 375×812 the header
  goes from 252 to 101 px and the Meaning box starts at 299 px (was 524). The header keeps to one line from 1,024 px up (was 1,180).
- Pāḷi passages and citations fold to their first 5 lines, with *show all (N)*; lines of under 3 Pāḷi words or over 30% non-letters,
  and citations with no work abbreviation (digits only, "2.50"), are hidden behind *show everything*: 172,598 of 504,587 passage lines
  (34.2%) and 16,953 of 530,971 citations (3.2%); on sīla 24 of 59 and 1 of 30. The "extracted by machine" note moved to the top of
  each list.
- Long headwords wrap in the list (full word in a tooltip) and in the article; *label not read* / *analysis not read* where the
  reading yielded none; the homonyms beside the headword (*homónimos 1 2 3 4*); previous / next side by side at the foot on phones;
  a tooltip on *borrador*. The label table on `/abbreviations/` scrolls in its own box on phones (it pushed the page sideways).

## v0.26.2 — 28 Sep 2026

- **`merge` re-applies `docs/translation/corrections-es.tsv`** (brief §65): a re-merge no longer drops the editor's corrections;
  `merge --ids` keeps the work file's order instead of sorting by id. New `tools/test_meanings_merge.py`: re-merging vols. 18, 16 and 19
  is byte-identical to the committed files, all 9 corrections kept.
- **Vol. 4/3's "see X" targets restored in `prep`** (ဩ read as သြ / သ / သဩ, stray brackets and quotation marks) and 4c re-merged
  without redrafting: 250 rows' links changed; links matching a headword 652 → 884 of 1,136 (57.4 → 77.8%).
- A sense marker (ရ) after "see X" is OCR's reading of the digit ၇ (174722, checked on the page): now *(7)*. 176231 and 193595's
  (န) / (လ) are spelling marks, not senses (checked on the page): left for the editor.

## v0.26.1 — 28 Sep 2026

- **Docs only; no data or site change.** The brief's §2–49 moved unchanged into `docs/abhidhana-brief-archive.md` (the numbering
  kept); the brief keeps §1, a summary of the facts still in use, and §50–64 (248,594 → 114,880 bytes).
- The Reader is retired (the editor): the website replaces it; the artifact is left as it is. Noted in the README and NEXT-SESSION.
- NEXT-SESSION: the plan for the next phase (run-on splits, unplaced articles, the final revision, housekeeping), with the editor's
  decisions of 28 Sep; 00x (the v0.26.0 live check) marked done.

## v0.26.0 — 28 Sep 2026

- **Vol. 4/3's Meaning boxes, with the supplements to vols. 15, 4/2 and 16 bound after it, merged from the drafts of §63** (brief §64;
  not drafted again): 4,784 rows in `docs/translation/meanings/4c.jsonl` (9 formula, 4,775 drafted), all `drafted`, `source: ocr`;
  2,232 rows flagged (`4c-flags.tsv`), 3,015 lines of what the drafts left out (`4c-omitted.tsv`), 468 terms kept in Pāḷi
  (`4c-terms.tsv`). 207 of the rows are the supplements (50 to vol. 15, 107 to 4/2, 50 to 16), kept under book 4c as the index files
  them. 446 of the book's 5,230 articles have no Meaning (400 have no body). About and README: every volume drafted. Meaning rows in
  all: **217,212, 98.2% of the index, none reviewed**; every one of the 29 books has its drafts.
- "See X" links in 4/3 match a headword in 57.4% of cases (other OCR books 77–84%): ဩ read as သြ / သ in the target (brief §51) and
  stray `[` / `”`; not fixed. NEXT-SESSION: 00x, 1b, 1c (af).

## v0.25.0 — 28 Sep 2026

- **Vol. 14/3's Meaning boxes drafted from our OCR** (brief §63): 9,348 rows in `docs/translation/meanings/14c.jsonl` (12 formula,
  9,336 drafted), all `drafted`, `source: ocr`; 21 shards, one agent each, the OCR-book prompt of vols. 20–25. 2,956 rows flagged
  (`14c-flags.tsv`), 5,920 lines of what the drafts left out (`14c-omitted.tsv`), 737 terms kept in Pāḷi (`14c-terms.tsv`); 1,042 of the
  book's 10,390 articles have no Meaning (845 have no body). About and README: "vols. 1–3, 4/1, 4/2, 5–13 and 14/1–25". Meaning rows in
  all: **212,428, 96.1% of the index, none reviewed**.
- Vol. 4/3's shards were drafted too, not merged (brief §63; outputs kept in `tmp/`, gitignored). NEXT-SESSION: 1b, 1c (ab)–(ae), 00w.

## v0.24.1 — 28 Sep 2026

- **`abhidhana_meanings.py prep`: a witness join that pairs no row counts as no join** (brief §62). `witness/join-4c.jsonl` exists but
  pairs nothing (PCED has no vol. 4/3), and `prep` took the raw `body_joined` for 4c. Books with a real join, and books with none, are
  unchanged: `prep` for 14b, 15 and 23 byte-identical before and after; `prep 15` against the real witness byte-identical to the files
  vol. 15 was drafted from; `prep 4c` now gives the work file and shards of §62.
- Brief §62: vols. 14/3 and 4/3 prepared (not drafted), and the clean-row signal measured on the OCR books. NEXT-SESSION: 00v done
  (0.24.0 checked live); the editor's decision to draft 14/3 and 4/3; the `prep 15` checks done. No data or site change.

## v0.24.0 — 28 Sep 2026

- **Vol. 25's Meaning boxes drafted from our OCR** (brief §61): 3,732 rows in `docs/translation/meanings/25.jsonl` (57 formula,
  3,675 drafted), all `drafted`, `source: ocr`; 8 shards, one agent each, the OCR-book prompt of vols. 20–24. 1,801 rows flagged
  (`25-flags.tsv`), 3,144 lines of what the drafts left out (`25-omitted.tsv`), 330 terms kept in Pāḷi (`25-terms.tsv`); 314 of the
  book's 4,046 articles have no Meaning. The noisiest book so far: 10.4% of drafted lines clean. About and README list vol. 25.
  Meaning rows in all: **203,080, 91.8% of the index, none reviewed**.
- NEXT-SESSION: 00u done (0.23.0 checked live); 1b and 1c updated for vol. 25; 1c (w): vol. 20's vedanā to check on the page.

## v0.23.0 — 28 Sep 2026

- **Vol. 20's Meaning boxes drafted from our OCR** (brief §60): 6,947 rows in `docs/translation/meanings/20.jsonl` (199 formula,
  6,748 drafted), all `drafted`, `source: ocr`; 15 shards, one agent each, the OCR-book prompt of vols. 21–24. 2,253 rows flagged
  (`20-flags.tsv`), 3,945 lines of what the drafts left out (`20-omitted.tsv`), 946 terms kept in Pāḷi (`20-terms.tsv`); 419 of the
  book's 7,366 articles have no Meaning. About and README list vol. 20. Meaning rows in all: **199,348, 90.1% of the index, none
  reviewed**.
- NEXT-SESSION: 00t done (0.22.0 checked live); 1b and 1c updated for vol. 20.

## v0.22.0 — 28 Sep 2026

- **Vol. 21's Meaning boxes drafted from our OCR** (brief §59): 7,752 rows in `docs/translation/meanings/21.jsonl` (221 formula,
  7,531 drafted), all `drafted`, `source: ocr`; 17 shards, one agent each, the OCR-book prompt of vols. 22–24. 2,499 rows flagged
  (`21-flags.tsv`), 4,402 lines of what the drafts left out (`21-omitted.tsv`), 736 terms kept in Pāḷi (`21-terms.tsv`); 377 of the
  book's 8,129 articles have no Meaning. About and README list vol. 21. Meaning rows in all: **192,401, 87.0% of the index, none
  reviewed**.
- NEXT-SESSION: 00s done (0.21.0 checked live); 1b and 1c updated for vol. 21.

## v0.21.0 — 28 Sep 2026

- **Vol. 24's Meaning boxes drafted from our OCR** (brief §58): 6,685 rows in `docs/translation/meanings/24.jsonl` (180 formula,
  6,505 drafted), all `drafted`, `source: ocr`; 15 shards, one agent each, the OCR-book prompt of vols. 22–23. 2,539 rows flagged
  (`24-flags.tsv`), 3,611 lines of what the drafts left out (`24-omitted.tsv`), 520 terms kept in Pāḷi (`24-terms.tsv`); 403 of the
  book's 7,088 articles have no Meaning. About and README list vol. 24. Meaning rows in all: **184,649, 83.5% of the index, none
  reviewed**.
- NEXT-SESSION: 00q and 00r done (0.20.0 checked live); 1b and 1c updated for vol. 24.

## v0.20.0 — 28 Sep 2026

- **Vol. 22's Meaning boxes drafted from our OCR** (brief §57): 7,613 rows in `docs/translation/meanings/22.jsonl` (160 formula,
  7,453 drafted), all `drafted`, `source: ocr`; 17 shards, one agent each, the OCR-book prompt of vol. 23. 2,799 rows flagged
  (`22-flags.tsv`), 5,073 lines of what the drafts left out (`22-omitted.tsv`), 773 terms kept in Pāḷi (`22-terms.tsv`); 465 of the
  book's 8,078 articles have no Meaning (no body, nothing left after `prep`, or nothing translatable). About and README list vol. 22.
  Meaning rows in all: **177,964, 80.5% of the index, none reviewed**.
- NEXT-SESSION 1b and 1c: vol. 22 done; its review questions added for the final revision.

## v0.19.1 — 28 Sep 2026

- **Search: the typed word first.** In Browse's header search and the Volumes page search, matches that begin with a roman
  query are ordered by closeness to what was typed: the word itself (ignoring diacritics) first, then long vowels typed
  short (cost 1), then consonants typed without their mark, ṅ ñ ṭ ḍ ṇ ḷ ṁ (cost 2); dictionary order within each. So "na"
  gives na, nā, then ṅa, ña, ṇa, where ṅ and ñ used to come first. Burmese queries unchanged (`common.js` `dmiss()`,
  `browse.js` `search()`). No data changed.

## v0.19.0 — 28 Sep 2026

- **Vol. 23's Meaning boxes drafted from our OCR** (brief §56): 6,906 rows in `docs/translation/meanings/23.jsonl` (206 formula,
  6,700 drafted), all `drafted`, `source: ocr`, the first book drafted from the scanned pages' OCR; 15 shards (shard 00 is §55's
  trial). 2,033 rows flagged (`23-flags.tsv`), 3,873 lines of what the drafts left out (`23-omitted.tsv`), 595 terms kept in Pāḷi
  (`23-terms.tsv`). About and README list vol. 23. Meaning rows in all: **170,351, 77.0% of the index, none reviewed**.
- NEXT-SESSION 1c: the review questions of the OCR drafts, for the final revision.

## v0.18.5 — 28 Sep 2026

- `tools/abhidhana_meanings.py prep`, books drafted from our OCR (`source: ocr`: 14/3, 20–25, 4/3): where a damaged analysis
  bracket's part up to the first `]` holds Burmese gloss words, only the analysis formulas in it (Pāḷi elements joined by +)
  are left out and the `]` becomes ။; before, the whole part went, and with it the gloss where the `]` was scan noise or a
  later bracket (vol. 23: 64 rows' text changed, vol. 22: 241). 14/2 and the PCED books unchanged (byte-identical `prep`
  output). No published data changed.
- **The OCR pilot** (brief §55): vols. 23 and 22 prepared from our OCR; vol. 23 shard 00 (451 rows) drafted as a trial, not
  merged (`docs/translation/trial/23-shard00-{in,out}.jsonl`, the prompt as given in `23-shard00-prompt.md`): 137 flagged,
  270 with `omitted`, 10 empty. Meaning rows in all unchanged: 163,445, none reviewed.
- NEXT-SESSION: 00o done (0.18.3 checked live), v0.18.4 noted (00p).

## v0.18.4 — 28 Sep 2026

- **Vol. 4/3: article step re-run** (`abhidhana_articles.py 4c`, `abhidhana_romanise.py 4c`) with the three analyses corrected
  in editor mode and exported in v0.18.2 (176136 omakapatta, 176140 omakasatta, 176144 omakkhi): each now carries the corrected
  analysis and is marked `corrected`. No other data changed by intent.

## v0.18.3 — 28 Sep 2026

- **Vol. 14/2: 497 Meaning rows redrafted** (brief §54): the rows whose Burmese now begins with the body's restored first
  words (brief §50, `docs/translation/meanings/14b-redraft.tsv`), drafted again in two shards and merged over the old rows;
  all still `drafted`. No other row changed. Flags 1,406 → 1,128 (the old ones mostly noted the lost first word), omitted
  lines 1,165 → 1,172, terms 571 → 572. Meaning rows in all: 163,445, none reviewed.
- `tools/abhidhana_meanings.py`: `prep` / `merge` take `--ids FILE` (draft and merge only those ids over the existing rows),
  `--shards N` and `--work DIR`.
- Brief §53 corrected: the weekly export workflow was added in v0.18.1 and its first run opened PR #33 (v0.18.2).

## v0.18.2 — 2026-09-28

- **Edits from editor mode exported** (weekly workflow): 0 Meaning row(s), 3 correction(s) to `docs/corrections.tsv`, 0 line(s) to `corrections-es.tsv`. Books and fields: 4c: analysis. Article step still to re-run on the Mac for: 4c.

## v0.18.1 — 28 Sep 2026

- **Weekly export of the editor's edits** (`.github/workflows/export-edits.yml`, `docs/editor-mode.md` §5): every Monday
  at 10:00 UTC (04:00 in Mexico City), and on demand from the Actions tab, GitHub reads `/api/edits?book=all`, runs
  `tools/abhidhana_edits_export.py --api --write --summary`, and if any file changed bumps the patch, adds a CHANGELOG
  section and opens a pull request on `edits/YYYY-MM-DD` listing the books whose article step must be re-run on the Mac.
  No change, no PR. Written in a Cowork chat (the cloud session's permission check had refused the file); its version
  and changelog step tested on a scratch copy, the export itself not yet run on GitHub. No data changed.

## v0.18.0 — 28 Sep 2026

- **Roman input in the editor's form** (brief §53, `docs/editor-mode.md` §3): the headword, label and analysis each have a
  switch *Birmano / Latín*; in *Latín* they are typed in IAST and converted to Burmese script by `ROMAN.burmese`
  (`site/src/assets/roman.js`, a port of Aksharamukha's IAST → Burmese; it agrees with Aksharamukha on 256,123 of 256,203
  distinct words, the 80 others being ဂြ + ā, written short as the dictionary prints it). The form shows, for each of the
  three fields, the Burmese to be stored and its roman read-back; a save needs the read-back to equal what was typed. The
  Burmese is stored, as before. The mode is remembered per field in the browser.
- **Round trip measured** (`site/test/roman/roundtrip.js`): headwords 220,623 of 221,154 (99.76%), PCED analyses without
  a derivation 139,759 of 140,281 (99.63%); the failures are malformed OCR, Burmese prose, stray characters and the tall ā.
  Browser tests `ui-test.js` 48/48 (20 new), `api-test.js` 28/28.
- `tools/abhidhana_edits_export.py`: `--summary FILE` (what changed, as JSON) and a User-Agent on `--api`. No data changed.

## v0.17.0 — 27 Sep 2026

- **Editor mode** (brief §52, `docs/editor-mode.md`): in Browse, when the editor is signed in, each article has an
  **Editar** button with a form for the Meaning (ES/EN, the status of the Spanish, whole or by sense) and the article's
  fields (headword, label, analysis, body, in Burmese, with a live roman preview). Saves go to a Cloudflare D1 database
  through Pages Functions (`functions/`); `/edit/` and `/api/admin/` are for Cloudflare Access, and the write API checks
  the Access token itself. Every edit is kept; the latest per id + field + sense counts.
- **Every visitor's Browse lays the saved edits over the published data** (`/api/edits?book=NN`), marked *corregido* /
  *revisado* (or *en parte*, by sense), with the date; if the API fails, the page shows the published data.
- `tools/abhidhana_edits_export.py` writes the edits into `docs/translation/meanings/NN.jsonl`, `corrections-es.tsv` and
  `docs/corrections.tsv`, and lists the books whose article step must be re-run on the Mac.
- The build now writes a "véase" link to a word that is not a headword as `[[x|]]` (still shown in italics), so the form
  can give back the source text. No data changed. **Not yet switched on**: the dashboard steps of `docs/editor-mode.md` §2.

## v0.16.0 — 27 Sep 2026

- **The editor's decisions of 27 Sep recorded** for new drafts (brief §51): person by the Pāḷi ending; ပယ်, ဖောက်ပြန် by sense;
  -attha *el beneficio de X*; ပရိသတ် *asamblea*; ငရဲ *infierno*; pariveṇa, parikamma, parikkhāra, maṅgala translated; one
  rendering for stacked futures; marica *pimienta negra*; လေ as element *aire* (`stems.tsv`, `glossary.tsv`, `drafting-prompt.md`).
- **Nine Meaning rows corrected** by the editor (`docs/translation/corrections-es.tsv`); three corrected in part, shown on the
  site as *corregido en parte* with the corrected sense named.
- **No re-rendering**: the rows whose draft conflicts with a rule (3,382) are listed for the final revision in
  `docs/translation/revision-queue.tsv`.
- **Vol. 4/3**: ဩ restored at the start of 393 OCR analyses read as သ or သဩ (`analysis_o_restored`); two hand corrections
  (176133, 176134).

## v0.15.0 — 27 Sep 2026

- **The body's first words restored** (brief §50): words printed on the headword's line after the analysis's ] were
  dropped as debris by the article step's noise filter. **6,003 bodies** in 29 books gained them; in books 01–19 only
  where the PCED definition begins with them (4,577 kept, 289 taken out), elsewhere by their shape (1,426; 497 in 14/2).
  No placement, label or analysis changed in any row. Rows gain `body_head_restored` and `body_head_how`. Romanisation
  re-run for all books. Vol. 14/2's 497 affected Meaning rows are listed for a redraft
  (`docs/translation/meanings/14b-redraft.tsv`); their drafts are unchanged for now.

## v0.14.0 — 27 Sep 2026

- **Vol. 14/2 Meaning boxes drafted** from the PDF's own text layer (no PCED): 6,795 rows, all `drafted`, `source` text
  layer; 1,406 flagged (`docs/translation/meanings/14b-flags.tsv`), what the drafts left out in `14b-omitted.tsv`. Drafted so
  far: 163,445 rows in 21 books (73.9% of the index), none reviewed. About and README updated.
- `prep` (books without a join) also strips citations without numbers and dash-joined lists of inflected forms (681 of
  14/2's rows changed); drafts record omissions in a field `omitted`, which `merge` keeps out of the rows. Shard 00, the
  trial, kept as drafted. Brief §49.

## v0.13.1 — 27 Sep 2026

- **`abhidhana_meanings.py prep` for books without a witness join** (14/2, 14/3, 20–25, 4/3): the Burmese comes from our
  text (`articles.jsonl` body), `source` *text layer* for 14/2, *ocr* otherwise; line-end hyphens kept outside Pāḷi and
  dropped inside it; multi-word Pāḷi quotations, citations and reference lists removed; one-word Pāḷi kept. Books with a
  join unchanged (`prep 15` byte-identical on a synthetic witness; to be confirmed on the Mac). Vol. 14/2: 6,804
  explanations in 15 shards. The drafting prompt has a section for books drafted from our own text.
- **Trial shard 00 of vol. 14/2 drafted** (454 rows, 181 flagged), kept apart in `docs/translation/trial/`, not merged.
- **No published data changed**: `meanings/` and the site are as in v0.13.0. Brief §49.

## v0.13.0 — 27 Sep 2026

- **Vols. 15, 16, 17, 18 and 19 Meaning boxes drafted** from PCED: 9,340 + 10,393 + 6,510 + 7,826 + 9,250 rows, all
  `drafted`; 8,695 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 156,650 rows in 20 books (70.8% of
  the index), none reviewed. PCED's vols. 1–19 are now all drafted. About and README updated.
- The drafting prompt is now kept in the repo, `docs/translation/drafting-prompt.md`. Brief §48.

## v0.12.0 — 26 Sep 2026, later still

- **Vols. 10, 11, 12, 13 and 14/1 Meaning boxes drafted** from PCED: 7,353 + 5,662 + 7,020 + 7,279 + 5,219 rows, all
  `drafted`; 3,889 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 113,331 rows in 15 books (51.2% of
  the index), none reviewed. About and README updated. Brief §47.

## v0.11.0 — 26 Sep 2026, later still

- **Vols. 7, 8 and 9 Meaning boxes drafted** from PCED: 6,877 + 6,448 + 6,805 rows (every article with a definition),
  all `drafted`; 683 + 636 + 798 flagged (`docs/translation/meanings/NN-flags.tsv`). Drafted so far: 80,798 rows in
  vols. 1–3, 4/1, 4/2 and 5–9, none reviewed. About and README updated.
- Stems L105 (ဂုဏ် *cualidad / virtud*) and L106 (လူ in the gihi- compounds, *laico*), the editor's. Brief §46.

## v0.10.0 — 26 Sep 2026, later still

- **Vol. 6 Meaning boxes drafted** from PCED: 11,424 rows (every article with a definition but one), all
  `drafted`; 1,154 flagged (`docs/translation/meanings/06-flags.tsv`), 397 terms kept in Pāḷi
  (`06-terms.tsv`). About and README list vols. 1–3, 4/1, 4/2, 5 and 6 as drafted.
- The live site checked after v0.9.0 (printed page numbers, the analysis and its derivation). Brief §45.

## v0.9.0 — 26 Sep 2026, later

- **Vol. 5 Meaning boxes drafted** from PCED: 8,012 rows (every article with a definition but one), all
  `drafted`; 1,275 flagged (`docs/translation/meanings/05-flags.tsv`). Vol. 4/3 deferred (no PCED text).
  Glossary: ကုသိုလ် as merit → *mérito / meritorio*; stems L101–L104 (နတ်, ရဟန်း, ပယ်, ဥတု). Brief §44.
- **The compound analysis split from its derivation** (`tools/abhidhana_romanise.py`): the romanised line
  gives the analyses and, where it is wholly Pāḷi, the derivation (ulūka); a derivation in Burmese stays
  on the Burmese line, shown below it (katvā: [kara + tvā]). 19,871 rows' `analysis_iast` changed, no
  other field.
- **Printed page numbers**: Browse, the page pane, the search list and the page view show the book's
  own page beside the PDF page (`site/volumes.json` `offset`, with vol. 2's and vol. 22's exceptions).
- Labels: (ကြိ၊ဝိ) Spanish without *-tuṁ*. Personal names removed from the repository's docs and data
  (`IEBH` in data columns). Dates of v0.7.0–v0.8.0 and brief §42–43 corrected from 27 to 26 Sep.

## v0.8.0 — 26 Sep 2026

- **Vols. 4/1 and 4/2 Meaning boxes drafted** from PCED: 7,519 and 6,654 rows, all `drafted`; 409 and 872
  flagged. `prep` links more "see X" forms; a `report` step writes the flags and terms lists. Brief §43.
- Site: the IEBH footer with logo, related sites, licences and the version on every page; a back-to-top
  button; "Análisis" without the PCED chip; PCED described as a typed witness on About; citation tooltips
  (work · volume, page); "see X" in the Burmese definition linked; mode bar wording.
- Labels: *sustantivo* → *nombre*; (ကြိ၊ဝိ), (နာမ-ကြိ), (စတုတ္ထန္တ), (တတိယန္တ-ဗျ) corrected and confirmed (the editor).

## v0.7.0 — 26 Sep 2026

- **Vol. 3 Meaning boxes drafted** from PCED: 11,726 rows (372 by formula, 11,354 drafted in 24
  shards), all `drafted`; 1,076 flagged (`docs/translation/meanings/03-flags.tsv`). Brief §42.
- This changelog and `VERSION`.

## v0.6.0 — 26 Sep 2026, night (`5db316f`)

PCED's compound analyses for books 01–19 (155,072 rows); hand corrections (`docs/corrections.tsv`);
kusala = *sano*, akusala = *insano*; Browse fixes (search list, Hide index, romanised printed labels);
`/assets/` links versioned by content hash; **vol. 2 Meaning boxes drafted** (7,189 rows). Brief §40–41.
Commits `cef941c` … `5db316f`.

## v0.5.0 — 26 Sep 2026, early morning (`b7881c4`)

Site redesign: Browse is the home page, `/volumes/`, `/abbreviations/`; **vol. 1 Meaning boxes
drafted** (8,144 rows). Brief §38–39.

## v0.4.0 — 25 Sep 2026, night (`571f566`)

Page images live (25,700 pages in R2), light/dark switch, Introduction page, compound analysis with a
lost `[` (+4,907), citations keep their whole abbreviation, translation batch 1 for review.
Brief §31–37.

## v0.3.0 — 25 Sep 2026, evening (`493b459`)

**All 29 books** digitised: 221,154 index rows, 94.1% located, 88.1% label + body; the public website
and one label table. Brief §28–30.

## v0.2.0 — 25 Sep 2026 (`e2e32b5`)

27 books (the batch of vols. 10–24), the index's page errors applied, the Reader in binary.
Brief §13–27.

## v0.1.0 — 24–25 Sep 2026 (`9d5203d`)

Vol. 1 digitised end to end; tools, runbook, docs; the repository made public. Brief §1–12.
