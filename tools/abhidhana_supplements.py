#!/usr/bin/env python3
"""The supplements bound in vol. 4/3 (book 4c, PDF pp. 713-735; brief §16, §78, §79): which volume
each of the 223 index rows 177206-177428 belongs to, and where it goes in that volume's alphabet.

    python3 tools/abhidhana_supplements.py          # report: anchors and the rows the key is unsure of
    python3 tools/abhidhana_supplements.py --write  # (re)write docs/supplements.tsv, keeping every
                                                    # row already marked `checked` as it is

docs/supplements.tsv: id, book (4c), belongs_to (15 / 4b / 16), after_id (the row of that volume the
supplement row follows in Browse), how (key: placed by the Pali-alphabet key; checked: looked at on
the page images), note. Nothing in the data changes: tools/abhidhana_browse.py reads the table.

The key: the romanised headword as a list of Pali letters in the dictionary's order (niggahita
first, then the letters of tools/abhidhana_browse.py LETTERS). The anchor is the insertion point in
the volume's index order that leaves the fewest rows out of key order on either side (ties: after
equal keys, i.e. after the volume's own homonyms, and the latest such point). A row is `unsure` when
its IAST is shared with a row of that volume, when the best point is not unique, or when the rows on
either side of it are themselves out of key order.
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from abhidhana_browse import letters, LETTERS

TSV = ROOT / 'docs/supplements.tsv'
COLS = ['id', 'book', 'belongs_to', 'after_id', 'how', 'note']
# the headwords that open each supplement in print (brief §64): bhijja, udavā, maṁsakāraṇa
RANGES = [(177206, 177258, '15'), (177259, 177372, '4b'), (177373, 177428, '16')]
RANK = {ro: i for i, (ro, _) in enumerate(LETTERS)}; RANK['ṁ'] = -2   # the end of a word is -1
# Looked at on the page images of 4c (PDF pp. 721-735) and vol. 15 p. 738, 29 Sep 2026 (brief §79).
# The headword as printed, where the index spells it otherwise: the anchor is found on this spelling.
PRINTED = {177260: 'udānita', 177267: 'upakkilesasamuccheda', 177269: 'upaghātabhūmi',
           177277: 'upajjhāyinī', 177282: 'upanāhaka', 177287: 'upapakkilesasamuccheda',
           177300: 'upavananta', 177305: 'upavīyati', 177307: 'upavesana', 177314: 'upasampādya',
           177326: 'upāna', 177327: 'upāntabhū', 177332: 'upāvatta', 177336: 'upekkhikā',
           177337: 'upeyamāna', 177338: 'uppajjantī', 177343: 'ubbaṭṭa', 177344: 'ubbaṭṭabījaka',
           177368: 'ussiñcanti', 177373: 'maṁkāraṇa', 177389: 'māṇivara', 177424: 'modaka'}
# index rows that belong to another row's printed article: placed with it
SAME_AS = {177266: 177267, 177350: 177349, 177402: 177401}
NOTES = {
    177266: 'no article of its own on p. 721: the page prints ဥပက္ကိလေသသမုစ္ဆေဒ (177267); placed with it',
    177267: 'printed ဥပက္ကိလေသသမုစ္ဆေဒ (the index: ဥပက္ကိလေသမုစ္ဆေဒ)',
    177269: 'printed ဥပဃာတဘူမိ (the index: ဥပါဃာတဘူမိ)',
    177282: 'printed ဥပနာဟက (the index: ဥပါနာဟက)',
    177287: 'printed ဥပပက္ကိလေသသမုစ္ဆေဒ, a "see" entry (the index: ဥပပက္ကလေသမုစ္ဆေဒ)',
    177300: 'printed ဥပဝနန္တ (the index: ဥပနန္တ)',
    177307: 'printed ဥပဝေသန (the index: ဥပသေဝန)',
    177326: 'printed ဥပါန (the index: ဥပါနာဟက, as 177282)',
    177327: 'printed ဥပါန္တဘူ (the index: ဥပါဒန္တဘူ)',
    177349: 'one printed article with 177350: ဥဗ္ဘ၊ ဥဗ္ဘံ',
    177350: 'one printed article with 177349 (ဥဗ္ဘ၊ ဥဗ္ဘံ); placed with it',
    177373: 'printed မံကာရဏ (the index: မံသကာရဏ)',
    177380: 'printed မဇ္ဈ²', 177384: 'printed မဏိ²', 177385: 'printed မတ²',
    177401: 'printed မီ(မိ)ယမာန¹, one article with 177402',
    177402: 'one printed article with 177401 (မီ(မိ)ယမာန¹); placed with it',
    177403: 'printed မီယမာန²',
    177412: 'the index row covers two printed articles, မေဃဇ္ဇဝ and မေဃလ',
    177422: 'printed မေသ²',
    177424: 'printed မောဒက (the index: မေဒက)',
}
NOTES[177381] = 'p. 731 prints one မဋ္ဋက article; the index has two rows (177381, 177382); placed with 177382'
SAME_AS[177381] = 177382
# non-verbatim rows looked at and printed as the index spells them (OCR misreadings only)
AS_INDEXED = {177285, 177298, 177342, 177356, 177369, 177377, 177378, 177382, 177386, 177398, 177404,
              177405, 177407, 177408, 177409, 177411, 177415}


def belongs(i):
    for a, b, v in RANGES:
        if a <= i <= b: return v
    return None


def key(r):
    return tuple(RANK.get(x, 99) for x in letters(r)) + (-1,)


def rows(book):
    P = {}
    for line in (ROOT / f'ocr/{book}/pali.jsonl').open(encoding='utf-8'):
        r = json.loads(line); P[r['id']] = r
    out = []
    for line in (ROOT / f'ocr/{book}/articles.jsonl').open(encoding='utf-8'):
        r = json.loads(line)
        out.append({'i': r['id'], 'p': r['pdf_page'], 'h': r['headword'],
                    'r': r.get('iast') or P.get(r['id'], {}).get('headword_iast') or ''})
    return out


def anchor(vol, s, shared=()):
    """(after_id, unsure reasons) for supplement row s in the volume's rows"""
    r = PRINTED.get(s['i'], s['r'])
    ks = key(r); K = [key(d['r']) for d in vol]; n = len(K)
    # cost(j) = rows before j with key > ks + rows from j on with key <= ks
    after = sum(1 for k in K if k <= ks); cost = after; best = [cost]; bj = [0]
    costs = [cost]
    for j in range(1, n + 1):
        cost += (1 if K[j - 1] > ks else 0) - (1 if K[j - 1] <= ks else 0)
        costs.append(cost)
    m = min(costs); js = [j for j, c in enumerate(costs) if c == m]
    j = js[-1]
    why = []
    same = [x for x, d in enumerate(vol) if d['r'] == r]
    if same: why.append('shared IAST'); j = same[-1] + 1   # after the volume's last row of that headword
    elif r in shared: why.append('IAST shared elsewhere')
    if js[-1] - js[0] > 0 and any(K[x] != ks for x in range(js[0], js[-1])): why.append(f'{len(js)} equal points')
    lo, hi = max(0, j - 2), min(n, j + 2)
    if any(K[x] > K[x + 1] for x in range(lo, hi - 1)): why.append('neighbours out of order')
    if j == 0: why.append('before the first row')
    return (vol[j - 1]['i'] if j else 0), why, j


def main():
    c4 = rows('4c'); S = [d for d in c4 if belongs(d['i'])]
    V = {v: rows(v) for v in ('15', '4b', '16')}
    # IASTs a supplement row shares with any other row of the dictionary (the site's homonym sets)
    import unicodedata
    nf = lambda x: unicodedata.normalize('NFC', x or '').strip()
    cnt = {}
    for b in json.loads((ROOT / 'site/volumes.json').read_text(encoding='utf-8')):
        for d in rows(b['id']): cnt[nf(d['r'])] = cnt.get(nf(d['r']), 0) + 1
    shared = {s['r'] for s in S if cnt.get(nf(s['r']), 0) > 1}
    print(f'{len(shared)} supplement IASTs shared with another row', file=sys.stderr)
    out = []; unsure = 0; pos = {}
    for s in S:
        v = belongs(s['i']); aid, why, j = anchor(V[v], s, shared); pos[s['i']] = aid
        if s['i'] in SAME_AS: aid = pos[SAME_AS[s['i']]] if SAME_AS[s['i']] in pos else anchor(V[v], {**s, 'i': SAME_AS[s['i']]}, shared)[0]
        if why: unsure += 1
        vol = V[v]
        ctx = f"{vol[j-1]['r'] if j else '^'} < [{PRINTED.get(s['i'], s['r'])}] < {vol[j]['r'] if j < len(vol) else '$'}"
        print(f"{s['i']}\t{v}\t{s['p']}\t{s['r']}\tafter {aid}\t{ctx}\t{'UNSURE: ' + '; '.join(why) if why else ''}")
        seen = bool(why) or s['i'] in PRINTED or s['i'] in SAME_AS or s['i'] in NOTES or s['i'] in AS_INDEXED
        note = NOTES.get(s['i']) or ''
        if not note and s['i'] in PRINTED: note = f"printed {PRINTED[s['i']]}"
        if seen and v == '15' and not note:
            note = 'vol. 15 has no ဘိဇ္ဇ headword: the whole supplement follows ဘိင်္ကစ္ဆာပ (vol. 15 p. 738, seen)'
        if seen and not note: note = 'seen: ' + '; '.join(why) if why else 'seen: printed as indexed'
        out.append({'id': s['i'], 'book': '4c', 'belongs_to': v, 'after_id': aid,
                    'how': 'checked' if seen else 'key', 'note': note})
    print(f'{len(S)} rows; unsure {unsure}; checked {sum(1 for r in out if r["how"] == "checked")}', file=sys.stderr)
    if '--write' in sys.argv:
        with TSV.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, COLS, delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
        print(f'wrote {TSV}', file=sys.stderr)


if __name__ == '__main__':
    main()
