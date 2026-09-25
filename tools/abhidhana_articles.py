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
    fuzzy      not verbatim. The headwords left unplaced between two placed neighbours are
               aligned, in order, to the article starts in that span (a line whose head, of
               about the headword's length, is followed by ( or [), each pair >= FUZZY_MIN
               (0.70) similar. A headword hyphenated across a line counts as verbatim.
    unlocated  neither. The article's text then stays inside its predecessor's, and the
               row carries no body.

An article runs from its headword to the next located headword; the last on a page runs on
into the head of the next page (text before that page's first located headword).

Fields are then read off the article's text: the grammatical label in ( ) (normalised to the
printed label, see docs/labels.md), the compound
analysis in [ ], the rest as body, and the citations inside the body (abbreviation, then
Burmese numerals separated by ၊, closed by ။) collected into a list. The body is kept
whole; the citations are not removed from it.

Nothing here is reviewed. Every row carries status "ocr" and the Burmese is raw OCR.
"""
import json, re, sqlite3, sys, unicodedata
from difflib import SequenceMatcher
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from abhidhana_fold import fold

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
    # blank lines, and up to three lines of debris above the head (the page's top rule and
    # specks, read as ပ or ဝ)
    k = 0
    while lines and (not lines[0].strip() or (k < 3 and all(len(t) <= 3 for t in lines[0].split())
                                               and not re.search(r'[(\[]', lines[0]))):
        k += bool(lines[0].strip()); lines.pop(0)
    if lines:
        head = re.sub(r'\s', '', lines[0])
        # a head carrying a spelling variant, အနုပါဒိဏ္ဏ(န္န)ကအာဟာရ, runs longer (vol. 2 p. 115)
        if len(head) <= 24 or (len(head) <= 36 and re.search(r'[(（][^)）]{1,6}[)）]\S', head)
                               and not re.search(r'[\[။]', head)):
            lines.pop(0)
    return '\n'.join(lines)


def page_text(rec):
    t = rec['text'].get('col.psm6', '')
    # abhidhana_ocr.py joins the two columns with one '\n'; tesseract ends each with a form
    # feed, which is where to split.
    parts = t.split('\x0c')
    cols = [p for p in parts if p.strip()]
    return '\n'.join(header_cut(c) for c in cols)


# Scans bound out of order. {book: {pdf page the index implies: pdf page the text is on}}.
# Vol. 2: printed pp. 223 and 224 are PDF pp. 242 and 241 (the running heads say ၂၂၄ on 241),
# so the index's page 223 headwords are on 242 and its 224 headwords on 241.
PAGE_FIX = {'02': {241: 242, 242: 241}}

# Headwords the index files on the wrong page. {book: [(first id, last id, pdf page printed on)]}.
# Each run was found as a page the index gives no headwords (inside the body) whose column text
# begins entries with the unlocated headwords of a neighbouring page, and checked in the text.
#   4c: ids 176418-176427 are indexed at p. 615 and printed on p. 613, which the index skips
#       (brief §16).
#   06: ids 58264-58277 (ဂါဟေတဗ္ဗဂါမ ... ဂါဟေဿာမိ) are indexed at p. 851 and printed on p. 852,
#       which the index skips.
# They keep the index page the index gives them (`index_page`) and are marked `index_misfiled`.
ID_PAGE_FIX = {'4c': [(176418, 176427, 613)], '06': [(58264, 58277, 852)]}

# a homonym's superscript, as OCR reads it: glued debris, or a token of its own
SUP = re.compile(r'^(ာ?ါ|ဝ်|[”"\'’?၁-၉\-–—။]{1,3})?(?:\s+(ာ?ါ|ဝ်|[”"\'’?၁-၉]{1,2})(?=\s|[(\[（]))?(\s*)(\S?)')
FUZZY_MIN = float(__import__('os').environ.get('ABH_FUZZY_MIN', '0.70'))
FUZZY_SPAN = 48


def locate(text, gold):
    """Place each known headword in the page text, in printed order. See the module doc.

    Occurrences after the previous headword are ranked, and the first of the best rank is
    taken:  4 at a line start and followed by ( or [ ;  3 followed by ( or [ ;  2 at a line
    start and followed by a space.  A bare occurrence inside running text (rank 1) is the
    commonest false hit -- the headword quoted in another article, or a longer word that
    begins with it -- so it is tried only after the bounded fuzzy match has failed.
    Headwords of one or two characters (အ, အံ) need rank 3 or better, or a line of their own
    (rank 2: at a line start and followed by a space).

    A homonym's superscript numeral (အ¹, အည³) is read as debris glued to the headword or just
    after it: ါ, ာါ, ဝ်, a quote mark, a digit, a dash or ။ (ဤ”--, ဤ။- at the head of a letter). Debris of that shape between the headword and
    a bracket is passed over at a line start (rank 4); between a short headword and a space,
    too (rank 2). A single ာ is not, as အာ is a word.
    """
    f, offs = flatmap(text)
    line_starts = {0}
    for m in re.finditer('\n', text):
        k = len(re.sub(r'\s', '', text[:m.start() + 1]))
        line_starts.add(k)
    def sup_rank(j, h):
        """rank of h at line start j when a superscript's debris follows it, else 0"""
        o = offs[j]; e = text.find('\n', o); line = text[o:e if e != -1 else len(text)]
        if not line.startswith(h): return 0
        m = SUP.match(line[len(h):])
        if not m or not (m.group(1) or m.group(2)): return 0
        if m.group(4) in ('(', '[', '（'): return 4
        # without a bracket after it, only a short headword: in running text a longer word
        # ends in a real ါ (ဗဒ္ဓါ) or a closing quote as often as in a superscript
        return 2 if len(h) <= 2 and m.group(3) and m.group(4) else 0
    def rank(j, n):
        e = j + n
        nxt = f[e:e + 1]
        spaced = e >= len(f) or offs[e] - offs[e - 1] > 1
        ls = j in line_starts
        if nxt in ('(', '[', '（'): return 4 if ls else 3
        if n <= 2: return 2 if ls and spaced else 0
        if ls and spaced: return 2
        return 1 if spaced else 0
    loose = lambda s: s.replace('ံ', '').replace('့', '')
    pos = [None] * len(gold); how = ['unlocated'] * len(gold); inline = [None] * len(gold)
    twin = [None] * len(gold)
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
    # Article starts: a line start with the ( of the label or the [ of the analysis within
    # FUZZY_SPAN characters. The head is what precedes the bracket, with the hyphen of a
    # headword broken across a line dropped (flatmap has already removed the line break).
    starts = []
    for s0 in sorted(line_starts):
        m = re.search(r'[(\[（]', f[s0:s0 + FUZZY_SPAN])
        if not m or m.start() == 0: continue
        # a line of debris (every token three characters or fewer, no bracket) is not an
        # article start, though the next line's head would otherwise be read through it
        o = offs[s0]; e = text.find('\n', o); line = text[o:e if e != -1 else len(text)]
        if not re.search(r'[(\[（]', line) and all(len(tk) <= 3 for tk in line.split()): continue
        heads = [f[s0:s0 + m.start()]]
        # a ( that never closes before the next bracket is a variant whose ) was lost,
        # "အနုပါဒိဏ္ဏ(န္နဂဂအာဟာရ (၇)": read through it, or the stem alone would match every
        # compound of the stem (vol. 2 p. 115)
        if f[s0 + m.start()] in '(（':
            m2 = re.match(r'[(（]([^()（）\[\]]{1,30}?)(?=[(\[（])', f[s0 + m.start():s0 + FUZZY_SPAN + 30])
            if m2: heads = [heads[0] + m2.group(1)]
        # A spelling variant printed inside the headword, glued to what follows it:
        # အနုပါဒိဏ္ဏ(န္န)က (vol. 2 p. 115) is one printed entry for two index headwords,
        # အနုပါဒိဏ္ဏက and အနုပါဒိန္နက. Read both spellings: without the parenthesis, and with
        # it replacing as many characters before it as it has.
        v = re.match(r'([(（])([^()（）]{1,6})[)）]([^(\[（]*?)(?=[(\[（])', f[s0 + m.start():s0 + FUZZY_SPAN + 12])
        if v and v.group(3) and not normalise_label(v.group(2), '')[0]:
            pre, y, post = heads[0], v.group(2), v.group(3)
            heads = [pre + post, pre[:max(0, len(pre) - len(y))] + y + post]
        heads = tuple(loose(re.sub(r'[-—‐]', '', hd)) for hd in heads)
        # punctuation or a numeral inside the head means running text, not a headword
        # (vol. 1 p. 520: "အတပ္ပနီယံ..ကော တံ (အဂ္ဂိ" had taken the line of အတပ္ပနီယ)
        if heads[0] and not re.search(r'[။၊.,:;"“”‘’၀-၉0-9]', ''.join(heads)): starts.append((s0, heads))
    # Align each run of headwords the verbatim pass left unplaced to the article starts lying
    # between its placed neighbours, in order (a small Needleman-Wunsch: a headword and a
    # start may each be skipped, a pair scores its similarity above FUZZY_MIN). Choosing each
    # headword's best line independently let neighbours take each other's line -- the
    # dictionary's run-on compounds are all alike: vol. 1 p. 140 put အကပ္ပိယရူပကတ on the line
    # of အကပ္ပိယရူပါကုလ and left the latter unlocated.
    i = 0
    while i < len(gold):
        if pos[i] is not None: i += 1; continue
        j = i
        while j < len(gold) and pos[j] is None: j += 1
        lo = pos[i - 1] + 1 if i > 0 else 0
        hi = pos[j] if j < len(gold) else len(f)
        cands = [(s0, hd) for s0, hd in starts if lo <= s0 < hi]
        run = [loose(re.sub(r'\s', '', g)) for g in gold[i:j]]
        if cands:
            # the head must be about the headword's length: a longer run before the bracket is
            # running text (a quotation, a citation), not a damaged headword
            # a head much longer than the headword is running text, not a damaged headword
            score = lambda hd, h: round(SequenceMatcher(None, hd[:len(h) + 2], h).ratio(), 6) \
                if len(hd) <= len(h) + 6 else 0
            sim = [[max(score(hd, h) for hd in hds) for _, hds in cands] for h in run]
            n, m_ = len(run), len(cands)
            D = [[0.0] * (m_ + 1) for _ in range(n + 1)]
            for a_ in range(1, n + 1):
                for b_ in range(1, m_ + 1):
                    pair = sim[a_ - 1][b_ - 1] - FUZZY_MIN
                    D[a_][b_] = max(D[a_ - 1][b_], D[a_][b_ - 1],
                                    D[a_ - 1][b_ - 1] + pair if pair >= 0 else -1)
            a_, b_ = n, m_
            while a_ and b_:
                pair = sim[a_ - 1][b_ - 1] - FUZZY_MIN
                if pair >= 0 and D[a_][b_] == D[a_ - 1][b_ - 1] + pair:
                    k = i + a_ - 1; pos[k] = cands[b_ - 1][0]
                    how[k] = 'verbatim' if sim[a_ - 1][b_ - 1] == 1 and len(cands[b_ - 1][1]) == 1 else 'fuzzy'
                    a_ -= 1; b_ -= 1
                elif D[a_][b_] == D[a_][b_ - 1]: b_ -= 1     # skip a start before a headword
                else: a_ -= 1
        i = j
    # The second spelling of a variant entry shares its article: place it on the start its
    # twin took, when that start carries two spellings and the other one matches it.
    # Strict: the twin itself must not be a twin, a start takes one twin, and the spelling
    # must match >= 0.85 -- the run-on compounds of one stem are otherwise all alike.
    two = {s0: hds for s0, hds in starts if len(hds) == 2}
    taken = set()
    for i, g in enumerate(gold):
        if pos[i] is not None: continue
        h = loose(re.sub(r'\s', '', g))
        for k in (i - 1, i + 1):
            if 0 <= k < len(gold) and pos[k] in two and twin[k] is None and pos[k] not in taken \
                    and max(SequenceMatcher(None, hd, h).ratio() for hd in two[pos[k]]) >= .85:
                pos[i] = pos[k]; how[i] = 'fuzzy'; twin[i] = k; taken.add(pos[k]); break
    # Folded: a headword still unplaced after the fuzzy alignment, looked for again with the
    # spellings print, index and OCR disagree on folded together (tools/abhidhana_fold.py:
    # ါ/ာ, ဉ/ည, ဋ/ဌ/ဠ, ည္ဇ/ည္ဆ/ည္စ, ဏ္ဍ/ဏ္ဏ/ဏ္ဌ). Only between its placed neighbours, rank 2
    # or better. Run before the fuzzy alignment it moved three placements in vol. 5, two of them
    # wrongly (a quotation line; a cross-reference, "ကာသာဝကဏ္ဍ (ခ) ကြည့်"), so it runs after
    # it and moves nothing.
    ff = fold(f)
    for i, g in enumerate(gold):
        if pos[i] is not None: continue
        h = fold(re.sub(r'\s', '', g))
        lo = max([pos[k] + len(re.sub(r'\s', '', gold[k])) for k in range(i) if pos[k] is not None], default=0)
        hi = min([pos[k] for k in range(i + 1, len(gold)) if pos[k] is not None], default=len(f))
        best = (0, None); j = ff.find(h, lo)
        while j != -1 and j + len(h) <= hi:
            r = rank(j, len(h))
            if r > best[0]: best = (r, j)
            if r == 4: break
            j = ff.find(h, j + 1)
        if best[0] >= 2:
            pos[i] = best[1]; how[i] = 'folded'; inline[i] = None
    # A fuzzy placement whose line starts with the headword once folded is as good as verbatim:
    # say so, without moving it.
    for i, g in enumerate(gold):
        if how[i] == 'fuzzy' and twin[i] is None and ff.startswith(fold(re.sub(r'\s', '', g)), pos[i]):
            how[i] = 'folded'
    # Homonyms whose superscript was read as debris (အမူလကာါ (န), အဝ် အာ-ဥပသာရ): a last pass,
    # for headwords still unplaced, inside the span their placed neighbours leave. Tried first
    # in the verbatim pass, it let a homonym's first entry take the second's line when the first
    # line was misread (vol. 3 pp. 334, 384), where the fuzzy alignment had placed both right.
    used = {x for x in pos if x is not None}
    for i, g in enumerate(gold):
        if pos[i] is not None: continue
        h = re.sub(r'\s', '', g)
        lo = max([pos[k] + 1 for k in range(i) if pos[k] is not None], default=0)
        hi = min([pos[k] for k in range(i + 1, len(gold)) if pos[k] is not None], default=len(f))
        for s0 in sorted(line_starts):
            if lo <= s0 < hi and s0 not in used and f.startswith(h, s0) and sup_rank(s0, h):
                pos[i] = s0; how[i] = 'verbatim'; used.add(s0); break
    # Homonyms taken one line late. When a homonym's first entry is misread (its superscript read
    # as a glued ာ, "ကကစာ (ပုန) [", which SUP does not pass, since အာ is a word), the verbatim
    # pass gives the first index row the second entry's line and leaves the second unplaced
    # (vol. 5 p. 63: ကကစ¹ carried ကကစ²'s article; the typed witness showed it, see
    # docs/witness-join.md). For two identical headwords in a row, the first placed and the
    # second not, a line start between the first's placed predecessor and its position that
    # begins with the headword, then at most two characters of superscript debris (ာ ါ, a quote
    # mark, a digit), then ( or [, is the first's
    # entry: the second moves down to the line the first had.
    for i in range(len(gold) - 1):
        if not (pos[i] is not None and pos[i + 1] is None and twin[i] is None
                and re.sub(r'\s', '', gold[i]) == re.sub(r'\s', '', gold[i + 1])): continue
        h = re.sub(r'\s', '', gold[i])
        lo = max([pos[k] + 1 for k in range(i) if pos[k] is not None], default=0)
        for s0 in sorted(line_starts):
            if lo <= s0 < pos[i] and f.startswith(h, s0) and re.match(r'[ာါ”"\'’၁-၉¹²³]{0,2}[(\[（]', f[s0 + len(h):s0 + len(h) + 3]) \
                    and s0 not in used:
                pos[i + 1], how[i + 1] = pos[i], how[i]
                pos[i], how[i] = s0, 'verbatim'; used.add(s0); break
    for i, g in enumerate(gold):
        if pos[i] is not None or inline[i] is None: continue
        lo = max([pos[k] + 1 for k in range(i) if pos[k] is not None], default=0)
        hi = min([pos[k] for k in range(i + 1, len(gold)) if pos[k] is not None], default=len(f))
        if lo <= inline[i] < hi:
            pos[i] = inline[i]; how[i] = 'verbatim-inline'
    locate.twin = twin
    return f, offs, pos, how


LABEL = re.compile(r'^\s*[\(（]\s*([^)）\n]{1,14}?)\s*[\)）]')
# A label with one of its brackets lost, the [ of the analysis following: "(ကြို [" (vol. 4b
# p. 300), "ထီ) [" (p. 74). Taken only when the reading normalises to a label.
LABEL_LOOSE = re.compile(r'^\s*(?:[\(（]\s*([^)）\n\[]{1,14}?)\s*(?=\[)|([^\s()（）\[\]]{1,8})\s*[\)）](?=\s*\[))')

# ---- grammatical labels ---------------------------------------------------------------
# The label is a closed set (docs/spanish-method.md §2, extended by docs/labels.md). OCR
# reads it with a handful of stable confusions; this table maps every reading seen in vol. 1
# (125 distinct) to the printed label. Each mapping was checked against the page image on a
# sample (docs/labels.md gives the ids); a reading that could stand for more than one label
# is resolved by the headword's ending only where that was checked too, and marked
# `label_how: "inferred"`. A reading not in the table is left unnormalised: `label` is then
# None and `label_ocr` keeps what the OCR printed.
LABEL_SET = ('ပု', 'ထီ', 'န', 'တိ', 'ကြိ', 'ကြိ၊ဝိ', 'ကာ၊ကြိ', 'နာမ-ကြိ', 'ဗျ',
             'ပု၊န', 'ပု၊ထီ', 'ပု၊တိ', 'န၊ပု', 'န၊ထီ', 'န၊တိ', 'တိ၊န', 'ပုံ-ဗဟု',
             'စတုတ္ထန္တ', 'တတိယန္တ-ဗျ', 'ကမ္မ၊ကြိ', 'ထီ၊န', 'ထီ၊ပု', 'အ-လိင်', 'ကာ၊ကြိ၊ဝိ')
_LABEL_READINGS = {
    'ပု':      'ပု ပ ၇ ပြ ပူ ပုံ ဖု ြု ၇ု ု ပ၇ ပြု မ ပု၊ ပု။',
    'ထီ':      'ထီ ထိ ထံ ထ တီ သီ ၊ထီ',
    'န':       'န နံ',
    'တိ':      'တိ တ တ် ဘိ',
    'ကြိ':     'ကြိ က ကြ ကြု ကြံ ကြ် ကကြ ကြို ကြီ ကြါ ကြပ် ကြရ ကိ ဤ ၍',
    'ကြိ၊ဝိ':  'ကြိ၊ဝိ ကြ၊ဝိ ကြ်၊ဝိ ကြံ၊ဝိ ကြို၊ဝိ ကြါ၊ဝိ ကြီ၊ဝိ ကဝိ ၉ြိ၊ဝိ ကြိးဝိ ကြိ[ဝိ '
               'ကြု၊ဝိ ကြ၊ဒိ ကိ၊ဝိ ကြိ၊ဒိ ကြိုဝိ ကြိုငိ ကြုဝိ ကြ၊ပိ ကြါဝိ ကြိဝိ ကြ၊ဝ ကြ၊ ကြင် ကြံးဝိ ကြ်းဝိ ကြီးဝိ ကြိ၊ိ ိ၊ဝိ ကြဝိ',
    'ကာ၊ကြိ':  'ကာ၊ကြို ကာ၊ကြ ကာ၊ကြ်',
    'နာမ-ကြိ': 'နာမ-ကြ',
    'ဗျ':      'ဗျ ဗ',
    'ပု၊န':    'ပုန ပု၊န ပန ပု၊နု ပုန၊',
    'ပု၊ထီ':   'ပု၊ထီ ပုထ ပုသ ပု၊ထီ?',
    'ပု၊တိ':   'ပု၊တိ ပတိ',
    'န၊ပု':    'န၊ပု န၊၇',
    'န၊ထီ':    'န၊ထီ န၊ထံ န၊ထိ န၊သီ နု၊သီ န၊တီ',
    'န၊တိ':    'န၊တိ နတိ',
    'တိ၊န':    'တိ၊န',
    'ပုံ-ဗဟု': 'ပုဗဟု ပုံဗဟု ပုံ-ဗဟု ပု-ဗဟု',
    'စတုတ္ထန္တ': 'စတုတ္ထန္တ',
    'တတိယန္တ-ဗျ': 'တတိယန္တ-ဗျ',
    # from vol. 2; each is a label the typed PCED witness prints (docs/labels.md §4)
    'ကမ္မ၊ကြိ': 'ကမ္မ၊ကြိ ကမ္မ၊ကြို ကမ္မ၊ကြ် ကမ္မကြို ကမ္မကြိ ကမ္ပကြိ ကမ္ပ၊ကြိ',   # ကမ္ပ (ကြိ): 4b p. 300
    'ထီ၊န':    'ထီ၊န ထံ၊န',   # ထံ၊န: vol. 4b p. 300, image-checked
    'ထီ၊ပု':   'ထီ၊ပု ထိ၊ပု ထိ၊ပူ',
    'အ-လိင်':  'အ-လိင် အလိင်',   # aliṅga, from vol. 3; the witness prints it 20 times
    # causative absolutive; vol. 6 p. 852 ဂါဟေတွာ, image-checked. Until 25 Sep 2026 it fell to the
    # junk-tail rule below and was cut to (ကာ၊ကြိ): 35 rows in vols. 3-6, all -tvā / -tvāna.
    'ကာ၊ကြိ၊ဝိ': 'ကာ၊ကြိ၊ဝိ ကာ၊ကြ၊ဝိ ကာ၊ကြိံဝိ ကာ၊ကြိဝိ ကာကြိဝိ ကာ၊ကြ၊ဝိ၊ ကာ၊ကြါ၊ဝိ ကာ၊ကြးဝိ',
}
LABEL_MAP = {r: lab for lab, rs in _LABEL_READINGS.items() for r in rs.split()}
# Not mapped, because the image showed them ambiguous: (တံ) is (တိ) on id 455 and (ထီ) on
# ids 7901 and 4572 (atibuddhi, an -i stem), so the ending cannot decide it; (ယီ) is a
# spelling variant printed inside the headword on id 2906, အဇ္ဈာယိ (ယီ) (တိ).
# A verb reading on a -tvā / -tvāna / -tuṁ headword is (ကြိ၊ဝိ) with the ၊ဝိ lost: five of
# five checked (ids 711, 2002, 2710, 3146, 4557), including 711 read as a clean (ကြိ). -ya
# absolutives are NOT inferred: id 5662 adaṇḍiya is printed (ကြိ).
_VI_END = ('tvā', 'tvāna', 'tuṁ')


def label_clean(s):
    """candidate keys for a reading: whole, then cut at a stray [ (the analysis run in)"""
    strip = lambda x: re.sub(r'[\s(\[（?”"။]', '', x)
    s = s.lstrip('[')
    c = [strip(s), strip(s.split('[')[0]), strip(re.split(r'[(（]', s)[0])]
    # a sense number run into the label: (ပု ၂) -> ပု
    return c + [re.sub('[၀-၉]+$', '', x) for x in c if re.search('[^၀-၉][၀-၉]+$', x)]


def normalise_label(reading, iast):
    """(label, how) for an OCR reading of the label. how: exact | mapped | inferred | None"""
    if reading is None: return None, None
    cands = label_clean(reading); s = cands[0]
    lab = next((LABEL_MAP[c] for c in cands if c in LABEL_MAP), None)
    # a junk tail after a valid combination: 'န၊ပုအဂ္ဂ နခါ' -> 'န၊ပု'
    if lab is None:
        for k in sorted(LABEL_MAP, key=len, reverse=True):
            if len(k) >= 3 and s.startswith(k) and '၊' in k: lab = LABEL_MAP[k]; break
    if lab is None: return None, None
    how = 'exact' if reading.strip() == lab else 'mapped'
    if lab == 'ကြိ' and iast.endswith(_VI_END): return 'ကြိ၊ဝိ', 'inferred'
    return lab, how


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


def fields(raw, hw, iast=''):
    rest = raw
    h = re.sub(r'\s', '', hw)
    # step past the headword as printed (possibly OCR-damaged): consume its length in
    # non-space characters
    # A spelling variant can sit inside the printed headword, အကာလုသိ(ဿိ)ယ (န): take it as
    # part of the headword when it is not itself a label and a ( or [ follows.
    m = re.match(r'^\s*([^\s(\[（]+ ?[(（] ?([^()（）\s]{1,6}) ?[)）][^\s(\[（]+)\s*(?=[(\[（])', rest)
    if m and not normalise_label(m.group(2), iast)[0] and len(m.group(1)) <= len(h) + 10:
        out = fields_after(rest[m.end():], out_hw=m.group(1), iast=iast)
        out['headword_variant'] = m.group(2)
        return out
    m = re.match(r'^\s*([^\s(\[（]+)(\s*)(?=[(\[（])', rest)
    if m and len(m.group(1)) <= len(h) + 4:
        return fields_after(rest[m.end():], out_hw=m.group(1), iast=iast, glued=not m.group(2))
    n = 0; k = 0
    while k < len(rest) and n < len(h):
        if not rest[k].isspace(): n += 1
        k += 1
    return fields_after(rest[k:], out_hw=None, iast=iast)


def fields_after(rest, out_hw, iast='', glued=False):
    out = {'label': None, 'label_ocr': None, 'label_how': None, 'analysis': None,
           'headword_ocr': out_hw}
    m = LABEL.match(rest)
    if not m:
        ml = LABEL_LOOSE.match(rest)
        if ml and normalise_label((ml.group(1) or ml.group(2)).strip(), iast)[0]:
            r1 = (ml.group(1) or ml.group(2)).strip(); rest = rest[ml.end():]
            lab, how = normalise_label(r1, iast)
            out['label_ocr'] = r1; out['label'] = lab; out['label_how'] = how
            out['label_bracket_damaged'] = True
    if m:
        r1 = m.group(1).strip(); rest = rest[m.end():]
        lab, how = normalise_label(r1, iast)
        # Two parentheses in a row. The first may be a spelling variant printed inside the
        # headword, glued to it -- အကာလုသိ(ဿိ)ယ (န), အဇ္ဈာရု(ရူ) (တိ) -- or debris,
        # အဋ္ဌိသင်ာတ (ဋ) (တိ). If the second is a label and the first is not (or was glued
        # to the headword), the second is the label.
        m2 = LABEL.match(rest)
        if m2:
            r2 = m2.group(1).strip(); lab2, how2 = normalise_label(r2, iast)
            if lab2 and (lab is None or glued):
                out['headword_variant' if glued else 'label_debris'] = r1
                r1, lab, how = r2, lab2, how2; rest = rest[m2.end():]
        out['label_ocr'] = r1; out['label'] = lab; out['label_how'] = how
    # Debris lines (below) can fall inside a compound analysis that breaks across a line,
    # "[အပရန္တကပ္ပိက+ / တု ပ တ ပ / ဘာဝ ]" (vol. 2 p. 500), and hide its closing ]. Drop them
    # before reading the analysis, but keep a short line that carries the ] or a +.
    lines = rest.split('\n')
    debris = lambda ln: ln.split() and all(len(t) <= 3 for t in ln.split()) and not re.search(r'[\]+]', ln)
    pre_noise = sum(1 for ln in lines if debris(ln))
    rest = '\n'.join(ln for ln in lines if not debris(ln))
    m = ANALYSIS.match(rest)
    if m:
        out['analysis'] = re.sub(r'\s+', ' ', m.group(1)).strip(); rest = rest[m.end():]
    else:
        # the closing ] is often read as ျ ု ံ ါ or lost: take the opening [ and the run of
        # tokens that carry a + , and flag it
        # element (+ element)+, the elements free of brackets and +; the last may keep the
        # character the ] was misread as (ပရိစ္ဆိန္နံ for ပရိစ္ဆိန္န]) -- hence the flag
        m = re.match(r'^\s*\[\s*([^\s\[\]+]+(?:\s*\+\s*[^\s\[\]+]+)+)', rest)
        if m and '+' in m.group(1):
            out['analysis'] = m.group(1).strip(); out['analysis_bracket_damaged'] = True
            rest = rest[m.end():]
    # tesseract turns the dots and marks between lines into short lines of debris
    # ("ဝ ချူ ဝ ။", "[ ကြု တး ဝ"). A line whose every token is three characters or fewer is
    # dropped from the body; `raw` keeps it.
    keep = [ln for ln in rest.split('\n')
            if ln.strip() and not all(len(t) <= 3 for t in ln.split())]
    out['noise_lines'] = pre_noise + sum(1 for ln in rest.split('\n') if ln.strip()) - len(keep)
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
    fix = PAGE_FIX.get(book, {})
    ipage = {}
    misfiled = {}
    for wid, w, p in c.execute('select id,word,page_number from words where book_id=? order by id', (book,)):
        q = fix.get(p + start, p + start)
        for a, b, pq in ID_PAGE_FIX.get(book, []):
            if a <= wid <= b: q = pq; misfiled[wid] = p
        idx.setdefault(q, []).append((wid, nfc(w)))
        if q not in ipage or wid not in misfiled: ipage[q] = p
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
    located = {}; twins = {}
    for p, rec in pages.items():
        t = page_text(rec); gold = [w for _, w in idx[p]]
        located[p] = (t,) + locate(t, gold); twins[p] = locate.twin

    # Reading order. A page's place is the PDF page the index implies for it (PAGE_FIX undone);
    # pages the index does not cover at all lie inside a long article (vol. 1 has 22 such pages
    # between its first and last indexed page, vol. 2 has 24) and are read whole into it.
    inv = {v: k for k, v in fix.items()}
    place = lambda q: inv.get(q, q)
    lo_p, hi_p = min(pages), max(pages)
    seq = sorted((q for q in range(lo_p, hi_p + 2) if (pdir / f'p{q:04d}.json').exists()), key=place)
    nxt_in_seq = {a: b for a, b in zip(seq, seq[1:]) if place(b) == place(a) + 1}
    order = sorted(pages, key=place)

    def continuation(p):
        """text after the last located article of page p, up to the next located headword"""
        parts, via, uncertain = [], [], False
        q = nxt_in_seq.get(p)
        while q is not None:
            if q in located:
                t2, f2, offs2, pos2, _ = located[q]
                first = min([x for x in pos2 if x is not None], default=None)
                cont = t2[:offs2[first]] if first is not None else ''
                if cont.strip(): parts.append(cont); via.append(q)
                if first is None or pos2[0] is None: uncertain = True
                break
            rec = json.loads((pdir / f'p{q:04d}.json').read_text())
            parts.append(page_text(rec)); via.append(q)
            q = nxt_in_seq.get(q)
        return parts, via, uncertain

    rows = []
    for pi, p in enumerate(order):
        t, f, offs, pos, how = located[p]
        ents = idx[p]
        found = sorted((pos[i], i) for i in range(len(ents)) if pos[i] is not None)
        # an article runs to the next located headword at a later position (the two spellings
        # of a variant entry share one position and one article)
        nxt_pos = {i: next((q for q, _ in found[k + 1:] if q > pos[i]), None) for k, (_, i) in enumerate(found)}
        for i, (wid, hw) in enumerate(ents):
            row = dict(id=wid, book=book, pdf_page=p, index_page=ipage[p], headword=hw,
                       located=how[i], status='ocr')
            if twins[p][i] is not None: row['variant_of'] = ents[twins[p][i]][0]
            if wid in misfiled: row['index_page'] = misfiled[wid]; row['index_misfiled'] = True
            base = re.sub('[' + MY_DIGITS + r'\d\s]', '', hw)
            iast = transliterate.process('Burmese', 'IAST', base).replace('ṃ', 'ṁ')
            if pos[i] is not None:
                a = offs[pos[i]]
                e = offs[nxt_pos[i]] if nxt_pos[i] is not None else len(t)
                raw = t[a:e]
                if nxt_pos[i] is None:
                    parts, via, uncertain = continuation(p)
                    if parts:
                        raw += '\n' + '\n'.join(parts); row['continues_on'] = via[0]
                        if len(via) > 1: row['runs_through'] = via
                    if uncertain: row['continuation_uncertain'] = True
                row['raw'] = raw.strip()
                row.update(fields(raw, hw, iast))
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
           f'| located verbatim after folding (tools/abhidhana_fold.py) | {pct(cnt(lambda r: r["located"] == "folded"))} |',
           f'| located verbatim, inline only | {pct(cnt(lambda r: r["located"] == "verbatim-inline"))} |',
           f'| located by bounded fuzzy match | {pct(cnt(lambda r: r["located"] == "fuzzy"))} |',
           f'| **located, any** | **{pct(loc)}** |',
           f'| unlocated | {pct(n - loc)} |',
           f'| label ( ) read | {pct(cnt(lambda r: r.get("label_ocr")))} |',
           f'| label normalised to the closed set (docs/labels.md) | {pct(cnt(lambda r: r.get("label")))} |',
           f'| of which read exactly as printed / mapped / inferred from the ending | '
           f'{cnt(lambda r: r.get("label_how") == "exact"):,} / {cnt(lambda r: r.get("label_how") == "mapped"):,} / '
           f'{cnt(lambda r: r.get("label_how") == "inferred"):,} |',
           f'| label read but left unnormalised | {pct(cnt(lambda r: r.get("label_ocr") and not r.get("label")))} |',
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
    rep += ['', 'Labels, normalised: ' + ' · '.join(f'({k}) {v:,}' for k, v in sorted(labels.items(), key=lambda x: -x[1]))]
    left = {}
    for r in rows:
        if r.get('label_ocr') and not r.get('label'): left[r['label_ocr']] = left.get(r['label_ocr'], 0) + 1
    if left:
        rep += ['', 'Readings left unnormalised: ' + ' · '.join(f'({k}) {v:,}' for k, v in sorted(left.items(), key=lambda x: -x[1]))]
    # Keep what was written by hand: the title and the italic note under it, and everything from
    # the first "## " heading on. Only the tables between them are regenerated. (Until 25 Sep
    # 2026 the whole file was overwritten, and the notes had to be restored from git.)
    rp = ROOT / f'ocr/{book}/articles-report.md'
    if rp.exists():
        old_rep = rp.read_text()
        head = old_rep.split('\n\n')[:2]
        if len(head) == 2 and head[1].startswith('*'): rep[:1] = [head[0], '', head[1]]
        k = old_rep.find('\n## ')
        if k != -1: rep += [old_rep[k:].rstrip('\n')]
    rp.write_text('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    main(sys.argv[1])
