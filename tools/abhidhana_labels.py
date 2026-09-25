#!/usr/bin/env python3
"""The grammatical labels: one table, in docs/labels.md §0, read by the pipeline and the site.

    from abhidhana_labels import LABELS         # [{label, pali, en, es, abbr_en, abbr_es, status, es_status, readings}]
    python3 tools/abhidhana_labels.py           # print the table as parsed, and check it

The table sits between the markers <!-- labels:begin --> and <!-- labels:end --> in
docs/labels.md. One row per printed label:

    | label | Pāḷi | English | Spanish | abbr. en | abbr. es | status | es | OCR readings |

- label      the label as printed, without brackets
- Pāḷi       its expansion (IAST); a trailing ? marks a guess
- English, Spanish   what it marks, in words, as the site's pop-up shows it
- abbr. en, abbr. es the short gloss shown beside the label; empty = none shown
- status     confirmed (Angel has agreed the label and its Pāḷi) or provisional
- es         confirmed or draft: whether the Spanish words are agreed
- OCR readings   every reading tools/abhidhana_articles.py maps to this label, space-separated,
             spaces inside a reading removed. Add a reading only after checking it on the image.

Written 25 Sep 2026; until then the readings were a dict in abhidhana_articles.py
(_LABEL_READINGS), and the table reproduces it exactly.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / 'docs/labels.md'
COLS = ['label', 'pali', 'en', 'es', 'abbr_en', 'abbr_es', 'status', 'es_status', 'readings']


def load(path=DOC):
    s = path.read_text(encoding='utf-8')
    m = re.search(r'<!-- labels:begin -->(.*?)<!-- labels:end -->', s, re.S)
    if not m: sys.exit(f'{path}: no <!-- labels:begin --> ... <!-- labels:end --> table')
    rows = [l for l in m.group(1).splitlines() if l.strip().startswith('|')][2:]   # skip header, rule
    out = []
    for l in rows:
        cells = [c.strip() for c in l.strip().strip('|').split('|')]
        if len(cells) != len(COLS): sys.exit(f'{path}: a label row has {len(cells)} cells, not {len(COLS)}: {l}')
        d = dict(zip(COLS, cells))
        d['label'] = d['label'].strip('()')
        d['readings'] = d['readings'].split()
        if d['status'] not in ('confirmed', 'provisional'): sys.exit(f'{path}: status must be confirmed/provisional: {l}')
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
