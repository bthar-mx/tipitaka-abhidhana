# Runbook — digitising one volume

For anyone running the pipeline on their own machine. One volume at a time, claimed through its
GitHub issue so that two people never OCR the same book.

## 0. Once per machine

Run everything **natively in Terminal**, not inside a VM or container that emulates the CPU.
Tesseract inside the Cowork desktop VM measured 37 s a page, against 5 s natively.

```sh
brew install tesseract poppler gh          # macOS; on Linux: apt install tesseract-ocr poppler-utils gh
python3 -m pip install pillow aksharamukha
gh auth login
git clone git@github.com:bthar-mx/tipitaka-abhidhana.git
cd tipitaka-abhidhana
tools/fetch_sources.sh                     # 29 PDFs + the index db from the release, checksummed
```

The OCR model `myap.traineddata` (Pn Daza's Burmese-Pāḷi model) goes in `tessdata/`, which
git ignores. Point to it with `export ABHIDHANA_TESSDATA=$PWD/tessdata`.

To check romanised headwords against the canon, place the OSBCT vocabulary (one word per
line, 682,010 words) at `ocr/osbct_vocab.txt`. Ask for it; it is built from OSBCT's index
files. Without it the article step still runs and simply skips the `osbct` column.

## 1. Claim the volume

Assign yourself its issue ("Vol. N — OCR + articles") and branch: `git switch -c vol-N`.

Book ids are the PDF names: `01 02 03 4a 4b 4c 05 … 14 14b 14c 15 … 25`.

## 2. Check the book before running

```sh
pdfimages -list -f 300 -l 300 pdfs/NN.pdf     # image width/height and x-ppi
pdfinfo -f 300 -l 300 pdfs/NN.pdf | grep size # page size in pt
```

**Render at the scan's native resolution.** If `x-ppi` is ~72 and the page is ~2000 pt wide
(like vol. 1), use `--dpi 72`. If the page is declared at a normal paper size, use the dpi at
which the rendered width matches the image width. Rendering above native resolution
upsamples a 1-bit scan and *lowers* recall (vol. 1: 92.1% at native, 87.8% at 200 dpi).
If unsure, OCR ten spread-out pages at two settings and compare. Record what you chose in
the volume's report.

**Book 21:** its index runs 65 pages past its PDF (990 against 925). Do not run it until
that is explained.

## 3. OCR

```sh
python3 tools/abhidhana_ocr.py NN --columns --dpi <native> --passes page.psm6 \
        --workers <cores> --budget 100000
```

It is resumable: each page is written to `ocr/NN/pages/pNNNN.json` as it finishes, and a
re-run skips pages already on disk. At the end it prints recall and in-order figures.

- **Gutter**: after the run, list pages whose `_gutter` is outside 0.44–0.555. The tool
  falls back to the white channel there, but look at a couple against the image.
- **Front matter** is often one column. The column cut garbles it, so read `page.psm6` for those pages.

## 4. Articles

```sh
python3 tools/abhidhana_articles.py NN
```

This writes `ocr/NN/articles.jsonl` and `ocr/NN/articles-report.md`. Then write
`ocr/NN/ocr-report.md` on the model of `ocr/01/ocr-report.md`: settings and why, the
results table, the worst pages, and anything odd. Add to the articles report what the
figures mean, as in vol. 1's. The script regenerates the table part, so keep the notes below it.

**Spot-check before you open the PR:** open three pages as images and compare them with
their rows. Note what you find in the report, in the same form as vol. 1's p. 300 check.

## 5. Hand in

```sh
tar czf ocr-NN-pages.tar.gz -C ocr/NN pages     # page records: too big for git, go in the release
git add ocr/NN/*.jsonl ocr/NN/*.md
git commit -m "Vol. NN: OCR + articles"
git push -u origin vol-N && gh pr create --fill
```

Attach `ocr-NN-pages.tar.gz` to the PR, or ask for it to be added to the release.

## What not to do

- Do not edit the Burmese in `articles.jsonl` by hand in a volume PR. Corrections go through
  review and change the row's `status`.
- Do not translate. Spanish is done by agreed formula-stems, not per article; see `docs/spanish-method.md`.
- Do not change a tool's behaviour silently. If you change `tools/`, say what you measured
  before and after in the PR, the way the tool docstrings do.
