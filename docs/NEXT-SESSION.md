# Abhidhāna — handover, 24 September 2026 (end of day)

*Vols. 1–3 are digitised end to end. Read `abhidhana-project-brief.md` first: §12 covers vol. 1
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

| | vol. 1 | vol. 2 | vol. 3 |
|---|---|---|---|
| OCR, articles, romanisation | done, committed | done | done |
| reports (`ocr-report`, `articles-report`, `pali-report`) | done | done | done |
| image spot check | done (38 placements, 32 labels) | done (pp. 500, 241–242, 115) | **not done** |
| in the Reader | yes | **no** | **no** |
| page records in the release | `ocr-01-pages.tar.gz` | `release/ocr-02-pages.tar.gz`, to upload | `release/ocr-03-pages.tar.gz`, to upload |
| GitHub issue | #1 closed | #2: close after the commit | #3: keep open until the spot check and the Reader |

`abhidhana_articles.py` changed today. Vol. 1 was regenerated with it (94.1% located), so vol. 1's
files change in the next commit too. What changed: the vol. 2 page-order fix (`PAGE_FIX`);
spelling-variant entries (`variant_of`); unindexed pages read into their article (`runs_through`);
debris removed before the compound analysis is read; the bracket-damaged analysis fallback;
running heads with debris above them; and the new labels (ကမ္မ၊ကြိ, ထီ၊န, ထီ၊ပု, အ-လိင်).

## Next, in order

1. **Spot-check vol. 3** against `03.pdf`: an ordinary page, the worst page (p. 654, 0 of 4), and
   one of pp. 1007–1009.
2. **Reader: add vols. 2–3 with a volume switch.** Build `reader/vol02.json` and `vol03.json` with
   `tools/abhidhana_reader_data.py NN` (gitignored). Change `reader/index.html` so it loads
   `vol{NN}.json` from a volume selector: today it is vol.-1 specific (title, the "a – anīḷaka"
   range, the default page 300, the footer links). Republish to
   claude.ai/artifact/RjuFxtkh4FASRkhBeYhVS3: read it with the Artifact tool first, then publish
   all three json files beside the page.
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
6. **Next volumes**: 4a, 4b, 4c, then 05 onwards, on the Mac natively or on Winston's.
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
