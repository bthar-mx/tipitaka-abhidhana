#!/usr/bin/env python3
"""The compound analysis [ ] from the typed PCED witness, where it has one (the editor, 26 Sep 2026).

Measured before the decision, books 01-19 (4a, 4b included): of 119,627 articles where both our
OCR and PCED have an analysis, 60,859 (50.9%) differed after spaces and + signs were evened out;
in 50,431 of those PCED's elements spelled the headword more closely, in 3,402 ours did, 7,026
tied. PCED also has an analysis for 35,445 articles where the OCR gave none. Spot checks by the editor:
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
The editor decided on 26 Sep 2026 to publish its analyses (and to draft the Meaning boxes from its
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


# --- The body's first words (brief §50) -----------------------------------------------------
# abhidhana_articles.py keeps the rest of the line an analysis ends on, when its tokens have the
# shape of words, and marks the row body_head_restored. By shape alone ~5% of such additions in
# the OCR books were debris (ချူ, ချာ, ဦရူ; measured on books 01, 05, 10, 15). So in the books PCED
# covers (the editor, 27 Sep 2026) the words are kept only where PCED's definition begins with
# them: verbatim (spaces aside) within its first characters, or with a similarity of 0.6 or more
# (OCR letter errors: ဂ- for ၈-). Elsewhere, or with no PCED line, they are taken out again. In
# other books the shape rule stands (body_head_how "shape"). Without witness/ the PCED books keep
# none of them, so a run without the witness cannot add debris.
import difflib
PCED_BOOKS = {'01', '02', '03', '4a', '4b', '05', '06', '07', '08', '09', '10', '11', '12', '13',
              '14', '15', '16', '17', '18', '19'}
_D = None


def definitions():
    global _D
    if _D is None:
        f = ROOT / 'witness/pced_k.jsonl'
        _D = {}
        if f.exists():
            for line in f.open(encoding='utf-8'):
                w = json.loads(line)
                if w.get('definition'): _D[w['seq']] = nfc(w['definition'])
    return _D


def head_agrees(added, definition):
    ns = lambda x: re.sub(r'\s', '', x or '')
    a, p = ns(added), ns(definition)
    if not a or not p: return None
    if a in p[:len(a) + 8]: return 'verbatim'
    if max(difflib.SequenceMatcher(None, a, p[k:k + len(a)]).ratio() for k in range(4)) >= 0.6:
        return 'similar'
    return None


def gate_head(book, rows):
    from abhidhana_articles import cites
    cand = [r for r in rows if r.get('body_head_restored')]
    if book not in PCED_BOOKS:
        for r in cand: r['body_head_how'] = 'shape'
        return [f'first words on the headword line: {len(cand):,} bodies gained them (by shape; no PCED for book {book})']
    jf = ROOT / f'witness/join-{book}.jsonl'
    D = definitions() if jf.exists() else {}
    seq = {}
    if jf.exists():
        for line in jf.open(encoding='utf-8'):
            j = json.loads(line)
            if j.get('seq') is not None: seq[j['id']] = j['seq']
    kept = {'verbatim': 0, 'similar': 0}; out = 0
    for r in cand:
        how = head_agrees(r['body_head_restored'], D.get(seq.get(r['id'])))
        if how:
            r['body_head_how'] = 'pced'; kept[how] += 1; continue
        # take the words out again: they are the body's first line
        body = r['body']; h = r.pop('body_head_restored')
        lines = body.split('\n')
        assert re.sub(r'\s', '', lines[0]) == re.sub(r'\s', '', h), (r['id'], lines[0], h)
        r['body'] = '\n'.join(lines[1:]).strip()
        r['noise_lines'] = r.get('noise_lines', 0) + 1
        r['citations'] = cites(r['body'])
        out += 1
    note = '' if D else ' (no witness here: none kept)'
    return [f'first words on the headword line: {len(cand):,} candidates; PCED agrees with {kept["verbatim"]:,} verbatim '
            f'and {kept["similar"]:,} by similarity, kept; {out:,} taken out{note}']
