#!/usr/bin/env python3
"""Build witness/pced_k.jsonl from PCED 1.94's dictionary K (siongui/data, dict_words_{1,2}.csv).

    pip install python-myanmar
    python3 tools/abhidhana_witness.py        # downloads the two CSVs into witness/src/ if absent

Dictionary K is "Tipiṭaka Pāḷi-Myanmar Dictionary", typed in Zawgyi; tools/zawgyi.py converts it.
See docs/witness.md for the checks and for what the witness omits. Its licence is not stated:
witness/ is gitignored, and nothing derived from it is published until that is settled.

Each row: seq (the CSV's row number), key (PCED's romanised headword, as given), headword,
label, analysis, definition (Unicode, converted from Zawgyi by zawgyi.py), in_index (the headword,
so converted, is an index headword), and zg (the source cell, untouched). Full-width punctuation, which PCED substitutes for ASCII, is mapped back; a ဝ standing
for the digit zero inside a number is written ၀.
"""
import csv, json, re, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zawgyi import zg2uni, RESIDUE

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'witness/src'
URL = 'https://raw.githubusercontent.com/siongui/data/master/dictionary/dict_words_{}.csv'

csv.field_size_limit(10**9)

FW = {c: chr(c - 0xFEE0) for c in range(0xFF01, 0xFF5F)}
LET = 'က-ဿၐ-႟'
ZERO = re.compile(f'(?<![{LET}])[၀-၉ဝ]*[၀-၉][၀-၉ဝ]*(?![{LET}])|(?<![{LET}])ဝ(?=[၀-၉])')

def digits(s):
    return ZERO.sub(lambda m: m.group(0).replace('ဝ', '၀'), s)

def clean(s):
    return digits(zg2uni(s).translate(FW)).strip()

HEAD = re.compile(r'^(?P<key>[^：]*)：\s*＂?(?P<rest>.*)$', re.S)
LAB = re.compile(r'^(?P<h>[^（(\[]+?)\s*[（(](?P<l>[^）)]{0,20})(?:[）)]|$)\s*(?P<after>.*)$', re.S)

def parse(cell):
    m = HEAD.match(cell)
    key, rest = (m.group('key'), m.group('rest')) if m else ('', cell)
    parts = [p.strip() for p in re.split(r'<br\s*/?>', rest)]
    first = parts.pop(0) if parts else ''
    d = {'key': key}
    lm = LAB.match(first)
    if lm:
        d['headword'] = clean(lm.group('h'))
        if lm.group('l').strip(): d['label'] = clean(lm.group('l'))
        if lm.group('after').strip(): parts.insert(0, lm.group('after').strip())
    else:
        d['headword'] = clean(first)
    if parts and parts[0].startswith('['):
        a = parts.pop(0)
        d['analysis'] = clean(a[1:a.rindex(']')] if ']' in a else a[1:])
        tail = a[a.rindex(']') + 1:].strip() if ']' in a else ''
        if tail: parts.insert(0, tail)
    d['definition'] = clean('\n'.join(p for p in parts if p))
    return d

def main(out=ROOT / 'witness/pced_k.jsonl'):
    SRC.mkdir(parents=True, exist_ok=True)
    idx = set()
    db = ROOT / 'db/tipitaka_abidan.db'
    if db.exists():
        import sqlite3
        idx = {w for (w,) in sqlite3.connect(db).execute('select word from words')}
    n = res = hit = 0
    with open(out, 'w') as f:
        for k in (1, 2):
            src = SRC / f'dict_words_{k}.csv'
            if not src.exists():
                print(f'downloading {src.name}'); urllib.request.urlretrieve(URL.format(k), src)
            for row in csv.reader(open(src, encoding='utf-8')):
                if row[2] != 'K': continue
                d = {'seq': int(row[0])}; d.update(parse(row[6]))
                if idx: d['in_index'] = d['headword'] in idx; hit += d['in_index']
                d['zg'] = row[6]
                if any(RESIDUE.search(d.get(x, '')) for x in ('headword', 'label', 'analysis', 'definition')): res += 1
                f.write(json.dumps(d, ensure_ascii=False) + '\n'); n += 1
    print(f'{out}: {n:,} entries; {hit:,} with a headword spelled as in the index; '
          f'{res:,} with characters outside U+1000-104F after conversion')

if __name__ == '__main__':
    main(*sys.argv[1:2])
