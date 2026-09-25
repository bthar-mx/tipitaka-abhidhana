#!/usr/bin/env python3
"""Build the Abhidhāna Reader's data file for one volume.

    python3 tools/abhidhana_reader_data.py 01 [02 ...]  ->  reader/vol01.json (+ .wasm), and reader/search.json

search.json is rebuilt each time from every reader/vol*.json present: one row per headword,
[book, i, p, h, r] (i is the record's position in vol<book>.json), so the Reader can search all
volumes without loading them.

Reads ocr/<book>/articles.jsonl and ocr/<book>/pali.jsonl (run abhidhana_articles.py and
abhidhana_romanise.py first) and writes one compact record per headword, in index order:

    p  PDF page          q  index (printed) page     h  headword (index spelling)
    r  headword, IAST    o  OSBCT: word / inside / none
    x  located: v (verbatim, incl. inline) / f (fuzzy) / u (unlocated)
    l  label, normalised (docs/labels.md)            lo label as the OCR read it, when different
    a  compound analysis ai analysis, IAST
    b  definition, line-break hyphens joined         sp Pāḷi spans in b: [start, end, IAST]
    c  citations         ci citations, romanised

The page itself is the private artifact "Abhidhāna Reader"; this file is published beside it
gzipped, as vol<book>.wasm (and search.wasm): the gzip bytes under a .wasm name, because
artifacts serve .wasm as binary and do not serve .gz. Eight volumes as plain JSON passed the
artifact's 64 MB per version (25 Sep 2026); twenty-one as base64 text (.gz.txt, until 25 Sep
2026) reached 63.5 MB, and base64 costs a third. As raw gzip, twenty-four books are ~52 MB. The
page inflates them with DecompressionStream. Without `lo`, and run on commit 40e6be1's data, this reproduces the
vol01.json that was first published byte for byte.
"""
import gzip, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
X = {'verbatim': 'v', 'verbatim-inline': 'v', 'folded': 'v', 'fuzzy': 'f', 'unlocated': 'u'}


def main(book, index=True):
    P = {}
    for line in (ROOT / f'ocr/{book}/pali.jsonl').open():
        r = json.loads(line); P[r['id']] = r
    V = []
    for line in (ROOT / f'ocr/{book}/articles.jsonl').open():
        r = json.loads(line); p = P[r['id']]
        d = {'p': r['pdf_page'], 'q': r['index_page'], 'h': r['headword'], 'r': r['iast']}
        if r.get('osbct'): d['o'] = r['osbct']
        d['x'] = X[r['located']]
        if r.get('label'): d['l'] = r['label']
        if r.get('label_ocr') and r['label_ocr'] != r.get('label'): d['lo'] = r['label_ocr']
        if r.get('analysis'): d['a'] = r['analysis']
        b = p.get('body_joined') or re.sub(r'-\s*\n\s*', '', r.get('body') or '').replace('\n', ' ')
        if b: d['b'] = b
        if r.get('citations'): d['c'] = r['citations']
        if p.get('analysis_iast'): d['ai'] = p['analysis_iast']
        if p.get('citations_iast'): d['ci'] = p['citations_iast']
        if p.get('pali'): d['sp'] = [[s['start'], s['end'], s['iast']] for s in p['pali']]
        V.append(d)
    out = ROOT / f'reader/vol{book}.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(V, ensure_ascii=False, separators=(',', ':')))
    gz(out)
    print(f'{out.relative_to(ROOT)}: {len(V):,} records, {out.stat().st_size / 1e6:.1f} MB '
          f'({out.with_suffix(".wasm").stat().st_size / 1e6:.1f} MB as .wasm)')
    if index: search_index()


def gz(path):
    """<stem>.wasm beside path: gzip bytes (reproducible: no name or time in the header)"""
    path.with_suffix('.wasm').write_bytes(gzip.compress(path.read_bytes(), compresslevel=9, mtime=0))


def search_index():
    S = []
    for f in sorted((ROOT / 'reader').glob('vol*.json')):
        book = f.stem[3:]
        for i, d in enumerate(json.loads(f.read_text())):
            S.append([book, i, d['p'], d['h'], d['r']])
    out = ROOT / 'reader/search.json'
    out.write_text(json.dumps(S, ensure_ascii=False, separators=(',', ':')))
    gz(out)
    print(f'{out.relative_to(ROOT)}: {len(S):,} headwords from {len({r[0] for r in S})} volumes, '
          f'{out.stat().st_size / 1e6:.1f} MB ({out.with_suffix(".wasm").stat().st_size / 1e6:.1f} MB as .wasm)')


if __name__ == '__main__':
    for b in sys.argv[1:]: main(b, index=False)
    search_index()
