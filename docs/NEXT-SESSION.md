# Abhidhāna — handover, 25 September 2026

*Vols. 1–3 are digitised end to end, spot-checked and in the Reader. Read `abhidhana-project-brief.md` first: §12 covers vol. 1
and §13 vols. 2–3, and every figure is there. `docs/labels.md` holds the label map and the typed
witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. Angel runs
  git and `gh` in Terminal; the session has no GitHub credentials.
- **Run OCR natively on the Mac** (about 45 pages a minute with `--workers 10`). Check the dpi per
  book with `pdfimages -list`. After the OCR, run `abhidhana_articles.py NN` and then
  `abhidhana_romanise.py NN`, always in that order.

## State

| | vol. 1 | vol. 2 | vol. 3 | vol. 4a |
|---|---|---|---|---|
| OCR, articles, romanisation | done | done | done | OCR started 25 Sep on the Mac (96 dpi native) |
| reports (`ocr-report`, `articles-report`, `pali-report`) | done | done | done | — |
| image spot check | done (38 placements, 32 labels) | done (pp. 500, 241–242, 115) | done 25 Sep (pp. 600, 654, 1008) | — |
| in the Reader | yes | yes, 25 Sep | yes, 25 Sep | — |
| page records in the release | `ocr-01-pages.tar.gz` | `release/ocr-02-pages.tar.gz`, to upload if not yet | `release/ocr-03-pages.tar.gz`, to upload if not yet | — |
| GitHub issue | #1 closed | #2: close (committed in `83cf739`) | #3: close after this session's commit | open when the OCR is done |

Vols. 1–3 were committed and pushed in `83cf739`. This session (25 Sep) changed
`ocr/03/articles-report.md` (the spot checks), `reader/index.html` (the volume switch) and the brief
and this file. The Reader's data files (`reader/vol0N.json`) are gitignored; the artifact now holds
all three, vol. 1 regenerated from the current `articles.jsonl` (94.1% located).

**Vol. 3 spot check, in short**: 30 of 31 headwords at the right entry, none wrong, 1 unlocated (a
variant twin); no label wrong, 2 not read. P. 654's 0 of 4 is the index writing ါ where the print
has ာ after a stacked consonant, not an OCR failure. Details in `ocr/03/articles-report.md`.

## Next, in order

1. **Vol. 4a**: when Angel's OCR run finishes, `abhidhana_articles.py 4a` and then
   `abhidhana_romanise.py 4a`; the reports; a 3-page spot check; add `4a` to `VOLS` in
   `reader/index.html` (id, Burmese and roman range from `books.name_info`, a default page) and build
   `vol4a.json`; republish (read the artifact and each published json first).
2. **Fold ါ/ာ after a stacked consonant** when matching headwords (`abhidhana_ocr.py` scoring and
   `abhidhana_articles.py`). Measured: it would recover 1, 6 and 26 of the missed headwords in vols. 1–3.
3. **The typed witness.** PCED 1.94's "Tipiṭaka Pāḷi-Myanmar Dictionary" (public repo
   `siongui/data`, `dictionary/dict_words_{1,2}.csv`, dictionary id `K`, 157,271 entries, **Zawgyi**)
   has 94.5–96.0% of each volume's headwords. The plan:
   a. Convert it to Unicode with a Zawgyi→Unicode converter. Check the conversion on ~20 entries
      against the page images.
   b. Store it as `witness/pced_k.jsonl` (headword, label, analysis, definition), keyed by the
      romanised headword. Check its provenance and licence before publishing anything derived.
   c. Use it per article, as a second witness: flag labels and analyses that disagree; offer the
      typed definition beside the OCR one in the Reader; and keep the OCR for the Pāḷi quotations
      and citations, which the witness appears to omit.
   d. The index stays the authority for headwords, and the page for everything else.
4. **Angel's review of the new labels**: `docs/labels.md` §1 and §6. There is a Pāḷi expansion and a
   Spanish abbreviation for each (ကြိ၊ဝိ, ဗျ, ကာ၊ကြိ, ကမ္မ၊ကြိ, …).
5. **Re-run vol. 25** with `--columns` at its native resolution.
6. **Next volumes**: 4b, 4c, then 05 onwards, on the Mac natively or on Winston's.
   Per volume: reports, a 3-page spot check, the Reader, then close the issue.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **The `page.psm6` fallback** for headwords the column pass lost is still not tried (5.4–6.5% of
  articles remain unlocated).
- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is
  explained; the vol. 2 page swap is a hint of what such problems look like.
- **Title-page entry counts vs the index** (vol. 4/3: 5,163 vs 5,230). Explain per volume.
- **The witness's coverage**: 157,271 entries against the index's 215,447 headwords. Which
  volumes, and which headwords, does it lack?
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
