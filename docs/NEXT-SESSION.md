# Abhidhāna — handover, 25 September 2026 (after vol. 9)

*Vols. 1–9 (vol. 4 in three parts) are digitised end to end, spot-checked and in the Reader. Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool. Every figure is there. `docs/labels.md` holds the label map, `docs/witness.md` and
`docs/witness-join.md` the typed witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. Angel runs
  git and `gh` in Terminal; the session has no GitHub credentials.
- **Run OCR natively on the Mac** (about 45 pages a minute with `--workers 10`; ~41 while the Cowork
  VM was busy on the same Mac). Check the dpi per book with `pdfimages -list`. After the OCR, run
  `abhidhana_articles.py NN` and then `abhidhana_romanise.py NN`, always in that order; then
  `abhidhana_reader_data.py NN` and `abhidhana_witness_join.py` with every witnessed book.
- **In the Cowork VM, a background job dies when the call returns**, and `pkill -f` with a pattern
  that appears in the command line kills the calling shell. Run the article step for up to four
  books in parallel inside one call (about 55 s a book).
- **The Reader's data are `reader/*.gz.txt`** (gzip, base64), not `.json`: republish those.

## State

| | vols. 1–8 | vol. 9 | vol. 10 |
|---|---|---|---|
| OCR, articles, romanisation | done | done 25 Sep | OCR running (Angel, 25 Sep) |
| reports, spot check, Reader | done | done 25 Sep | — |
| page records in release `sources-v1` | uploaded (07, 08: check) | `release/ocr-09-pages.tar.gz`, to upload | — |
| GitHub issue | close any of #1–#10 still open | #11, close after this commit | open |

`tmp/_to_delete/` holds nine `*.json.gz` files from a first try at the Reader's data; the VM
cannot delete. Delete the folder by hand (`tmp/` is gitignored).

## Next, in order

1. **Vol. 10** (book 10, ဒ – ဒွေဠှကပုစ္ဆာ, 981 PDF pages, 7,366 index headwords), OCR started 25 Sep at
   75 dpi (images 71–75 ppi). Then as for vol. 9. The typed witness covers it.
2. **Re-cut the gutters** with `tools/abhidhana_recut.py` (brief §24), natively, book by book, when
   no OCR is running (it competes for the CPU, not for files):
   `python3 tools/abhidhana_recut.py NN --scan --workers 10`, then `--run --workers 10`. Then
   re-run articles, romanisation, the witness join and the Reader for every book, and compare
   located and label + body before and after. **Vol. 9 p. 823** (a failed reading, brief §23):
   move `ocr/09/pages/p0823.json` aside and re-run `abhidhana_ocr.py 09 ... --first 823 --last 823`
   before that. Afterwards try the `page.psm6` fallback for headwords still unlocated.
3. **Image-check the label disagreements** with the witness (`docs/witness-join.md` §3): a sample
   of (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ). And the vol. 6 readings (ထိန), (ထီ၊၇), (ထိ၊န)
   (`docs/labels.md` §7; ids 51227, 51941, 54340), and vol. 8's (ကာ၊ကမ္မ၊ကြို) (the witness has
   (ကာ၊ကမ္မ၊ကြိ) 43 times), before mapping them.
4. **Angel's review of the labels**: `docs/labels.md` §1, §6 and now §7 (ကာ၊ကြိ၊ဝိ). A Pāḷi expansion
   and a Spanish abbreviation for each.
5. **An index-errata list**, `docs/index-errata.md`, with the printed form: the typos of brief §15–17,
   the misfiled runs of §18 (4c p. 615 → 613, 06 p. 851 → 852), ကဉ္စိက.
6. **Re-run vol. 25** with `--columns` at its native resolution.
7. **Next volumes**: 11 onwards. **Vol. 15** must be joined with 4c's supplement to it (53 ဘိဇ္ဇ
   headwords indexed only there). Per volume: reports, a 3-page spot check, the Reader, the witness
   join, then close the issue.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **Book 21's index runs 65 pages past its PDF** (990 vs 925). Don't run it until this is
  explained; the misfiled runs of brief §18 and the vol. 2 page swap show what such problems look like.
- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **The witness's labels for rows we could not read** (7,002): usable privately; not published
  until its licence is known.
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
- **The Reader needs `DecompressionStream`** (Safari 16.4+, Chrome 80+, Firefox 113+). Say so if someone reports a blank page.
