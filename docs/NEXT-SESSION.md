# Abhidhāna — handover, 25 September 2026, late night (all 29 books done)

*All 29 books are digitised end to end, spot-checked and in the Reader: 221,154 index rows, 94.1%
located, 88.1% with label + body (brief §30). Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool, §25 vol.
14/2's text layer, §26 the batch (vols. 10–22), §27 vols. 23, 24, 14/2, the index's page errors,
book 21 and the Reader in binary, §28 the website, the page images and the label table, §29 vol.
21, vol. 25's resolution and the labels as the dictionary prints them, §30 vol. 25 and the total. Every figure is there.
`docs/labels.md` §0 holds the label table (the one source for the pipeline and the site),
`docs/abbreviations.md` the dictionary's own abbreviations and its prose on the labels,
`docs/index-errata.md` the index's errors, `docs/witness.md` and `docs/witness-join.md` the typed
witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. Angel runs
  git and `gh` in Terminal; the session has no GitHub credentials.
- **Run OCR natively on the Mac** (about 45 pages a minute with `--workers 10`). Check the dpi per
  book with `pdfimages -list`, and **measure a sample before trusting "native"**: vol. 25 read far
  worse at its native 300 than at 200 (brief §29). After the OCR: `abhidhana_articles.py NN`, then
  `abhidhana_romanise.py NN`, always in that order; then `abhidhana_ocr_stats.py NN` for the OCR
  report, `abhidhana_reader_data.py NN [NN ...]`, and the witness joins for books 01–19.
- **In the Cowork VM, a background job dies when the call returns**, and `pkill -f` with a pattern
  that appears in the command line kills the calling shell (the cloud container too). Run the
  article step for up to five books in parallel inside one call (about 45–65 s for five). In a
  fresh VM, `pip install --user aksharamukha python-myanmar pymupdf` first.
- **The Reader's data are `reader/*.wasm`** (gzip bytes, served as application/wasm; gitignored):
  republish them with `reader/index.html` to https://claude.ai/artifact/RjuFxtkh4FASRkhBeYhVS3.
- **Docs in the folder and in the Project must match.** On 25 Sep night the folder's brief and
  NEXT-SESSION twice went back to an older version. The cause was this session: `device_commit_files`
  sent a stale copy when the same staged path under `/mnt/user-data/outputs/` was reused. Give each
  commit a fresh staged file name, and check the folder copy (md5, or its headings) afterwards.

## State

All 29 books: OCR (14/2 from its text layer), articles, romanisation, reports, spot check, Reader.
Page records for `sources-v1`: upload `release/ocr-NN-pages.tar.gz` for 10–25 with 14c. GitHub:
close #29 (vol. 25) and any volume issue still open.

`tmp/_to_delete/` holds nine `*.json.gz` files from a first try at the Reader's data; delete it by
hand (`tmp/` is gitignored). `tmp/ocr-25-pilot-pages/` and `tmp/ocr-25-300dpi/` are the discarded
vol. 25 runs.

## Next, in order

0. ~~Vol. 25 at 200 dpi~~, ~~the README~~, ~~the website~~: done 25–26 Sep. **The site is live** at
   https://abhidhana.buddha-dhamma.net (Angel deployed it; checked 26 Sep in the browser: all 29 books,
   221,154 headwords, search, label pop-ups, About and Labels pages, 404 page). `site/src/_headers` now
   makes browsers revalidate `/data/*` and `/assets/*` on every load; with the old one-hour cache a
   visitor saw vol. 25 as "coming" after it was published.
1. **Page images**: `https://abhidhana-img.buddha-dhamma.net/<book>/<NNNN>.webp` answers 404, so the
   R2 domain is connected but nothing is uploaded yet (the site shows "image not yet available").
   Angel: create the R2 token, then on the Mac `python3 tools/abhidhana_pages_r2.py render 01 --last
   50`, `check 01`, then `all` (renders and uploads every book; ~2.5 GB; resumable). Afterwards open a
   page of each book on the site.
3. **Labels, Angel's to confirm** (`docs/labels.md` §0; `python3 tools/abhidhana_labels.py` checks
   the table after an edit): kammavācaka-kriyā for ကံဟောကြိယာ; sakkata, pākata (and ဗု၊သံ,
   ဗုဒ္ဓဘာသာသက္ကတ, "Buddhist Sanskrit", vol. 2 p. 14); (နာမ-ကြိ) nāmadhātu?; the provisional
   combinations (ပု၊ထီ) (န၊ပု) (န၊ထီ) (ပု၊တိ) (န၊တိ) (တိ၊န) and (ကာ၊ကြိ၊ဝိ), (စတုတ္ထန္တ),
   (တတိယန္တ-ဗျ), (အ-လိင်); all the Spanish meanings (drafts) and the Spanish abbreviations.
   The site's pop-ups and Labels page follow the table on the next build.
3b. **Case and number abbreviations** (ဧ, ဗ, ပ, ဒု, တ, စ, ပဉ္စ, ဆ, သ; `docs/abbreviations.md`) appear
   inside analyses and definitions; the site could explain them the same way. And the **citation
   abbreviations** (vol. 4/1 pp. 31–36, vol. 15 pp. 17–22) are the key for resolving citations
   against OSBCT: transcribe them from the images when that work starts.
4. **Repo size** (brief §28): run `git count-objects -vH` and `git gc` (the objects are loose;
   a pack stores a re-run as deltas). If it still grows fast: stop committing `raw` (articles) and
   `body_joined` (pali), which repeat other fields (~40%), and keep them in a release tarball;
   only past ~1 GB move `articles.jsonl` / `pali.jsonl` to release assets, with the site build
   downloading them.
5. **Weak `ID_PAGE_FIX` candidates**, on the image: 14/3 pp. 605 (198069–198070) and 976
   (201781–201786), 18 p. 815 (146728–146731), 10 p. 219 (81975–81976); and 14/3 pp. 564, 607, 620.
6. **Re-cut the gutters** with `tools/abhidhana_recut.py` (brief §24), natively, book by book, when
   no OCR is running: `python3 tools/abhidhana_recut.py NN --scan --workers 10`, then `--run
   --workers 10`. Then re-run articles, romanisation, the witness joins and the Reader for every
   book, and compare. Vol. 24 has 15 pages with a gutter ≥ 0.54 (column recall 80.8%). **Vol. 9
   p. 823** (brief §23): move `ocr/09/pages/p0823.json` aside and re-run it before that. Afterwards
   try the `page.psm6` fallback for headwords still unlocated.
7. **Why is compound analysis low in vols. 23 and 14/3** (59%) against ~72–81% elsewhere? Look at a
   page's [ ] in the text.
8. **Image-check the label disagreements** with the witness (`docs/witness-join.md` §3): a sample
   of (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ). And (ထိန), (ထီ၊၇), (ထိ၊န) (`docs/labels.md` §7; ids
   51227, 51941, 54340; vol. 24 has (ထီ၊ ၇) 17 and (ထိ၊ န) 11 unnormalised) before mapping them.
9. **Vol. 15** must be joined with 4c's supplement to it (53 ဘိဇ္ဇ headwords indexed only there).
10. **Vol. 13's sixteen pages of vol. 15 headwords** (`docs/index-errata.md` §2): their real
   headwords can only come from our OCR; a later task.

Don't translate at scale. Flag uncertainty rather than guessing.

## Open questions

- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **The witness's labels for rows we could not read** (7,002): usable privately; not published
  until its licence is known.
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
- **The Reader needs `DecompressionStream`** (Safari 16.4+, Chrome 80+, Firefox 113+). Say so if someone reports a blank page.
