#!/usr/bin/env python3
"""Vol. 14/2 (book 14b) from its text layer: Win-Burmese -> Unicode, no OCR.

    pip install pymupdf python-myanmar
    python3 tools/abhidhana_winburmese.py 14b      # writes ocr/14b/pages/pNNNN.json

14b.pdf is not a scan. It is typeset text in the WinInnwa family of fonts (WinResearcher,
Win---Researcher2, WinHaka, WinPinya, WinKalaw, WinInnwa): one legacy encoding, a Latin-1
keyboard layout drawn with Burmese glyphs, typed in visual order (ေ and ြ before the
consonant, marks in the order they are drawn). python-myanmar's `wininnwa` converter does the
syllable reordering; the corrections below are what this book needs beyond it, each found by
converting the whole book and checking the headwords against the index (ocr/14b/extract-report.md).

The result is written in the shape of an OCR page record: text['col.psm6'] holds the left
column's lines, then the right column's, so abhidhana_articles.py, abhidhana_romanise.py and the
reports run on it unchanged. Records say `source: "text layer"`; nothing in them was OCR'd.
Spans in other fonts are not Burmese: SanskritKavya (Sanskrit quotations, 9,634 characters in
the book) is kept as ⟨…⟩ raw; the Mahar4/Pinny9 ornament between headword and label is dropped.
"""
import json, re, sys, unicodedata
from pathlib import Path
from myanmar import converter, encodings

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

WA, S_DDA, S_DDHA = '', '', ''


def _patch():
    """teach the converter three codes it lacks: ဝ as distinct from the digit ၀ (both are '0'
    in the encoding), and stacked ဍ and ဎ, which the ligatures × ¹ @ are made of"""
    enc = converter.encoders['wininnwa']; d = enc.json_data
    d['consonant']['wa_alt'] = WA
    d['stack']['stack-dda'] = S_DDA; d['stack']['stack-ddha'] = S_DDHA
    enc.table = encodings.build_table(d); enc.reverse_table = encodings.build_table(d, reverse=True)
    pat = '|'.join(encodings.build_pattern(x, d) for x in enc._morphologic_pattern)
    enc.morphologic_pattern = re.compile('(?P<syllable>{})'.format(pat), re.UNICODE)
_patch()

# One glyph code -> the codes the converter knows. Ligatures the converter maps to a key it then
# truncates (dropping a part: kinzi_i_lig -> kinzi) are spelt out; the ligatures of two stacked
# consonants are split, so that a vowel after them can attach.
PRE = [
    ('ð', 'dH'), ('Ø', 'Fd'), ('Ð', 'FD'), ('ø', 'FH'),          # + i / ii / anusvara
    ('û', 'jk'), ('ê', 'Mk'),                                     # ya-yit + u
    ('Ó', 'Úm'),                                                  # ဉ + ာ
    ('Å', 'å'),                                                   # stacked ta, the form under na
    ('É', 'åG'),                                                  # stacked ta + wa-hswe (န္တွ)
    ('|', '#²'), ('¥', '#³'), ('×', '!' + S_DDA), ('¹', '!' + S_DDHA), ('@', 'P' + S_DDA),
    (']]', '“'), ('}}', '”'),
]

# Visual order puts a mark wherever the typist reached it; the converter wants a syllable's marks
# in its own order. Rank the marks and sort each run of them (stable), never across a consonant.
RANK = {}
for chars, r in (('Fú©¾¢öäÆÑ³²Öå¬¦´¨éÜæÁÇ®’' + S_DDA + S_DDHA, 1),     # kinzi, stacked consonants
                 ('sßRQWGTS§Iª', 2),                                       # medials
                 ('dDkKlLH', 3),                                           # upper / lower vowels
                 ('J', 4), ('gm:fUYh', 5), (';', 6)):
    for c in chars: RANK[c] = r


def reorder(s):
    out, run = [], []
    for c in s:
        if c in RANK: run.append(c); continue
        if run: out.extend(sorted(run, key=RANK.get)); run = []
        out.append(c)
    out.extend(sorted(run, key=RANK.get))
    return ''.join(out)


def to_unicode(win):
    s = win
    for a, b in PRE: s = s.replace(a, b)
    s = re.sub(r'(?<![0-9])0(?![0-9])', WA, s)       # ဝ, unless among digits
    s = reorder(s)
    u = converter.convert(s, 'wininnwa', 'unicode')
    u = u.replace('«', '[').replace('»', ']')
    # glyphs of the Win fonts that are punctuation, identified on the page image (pp. 26, 32, 40,
    # 625): ç a comma in Pāḷi quotations (1,370 times), ¿ a question mark, µ an exclamation mark;
    # Þ (font WinInnwa070A) the dash before a quotation or reference
    for a, b in (('ç', ','), ('¿', '?'), ('µ', '!'), ('Þ', '—')): u = u.replace(a, b)
    return unicodedata.normalize('NFC', u)


def page_lines(page):
    """[(column, y, text)]. Spans are kept in the order the PDF draws them (it is the typing
    order, which x order is not: a mark is drawn over or under its consonant). Spans on one
    baseline in one column make a line, in x order. A span of marks alone (ံ or ဲ set as its
    own span, 202 times in the book) is put after the last character to its left."""
    import pymupdf
    raw = page.get_text('rawdict', flags=pymupdf.TEXT_INHIBIT_SPACES | pymupdf.TEXT_PRESERVE_WHITESPACE)
    W = page.rect.width; spans = []
    for b in raw['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                f = sp['font']
                if 'Mahar' in f or 'Pinny' in f or 'ArtHouse' in f or not sp['chars']: continue
                kind = 'win' if f.startswith('Win') else 'other'
                ch = [(c['origin'][0], c['c']) for c in sp['chars']]
                x0, y = sp['chars'][0]['origin']
                spans.append(dict(x=x0, y=y, sz=sp['size'], kind=kind, ch=ch,
                                  col=0 if x0 < W / 2 - 4 else 1,
                                  marks=kind == 'win' and all(c in RANK for _, c in ch)))
    rows = []
    for sp in sorted(spans, key=lambda t: (t['y'], t['x'])):
        for r in rows:
            if r['col'] == sp['col'] and abs(r['y'] - sp['y']) <= .45 * sp['sz']: r['sp'].append(sp); break
        else: rows.append(dict(col=sp['col'], y=sp['y'], sp=[sp]))
    out = []
    for r in rows:
        seq = []                                          # [(x, char, kind)] in drawing order
        for sp in sorted((s for s in r['sp'] if not s['marks']), key=lambda t: t['x']):
            seq += [(x, c, sp['kind']) for x, c in sp['ch']]
        for sp in (s for s in r['sp'] if s['marks']):
            for x, c in sp['ch']:
                k = max((i for i, t in enumerate(seq) if t[0] <= x + .5), default=-1)
                seq.insert(k + 1, (x, c, 'win'))
        txt, cur, kind = '', '', None
        for x, c, k in seq + [(0, '', None)]:
            if k != kind and cur:
                txt += to_unicode(cur) if kind == 'win' else '⟨' + cur + '⟩'; cur = ''
            kind = k; cur += c
        out.append((r['col'], r['y'], txt))
    return sorted(out, key=lambda t: (t[0], t[1]))


def main(book='14b'):
    import pymupdf
    sys.path.insert(0, str(ROOT / 'tools'))
    from abhidhana_ocr import index, score
    idx, start = index(book)
    doc = pymupdf.open(ROOT / f'pdfs/{book}.pdf')
    outdir = ROOT / f'ocr/{book}/pages'; outdir.mkdir(parents=True, exist_ok=True)
    tot = hit = 0
    for i, page in enumerate(doc):
        p = i + 1; lines = page_lines(page)
        cols = ['\n'.join(t for c, y, t in lines if c == k) for k in (0, 1)]
        text = {'col.psm6': cols[0] + '\n' + cols[1], '_gutter': .5}
        gold = idx.get(p, [])
        rec = dict(pdf_page=p, index_page=p - start, dpi=None, source='text layer', indexed=p in idx,
                   **score({'col.psm6': text['col.psm6']}, gold), text=text)
        (outdir / f'p{p:04d}.json').write_text(json.dumps(rec, ensure_ascii=False))
        tot += rec['headwords']; hit += rec['union']
    print(f'{book}: {len(doc)} pages; {hit:,}/{tot:,} index headwords verbatim = {100 * hit / tot:.1f}%')


if __name__ == '__main__':
    main(*sys.argv[1:2])
