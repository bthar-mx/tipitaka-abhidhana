#!/usr/bin/env python3
"""Romanise the Pāḷi in a volume's articles: headword, compound analysis, and the Pāḷi
quoted inside the Burmese definitions.

Reads ocr/<book>/articles.jsonl (written by abhidhana_articles.py) and writes
ocr/<book>/pali.jsonl, one line per article keyed by `id`, plus ocr/<book>/pali-report.md.
It does not modify articles.jsonl, so it can run after any regeneration of it.

Transliteration is Aksharamukha, Burmese -> IAST, with ṃ written ṁ as OSBCT writes it.

The hard part is not transliteration but deciding WHICH text is Pāḷi. A definition mixes
Burmese explanation with Pāḷi quotations and their references:

    လွန်၍ ပြောဆို၏။ ... ဘိက္ခုနိယော ဘိက္ခုနိယော အစ္စာဝဒတိ။ ဝိ၊၂။၃၄၅။

Both are in the same script. A token is taken as Pāḷi-shaped when it has none of the marks
Pāḷi in Burmese script never uses:
    asat ် (except inside the kinzi င်္), visarga း, dot below ့, the vowel ဲ,
    ိ and ု stacked on one consonant (ကို), and the Burmese symbols ၌ ၍ ၎ ၏.
That is necessary but not sufficient: many short Burmese words carry none of those marks
(သော, သူ, မှာ). So a run of consecutive Pāḷi-shaped tokens is accepted as a Pāḷi span only if

    it has two or more tokens and at least half of them are attested in OSBCT
    (whole, or with a quotation -ti / -ti stripped), or
    it is one token of at least 5 romanised letters that is attested.

Everything else is left as Burmese. Each span records how many of its tokens OSBCT attests,
so a reader can see how firm the call is.

Citations (ဝိ၊၂။၃၄၅။) are romanised mechanically, with Burmese numerals made Arabic:
`vi 2.345`. The abbreviations are not expanded to text names; that needs a table.
"""
import json, re, sys
from pathlib import Path
from aksharamukha import transliterate

ROOT = Path(__file__).resolve().parent.parent
MY_DIGITS = str.maketrans('၀၁၂၃၄၅၆၇၈၉', '0123456789')
NOT_PALI = re.compile('[း့ဲ၌၍၎၏]|ို|်(?!္)')
TOKEN = re.compile(r'[က-၉၌-႟္]+')
_cache = {}


def iast(s):
    if s not in _cache:
        _cache[s] = transliterate.process('Burmese', 'IAST', s).replace('ṃ', 'ṁ')
    return _cache[s]


def warm(tokens):
    """transliterate many tokens in one call (Aksharamukha is fast per call, not per token)"""
    todo = sorted({t for t in tokens if t not in _cache})
    for i in range(0, len(todo), 3000):
        chunk = todo[i:i + 3000]
        out = transliterate.process('Burmese', 'IAST', '\n'.join(chunk)).split('\n')
        if len(out) != len(chunk):
            out = [transliterate.process('Burmese', 'IAST', t) for t in chunk]
        for t, o in zip(chunk, out):
            _cache[t] = o.replace('ṃ', 'ṁ')


def pali_shaped(tok):
    # a token that starts with a combining mark (ီ, ူ …) is OCR debris, not a word
    return not NOT_PALI.search(tok) and not re.match('[\u102B-\u103E]', tok)


# short words that really do stand at the edge of a quotation; any other one- or two-letter
# token at a span's edge is taken as OCR debris and trimmed off
EDGE_OK = {'ca', 'vā', 'na', 'hi', 'pi', 'ti', 'me', 'te', 'no', 'so', 'sā', 'yo', 'ye', 'ko', 'kho'}


def attested(r, vocab):
    r = r.lower()
    if r in vocab: return True
    for suf in ('ti', 'nti', 'ī'):          # quotation particle glued on: ...ssāti, ...ntī
        if r.endswith('ti') and r[:-2] in vocab: return True
        if r.endswith('āti') and r[:-3] + 'a' in vocab: return True
        if r.endswith('īti') and r[:-3] + 'i' in vocab: return True
        if r.endswith('ūti') and r[:-3] + 'u' in vocab: return True
    return False


CITATION = re.compile(r'(?:[\u1000-\u1049\u104C-\u109F\u1039]{1,8}\s*[၊,.]\s*){1,3}[၀-၉]+(?:\s*[၊။,.\-]\s*[၀-၉]+)*\s*။?')


def spans(text, vocab):
    """Pāḷi spans in a Burmese text, as (start, end, burmese, iast, n_tokens, n_attested).

    References (ဝိ၊၂။၃၄၅။) are blanked out first, keeping offsets, so that an abbreviation
    is never read as the end of the quotation before it.
    """
    # a word broken across lines ("အစ္စာ-" / "ဝဒတိ") is rejoined, and line breaks become
    # spaces: lines are the printer's, not the text's. Offsets refer to this joined text,
    # which is stored as `body_joined` beside the spans.
    text = re.sub(r'-\s*\n\s*', '', text).replace('\n', ' ')
    blank = CITATION.sub(lambda m: ' ' * len(m.group()), text)
    toks = [(m.start(), m.end(), m.group()) for m in TOKEN.finditer(blank)
            if not re.fullmatch(r'[၀-၉]+', m.group())]
    out, run = [], []
    def close():
        while run and len(iast(run[0][2])) <= 2 and iast(run[0][2]) not in EDGE_OK: run.pop(0)
        while run and len(iast(run[-1][2])) <= 2 and iast(run[-1][2]) not in EDGE_OK: run.pop()
        if not run: return
        rs = [iast(t) for _, _, t in run]
        att = sum(attested(r, vocab) for r in rs)
        # one- and two-letter words (va, ma, dha) are attested by accident: OCR debris is made
        # of them. A span needs at least one attested word of four letters or more.
        strong = sum(1 for r in rs if len(r) >= 4 and attested(r, vocab))
        n = len(run)
        ok = strong >= 1 and ((n >= 2 and att * 2 >= n) or (n == 1 and len(rs[0]) >= 5))
        if ok:
            a, b = run[0][0], run[-1][1]
            seg = text[a:b]
            out.append(dict(start=a, end=b, my=seg, iast=romanise_segment(seg), tokens=n, attested=att))
        run.clear()
    prev_end = None
    for s, e, t in toks:
        gap = text[prev_end:s] if prev_end is not None else ''
        # a run continues across spaces, commas, hyphens and the Pāḷi ၊ ; it breaks at the
        # sentence-final ။, a line break, brackets and quotation marks
        if run and (re.search(r'[။()\[\]“”"=]', gap) or not pali_shaped(t)):
            close()
        if pali_shaped(t):
            run.append((s, e, t))
        prev_end = e
    close()
    return out


def romanise_segment(seg):
    out = []
    for piece in re.split(r'([က-၉၌-႟္]+)', seg):
        if TOKEN.fullmatch(piece or ' '):
            out.append(iast(piece).translate(MY_DIGITS))
        else:
            out.append(piece.replace('၊', ',').replace('။', '.'))
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def cite(c):
    """ဝိ၊၂။၃၄၅။ -> vi 2.345 ; ပဋိသံ၊ဋ္ဌ၊ ၁။၉၇။ -> paṭisaṁ ṭṭha 1.97"""
    m = re.match(r'(.*?)([၀-၉].*)$', c)
    if not m: return iast(c)
    abbr, nums = m.groups()
    abbr = ' '.join(iast(x) for x in re.split(r'[၊,.\s]+', abbr) if x)
    nums = re.sub(r'[၊။,.\s]+', '.', nums.translate(MY_DIGITS)).strip('.')
    return f'{abbr} {nums}'


def main(book):
    src = ROOT / f'ocr/{book}/articles.jsonl'
    rows = [json.loads(l) for l in src.open()]
    vp = ROOT / 'ocr/osbct_vocab.txt'
    vocab = set(vp.read_text().split('\n')) if vp.exists() else set()
    toks = []
    for r in rows:
        for f in ('headword', 'analysis', 'body'):
            if r.get(f): toks += TOKEN.findall(r[f])
        for c in r.get('citations') or []: toks += TOKEN.findall(c)
    warm(toks)

    out = []; n_sp = n_tok = n_att = 0; with_sp = 0
    for r in rows:
        d = dict(id=r['id'], book=r['book'], pdf_page=r['pdf_page'], headword=r['headword'],
                 headword_iast=r.get('iast') or iast(re.sub('[၀-၉\\s]', '', r['headword'])))
        if r.get('analysis'):
            parts = [p.strip() for p in r['analysis'].split('+')]
            d['analysis_iast'] = ' + '.join(romanise_segment(p) if pali_shaped(p.replace(' ', '')) else f'⟨{p}⟩'
                                            for p in parts if p)
        if r.get('body'):
            sp = spans(r['body'], vocab)
            if sp:
                d['pali'] = sp; with_sp += 1
                d['body_joined'] = re.sub(r'-\s*\n\s*', '', r['body']).replace('\n', ' ')
                n_sp += len(sp); n_tok += sum(s['tokens'] for s in sp); n_att += sum(s['attested'] for s in sp)
        if r.get('citations'):
            d['citations_iast'] = [cite(c) for c in r['citations']]
        d['status'] = 'ocr'
        out.append(d)
    (ROOT / f'ocr/{book}/pali.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in out))

    n = len(out)
    an = sum(1 for d in out if 'analysis_iast' in d)
    an_all = sum(1 for d in out if 'analysis_iast' in d and '⟨' not in d['analysis_iast'])
    rep = f"""# Vol. {book} — romanised Pāḷi

*`tools/abhidhana_romanise.py {book}` over `articles.jsonl`. Aksharamukha Burmese → IAST, ṃ written ṁ.
Output: `pali.jsonl`, one row per article, keyed by `id`.*

| | |
|---|---:|
| headwords romanised | {n:,} (all) |
| compound analyses romanised | {an:,} |
| of which every element Pāḷi-shaped | {an_all:,} = {100*an_all/max(an,1):.1f}% (the rest keep Burmese parts in ⟨ ⟩) |
| articles with Pāḷi found in the definition | {with_sp:,} = {100*with_sp/n:.1f}% |
| Pāḷi spans | {n_sp:,} |
| tokens in those spans | {n_tok:,}, of which **{100*n_att/max(n_tok,1):.1f}% attested in OSBCT** |
| citations romanised (mechanically, abbreviations not expanded) | {sum(len(d.get('citations_iast', [])) for d in out):,} |

What is and is not claimed:

- The **headword** romanisation rests on the index spelling, so it is as good as Aksharamukha.
- **Analyses and quoted Pāḷi** are romanised from OCR text. An OCR error becomes a romanisation
  error; the OSBCT attestation rate above is the measure of how much of it is clean.
- **Which text is Pāḷi** is decided by script shape plus OSBCT attestation (see the tool's
  docstring). Short Burmese words that look like Pāḷi can slip in when they sit next to
  attested Pāḷi, and a badly OCR'd quotation can be missed. Each span carries `tokens` and
  `attested` so its strength is visible.
- Nothing is reviewed. Every row is `status: "ocr"`.
"""
    (ROOT / f'ocr/{book}/pali-report.md').write_text(rep)
    print(rep)


if __name__ == '__main__':
    main(sys.argv[1])
