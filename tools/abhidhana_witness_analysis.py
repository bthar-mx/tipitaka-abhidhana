#!/usr/bin/env python3
"""The compound analysis [ ] from the typed PCED witness, where it has one (Angel, 26 Sep 2026).

Measured before the decision, books 01-19 (4a, 4b included): of 119,627 articles where both our
OCR and PCED have an analysis, 60,859 (50.9%) differed after spaces and + signs were evened out;
in 50,431 of those PCED's elements spelled the headword more closely, in 3,402 ours did, 7,026
tied. PCED also has an analysis for 35,445 articles where the OCR gave none. Spot checks by Angel:
akusala [န + ကုသလ] (OCR ကုသလျ), akuppa [န + ကုပ္ပ] (OCR ကပ္ပါ) -- PCED right both times.

So abhidhana_articles.py calls apply() after reading the articles and before the hand corrections
(docs/corrections.tsv, which still win): wherever witness/join-<book>.jsonl pairs the row with a
PCED entry that has an analysis, that analysis replaces ours, whole (PCED's field, like the
print's bracket, runs on past ။ into the grammarians' derivation), with + spaced " + ". The row
gains
    analysis_source  "pced"
    analysis_read    what our OCR read (absent if it read nothing)
and keeps analysis_ocr (the reading before the + signs were repaired) if it had one.

The witness is PCED, Pali Canon E-Dictionary 1.94's "Tipiṭaka Pāḷi-Myanmar Dictionary" (repo
siongui/data), converted from Zawgyi by tools/abhidhana_witness.py. Its licence is not stated;
Angel decided on 26 Sep 2026 to publish its analyses (and to draft the Meaning boxes from its
definitions), credited on the site and in the README. Books it does not cover (4/3's own text,
14/2, 14/3, 20-25) keep the OCR. witness/ is gitignored, so this runs only where it exists:
without it the OCR stays, and the step says so.
"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
nfc = lambda s: unicodedata.normalize('NFC', s or '')
_W = None


def witness():
    global _W
    if _W is None:
        f = ROOT / 'witness/pced_k.jsonl'
        _W = {}
        if f.exists():
            for line in f.open(encoding='utf-8'):
                w = json.loads(line)
                if w.get('analysis'): _W[w['seq']] = nfc(w['analysis'])
    return _W


def spaced(a):
    a = re.sub(r'\s*\+\s*', ' + ', a.strip())
    return re.sub(r'[ \t]+', ' ', a)


def apply(book, rows):
    jf = ROOT / f'witness/join-{book}.jsonl'
    W = witness()
    if not jf.exists() or not W:
        return [f'witness analyses: none for book {book} (no {jf.relative_to(ROOT)} or witness/pced_k.jsonl); OCR kept']
    seq = {}
    for line in jf.open(encoding='utf-8'):
        j = json.loads(line)
        if j.get('seq') is not None: seq[j['id']] = j['seq']
    n = changed = added = 0
    for r in rows:
        s = seq.get(r['id'])
        if s is None or s not in W: continue
        new = spaced(W[s])
        if not new: continue
        old = r.get('analysis')
        if old: r['analysis_read'] = old
        if not old: added += 1
        elif old.replace(' ', '') != new.replace(' ', ''): changed += 1
        r['analysis'] = new; r['analysis_source'] = 'pced'; n += 1
    return [f'witness analyses (PCED): {n:,} rows take it; {changed:,} differed from the OCR, {added:,} where the OCR had none']
