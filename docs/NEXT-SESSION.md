# Abhidhāna — handover, 24 September 2026

*Volume 1 is done end to end and the project is public at `bthar-mx/tipitaka-abhidhana`.
Read `abhidhana-project-brief.md` first. §10–12 carry every figure; this file does not repeat
them.*

## Every session: connect the folder first

Connect `~/Documents/abhidhana` (now also the git working copy) and `~/Tipitaka/nissaya`
(for `tessdata/`). The OSBCT vocabulary is now also at `ocr/osbct_vocab.txt`, so
`anchor/osbct/` is needed only to rebuild it. Don't run `git` from the Cowork VM: it leaves an
`index.lock` it cannot delete. Angel runs git in Terminal.

## Where things stand

- **Vol. 1 is done**: 913 pages, 92.0% of 8,150 headwords verbatim, 76.1% in printed order
  column-cut. **93.8% of articles located, 87.3% have a normalised label + body** (24 Sep, after
  items 3–4). See `ocr/01/*-report.md` and `docs/labels.md`.
- **Repository `bthar-mx/tipitaka-abhidhana`, public**, created 24 Sep. Pushed from
  `~/Documents/abhidhana` by Angel over SSH (the session has no GitHub credentials; Angel runs
  git and `gh` in his Terminal). PDFs and the db are release `sources-v1`.
- **Publication decided**: no longer blocked on licence (brief §10). Credit everyone named in
  `docs/app-info.html`; the licences are split: MIT for code, CC BY-SA for our additions, and the
  dictionary text is not relicensed.
- **Winston** (Claude Team) may run volumes on his own Mac. `RUNBOOK.md` is written for him:
  run natively in Terminal, claim a volume by its issue, one PR per volume.

## Next, in order

1. **Done 24 Sep:** pushed; release `sources-v1` has all 31 assets; issues #1–#29, one per book,
   #1 closed. Still to do: add Winston to bthar-mx and point him at `RUNBOOK.md`; check `myap`'s
   licence before attaching it.
2. **Done 24 Sep: + signs in the compound analysis** repaired (`normalise_analysis`; original kept
   in `analysis_ocr`).
2b. **Done 24 Sep: all the Pāḷi in vol. 1 romanised**: `tools/abhidhana_romanise.py 01` →
   `ocr/01/pali.jsonl` and `pali-report.md`. It reads `articles.jsonl`, so **re-run it after every
   regeneration of `articles.jsonl`**.
2c. **Reader page** (private artifact "Abhidhāna Reader", claude.ai/artifact/RjuFxtkh4FASRkhBeYhVS3):
   browse vol. 1 by page, search headwords, Pāḷi shown in roman, labels normalised (hover shows
   the OCR reading). The page source is `reader/index.html`, and `vol01.json` is built by
   `tools/abhidhana_reader_data.py 01` (gitignored). To update it, read the artifact with the
   Artifact tool and republish both files to that URL. The page is vol.-1 specific: adding vol. 2
   means a volume switch.
3. **Done 24 Sep: labels normalised.** There are 125 OCR readings, mapped to 19 printed labels
   (`label`, with `label_ocr` and `label_how`). The map and its image checks are in
   `docs/labels.md`. A blind check of 32 rows against the images found 30 right, and both errors
   were fixed. **98.5% agree with the typed witness** (3b), against 81.3% for the raw readings.
   `spanish-method.md` §2 lists 5 labels, and vol. 1 prints 19. The Pāḷi expansions and Spanish
   abbreviations of the new ones (ကြိ၊ဝိ, ဗျ, ကာ၊ကြိ, …) are **Angel's decision**: they are listed
   in `docs/labels.md` §1.
3b. **Found 24 Sep: a typed copy of this dictionary.** PCED 1.94's data (public repo `siongui/data`,
   `dictionary/dict_words_{1,2}.csv`, dictionary id `K`, "Tipiṭaka Pāḷi-Myanmar Dictionary") has
   157,271 entries in **Zawgyi** and covers 94.7% of vol. 1's headwords. It gives the label,
   analysis and definition as printed (p. 300 accāvadati checked), but it seems to omit the Pāḷi
   quotations and citations. See `docs/labels.md` §4. **Next:** convert it to Unicode (a
   Zawgyi→Unicode converter, checked on a sample) and use it as the second witness for analysis
   and definition. Where it has the entry, it could replace OCR for the definition text, while OCR
   keeps the quotations. It stays a second witness: the index and the page are the authorities.
   Check its provenance before publishing text derived from it.
4. **Done 24 Sep: unlocated articles 13.0% → 6.2%.** The headwords the verbatim pass leaves are
   aligned in order to the article starts between their placed neighbours (similarity ≥ 0.70), and
   hyphen-split headwords are joined. A sample checked against the images found 36 of 38 right.
   Still open: the `page.psm6` fallback for headwords the column pass lost.
5. **Vol. 2**: OCR running on Angel's Mac (natively, ~45 pages a minute, 72 dpi). Then Angel runs
   `abhidhana_articles.py 02` and `abhidhana_romanise.py 02`. After that: write vol. 2's reports,
   re-run the label census for readings the map doesn't know (foot of `articles-report.md`), and
   add vol. 2 to the Reader.
6. **Re-run vol. 25** with `--columns` at its native resolution (check `pdfimages -list`).
7. **Next volumes**: 03, 4a–4c in order, on the Mac natively or on Winston's.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions, each with the check that answers it

- ~~Does dictionary.sutta.org contain this dictionary's text?~~ **Yes** (3b). Still open: does it
  cover every volume evenly, and how do its 157,271 entries relate to the index's 215,447 headwords?
- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is explained.
- **Title-page entry counts vs the index** (vol. 4/3: 5,163 vs 5,230). Explain per volume.
- **Pp. 253–254 of vol. 1** have no printed rule and are still weak. Look at the image, and try a
  smaller margin or deskewing.
- **`myap` redistribution:** check Pn Daza's licence before attaching the model to the release.
