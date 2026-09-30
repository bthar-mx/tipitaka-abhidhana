"""Damaged citation abbreviations -> a key of docs/introduction/citation-abbreviations.tsv.

Used by abhidhana_browse.cite_key() for the site's tooltip only, when the exact and FOLD matches fail;
the citation text shown is never changed. Every rule was measured on all 530,965 citations and checked on
the page images (tmp/cite-norm/README.md, 29 Sep 2026): A (mechanical OCR forms of ၊ and the commentary
marks), T (whole-word misreadings), B1 (the niggahīta of အံ lost; ၊ဋ where only one reading is a key), and
the lost head အဋ္ဌ -> အံ၊ဋ္ဌ. Not resolved on purpose: ၊ဋ where both ၊ဋ္ဌ and ၊ဋီ are keys (the print has
either: 6 ဋ္ဌ / 11 ဋီ in two samples). Added 30 Sep: အပါ alone -> အပ၊ဋ္ဌ (16 / 16 on the page), and head() below.
resolve(k, K) takes the abbreviation part of a citation as cite_key() builds it (no spaces, no ။) and
returns the table key it maps to, or None.

head(k, before) (30 Sep 2026, tmp/cite-norm/section.md): a citation that is only the commentary mark (ဋ္ဌ၊၂။၁၇၉။,
ဋီ၊၁။, ဌ …) lost its work, and the work is almost always the word just before it in the body: the head
printed at a line's end (ပဋိသံ၊ / ဋ္ဌ), or ended by ။ instead of ၊ (ဇာ။ ဋ္ဌ), so the citation parser left it
out. head() returns that word, to be joined to the citation and matched again; only the one word right
before the citation is tried."""
import re

T = 'ဋ္ဌ'
TYPO = {'ဝိသဒိ': 'ဝိသုဒ္ဓိ', 'ဝိသုဒ္ဓါ': 'ဝိသုဒ္ဓိ', 'ပူလဋီ': 'မူလဋီ', 'မဏိမဉ္စူ': 'မဏိမဉ္ဇူ', 'ရတ္ထ': 'သာရတ္ထ',
        'ဝိ၊ဝိနိစ္ဆယ': 'ဝိ၊နိစ္ဆယ', 'ဝိ၊လင်္ကာရ': 'ဝိနယာလင်္ကာရ', 'မဟာဝံသ': 'မဟာဝံ', 'သုတ္တန': 'သုတ္တနိ',
        'ဝိမဘိ': 'ဝိမတိ'}
APA = {'အပါ', 'အပါဌ', 'အပါဋ'}   # အပါ alone read on the page 16 times (29-30 Sep): always အပ၊ဋ္ဌ, never အပ
FOLD = [(r'၊(?:ဌ|္ဌ)$', '၊' + T), (r'(?<=[^၊])ဋ္ဌ$', '၊' + T), (r'၊(?:ဋံ|ဋိ)$', '၊ဋီ'), (r'(?<=[^၊])ဋီ$', '၊ဋီ')]


def _mech(k):
    x = k.replace('ဋ်ဌ', T).replace('ဋ္ဋ', T)
    x = re.sub(r'(?<!ဋ)္ဌ', '၊' + T, x)                                   # ဝိ္ဌ: ဋ lost
    x = re.sub(r'([^၊])[ါု]?(ဋ္ဌ|ဋီ)', lambda m: m.group(1) + '၊' + m.group(2), x)  # မါဋ္ဌ, ဓမ္မုဋ္ဌ
    x = re.sub(r'၊(?:ဋံ|ဋိ)(?=၊|$)', '၊ဋီ', x)
    x = re.sub(r'(?<=[^၊])(?:ဋံ|ဋိ)(?=၊|$)', 'ဋီ', x)                    # အနုဋံ, မူလဋိ
    x = re.sub(r'ဋီသစ်$', 'ဋီ၊သစ်', x)
    x = re.sub(r'([^၊])ဋီ၊သစ်$', r'\1၊ဋီ၊သစ်', x)
    x = re.sub(r'ါ(?=၊)', '', x)                                           # အပါ၊ဋ္ဌ
    x = re.sub(r'၊ဌ(?=၊|$)', '၊' + T, x)
    x = re.sub(r'([^၊္])ဌ$', r'\1၊' + T, x)                                # အပါဌ
    return x


def _key(x, K):
    if x in K: return x
    for a, b in FOLD: x = re.sub(a, b, x)
    return x if x in K else None


def _a(k, K):
    if k in APA: return 'အပ၊ဋ္ဌ' if 'အပ၊ဋ္ဌ' in K else None                    # အပါ: 16 / 16 အပ၊ဋ္ဌ on the page
    return _key(_mech(k), K)


def _t(k, K):
    for a, b in TYPO.items():
        if k.startswith(a):
            y = b + k[len(a):]
            return _key(y, K) or _a(y, K)
    return None


def _b1(k, K):
    out = set()
    if re.search(r'၊ဋ$', k):
        for y in (k[:-1] + T, k[:-1] + 'ဋီ'):
            z = _key(y, K) or _a(y, K)
            if z: out.add(z)
    if k == 'အ' or k.startswith('အ၊') or k.startswith('အါ'):
        y = 'အံ' + k[1:]
        z = _key(y, K) or _a(y, K)
        if z: out.add(z)
    return out.pop() if len(out) == 1 else None


def resolve(k, K):
    if not k: return None
    if k == 'အဋ္ဌ': return 'အံ၊ဋ္ဌ' if 'အံ၊ဋ္ဌ' in K else None               # lost head: 5 / 5 on the page
    return _a(k, K) or _t(k, K) or _b1(k, K)


LOST = re.compile(r'^(?:ဋ္ဌ|ဋီ|ဌ|ဋ|ဋိ|ဋံ|္ဌ)(?:၊|$)')          # the citation begins with the mark: its work is lost
HEADTYPO = {'သုတ္တန်': 'သုတ္တနိ'}                                   # the print's သုတ္တနိ read with an asat


def head(k, before):
    """the word right before a lost-head citation in the body (its work, cut off by the parser), or None"""
    if not before or not LOST.match(k): return None
    toks = before.split()
    if not toks: return None
    t = re.sub(r'^[(\[\-–]+', '', re.sub(r'[။၊\-–,.]+$', '', toks[-1]))
    t = t.rsplit('။', 1)[-1]
    if not t or re.search('[၀-၉0-9]', t): return None
    return HEADTYPO.get(t, t)
