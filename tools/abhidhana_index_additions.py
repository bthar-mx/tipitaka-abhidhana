#!/usr/bin/env python3
"""Headwords the app's index lacks, added as index rows (docs/index-additions.tsv; brief §97).

The app's index (db/tipitaka_abidan.db) is the project's ground truth, but in one place it has a hole: in vol.
14/1 it runs from 113054 ပပဉ္စသညာသင်္ခါနိရောဓသာရုပ္ပဂါမိနီ (PDF p. 695) straight to 113055 ပဗ္ဗာဇေတုံ (p. 777),
ids consecutive, so the ~80 pages between have no index row at all (pabbata, pabbajita, pabbajjā ... were not
searchable, and the article step read all their text into 113054). PCED, typed from the same dictionary, has
the 587 entries of that stretch: their headwords become index rows here, with ids of our own (300001 on, so
that no id can be taken for one of the app's), each placed after an index row of its book in print order.

    python3 tools/abhidhana_index_additions.py build     # (re)write the table from witness/pced_k.jsonl,
                                                         # keeping pdf_page / page_how / note already set
    python3 tools/abhidhana_index_additions.py pages 14  # on the Mac: the PDF page of each row, read from
                                                         # ocr/14/pages/ (needs no db); then the article step
    python3 tools/abhidhana_index_additions.py check     # the table's own consistency (anywhere)

Columns: id, book, after_id (the index row the gap follows; the rows of one gap follow it in table order),
pdf_page and page_how (filled by `pages`: `line` = the headword begins a line on that page, exact or by the
spelling folds; `between` = not found at a line start, given the page of the row found before it, so the
article step's fuzzy pass looks for it there), headword (PCED's spelling, converted from Zawgyi), iast
(PCED's own romanised key), pced_seq (the witness row), label_pced, note.
Rows with no pced_seq were read from the page image (books without PCED; brief §97): page_how `image`, the
headword as printed (homonym numbers left out, as the index does), iast by Aksharamukha; `build` keeps them.

Read by tools/abhidhana_articles.py (the rows join the index rows of their page, so the article step cuts
their text out of the host's) and tools/abhidhana_witness_join.py (they pair with PCED as index rows do).
A row without pdf_page is skipped by the article step, with a message: run `pages` first.
"""
import csv, json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TSV = ROOT / 'docs/index-additions.tsv'
COLS = ['id', 'book', 'after_id', 'pdf_page', 'page_how', 'headword', 'iast', 'pced_seq', 'label_pced', 'note']
# (book, the index row before the gap, the index row after it, first id, PDF pages the gap may touch)
GAPS = [('14', 113054, 113055, 300001, (695, 777))]
nfc = lambda s: unicodedata.normalize('NFC', s or '')
SP = lambda s: re.sub(r'\s', '', s or '')


def additions(book=None):
    """the table's rows (dicts, ints where they are numbers), in table order; [] if there is no table"""
    if not TSV.exists(): return []
    out = []
    for r in csv.DictReader(TSV.open(encoding='utf-8'), delimiter='\t'):
        if book and r['book'] != book: continue
        r = dict(r)
        for k in ('id', 'after_id'): r[k] = int(r[k])
        r['pced_seq'] = int(r['pced_seq']) if r.get('pced_seq') else None   # empty: read from the image
        r['pdf_page'] = int(r['pdf_page']) if r.get('pdf_page') else None
        r['headword'] = nfc(r['headword'])
        out.append(r)
    return out


def write(rows):
    with TSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, COLS, delimiter='\t', lineterminator='\n')
        w.writeheader()
        for r in rows: w.writerow({k: ('' if r.get(k) is None else r.get(k)) for k in COLS})


def _key():
    sys.path.insert(0, str(ROOT / 'tools'))
    from abhidhana_browse import letters, LETTERS
    rank = {ro: i for i, (ro, _) in enumerate(LETTERS)}; rank['ṁ'] = -2
    return lambda r: tuple(rank.get(x, 99) for x in letters(nfc(r).replace('ṃ', 'ṁ'))) + (-1,)


def _iast_of(book, ids):
    got = {}
    for l in open(ROOT / f'ocr/{book}/articles.jsonl', encoding='utf-8'):
        r = json.loads(l)
        if r['id'] in ids: got[r['id']] = r['iast']
    return got


def build():
    """the PCED entries whose romanised key sorts strictly between the two index rows around each gap"""
    key = _key()
    W = [json.loads(l) for l in open(ROOT / 'witness/pced_k.jsonl', encoding='utf-8')]
    old = {r['pced_seq']: r for r in additions() if r['pced_seq']}
    rows = []
    for book, before, after, first, _ in GAPS:
        ia = _iast_of(book, {before, after})
        lo, hi = key(ia[before]), key(ia[after])
        got = sorted((d for d in W if lo < key(d['key']) < hi), key=lambda d: (key(d['key']), d['seq']))
        for n, d in enumerate(got):
            o = old.get(d['seq'], {})
            rows.append({'id': first + n, 'book': book, 'after_id': before, 'pdf_page': o.get('pdf_page'),
                         'page_how': o.get('page_how', ''), 'headword': nfc(d['headword']),
                         'iast': nfc(d['key'].replace('ṃ', 'ṁ')), 'pced_seq': d['seq'],
                         'label_pced': d.get('label', ''), 'note': o.get('note', '')})
        print(f'vol. {book}: {len(got)} PCED entries between {before} {ia[before]} and {after} {ia[after]} '
              f'(ids {first}–{first + len(got) - 1})')
    rows += [r for r in additions() if not r['pced_seq']]   # the rows read from the image are kept as they are
    write(rows)


def place(heads, rows, fold):
    """heads: [(page, line no., text without spaces)] in reading order; rows: the gap's rows in table order.
    Each row takes one line that begins with its headword (exact, else after the spelling folds), the lines
    chosen in increasing order and as many rows placed as can be (longest chain). -> {id: (page, how)}"""
    import bisect
    OK = set('([-') | set('၀၁၂၃၄၅၆၇၈၉¹²³⁴⁵')
    fl = [fold(s) for _, _, s in heads]
    occ = []
    for r in rows:
        h = SP(r['headword']); fh = fold(h); o = []
        for j, (_, _, s) in enumerate(heads):
            if s.startswith(h) and (len(s) == len(h) or s[len(h)] in OK): o.append(j)
            elif fl[j].startswith(fh) and (len(fl[j]) == len(fh) or fl[j][len(fh)] in OK): o.append(j)
        occ.append(o)
    tails, refs, prev = [], [], {}
    for ci, o in enumerate(occ):
        for j in sorted(o, reverse=True):   # descending, so one row takes at most one line
            k = bisect.bisect_left(tails, j)
            node = (ci, j); prev[node] = refs[k - 1] if k else None
            if k == len(tails): tails.append(j); refs.append(node)
            else: tails[k] = j; refs[k] = node
    chain, n = [], (refs[-1] if refs else None)
    while n: chain.append(n); n = prev[n]
    on = {ci: j for ci, j in chain}
    out, last = {}, None
    for ci, r in enumerate(rows):
        if ci in on: last = heads[on[ci]][0]; out[r['id']] = (last, 'line')
        else: out[r['id']] = (last if last is not None else heads[0][0], 'between')
    return out


def pages(book):
    """the PDF page of each row of the book's gaps, from ocr/<book>/pages/ (the column-cut OCR)"""
    sys.path.insert(0, str(ROOT / 'tools'))
    from abhidhana_articles import page_text
    from abhidhana_fold import fold
    rows = additions()
    for gbook, before, after, _, (p0, p1) in GAPS:
        if gbook != book: continue
        g = [r for r in rows if r['book'] == book and r['after_id'] == before]
        arts = {}
        for l in open(ROOT / f'ocr/{book}/articles.jsonl', encoding='utf-8'):
            a = json.loads(l)
            if a['id'] in (before, after): arts[a['id']] = a
        heads = []
        for q in range(p0, p1 + 1):
            fp = ROOT / f'ocr/{book}/pages/p{q:04d}.json'
            if not fp.exists(): print(f'p. {q}: no OCR page file'); continue
            for i, ln in enumerate(page_text(json.loads(fp.read_text(encoding='utf-8'))).split('\n')):
                if SP(ln): heads.append((q, i, SP(ln)))
        # only the lines after the host's head line on its page, and before the next index row's on its own
        def cut(aid, side):
            a = arts.get(aid)
            if not a or a.get('located') == 'unlocated': return None
            h = fold(SP(a.get('headword_ocr') or a['headword']))
            js = [j for j, (q, _, s) in enumerate(heads) if q == a['pdf_page'] and fold(s).startswith(h)]
            return js[0] if js else None
        j0, j1 = cut(before, 'before'), cut(after, 'after')
        span = heads[(j0 + 1 if j0 is not None else 0):(j1 if j1 is not None else len(heads))]
        if j0 is None: print(f'{before}: its head line not found on p. {arts.get(before, {}).get("pdf_page")}; all of it searched')
        if j1 is None: print(f'{after}: its head line not found on p. {arts.get(after, {}).get("pdf_page")}; all of it searched')
        got = place(span, g, fold)
        for r in g: r['pdf_page'], r['page_how'] = got[r['id']]
        n_line = sum(1 for r in g if r['page_how'] == 'line')
        per = {}
        for r in g: per[r['pdf_page']] = per.get(r['pdf_page'], 0) + 1
        empty = [q for q in range(p0 + 1, p1) if q not in per]
        print(f'vol. {book}, after {before}: {len(g)} rows; {n_line} found at a line start, {len(g) - n_line} between; '
              f'pages {min(per)}–{max(per)}; gap pages with no row: {empty or "none"}')
    write(rows)


def check():
    rows = additions(); bad = []
    ids = [r['id'] for r in rows]
    if len(ids) != len(set(ids)): bad.append('ids repeat')
    if ids and min(ids) <= 221154: bad.append('an id inside the app index range (1-221154)')
    key = _key()
    for book, before, after, first, _ in GAPS:
        g = [r for r in rows if r['book'] == book and r['after_id'] == before and r['pced_seq']]
        ks = [key(r['iast']) for r in g]
        if ks != sorted(ks): bad.append(f'{book}: rows out of key order')
        if [r['id'] for r in g] != list(range(first, first + len(g))): bad.append(f'{book}: ids not consecutive from {first}')
        un = [r['id'] for r in g if not r['pdf_page']]
        print(f'vol. {book}, after {before}: {len(g)} rows, ids {first}–{first + len(g) - 1}; '
              f'pages {"not yet set (run `pages %s` on the Mac)" % book if un else "set"}'
              + (f"; {sum(1 for r in g if r['page_how'] == 'between')} placed between" if not un else ''))
    img = [r for r in rows if not r['pced_seq']]
    if any(not r['pdf_page'] for r in img): bad.append('a row read from the image has no pdf_page')
    if img: print(f'read from the image: {len(img)} rows in {len({(r["book"], r["pdf_page"]) for r in img})} pages '
                  f'(ids {min(r["id"] for r in img)}–{max(r["id"] for r in img)})')
    print('check: ' + ('; '.join(bad) if bad else 'ok'))
    return not bad


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'build': build()
    elif cmd == 'pages': pages(sys.argv[2])
    elif cmd == 'check': sys.exit(0 if check() else 1)
    else: sys.exit(__doc__)
