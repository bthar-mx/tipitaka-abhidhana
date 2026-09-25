#!/usr/bin/env python3
"""Cut a volume's OCR into articles, anchored on the app's index, and romanise the headwords.

Reads ocr/<book>/pages/p*.json (from abhidhana_ocr.py --columns) and writes
ocr/<book>/articles.jsonl plus a report.

How an article is found. For every indexed page the headwords are known, in printed order,
from db/tipitaka_abidan.db. Each is looked for in the column-cut text (left column, then
right), moving forward only, so a headword is never placed before the one that precedes it:

    verbatim   the headword occurs after the previous one, preferring an occurrence at the
               start of a line or followed by a ( or [ -- this is what tells an entry from a
               cross-reference inside another article ("X-ကြည့်").
    fuzzy      not verbatim, but a line inside the span bounded by its located neighbours
               begins with a string >= 0.80 similar to it.
    unlocated  neither. The article's text then stays inside its predecessor's, and the
               row carries no body.

An article runs from its headword to the next located headword; the last on a page runs on
into the head of the next page (text before that page's first located headword).

Fields are then read off the article's text: the grammatical label in ( ), the compound
analysis in [ ], the rest as body, and the citations inside the body (abbreviation, then
Burmese numerals separated by ၊, closed by ။) collected into a list. The body is kept
whole; the citations are not removed from it.

Nothing here is reviewed. Every row carries status "ocr" and the Burmese is raw OCR.
"""
import json, re, sqlite3, sys, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
nfc = lambda s: unicodedata.normalize('NFC', s)
MY_DIGITS = '၀၁၂၃၄၅၆၇၈၉'


def flatmap(text):
    """whitespace-free text, and for each of its characters the offset in the original"""
    chars, offs = [], []
    for i, ch in enumerate(text):
        if not ch.isspace(): chars.append(ch); offs.append(i)
    return ''.join(chars), offs


def header_cut(col):
    """drop the running head: the first line of a column, if it is short.

    Cut at the gutter, the head splits into the left headword on the left column's first
    line and the page number + right headword on the right's. Both are real headwords of
    the page and would otherwise be taken for the first article.
    """
    lines = col.split('\n')
    while lines and not lines[0].strip(): lines.pop(0)
    if lines and len(re.sub(r'\s', '', lines[0])) <= 24: lines.pop(0)
    return '\n'.join(lines)


def page_text(rec):
    t = rec['text'].get('col.psm6', '')
    # abhidhana_ocr.py joins the two columns with one '\n'; tesseract ends each with a form
    # feed, which is where to split.
    parts = t.split('\x0c')
    cols = [p for p in parts if p.strip()]
    return '\n'.join(header_cut(c) for c in cols)


def locate(text, gold):
    """Place each known headword in the page text, in printed order. See the module doc.

    Occurrences after the previous headword are ranked, and the first of the best rank is
    taken:  4 at a line start and followed by ( or [ ;  3 followed by ( or [ ;  2 at a line
    start and followed by a space.  A bare occurrence inside running text (rank 1) is the
    commonest false hit -- the headword quoted in another article, or a longer word that
    begins with it -- so it is tried only after the bounded fuzzy match has failed.
    Headwords of one or two characters (အ, အံ) need rank 3 or better.
    """
    f, offs = flatmap(text)
    line_starts = {0}
    for m in re.finditer('\n', text):
        k = len(re.sub(r'\s', '', text[:m.start() + 1]))
        line_starts.add(k)
    def rank(j, n):
        e = j + n
        nxt = f[e:e + 1]
        spaced = e >= len(f) or offs[e] - offs[e - 1] > 1
        ls = j in line_starts
        if nxt in ('(', '[', '（'): return 4 if ls else 3
        if n <= 2: return 0
        if ls and spaced: return 2
        return 1 if spaced else 0
    loose = lambda s: s.replace('ံ', '').replace('့', '')
    pos = [None] * len(gold); how = ['unlocated'] * len(gold); inline = [None] * len(gold)
    cur = 0
    for i, g in enumerate(gold):
        h = re.sub(r'\s', '', g); best = (0, None); j = f.find(h, cur)
        while j != -1:
            r = rank(j, len(h))
            if r > best[0]: best = (r, j)
            if r == 4: break
            j = f.find(h, j + 1)
        if best[0] >= 2:
            pos[i] = best[1]; how[i] = 'verbatim'; cur = best[1] + len(h)
        elif best[0] == 1:
            inline[i] = best[1]
    for i, g in enumerate(gold):
        if pos[i] is not None: continue
        h = loose(re.sub(r'\s', '', g))
        lo = max([pos[k] + 1 for k in range(i) if pos[k] is not None], default=0)
        hi = min([pos[k] for k in range(i + 1, len(gold)) if pos[k] is not None], default=len(f))
        cand = []
        for s in line_starts:
            if not (lo <= s < hi): continue
            seg = f[s:s + len(h) + 6]
            head = loose(seg)[:len(h)]
            # a fuzzy placement must be followed, within a few characters, by the ( of the
            # grammatical label or the [ of the analysis: without that, a line that merely
            # begins with a similar word (a quotation, a citation) wins too often
            if not re.search(r'[(\[（]', seg[max(1, len(h) - 3):]): continue
            r = SequenceMatcher(None, head, h).ratio()
            cand.append((r, -s, s))
        if cand:
            r, _, s = max(cand)
            if r >= .80: pos[i] = s; how[i] = 'fuzzy'; continue
        if inline[i] is not None and lo <= inline[i] < hi:
            pos[i] = inline[i]; how[i] = 'verbatim-inline'
    return f, offs, pos, how


LABEL = re.compile(r'^\s*[\(（]\s*([^)）\n]{1,14}?)\s*[\)）]')
ANALYSIS = re.compile(r'^\s*\[([^\]\n]{0,90}(?:\n[^\]\n]{0,90})?)\]')
CITE = re.compile(r'[\u1000-\u1049\u104C-\u109F]{1,8}\s*[၊,.]\s*[' + MY_DIGITS + r']+(?:\s*[၊။,.]\s*[' + MY_DIGITS + r']+)*\s*။')

# Burmese marks that Pāḷi written in Burmese script never carries: asat, visarga-tone, dot-below
BURMESE_ONLY = re.compile('[\u103A\u1038\u1037\u104A\u104B]')


def normalise_analysis(a):
    """Put back the + signs of a compound analysis that OCR lost or misread.

    The analysis is printed as Pāḷi elements joined by +, e.g. [အတိ + အာ + ဝဒ + အ + တိ]. OCR
    reads + as ၂ and often drops it altogether: that article came out "အတိ ၂ အာ ဝဒ အ တိ"
    (vol. 1 p. 300, reported by Angel). Two repairs, and only these:

    - a free-standing ၂ between elements becomes +  (a digit is never an element);
    - when every token is Pāḷi -- no asat, visarga or dot-below, none of the ။ ၊ that start a
      derivation note -- the tokens are joined with ' + ', and a hyphen left dangling at a
      token's end (the other common misreading of +) is dropped.

    An analysis holding a derivation note or Burmese words is left as read, apart from the
    ၂ repair. Returns (text, changed).
    """
    t = re.sub(r'\s+', ' ', a).strip()
    # ၂ standing alone between elements (not part of a number, not a "-ကြည့်" cross-reference)
    # (skipped when the analysis holds a derivation note: there ၁ ... ၂ number its parts)
    if not re.search(r'[။(]', t):
      t = re.sub(r'(?<=[^\s၀-၉])(?:\s+|\s*-\s*)၂\.?(?:\s*-\s*|\s+)(?![၀-၉]|ကြည့်)(?=\S)', ' + ', t)
    toks = [x for x in re.split(r'\s*\+\s*|\s+', t) if x]
    if toks and all(not BURMESE_ONLY.search(x) and not re.search(r'[()\[\]=]', x) for x in toks):
        open_end = bool(re.search(r'[+\-]\s*$', t))   # the analysis runs on past what was read
        toks = [x.strip('-') for x in toks]
        toks = [x for x in toks if not re.fullmatch(r'[၀-၉.,]+', x)]   # stray numerals
        # debris: a token that begins with a combining mark (ီ, ူ, ့ …) cannot be an element
        toks = [x for x in toks if x not in ('-', '') and not re.match('[\u102B-\u103E]', x)]
        t = ' + '.join(toks) + (' +' if open_end and toks else '')
    else:
        t = re.sub(r'\s*\+\s*', ' + ', t).strip()
    return t, re.sub(r'\s', '', t) != re.sub(r'\s', '', a)


def fields(raw, hw):
    rest = raw
    h = re.sub(r'\s', '', hw)
    # step past the headword as printed (possibly OCR-damaged): consume its length in
    # non-space characters
    m = re.match(r'^\s*([^\s(\[（]+)\s*(?=[(\[（])', rest)
    if m and len(m.group(1)) <= len(h) + 4:
        return fields_after(rest[m.end():], out_hw=m.group(1))
    n = 0; k = 0
    while k < len(rest) and n < len(h):
        if not rest[k].isspace(): n += 1
        k += 1
    return fields_after(rest[k:], out_hw=None)


def fields_after(rest, out_hw):
    out = {'label': None, 'analysis': None, 'headword_ocr': out_hw}
    m = LABEL.match(rest)
    if m: out['label'] = m.group(1).strip(); rest = rest[m.end():]
    m = ANALYSIS.match(rest)
    if m:
        out['analysis'] = re.sub(r'\s+', ' ', m.group(1)).strip(); rest = rest[m.end():]
    else:
        # the closing ] is often read as ျ ု ံ ါ or lost: take the opening [ and the run of
        # tokens that carry a + , and flag it
        m = re.match(r'^\s*\[((?:[^\s\[\]]*\+[^\s\[\]]*|[^\s\[\]]+(?=\s*\+))(?:\s*\+?\s*[^\s\[\]]*\+[^\s\[\]]*)*)', rest)
        if m and '+' in m.group(1):
            out['analysis'] = m.group(1).strip(); out['analysis_bracket_damaged'] = True
            rest = rest[m.end():]
    # tesseract turns the dots and marks between lines into short lines of debris
    # ("ဝ ချူ ဝ ။", "[ ကြု တး ဝ"). A line whose every token is three characters or fewer is
    # dropped from the body; `raw` keeps it.
    keep = [ln for ln in rest.split('\n')
            if ln.strip() and not all(len(t) <= 3 for t in ln.split())]
    out['noise_lines'] = sum(1 for ln in rest.split('\n') if ln.strip()) - len(keep)
    body = re.sub(r'[ \t]+', ' ', '\n'.join(keep)).strip()
    if out.get('analysis'):
        norm, changed = normalise_analysis(out['analysis'])
        if changed:
            out['analysis_ocr'] = out['analysis']
        out['analysis'] = norm
    out['body'] = body
    out['citations'] = [re.sub(r'\s+', '', c) for c in CITE.findall(body)]
    return out


def main(book):
    c = sqlite3.connect(f'file:{ROOT}/db/tipitaka_abidan.db?mode=ro', uri=True)
    start = c.execute('select start_page from books where id=?', (book,)).fetchone()[0]
    idx = {}
    for wid, w, p in c.execute('select id,word,page_number from words where book_id=? order by id', (book,)):
        idx.setdefault(p + start, []).append((wid, nfc(w)))
    pdir = ROOT / f'ocr/{book}/pages'
    pages = {}
    for p in sorted(idx):
        fp = pdir / f'p{p:04d}.json'
        if fp.exists(): pages[p] = json.loads(fp.read_text())

    from aksharamukha import transliterate
    vocab_p = ROOT / 'ocr/osbct_vocab.txt'
    vocab = set(vocab_p.read_text().split('\n')) if vocab_p.exists() else None
    blob = '\n' + '\n'.join(vocab) + '\n' if vocab else ''

    # first pass: locate on every page
    located = {}
    for p, rec in pages.items():
        t = page_text(rec); gold = [w for _, w in idx[p]]
        located[p] = (t,) + locate(t, gold)

    rows = []; order = sorted(pages)
    for pi, p in enumerate(order):
        t, f, offs, pos, how = located[p]
        ents = idx[p]
        found = sorted((pos[i], i) for i in range(len(ents)) if pos[i] is not None)
        nxt_pos = {i: (found[k + 1][0] if k + 1 < len(found) else None) for k, (_, i) in enumerate(found)}
        for i, (wid, hw) in enumerate(ents):
            row = dict(id=wid, book=book, pdf_page=p, index_page=p - start, headword=hw,
                       located=how[i], status='ocr')
            if pos[i] is not None:
                a = offs[pos[i]]
                e = offs[nxt_pos[i]] if nxt_pos[i] is not None else len(t)
                raw = t[a:e]
                if nxt_pos[i] is None and pi + 1 < len(order) and order[pi + 1] == p + 1:
                    t2, f2, offs2, pos2, _ = located[p + 1]
                    first = min([q for q in pos2 if q is not None], default=None)
                    cont = t2[:offs2[first]] if first is not None else ''
                    if cont.strip():
                        raw += '\n' + cont; row['continues_on'] = p + 1
                    if first is None or pos2[0] is None: row['continuation_uncertain'] = True
                row['raw'] = raw.strip()
                row.update(fields(raw, hw))
            base = re.sub('[' + MY_DIGITS + r'\d\s]', '', hw)
            iast = transliterate.process('Burmese', 'IAST', base).replace('ṃ', 'ṁ')
            row['iast'] = iast
            if vocab is not None:
                k = iast.lower()
                row['osbct'] = 'word' if k in vocab else ('inside' if k in blob else 'none')
            rows.append(row)

    out = ROOT / f'ocr/{book}/articles.jsonl'
    out.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))

    n = len(rows); cnt = lambda pred: sum(1 for r in rows if pred(r))
    pct = lambda k: f'{k:,} = {100 * k / n:.1f}%'
    loc = cnt(lambda r: r['located'] != 'unlocated')
    rep = [f'# Vol. {book} — articles', '',
           f'{n:,} index headwords on {len(pages)} OCR\'d indexed pages (of {len(idx)} indexed).', '',
           '| | |', '|---|---:|',
           f'| located verbatim (line start or before ( / [ ) | {pct(cnt(lambda r: r["located"] == "verbatim"))} |',
           f'| located verbatim, inline only | {pct(cnt(lambda r: r["located"] == "verbatim-inline"))} |',
           f'| located by bounded fuzzy match | {pct(cnt(lambda r: r["located"] == "fuzzy"))} |',
           f'| **located, any** | **{pct(loc)}** |',
           f'| unlocated | {pct(n - loc)} |',
           f'| label ( ) recovered | {pct(cnt(lambda r: r.get("label")))} |',
           f'| compound analysis [ ] recovered | {pct(cnt(lambda r: r.get("analysis")))} |',
           f'| of which + signs repaired (normalise_analysis) | {pct(cnt(lambda r: r.get("analysis_ocr")))} |',
           f'| non-empty body | {pct(cnt(lambda r: r.get("body")))} |',
           f'| at least one citation parsed | {pct(cnt(lambda r: r.get("citations")))} |',
           f'| label + body (the article is usable) | {pct(cnt(lambda r: r.get("label") and r.get("body")))} |']
    if vocab is not None:
        rep += ['', '**Romanised headwords against OSBCT** (682,010 canonical words):', '',
                '| | |', '|---|---:|',
                f'| a canonical word | {pct(cnt(lambda r: r["osbct"] == "word"))} |',
                f'| inside a canonical word | {pct(cnt(lambda r: r["osbct"] == "inside"))} |',
                f'| neither | {pct(cnt(lambda r: r["osbct"] == "none"))} |']
    labels = {}
    for r in rows:
        if r.get('label'): labels[r['label']] = labels.get(r['label'], 0) + 1
    rep += ['', 'Labels: ' + ' · '.join(f'({k}) {v:,}' for k, v in sorted(labels.items(), key=lambda x: -x[1])[:15])]
    (ROOT / f'ocr/{book}/articles-report.md').write_text('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    main(sys.argv[1])
