#!/usr/bin/env python3
"""Join the typed witness (witness/pced_k.jsonl) to the articles, and report agreement.

    python3 tools/abhidhana_witness_join.py 01 02 03 4a 4b 05 ...

Pairing. For each headword, the index rows carrying it (all books, in index id order) are
paired in order with the witness entries carrying it (in the witness's own order): the k-th
homonym with the k-th. A headword is looked up as the index spells it, then with the spelling
folds of tools/abhidhana_fold.py (the witness writes ာ after a stacked consonant where the
index writes ါ, like the print). When the two counts differ the pairing is still made in
order, but every pair of that headword is marked `count_mismatch`.

Comparison, per paired article:
    label     ours (normalised, docs/labels.md) against the witness's, spaces removed:
              agree / differ / one side missing.
    analysis  similarity of the [ ] contents, + signs and spaces removed (difflib ratio);
              below 0.4 is flagged `analysis_differs`, the threshold of brief §13.
    body      similarity of the witness definition to the head of our body, as long as the
              definition (the witness omits the quotations, so the tail is not compared).
              The witness's analysis field runs on past the ] into the grammarians' derivation;
              only its first clause (to ။) is compared as analysis, the rest goes with the body.

Output: witness/join-<book>.jsonl, one line per index row (ids, seq, flags and ratios; no
witness text), and docs/witness-join.md with the figures per volume. witness/ is gitignored
and stays so until the witness's licence is known (docs/witness.md §5); the report publishes
figures only, none of the witness's text.
"""
import json, re, sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from abhidhana_fold import fold

ROOT = Path(__file__).resolve().parent.parent
sp = lambda s: re.sub(r'\s', '', s or '')
ana = lambda s: re.sub(r'[\s+＋]', '', s or '')


def load_witness():
    exact, folded = defaultdict(list), defaultdict(list)
    for l in open(ROOT / 'witness/pced_k.jsonl'):
        r = json.loads(l)
        w = {k: r.get(k) for k in ('seq', 'label', 'analysis', 'definition')}
        exact[sp(r['headword'])].append(w); folded[fold(sp(r['headword']))].append(w)
    return exact, folded


def main(books):
    exact, folded = load_witness()
    rows = {}
    for b in books:
        for l in open(ROOT / f'ocr/{b}/articles.jsonl'):
            r = json.loads(l); rows[r['id']] = r
    # all index rows per headword, all books in the db, so homonyms split across books pair right
    import sqlite3
    db = sqlite3.connect(f'file:{ROOT}/db/tipitaka_abidan.db?mode=ro', uri=True)
    byhw = defaultdict(list)
    for wid, w in db.execute('select id, word from words order by id'): byhw[sp(w)].append(wid)
    pair = {}
    for h, ids in byhw.items():
        if not any(i in rows for i in ids): continue
        ws, how = exact.get(h), 'exact'
        if not ws: ws, how = folded.get(fold(h)), 'folded'
        if not ws: continue
        mism = len(ws) != len(ids)
        for k, wid in enumerate(ids):
            if k < len(ws): pair[wid] = (ws[k], how, mism)
    stats = {}
    for b in books:
        out = []; S = defaultdict(int)
        for l in open(ROOT / f'ocr/{b}/articles.jsonl'):
            r = json.loads(l); S['rows'] += 1
            j = {'id': r['id'], 'book': b, 'located': r['located']}
            if r['id'] not in pair:
                j['witness'] = None; out.append(j); continue
            w, how, mism = pair[r['id']]
            S['paired'] += 1; S['paired_' + how] += 1; S['mismatch'] += mism
            j.update(seq=w['seq'], match=how, count_mismatch=mism)
            ol, wl = r.get('label'), sp(w.get('label'))
            if ol and wl:
                S['lab_both'] += 1
                if sp(ol) == wl: S['lab_agree'] += 1; j['label'] = 'agree'
                else: j['label'] = 'differs'; j['label_ours'] = ol; S['lab_differ'] += 1
            elif wl: j['label'] = 'ours missing'; S['lab_ours_missing'] += 1
            elif ol: j['label'] = 'witness missing'
            # The witness's analysis field runs on past the ]: the grammarians' derivation that
            # the print sets after the bracket (ကစ+ဆ။ ကစ ဗန္ဓနေ။ ဓာန်၊ ဋီ။ ၂၄၆။ ...). Compare its
            # first clause, to the first ။, with ours (ours cut the same way); the rest goes with the body.
            wfull = w.get('analysis') or ''
            whead, _, wtail = wfull.partition('။')
            ours = r.get('analysis_read', '') if r.get('analysis_source') == 'pced' else r.get('analysis')   # our OCR, not the witness's own text
            oa, wa = ana((ours or '').partition('။')[0]), ana(whead)
            if oa and wa:
                x = round(SequenceMatcher(None, oa, wa).ratio(), 3); j['analysis_ratio'] = x
                S['ana_both'] += 1; S['ana_hi'] += x >= .8
                if x < .4: j['analysis_differs'] = True; S['ana_differ'] += 1; S['ana_differ_' + r['located']] += 1
                S['ana_both_' + r['located']] += 1
            ob, wd = sp(r.get('body')), sp(wtail + (w.get('definition') or ''))
            if ob and wd:
                x = round(SequenceMatcher(None, ob[:len(wd)], wd, autojunk=False).ratio(), 3)
                j['body_ratio'] = x; S['body_both'] += 1; S['body_hi'] += x >= .8; S['body_lo'] += x < .4
            out.append(j)
        (ROOT / f'witness/join-{b}.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in out))
        stats[b] = S
    return stats


def pc(a, b): return f'{100 * a / b:.1f}%' if b else '—'


if __name__ == '__main__':
    books = sys.argv[1:]
    st = main(books)
    L = ['| vol. | rows | paired | of which by fold | homonym count differs | labels: both / agree | '
         'analyses: both / ≥ 0.8 / < 0.4 | < 0.4 verbatim / fuzzy / folded | bodies: both / ≥ 0.8 / < 0.4 |',
         '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for b, S in st.items():
        d = lambda k: pc(S['ana_differ_' + k], S['ana_both_' + k])
        L.append(f"| {b} | {S['rows']:,} | {S['paired']:,} ({pc(S['paired'], S['rows'])}) | {S['paired_folded']:,} | "
                 f"{S['mismatch']:,} | {S['lab_both']:,} / **{pc(S['lab_agree'], S['lab_both'])}** | "
                 f"{S['ana_both']:,} / {pc(S['ana_hi'], S['ana_both'])} / {pc(S['ana_differ'], S['ana_both'])} | "
                 f"{d('verbatim')} / {d('fuzzy')} / {d('folded')} | "
                 f"{S['body_both']:,} / {pc(S['body_hi'], S['body_both'])} / {pc(S['body_lo'], S['body_both'])} |")
    print('\n'.join(L))
    (ROOT / 'witness/join-table.md').write_text('\n'.join(L) + '\n')
