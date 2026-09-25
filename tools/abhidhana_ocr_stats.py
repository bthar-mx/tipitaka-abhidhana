#!/usr/bin/env python3
"""Figures for a book's ocr-report.md, from its page records.

    python3 tools/abhidhana_ocr_stats.py 23 24

Prints: page counts (front matter, indexed, unindexed inside the body, back matter), headwords,
dpi, recall (verbatim, folded, per pass, in printed order), whole / >= 90% / >= 80% / < 50% pages,
the gutter's median and spread and the pages cut at >= 0.54 (brief §22), recall per hundred
pages, and the eight worst pages. Written 25 Sep 2026 for vols. 23 and 24.
"""
import json, sys, sqlite3, statistics, subprocess, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'tools'))
for book in sys.argv[1:]:
    c = sqlite3.connect(f'file:{ROOT}/db/tipitaka_abidan.db?mode=ro', uri=True)
    start, = c.execute('select start_page from books where id=?', (book,)).fetchone()
    rows = c.execute('select word,page_number from words where book_id=?', (book,)).fetchall()
    from abhidhana_ocr import index   # with the index's page errors corrected (PAGE_FIX, ID_PAGE_FIX)
    idxpages = set(index(book)[0])
    npdf = int(subprocess.run(['pdfinfo', str(ROOT/f'pdfs/{book}.pdf')], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0])
    recs = [json.loads(f.read_text()) for f in sorted((ROOT/f'ocr/{book}/pages').glob('p*.json'))]
    ind = [r for r in recs if r['headwords']]
    tot = sum(r['headwords'] for r in ind); U = sum(r['union'] for r in ind); UF = sum(r.get('union_folded', r['union']) for r in ind)
    pp = {}; od = {}
    for r in ind:
        for k, v in r['per_pass'].items(): pp[k] = pp.get(k, 0)+v
        for k, v in r['order'].items(): od[k] = od.get(k, 0)+v
    lo, hi = min(idxpages), max(idxpages)
    front = lo-1; back = npdf-hi; inside = sum(1 for p in range(lo, hi+1) if p not in idxpages)
    full = sum(1 for r in ind if r['union'] == r['headwords'])
    ge = lambda t: 100*sum(1 for r in ind if r['union'] >= t*r['headwords'])/len(ind)
    below50 = sum(1 for r in ind if r['union'] < .5*r['headwords'])
    g = [r['text'].get('_gutter') for r in ind if r['text'].get('_gutter') is not None]
    hig = [r for r in ind if (r['text'].get('_gutter') or 0) >= .54]
    higr = sum(r['per_pass'].get('col.psm6', 0) for r in hig)/max(1, sum(r['headwords'] for r in hig))
    byh = []
    for k in range(0, npdf, 100):
        rr = [r for r in ind if k < r['pdf_page'] <= k+100]
        if rr: byh.append(round(100*sum(r['union'] for r in rr)/sum(r['headwords'] for r in rr)))
    missed = [m for r in ind for m in r['missed']]
    worst = sorted(ind, key=lambda r: (r['union']/r['headwords'], -r['headwords']))[:8]
    dpis = {r['dpi'] for r in recs}
    print(f'== {book}: {npdf} PDF pages; front {front}, indexed {len(idxpages)} (OCR recs with headwords {len(ind)}), inside-unindexed {inside}, back {back}; start_page {start}')
    print(f'headwords {len(rows):,} distinct {len({w for w,_ in rows}):,}; dpi {dpis}')
    print(f'verbatim {U:,}/{tot:,} = {100*U/tot:.1f}%; folded {100*UF/tot:.1f}%')
    for k in sorted(pp): print(f'  {k}: {100*pp[k]/tot:.1f}%  order {100*od[k]/tot:.1f}%')
    print(f'full pages {full}/{len(ind)} = {100*full/len(ind):.1f}%; >=90 {ge(.9):.1f}%; >=80 {ge(.8):.1f}%; <50: {below50}')
    print(f'gutter median {statistics.median(g):.3f} sd {statistics.pstdev(g):.3f}; >=0.54: {len(hig)} pages, col recall {100*higr:.1f}%')
    print('by hundred:', byh, 'median missed len', statistics.median(len(m) for m in missed) if missed else '-')
    print('worst:', ', '.join(f"p. {r['pdf_page']} ({r['union']} of {r['headwords']})" for r in worst))
