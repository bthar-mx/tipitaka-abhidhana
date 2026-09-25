#!/bin/bash
# Run the whole per-volume pipeline for several books, one after the other, unattended:
#   OCR (column cut) -> articles -> romanise
# Usage, from the repo root:
#   caffeinate -i tools/run_volumes.sh                 # the default list below
#   caffeinate -i tools/run_volumes.sh 11 12 13        # just these books
# `caffeinate -i` keeps the Mac awake until the script ends (the screen may still sleep).
#
# - Resolution: each book's --dpi is its scan's own resolution, read with pdfimages at three
#   pages (25%, 50%, 75% of the book) and the median taken. Upsampling a 1-bit scan lowers
#   recall (vol. 1: 92.1% native vs 87.8% at 200 dpi), so never render above native.
# - Resumable: OCR skips pages already on disk; a book whose articles.jsonl exists is skipped
#   entirely. Re-running the script after an interruption carries on where it stopped.
# - Book 21 used to be left out: its index seemed to run 65 pages past its PDF. It does not; ten
#   headwords carry p. 962 for 692 (brief §27), now corrected by ID_PAGE_FIX, so 21 runs normally.
# - Book 25's old whole-page pilot (200 dpi, no column cut) was moved out of ocr/25/pages to
#   tmp/ocr-25-pilot-pages on 25 Sep 2026, so 25 now runs like any other book (300 ppi scan).
# - Book 14b is not a scan: it is typeset text in legacy Win-Burmese fonts (WinResearcher,
#   WinPinya, WinHaka), so it has no page images and is skipped automatically. Its text can be
#   extracted and converted to Unicode instead of OCR'd.
# - One book at a time. Never start this while another OCR is running.
# - Reports, spot checks, the Reader and commits are NOT done here; a chat or Claude Code does
#   those afterwards from the log and the files.

cd "$(dirname "$0")/.." || exit 1
export ABHIDHANA_TESSDATA="${ABHIDHANA_TESSDATA:-$HOME/Tipitaka/nissaya/tessdata}"
WORKERS="${WORKERS:-10}"
BOOKS=("$@")
[ ${#BOOKS[@]} -eq 0 ] && BOOKS=(10 11 12 13 14 14b 14c 15 16 17 18 19 20 22 23 24)

mkdir -p logs
LOG="logs/run-$(date +%Y%m%d-%H%M).log"
say() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $*" | tee -a "$LOG"; }

say "start: ${BOOKS[*]}  (workers $WORKERS)"
for b in "${BOOKS[@]}"; do
  pdf="pdfs/$b.pdf"
  if [ ! -f "$pdf" ]; then say "$b: no $pdf, skipped"; continue; fi
  if [ -f "ocr/$b/articles.jsonl" ]; then say "$b: articles.jsonl exists, skipped"; continue; fi

  n=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
  ppis=()
  for f in 25 50 75; do
    p=$(( n * f / 100 ))
    ppis+=( "$(pdfimages -list -f "$p" -l "$p" "$pdf" | awk 'NR>2{print $(NF-3); exit}')" )
  done
  dpi=$(printf '%s\n' "${ppis[@]}" | sort -n | sed -n 2p)
  if [ -z "$dpi" ]; then
    # no page image at all: the PDF is not a scan (14b is typeset text in legacy Win-Burmese
    # fonts). Rendering it at a guessed dpi would OCR at a fraction of the right size.
    say "$b: no scanned images found in $pdf; not a scan, skipped (needs its own treatment)"
    continue
  fi
  # Vol. 25 is the exception to "render at native": at its 300 ppi, 16 pages read 57.8% of their
  # headwords; at 200 dpi, 88.3% (brief §5 and §29). Measured per book, never assumed.
  if [ "$b" = "25" ]; then dpi=200; fi
  say "$b: $n pages, scan ppi ${ppis[*]} -> --dpi $dpi"

  t0=$(date +%s)
  python3 tools/abhidhana_ocr.py "$b" --columns --dpi "$dpi" --passes page.psm6 \
      --workers "$WORKERS" --budget 100000 2>&1 | grep -v Warning | tee -a "$LOG" | tail -4
  got=$(ls "ocr/$b/pages" 2>/dev/null | wc -l | tr -d ' ')
  say "$b: OCR finished in $(( ($(date +%s) - t0) / 60 )) min, $got of $n pages on disk"
  if [ "$got" -lt "$n" ]; then
    say "$b: pages missing; re-run the script later to retry them. Articles step skipped."
    continue
  fi

  python3 tools/abhidhana_articles.py "$b" 2>&1 | grep -E 'located, any|label \+ body' | tee -a "$LOG"
  python3 tools/abhidhana_romanise.py "$b" 2>&1 | grep -E 'tokens in those spans' | tee -a "$LOG"
  say "$b: done"
done
say "all done"
