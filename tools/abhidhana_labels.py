#!/usr/bin/env python3
"""The grammatical labels: one table, in docs/labels.md §0, read by the pipeline and the site.

    from abhidhana_labels import LABELS   # [{label, roman, printed, pali, en, es, abbr_en, abbr_es, status, es_status, source, readings}]
    python3 tools/abhidhana_labels.py           # print the table as parsed, and check it

The table sits between the markers <!-- labels:begin --> and <!-- labels:end --> in
docs/labels.md. One row per printed label:

    | label | roman | printed | Pāḷi | English | Spanish | abbr. en | abbr. es | status | es | source | OCR readings |

Columns are found by their header, so their order may change and new ones may be added.

- label      the label as printed, without brackets
- roman      the printed label romanised, with brackets: (ti), (pu, na); what the Pāḷi reader shows
- printed    the dictionary's own expansion, from its tables of abbreviations (docs/abbreviations.md)
- Pāḷi       its expansion (IAST); a trailing ? marks a term for the editor to confirm
- English, Spanish   what it marks, in words, as the site's pop-up shows it
- abbr. en, abbr. es the short gloss shown beside the label; empty = none shown
- status     confirmed (the editor has agreed it), printed (the dictionary itself gives the meaning),
             or provisional (our reading of the dictionary's usage)
- es         confirmed or draft: whether the Spanish words are agreed
- source     where the meaning is printed, or how it was inferred
- OCR readings   every reading tools/abhidhana_articles.py maps to this label, space-separated,
             spaces inside a reading removed. Add a reading only after checking it on the image.

Written 25 Sep 2026; until then the readings were a dict in abhidhana_articles.py
(_LABEL_READINGS), and the table reproduces it exactly.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / 'docs/labels.md'
HEAD = {'label': 'label', 'roman': 'roman', 'printed': 'printed', 'pāḷi': 'pali', 'english': 'en', 'spanish': 'es',
        'abbr. en': 'abbr_en', 'abbr. es': 'abbr_es', 'status': 'status', 'es': 'es_status',
        'source': 'source', 'ocr readings': 'readings'}
NEEDED = ('label', 'pali', 'en', 'es', 'status', 'es_status', 'readings')
STATUS = ('confirmed', 'printed', 'provisional')


def load(path=DOC):
    s = path.read_text(encoding='utf-8')
    m = re.search(r'<!-- labels:begin -->(.*?)<!-- labels:end -->', s, re.S)
    if not m: sys.exit(f'{path}: no <!-- labels:begin --> ... <!-- labels:end --> table')
    lines = [l for l in m.group(1).splitlines() if l.strip().startswith('|')]
    cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
    head = [HEAD.get(h.lower(), h.lower()) for h in cells(lines[0])]
    miss = [k for k in NEEDED if k not in head]
    if miss: sys.exit(f'{path}: the label table has no column for {miss}')
    out = []
    for l in lines[2:]:
        c = cells(l)
        if len(c) != len(head): sys.exit(f'{path}: a label row has {len(c)} cells, not {len(head)}: {l}')
        d = {k: '' for k in HEAD.values()} | dict(zip(head, c))
        d['label'] = d['label'].strip('()')
        d['readings'] = d['readings'].split()
        if d['status'] not in STATUS: sys.exit(f'{path}: status must be one of {STATUS}: {l}')
        if d['es_status'] not in ('confirmed', 'draft'): sys.exit(f'{path}: es must be confirmed/draft: {l}')
        out.append(d)
    seen = {}
    for d in out:
        for r in d['readings']:
            if r in seen: sys.exit(f'{path}: reading {r} is mapped to both ({seen[r]}) and ({d["label"]})')
            seen[r] = d['label']
    return out


LABELS = load()

if __name__ == '__main__':
    for d in LABELS:
        print(f"({d['label']}) {d['pali']} · {d['en']} · {d['es']} [{d['status']}/{d['es_status']}] {len(d['readings'])} readings")
    print(f'{len(LABELS)} labels, {sum(len(d["readings"]) for d in LABELS)} readings')
