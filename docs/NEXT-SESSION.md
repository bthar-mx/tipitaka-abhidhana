# Abhidhāna — handover, 27 September 2026 (vol. 3 Meaning boxes drafted; version numbers proposed)

*All 29 books are digitised end to end, spot-checked and in the Reader: 221,154 index rows, 94.1%
located, 88.1% with label + body (brief §30). Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool, §25 vol.
14/2's text layer, §26 the batch (vols. 10–22), §27 vols. 23, 24, 14/2, the index's page errors,
book 21 and the Reader in binary, §28 the website, the page images and the label table, §29 vol.
21, vol. 25's resolution and the labels as the dictionary prints them, §30 vol. 25 and the total, §31–37 the page images, the Introduction and the stem lexicon, §38 the site redesign, §39 the vol. 1 drafts, §40 the site fixes, the PCED analyses, hand corrections and sano / insano, §41 versioned assets and vol. 2's drafts, §42 the live check after `5db316f`, vol. 3's drafts and version numbers. Every figure is there.
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

00. **Versions** (brief §42, `CHANGELOG.md`): confirm the scheme; if yes, Angel creates the tags v0.1.0–v0.6.0 on
   the commits listed there and v0.7.0 on this push; `VERSION` holds the current number. Then show it in the site footer.
00b. ~~Check the live site after `5db316f`~~: done 27 Sep (brief §42).

0. ~~Vol. 25 at 200 dpi~~, ~~the README~~, ~~the website~~: done 25–26 Sep. **The site is live** at
   https://abhidhana.buddha-dhamma.net (Angel deployed it; checked 26 Sep in the browser: all 29 books,
   221,154 headwords, search, label pop-ups, About and Labels pages, 404 page). `site/src/_headers` now
   makes browsers revalidate `/data/*` and `/assets/*` on every load; with the old one-hour cache a
   visitor saw vol. 25 as "coming" after it was published.
1. ~~Page images~~: all 29 books live, 25,700 pages, 2.5 GB; `check` clean (brief §35).
0b. ~~**Push the 26 Sep night work** (brief §40)~~ (pushed as `5db316f`; the §42 check covered the Meaning box,
   (ti) labels, PCED and "corrected" marks, versioned assets). Still to look at on the live site: the search list, Hide index
   (`\`), the ES/EN switch at ~1,000 px, the alphabet in roman mode, the About credits. (`tmp/sitetest/`, the test tarballs,
   was deleted by Angel on 26 Sep.) The Reader artifact is not republished with the new analyses
   (`abhidhana_reader_data.py` for all books, then republish).
0c. **Hand corrections** go in `docs/corrections.tsv` (brief §40); re-run `abhidhana_articles.py NN` and
   `abhidhana_romanise.py NN`. Confirm the `roman` column of `docs/labels.md` §0.
1b. **Translation** (brief §37, §39–42). **Vols. 2 and 3 drafted** (7,189 rows, 517 flagged; 11,726 rows, 1,076 flagged:
   `meanings/0N-flags.tsv`). Next: vol. 4/1 (book 4a), `prep 4a` (working files in `tmp/meanings/`, gitignored; move the
   previous volume's `shards/`, `out/`, `workNN.json` to `tmp/meanings/vNN/` first, as for v02 and v03), ~24 shards of
   ~470 lines (`prep('4a', 24)` from Python), one agent and one scratch folder each (at most 20 at once), then `merge 4a`
   and the flags/terms TSVs (brief §42 says how they were made; the script is not in the tool yet). Source: **PCED** (Angel, 26 Sep). kusala = *sano*, akusala =
   *insano* (`docs/translation/glossary.tsv`); the other batch-1 stems are not yet reviewed. Six vol. 1
   rows have no draft (ids 21, 2190, 3938, 3988, 5435, 7881); row 2767 needs its Burmese tree names. Vol. 1's Meaning boxes are filled with **drafts**: 8,144 rows in
   `docs/translation/meanings/01.jsonl`, all `drafted`. Waiting for Angel:
   - the batch 1 stems (`docs/translation/batch01-review.md`);
   - further doctrinal terms for `glossary.tsv` (no IEBH doctrinal glossary was found; the one lead,
     `~/Tipitaka/nissaya/anchor/glosario-data.json`, is grammatical and names `comun/glosario.md`
     in another repo);
   - a look at the flagged rows (`meanings/01-flags.tsv`, 816) and the kept Pāḷi terms
     (`meanings/01-terms.tsv`, 555).

   Once stems are approved, re-render the rows that use them. The next volumes follow the same path:
   `python3 tools/abhidhana_meanings.py prep NN`, draft the shards per `docs/translation/drafting-brief.md`
   (give each drafting agent its **own** scratch folder: shared helper scripts crossed shards in vol. 1),
   then `merge NN`.
2a. ~~Site redesign~~: built 26 Sep (brief §38). After Angel's push, check the live site. Browse is
   the home page; `/volumes/` and `/abbreviations/` are new; run `git rm -r site/src/labels`.
2. **The Introduction page** (brief §35) rebuilds itself from `docs/introduction/` on every push; keep the
   chapter files to the contract in `tools/abhidhana_intro.py`'s docstring. It shows drafts under a banner,
   while the About page's History waits for review (item 7c): decide whether ch. 4's names should wait too.
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
5. ~~Weak `ID_PAGE_FIX` candidates~~: done 25 Sep (brief §32): four 14/3 runs and vol. 10's ဒသ² applied,
   vol. 18's rejected (the index is right). The Reader artifact is **not yet republished** with vols. 10
   and 14/3's new data (`reader/vol10.wasm`, `vol14c.wasm`, `search.wasm`); the website follows on push.
5b. **Homonyms paired one entry late, the converse of §18** (brief §32): 177 runs where an earlier
   identical headword is unplaced and a later one placed on the same page (vol. 10 p. 220: 81977–81978
   hold ဒသ³⁻⁴). Sort them with the witness joins for books 01–19 (a placed row whose body ratio
   against its own witness row is low but high against the next one's), on the image elsewhere; then
   a rule in `abhidhana_articles.py`, tested so that it moves nothing already right.
6. **Re-cut the gutters** with `tools/abhidhana_recut.py` (brief §24), natively, book by book, when
   no OCR is running: `python3 tools/abhidhana_recut.py NN --scan --workers 10`, then `--run
   --workers 10`. Then re-run articles, romanisation, the witness joins and the Reader for every
   book, and compare. Vol. 24 has 15 pages with a gutter ≥ 0.54 (column recall 80.8%). **Vol. 9
   p. 823** (brief §23): move `ocr/09/pages/p0823.json` aside and re-run it before that. Afterwards
   try the `page.psm6` fallback for headwords still unlocated.
7. ~~Why is compound analysis low in vols. 23 and 14/3~~: done 25 Sep for vol. 23 (brief §33: a lost
   opening bracket; all books re-run, analysis 75.0 → 77.2%, witness agreement of the gains 97.2%).
7b. **14/3's analysis** (60.0%): its `+` signs are lost and its `]` read as ု/ျု/ါ. Try delimiting the
   analysis by the headword (the elements spell it out, sandhi aside), test on books 01–19 against
   the witness, and image-check a 14/3 page before keeping it.
7c. **History on the About page** (brief §34): review the romanised names in `docs/history.md` (and
   its open points: vol. 25's era year, vol. 4's compiler, vol. 14's), then change its status line to
   `<!-- site: publish -->`. The Project description and instructions still credit the Masoeyein
   board with the whole dictionary.
8. **Image-check the label disagreements** with the witness (`docs/witness-join.md` §3): a sample
   of (တိ)/(gender), (ပု)/(ပု၊န), (ကြိ)/(တိ). And (ထိန), (ထီ၊၇), (ထိ၊န) (`docs/labels.md` §7; ids
   51227, 51941, 54340; vol. 24 has (ထီ၊ ၇) 17 and (ထိ၊ န) 11 unnormalised) before mapping them.
9. **Vol. 15** must be joined with 4c's supplement to it (53 ဘိဇ္ဇ headwords indexed only there).
10. **Vol. 13's sixteen pages of vol. 15 headwords** (`docs/index-errata.md` §2): their real
   headwords can only come from our OCR; a later task.

Translate volume by volume only as drafts, never presented as readings. Flag uncertainty rather than guessing.

## Open questions

- **Title-page entry counts vs the index**: vol. 4/3 prints 5,163; the index has 5,007 for 4/3 itself
  and 223 for the supplements bound after it. Neither matches. Read the title page again; explain per volume.
- **The witness's labels for rows we could not read** (7,002): usable privately; not published
  until its licence is known.
- **Body text of a head placed by its superscript** starts with the debris (ာါ, ဝ်): cosmetic, not yet stripped.
- **The last 160 pages of 4a** are worn print. `pdfs-drive/` has another copy of vol. 4/1; compare a page before re-OCRing.
- **`myap` redistribution**: check Pn Daza's licence before attaching the model to the release.
- **The Reader needs `DecompressionStream`** (Safari 16.4+, Chrome 80+, Firefox 113+). Say so if someone reports a blank page.
