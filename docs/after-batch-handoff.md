# After the batch — handoff (2026-09-25)

State: run_volumes.sh finished 13:26:31 ("all done"), vols 10–20, 22, 23, 24 OCR'd with articles + pali.
Latest commit 10852bd (reports 15–20, 22; Reader to vol. 22). Nothing edited since.

## Measured, ready to apply to tools/abhidhana_articles.py (pipeline edits now allowed)

1. Label map: add (ကာ၊ကမ္မ၊ကြိ). Readings seen: ကာ၊ကမ္မ၊ကြိ · ကာ၊ ကမ္မ၊ ကြို · ကာ၊ကမ္မ၊ ကြို · ကာ၊ ကမ္မ၊ကြ.
   Also add to reader/index.html GL.
2. PAGE_FIX['22'] = {q: q-1 for q in range(920, 935)}
   Verified: PDF 919 holds p920's list 9/9 and only 2/11 of its own, so 919's own printed page is missing from the scan;
   from 920 to the end each index list sits one page early.
3. ID_PAGE_FIX, strong runs (book: (id_from, id_to, pdf page printed on)); keep existing 4c and 06 entries:
   - 14c: (196222,196234,402) (197721,197732,565) (198069,198070,605) (198200,198207,625) (201263,201269,930) (201325,201334,936) (201634,201646,962)
   - 22: (178676,178682,169) (178835,178847,184) (179577,179585,253) (185264,185267,894)
     [185467–185470 at 929 lies in the shifted zone: handled by PAGE_FIX, not an ID fix]
   - 23: (187848,187857,275) (187871,187878,277) (189039,189048,390) (189502,189513,436) (190351,190359,523)
   - 24: (206034,206036,329)
   Weak — check the image before adding: 14c 976 (201781–201786, 2 of 6 hits); 18 815 (146728–146731, 2 of 4); 10 219 (81975–81976).
   Uncertain: 14c 605 is only 2 ids; confirm on the image.

## Then, in order

1. Re-run articles + romanise for every book, including 14b (text layer, ocr/14b/pages). ≤4 in parallel per VM call (180 s limit; background jobs die).
2. Re-run witness joins: PCED (tools/abhidhana_witness_join.py) and Pn Daza (tools/abhidhana_witness_pndaza.py) for 01–19.
3. Vols 23, 24: ocr-report + articles notes (~/stats.py 23 24, ~/mkrep.py needs IMG/WIT/NOTES/SPOT entries for them);
   spot check against images (no witness covers 23/24; 23 is at ~323 ppi). Tarballs to release sources-v1 (--clobber). Close issues.
4. Reader: at 63.46 MB of the 64 MB limit, 23/24 won't fit. Switch reader data from base64 .gz.txt to a served binary type
   (e.g. gzip bytes in .wasm, ~25% smaller) or trim fields; update abhidhana_reader_data.py and index.html; test; republish
   to https://claude.ai/artifact/RjuFxtkh4FASRkhBeYhVS3. Add 14b, 23, 24 to VOLS.
5. Regenerate report tables after the re-run.
6. docs/index-errata.md: vol 13 index pp 145–160 (PDF 175–190) list 232 ဗ headwords belonging to vol 15 (typed text has the same error);
   vol 22 missing page; the misfiled runs above; typos from brief §15–17; ကဉ္စိက.
7. Brief §27 and NEXT-SESSION, in folder and Project. Commit commands in batches; close issues with the title-matching loop.
8. Later: gutter re-cut natively (tools/abhidhana_recut.py --scan/--run/--report); vol 9 p823 re-read; label-disagreement image checks; vols 21, 25.

Leave .gitignore to the editor (the other chat changed it).
