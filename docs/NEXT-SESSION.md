# Abhidhāna — handover, 24 September 2026

*Volume 1 is done end to end and the project is public at `bthar-mx/tipitaka-abhidhana`.
Read `abhidhana-project-brief.md` first. §10–12 are new and carry every figure; this file
does not repeat them.*

## Every session: connect the folder first

Connect `~/Documents/abhidhana` (now also the git working copy) and `~/Tipitaka/nissaya`
(for `tessdata/`). The OSBCT vocabulary is now also at `ocr/osbct_vocab.txt`, so
`anchor/osbct/` is needed only to rebuild it.

## Where things stand

- **Vol. 1 is done**: 913 pages, 92.0% of 8,150 headwords verbatim, 76.1% in printed order
  column-cut. 80.3% of articles have label + body. See `ocr/01/*-report.md`.
- **Repository `bthar-mx/tipitaka-abhidhana`, public**, created 24 Sep. Pushed from
  `~/Documents/abhidhana` by Angel over SSH (the session has no GitHub credentials; Angel runs
  git and `gh` in his Terminal). PDFs and the db are release `sources-v1`.
- **Publication decided**: no longer blocked on licence (brief §10). Credit everyone named in
  `docs/app-info.html`; the licences are split: MIT for code, CC BY-SA for our additions, and the
  dictionary text is not relicensed.
- **Winston** (Claude Team) may run volumes on his own Mac. `RUNBOOK.md` is written for him:
  run natively in Terminal, claim a volume by its issue, one PR per volume.
  `tools/create_volume_issues.sh` creates the 29 issues once the repo is pushed.

## Next, in order

1. ~~After the push~~ **Done 24 Sep:** pushed (commit 9d5203d); release `sources-v1` has all 31
   assets (29 PDFs, the db, `ocr-01-pages.tar.gz`); issues #1–#29, one per book, #1 (vol. 1)
   closed. `gh` is installed on the Mac, logged in as admin-iebh. Still to do: add Winston to
   bthar-mx and point him at `RUNBOOK.md`; check `myap`'s licence before attaching it.
2. **Done 24 Sep: + signs in the compound analysis** repaired (`normalise_analysis`; 17.7% of
   vol. 1 articles; original kept in `analysis_ocr`). Tool, articles and report are in the folder,
   not yet committed.
3. **Normalise labels** against the closed set in `docs/spanish-method.md` §2. The vol. 1 tail
   (၇), (က), (ကြု), (ထိ), (ပ) is mostly OCR confusions of (ကြိ), (ထီ), (ပု). Build the map from the
   whole of vol. 1, check a sample against the images, then apply it in `abhidhana_articles.py`.
4. **Recover unlocated articles** (13.0% of vol. 1). Try matching the tail of a headword split
   across a line, and use the `page.psm6` text where the column pass lost the headword.
5. **Re-run vol. 25** with `--columns` at its native resolution (check `pdfimages -list`).
6. **Next volumes**: vol. 2 is being run on Angel's Mac (natively, ~45 pages a minute, 72 dpi
   confirmed; first 40 pages 97.1% recall). Then 03, 4a–4c in order, on the Mac natively or on Winston's.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions, each with the check that answers it

- **Does dictionary.sutta.org's Pāḷi-Burmese section contain this dictionary's text?** It is built
  from PCED 1.94. If its Burmese entries are typed text of the Tipiṭaka Pāḷi-Myanmā Abhidhāna (or
  part of it), they are a second witness for every article, far better than OCR. Look up a few vol. 1
  headwords (e.g. accāvadati, p. 300) and compare with the page; check the paligo repo for its data.

- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is explained.
- **Title-page entry counts vs the index** (vol. 4/3: 5,163 vs 5,230). Explain per volume.
- **Pp. 253–254 of vol. 1** have no printed rule and are still weak (4/9, 2/10 in the column
  pass). Look at the image, and try a smaller margin or deskewing.
- **`myap` redistribution:** check Pn Daza's licence before attaching the model to the release.
