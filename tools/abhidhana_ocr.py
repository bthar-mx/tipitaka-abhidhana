#!/usr/bin/env python3
"""OCR a volume of the Tipiṭaka Pāḷi-Myanmā Abhidhāna, and score it against the app's index.

Why this is not ~/Tipitaka/nissaya/tools/nissaya_ocr.py. That script splits units on the
printed lemma hyphen, which is a nissaya convention; a dictionary page has none. And it has
no ground truth — its anchor rate asks only whether an OCR'd Pāḷi word exists somewhere in
the canon. Here the ground truth is exact: `db/tipitaka_abidan.db` holds 221,154
(headword, book, page) rows, so for every page the correct headwords are known, in correct
spelling, before a pixel is read. The measure below is a RECALL against a known list.

    the page identity: words.page_number + books.start_page == the PDF page. Verified on
    vol. 1 p. 300 (index p. 180) and holding for every book but 21, whose index runs 65
    pages past its PDF and has not been explained.

THE PAGE IS TWO COLUMNS, AND THIS MATTERS MORE THAN THE MODEL. Run whole, tesseract
interleaves the columns: on twelve sampled pages of vol. 25 only 56.6% (psm 6) or 67.0%
(psm 3) of the headwords came out in the index's own order, so the article text around a
headword is not the article's. Cutting the page at the gutter first and reading each column
separately raises that to 79.2% and the headword recall from 86.8% to 90.6% on the same
pages. The gutter is at 0.500 of the page width, sd 0.001 across the sample, found as the
darkest vertical band in the middle third — that is the printed rule, not a guess.

Measured on vol. 25, all 466 pages (429 of them carrying index entries), 200 dpi, myap:

    headwords verbatim, union of psm 6 and psm 3 over the whole page   94.0%
    pages where every headword came out                                63%
    pages at or above 80%                                              92%
    placeable when a fuzzy match inside a bounded span is allowed       96.5%

200 dpi, not 300: the recall is identical on the same pages and the images are half the
size. A worse-printed volume should be re-tested rather than assumed.

DPI IS NOT PORTABLE BETWEEN BOOKS. Vol. 1's pages are declared 2014 x 3142 pt, i.e. the
1-bit JBIG2 scan sits at 72 ppi, so `-r 200` upsamples it 2.8x to 5595 x 8728 px. Measured
on fifteen vol. 1 pages, column-cut, psm 6 (24 Sep 2026):

    dpi  72 (native)   recall 92.1%   in order 78.7%   ~7 cpu-s a page
    dpi 100            recall 91.5%   in order 78.7%   ~10
    dpi 200            recall 87.8%   in order 77.4%   ~18

Render at the scan's native resolution: check `pdfimages -list` for the book first.

Usage:
    python3 tools/abhidhana_ocr.py 25 --budget 150        # a slice; resumable
    python3 tools/abhidhana_ocr.py 25 --columns           # cut at the gutter (recommended)
    python3 tools/abhidhana_ocr.py 25 --score             # score what is on disk
"""
import argparse, glob, json, os, re, sqlite3, subprocess, sys, time, unicodedata
from bisect import bisect_left
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'db/tipitaka_abidan.db'
TESSDATA = Path(os.environ.get('ABHIDHANA_TESSDATA', Path.home() / 'mnt/nissaya/tessdata'))
SCRATCH = Path(os.environ.get('ABHIDHANA_SCRATCH', Path.home() / 'abh_tmp'))
DPI = 200

nfc = lambda s: unicodedata.normalize('NFC', s)
flat = lambda s: re.sub(r'\s+', '', nfc(s))


def index(book):
    """{pdf_page: [headwords, in the order the dictionary prints them]}"""
    c = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    row = c.execute('select start_page from books where id=?', (book,)).fetchone()
    if not row: sys.exit(f'book {book} is not in {DB}')
    start = row[0]; out = {}
    for w, p in c.execute('select word,page_number from words where book_id=? order by id', (book,)):
        out.setdefault(p + start, []).append(nfc(w))
    return out, start


def tess(path, psm, lang='myap'):
    # OMP_THREAD_LIMIT=1: tesseract's OpenMP pool takes every core by default, so several
    # workers oversubscribe and each page takes as many times longer. Parallelism belongs
    # to the pool below, not to each process.
    return subprocess.run(['tesseract', str(path), 'stdout', '--tessdata-dir', str(TESSDATA),
                           '-l', lang, '--psm', psm], capture_output=True, text=True,
                          env={**os.environ, 'OMP_THREAD_LIMIT': '1'}).stdout


def gutter(im):
    """x of the column break: the printed rule if there is one, else the white channel.

    The rule is found as the darkest column of the middle third. `resize((w, 1))` averages
    each column in one C call, which is why this costs nothing.

    Some pages have no rule. Vol. 1 p. 254 is one: the darkest column there is a heavily
    inked stretch of the right-hand text, at 0.57, and cutting there splits every line of
    that column. So the darkest column is accepted only inside 0.44-0.555 of the width, where every ruled page of vol. 1 has it (median
    0.505; pages printed off-centre reach 0.46). Outside that range the cut goes at the
    centre of the least-inked band, 2% of the page wide, between 0.40 and 0.60: the white
    channel between the columns. A test requiring the darkest column to be 3x the median
    ink was tried and dropped: it rejected the faint rule on ~120 good vol. 1 pages.
    """
    w, h = im.size
    g = im.convert('L').crop((0, int(h * .12), w, int(h * .95)))   # skip the running head
    ink = [255 - v for v in g.resize((w, 1), Image.BOX).getdata()]
    lo, hi = int(w * .38), int(w * .62)
    x = lo + max(range(hi - lo), key=lambda i: ink[lo + i])
    if .44 * w <= x <= .555 * w:
        return x
    lo, hi, win = int(w * .40), int(w * .60), max(3, int(w * .02))
    acc = [0]
    for v in ink: acc.append(acc[-1] + v)
    best = min(range(lo, hi - win), key=lambda s: acc[s + win] - acc[s])
    return best + win // 2


def render(pdf, page, dpi):
    # the process id is in the name: two runs sharing one scratch folder (two Terminal tabs,
    # say) would otherwise write the same file at once, and one reads it half-written
    # ("OSError: image file is truncated", vol. 2, 24 Sep 2026)
    base = SCRATCH / f'{pdf.stem}-{page}-{os.getpid()}'
    subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-gray',
                    '-png', str(pdf), str(base)], check=True, capture_output=True)
    return Path(glob.glob(str(base) + '-*.png')[0])


def ocr_page(pdf, page, dpi, columns, passes=('page.psm6', 'page.psm3')):
    src = render(pdf, page, dpi)
    texts = {k: tess(src, k.split('psm')[1]) for k in passes}
    if columns:
        im = Image.open(src); g = gutter(im); w, h = im.size
        lp, rp = src.with_suffix('.L.png'), src.with_suffix('.R.png')
        im.crop((0, 0, max(1, g - 8), h)).save(lp)
        im.crop((min(w - 1, g + 8), 0, w, h)).save(rp)
        texts['col.psm6'] = tess(lp, '6') + '\n' + tess(rp, '6')
        texts['_gutter'] = round(g / w, 4)
        lp.unlink(missing_ok=True); rp.unlink(missing_ok=True)
    src.unlink(missing_ok=True)
    return texts


def in_order(text, gold):
    """Longest subsequence of headwords appearing in the order the dictionary prints them.

    Recall alone cannot see a scrambled page: every headword can be present and the article
    text between them still belong to the other column. This is the measure that can.
    """
    f = flat(text)
    pos = [f.find(flat(g)) for g in gold if flat(g) in f]
    tails = []
    for p in pos:
        i = bisect_left(tails, p)
        (tails.append(p) if i == len(tails) else tails.__setitem__(i, p))
    return len(tails)


def score(texts, gold):
    fl = {k: flat(v) for k, v in texts.items() if isinstance(v, str)}
    return dict(headwords=len(gold),
                per_pass={k: sum(1 for g in gold if flat(g) in v) for k, v in fl.items()},
                order={k: in_order(v, gold) for k, v in fl.items()},
                union=sum(1 for g in gold if any(flat(g) in v for v in fl.values())),
                missed=[g for g in gold if not any(flat(g) in v for v in fl.values())])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('book')
    ap.add_argument('--budget', type=int, default=150, help='seconds; the shell dies at 180')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--dpi', type=int, default=DPI)
    ap.add_argument('--columns', action='store_true', help='also cut the page at the gutter')
    ap.add_argument('--passes', default='page.psm6,page.psm3',
                    help='whole-page passes to run beside the column pass; "" for none')
    ap.add_argument('--first', type=int, default=1, help='first PDF page to OCR')
    ap.add_argument('--last', type=int, default=0, help='last PDF page to OCR (0: the end)')
    ap.add_argument('--score', action='store_true', help='score what is on disk, OCR nothing')
    a = ap.parse_args()
    idx, start = index(a.book)
    pdf = ROOT / f'pdfs/{a.book}.pdf'
    npdf = int(subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True
                              ).stdout.split('Pages:')[1].split()[0])
    outdir = ROOT / f'ocr/{a.book}/pages'; outdir.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    if not a.score:
        # end to end: the index covers the article pages, but the front and back matter are
        # part of the volume. They are OCR'd with nothing to score against, and recorded as
        # headwords=0 rather than counted as perfect pages.
        todo = [p for p in range(a.first, (a.last or npdf) + 1) if not (outdir / f'p{p:04d}.json').exists()]
        t0 = time.time(); n = 0
        def work(p):
            if time.time() - t0 > a.budget: return None
            if (outdir / f'p{p:04d}.json').exists(): return None   # another run got there first
            try:
                texts = ocr_page(pdf, p, a.dpi, a.columns, [x for x in a.passes.split(',') if x])
            except OSError as e:
                print(f'p. {p}: {e}; skipped, re-run to retry', flush=True); return None
            gold = idx.get(p, [])
            rec = dict(pdf_page=p, index_page=p - start, dpi=a.dpi, indexed=p in idx,
                       **score(texts, gold), text=texts)
            (outdir / f'p{p:04d}.json').write_text(json.dumps(rec, ensure_ascii=False))
            return p
        with ThreadPoolExecutor(a.workers) as ex:
            for r in ex.map(work, todo):
                if r: n += 1
        print(f'+{n} pages this slice, {len(todo)-n} of {npdf} still to do')

    got = sorted(outdir.glob('p*.json'))
    tot = hit = 0; per = {}; order = {}
    for f in got:
        d = json.loads(f.read_text())
        if not d['headwords']: continue
        tot += d['headwords']; hit += d['union']
        for k, v in d['per_pass'].items(): per[k] = per.get(k, 0) + v
        for k, v in (d.get('order') or {}).items(): order[k] = order.get(k, 0) + v
    if tot:
        print(f'{len(got)}/{npdf} pages on disk · {hit:,}/{tot:,} headwords verbatim '
              f'= {100*hit/tot:.1f}% (union)')
        for k in sorted(per):
            o = f'  in order {100*order[k]/tot:5.1f}%' if k in order else ''
            print(f'   {k:12} {100*per[k]/tot:5.1f}%{o}')


if __name__ == '__main__':
    main()
