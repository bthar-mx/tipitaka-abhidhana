#!/usr/bin/env python3
"""Pn Daza's dict.db, book 1, as a typed witness with page references; joined to the articles
by book, page and headword.

    python3 tools/abhidhana_witness_pndaza.py build             # witness/pndaza_k.jsonl
    python3 tools/abhidhana_witness_pndaza.py join 01 02 ...    # witness/pjoin-NN.jsonl + table
    python3 tools/abhidhana_witness_pndaza.py unmatched         # the headwords not in PCED K

`witness/pndaza-dict.db` is the database of Pn Daza's Pali-Myanmar Dictionary app
(docs/witness-pndaza.md). Its book 1 is the typing PCED's dictionary K was made from, with the
page reference `တိပိ၊vol၊page` kept on 98.8% of entries. Each entry's `content` (Zawgyi) is
headword (label) / [analysis] / definition / reference, separated by blank lines; it is converted
with tools/zawgyi.py, the converter used for PCED, so the two witnesses are spelled alike.

The join. An index row (id, book, index page, headword) is paired with the typed entries that
carry the same book and page and the same headword, homographs on one page in order. The
headword is compared as our conversion of `zword`, then as Pn Daza's `uword`, then folded
(tools/abhidhana_fold.py). A reference spanning pages (`၂+၃+၄`) is filed under its first page.
Labels, analyses and bodies are then compared with the article as abhidhana_witness_join.py does.

witness/ is gitignored: dict.db states no licence (docs/witness-pndaza.md §6.5). Nothing here is
published but figures.
"""
import json, re, sqlite3, sys, unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zawgyi import zg2uni
from abhidhana_fold import fold

ROOT = Path(__file__).resolve().parent.parent
MY = str.maketrans('၀၁၂၃၄၅၆၇၈၉', '0123456789')
VOL = {'၄က': '4a', '၄ခ': '4b'}
REF = re.compile(r'တိပိ၊\s*([^၊\s]+)\s*၊\s*([၀-၉+\-\s]+?)\s*$')
nfc = lambda s: unicodedata.normalize('NFC', s)
sp = lambda s: re.sub(r'\s', '', s or '')
ana = lambda s: re.sub(r'[\s+＋]', '', s or '')
FW = {c: chr(c - 0xFEE0) for c in range(0xFF01, 0xFF5F)}


def book_of(vol):
    if vol in VOL: return VOL[vol]
    n = vol.translate(MY)
    return n.zfill(2) if n.isdigit() else None


def parse(content):
    """(label, analysis, definition, book, page) from a Zawgyi content cell, converted"""
    t = zg2uni(content.translate(FW)).strip()
    book = page = None
    m = REF.search(t)
    if m:
        book = book_of(m.group(1).strip())
        pg = re.split(r'[+\-]', m.group(2).translate(MY).replace(' ', ''))[0]
        page = int(pg) if pg.isdigit() else None
        t = t[:m.start()].rstrip()
    parts = [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]
    head = parts.pop(0) if parts else ''
    lab = re.search(r'\(([^()]{1,20})\)\s*$', head)
    label = sp(lab.group(1)) if lab else None
    analysis = None
    if parts and parts[0].startswith('['):
        a = parts.pop(0); analysis = a[1:a.rindex(']')] if ']' in a else a[1:]
    return label, analysis, '\n'.join(parts), book, page


def build():
    c = sqlite3.connect(f'file:{ROOT}/witness/pndaza-dict.db?mode=ro', uri=True)
    n = 0
    with open(ROOT / 'witness/pndaza_k.jsonl', 'w') as f:
        for _id, zw, uw, content in c.execute("select _id, zword, uword, content from define where book='1' order by _id"):
            label, analysis, definition, book, page = parse(content)
            d = dict(id=_id, headword=nfc(zg2uni(zw)), uword=nfc(uw or ''), label=label, analysis=analysis,
                     definition=definition, book=book, page=page)
            f.write(json.dumps(d, ensure_ascii=False) + '\n'); n += 1
    print(f'witness/pndaza_k.jsonl: {n:,} entries')


def load():
    return [json.loads(l) for l in open(ROOT / 'witness/pndaza_k.jsonl')]


def join(books):
    W = load()
    at = defaultdict(list)                       # (book, index page) -> typed entries, in order
    for w in W:
        if w['book'] and w['page'] is not None: at[(w['book'], w['page'])].append(w)
    db = sqlite3.connect(f'file:{ROOT}/db/tipitaka_abidan.db?mode=ro', uri=True)
    table = []
    for b in books:
        rows = {json.loads(l)['id']: json.loads(l) for l in open(ROOT / f'ocr/{b}/articles.jsonl')}
        byp = defaultdict(list)
        for wid, word, pg in db.execute('select id, word, page_number from words where book_id=? order by id', (b,)):
            byp[pg].append((wid, nfc(word)))
        S = defaultdict(int); out = []
        for pg, ids in byp.items():
            cand = list(at.get((b, pg), []))
            for wid, word in ids:
                h = sp(word); how = None; hit = None
                for key, name in ((lambda w: sp(w['headword']), 'ours'), (lambda w: sp(w['uword']), 'uword'),
                                  (lambda w: fold(sp(w['headword'])), 'folded')):
                    hk = fold(h) if name == 'folded' else h
                    hit = next((w for w in cand if key(w) == hk), None)
                    if hit: how = name; break
                j = {'id': wid, 'book': b}
                S['rows'] += 1
                if hit is None:
                    j['typed'] = None; out.append(j); continue
                cand.remove(hit); S['paired'] += 1; S['by_' + how] += 1
                j.update(typed=hit['id'], match=how)
                r = rows.get(wid)
                if r is None: out.append(j); continue
                ol, wl = r.get('label'), hit.get('label')
                if ol and wl:
                    S['lab_both'] += 1; ok = sp(ol) == wl; S['lab_agree'] += ok
                    j['label'] = 'agree' if ok else 'differs'
                oa = ana((r.get('analysis') or '').partition('။')[0])
                wa = ana((hit.get('analysis') or '').partition('။')[0])
                if oa and wa:
                    x = round(SequenceMatcher(None, oa, wa).ratio(), 3); j['analysis_ratio'] = x
                    S['ana_both'] += 1; S['ana_hi'] += x >= .8; S['ana_lo'] += x < .4
                ob, wd = sp(r.get('body')), sp(hit.get('definition'))
                if ob and wd:
                    x = round(SequenceMatcher(None, ob[:len(wd)], wd, autojunk=False).ratio(), 3)
                    j['body_ratio'] = x; S['body_both'] += 1; S['body_hi'] += x >= .8
                if r['located'] == 'unlocated': S['unlocated_paired'] += 1
                out.append(j)
        (ROOT / f'witness/pjoin-{b}.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in out))
        pc = lambda a, c: f'{100 * a / c:.1f}%' if c else '—'
        table.append(f"| {b} | {S['rows']:,} | {S['paired']:,} ({pc(S['paired'], S['rows'])}) | "
                     f"{S['by_uword']:,} / {S['by_folded']:,} | {S['lab_both']:,} / **{pc(S['lab_agree'], S['lab_both'])}** | "
                     f"{S['ana_both']:,} / {pc(S['ana_hi'], S['ana_both'])} / {pc(S['ana_lo'], S['ana_both'])} | "
                     f"{S['body_both']:,} / {pc(S['body_hi'], S['body_both'])} | {S['unlocated_paired']:,} |")
    head = ['| vol. | index rows | paired by book, page, headword | of which by uword / folded | labels: both / agree | '
            'analyses: both / ≥ 0.8 / < 0.4 | bodies: both / ≥ 0.8 | unlocated articles with a typed text |',
            '|---|---:|---:|---:|---:|---:|---:|---:|']
    (ROOT / 'witness/pjoin-table.md').write_text('\n'.join(head + table) + '\n')
    print('\n'.join(head + table))


def unmatched():
    """the book-1 headwords (Pn Daza's uword) not among PCED K's converted headwords"""
    W = load()
    P = set(); Pf = set()
    for l in open(ROOT / 'witness/pced_k.jsonl'):
        h = sp(json.loads(l)['headword']); P.add(h); Pf.add(fold(h))
    db = sqlite3.connect(f'file:{ROOT}/db/tipitaka_abidan.db?mode=ro', uri=True)
    I = {sp(nfc(w)) for (w,) in db.execute('select word from words')}
    un = sorted({sp(w['uword']) for w in W} - P)
    cls = defaultdict(list); ours = {sp(w['uword']): sp(w['headword']) for w in W}
    for u in un:
        o = ours[u]
        if o in P: k = 'conversion: our converter gives the PCED spelling'
        elif fold(u) in Pf or fold(o) in Pf: k = 'fold: differs from PCED only by a folded spelling'
        elif u in I or o in I: k = 'an index headword PCED lacks'
        else: k = 'neither in PCED nor in the index'
        cls[k].append((u, o))
    print(f'{len(un):,} distinct uwords not in PCED K')
    for k, v in sorted(cls.items(), key=lambda x: -len(x[1])):
        print(f'  {len(v):5,}  {k}   e.g. ' + ', '.join(f'{u}→{o}' if u != o else u for u, o in v[:4]))
    return cls


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'build': build()
    elif cmd == 'join': join(sys.argv[2:])
    elif cmd == 'unmatched': unmatched()
