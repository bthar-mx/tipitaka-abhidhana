#!/usr/bin/env python3
"""The Meaning box: drafted Spanish and English renderings of the Burmese explanations.

Two steps, around a drafting pass done outside this script:

    prep  <book>   writes tmp/meanings/work<book>.json and tmp/meanings/shards/NN.jsonl:
                   the Burmese explanation of each article, with the "see X" / "same meaning
                   as X" sentences replaced by placeholders «S1» «S2» …
    report <book>  writes meanings/<book>-flags.tsv and <book>-terms.tsv after merge
    merge <book>   reads tmp/meanings/out/NN.jsonl (one {id, es, en, terms, flag} per line,
                   written by the drafting pass following docs/translation/drafting-brief.md) and
                   writes docs/translation/meanings/<book>.jsonl, which tools/abhidhana_site.py
                   reads into the records' `t` field. A draft's `omitted` (what a draft from our own
                   text left out) is not put in the rows but in <book>-omitted.tsv.

The source of the Burmese is the PCED witness (witness/pced_k.jsonl.gz, joined by
witness/join-<book>.jsonl), whose definition line is the dictionary's text without our OCR
errors. Its licence is unresolved (brief §31). Where no witness row is joined, our OCR is used.
A book with no witness join at all (14/2, 14/3, 20-25, 4/3) takes its Burmese from our text,
without the Pāḷi quotations and the citations (our_text). Each row records which one:
`source`: pced | ocr | text layer (14/2, from the PDF's typeset text, brief §25).

Only the Burmese is translated. Pāḷi in the definition (words, compounds and quoted passages) is
kept, romanised: the drafts mark it ⟦burmese⟧ and this script transliterates it (Aksharamukha,
as tools/abhidhana_romanise.py), or ⟦=iast⟧ for a technical term the draft kept in Pāḷi.
The output uses a small markup that assets/browse.js renders: *pāḷi* in italics, [[iast]] a
link to a headword (resolved by tools/abhidhana_browse.py; unresolved ones become *iast*),
‹…› a Burmese word the draft could not translate.

Every row is `drafted` in both languages. A reviewer changes status_es / status_en to
reviewed or corrected; nothing drafted is presented as a reading.
"""
import glob, gzip, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'tmp/meanings'   # working files, gitignored (vol. 1's were in the VM)
mn = lambda t: (t or '').replace('့်', '့်')
NOT_PALI = re.compile('[း့ဲ၌၍၎၏]|ို|်(?!္)')
SEE = re.compile(r'^(?P<x>[^။()]+?)\s*-?\s*(?:\((?P<n>[၀-၉က-အ]{1,2}(?:-[၀-၉က-အ]{1,2})?)\)\s*-?\s*)?(?P<pl>တို့\s*)?(?P<also>လည်း\s*-?\s*)?ကြည့်(?:၍)?$')
SAME = re.compile(r'^(?P<x>[^။()]+?)\s*-?\s*(?:\((?P<n>[၀-၉က-အ]{1,2}(?:-[၀-၉က-အ]{1,2})?)\)\s*-?\s*)?(?:နှင့်\s*အနက်တူ(?:၏)?|,\s*တူ)$')
# from vol. 4/1 (26 Sep 2026): sense markers or a label before the formula, "(၂)" after X, the whole
# formula in brackets, and "လည်း-ကြည့်", which prep 01–03 left for the drafts to render by hand
PRE = re.compile(r'^((?:\([^()]{1,8}\)\s*)+)')
SENSE = dict(zip('၀၁၂၃၄၅၆၇၈၉', '0123456789')) | dict(zip('ကခဂဃငစဆဇဈည', 'abcdefghij'))


def formula_of(t):
    """(prefix, form, bracketed) if t is a see / see-also / same-meaning sentence, else None"""
    pre = ''; br = False
    if t.startswith('(') and t.endswith(')') and t.count('(') == 1: t = t[1:-1].strip(); br = True
    m = PRE.match(t)
    if m: pre = m.group(1); t = t[m.end():].strip()
    m = SEE.match(t)
    if m and pali_list(m.group('x')):
        f = {'kind': 'also' if m.group('also') else 'see', 'x': pali_list(m.group('x'))}
    else:
        m = SAME.match(t)
        if not (m and pali_list(m.group('x'))): return None
        f = {'kind': 'same', 'x': pali_list(m.group('x'))}
    if m.group('n'): f['n'] = ''.join(SENSE.get(c, c) for c in m.group('n'))
    return pre, f, br


def pali_list(x):
    xs = [s.strip(' -') for s in re.split(r'[,၊]', x) if s.strip(' -')]
    if xs and all(not NOT_PALI.search(s) and ' ' not in s for s in xs): return xs


LEGACY = {'01', '02', '03'}


# a citation of a work in one volume, which CITE does not parse: abbreviation ။ page ။ (မိလိန္ဒ။၁၂၃။)
_AB = r'[\u1000-\u1036\u1039\u103B-\u103F\u104C-\u109F]{1,8}'   # letters: no digit, asat, visarga or dot below
CITE_WORK = re.compile(r'(?<![\u1000-\u109F])((?:' + _AB + r'\s*၊\s*){0,2}' + _AB + r')\s*။\s*[၀-၉]+(?:\s*[-၊။,.]\s*[၀-၉]+)*\s*။')
# Burmese read as a Pāḷi span by tools/abhidhana_romanise.py (…-သော၊ သတိ / ကင်းလွတ်, ပညာ ရှိသော):
# its words are joined by the Burmese hyphen, or it holds one of these words
NOT_QUOTED = {'ရှိသော', 'စသော', 'အရာ', 'သောအရာ'}


def quoted(s, J):
    """a Pāḷi span of two words or more that is a quotation, not Burmese read as Pāḷi"""
    ws = re.split(r'[\s၊,]+', s['my'].strip())
    return (s['tokens'] >= 2 and '-' not in s['my'] and ws[-1] != 'သော' and not NOT_QUOTED & set(ws)
            and J[s['end']:s['end'] + 1] != '-' and (J[s['start'] - 1:s['start']] != '-' or J[s['start'] - 2:s['start']] == '(-'))


# a list of inflected forms, each with its page numbers, joined by dashes: ပမုစ္စန္တိ — ပမုစ္စေ — ၂၄၈-၉။
FORM_DASH = re.compile(r'(?:^|(?<=[\s။(—–-]))([^\s။၊()—–-]+(?:-[^\s။၊()—–-]+)?)(?:\s*\([^()]*\))?\s*(?:—+|–+|-{2,})\s*(?:[၀-၉][-၀-၉၊,.]*\s*။?)?')
_WORKS = []
# abbreviations with an asat, which abhidhana_articles.py's cite_trim takes for Burmese and drops
WORKS_ASAT = {'ဣတိဝုတ်', 'ဣတိဝုတ်၊ဋ္ဌ', 'ကင်္ခါ၊ဋီ၊သစ်', 'ကင်္ခါ၊ဋီ၊ဟောင်း', 'ပါစိတ်၊ယော', 'ဓါန်', 'ဓါန်၊ဋီ', 'ဇာတ်၊ဋီ၊သစ်'}


def works():
    """the works' abbreviations as the citations print them (ဣတိဝုတ်၊ဋ္ဌ, ဝဇိရ): every one parsed in any
    book (abhidhana_articles.py citations, CITE_WORK) at least five times. A sentence that is only
    one of them is a citation that lost its numbers."""
    if not _WORKS:
        import collections
        C = collections.Counter()
        for f in sorted(glob.glob(str(ROOT / 'ocr/*/articles.jsonl'))):
            for l in open(f, encoding='utf-8'):
                a = json.loads(l)
                for c in a.get('citations') or []: C[re.sub(r'[၊,.]?[၀-၉][-၀-၉၊။,.]*$', '', c).rstrip('၊။,.')] += 1
                for m in CITE_WORK.finditer(a.get('body') or ''): C[re.sub(r'\s', '', m.group(1))] += 1
        _WORKS.append({k for k, n in C.items() if n >= 5 and k and not re.search('[၀-၉]', k)} | WORKS_ASAT)
    return _WORKS[0]


def our_text(a, p):
    """The Burmese explanation from our own text (a book with no witness join): the article's
    body with its printer's line breaks undone, the Pāḷi quotations and the citations left out.

    A hyphen at a line's end is kept where the Burmese has one (မေ့- / မေ့လျော့-ခြင်း) and dropped
    inside a Pāḷi span, where it only breaks a word (စိတ္တ- / က္ခေပေါ). The spans are
    pali.jsonl's, whose offsets are into body_joined; body_joined is rebuilt here from the body
    (as tools/abhidhana_romanise.py builds it) to carry them over. Spans of two words or more are
    removed (quoted()); a one-word span (a term inside a Burmese sentence) is kept. Citations are
    removed as abhidhana_articles.py parses them (CITE, cite_trim), with any page numbers left
    after; so are bracketed references, (ဓမ္မ။ ၅၇), and the lists of further ones, (-ဝိ၊၁။၃၆။ …).
    Where the analysis bracket was damaged, the body starts with the rest of the analysis and its
    derivation, up to ]: that part is left out too (PCED keeps it out of the definition line)."""
    sys.path.insert(0, str(ROOT / 'tools')); from abhidhana_articles import CITE, cite_trim
    body = a.get('body') or ''
    J = []; out = []   # J: body_joined as rebuilt; out: (character, its index in J, kind)
    for piece in re.split(r'(-\s*\n\s*|\n)', body):
        if not piece: continue
        if piece == '\n': out.append((' ', len(J), 'nl')); J.append(' ')
        elif piece.startswith('-') and '\n' in piece: out.append(('-', len(J), 'hy'))
        else:
            for c in piece: out.append((c, len(J), 'c')); J.append(c)
    J = ''.join(J)
    if p.get('body_joined') and p['body_joined'] != J: raise ValueError(f"{a['id']}: body_joined does not match the body")
    sp = p.get('pali') or []
    cut = set()
    i = J.find(']')
    if a.get('analysis_bracket_damaged') and i >= 0 and '[' not in J[:i]: cut.update(range(i + 1))
    for s in sp:
        if quoted(s, J): cut.update(range(s['start'], s['end']))
    for m in CITE.finditer(J):
        t = cite_trim(m.group()); e = m.end()
        n = re.match(r'(?:\s*[-၊။,.]\s*[၀-၉]+)*\s*။?', J[e:])   # the rest of a page list: ၁၂၀-၁။
        cut.update(range(e - len(t), e + n.end()))
    for m in CITE_WORK.finditer(J): cut.update(range(m.start(1), m.end()))
    for m in re.finditer(r'\([^()]*\)', J):
        x = m.group()[1:-1]
        if (x.lstrip().startswith('-') and '။' in x) or (re.search('[၀-၉]', x) and re.search('[၊။]', x) and not re.search('[\u103A\u1037\u1038]', x)):
            cut.update(range(m.start(), m.end()))
    t = ''.join('' if j in cut else c if k != 'hy' else '' if any(s['start'] < j < s['end'] for s in sp) else '-'
                for c, j, k in out)
    t = re.sub(r'\s+', ' ', t)
    for _ in range(3):   # what the cuts leave behind: page numbers of a citation CITE does not parse
        # (ဗုဒ္ဓဝံ၊ဋ္ဌ။၉၅။, whose abbreviation went with the Pāḷi spans), empty quotation marks and
        # brackets, doubled or stray punctuation
        t = re.sub(r'(^|[။၊(])\s*-?\s*[၀-၉]+(?:\s*[-၊,.]\s*[၀-၉]+)*\s*-?\s*။', r'\1', t)
        t = re.sub(r'“\s*”(?:န္တိ|တိ)?|\(\s*[-၊။,.\s]*\)|\[\s*[-၊။,.\s]*\]', ' ', t)
        t = re.sub(r'\s*([၊။])(?:\s*[၊။,.])+', r'\1', t)
        t = re.sub(r'^\s*[-၊။,.]+\s*', '', t)
        t = re.sub(r'\s+([၊။])', r'\1', t)
        t = re.sub(r'\s+', ' ', t).strip()
    # a sentence left holding only a one-word Pāḷi span (the lemma of a quoted gloss: ပမတ္တော။), or
    # only sense markers, quotation marks and brackets (a sense explained only by a quotation: (၂)။)
    # then a sentence that is only a work's abbreviation, a citation without its
    # numbers (ဝဇိရ။), and the lists of inflected forms joined by dashes
    t = FORM_DASH.sub(lambda m: '' if not NOT_PALI.search(m.group(1)) else m.group(), t)
    t = re.sub(r'\s+', ' ', re.sub(r'\s+([၊။])', r'\1', t)).strip()
    one = {s['my'] for s in sp if s['tokens'] == 1}
    W = works()
    def keep(x):
        y = x.rstrip('။').strip()
        return (y not in one and re.sub(r'\s', '', re.sub(r'^(?:\([^()]{1,4}\)\s*)+', '', y)).rstrip('၊') not in W
                and not re.fullmatch(r'(?:\([^()]{1,4}\)|[“”()\[\]\s?။])*', x))
    return ' '.join(x for x in re.split(r'(?<=။)\s*', t) if keep(x))


def prep(book, nshards=16):
    jp = ROOT / f'witness/join-{book}.jsonl'
    J, W = {}, {}
    if jp.exists():
        J = {j['id']: j for j in map(json.loads, open(jp, encoding='utf-8'))}
        need = {int(j['seq']) for j in J.values() if j.get('seq')}
        for l in gzip.open(ROOT / 'witness/pced_k.jsonl.gz', 'rt', encoding='utf-8'):
            w = json.loads(l)
            if w['seq'] in need: W[w['seq']] = w
    P = {}
    for l in open(ROOT / f'ocr/{book}/pali.jsonl', encoding='utf-8'):
        p = json.loads(l); P[p['id']] = p
    out = []
    for l in open(ROOT / f'ocr/{book}/articles.jsonl', encoding='utf-8'):
        a = json.loads(l)
        j = J.get(a['id']); w = W.get(int(j['seq'])) if j and j.get('seq') else None
        if w and w.get('definition'):
            d = mn(w['definition'].split('\n')[0]).strip(); src = 'pced'
        elif jp.exists():
            d = mn(P.get(a['id'], {}).get('body_joined') or '').strip(); src = 'ocr'
        else:   # no witness join: our own text, the quotations and citations left out
            d = mn(our_text(a, P.get(a['id'], {}))).strip(); src = 'text layer' if book == '14b' else 'ocr'
        if not d: continue
        F = {}; core = []
        for s in [s for s in re.split(r'(?<=။)\s*', d) if s.strip()]:
            t = s.strip().rstrip('။').strip()
            r = formula_of(t) if book not in LEGACY else None
            if book in LEGACY:   # vols. 1-3 were drafted with prep's first pattern; keep their placeholders
                m = SEE.match(t)
                if m and not m.group('n') and pali_list(m.group('x')) and '-' not in (m.group('also') or ''):
                    r = ('', {'kind': 'also' if m.group('also') else 'see', 'x': pali_list(m.group('x'))}, False)
                else:
                    m = SAME.match(t)
                    if m and not m.group('n') and pali_list(m.group('x')): r = ('', {'kind': 'same', 'x': pali_list(m.group('x'))}, False)
            if not r and re.sub(r'\s', '', t) == 'အထက်ပုဒ်နှင့်အနက်တူ': r = ('', {'kind': 'prev', 'x': []}, False)
            if r:
                pre, f, br = r
                k = f'«S{len(F) + 1}»'; F[k] = f
                core.append((pre + ' ' if pre else '') + (f'({k})' if br else k))
            else:
                core.append(s.strip())
        text = ' '.join(core)
        out.append({'id': a['id'], 'hw': a['headword'], 'iast': a.get('iast') or P.get(a['id'], {}).get('headword_iast', ''),
                    'label': a.get('label'), 'src': src, 'text': text, 'forms': F,
                    'only': not re.sub(r'«S\d+»|\s', '', text)})
    (WORK / 'shards').mkdir(parents=True, exist_ok=True)
    json.dump(out, open(WORK / f'work{book}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    todo = [o for o in out if not o['only']]; size = -(-len(todo) // nshards)
    for k in range(nshards):
        with open(WORK / f'shards/{k:02d}.jsonl', 'w', encoding='utf-8') as f:
            for o in todo[k * size:(k + 1) * size]:
                f.write(json.dumps({'id': o['id'], 'iast': o['iast'], 'label': o['label'], 'text': o['text']}, ensure_ascii=False) + '\n')
    print(f'{book}: {len(out)} explanations, {sum(o["only"] for o in out)} formula-only, {len(todo)} to draft in {nshards} shards')


FORM = {'es': {'see': ('Véase', 'Véanse'), 'also': ('Véase también', 'Véanse también'), 'same': 'Mismo significado que',
               'prev': 'Mismo significado que la entrada anterior.'},
        'en': {'see': ('See', 'See'), 'also': ('See also', 'See also'), 'same': 'Same meaning as',
               'prev': 'Same meaning as the preceding headword.'}}


def merge(book):
    from aksharamukha import transliterate
    cache = {}
    def iast(s):
        if s not in cache: cache[s] = transliterate.process('Burmese', 'IAST', s).replace('ṃ', 'ṁ')
        return cache[s]
    def pali(m):
        x = m.group(1).strip()
        return '*' + (x[1:].strip() if x.startswith('=') else iast(x.replace("'", '').strip())) + '*'
    def formula(f, lang):
        F = FORM[lang]; k = f['kind']
        if k == 'prev': return F['prev']
        xs = ', '.join(f'[[{iast(x)}]]' for x in f['x'])
        if f.get('n'): xs += f" ({f['n']})"
        return f"{F['same']} {xs}." if k == 'same' else f"{F[k][len(f['x']) > 1]} {xs}."
    W = {o['id']: o for o in json.load(open(WORK / f'work{book}.json', encoding='utf-8'))}
    R = {}
    for f in sorted(glob.glob(str(WORK / 'shards/[0-9][0-9].jsonl'))):
        ids = {json.loads(l)['id'] for l in open(f, encoding='utf-8')}
        own = WORK / 'out' / Path(f).name
        for g in [own] + [Path(x) for x in sorted(glob.glob(str(WORK / 'out/[0-9][0-9].jsonl'))) if Path(x) != own]:
            if not g.exists(): continue
            for l in open(g, encoding='utf-8'):
                try: o = json.loads(l)
                except ValueError: continue
                if o['id'] in ids and o['id'] not in R: R[o['id']] = o
    out = []; omitted = []
    for i, w in W.items():
        r = R.get(i)
        if r and r.get('omitted'): omitted.append((i, w['iast'], r['omitted']))
        if w['only']: es = en = w['text']; flag = ''; terms = []; method = 'formula'
        elif r: es, en, flag, terms = r.get('es', ''), r.get('en', ''), r.get('flag', ''), r.get('terms', []); method = 'draft'
        else: continue
        row = {'id': i, 'iast': w['iast']}
        for lang, t in (('es', es), ('en', en)):
            for k, f in w['forms'].items(): t = t.replace(k, formula(f, lang))
            t = re.sub(r'⟦([^⟧]*)⟧', pali, t)
            # a "see X" the draft wrote out itself becomes a link too
            t = re.sub(r'((?:Véan?se|See)(?: también| also)? )((?:\*[^*]+\*(?:,? (?:y |and )?)?)+)',
                       lambda m: m.group(1) + re.sub(r'\*([^*]+)\*', r'[[\1]]', m.group(2)), t)
            t = re.sub(r'((?:Mismo significado que|Same meaning as) )\*([^*]+)\*', r'\1[[\2]]', t)
            row[lang] = re.sub(r'\s+', ' ', t).strip()
        row.update(status_es='drafted', status_en='drafted', source=w['src'], method=method)
        if flag: row['flag'] = flag
        if terms: row['terms'] = terms
        if row['es'] or row['en']: out.append(row)
    dest = ROOT / f'docs/translation/meanings/{book}.jsonl'
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    if omitted:   # what a draft from our own text left out (quotation fragments, citations …): kept apart, not in the rows
        with open(ROOT / f'docs/translation/meanings/{book}-omitted.tsv', 'w', encoding='utf-8') as f:
            f.write('id\tiast\tomitted\n')
            for i, x, o in omitted: f.write(f"{i}\t{x}\t{o.replace(chr(9), ' ').replace(chr(10), ' ')}\n")
    print(f'{book}: {len(out)} rows ({sum(r["method"] == "formula" for r in out)} formula, '
          f'{sum(r["method"] == "draft" for r in out)} drafted), {sum("flag" in r for r in out)} flagged; '
          f'{len(W) - len(out)} explanations without a row')


def report(book):
    """docs/translation/meanings/<book>-flags.tsv (flagged rows with the Burmese) and <book>-terms.tsv
    (Pāḷi terms kept, by number of articles). Vols. 1-3's were written by hand with the same code."""
    import collections
    W = {w['id']: w for w in json.load(open(WORK / f'work{book}.json', encoding='utf-8'))}
    R = [json.loads(l) for l in open(ROOT / f'docs/translation/meanings/{book}.jsonl', encoding='utf-8')]
    cl = lambda s: (s or '').replace('\t', ' ').replace('\n', ' ')
    with open(ROOT / f'docs/translation/meanings/{book}-flags.tsv', 'w', encoding='utf-8') as f:
        f.write('id\tiast\tburmese\tes\ten\tflag\n')
        for r in R:
            if r.get('flag'):
                f.write('\t'.join([str(r['id']), r['iast'], cl(W[r['id']]['text']), cl(r['es']), cl(r['en']), cl(r['flag'])]) + '\n')
    C = collections.Counter(t for r in R for t in set(r.get('terms', [])))
    with open(ROOT / f'docs/translation/meanings/{book}-terms.tsv', 'w', encoding='utf-8') as f:
        f.write('term\tarticles\tproposal\n')
        for t, n in sorted(C.items(), key=lambda x: (-x[1], x[0])):
            f.write(f'{t}\t{n}\tkeep in Pāḷi (drafts); IEBH to fix a rendering\n')
    print(f'{book}: {sum(1 for r in R if r.get("flag"))} flagged, {len(C)} terms')


if __name__ == '__main__':
    {'prep': prep, 'merge': merge, 'report': report}[sys.argv[1]](sys.argv[2])
