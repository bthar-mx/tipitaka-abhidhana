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

Nothing here is reviewed. Every row carries status "ocr" and the Burmese is raw OCR, except
the fields corrected by hand in docs/corrections.tsv (tools/abhidhana_corrections.py), which
are applied last and marked on the row as `corrected`.
Before them, the compound analysis is taken from the typed PCED witness wherever it has one
(tools/abhidhana_witness_analysis.py, decided 26 Sep 2026); the OCR's reading stays as
`analysis_read`, and the row carries `analysis_source: "pced"`.
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
# Vol. 22: one printed page is missing from the scan just before PDF p. 920. PDF p. 919 holds the
# index's p. 920 list (9 of 9) and only 2 of 11 of its own; from p. 920 to the end each index list
# sits one PDF page early (brief §26-27). The missing page's own headwords are lost with it.
PAGE_FIX = {'02': {241: 242, 242: 241}, '22': {q: q - 1 for q in range(920, 935)}}

# Headwords the index files on the wrong page. {book: [(first id, last id, pdf page printed on)]}.
# Each run was found as a page the index gives no headwords (inside the body) whose column text
# begins entries with the unlocated headwords of a neighbouring page, and checked in the text.
#   4c: ids 176418-176427 are indexed at p. 615 and printed on p. 613, which the index skips
#       (brief §16).
#   06: ids 58264-58277 (ဂါဟေတဗ္ဗဂါမ ... ဂါဟေဿာမိ) are indexed at p. 851 and printed on p. 852,
#       which the index skips.
# They keep the index page the index gives them (`index_page`) and are marked `index_misfiled`.
#   14c, 22, 23, 24: runs found after the batch of 25 Sep 2026 (docs/after-batch-handoff.md;
#       brief §27), each an unindexed page whose entries begin with a neighbour's unlocated headwords.
ID_PAGE_FIX = {'4c': [(176418, 176427, 613)], '06': [(58264, 58277, 852)],
               '14c': [(196222, 196234, 402), (197721, 197732, 565), (198200, 198207, 625),
                       (201263, 201269, 930), (201325, 201334, 936), (201634, 201646, 962),
                       # image-checked 25 Sep 2026 (index-errata.md §1): PDF 605 prints ၅၇၈, 608
                       # ၅၈၁, 621 ၅၉၄, 976 ၉၄၉, each beginning with these runs
                       (198064, 198070, 605), (198090, 198096, 608), (198166, 198168, 621),
                       (201781, 201786, 976)],
               # 10: ဒသ² is printed on PDF 219 (၁၇၁), ဒသ³⁻⁵ on 220 (image, 25 Sep 2026)
               '10': [(81975, 81975, 219)],
               '22': [(178676, 178682, 169), (178835, 178847, 184), (179577, 179585, 253),
                      (185264, 185267, 894)],
               '23': [(187848, 187857, 275), (187871, 187878, 277), (189039, 189048, 390),
                      (189502, 189513, 436), (190351, 190359, 523)],
               '24': [(206034, 206036, 329), (208187, 208194, 542)],
               # 21: the index gives p. 962 for p. 692 (a transposition); PDF p. 720 prints ၆၉၂ with
               # exactly these ten headwords (image, 25 Sep 2026). This, not an offset, is why book
               # 21's index seemed to run 65 pages past its PDF.
               '21': [(170346, 170355, 720)]}

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
# The labels and their OCR readings are one table, docs/labels.md §0, read by
# tools/abhidhana_labels.py and shared with the website (25 Sep 2026; until then LABEL_SET and
# _LABEL_READINGS were written out here, and the table reproduces them exactly).
from abhidhana_labels import LABELS
LABEL_SET = tuple(d['label'] for d in LABELS)
_LABEL_READINGS = {d['label']: ' '.join(d['readings']) for d in LABELS}
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
# A citation: the work's abbreviation, then volume, page (and more numbers), then ။. The
# abbreviation can have up to three parts joined by ၊ -- ဒီ၊ ဋ္ဌ၊ ၂။၃၉၆။ is the Dīgha
# Aṭṭhakathā, vol. 2 p. 396. (Until 25 Sep 2026 only the last part was kept, ဋ္ဌ၊၂။၃၉၆။,
# which lost the work: brief §36.)
_SEG = r'[\u1000-\u1049\u104C-\u109F]{1,8}'
CITE = re.compile(r'(?:' + _SEG + r'\s*၊\s*){0,2}' + _SEG + r'\s*[၊,.]\s*[' + MY_DIGITS + r']+(?:\s*[၊။,.]\s*[' + MY_DIGITS + r']+)*\s*။')

# Burmese marks that Pāḷi written in Burmese script never carries: asat, visarga-tone, dot-below
BURMESE_ONLY = re.compile('[\u103A\u1038\u1037\u104A\u104B]')


def cite_trim(c):
    """drop leading parts of a citation that are Burmese words, not abbreviation: a Pāḷi
    abbreviation never carries asat, visarga or dot below (the one exception, သစ် "new", only
    ever follows a work, never leads)"""
    parts = re.split(r'(\s*၊\s*)', c)
    while len(parts) > 2 and BURMESE_ONLY.search(parts[0]) and not re.search('[' + MY_DIGITS + ']', parts[0]):
        parts = parts[2:]
    return ''.join(parts)


def normalise_analysis(a):
    """Put back the + signs of a compound analysis that OCR lost or misread.

    The analysis is printed as Pāḷi elements joined by +, e.g. [အတိ + အာ + ဝဒ + အ + တိ]. OCR
    reads + as ၂ and often drops it altogether: that article came out "အတိ ၂ အာ ဝဒ အ တိ"
    (vol. 1 p. 300, reported by the editor). Two repairs, and only these:

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


# A token with the shape of a word: a sense marker "(၁)" "(က)", a hyphen, or a Burmese run that
# starts with a consonant or independent vowel. Not a run of ဝ / ၀ (the dots between lines), not
# ရျ (a misread ]), not a mark stacked on ့ or ်, not ၌ ၍ ၎ ၏ at the start, and not a lone
# consonant or vowel other than မ (§50).
HEAD_WORD = re.compile(r'^(?:\([\u1000-\u1049]{1,3}\)|-|[\u1000-\u102A\u103F\u104C-\u104F][\u1000-\u103E\u104F]*-?)$')


def head_words(line):
    t = line.split()
    return (bool(t) and any(x != '-' for x in t)
            and all(HEAD_WORD.match(x) and not re.fullmatch(r'[ဝ၀]+-?', x) and 'ရျ' not in x
                    and not re.search(r'[့်][ျြွှ]', x) and not re.match(r'[\u104C-\u104F]', x)
                    and not (re.fullmatch(r'[\u1000-\u102A]-?', x) and x.rstrip('-') != 'မ') for x in t))


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
        else:
            # the opening [ lost, or read as ] or | (vol. 23 sets it apart, "[ သမ္မဇ္ဇနီ + ဒဏ္ဍ ]",
            # and OCR drops it: brief §33): elements joined by + straight after the label,
            # accepted only when the closing ] follows them
            m = re.match(r'^\s*[\]|]?\s*([^\s\[\]+()]+(?:\s*\+\s*[^\s\[\]+()]+)+(?:\s*။[^\[\]()]{0,60}?)?)\s*\]', rest)
            if m:
                out['analysis'] = re.sub(r'\s+', ' ', m.group(1)).strip()
                out['analysis_bracket_damaged'] = True; out['analysis_open_lost'] = True
                rest = rest[m.end():]
    # tesseract turns the dots and marks between lines into short lines of debris
    # ("ဝ ချူ ဝ ။", "[ ကြု တး ဝ"). A line whose every token is three characters or fewer is
    # dropped from the body; `raw` keeps it.
    # ... except the rest of the line the analysis ends on: text printed after ] on the headword's
    # line is the definition's first word(s), "[ပမတ္တ+ကရဏ+အတ္ထ] မေ့ / လျော့ခြင်း" (14/2), and was
    # lost with the debris. It is kept when the ] was read (after a damaged bracket the rest of the
# line is the analysis's own tail) and every token has the shape of a word (§50).
    first = rest.split('\n')[0] if out.get('analysis') and not out.get('analysis_bracket_damaged') else ''
    keep = [ln for i, ln in enumerate(rest.split('\n'))
            if ln.strip() and (not all(len(t) <= 3 for t in ln.split()) or (i == 0 and head_words(first)))]
    out['noise_lines'] = pre_noise + sum(1 for ln in rest.split('\n') if ln.strip()) - len(keep)
    body = re.sub(r'[ \t]+', ' ', '\n'.join(keep)).strip()
    if first.strip() and head_words(first) and all(len(t) <= 3 for t in first.split()):
        out['body_head_restored'] = re.sub(r'[ \t]+', ' ', first).strip()
    if out.get('analysis'):
        norm, changed = normalise_analysis(out['analysis'])
        if changed:
            out['analysis_ocr'] = out['analysis']
        out['analysis'] = norm
    out['body'] = body
    out['citations'] = [re.sub(r'\s+', '', cite_trim(c)) for c in CITE.findall(body)]
    return out



# ---- run-on articles split out of their neighbour (brief §67, §69; plan step 1.3) ----------------
# In the books drafted from our own text, an article the index places but the pass above could not
# (unlocated), or placed on a stub line, often has its text inside the nearest article with a body,
# before or after it: its headword at a line start of that body, followed by a label or [. That line,
# up to the next such line in the same host or the host's end, becomes the article's text. The rule
# is the measurement of §67 (tmp/split11/measure.py) made a pass, except that a ( ) counts as a label
# when it normalises to one (docs/labels.md §0), not by a count over all books' articles. Only the
# books without PCED (the editor, 28 Sep 2026): in 01-19 the Meaning comes from PCED per headword.
# Each split was checked on the page image (docs/splits-checked.tsv, the editor's decision of 28 Sep):
# a split marked `wrong` there is not made.
SPLIT_BOOKS = {'14b', '14c', '20', '21', '22', '23', '24', '25', '4c'}
SPLIT_CHECKED = ROOT / 'docs/splits-checked.tsv'
HOMONYMS_CHECKED = ROOT / 'docs/homonyms-checked.tsv'


def _homonym_fix():
    """HOMONYM_FIX {book: {id: (verdict, printed, pdf page, line start | 'same_as:<id>')}} from docs/homonyms-checked.tsv
    (brief §85 4(c), §88): every homonym run read on the page image in plan step 1.8, stage 2. A row read as 'right now'
    or 'wrong now' takes the page line that begins with `line` (spaces removed); 'same_as' rows are index rows with no
    printed entry of their own: kept as records, given no text; 'unsure' rows are not in the table. An entry wins over R
    and the PCED pass for its whole run."""
    out = {}
    if HOMONYMS_CHECKED.exists():
        for ln in HOMONYMS_CHECKED.read_text(encoding='utf-8').splitlines()[1:]:
            c = ln.split('\t')
            if len(c) >= 7 and c[0].isdigit() and c[4] in ('right now', 'wrong now', 'same_as') and c[6]:
                out.setdefault(c[1], {})[int(c[0])] = (c[4], c[3], int(c[5]), c[6])
    return out
HOMONYM_FIX = _homonym_fix() if __import__('os').environ.get('ABH_HOMONYM', '1') != '0' else {}
_SP = lambda s: re.sub(r'\s', '', s or '')
_BASE = re.compile(r'[က-ဪ]')
_TRAIL = re.compile(r'(?:ာ?ါ|ဝ်|[”"\'’?၁-၉¹²³⁴⁵⁶⁷⁸⁹\-–—။])+$')
_KINDRANK = {'exact': 3, 'fold': 2, 'fuzzy': 1}


def _split_checked():
    """{id: (verdict, host)} from docs/splits-checked.tsv (id, book, headword, host, verdict, note)"""
    out = {}
    if SPLIT_CHECKED.exists():
        for ln in SPLIT_CHECKED.read_text(encoding='utf-8').splitlines()[1:]:
            c = ln.split('\t')
            if len(c) >= 8 and c[7].startswith('§89'): continue       # farbody_split's own verdicts (brief §89)
            if len(c) >= 5 and c[0].strip().isdigit(): out[int(c[0])] = (c[4].strip(), int(c[3]) if c[3].strip().isdigit() else None)
    return out


def _jlines(text):
    """a body's lines; a line ending in '-' with no ( or [ is read joined to the next (a headword
    broken by the printer). Same length as the lines, index for index."""
    ls = text.split('\n'); out = []
    for k, ln in enumerate(ls):
        if ln.rstrip().endswith('-') and not re.search(r'[(\[]', ln) and k + 1 < len(ls):
            out.append(ln.rstrip()[:-1] + ls[k + 1])
        else: out.append(ln)
    return out, ls


def _head_match(line, h, hf, allhw, iast, lead=False):
    """the line starts with headword h (exact, folded, or an OCR misreading of it), then a label in
    ( ) or a [ : (how, delimiter) or None. lead: an initial ပ read as ၂ ၆ or ) is read back (used only to
    end a split, not to make one)"""
    s = _SP(line)
    m = re.search(r'[(\[（［]', s)
    if not m or m.start() == 0: return None
    pre = _TRAIL.sub('', s[:m.start()])
    if lead and h.startswith('ပ'): pre = re.sub(r'^(?:[၂၆]\)?|\))(?=[\u1000-\u102A])', 'ပ', pre)
    how = 'exact' if pre == h else ('fold' if fold(pre) == hf else None)
    # same length +-1, same last letter, >= 0.8 alike, and not itself a headword of the index (the
    # dictionary's stem families differ by a syllable)
    if (not how and len(h) >= 5 and abs(len(pre) - len(h)) <= 1 and pre[-1:] == h[-1:] and pre not in allhw
            and SequenceMatcher(None, pre, h, autojunk=False).ratio() >= 0.8): how = 'fuzzy'
    if not how: return None
    rest = s[m.start():]
    if rest[0] in '[［': return how, 'bracket'
    m2 = re.match(r'[(（]([^)）]{1,20})[)）]', rest)
    if m2 and normalise_label(m2.group(1), iast)[0]: return how, 'label'
    return None


def split_runons(book, rows, allhw, pages_text):
    """split run-on articles out of their host's body, in place; returns report lines.
    pages_text(p) gives a PDF page's column text (to tell on which page the split line stands)."""
    if book not in SPLIT_BOOKS: return []
    checked = _split_checked()
    rs = sorted(rows, key=lambda r: int(r['id']))
    def stub(r):
        b = r.get('body')
        return not b or (len(_BASE.findall(b)) < 8 and 'ကြည့်' not in b)
    def kind(r):
        if r.get('homonym_fix'): return None                  # decided on the image (§88): never split
        if r['located'] == 'unlocated': return 'unlocated'
        if stub(r): return 'stub'
        if not r.get('label') and not r.get('analysis'): return 'nolabel'   # competes for a line, never split
        return None
    kinds = [kind(r) for r in rs]
    bodyless = lambda j: not rs[j].get('body')
    lines, claims = {}, {}
    for i, r in enumerate(rs):
        if not kinds[i]: continue
        h = _SP(r['headword']); hf = fold(h)
        for side, rng in (('prev', range(i - 1, max(-1, i - 40), -1)), ('next', range(i + 1, min(len(rs), i + 40)))):
            for j in rng:
                if (kinds[j] or rs[j].get('homonym_fix')) and bodyless(j): continue   # walk over bodiless candidates (and
                                                                                     # same_as rows, §88) to the host
                if j not in lines: lines[j] = _jlines(rs[j].get('body') or '')
                for k, ln in enumerate(lines[j][0]):
                    hm = _head_match(ln, h, hf, allhw, r.get('iast', ''))
                    if hm:
                        claims.setdefault((j, k), []).append((_KINDRANK[hm[0]] * 10 + (side == 'prev'), i, side, hm)); break
                break                                          # the nearest article with a body, each side
    won = {}
    for (j, k), cs in claims.items():                          # one line, one article: exact > fold > fuzzy, prev first
        cs.sort(key=lambda c: -c[0])
        for sc, i, side, hm in cs:
            if i not in won or won[i][0] < sc: won[i] = (sc, j, k, side, hm); break
    # Homonyms (¹ ²): both lines begin with the same headword, and the first took the first line. A
    # candidate with no line of its own, whose previous row has the same headword and was given a
    # line, takes the next line of that host that begins with the headword (brief §69; else the first
    # homonym's text ran on over the second's).
    taken = {(j, k) for sc, j, k, side, hm in won.values()}
    for i in range(1, len(rs)):
        if i in won or kinds[i] not in ('unlocated', 'stub') or (i - 1) not in won: continue
        h = _SP(rs[i]['headword'])
        if h != _SP(rs[i - 1]['headword']): continue
        sc, j, k, side, hm = won[i - 1]
        for k2 in range(k + 1, len(lines[j][0])):
            hm2 = _head_match(lines[j][0][k2], h, fold(h), allhw, rs[i].get('iast', ''))
            if hm2 and (j, k2) not in taken:
                won[i] = (sc, j, k2, side, (hm2[0], hm2[1] + '+homonym')); taken.add((j, k2)); break
    splits = {i: w for i, w in won.items() if kinds[i] in ('unlocated', 'stub')}
    dropped = [i for i in splits if checked.get(int(rs[i]['id']), ('',))[0] == 'wrong']
    for i in dropped: del splits[i]
    # With the homonym rule on (§86), R gives some rows a line and changes some bodies, and the split test then finds
    # splits §69 never saw. Every split is checked on the image before it is made (the editor, 28 Sep): one not in
    # docs/splits-checked.tsv with the same host is reported, not made.
    unchecked = []
    if HOMONYM:
        # §88: a split R's changes exposed is made only when the image said right (the editor, 30 Sep)
        s88 = set()
        if SPLIT_CHECKED.exists():
            for ln in SPLIT_CHECKED.read_text(encoding='utf-8').splitlines()[1:]:
                c = ln.split('\t')
                if len(c) >= 8 and c[0].strip().isdigit() and c[4].strip() != 'right' and c[7].startswith('§88'): s88.add(int(c[0]))
        for i in [i for i in splits if int(rs[i]['id']) in s88]: del splits[i]
        unchecked = [i for i in splits if checked.get(int(rs[i]['id']), (None, None))[1] != int(rs[splits[i][1]]['id'])
                     and not (checked.get(int(rs[i]['id']), ('',))[0] == 'right' and rs[splits[i][1]].get('homonym_fix'))]
        for i in unchecked: del splits[i]
    byhost = {}
    for i, (sc, j, k, side, hm) in splits.items(): byhost.setdefault(j, []).append((k, i, side, hm))
    for j, xs in sorted(byhost.items()):
        host = rs[j]; jl, ls = lines[j]; ks = sorted(k for k, *_ in xs)
        # a line of the host's body that begins with the host's own headword (+ label or [) is the host's
        # own entry, the host having been placed on a line above it: a split ends there, and the host
        # keeps it (a split from the article after it otherwise took that article too)
        # Likewise a line that begins with any other headword of the neighbourhood (+ label or [): another
        # entry, which the split must not take with it; it stays in the host as before.
        near = {(_SP(rs[q]['headword']), rs[q].get('iast', '')) for q in range(max(0, j - 40), min(len(rs), j + 40))}
        near -= {(_SP(rs[i]['headword']), rs[i].get('iast', '')) for _, i, _, _ in xs}
        near.add((_SP(host['headword']), host.get('iast', '')))
        stops = [q for q in range(1, len(jl)) if q not in ks
                 and any(_head_match(jl[q], hh, fold(hh), allhw, ia, lead=True) for hh, ia in near)]
        ends = sorted(set(ks) | set(stops))
        old_body = host['body']; covered = set()
        for k, i, side, hm in xs:
            nxt = next((q for q in ends if q > k), len(ls))
            covered.update(range(k, nxt))
            joined = jl[k] != ls[k]
            seg = [jl[k]] + ls[k + (2 if joined else 1):nxt] if not (joined and k + 1 >= nxt) else [jl[k]]
            text = '\n'.join(seg)
            r = rs[i]
            before = {f: r.get(f) for f in ('located', 'pdf_page', 'raw', 'label', 'body') if r.get(f) is not None}
            for f in ('label', 'label_ocr', 'label_how', 'analysis', 'headword_ocr', 'analysis_ocr', 'analysis_bracket_damaged',
                      'analysis_open_lost', 'label_bracket_damaged', 'label_debris', 'headword_variant', 'noise_lines',
                      'body_head_restored', 'body', 'citations', 'raw', 'continues_on', 'runs_through', 'continuation_uncertain'):
                r.pop(f, None)
            r.update(fields(text, r['headword'], r.get('iast', '')))
            r['raw'] = text
            # the page the split line stands on: the host's page or one its text runs on into
            head = _SP(jl[k])[:24]
            for q in [host['pdf_page']] + ([host['continues_on']] if host.get('continues_on') else []) + host.get('runs_through', [])[1:]:
                if head and head in _SP('\n'.join(_jlines(pages_text(q))[0])): r['pdf_page'] = q; break
            else: r['pdf_page'] = host['pdf_page']
            r['located'] = 'split'
            r['split_from'] = host['id']
            r['split_rule'] = f'run-on:{hm[0]}:{hm[1]}:{side}'
            if before: r['split_replaced'] = before
            v = checked.get(int(r['id']))
            if v: r['split_checked'] = v[0]
        host['body'] = re.sub(r'[ \t]+', ' ', '\n'.join(ln for q, ln in enumerate(ls) if q not in covered)).strip()
        if any(q > ks[0] and q not in covered for q in range(len(ls))): host['split_own_line'] = True
        host['citations'] = [re.sub(r'\s+', '', cite_trim(c)) for c in CITE.findall(host['body'])]
        host['split_to'] = sorted(rs[i]['id'] for _, i, _, _ in xs)
        host['body_before_split'] = old_body
    n = len(splits)
    return [f'run-on articles split out of a neighbour (§67 rule): {n} '
            f'(unlocated {sum(kinds[i] == "unlocated" for i in splits)}, stub {sum(kinds[i] == "stub" for i in splits)}; '
            f'hosts {len(byhost)}; left out as wrong on the image {len(dropped)})'] + \
        ([f'split candidates not in docs/splits-checked.tsv with this host, not made: {len(unchecked)}: '
          + ' '.join(f'{rs[i]["id"]}<{rs[won[i][1]]["id"]}' for i in sorted(unchecked))] if unchecked else [])


# ---- farther-body run-ons (brief §89; plan step 1.8) ----
# An unlocated headword, not in a homonym run, whose entry line (the headword at a line start, then a label or [, as
# _head_match) lies inside the body of an article placed on its page (or the page before or after, as the measurement)
# further back than split_runons' host: the rows between
# were placed out of order, and that article's span swallowed the entry. The line, up to the next split line in the host,
# or a line that begins a headword of the neighbourhood (+ label or [), or the host's end, becomes the row's text (§69).
# The chain: when the text ends at the host's end and the article that follows it in the page text is a row between host
# and candidate (id order), placed on a line that is not its own entry, the entry runs on into that row's text: the row's
# whole text goes to the candidate, and the row takes its own entry line inside the host (before the candidate's line)
# when one is there, else it becomes unlocated, flagged `farbody_unlocated` (the editor, 30 Sep: not left showing another
# headword's text). All 29 books (the editor, 30 Sep): in 01-19 PCED gates each split and each moved row (a text PCED
# contradicts is not made); in the nine books without PCED only what the page image said right is made (rows of
# docs/splits-checked.tsv whose note begins "§89"). Rows the homonym image table placed (homonym_fix) are left alone:
# never a candidate, a host or a chained row. ABH_FARBODY=0 turns it off; ABH_FARBODY_TRACE=<dir> writes every proposal.
FARBODY = __import__('os').environ.get('ABH_FARBODY', '1') != '0'
FARBODY_WINDOW = 20          # a host within 20 ids before the candidate (the measurement: 494 of 495 were 2-17 before)
_TEXT_FIELDS = ('label', 'label_ocr', 'label_how', 'analysis', 'headword_ocr', 'analysis_ocr', 'analysis_bracket_damaged',
                'analysis_open_lost', 'label_bracket_damaged', 'label_debris', 'headword_variant', 'noise_lines',
                'body_head_restored', 'body', 'citations', 'raw', 'continues_on', 'runs_through', 'continuation_uncertain')


def _farbody_checked():
    """{id: (verdict, host, rule)} from the rows of docs/splits-checked.tsv whose note begins '§89'"""
    out = {}
    if SPLIT_CHECKED.exists():
        for ln in SPLIT_CHECKED.read_text(encoding='utf-8').splitlines()[1:]:
            c = ln.split('\t')
            if len(c) >= 8 and c[0].strip().isdigit() and c[7].startswith('§89'):
                out[int(c[0])] = (c[4].strip(), int(c[3]) if c[3].strip().isdigit() else None, c[6].strip())
    return out


def _pced_cont(text, w):
    """containment: the share of PCED's analysis + definition (spaces out, first 600 characters) found in order in the
    first 2x that length + 60 characters of the text (the measure of the 30 Sep measurement, tmp/farbody18/cont.py)"""
    t = _SP((w.get('analysis') or '') + (w.get('definition') or ''))[:600]
    if not t: return None
    ob = _SP(text)[:2 * len(t) + 60]
    if not ob: return 0.0
    return round(sum(b.size for b in SequenceMatcher(None, ob, t, autojunk=False).get_matching_blocks()) / len(t), 3)


def _farbody_pced(book):
    """a gate(text, id, other ids) for the PCED books: ('right' | 'contradicted' | 'none', own, (best other, seq)).
    Contradicted: the text holds under 0.4 of the row's own PCED entry, or another entry (the host's, the chained row's,
    another of the headword's) scores >= 0.6 and >= 0.2 above its own (§86's margin, on containment)."""
    jf = ROOT / f'witness/join-{book}.jsonl'
    J = {}
    if jf.exists():
        for line in jf.open(encoding='utf-8'):
            j = json.loads(line)
            if j.get('seq') is not None: J[j['id']] = j['seq']
    E, ex, fo = _pced()
    def gate(text, rid, hw, others, nbrs=()):
        s = J.get(rid)
        if s is None or s not in E: return 'none', None, None, None
        o = _pced_cont(text, E[s])
        if o is None: return 'none', None, None, None
        h = _SP(hw)
        seqs = ({J.get(x) for x in others} | set(ex.get(h) or fo.get(fold(h)) or [])) - {s, None}
        alts = [(v, q) for q in seqs if q in E for v in [_pced_cont(text, E[q])] if v is not None]
        a = max(alts) if alts else None
        if o < .4: return 'contradicted', o, a, 'own < 0.4'
        if a and a[0] >= .6 and a[0] - o >= .2: return 'contradicted', o, a, 'another entry'
        # the end (brief §89): the text's tail, past what its own entry would fill (1.3x its PCED length + 40), holds another
        # neighbour's PCED entry (>= 0.8 contained): the text ran on into the next article. Located rows with label + body
        # score so in 2.8% (1,651 rows, seed 11), the proposed splits in 11.3%.
        own = _SP((E[s].get('analysis') or '') + (E[s].get('definition') or ''))
        tail = _SP(text)[int(len(own) * 1.3) + 40:]
        if len(tail) >= 20:
            for x in nbrs:
                q = J.get(x)
                if q in E and q != s:
                    c = _pced_cont(tail, E[q])
                    if c is not None and c >= .8: return 'contradicted', o, (c, q), f'end: holds {x}'
        return 'right', o, a, None
    return gate


def farbody_split(book, rows, allhw, pages_text):
    """split farther-body run-ons out of their host, in place (brief §89). Returns (report lines, proposals)."""
    if not FARBODY: return [], []
    from abhidhana_witness_analysis import PCED_BOOKS
    pced = book in PCED_BOOKS
    gate = _farbody_pced(book) if pced else None
    checked = {} if pced else _farbody_checked()
    rs = sorted(rows, key=lambda r: int(r['id'])); n = len(rs)
    H = [_SP(r['headword']) for r in rs]; ids = [int(r['id']) for r in rs]
    L = {}
    def lines(j):
        if j not in L: L[j] = _jlines(rs[j].get('body') or '')
        return L[j]
    def inrun(i):
        return ((i > 0 and H[i - 1] == H[i] and ids[i - 1] == ids[i] - 1)
                or (i + 1 < n and H[i + 1] == H[i] and ids[i + 1] == ids[i] + 1))
    def hm_line(ln, q, lead=False):
        return _head_match(ln, H[q], fold(H[q]), allhw, rs[q].get('iast', ''), lead)
    def own_entry(ln, q):      # R's wider test (strict, weak or sup): a row's own entry line, for the chain
        return entry_tier(ln, H[q], fold(H[q]), allhw, rs[q].get('iast', ''))
    st = {k: 0 for k in ('nearest', 'farther', 'run', 'host_fixed', 'lost', 'taken')}
    claims = {}
    for i, r in enumerate(rs):
        if r['located'] != 'unlocated' or r.get('homonym_fix') or r.get('split_from'): continue
        # the nearest article with a body, each side (walking over bodiless rows): split_runons' domain (§67 / §69)
        near = False
        for rng in (range(i - 1, max(-1, i - 40), -1), range(i + 1, min(n, i + 40))):
            for j in rng:
                if not rs[j].get('body'): continue
                near = near or any(hm_line(ln, i) for ln in lines(j)[0])
                break
        if near: st['nearest'] += 1; continue
        best = None
        for j in range(i - 2, max(-1, i - FARBODY_WINDOW - 1), -1):
            if rs[j].get('pdf_page') not in (r['pdf_page'] - 1, r['pdf_page'], r['pdf_page'] + 1) or not rs[j].get('body'): continue
            for k, ln in enumerate(lines(j)[0]):         # the host's best line: exact > fold > fuzzy, the first of a rank
                hm = hm_line(ln, i)
                if hm:
                    sc = (_KINDRANK[hm[0]], -(i - j))
                    if best is None or sc > best[0]: best = (sc, j, k, hm)
        if not best: continue
        st['farther'] += 1
        if inrun(i): st['run'] += 1; continue
        if rs[best[1]].get('homonym_fix'): st['host_fixed'] += 1; continue
        claims.setdefault((best[1], best[2]), []).append((best[0], i, best[3]))
    won = {}
    for (j, k), cs in claims.items():                  # one line, one article: exact > fold > fuzzy, then the nearest host
        cs.sort(key=lambda c: c[0], reverse=True)
        won[cs[0][1]] = (j, k, cs[0][2]); st['lost'] += len(cs) - 1
    st['taken'] = len(won)
    # the proposals: each split's text, and the chain
    byhost = {}
    for i, (j, k, hm) in won.items(): byhost.setdefault(j, []).append((k, i, hm))
    props = []; chained = set()
    def page_of(host, line):
        head = _SP(line)[:24]
        for q in [host['pdf_page']] + ([host['continues_on']] if host.get('continues_on') else []) + host.get('runs_through', [])[1:]:
            if head and head in _SP('\n'.join(_jlines(pages_text(q))[0])): return q
        return host['pdf_page']
    for j, xs in sorted(byhost.items()):
        host = rs[j]; jl, ls = lines(j); ks = sorted(k for k, _, _ in xs)
        nearhw = set()
        for _, i, _ in xs:
            nearhw |= {q for q in list(range(max(0, i - 40), min(n, i + 41))) + list(range(max(0, j - 40), min(n, j + 41)))}
        nearhw -= {i for _, i, _ in xs}
        nearq = {}
        for q in nearhw: nearq.setdefault((H[q], rs[q].get('iast', '')), q)
        def is_stop(ln):
            return any(_head_match(ln, hh, fold(hh), allhw, ia, lead=True) for hh, ia in nearq)
        stops = [q for q in range(1, len(jl)) if q not in ks and is_stop(jl[q])]
        # the chain, for a split that ends at the host's end
        chains = {}
        for k, i, hm in xs:
            ends = sorted(set(ks) | set(stops))
            if next((q for q in ends if q > k), None) is not None: continue
            p = host['pdf_page']; t = _SP(pages_text(p) + '\n' + pages_text(p + 1))
            tail = _SP(host.get('raw'))[-80:]; ph = t.find(tail) if tail else -1
            if ph < 0: chains[i] = ('host not found in the page text', None); continue
            pe = ph + len(tail); nxt = None
            for m in range(j + 1, i):
                rm = rs[m]
                if rm['located'] == 'unlocated' or not rm.get('raw'): continue
                q = t.find(_SP(rm['raw'])[:60], max(0, pe - 5))
                if q >= 0 and (nxt is None or q < nxt[0]): nxt = (q, m)
            if not nxt or nxt[0] - pe > 3: chains[i] = ('next article not a row between', None); continue
            m = nxt[1]; rm = rs[m]
            if rm.get('homonym_fix'): chains[i] = ('next row placed by the image table', None); continue
            if m in byhost or m in chained: chains[i] = ('next row is itself a host or chained', None); continue
            if own_entry(rm['raw'].split('\n')[0], m): chains[i] = ('next row on its own entry', None); continue
            near2 = {(H[q], rs[q].get('iast', '')) for q in range(max(0, i - 40), min(n, i + 41)) if q != i}
            mjl = _jlines(rm['raw'])[0]
            end = next((q for q in range(len(mjl)) if any(_head_match(mjl[q], hh, fold(hh), allhw, ia, lead=True)
                                                           for hh, ia in near2)), len(mjl))
            if end == 0: chains[i] = ('next row begins a neighbour\'s entry', None); continue
            if end < len(mjl): chains[i] = ('the entry ends inside the next row (not chained)', None); continue
            k2 = next((q for q in range(0, k) if q not in ks and own_entry(jl[q], m)), None)
            chains[i] = ('chain', (m, k2)); chained.add(m)
        starts = set(ks) | {c[1][1] for c in chains.values() if c[1] and c[1][1] is not None}
        ends = sorted(starts | set(stops))
        def seg(k):
            nxt = next((q for q in ends if q > k), len(ls))
            joined = jl[k] != ls[k]
            s = [jl[k]] + ls[k + (2 if joined else 1):nxt] if not (joined and k + 1 >= nxt) else [jl[k]]
            return s, nxt
        for k, i, hm in sorted(xs):
            s, nxt = seg(k)
            c = chains.get(i)
            pr = dict(id=rs[i]['id'], i=i, hw=rs[i]['headword'], host=host['id'], j=j, k=k, nxt=nxt, how=hm[0], delim=hm[1],
                      dist=i - j, text='\n'.join(s), page=page_of(host, jl[k]), host_page=host['pdf_page'],
                      end='split' if nxt in starts else ('neighbour head' if nxt < len(ls) else 'host end'),
                      next_line=ls[nxt] if nxt < len(ls) else None, chain_note=c[0] if c else None, chain=None, mid=None)
            pr['rule'] = f'farbody:{hm[0]}:{hm[1]}:{i - j}'
            if c and c[1]:
                m, k2 = c[1]; rm = rs[m]
                pr['chain'] = dict(id=rm['id'], m=m, hw=rm['headword'], raw=rm['raw'], page=rm['pdf_page'],
                                   located=rm['located'], k2=k2)
                pr['rule'] += '+chain'
                if k2 is not None:
                    ms, mn = seg(k2)
                    pr['mid'] = dict(id=rm['id'], m=m, hw=rm['headword'], k=k2, nxt=mn, text='\n'.join(ms),
                                     page=page_of(host, jl[k2]), rule=f'farbody-chain:own-line:{own_entry(jl[k2], m)[0]}',
                                     next_line=ls[mn] if mn < len(ls) else None)
            props.append(pr)
    # the gate: PCED (01-19) or the page image (the nine books)
    made = []
    for pr in props:
        i = pr['i']; ch = pr['chain']
        full = pr['text'] + ('\n' + ch['raw'] if ch else '')
        pr['decision'] = None
        if pced:
            nb_i = [rs[q]['id'] for q in range(max(0, i - 8), min(n, i + 9)) if q not in (i, pr['j'])]
            g = gate(full, pr['id'], pr['hw'], [pr['host']] + ([ch['id']] if ch else []), nb_i)
            pr['pced'] = g
            if ch:
                gm = gate(ch['raw'], ch['id'], ch['hw'], [pr['id'], pr['host']])
                pr['pced_mid_now'] = gm
                # the chained row's present text is its own by PCED (>= 0.6 and >= 0.2 above the candidate's entry, §86's
                # "right"): the chain would take it away, so it is not made
                owns = gm[1] is not None and gm[1] >= .6 and (not gm[2] or gm[1] - gm[2][0] >= .2)
                if g[0] == 'contradicted' or owns:
                    g0 = gate(pr['text'], pr['id'], pr['hw'], [pr['host']], nb_i)
                    pr['pced_plain'] = g0
                    pr['chain_dropped'] = 'PCED'
                    ch = None; g = g0
            if g[0] == 'contradicted': pr['decision'] = 'not made (PCED)'; continue
            pr['decision'] = 'made' if g[0] == 'right' else 'made (no PCED entry)'
            if ch and pr['mid']:
                mm = pr['mid']['m']
                gm2 = gate(pr['mid']['text'], ch['id'], ch['hw'], [pr['id'], pr['host']],
                           [rs[q]['id'] for q in range(max(0, mm - 8), min(n, mm + 9)) if q not in (mm, pr['j'])])
                pr['pced_mid'] = gm2
                pr['mid_decision'] = 'unlocated (PCED)' if gm2[0] == 'contradicted' else 'own line'
            elif ch: pr['mid_decision'] = 'unlocated (own line not found)'
        else:
            v = checked.get(int(pr['id']))
            if not v or v[1] != int(pr['host']) or v[2] != pr['rule']:
                pr['decision'] = 'not made (not checked on the image)' if not v else f'not made (image: {v[0]}; checked {v[2]} < {v[1]})'
                if v and v[0] == 'right': pr['decision'] = f'not made (checked another proposal: {v[2]} < {v[1]})'
                continue
            if v[0] != 'right': pr['decision'] = f'not made (image: {v[0]})'; continue
            pr['decision'] = 'made (image)'
            if ch and pr['mid']:
                vm = checked.get(int(ch['id']))
                ok = vm and vm[0] == 'right' and vm[1] == int(pr['host']) and vm[2] == pr['mid']['rule']
                pr['mid_decision'] = 'own line' if ok else f'unlocated (image: {vm[0] if vm else "not checked"})'
            elif ch: pr['mid_decision'] = 'unlocated (own line not found)'
        made.append((pr, ch))
    # apply
    covered = {}
    for pr, ch in made:
        i, j = pr['i'], pr['j']; r = rs[i]; host = rs[j]
        covered.setdefault(j, set()).update(range(pr['k'], pr['nxt']))
        text = pr['text'] + ('\n' + ch['raw'] if ch else '')
        before = {f: r.get(f) for f in ('located', 'pdf_page', 'raw', 'label', 'body') if r.get(f) is not None}
        for f in _TEXT_FIELDS: r.pop(f, None)
        r.update(fields(text, r['headword'], r.get('iast', '')))
        r['raw'] = text; r['pdf_page'] = pr['page']; r['located'] = 'split'
        r['split_from'] = host['id']; r['split_rule'] = pr['rule'] if ch else pr['rule'].replace('+chain', '')
        if ch: r['farbody_chain'] = ch['id']
        if before: r['split_replaced'] = before
        if pced: r['split_checked'] = 'pced:' + ('right' if (pr.get('pced_plain') or pr['pced'])[0] == 'right' else 'none')
        else: r['split_checked'] = 'right'
        if ch:
            m = ch['m']; rm = rs[m]
            fb = {'located': rm['located'], 'pdf_page': rm['pdf_page'], 'raw': rm['raw'].split('\n')[0]}
            for f in _TEXT_FIELDS: rm.pop(f, None)
            rm['farbody_before'] = fb; rm['farbody_text_to'] = r['id']
            if pr.get('mid_decision') == 'own line':
                md = pr['mid']
                covered[j].update(range(md['k'], md['nxt']))
                rm.update(fields(md['text'], rm['headword'], rm.get('iast', '')))
                rm['raw'] = md['text']; rm['pdf_page'] = md['page']; rm['located'] = 'split'
                rm['split_from'] = host['id']; rm['split_rule'] = md['rule']
                rm['split_checked'] = ('pced:' + ('right' if pr['pced_mid'][0] == 'right' else 'none')) if pced else 'right'
            else:
                rm['located'] = 'unlocated'; rm['farbody_unlocated'] = True
    for j, cov in covered.items():
        host = rs[j]; jl, ls = lines(j)
        old = host['body']
        host['body'] = re.sub(r'[ \t]+', ' ', '\n'.join(ln for q, ln in enumerate(ls) if q not in cov)).strip()
        host['citations'] = [re.sub(r'\s+', '', cite_trim(c)) for c in CITE.findall(host['body'])]
        host['split_to'] = sorted(set(host.get('split_to', [])) | {pr['id'] for pr, _ in made if pr['j'] == j}
                                  | {ch['id'] for pr, ch in made if pr['j'] == j and ch and pr.get('mid_decision') == 'own line'})
        host.setdefault('body_before_split', old)
    nm = len(made); nch = sum(1 for _, ch in made if ch)
    own = sum(1 for pr, ch in made if ch and pr.get('mid_decision') == 'own line')
    _nm = __import__('collections').Counter(pr['decision'] for pr in props if not pr['decision'].startswith('made'))
    rep = [f'farther-body run-ons (§89): {st["farther"]} unlocated headwords at a line start + label in a farther body '
           f'(in a homonym run {st["run"]}, host placed by the image table {st["host_fixed"]}, lost the line {st["lost"]}); '
           f'{st["taken"]} proposed, {nm} made (chained {nch}: {own} rows moved to their own line, {nch - own} left unlocated); '
           f'hosts {len(covered)}; not made {len(props) - nm}'
           + (' (' + ', '.join(f'{k} {v}' for k, v in sorted(_nm.items())) + ')' if _nm else '')]
    tp = __import__('os').environ.get('ABH_FARBODY_TRACE')
    if tp:
        with open(f'{tp}/farbody-{book}.jsonl', 'w', encoding='utf-8') as tf:
            tf.write(json.dumps(dict(stats=st), ensure_ascii=False) + '\n')
            for pr in props: tf.write(json.dumps(pr, ensure_ascii=False, default=str) + '\n')
    return rep, props

# ---- homonyms placed on each other's line: the order rule R and the PCED pass (brief §85, §86; plan step 1.8) ----
# A run is a maximal sequence of consecutive index ids with one headword (spaces removed). The index is ground truth
# for how many entries the run has and in what order they are printed; where OCR misread a head line (a superscript ¹
# read as ံ or ာ, a ( lost, a label not recognised), a row took its sibling's line and the rows after it shifted by one.
# R: the lines of the run's pages that begin an entry of the headword, in reading order, between the run's placed
# neighbours (the page before the run's first row, the one after its last; a run that ends its page also reaches the
# head of the next page, the text that is otherwise its last article's continuation). If there are exactly n such lines
# for n rows, row i takes line i; otherwise the run is left as it is. An entry line: §67's test (_head_match: the
# headword exact, folded or an OCR misreading, then a label or [) -- "strict"; or the headword exact or folded, then a
# ( or [ whose first characters hold no digit and no ။ (not a citation) -- "weak"; or the same with a superscript ¹
# read as a final ံ or ာ, taken as the headword when that form is not itself an index headword -- "sup".
# In the PCED books (01-19) PCED gates R (a run in which PCED puts a moved row's new text on another entry of the
# headword is left as it was) and completes it (pced_homonyms, below). ABH_HOMONYM=0 turns both off.
HOMONYM = __import__('os').environ.get('ABH_HOMONYM', '1') != '0'
_HOMONYM_KEEP = ('id', 'book', 'index_page', 'index_misfiled', 'headword', 'iast', 'osbct', 'status')


def page_lines(t, f, offs):
    """[(flat offset, line, joined line)] for the non-empty lines of a page's text: a line ending in '-' with no ( or [
    is read joined to the next (a headword broken by the printer), as _jlines"""
    raw = []; o = 0
    for ln in t.split('\n'):
        if ln.strip(): raw.append((len(re.sub(r'\s', '', t[:o])), ln))
        o += len(ln) + 1
    out = []
    for k, (s0, ln) in enumerate(raw):
        j = ln.rstrip()[:-1] + raw[k + 1][1] if ln.rstrip().endswith('-') and not re.search(r'[(\[]', ln) and k + 1 < len(raw) else ln
        out.append((s0, ln, j))
    return out


def entry_tier(line, h, hf, allhw, iast):
    """(tier, how) when the line begins an entry of headword h: tier strict | weak | sup, how exact | fold | fuzzy"""
    hm = _head_match(line, h, hf, allhw, iast)
    if hm: return 'strict', hm[0]
    s = _SP(line); m = re.search(r'[(\[（［]', s)
    if not m or m.start() == 0: return None
    pre = _TRAIL.sub('', s[:m.start()]); sup = False
    if pre[:-1] == h and pre[-1:] in ('ံ', 'ာ') and pre not in allhw: pre = h; sup = True
    if (pre == h or fold(pre) == hf) and not re.search(r'[၀-၉0-9။]', s[m.start() + 1:m.start() + 12].split(')')[0]):
        return ('sup' if sup else 'weak'), ('exact' if pre == h else 'fold')
    return None


def order_rule(order, idx, located, P, H, twins, nxt_in_seq, allhw, iasts, disabled=frozenset(), fixed=frozenset()):
    """R over the book, on the placements P[p] / H[p] (copies, changed in place). Returns (moves, cross, extras, stats):
    moves {(p, i): info}, cross {(p, i): (q, s0)} for a row given a line on another page, extras {q: [s0]}."""
    seqr = [(p, i) for p in order for i in range(len(idx[p]))]
    runs, cur = [], []
    for p, i in seqr:
        wid, hw = idx[p][i]
        if cur and _SP(hw) == _SP(idx[cur[-1][0]][cur[-1][1]][1]) and wid == idx[cur[-1][0]][cur[-1][1]][0] + 1: cur.append((p, i))
        else:
            if len(cur) > 1: runs.append(cur)
            cur = [(p, i)]
    if len(cur) > 1: runs.append(cur)
    LN = {}
    def lines(q):
        if q not in LN:
            t, f, offs = located[q][:3]
            LN[q] = page_lines(t, f, offs)
        return LN[q]
    moves, cross, extras = {}, {}, {}
    trace = order_rule.trace = []
    st = {'runs': len(runs), 'keep': 0, 'reassign': 0, 'abstain': 0, 'skipped': 0, 'disabled': 0}
    for run in runs:
        key = idx[run[0][0]][run[0][1]][0]
        ids = [idx[p][i][0] for p, i in run]
        if key in disabled: st['disabled'] += 1; trace.append({'ids': ids, 'act': 'disabled'}); continue
        if any(i in fixed for i in ids): st.setdefault('fixed', 0); st['fixed'] += 1; trace.append({'ids': ids, 'act': 'fixed'}); continue
        pages = []
        for p, _ in run:
            if p not in pages: pages.append(p)
        twinned = any(twins[p][i] is not None for p, i in run) or \
            any(twins[p][k] in [i for q, i in run if q == p] for p in pages for k in range(len(idx[p])))
        if twinned or any(nxt_in_seq.get(a) != b for a, b in zip(pages, pages[1:])):
            st['skipped'] += 1; trace.append({'ids': ids, 'act': 'skip', 'why': 'twin' if twinned else 'pages', 'pages': pages}); continue
        n = len(run); h = _SP(idx[run[0][0]][run[0][1]][1]); hf = fold(h); ia = iasts[key]
        p0, i0 = run[0]; pl, il = run[-1]
        lo = max([P[p0][k] + 1 for k in range(i0) if P[p0][k] is not None], default=0)
        after = [P[pl][k] for k in range(il + 1, len(idx[pl])) if P[pl][k] is not None]
        rng = [(q, lo if q == p0 else 0, None) for q in pages]
        if after: rng[-1] = (pl, rng[-1][1], min(after))
        elif il == len(idx[pl]) - 1 and nxt_in_seq.get(pl) in located:
            qn = nxt_in_seq[pl]
            first = min([x for x in P[qn] if x is not None], default=None)
            rng.append((qn, 0, first))
        E = []
        for q, a, b in rng:
            for s0, ln, jl in lines(q):
                if s0 < a or (b is not None and s0 >= b): continue
                et = entry_tier(jl, h, hf, allhw, ia)
                if et: E.append((q, s0) + et)
        tr = {'ids': ids, 'pages': pages, 'rng': [x[0] for x in rng], 'm': len(E), 'E': [[e[0], e[2]] for e in E]}
        trace.append(tr)
        if len(E) != n: st['abstain'] += 1; tr['act'] = 'abstain'; continue
        if all(E[k][:2] == (p, P[p][i]) for k, (p, i) in enumerate(run)): st['keep'] += 1; tr['act'] = 'keep'; continue
        st['reassign'] += 1; tr['act'] = 'reassign'
        eset = {e[:2] for e in E}
        for k, (p, i) in enumerate(run):
            q, s0, tier, how = E[k]
            old = P[p][i]
            if (q, s0) == (p, old): continue
            kind = 'unplaced' if old is None else ('other homonym' if (p, old) in eset
                                                   else ('non-entry line' if old in {x for x, _, _ in lines(p)}
                                                         else 'line not found'))
            moves[(p, i)] = {'n': n, 'tier': tier, 'kind': kind, 'old': old, 'old_how': H[p][i], 'q': q, 'run': key}
            newhow = {'exact': 'verbatim', 'fold': 'folded', 'fuzzy': 'fuzzy'}[how]
            if q == p: P[p][i] = s0; H[p][i] = newhow
            else:
                P[p][i] = None; H[p][i] = newhow; cross[(p, i)] = (q, s0); extras.setdefault(q, []).append(s0)
    return moves, cross, extras, st


_PCED = None


def _pced():
    """({seq: entry}, {headword key: [seq]}, {folded key: [seq]}) from witness/pced_k.jsonl"""
    global _PCED
    if _PCED is None:
        f = ROOT / 'witness/pced_k.jsonl'; E, ex, fo = {}, {}, {}
        if f.exists():
            for line in f.open(encoding='utf-8'):
                w = json.loads(line); k = _SP(nfc(w['headword']))
                E[w['seq']] = w; ex.setdefault(k, []).append(w['seq']); fo.setdefault(fold(k), []).append(w['seq'])
        _PCED = (E, ex, fo)
    return _PCED


def _pced_verdict(r, own, others, E):
    """'right' | ('another', seq) | 'unclear' for a row's body against its own PCED entry and the headword's others
    (the join's measure: SequenceMatcher on the body against the analysis's tail after ။ + the definition, capped at
    600 characters; right: own >= 0.6 and >= 0.2 above every other; another: another >= 0.6 and >= 0.2 above own)"""
    ob = _SP(r.get('body'))
    if r.get('located') == 'unlocated' or not ob: return 'unclear'
    def ratio(seq):
        w = E[seq]; wd = _SP(nfc((w.get('analysis') or '').partition('။')[2] + (w.get('definition') or '')))[:600]
        return round(SequenceMatcher(None, ob[:len(wd)], wd, autojunk=False).ratio(), 3) if wd else None
    o = ratio(own) if own in E else None
    alts = [(v, s) for s in others for v in [ratio(s)] if v is not None]
    a, aseq = max(alts) if alts else (None, None)
    if o is None: return 'unclear'
    if a is not None and a >= .6 and a - o >= .2: return ('another', aseq)
    if o >= .6 and (a is None or o - a >= .2): return 'right'
    return 'unclear'


def pced_runs(book, rows):
    """the PCED view of each run of the book: {row id: (run key, own seq, [other seqs of the headword], {seq: id})}"""
    jf = ROOT / f'witness/join-{book}.jsonl'
    E, ex, fo = _pced()
    if not jf.exists() or not E: return {}
    J = {}
    for line in jf.open(encoding='utf-8'):
        j = json.loads(line)
        if j.get('seq') is not None and not j.get('count_mismatch'): J[j['id']] = j['seq']
    rs = sorted(rows, key=lambda r: int(r['id'])); out = {}; cur = []
    def close(g):
        if len(g) < 2 or any(r.get('homonym_fix') for r in g): return
        h = _SP(g[0]['headword']); seqs = ex.get(h) or fo.get(fold(h)) or []
        owner = {J[r['id']]: r['id'] for r in g if r['id'] in J}
        for r in g:
            if r['id'] in J and J[r['id']] in seqs:
                out[r['id']] = (g[0]['id'], J[r['id']], [s for s in seqs if s != J[r['id']]], owner)
    for r in rs:
        if cur and _SP(r['headword']) == _SP(cur[-1]['headword']) and int(r['id']) == int(cur[-1]['id']) + 1: cur.append(r)
        else: close(cur); cur = [r]
    close(cur)
    return out


def pced_gate(book, rows):
    """the runs in which PCED puts an R-moved row's new text on another entry: {run key}, and the rows so contradicted"""
    V = pced_runs(book, rows); E = _pced()[0]; bad, rows_bad = set(), []
    for r in rows:
        if not str(r.get('homonym_rule', '')).startswith('order') or r['id'] not in V: continue
        key, own, others, owner = V[r['id']]
        v = _pced_verdict(r, own, others, E)
        if isinstance(v, tuple): bad.add(r['homonym_run']); rows_bad.append(r['id'])
    return bad, rows_bad


def pced_homonyms(book, rows):
    """PCED completes R: a row R did not move whose text PCED decides as another homonym's gives it to that homonym's
    row, in the same run, when that row is unplaced or itself gives its text away (a permutation of the run's texts);
    a row that gives its text and receives none is left unlocated. Moved rows get homonym_rule "pced", homonym_before,
    and homonym_from (the id whose text they took). Returns report lines and the stats."""
    V = pced_runs(book, rows); E = _pced()[0]
    by = {r['id']: r for r in rows}
    verdict = {}
    for i, (key, own, others, owner) in V.items():
        r = by[i]
        if str(r.get('homonym_rule', '')).startswith('order'): continue
        verdict[i] = _pced_verdict(r, own, others, E)
    want = {}
    for i, v in verdict.items():
        if isinstance(v, tuple):
            b = V[i][3].get(v[1])
            if b is not None and b != i: want[i] = b
    conflicts = set()
    claim = {}
    for a, b in want.items(): claim.setdefault(b, []).append(a)
    ok = {a: b for a, b in want.items() if len(claim[b]) == 1}
    conflicts |= {a for a in want if a not in ok}
    while True:
        drop = [a for a, b in ok.items()
                if not (by[b].get('located') == 'unlocated' or b in ok)
                or str(by[b].get('homonym_rule', '')).startswith('order')]
        if not drop: break
        for a in drop: del ok[a]; conflicts.add(a)
    texts = {i: {k: v for k, v in by[i].items() if k not in _HOMONYM_KEEP and k != 'pdf_page'} for i in set(ok) | set(ok.values())}
    pages = {i: by[i]['pdf_page'] for i in texts}
    before = {i: {'located': by[i]['located'], 'pdf_page': by[i]['pdf_page'],
                  'raw': (by[i].get('raw') or '').split('\n')[0] or None} for i in texts}
    recv = {b: a for a, b in ok.items()}
    for i in texts:
        r = by[i]
        for k in list(r):
            if k not in _HOMONYM_KEEP and k != 'pdf_page': del r[k]
        if i in recv:
            r.update(texts[recv[i]]); r['pdf_page'] = pages[recv[i]]; r['homonym_from'] = recv[i]
        else:
            r['located'] = 'unlocated'
        r['homonym_rule'] = 'pced'
        r['homonym_before'] = {k: v for k, v in before[i].items() if v is not None}
    st = {'moved': len(texts), 'received': len(recv), 'left_unlocated': len(texts) - len(recv), 'conflicts': len(conflicts),
          'decided_another': sum(isinstance(v, tuple) for v in verdict.values())}
    return [f'homonyms, PCED pass: {len(texts)} rows changed ({len(recv)} took a sibling\'s text, '
            f'{len(texts) - len(recv)} left unlocated); {len(conflicts)} conflicts left'], st


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

    iasts = {wid: transliterate.process('Burmese', 'IAST', re.sub('[' + MY_DIGITS + r'\d\s]', '', hw)).replace('ṃ', 'ṁ')
             for p in order for wid, hw in idx[p]}
    allhw = {re.sub(r'\s', '', nfc(w)) for (w,) in c.execute('select word from words')}

    def build(disabled=frozenset()):
        """the rows, from the placements of the first pass with R applied (unless ABH_HOMONYM=0)"""
        P = {p: list(located[p][3]) for p in order}; H = {p: list(located[p][4]) for p in order}
        fx = HOMONYM_FIX.get(book, {}) if HOMONYM else {}
        cross, extras = {}, {}
        # the image table (brief §88): the rows of every run read on the page image take the line read there, or no text
        # (same_as); R and the PCED pass leave these runs alone
        fmoves, displaced = {}, {}
        if fx:
            where = {wid: (p, i) for p in order for i, (wid, _) in enumerate(idx[p])}
            LNf = {}
            def flines(q):
                if q not in LNf: LNf[q] = page_lines(*located[q][:3])
                return LNf[q]
            taken = {}
            for wid, (verdict, printed, q, line) in sorted(fx.items()):
                if wid not in where: continue
                p, i = where[wid]
                old = cross.get((p, i), (p, P[p][i])); old_how = H[p][i]
                new = None; how = 'unlocated'
                if not line.startswith('same_as:'):
                    hits = [(s0, jl) for s0, ln, jl in (flines(q) if q in located else []) if _SP(ln).startswith(line)]
                    if len(hits) != 1:
                        print(f'HOMONYM_FIX {wid}: {len(hits)} lines on p. {q} begin with {line}; left as it is'); continue
                    new = (q, hits[0][0]); h = _SP(idx[p][i][1])
                    et = entry_tier(hits[0][1], h, fold(h), allhw, iasts[wid])
                    how = {'exact': 'verbatim', 'fold': 'folded'}.get(et[1] if et else '', 'fuzzy')
                cross.pop((p, i), None)
                if old[0] != p and old[1] in extras.get(old[0], []): extras[old[0]].remove(old[1])
                P[p][i] = None; H[p][i] = how
                if new:
                    if new[0] == p: P[p][i] = new[1]
                    else: cross[(p, i)] = new; extras.setdefault(new[0], []).append(new[1])
                    taken[new] = wid
                fmoves[(p, i)] = {'verdict': verdict, 'printed': printed, 'old': old, 'old_how': old_how, 'line': line}
            fcross, fextras = cross, extras
        else:
            fcross, fextras = {}, {}
        # R, on the placements with the table's rows already set (so that a run beside a fixed run sees its neighbours
        # where the page has them)
        moves, cross, extras, st = (order_rule(order, idx, located, P, H, twins, nxt_in_seq, allhw, iasts, disabled, frozenset(fx))
                                    if HOMONYM else ({}, {}, {}, None))
        cross.update(fcross)
        for q, xs in fextras.items(): extras.setdefault(q, []).extend(xs)
        if fx:
            # a row outside the table standing on a line the table gives to a row of the run loses it
            for p in order:
                for i, x in enumerate(P[p]):
                    wid = idx[p][i][0]
                    at = cross.get((p, i), (p, x))
                    if wid not in fx and at[1] is not None and at in taken:
                        displaced[(p, i)] = {'by': taken[at], 'old_how': H[p][i], 'old': at}
                        cross.pop((p, i), None); P[p][i] = None; H[p][i] = 'unlocated'
        # an article's text runs to the next start on its page: a placed row's, or a line R gave to a row of another page
        bounds = {p: sorted({x for x in P[p] if x is not None} | set(extras.get(p, []))) for p in order}

        def continuation(p):
            """text after the last located article of page p, up to the next located headword"""
            parts, via, uncertain = [], [], False
            q = nxt_in_seq.get(p)
            while q is not None:
                if q in located:
                    t2, f2, offs2 = located[q][:3]; pos2 = P[q]
                    first = bounds[q][0] if bounds[q] else None
                    cont = t2[:offs2[first]] if first is not None else ''
                    if cont.strip(): parts.append(cont); via.append(q)
                    if first is None or (pos2[0] is None and first not in extras.get(q, [])): uncertain = True
                    break
                rec = json.loads((pdir / f'p{q:04d}.json').read_text())
                parts.append(page_text(rec)); via.append(q)
                q = nxt_in_seq.get(q)
            return parts, via, uncertain

        rows = []
        for pi, p in enumerate(order):
            ents = idx[p]
            for i, (wid, hw) in enumerate(ents):
                q, at = cross.get((p, i), (p, P[p][i]))
                row = dict(id=wid, book=book, pdf_page=q, index_page=ipage[p], headword=hw,
                           located=H[p][i], status='ocr')
                if twins[p][i] is not None: row['variant_of'] = ents[twins[p][i]][0]
                if wid in misfiled: row['index_page'] = misfiled[wid]; row['index_misfiled'] = True
                iast = iasts[wid]
                if at is not None:
                    t, f, offs = located[q][:3]
                    a = offs[at]
                    nb = next((x for x in bounds[q] if x > at), None)
                    e = offs[nb] if nb is not None else len(t)
                    raw = t[a:e]
                    if nb is None:
                        parts, via, uncertain = continuation(q)
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
                fm = fmoves.get((p, i)) or displaced.get((p, i))
                if fm:
                    q0, s00 = fm['old']
                    before = {'located': fm['old_how'], 'pdf_page': q0}
                    if s00 is not None:
                        t0, f0, offs0 = located[q0][:3]; a0 = offs0[s00]; e0 = t0.find('\n', a0)
                        before['raw'] = t0[a0:e0 if e0 != -1 else len(t0)].strip()
                    row['homonym_before'] = before
                    if (p, i) in fmoves:
                        row['homonym_rule'] = 'image'
                        row['homonym_fix'] = {'verdict': fm['verdict'], 'printed': fm['printed']}
                        if fm['line'].startswith('same_as:'): row['same_as'] = int(fm['line'].split(':')[1])
                    else:
                        row['homonym_rule'] = 'image:displaced'; row['homonym_displaced_by'] = fm['by']
                mv = moves.get((p, i))
                if mv:
                    t0, f0, offs0 = located[p][:3]
                    old = mv['old']
                    before = {'located': mv['old_how'], 'pdf_page': p}
                    if old is not None:
                        a0 = offs0[old]; e0 = t0.find('\n', a0)
                        before['raw'] = t0[a0:e0 if e0 != -1 else len(t0)].strip()
                    before['kind'] = mv['kind']
                    row['homonym_rule'] = f'order:{mv["n"]}:{mv["tier"]}'
                    row['homonym_before'] = before
                    row['homonym_run'] = mv['run']
                rows.append(row)
        return rows, moves, st

    rows, moves, rst = build()
    if HOMONYM_FIX.get(book):
        img = [r for r in rows if r.get('homonym_rule') == 'image']
        print(f'homonyms, image table (docs/homonyms-checked.tsv): {len(img)} rows set '
              f'({sum(1 for r in img if r.get("same_as"))} same_as), '
              f'{sum(1 for r in rows if r.get("homonym_rule") == "image:displaced")} rows displaced from a line the table gives to another')
    trace0 = getattr(order_rule, 'trace', [])
    hst = None; gate_rows = []; undone = 0
    if HOMONYM:
        from abhidhana_witness_analysis import PCED_BOOKS
        if book in PCED_BOOKS:
            bad, gate_rows = pced_gate(book, rows)
            if bad:
                undone = sum(1 for r in rows if r.get('homonym_run') in bad)
                rows, moves, rst = build(frozenset(bad))
        kinds = {}
        for mv in moves.values(): kinds[mv['kind']] = kinds.get(mv['kind'], 0) + 1
        print(f'homonyms, order rule R: {rst["runs"]} runs; reassigned {rst["reassign"]}, kept {rst["keep"]}, '
              f'abstained {rst["abstain"]}, skipped {rst["skipped"]} (pages not consecutive or a variant twin); '
              f'{len(moves)} rows moved (' + ', '.join(f'{k} {v}' for k, v in sorted(kinds.items())) + ')'
              + (f'; PCED contradicted {len(gate_rows)} rows, {rst["disabled"]} runs left as they were ({undone} R moves undone)'
                 if book in PCED_BOOKS else ''))
        if book in PCED_BOOKS:
            m, hst = pced_homonyms(book, rows)
            for x in m: print(x)
        for r in rows: r.pop('homonym_run', None)
        tp = __import__('os').environ.get('ABH_HOMONYM_TRACE')
        if tp:   # a record of R's decision on every run (measurement only; nothing in the output depends on it)
            with open(f'{tp}/trace-{book}.jsonl', 'w', encoding='utf-8') as tf:
                for x in trace0: tf.write(json.dumps(dict(x, stage='first'), ensure_ascii=False) + '\n')
                if getattr(order_rule, 'trace', []) is not trace0:
                    for x in order_rule.trace: tf.write(json.dumps(dict(x, stage='after gate'), ensure_ascii=False) + '\n')

    # run-on articles split out of their neighbour (books without PCED only; brief §67, §69)
    _pt = {}
    def pages_text(q):
        if q not in _pt:
            fp = pdir / f'p{q:04d}.json'
            _pt[q] = page_text(json.loads(fp.read_text())) if fp.exists() else ''
        return _pt[q]
    if book in SPLIT_BOOKS:
        for m in split_runons(book, rows, allhw, pages_text): print(m)
    # farther-body run-ons, all 29 books (brief §89); after split_runons and the homonym passes
    if FARBODY:
        for m in farbody_split(book, rows, allhw, pages_text)[0]: print(m)
    # the compound analysis from the typed PCED witness where it has one (tools/abhidhana_witness_analysis.py)
    from abhidhana_witness_analysis import apply as apply_witness_analysis
    for m in apply_witness_analysis(book, rows): print(m)
    # the body's first words on the headword's line (§50): kept in books 01-19 only where PCED's
    # definition begins with them, elsewhere by their shape alone
    from abhidhana_witness_analysis import gate_head
    for m in gate_head(book, rows): print(m)
    # hand corrections against the print (docs/corrections.tsv), last, so every re-run keeps them
    from abhidhana_corrections import apply as apply_corrections
    for m in apply_corrections(book, rows): print(m)
    # ဩ read as သ (the vowel's mark missed): an OCR analysis of a headword that begins with ဩ always
    # begins with ဩ too (vol. 4/3, 394 rows, 27 Sep 2026); PCED analyses and hand corrections untouched
    n_o = 0
    for row in rows:
        a = row.get('analysis') or ''
        if (row.get('headword', '').startswith('ဩ') and a.startswith('သ') and row.get('analysis_source') != 'pced'
                and 'analysis' not in row.get('corrected', {})):
            # read as သ (သမကာ), or as သ before a ဩ read right (သဩလီန): the first letter is ဩ
            row['analysis_o_restored'] = a; row['analysis'] = 'ဩ' + a[2 if a.startswith('သဩ') else 1:]; n_o += 1
    if n_o: print(f'ဩ restored at the start of {n_o} analyses (read as သ or သဩ)')
    for row in rows:   # a corrected headword is romanised and checked against OSBCT afresh
        if 'headword' in row.get('corrected', {}):
            base = re.sub('[' + MY_DIGITS + r'\d\s]', '', row['headword'])
            row['iast'] = transliterate.process('Burmese', 'IAST', base).replace('ṃ', 'ṁ')
            if vocab is not None:
                k = row['iast'].lower()
                row['osbct'] = 'word' if k in vocab else ('inside' if k in blob else 'none')

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
           f'| compound analysis [ ] recovered by the OCR | {pct(cnt(lambda r: r.get("analysis_read") or (r.get("analysis") and r.get("analysis_source") != "pced")))} |',
           f'| compound analysis taken from the typed PCED witness (tools/abhidhana_witness_analysis.py) | {pct(cnt(lambda r: r.get("analysis_source") == "pced"))} |',
           f'| compound analysis, either | {pct(cnt(lambda r: r.get("analysis")))} |',
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
