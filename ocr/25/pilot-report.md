# Volume 25 pilot — what was run

466 pages, 200 dpi, tesseract 5 with `myap` (pndaza) from `~/Tipitaka/nissaya/tessdata`,
two passes per page (psm 6 and psm 3), union scored against the 4,046 headwords the app's
index lists for this volume. Run in the session's cloud container at 13 pages a minute;
`pages-container.tar.gz` is the tarball it came back in, and `pages/` is that unpacked.

Results, and everything that follows from them, are in `../../abhidhana-project-brief.md`
§§5-6. The headline: **94.0% of headwords verbatim, 63% of pages perfect, 96.5% placeable**,
and the one thing the recall figure cannot see — **the two columns are interleaved** and
the pages must be re-run with `--columns` before any article is extracted.

`pages/pNNNN.json` per page: `pdf_page`, `index_page`, `dpi`, `indexed`, `headwords`,
`per_pass`, `union`, `missed`, and `text` (both passes, verbatim). `coltest_sample.txt` is
one page read with the columns cut, for comparison.

The 18 loose `.txt` files are the psm-6 text of the first 17 pages, written by an earlier
run in the Cowork VM at 300 dpi before the work moved to the container. Their JSON was
overwritten by the 200 dpi run; recall was identical either way.
