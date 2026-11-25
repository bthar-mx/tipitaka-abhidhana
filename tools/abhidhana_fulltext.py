#!/usr/bin/env python3
"""Full-text search: the Pāḷi words inside the articles (docs/fulltext-search-plan.md; brief §98).

Called by tools/abhidhana_browse.py at the end of its build, with every record in the dictionary's order (`g`)
and its address (`sl`) already set. Writes, under site/dist/data/ft/:

    meta.json     {"keys": [shard keys], "block": B, "forms": n, "postings": n, "articles": n, "stop": [...]}
    s/<key>.json  {form: "g,g,…"}: every word form (romanised, as written) that begins with <key> once folded
                  (diacritics off, lower case: the fold of assets/common.js), each with the articles it occurs in,
                  as ordinals in the dictionary's order, delta-coded in base 36
    d/<n>.json    the articles B*n … B*n+B-1 by ordinal: [address, IAST, Burmese, book, PDF page] (+ [book of a
                  supplement row]), what a result line shows and links to

What is indexed: the Pāḷi passages romanise found inside each article's Burmese text (`sp`), with these left out
(the editor's decisions of 25 Nov 2026): passages that overlap one of the article's citations (the abbreviations of
the works cited, ဋ္ဌ → *ṭṭha* …), the forms in STOP (fragments of those abbreviations where the citation parser
missed them), and one-letter forms. The headword itself is not indexed here (the headword search covers it).
"""
import json, re, unicodedata
from collections import defaultdict

BLOCK = 500            # articles per d/ file
SPLIT_AT = 300_000     # a shard over this many bytes is split by one more letter
MAX_KEY = 5
# fragments of the citation abbreviations that are not Pāḷi words, where the parser missed the citation (measured
# 25 Nov 2026: found mostly inside citations, in ≥ 20 articles, and no headword; brief §98). Real words among the
# candidates (cariyā, therī, ani, dhā, pārā, gaṁ, ṭaṁ, maṭṭhā, nettaṁ) are kept.
STOP = {'ṭṭha', 'ṭhṭha', 'paṭisaṁ', 'mahāni', 'mahāna', 'mahāṭī', 'cūl', 'buddhavaṁ', 'buddhavā', 'buddhava',
        'suttani', 'khuddakaṭṭha', 'vibhāvinaṁ', 'sammo', 'theri'}
TOK = re.compile(r'[a-zāīūṁṅñṭḍṇḷ]+')
WS = re.compile(r'\s+')


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()


def cite_ranges(b, cites):
    """the character ranges of b where the citations stand (spaces ignored)"""
    if not b or not cites: return []
    pos = [i for i, ch in enumerate(b) if not ch.isspace()]
    comp = ''.join(b[i] for i in pos)
    out = []
    for c in cites:
        cc = WS.sub('', c or '')
        if len(cc) < 2: continue
        k = comp.find(cc)
        while k >= 0:
            out.append((pos[k], pos[k + len(cc) - 1] + 1)); k = comp.find(cc, k + 1)
    return out


def words(d):
    """the forms indexed for one record"""
    R = cite_ranges(d.get('b') or '', d.get('c'))
    out = set()
    for s in d.get('sp') or []:
        st, en, iast = s[0], s[1], s[2]
        if any(st < e and en > b for b, e in R): continue
        for t in TOK.findall(unicodedata.normalize('NFC', iast or '').lower().replace('ṃ', 'ṁ')):
            if len(t) >= 2 and t not in STOP: out.add(t)
    return out


def b36(n):
    s = ''
    while True:
        n, r = divmod(n, 36); s = '0123456789abcdefghijklmnopqrstuvwxyz'[r] + s
        if not n: return s


def enc(gs):
    prev, out = 0, []
    for g in gs: out.append(b36(g - prev)); prev = g
    return ','.join(out)


def build(OUT, E, dump):
    post = defaultdict(list)
    for d in E:
        for w in words(d): post[w].append(d['g'])
    for w in post: post[w].sort()
    # shards by folded prefix, split while too big
    def shard_of(keys_len, forms):
        groups = defaultdict(dict)
        for w in forms: groups[fold(w)[:keys_len]][w] = enc(post[w])
        return groups
    done = {}
    todo = [(2, list(post))]
    while todo:
        n, forms = todo.pop()
        for k, g in shard_of(n, forms).items():
            size = len(json.dumps(g, ensure_ascii=False, separators=(',', ':')).encode())
            # split further only if every form in it is longer than the key (else the short form stays here)
            if size > SPLIT_AT and n < MAX_KEY:
                short = {w: v for w, v in g.items() if len(fold(w)) <= n}
                rest = [w for w in g if len(fold(w)) > n]
                if short: done[k] = short
                todo.append((n + 1, rest))
            else:
                done.setdefault(k, {}).update(g)
    (OUT / 'data/ft/s').mkdir(parents=True, exist_ok=True); (OUT / 'data/ft/d').mkdir(parents=True, exist_ok=True)
    keys = sorted(done)
    for k in keys: dump(OUT / f'data/ft/s/{k}.json', done[k])
    for i in range(0, len(E), BLOCK):
        dump(OUT / f'data/ft/d/{i // BLOCK}.json',
             [[d['sl'], d.get('r', ''), d['h'], d['k'], d['p']] + ([d['kb']] if d.get('kb') else []) for d in E[i:i + BLOCK]])
    meta = {'keys': keys, 'block': BLOCK, 'forms': len(post), 'postings': sum(map(len, post.values())),
            'articles': len({g for v in post.values() for g in v}),
            'stop': sorted(STOP)}
    dump(OUT / 'data/ft/meta.json', meta)
    sizes = sorted((OUT / f'data/ft/s/{k}.json').stat().st_size for k in keys)
    print(f'fulltext: {meta["forms"]:,} forms, {meta["postings"]:,} postings in {meta["articles"]:,} articles; '
          f'{len(keys)} shards, {sum(sizes) / 1e6:.1f} MB (largest {sizes[-1] / 1e3:.0f} KB); '
          f'{(len(E) + BLOCK - 1) // BLOCK} article blocks')
    return meta
