#!/usr/bin/env python3
"""The Meaning box: drafted Spanish and English renderings of the Burmese explanations.

Two steps, around a drafting pass done outside this script:

    prep  <book>   writes tmp/meanings/work<book>.json and tmp/meanings/shards/NN.jsonl:
                   the Burmese explanation of each article, with the "see X" / "same meaning
                   as X" sentences replaced by placeholders «S1» «S2» …
    merge <book>   reads tmp/meanings/out/NN.jsonl (one {id, es, en, terms, flag} per line,
                   written by the drafting pass following docs/translation/drafting-brief.md) and
                   writes docs/translation/meanings/<book>.jsonl, which tools/abhidhana_site.py
                   reads into the records' `t` field.

The source of the Burmese is the PCED witness (witness/pced_k.jsonl.gz, joined by
witness/join-<book>.jsonl), whose definition line is the dictionary's text without our OCR
errors. Its licence is unresolved (brief §31). Where no witness row is joined, our OCR is used.
Each row records which one: `source`: pced | ocr.

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
SEE = re.compile(r'^(?P<x>[^။()]+?)\s*-?\s*(?P<pl>တို့\s*)?(?P<also>လည်း\s*)?ကြည့်(?:၍)?$')
SAME = re.compile(r'^(?P<x>[^။()]+?)\s*-?\s*(?:နှင့်\s*အနက်တူ(?:၏)?|,\s*တူ)$')


def pali_list(x):
    xs = [s.strip(' -') for s in re.split(r'[,၊]', x) if s.strip(' -')]
    if xs and all(not NOT_PALI.search(s) and ' ' not in s for s in xs): return xs


def prep(book, nshards=16):
    J = {j['id']: j for j in map(json.loads, open(ROOT / f'witness/join-{book}.jsonl', encoding='utf-8'))}
    need = {int(j['seq']) for j in J.values() if j.get('seq')}
    W = {}
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
        else:
            d = mn(P.get(a['id'], {}).get('body_joined') or '').strip(); src = 'ocr'
        if not d: continue
        F = {}; core = []
        for s in [s for s in re.split(r'(?<=။)\s*', d) if s.strip()]:
            t = s.strip().rstrip('။').strip(); kind = None
            m = SEE.match(t)
            if m and pali_list(m.group('x')):
                kind = 'also' if m.group('also') else 'see'; xs = pali_list(m.group('x'))
            else:
                m = SAME.match(t)
                if m and pali_list(m.group('x')): kind = 'same'; xs = pali_list(m.group('x'))
                elif re.sub(r'\s', '', t) == 'အထက်ပုဒ်နှင့်အနက်တူ': kind = 'prev'; xs = []
            if kind:
                k = f'«S{len(F) + 1}»'; F[k] = {'kind': kind, 'x': xs}; core.append(k)
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
    out = []
    for i, w in W.items():
        r = R.get(i)
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
    print(f'{book}: {len(out)} rows ({sum(r["method"] == "formula" for r in out)} formula, '
          f'{sum(r["method"] == "draft" for r in out)} drafted), {sum("flag" in r for r in out)} flagged; '
          f'{len(W) - len(out)} explanations without a row')


if __name__ == '__main__':
    {'prep': prep, 'merge': merge}[sys.argv[1]](sys.argv[2])
