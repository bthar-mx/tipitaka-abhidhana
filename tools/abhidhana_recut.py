#!/usr/bin/env python3
"""Check where each page was cut into columns, and re-read the pages cut in the wrong place.

    python3 tools/abhidhana_recut.py 08 --scan --workers 10 # which pages to re-cut (no OCR)
    python3 tools/abhidhana_recut.py 08 --run --workers 10  # re-read their column pass
    python3 tools/abhidhana_recut.py 08 --report            # recall before and after

Why. `abhidhana_ocr.py` cuts at the darkest column of the middle of the page, accepted inside
0.44-0.555 of the width. On some pages that column is not the printed rule but a stack of
bold headwords at the left edge of the right-hand column, or the right-hand text itself: vol. 8
p. 500 was cut at 0.554, through the first letters of every headword in the right column
(brief §22). Pages cut at >= 0.54 read 69-79% of their headwords in the column pass in vols. 2,
6 and 8, against about 88% on the rest. On others a thick rule (vol. 7 p. 527, 13 px) is cut at
its edge and a strip of it stays in the right column's image.

How. The page (rows 12-95%, so the running head does not count) is divided into 100 horizontal
bands, and each pixel column is white where it carries no ink in more than one band. White runs
of at least 4 px between 0.40 and 0.60 of the width, separated only by a band of at most 1.5%
(the rule, whole or broken), form the channel; the group with the most white is taken. A band
count and not a mean: the hanging indent of the right-hand column is crossed only by the
headwords, so its mean ink can be as low as a gutter's, but its band count is not.

A page is re-read when either edge of its old crops (the old cut ± 8 px) is not in the channel's
white: the cut went through text, or a thick rule reached into a crop. The left column is then
cut at the middle of the channel's first white run and the right column starts at the middle of
its last, so neither image holds any of the rule. Pages where no channel is found are left alone
and listed.

Measured on vol. 8 (37 pages re-read in the cloud container, 25 Sep 2026): the 25 pages cut
through text went from 78.4% to 88.9% of their headwords in the column pass (worse on 4); the 12
with a thick rule in a crop from 87.6% to 86.5% (worse on 2). So --run re-reads only pages cut
through text, and keeps a new reading only if it finds at least as many headwords as the old
one: the choice between two readings of one page uses the index, like the rest of the pipeline,
and a rejected cut is recorded as `_cut_rejected`.

--scan writes ocr/<book>/recut.json. --run keeps the old column text as `col.psm6.cut0` and
`_gutter_cut0`, writes the new as `col.psm6` with `_cut` = [left end, right start] as fractions
of the width, and re-scores the record; it skips pages already done (`_cut` or `_cut_rejected`),
so it can be stopped and resumed. It does not touch abhidhana_ocr.py, which can run at the same time on
another book. After it, run abhidhana_articles.py and abhidhana_romanise.py for the book again.
"""
import argparse, json, os, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abhidhana_ocr import ROOT, SCRATCH, index, render, score, tess
from PIL import Image
warnings.filterwarnings('ignore', category=DeprecationWarning)

BANDS, MARGIN = 100, 8


def darkness(im):
    """for each pixel column, in how many of 100 horizontal bands (rows 12-95% of the page) it
    carries ink. A gutter is ink-free in every band; the rule is inked in nearly all; a
    column of text in most. A mean over the whole height (what abhidhana_ocr.py uses) cannot
    tell a gutter from the hanging indent of the right-hand column, which only the headwords
    cross: a band count can."""
    w, h = im.size
    g = im.convert('L').crop((0, int(h * .12), w, int(h * .95))).resize((w, BANDS), Image.BOX)
    px = g.load()
    return [sum(1 for y in range(BANDS) if px[x, y] < 247) for x in range(w)]


def channel(im):
    """(white runs of the channel, in order) as [(a, b), ...] in pixels, or None"""
    w = im.size[0]; dark = darkness(im)
    lo, hi = int(w * .40), int(w * .60)
    runs, s = [], None
    for x in range(lo, hi + 1):
        white = x < hi and dark[x] <= 1
        if white and s is None: s = x
        if not white and s is not None:
            if x - s >= 4: runs.append((s, x))
            s = None
    if not runs: return None, dark
    # runs separated only by a rule (a band <= 1.5% wide) are one channel; the channel is the
    # group with the most white in it
    groups = [[runs[0]]]
    for r in runs[1:]:
        if r[0] - groups[-1][-1][1] <= int(w * .015): groups[-1].append(r)
        else: groups.append([r])
    g = max(groups, key=lambda gr: sum(b - a for a, b in gr))
    return g, dark


def decide(im, old):
    """(left end, right start) in pixels and why, or (None, why) to leave the page alone.

    The old cut is good when both crop edges, old ± 8 px, fall in the channel's white; the
    page is then left alone whatever the old cut's position."""
    w = im.size[0]; g, dark = channel(im)
    if g is None: return None, 'no channel'
    ox = int(round(old * w))
    inwhite = lambda x: any(a <= x < b for a, b in g)
    if inwhite(ox - MARGIN) and inwhite(ox + MARGIN): return None, 'ok'
    first, last = g[0], g[-1]
    if first == last:
        m = (first[0] + first[1]) // 2; cut = (m - MARGIN, m + MARGIN)
    else:
        cut = ((first[0] + first[1]) // 2, (last[0] + last[1]) // 2)
    how = 'rule in a crop' if g[0][0] - int(w * .01) <= ox <= g[-1][1] + int(w * .01) else 'cut through text'
    return cut, how


def pages_of(book):
    d = ROOT / f'ocr/{book}/pages'
    for f in sorted(d.glob('p*.json')):
        rec = json.loads(f.read_text())
        if rec.get('indexed') and '_gutter' in rec['text']: yield f, rec


def rendered(pdf, pages, dpi, chunk=40):
    """(page, image) for each page, rendering a run of pages per pdftoppm call: one call per
    page reopens the PDF each time and was ten times slower on a 36 MB book"""
    import glob, subprocess
    pages = sorted(pages)
    for i in range(0, len(pages), chunk):
        part = pages[i:i + chunk]; base = SCRATCH / f'recut-{pdf.stem}-{os.getpid()}-{part[0]}-'
        subprocess.run(['pdftoppm', '-f', str(part[0]), '-l', str(part[-1]), '-r', str(dpi), '-gray',
                        '-png', str(pdf), str(base)], check=True, capture_output=True)
        files = {int(Path(f).stem.rsplit('-', 1)[1]): f for f in glob.glob(str(base) + '-*.png')}
        for p in part:
            im = Image.open(files[p]); im.load(); yield p, im
        for f in files.values(): os.unlink(f)


def suspects(rec):
    """a page whose record hints at a bad cut: gutter near either edge of the accepted range,
    the whole-page pass reading 3+ headwords more than the column pass, or the column pass
    reading under 70%"""
    g = rec['text']['_gutter']; c = rec['per_pass'].get('col.psm6', 0)
    return (not .46 <= g <= .54 or rec['per_pass'].get('page.psm6', 0) - c >= 3
            or c < .7 * rec['headwords'])


def scan(book, which='all', workers=4):
    pdf = ROOT / f'pdfs/{book}.pdf'; SCRATCH.mkdir(parents=True, exist_ok=True)
    recs = {rec['pdf_page']: rec for _, rec in pages_of(book)}
    if which == 'suspects': recs = {p: r for p, r in recs.items() if suspects(r)}
    elif which != 'all':
        keep = {int(x) for x in which.split(',')}; recs = {p: r for p, r in recs.items() if p in keep}
    dpis = {r['dpi'] for r in recs.values()}
    if len(dpis) != 1: sys.exit(f'{book}: pages were read at several dpi: {dpis}')
    dpi = dpis.pop(); pages = sorted(recs)
    def part(ps):
        res = []
        for p, im in rendered(pdf, ps, dpi):
            rec = recs[p]; w = im.size[0]
            cut, how = decide(im, rec['text'].get('_gutter_cut0', rec['text']['_gutter']))
            res.append((p, w, cut, how))
        return res
    # contiguous runs of at most 40 pages, one pdftoppm call each, spread over the workers
    runs, cur = [], []
    for p in pages:
        if cur and (p != cur[-1] + 1 or len(cur) == 40): runs.append(cur); cur = []
        cur.append(p)
    if cur: runs.append(cur)
    out, why = {}, {}
    with ThreadPoolExecutor(workers) as ex:
        for res in ex.map(part, runs):
            for p, w, cut, how in res:
                rec = recs[p]; why[how] = why.get(how, 0) + 1
                if cut:
                    out[p] = dict(old=rec['text']['_gutter'], cut=[round(cut[0] / w, 4), round(cut[1] / w, 4)],
                                  why=how, col=rec['per_pass'].get('col.psm6'), headwords=rec['headwords'])
                elif how == 'no channel':
                    out[p] = dict(old=rec['text']['_gutter'], cut=None, why=how)
    out = dict(sorted(out.items()))
    (ROOT / f'ocr/{book}/recut.json').write_text(json.dumps(out, indent=1))
    todo = [v for v in out.values() if v['cut']]
    print(f'{book}: {len(recs)} indexed pages scanned ({which}); ' + ', '.join(f'{k} {v}' for k, v in sorted(why.items())))
    if todo:
        c = sum(v['col'] for v in todo); h = sum(v['headwords'] for v in todo)
        print(f'  to re-read: {len(todo)} pages, whose column pass now reads {c}/{h} = {100 * c / h:.1f}%')
    print(f'  written ocr/{book}/recut.json')


def run(book, workers, reasons=('cut through text',)):
    from abhidhana_ocr import flat
    pdf = ROOT / f'pdfs/{book}.pdf'; SCRATCH.mkdir(parents=True, exist_ok=True)
    plan = json.loads((ROOT / f'ocr/{book}/recut.json').read_text())
    idx, _ = index(book)
    def work(p):
        f = ROOT / f'ocr/{book}/pages/p{int(p):04d}.json'
        rec = json.loads(f.read_text()); t = rec['text']
        if '_cut' in t or '_cut_rejected' in t or not plan[p]['cut'] or plan[p]['why'] not in reasons:
            return 0, 0
        src = render(pdf, int(p), rec['dpi']); im = Image.open(src); w, h = im.size
        a, b = plan[p]['cut']; lp, rp = src.with_suffix('.L.png'), src.with_suffix('.R.png')
        im.crop((0, 0, max(1, int(a * w)), h)).save(lp)
        im.crop((min(w - 1, int(b * w)), 0, w, h)).save(rp)
        new = tess(lp, '6') + '\n' + tess(rp, '6')
        for x in (lp, rp, src): x.unlink(missing_ok=True)
        gold = idx.get(int(p), [])
        hit = lambda text: sum(1 for g in gold if flat(g) in flat(text))
        if hit(new) < hit(t['col.psm6']):
            # the new cut reads fewer headwords: keep the old text, and say so
            t['_cut_rejected'] = [a, b]; f.write_text(json.dumps(rec, ensure_ascii=False)); return 1, 0
        t['col.psm6.cut0'] = t['col.psm6']; t['_gutter_cut0'] = t['_gutter']
        t['col.psm6'] = new; t['_cut'] = [a, b]
        rec.update(score({k: v for k, v in t.items() if k in ('col.psm6', 'page.psm6', 'page.psm3')}, gold))
        f.write_text(json.dumps(rec, ensure_ascii=False))
        return 1, 1
    t0 = time.time()
    with ThreadPoolExecutor(workers) as ex: res = list(ex.map(work, list(plan)))
    print(f'{book}: {sum(r[0] for r in res)} pages re-read in {time.time() - t0:.0f} s, '
          f'{sum(r[1] for r in res)} kept (the rest read fewer headwords and were not kept)')
    report(book)


def report(book):
    from abhidhana_ocr import flat
    idx, _ = index(book); n = h = before = after = 0
    for f, rec in pages_of(book):
        t = rec['text']
        if '_cut' not in t: continue
        gold = idx.get(rec['pdf_page'], []); n += 1; h += len(gold)
        before += sum(1 for g in gold if flat(g) in flat(t['col.psm6.cut0']))
        after += sum(1 for g in gold if flat(g) in flat(t['col.psm6']))
    if n:
        print(f'{book}: {n} pages re-cut; column pass {before}/{h} = {100 * before / h:.1f}% before, '
              f'{after}/{h} = {100 * after / h:.1f}% after')
    else:
        print(f'{book}: no page re-cut yet')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('book')
    ap.add_argument('--scan', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--pages', default='all',
                    help='all (default), suspects, or a comma-separated list of PDF pages')
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    if a.scan: scan(a.book, a.pages, a.workers)
    if a.run: run(a.book, a.workers)
    if a.report: report(a.book)
