#!/usr/bin/env python3
"""Build the Abhidhāna Reader's data file for one volume.

    python3 tools/abhidhana_reader_data.py 01      ->  reader/vol01.json

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
as vol<book>.json. Without `lo`, and run on commit 40e6be1's data, this reproduces the
vol01.json that was first published byte for byte.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
X = {'verbatim': 'v', 'verbatim-inline': 'v', 'fuzzy': 'f', 'unlocated': 'u'}


def main(book):
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
    print(f'{out.relative_to(ROOT)}: {len(V):,} records, {out.stat().st_size / 1e6:.1f} MB')


if __name__ == '__main__':
    main(sys.argv[1])
