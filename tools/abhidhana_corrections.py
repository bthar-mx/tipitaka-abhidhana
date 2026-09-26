#!/usr/bin/env python3
"""Corrections made by hand against the printed page: docs/corrections.tsv.

One row per corrected field of one article:

    id      the index row (words.id)
    book    its book (01 ... 25, 4a, 14c ...), a check against a mistyped id
    field   headword | label | analysis | body
            headword: the index misspells it (docs/index-errata.md). The row then shows and romanises
            the printed spelling and files it under its real letter; the index's spelling stays as
            headword_index (the index itself is never edited)
    value   the field as printed, in Burmese script, as the pipeline stores it
    ocr     what the OCR gave when the correction was made (so a later re-run that reads the
            field differently is reported, not silently overwritten)
    by      who read the print
    date    YYYY-MM-DD
    note    where, and anything else

abhidhana_articles.py applies them as the last step, so every re-run keeps them. A corrected
row keeps status "ocr" (the rest of the article is still unchecked) and gains
    corrected = {field: {"ocr": <the OCR reading>, "by": ..., "date": ...}}
which the site shows beside that field. abhidhana_romanise.py then romanises the corrected value.

    python3 tools/abhidhana_corrections.py          check the file and list it
"""
import csv, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / 'docs/corrections.tsv'
FIELDS = {'headword', 'label', 'analysis', 'body'}
nfc = lambda s: unicodedata.normalize('NFC', s or '')


def load():
    """[{id, book, field, value, ocr, by, date, note}], checked"""
    if not FILE.exists(): return []
    out, seen = [], set()
    with FILE.open(encoding='utf-8', newline='') as f:
        for n, r in enumerate(csv.DictReader(f, delimiter='\t'), start=2):
            r = {k: nfc(v).strip() for k, v in r.items() if k}
            if not r.get('id'): continue
            if r['field'] not in FIELDS: raise SystemExit(f'{FILE.name} line {n}: field {r["field"]!r} not one of {sorted(FIELDS)}')
            if not r.get('value'): raise SystemExit(f'{FILE.name} line {n}: empty value')
            key = (int(r['id']), r['field'])
            if key in seen: raise SystemExit(f'{FILE.name} line {n}: id {r["id"]} {r["field"]} corrected twice')
            seen.add(key); r['id'] = int(r['id']); out.append(r)
    return out


def apply(book, rows):
    """apply the corrections for this book to the article rows, in place; returns messages"""
    todo = [c for c in load() if c['book'] == book]
    byid = {r['id']: r for r in rows}
    msgs = []
    for c in todo:
        r = byid.get(c['id'])
        if r is None: msgs.append(f'correction for id {c["id"]}: no such row in book {book}'); continue
        old = r.get(c['field']) or ''
        if c['ocr'] and nfc(old) != c['ocr'] and nfc(old) != c['value']:
            msgs.append(f'id {c["id"]} {c["field"]}: the OCR now reads {old!r}, not {c["ocr"]!r} as when corrected; applied anyway')
        if c['field'] == 'headword': r.setdefault('headword_index', old)
        r[c['field']] = c['value']
        r.setdefault('corrected', {})[c['field']] = {'ocr': old, 'by': c['by'], 'date': c['date']}
    if todo: msgs.append(f'{len(todo)} hand correction(s) applied from docs/corrections.tsv')
    return msgs


if __name__ == '__main__':
    for c in load(): print(c['book'], c['id'], c['field'], c['ocr'], '->', c['value'], '·', c['by'], c['date'])
