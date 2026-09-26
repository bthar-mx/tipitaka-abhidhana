#!/usr/bin/env python3
"""Data for the Browse page (the site's home, /w/<headword>, /browse/<letter>/<syllable>).
Standard library only; called by tools/abhidhana_site.py with every book's records.

What it writes under site/dist/data/:
    nav.json            the 40 letters in the dictionary's order: roman, Burmese, entry count,
                        the books they occur in
    nav/<L>.json        one per letter (L = its number, 0-39): the thumb index, two levels --
                        group (the first two letters: ak-, ag-, ka- ...) and syllable (up to the
                        second vowel: aka-, akā-, akko- ...) -- each with its entry count and the
                        chunk files that hold its entries
    c/<n>.json          the articles, one file per group (split into parts of at most CHUNK
                        entries), in the dictionary's order; the records of tools/abhidhana_site.py
                        plus g (global order), k (book), sl (address), hn (homonym number),
                        see ([[iast, address]] for "see X"), cx (abbreviation index per citation)
    s/<L>.json          the search shard of a letter: [address, iast, Burmese, book, page, chunk]
    abbr.json           the citation abbreviations of docs/introduction/citation-abbreviations.tsv

The order is the book's: the books in site/volumes.json order, each in index order. Groups and
syllables are listed in the order they first occur, so the thumb index follows the printed
dictionary (niggahīta first, simple consonants before conjuncts) without a sorting rule.
The groups and syllables are computed on the romanised headword; a Burmese reader sees the
headwords in Burmese when that script is chosen, and the index keys in roman.
"""
import csv, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNK = 400
LETTERS = [('a', 'အ'), ('ā', 'အာ'), ('i', 'ဣ'), ('ī', 'ဤ'), ('u', 'ဥ'), ('ū', 'ဦ'), ('e', 'ဧ'), ('o', 'ဩ'),
           ('k', 'က'), ('kh', 'ခ'), ('g', 'ဂ'), ('gh', 'ဃ'), ('ṅ', 'င'), ('c', 'စ'), ('ch', 'ဆ'), ('j', 'ဇ'),
           ('jh', 'ဈ'), ('ñ', 'ဉ'), ('ṭ', 'ဋ'), ('ṭh', 'ဌ'), ('ḍ', 'ဍ'), ('ḍh', 'ဎ'), ('ṇ', 'ဏ'), ('t', 'တ'),
           ('th', 'ထ'), ('d', 'ဒ'), ('dh', 'ဓ'), ('n', 'န'), ('p', 'ပ'), ('ph', 'ဖ'), ('b', 'ဗ'), ('bh', 'ဘ'),
           ('m', 'မ'), ('y', 'ယ'), ('r', 'ရ'), ('l', 'လ'), ('v', 'ဝ'), ('s', 'သ'), ('h', 'ဟ'), ('ḷ', 'ဠ')]
LIDX = {ro: i for i, (ro, _) in enumerate(LETTERS)}
VOWELS = {'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'o'}
# every Pāḷi letter in IAST, longest first, plus ṁ (niggahīta), which starts no word
TOKENS = sorted([ro for ro, _ in LETTERS] + ['ṁ'], key=len, reverse=True)
TOKRE = re.compile('|'.join(re.escape(t) for t in TOKENS))


def letters(iast):
    """IAST -> list of Pāḷi letters (unknown characters are dropped)"""
    s = unicodedata.normalize('NFC', (iast or '').lower()).replace('ṃ', 'ṁ').replace('l̤', 'ḷ')
    return TOKRE.findall(s)


def keys(iast):
    """(letter index, group key, syllable key) of a headword, or None"""
    L = letters(iast)
    if not L or L[0] not in LIDX: return None
    group = ''.join(L[:2])
    nv, k = 0, 0
    for k, x in enumerate(L):
        if x in VOWELS:
            nv += 1
            if nv == 2: break
    syll = ''.join(L[:k + 1]) if nv >= 2 else ''.join(L)
    return LIDX[L[0]], group, syll


def mynorm(t):
    return (t or '').replace('့်', '့်')


# --- citations: which abbreviation of the table a citation begins with ----------------------------
def abbreviations():
    f = ROOT / 'docs/introduction/citation-abbreviations.tsv'
    if not f.exists(): return [], {}
    rows = list(csv.DictReader(f.open(encoding='utf-8'), delimiter='\t'))
    out, key = [], {}
    for r in rows:
        g = lambda k: (r.get(k) or '').strip()
        out.append({'my': g('abbr_my'), 'ro': g('abbr_iast'), 'work': g('work'), 'list': g('list'),
                    'list_es': g('list_es'), 'list_no': g('list_no'), 'note_en': g('note_en'),
                    'note_es': g('note_es'), 'p': g('pdf_page'), 'st': g('status') or 'drafted'})
        key.setdefault(re.sub(r'[\s။]', '', mynorm(g('abbr_my'))), len(out) - 1)
    return out, key


FOLD = [(r'၊(?:ဌ|္ဌ)$', '၊ဋ္ဌ'), (r'(?<=[^၊])ဋ္ဌ$', '၊ဋ္ဌ'), (r'၊(?:ဋံ|ဋိ)$', '၊ဋီ'), (r'(?<=[^၊])ဋီ$', '၊ဋီ')]


def cite_key(c, K):
    """the index in the table of a citation's abbreviation, or -1: exact, then with the OCR forms
    of the commentary marks folded (ဌ ္ဌ -> ဋ္ဌ, ဋံ ဋိ -> ဋီ) and a trailing သစ် ("new") dropped"""
    m = re.match(r'^(.*?)[၀-၉0-9]', mynorm(c))
    k = re.sub(r'[\s။]', '', m.group(1) if m else c).rstrip('၊,.')
    if k in K: return K[k]
    k2 = re.sub(r'၊?သစ်$', '', k)
    for a, b in FOLD: k2 = re.sub(a, b, k2)
    if k2 in K: return K[k2]
    # a stray word before the abbreviation: the longest table key it ends with
    for n in range(k2.count('၊'), 0, -1):
        tail = '၊'.join(k2.split('၊')[-n:])
        if tail in K: return K[tail]
    return -1


# --- the build -------------------------------------------------------------------------------------
def build(OUT, vols, book_records, dump):
    """vols: site/volumes.json rows; book_records: {book: [records]} in index order"""
    ABBR, AK = abbreviations()
    E = []   # every record, in the dictionary's order
    for v in vols:
        for d in book_records.get(v['id'], []):
            d['k'] = v['id']; E.append(d)
    # addresses: the IAST headword; homonyms (same IAST) get -2, -3 in the index's order
    seen = {}
    for g, d in enumerate(E):
        d['g'] = g
        base = unicodedata.normalize('NFC', d.get('r') or '').strip() or f"id-{d['i']}"
        base = re.sub(r'[\s/?#%]+', '-', base)
        n = seen.get(base, 0) + 1; seen[base] = n
        d['sl'] = base if n == 1 else f'{base}-{n}'
    first = {}
    for d in E:
        first.setdefault(unicodedata.normalize('NFC', d.get('r') or ''), d['sl'])
    # the Meaning box: [[iast]] (a "see X" in a translation) linked when X is a headword
    def link(m):
        x = m.group(1); sl = first.get(unicodedata.normalize('NFC', x))
        return f'[[{x}|{sl}]]' if sl else f'*{x}*'
    for d in E:
        for v in (d.get('t') or {}).values():
            if '[[' in v['x']: v['x'] = re.sub(r'\[\[([^\]|]+)\]\]', link, v['x'])
    homs = {}
    for d in E: homs.setdefault(d['sl'].rsplit('-', 1)[0] if re.search(r'-\d+$', d['sl']) else d['sl'], []).append(d)
    for base, ds in homs.items():
        if len(ds) > 1:
            for n, d in enumerate(ds, 1): d['hn'] = n
    # "see X": a Pāḷi span followed by ကြည့် (or လည်း ကြည့်), linked when X is a headword
    for d in E:
        b = d.get('b') or ''; see = []
        for sp in d.get('sp') or []:
            after = b[sp[1]:sp[1] + 16]
            if re.match(r'^\s*-?\s*(?:\([^)]{0,6}\)\s*-?\s*)?(?:တို့\s*)?(?:လည်း\s*)?ကြည့်', mynorm(after)):
                x = first.get(unicodedata.normalize('NFC', sp[2]))
                if x and x != d['sl']: see.append([sp[2], x])
        if see: d['see'] = see
        if d.get('c') and AK:
            cx = [cite_key(c, AK) for c in d['c']]
            if any(x >= 0 for x in cx): d['cx'] = cx
    # the thumb index and the chunks
    nav = [{'ro': ro, 'my': my, 'n': 0, 'books': [], 'groups': []} for ro, my in LETTERS]
    G = {}   # (letter, group) -> {'k', 'subs': {syll: [records]}, 'order': [syll]}
    other = []
    for d in E:
        kk = keys(d.get('r'))
        if not kk: other.append(d); continue
        li, gk, sk = kk
        L = nav[li]; L['n'] += 1
        if d['k'] not in L['books']: L['books'].append(d['k'])
        if (li, gk) not in G:
            G[(li, gk)] = {'k': gk, 'subs': {}, 'order': []}; L['groups'].append(G[(li, gk)])
        grp = G[(li, gk)]
        if sk not in grp['subs']: grp['subs'][sk] = []; grp['order'].append(sk)
        grp['subs'][sk].append(d)
    (OUT / 'data/c').mkdir(parents=True, exist_ok=True); (OUT / 'data/nav').mkdir(exist_ok=True)
    (OUT / 'data/s').mkdir(exist_ok=True)
    cn = 0; chunk_of = {}; ngroups = 0
    for li, L in enumerate(nav):
        out = []; shard = []
        for grp in L['groups']:
            recs = [d for sk in grp['order'] for d in grp['subs'][sk]]
            recs.sort(key=lambda d: d['g'])
            parts = [recs[i:i + CHUNK] for i in range(0, len(recs), CHUNK)]
            names = []
            for part in parts:
                name = str(cn); cn += 1; names.append(name)
                for d in part: chunk_of[d['g']] = name
                dump(OUT / f'data/c/{name}.json', part)
            subs = []
            for sk in grp['order']:
                cs = sorted({chunk_of[d['g']] for d in grp['subs'][sk]}, key=int)
                subs.append({'k': sk, 'n': len(grp['subs'][sk]), 'c': cs})
            out.append({'k': grp['k'], 'n': len(recs), 'subs': subs})
            shard += [[d['sl'], d.get('r', ''), d['h'], d['k'], d['p'], chunk_of[d['g']]] for d in recs]
        dump(OUT / f'data/nav/{li}.json', out)
        L['groups'] = len(out); ngroups += len(out)
        dump(OUT / f'data/s/{li}.json', shard)
    if other:   # headwords with no romanisation: kept findable by address, in a last chunk
        name = str(cn); cn += 1
        for d in other: chunk_of[d['g']] = name
        dump(OUT / f'data/c/{name}.json', other)
        dump(OUT / 'data/s/x.json', [[d['sl'], d.get('r', ''), d['h'], d['k'], d['p'], name] for d in other])
    dump(OUT / 'data/nav.json', {'letters': nav, 'total': len(E), 'unsorted': len(other)})
    dump(OUT / 'data/abbr.json', ABBR)
    matched = sum(1 for d in E for x in d.get('cx', []) if x >= 0)
    cites = sum(len(d.get('c') or []) for d in E)
    print(f'browse: {len(E):,} entries, {ngroups:,} groups, {cn:,} chunks; '
          f'see-links {sum(len(d.get("see", [])) for d in E):,}; citations matched {matched:,} of {cites:,} '
          f'({100 * matched / max(1, cites):.1f}%); without romanisation {len(other)}')
