# Abhidhāna — handover, 28 September 2026 (editor mode built, not yet switched on, v0.17.0; roman input in its form, v0.18.0; 14/2's 497 rows redrafted, v0.18.3; the OCR pilot, v0.18.5; vol. 23 drafted from our OCR, v0.19.0; vol. 22 drafted from our OCR, v0.20.0; vol. 24, v0.21.0; vol. 21, v0.22.0)

*All 29 books are digitised end to end, spot-checked and in the Reader: 221,154 index rows, 94.1%
located, 88.1% with label + body (brief §30). Read
`abhidhana-project-brief.md` first: §12 covers vol. 1, §13 vols. 2–3, §14–17 the witness and vols.
4/1–5, §18 the spelling folds and the homonym and misfiled-headword fixes, §19 the witness join, §20
vol. 6, §21 vol. 7, §22 vol. 8 and the gutter failures, §23 vol. 9, §24 the re-cut tool, §25 vol.
14/2's text layer, §26 the batch (vols. 10–22), §27 vols. 23, 24, 14/2, the index's page errors,
book 21 and the Reader in binary, §28 the website, the page images and the label table, §29 vol.
21, vol. 25's resolution and the labels as the dictionary prints them, §30 vol. 25 and the total, §31–37 the page images, the Introduction and the stem lexicon, §38 the site redesign, §39 the vol. 1 drafts, §40 the site fixes, the PCED analyses, hand corrections and sano / insano, §41 versioned assets and vol. 2's drafts, §42 the live check after `5db316f`, vol. 3's drafts and version numbers, §43 vols. 4/1–4/2, the IEBH footer, citation tooltips, cross-reference links and the labels the editor reviewed, §44 the live check after v0.8.0, vol. 4/3 deferred, vol. 5's drafts, the analysis split from its derivation and printed page numbers, §45 the live check after v0.9.0 and vol. 6's drafts, §46 stems L105–L106 and vols. 7–9, §47 vols. 10–14/1, §48 the live check after v0.12.0 and vols. 15–19, §49 vol. 14/2 from its text layer, §50 the body's first words restored, §51 the editor's decisions of 27 Sep and the revision queue, §52 editor mode, §53 roman input in the editor's form, §54 the redraft of 14/2's 497 rows with restored first words, §55 the OCR pilot (vols. 23 and 22 prepared, `prep`'s gloss fix for OCR books, vol. 23 shard 00 drafted), §56 vol. 23 drafted and merged, §57 vol. 22 drafted and merged (in Cowork), §58 vol. 24 likewise, §59 vol. 21 likewise. Every figure is there.
`docs/labels.md` §0 holds the label table (the one source for the pipeline and the site),
`docs/abbreviations.md` the dictionary's own abbreviations and its prose on the labels,
`docs/index-errata.md` the index's errors, `docs/witness.md` and `docs/witness-join.md` the typed
witness.*

## Every session

- Connect `~/Documents/abhidhana` (the git working copy of the public repo
  `bthar-mx/tipitaka-abhidhana`) and `~/Tipitaka/nissaya` (for `tessdata/`).
- **Don't run `git` from the Cowork VM**: it leaves an `index.lock` it cannot delete. The editor runs
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

## Now: the editor moves the heavy work to Claude Code in the cloud (27 Sep)

The editor has a **$250 credit for Claude Code cloud sessions** (expires 5 Nov 2026) and will use it, from the
**Claude desktop app with Cloud selected** (or claude.ai/code), for the token-heavy work; Cowork chats in this
Project are for advice and for what needs the Mac. What the new chat should know:

- **Push first.** v0.13.0 (brief §48) is ready but not yet pushed; `CLAUDE.md` at the repo root is new (the
  project's rules for Claude Code: read the brief and this file first, no personal names, VERSION + CHANGELOG
  on every push, leave `.gitignore`, flag uncertainty) and goes into the same commit. A cloud session sees only
  what is pushed to `bthar-mx/tipitaka-abhidhana`.
- **How the loop works.** The cloud session clones the repo, works on a branch, the editor reviews its diff,
  chooses **Create PR**, merges on github.com, then pulls into `~/Documents/abhidhana` (VS Code's Source
  Control panel or Terminal) and tags the version. Git never runs in the Cowork VM. The cloud has no
  `pdfs/`, `db/`, `witness/`, `tmp/` or OCR models: OCR, the witness joins and the Reader stay on the Mac.
  Anything that runs locally (the VS Code Claude Code extension, a Local session, `claude` in a terminal)
  uses the plan's normal limits, not the credit.
- **First cloud job: vol. 14/2's Meaning boxes (option A), recommended, the editor to confirm.** 14/2 is the
  PDF's typeset text layer, not OCR (brief §25, §27: label + body 97.6%); 6,319 of its 6,942 articles have a
  body. Its body carries the Pāḷi quotations and citations that PCED lacks, so only the Burmese explanation
  is drafted. Steps: change `abhidhana_meanings.py prep` so a book with no `witness/join-NN.jsonl` takes
  `pali.jsonl` `body_joined` (source `text layer` for 14b, `ocr` otherwise); draft ONE shard with
  `docs/translation/drafting-prompt.md` (add: leave out quoted Pāḷi passages and citations); check the cost
  on the Usage page and the quality; then the rest (~16 shards). Option B was to wait and review first.
  The scanned books without PCED (4/3, 14/3, 20–25) stay on hold until 14/2 has been seen (brief §44: the
  OCR body recovers PCED's line almost whole in only 40–51% of rows on 4/1–4/2).
- **Suggested first message to the cloud session:** "Read CLAUDE.md, then the brief's §44 and §48 and
  NEXT-SESSION item 1b. First, change `tools/abhidhana_meanings.py prep` so that a book with no
  `witness/join-NN.jsonl` takes its Burmese from our text (`pali.jsonl` `body_joined`), marked `source:
  text layer` for 14b; show me the change and the counts for 14b before drafting. Then draft ONE shard of
  14b with `docs/translation/drafting-prompt.md`, translating only the Burmese explanation (not the quoted
  Pāḷi or the citations), and stop, so I can check the cost and quality."
- **Cost.** The 97 shards of vols. 15–19 used about 19 million tokens (43,319 rows); how that maps onto the
  $250 is not known: check after one shard. Cloud sessions also share the account's usage limits (Claude
  Code docs); a free weekly reset ("Resets", Usage page) is available until 22 Oct — keep it for a limit hit.
- **Cheaper models** (Sonnet, or Fable, which has its own weekly limit) were discussed but not tried: test
  one shard against an Opus shard of vols. 15–19 before switching.
- **When a cloud job is merged and pulled**, a Cowork chat reads the brief and this file from the folder,
  checks the live site, and copies both into the Project (the cloud cannot reach the Project).

## Next, in order

00. ~~Versions~~: tags v0.1.0–v0.11.0 created by the editor; the footer shows `VERSION` (brief §43). Tag **v0.13.0** on the push of §48
   (and v0.12.0 on §47's, if not yet made). Each push that changes data or the site: bump `VERSION`, add a `CHANGELOG.md` section, tag.
00t. **After the §59 push (v0.22.0)**: `/data/version.json` 0.22.0; `/w/saddhā` and `/w/sati` (vol. 21) show a Meaning box, *borrador*;
   About: "vols. 1–3, 4/1, 4/2, 5–13, 14/1, 14/2, 15–19 y 21–24". Tag v0.22.0.
00s. ~~After the §58 push (v0.21.0)~~: done 28 Sep (the editor): 0.21.0 served, `/w/sīla` shows vol. 24's Meaning box (*borrador*), About
   lists 22–24. Was: `/data/version.json` 0.21.0; `/w/sīla` and `/w/sukha` (vol. 24) show a Meaning box, *borrador*;
   About: "vols. 1–3, 4/1, 4/2, 5–13, 14/1, 14/2, 15–19 y 22–24". Tag v0.21.0.
00r. ~~After the §57 push (v0.20.0)~~: done 28 Sep (the editor): 0.20.0 live, `/w/samādhi` *borrador*, About lists 22 and 23, search
   ranks na before ṅa / ña (v0.19.1). Was: `/data/version.json` 0.20.0; `/w/samādhi` and `/w/samatha` (vol. 22) show a Meaning box,
   *borrador*; About: "vols. 1–3, 4/1, 4/2, 5–13, 14/1, 14/2, 15–19, 22 y 23". Tag v0.20.0 (and v0.19.1, if not yet tagged).
00q. ~~After the §56 push (v0.19.0)~~: done (the editor, 28 Sep; checked with 00r). Was: `/data/version.json` 0.19.0; `/w/sāsana` (191175) and `/w/sāvaka` (190948) show a Meaning
   box, *borrador*; About: "vols. 1–3, 4/1, 4/2, 5–13, 14/1, 14/2, 15–19 y 23". Tag v0.18.5 and v0.19.0 (both on this branch).
00p. **v0.18.4** (28 Sep, no brief section): vol. 4/3's article step re-run (`abhidhana_articles.py 4c`, `abhidhana_romanise.py 4c`)
   with the three analyses corrected in editor mode and exported in v0.18.2 (176136 omakapatta, 176140 omakasatta, 176144
   omakkhi). Checked live 28 Sep (the editor): `/w/omakasatta` shows *Análisis corregido*.
00o. ~~After the §54 push (v0.18.3)~~: done, checked 28 Sep (the editor): 0.18.3 live, `/w/pamattakaraṇaṭṭha` shows the new
   draft. Was: `/data/version.json` 0.18.3; `/w/pamattakaraṇaṭṭha` (210168) shows the new draft
   (*el significado / sentido que es el hacer / producir el descuido*), *borrador*. Tag v0.18.3.
00n. ~~The weekly export workflow~~: done. Added in v0.18.1; its first run opened PR #33 (v0.18.2, three analyses of 4/3),
   merged 28 Sep (brief §53, corrected). Was: **The weekly export workflow** (v0.18.1): `.github/workflows/export-edits.yml`, Monday 10:00 UTC and on demand
   (Actions → Export edits → Run workflow). The repository and the organisation allow Actions to open pull requests
   (the editor, 28 Sep); the workflow asks for `contents: write` and `pull-requests: write` itself, so the default
   permission can stay read-only. First manual run: to do after the push; with no edits it ends "No new edits", with edits
   it opens a PR `vX.Y.Z: edits from editor mode (date)`. After merging such a PR: tag it, and on the Mac re-run the
   article step for the books the PR lists. This settles 00m (b).
00m. **After the §53 push (v0.18.0)**: `/data/version.json` 0.18.0; Browse unchanged for a visitor. Once editor mode is on
   (00l): open an article's *Editar*, switch *Análisis* to *Latín*, type `omaka + patta`: *se guarda* ဩမက + ပတ္တ, *relectura*
   ✓; type a capital: *Guardar* disabled. Check the Burmese in the Mac's font (the cloud's Chromium lacks a Myanmar shaper).
   For the editor: (a) the tall ā ါ / ာ is invisible in roman; the converter writes Aksharamukha's form (သမ္ပာ, while most
   volumes print သမ္ပါ): keep, or follow the print for ္ပ (brief §53)? (b) ~~the weekly export workflow~~: done in v0.18.1 (00n). Was: the weekly export workflow
   (`.github/workflows/export-edits.yml`, cron `0 10 * * 1` + manual; export via `--api`, patch bump, CHANGELOG line, PR on
   `edits/YYYY-MM-DD`) was not written: the cloud session's permission check refused the file. The export tool's new
   `--summary FILE` gives the books, fields and books to re-run for it. Allow it in a new session, or add it by hand; it
   needs Settings → Actions → General → Workflow permissions: *Read and write* and *Allow GitHub Actions to create and
   approve pull requests*.
00l. **After the §52 push (v0.17.0)**: check the live site (fetch `/data/version.json` first): 0.17.0; Browse unchanged for a
   visitor (`/w/luñcana`: *corregido*, no *Editar* button); `/api/edits?book=18` answers 503 "no database bound" until step C
   below (the page ignores it and shows the published data). Tag v0.17.0.
   **Then switch editor mode on** (the editor, Cloudflare dashboard; `docs/editor-mode.md` §2, steps 1–15): create the D1
   database `abhidhana-edits` and run `site/d1/schema.sql`; an Access application (self-hosted) on `abhidhana.buddha-dhamma.net`
   paths `edit` and `api/admin`, policy *Allow* the editor's e-mail; in the Pages project check the root directory is the repo
   root, bind D1 as `DB`, set `ACCESS_TEAM_DOMAIN`, `ACCESS_AUD`, `EDITOR_EMAILS`; redeploy; run the checks of §2 D.
   To bring edits into the repo (on the Mac): `npx wrangler d1 export abhidhana-edits --remote --output …/edits.sql`, then
   `python3 tools/abhidhana_edits_export.py --d1 …/edits.sql` (report) and `--write`; re-run the article step for the books it
   lists (`abhidhana_articles.py NN && abhidhana_romanise.py NN`); VERSION, CHANGELOG, push, tag.
00k. ~~After the §51 push, check the live site~~: done 27 Sep: version 0.16.0; `/w/omakadesanā` and `/w/omakadassa` show the
   analysis marked *corregido* (Análisis corregido); `/w/vātakuppa` shows *corregido*. Tag v0.16.0 (the editor).
00j. ~~After the §50 push, check the live site~~: done 27 Sep (in-app browser): `/data/version.json` and every page's meta 0.15.0;
   `/w/pamattakaraṇaṭṭha` (vol. 14/2): the Burmese definition begins မေ့ လျော့ခြင်းကို; `/w/akālacārī` (id 356) begins (က).
   Pushed as `e79103b`, tagged v0.15.0 by the editor.
00i. ~~After the §49 push, check the live site~~: done 27 Sep (the editor). Was: 0.14.0; `/w/parinibbāna` shows *borrador*; About lists 14/2.
00h. ~~After the §48 push, check the live site~~: done 27 Sep (the editor): 0.13.0 live, About lists vols. 15–19, the five
   /w/ pages show *borrador*. Was (fetch `/data/version.json` first): 0.13.0; `/w/bhava` (vol. 15),
   `/w/magga` (vol. 16), `/w/rūpa` (vol. 17), `/w/loka` (vol. 18), `/w/vipāka` (vol. 19) show a Meaning box, *borrador*;
   About: "vols. 1–3, 4/1, 4/2, 5–13, 14/1 y 15–19".
00g. ~~After the §47 push, check the live site~~: done 27 Sep (brief §48). Was (fetch `/data/version.json` first): 0.12.0; `/w/dukkha` (vol. 10),
   `/w/nibbāna` (vol. 12), `/w/paṭisandhi` (vol. 14/1) show a Meaning box, *borrador*; About: "vols. 1–3, 4/1, 4/2, 5–13 y 14/1".
00f. ~~After the §46 push, check the live site~~: done 26 Sep (brief §47). Was (fetch `/data/version.json` first): 0.11.0; `/w/cakkavatti` (vol. 7),
   `/w/jhāna` (vol. 8), `/w/taṇhā` (vol. 9) show a Meaning box, *borrador*; About: "vols. 1–3, 4/1, 4/2 y 5–9".
00e. ~~After the §45 push, check the live site~~: done 26 Sep (brief §46). Was (the Cloudflare build takes some minutes: fetch `/data/version.json`
   first): `/w/kilesa` shows vol. 6's Meaning box, *borrador*; About: "vols. 1–3, 4/1, 4/2, 5 y 6"; version 0.10.0.
00d. ~~After the §44 push, check the live site~~: done 26 Sep (brief §45). Was: `/w/katvā` shows `[kara + tvā]` with the Burmese analysis on its own
   line below; `/w/ulūka` the romanised derivation (`… dhān ṭī 638. ula + ṇūka. …`) and the Burmese line; the article
   line and the page pane read "p. 620 · p. del PDF 662" (`/w/ehalokika`; page the pane with ‹ › and the printed page
   follows); the search list; vol. 2 PDF 241 (p. 224) and vol. 22 PDF 920 (p. 881); `/volumes/` read page view (printed
   p. on pages without records); vol. 5's Meaning boxes (`/w/kaṅkhā`); About: "vols. 1–3, 4/1, 4/2 and 5".
00c. ~~After the §43 push, check the live site~~: done 26 Sep (brief §44).
   **"Budistas" or "Buddhistas"**: the logo and the footer say Buddhistas, About and README say Budistas; the editor to decide.
00b. ~~Check the live site after `5db316f`~~: done 26 Sep (brief §42).

0. ~~Vol. 25 at 200 dpi~~, ~~the README~~, ~~the website~~: done 25–26 Sep. **The site is live** at
   https://abhidhana.buddha-dhamma.net (the editor deployed it; checked 26 Sep in the browser: all 29 books,
   221,154 headwords, search, label pop-ups, About and Labels pages, 404 page). `site/src/_headers` now
   makes browsers revalidate `/data/*` and `/assets/*` on every load; with the old one-hour cache a
   visitor saw vol. 25 as "coming" after it was published.
1. ~~Page images~~: all 29 books live, 25,700 pages, 2.5 GB; `check` clean (brief §35).
0b. ~~**Push the 26 Sep night work** (brief §40)~~ (pushed as `5db316f`; the §42 check covered the Meaning box,
   (ti) labels, PCED and "corrected" marks, versioned assets). Still to look at on the live site: the search list, Hide index
   (`\`), the ES/EN switch at ~1,000 px, the alphabet in roman mode, the About credits. (`tmp/sitetest/`, the test tarballs,
   was deleted by the editor on 26 Sep.) The Reader artifact is not republished with the new analyses
   (`abhidhana_reader_data.py` for all books, then republish).
0c. **Hand corrections** go in `docs/corrections.tsv` (brief §40); re-run `abhidhana_articles.py NN` and
   `abhidhana_romanise.py NN`. Confirm the `roman` column of `docs/labels.md` §0.
1a. ~~**Vol. 14/2 drafted**~~: done, with the redraft of 28 Sep (brief §54); what follows is for review and the Mac. (Approved by the editor, 27 Sep, after trial shard 00; brief §49): 6,795 rows from the text layer,
   1,406 flagged, omissions in `meanings/14b-omitted.tsv`. Live check of v0.14.0 done 27 Sep (the editor).
   ~~Redraft 497 rows~~ whose Burmese now begins with the restored first words: done 28 Sep (brief §54, v0.18.3), two shards,
   339,035 agent tokens; flags 1,406 → 1,128. For the editor: aorists in -esi were put in the 2nd person by one agent (213807,
   213826, 214262) and the 3rd by the other (215427, 215433, 215546), all flagged: which person for -esi? 211785 runs on into
   six headwords (ပရသက္ကာရ … ပရသတ္တ), only the first translated. 213590 and 215011: `prep` still drops the restored ပရိ with a
   Pāḷi span (the drafts read it back, flagged).
   On the Mac: re-run `prep 15` and compare with a copy made before the §49 changes (should be byte-identical).
   For review:
   - run-on headwords with no body: 210255, 210257, 210262 (their text is inside 210254, 210256, 210261); left without a
     Meaning for now (the editor, 27 Sep). Across 14/2, 123 unlocated articles have no body; brief §49 lists the host rows,
     which the agents handled two ways (left out, or translated inside the host);
   - 210324: starts with a grammarian's note (…ဝ-ပစ္စည်း); its analysis bracket is not flagged as damaged, so prep did not cut it;
   - ~~the first word(s) of a body lost~~ in `abhidhana_articles.py`: fixed 27 Sep (brief §50), 6,003 bodies in 29 books; in books
     01–19 kept only where PCED agrees. 324 rows now have the restored words read as a Pāḷi span (brief §50): cosmetic, for the
     span finder (§40).
1c. **The final revision** (the editor, 27 Sep): the translations are revised after the whole dictionary is drafted; until then
   no re-rendering. `docs/translation/revision-queue.tsv` lists 3,382 rows that conflict with the rules of 27 Sep (brief §51);
   new drafts follow the rules through `drafting-prompt.md`. Corrections go in `docs/translation/corrections-es.tsv` (a re-`merge`
   of a book must re-apply them: `merge` does not yet). Rule 1 (split run-on articles, e.g. 210255 inside 210254) is for the
   article step on the Mac, each split checked on the page image.
   **Added 28 Sep (the editor: review questions wait for this revision, not asked before):** (a) the 20 ids of vol. 23 shard 00
   listed in brief §55, against the page image; (b) aorists in -si / -esi, drafted in the 3rd person and flagged as the prompt
   says (vol. 23: 185770, 185942 and the rest of the book's "aorist" flags; 14/2: brief §54); (c) run-on articles in the
   OCR books: only the headword's own text translated, the run-on text in `omitted`, flagged "run-on article: X" (vol. 23:
   185509/10, 185571/72, 185646–48, 185791/92, 185844/45, 185852/54 and the rest in `23-flags.tsv`; 177547 sannipatita inside
   177546 in vol. 22), to be split by rule 1; the «Sn» of a run-on article kept in its host row (185509, 185874).
   From the rest of vol. 23 (brief §56): (d) shard 04 translated a headword's definition from the previous line's run-on text in
   187500, 187501, 187506, 187608, 187609, 187611 (the other shards left it in `omitted`); (e) renderings that differ between
   shards: sikkhāpada *regla de entrenamiento* (shard 08) vs ⟦=sikkhāpada⟧ (11, 12); သဘောလက္ခဏာ (03); ဦးချို *copete* in 191722,
   191731; Burmese month names romanised or in ‹ ›; Pāḷi kept without a stem: sarūpa, saraṇagamana, sāsana, kahāpaṇa, meru;
   (f) headword and text disagree, and rows to check on the page: the lists in brief §56.
   From vol. 22 (brief §57): (g) the person of -si / -esi aorists and of -tha was not applied alike: most shards 3rd person, flagged;
   shards 00 (177619, 177654), 07 (180994), 08 (181408) 2nd person by the rule, flagged; -tha as a 3rd-person aorist in 180237,
   180549, 180993; (h) run-on articles (368 flags) and senses printed twice (68), as in vol. 23; shard 14 translated both parts of
   184524, shard 12 the second copy of 183148, 183239, 183446; (i) renderings the agents chose: ဝါဒ ⟦ဝါဒ⟧, သဗ္ဗညု kept Pāḷi, ပူပန်
   *angustia*, ငြိမ်းအေး *aquietamiento*, ရဟန်းတရား ⟦=dhamma⟧, ကောင်းစွာ (sam-) *completamente*, the ပယ်နုတ်-ပယ်ဖျက်-… chain,
   ကျမ်းတက် *nexo textual*, ဒြဗ် *cosa*; (j) rows to check on the page and headword / text disagreements: the lists in brief §57.
   From vol. 24 (brief §58): (k) run-on articles handled four ways: most shards as the prompt says; shard 10 moved proper-name articles'
   senses to the line where the article starts (207948/49, 208084/85, 208153/54, 208185/86); shard 13 translated a gloss from the previous
   line (209515, 209651); shard 06 translated run-on articles inside the host row (206033, 206202); shards 02 and 14 translated homonyms
   together (204189–90, 204388, 209954, 210023); (l) ~25 truncated glosses in 203784–203800, and split glosses (209243/44, 209453/54,
   209511/12, 209059/60); (m) renderings: ချမ်းသာ *felicidad*, သိမ်မွေ့ *sutil*, အဆောက်အဦ *equipamiento*, သုသာန် *osario*, အင်ကြင်း
   ⟦=sāla⟧, ‹ကညစ်› (209855 vs 209881–84); 134 rows keep Burmese names in ‹ ›; (n) headword / text disagreements and rows to check on
   the page: the lists in brief §58; shard 05 corrected မွှေး (fragrant) without flagging it.
   From vol. 21 (brief §59): (o) run-on articles and senses printed twice handled apart from the prompt: shard 04 translated five sagga
   homographs together (166028); shard 12 translated both printed copies of satti 170052, sattha 170159, satthaka 170167, satthu 170259;
   shard 01 moved «S» placeholders out of run-on text (6 lines); saddhā 171012–15 and saddhādhimutta 171074–75 spread over several ids;
   saṅkhāra 166574's two copies disagree on vitakka / vicāra (kāya- or vacīsaṅkhāra); (p) renderings the agents chose: saṁsāra kept Pāḷi,
   ဆုတ်နစ် *hundirse*, cakkavāḷa / lokadhātu / sāsana kept Pāḷi, သံဂါယနာတင် *llevar a la saṅgāyanā*, the robe names (ဒုကုဋ်, သင်းပိုင်,
   ကိုယ်ရုံ), သစ္စာ kept ⟦ ⟧ also as truthfulness or vow, ထာဝရဘုရား *Dios*, ပြာသာဒ် ⟦=pāsāda⟧ vs *palacio* (shard 11), သီတင်းတစ်ပတ်
   *semana de observancia*, သဒ္ဒါ *palabra*, grammatical သုတ် *regla*, သူတော်ကောင်းတရား *la Enseñanza de los buenos*, သပြေ *jambolán*;
   (q) person: 170811, 170829 follow the Burmese pronoun against the Pāḷi ending; 164276 saṁsariṁ 1st person against "they"; -si / -ttha
   aorists in the 3rd (saṅkhobhesi, saṅgamesi, 167879); (r) to fix or check: 166145 left ‹ရွဲရှာ› (ရွံရှာ, *recelar*); lost numbers in
   167097, 167190, 167285–88, 167293–94, 170013, 170259; garbled sense numbers in 171365–66, 171730–31; 169835's headword
   (sattavidhabojjhaṅga?); the rest in brief §59 and `21-flags.tsv`.
1b. **Translation** (brief §37, §39–56). **Drafted: vols. 1–3, 4/1, 4/2, 5–19, 14/2 and 21–24** (192,401 rows, 87.0% of the index, none reviewed; flags in `meanings/NN-flags.tsv`). **Vol. 4/3 deferred** (no PCED; the editor, 26 Sep; brief §44). PCED's vols. 1–19 are all drafted (brief §48).
   **The OCR books** (brief §55–56): **vol. 23 drafted and merged** (v0.19.0; 6,906 rows, 67.6% of drafted lines flagged,
   with `omitted` or empty; 3.75 M agent tokens). **Vol. 22 drafted and merged** (v0.20.0, brief §57; in Cowork, one wave of 17
   agents, no usage-limit stop; 7,613 rows; 75.0% of drafted lines flagged, with `omitted` or empty; 4.73 M agent tokens, ~626 a
   line). The Cowork VM's `/sessions` disk is full (pip fails there): run `merge` / `report` in the cloud container, or free space
   first. On the Mac: re-run `prep 15` against the real witness (byte-identical expected, §55).
   **Vol. 24 drafted and merged** (v0.21.0, brief §58; one wave of 15 agents, no usage-limit stop; 6,685 rows; 69.0% of drafted
   lines flagged, with `omitted` or empty; 3.94 M agent tokens, ~600 a line; the VM's disk still full, merge / report in the cloud).
   **Vol. 21 drafted and merged** (v0.22.0, brief §59; one wave of 17 agents, no usage-limit stop; 7,752 rows; 67.9% of drafted
   lines flagged, with `omitted` or empty; 4.77 M agent tokens, ~627 a line; the VM's disk still full, merge / report in the cloud).
   **Next OCR books, the editor to decide**: 14/3, 20, 25 (and 4/3, deferred). Same path: `prep NN --shards N --work
   tmp/meanings/vNN` (~445 lines a shard), agents with `23-shard00-prompt.md` (vol., shard, line count and paths changed).
   **Next: the books with no PCED** — 14/3, 20–25, and 4/3 (deferred) — could only be drafted from
   our OCR body: the editor to decide, as for 4/3 (brief §44 measured the OCR body against PCED on 4/1 and 4/2). If yes:
   `prep('NN', N)` from Python (N so that shards are ~450 lines), each book's `workNN.json` and `shards/` in
   `tmp/meanings/vNN/`; one agent and scratch folder per shard (20 at once) with `docs/translation/drafting-prompt.md`
   (brief §48; a wave can stop at the usage limit: its RESUMING note covers that); for `merge NN` and `report NN` move the
   book's three up to `tmp/meanings/` and back after (brief §46). Vol. 15's supplement in 4c (53 ဘိဇ္ဇ rows, item 9) is
   not drafted. Seven vol. 10 rows have `#NAME?` in PCED (brief §47): draft
   them from our OCR. **The future's person**: the print writes …လတ်အံ့ for the 1st person and …လတ္တံ့ for the 3rd (brief §47);
   the rule "3rd unless marked" now says so (`drafting-prompt.md`, brief §48). Decided 26 Sep: ဂုဏ် *cualidad / virtud* (L105), လူ as layperson *laico*
   (L106). Open from vols. 15–19 (brief §48): ပယ် for physical removal (*quitar* or *abandonar*); the three stacked future
   endings (one rendering or three); ငရဲ *infierno* or ⟦=niraya⟧; ဖောက်ပြန်; အကျိုး in -attha (*beneficio* / *propósito*);
   မင်္ဂလာ, ဝဋ်, ဝါ kept Pāḷi; ငရုတ် (marica) *ají* vs pepper. Open from vols. 6–9: ခေတ် ⟦=khetta⟧; ရှုတ်ချ *denigrar* vs ကဲ့ရဲ့ *censurar*; စောဒနာ *reprender*; ဥတု as menses.
   Settled for vol. 5 on: ကုသိုလ် as merit → *mérito / meritorio*; stems
   L101–L104 (နတ် ⟦=deva⟧, ရဟန်း *monje*, ပယ် *abandonar*, ဥတု ⟦=utu⟧ / *estación*). Raised by vol. 5's agents, for the
   editor: ကံ as the Saṅgha's act or the grammatical object, and ကြိယာ as "verb" (both kept Pāḷi, flagged); ကမ္ဘာ *eón*
   or *mundo*; ဘုံ, ဘီလူး, နတ်သား, နတ်သမီး; ပယ် where it means "reject"; the future (အံ့) in 1st or 3rd person; the
   source tag ထောမ; (သျ) as in 4/2. Source: **PCED** (the editor, 26 Sep). kusala = *sano*, akusala =
   *insano* (`docs/translation/glossary.tsv`); the other batch-1 stems are not yet reviewed. Six vol. 1
   rows have no draft (ids 21, 2190, 3938, 3988, 5435, 7881); row 2767 needs its Burmese tree names. Vol. 1's Meaning boxes are filled with **drafts**: 8,144 rows in
   `docs/translation/meanings/01.jsonl`, all `drafted`. Waiting for the editor:
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
2a. ~~Site redesign~~: built 26 Sep (brief §38). After the editor's push, check the live site. Browse is
   the home page; `/volumes/` and `/abbreviations/` are new; run `git rm -r site/src/labels`.
2. **The Introduction page** (brief §35) rebuilds itself from `docs/introduction/` on every push; keep the
   chapter files to the contract in `tools/abhidhana_intro.py`'s docstring. It shows drafts under a banner,
   while the About page's History waits for review (item 7c): decide whether ch. 4's names should wait too.
3. **Labels, the editor's to confirm** (`docs/labels.md` §0; `python3 tools/abhidhana_labels.py` checks
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
