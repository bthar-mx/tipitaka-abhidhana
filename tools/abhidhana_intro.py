#!/usr/bin/env python3
"""The Introduction page of the website, from docs/introduction/. Standard library only.

Called by tools/abhidhana_site.py; can also be run alone to write one page:
    python3 tools/abhidhana_intro.py OUT.html      # site/src/introduction/index.html filled in

**The contract** (the files are written by another chat and grow; this reads them as they are):
  docs/introduction/chN-*.md   one chapter each, N its number. It holds
      # <title>                          (English; the page takes each language's title from its section)
      *... PDF pp. A–B ...*              (the first italic line: the chapter's PDF pages)
      a status table before the first ##: either  | | status |  with rows "Burmese transcription",
          "English", "Spanish", or  | batch | PDF pp. | Burmese | English | Spanish |  one row a batch;
          a status cell is drafted / reviewed / corrected, or — (not yet done)
      ## 1. Burmese transcription  /  ## 2. English  /  ## 3. Español  /  ## Notes for review [...]
  Inside a section: paragraphs, headings as lines wholly in **bold** (several in a row make one
  heading), > quotes (verses and footnotes), numbered lists, **bold**, *italics*, `code`, and page
  markers `[p. N]` (also `[p. N, lower half]`, `[p. N continues]`), on a line of their own or inline.
  docs/introduction/citation-abbreviations.tsv   the abbreviations, one a row (header as in the file)
  docs/introduction/README.md   its "Contents and status" table gives the number of chapters, so the
      page can say which are not yet transcribed.

Views (buttons on the page, remembered per browser): the translation (EN/ES by the site's switch),
the Burmese original, or both side by side. Side by side pairs the texts page by page where the
translation carries the page markers, and shows the two whole sections otherwise.
"""
import csv, html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / 'docs/introduction'
IMG = 'https://abhidhana-img.buddha-dhamma.net/01/{:04d}.webp'   # the introduction is in vol. 1
E = lambda s: html.escape(s, quote=False)
MARK = re.compile(r'`\[p\.\s*(\d+)([^\]`]*)\]`')
LANGS = ('my', 'en', 'es')
SECTION = {'my': re.compile(r'^##\s*1\.'), 'en': re.compile(r'^##\s*2\.'), 'es': re.compile(r'^##\s*3\.'),
           'notes': re.compile(r'^##\s*Notes for review', re.I)}
ST = {'en': {'drafted': 'drafted', 'reviewed': 'reviewed', 'corrected': 'corrected', 'pending': 'not yet done'},
      'es': {'drafted': 'borrador', 'reviewed': 'revisado', 'corrected': 'corregido', 'pending': 'aún sin hacer'}}
PART = {'en': {'my': 'Burmese', 'en': 'English', 'es': 'Spanish'},
        'es': {'my': 'Birmano', 'en': 'Inglés', 'es': 'Español'}}


# --- inline and block Markdown (the subset the files use) --------------------------------------
def marker(m, inline=True):
    n = int(m.group(1)); rest = m.group(2).strip(' ,')
    label = f'p. {n}' + (f', {rest}' if rest else '')
    return (f'<a class="pg" href="{IMG.format(n)}" target="_blank" rel="noopener" '
            f'title="PDF p. {n} (vol. 1)">{E(label)}</a>')


def inline(t, burmese=False):
    """escape, then **bold**, *italics*, `code` (page markers become links), [text](url)"""
    out, pos = [], 0
    for m in re.finditer(r'`([^`]+)`', t):
        out.append(_text(t[pos:m.start()], burmese)); pos = m.end()
        mm = MARK.fullmatch(m.group(0))
        out.append(marker(mm) if mm else f'<code>{E(m.group(1))}</code>')
    out.append(_text(t[pos:], burmese))
    return ''.join(out)


def _text(t, burmese):
    t = E(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'\1', t)   # links to files in the repo: text only
    if not burmese:   # Burmese words inside a translation, in the Burmese face
        t = re.sub(r'[က-႟](?:[က-႟\s\-]*[က-႟])?',
                   lambda m: f'<span class="my" lang="my">{m.group(0)}</span>', t)
    return t


BOLDLINE = re.compile(r'^\*\*[^*]+\*\*\s*$')


def blocks(lines):
    """split a section's lines into blocks: ('h', [lines]) ('p', ...) ('q', ...) ('ol', ...) ('mark', m)"""
    out, cur, kind = [], [], None
    def flush():
        nonlocal cur, kind
        if cur: out.append((kind, cur))
        cur, kind = [], None
    for ln in lines:
        s = ln.rstrip()
        if not s.strip() or s.strip() == '---':
            flush(); continue
        m = MARK.fullmatch(s.strip())
        if m:
            flush(); out.append(('mark', [m])); continue
        k = ('h' if BOLDLINE.match(s) else 'q' if s.startswith('>') else
             'ol' if re.match(r'^\d+\.\s', s) else None)
        if k == 'ol' and kind == 'ol':
            cur.append(s); continue
        if k is None and kind == 'ol' and s.startswith(' '):
            cur[-1] += ' ' + s.strip(); continue
        if k is None: k = 'p'
        if k != kind or k == 'ol':
            flush(); kind = k
        cur.append(s)
    flush()
    return out


def render(bl, lang, ids=None, prefix=''):
    """blocks -> html; headings get ids (prefix-k) when ids is a list to collect (text, id) into"""
    burmese = lang == 'my'
    h, k = [], 0
    for kind, ls in bl:
        if kind == 'mark':
            h.append(f'<p class="pgline">{marker(ls[0])}</p>'); continue
        if kind == 'h':
            k += 1
            txt = [re.sub(r'^\*\*|\*\*\s*$', '', x.strip()) for x in ls]
            aid = f'{prefix}-{k}'
            if ids is not None: ids.append((' '.join(txt), aid))
            h.append(f'<h3 id="{aid}" data-a="{aid}">' + '<br>'.join(inline(x, burmese) for x in txt) + '</h3>')
        elif kind == 'q':
            body = [inline(re.sub(r'^>\s?', '', x), burmese) for x in ls]
            h.append('<blockquote>' + '<br>'.join(body) + '</blockquote>')
        elif kind == 'ol':
            items = [re.sub(r'^\d+\.\s+', '', x) for x in ls]
            start = re.match(r'^(\d+)\.', ls[0]).group(1)
            h.append(f'<ol start="{start}">' + ''.join(f'<li>{inline(i, burmese)}</li>' for i in items) + '</ol>')
        else:
            # a Burmese paragraph is one line; several lines are a list printed line by line.
            # A translation is wrapped: join, but keep "(1) …" items on lines of their own.
            if burmese:
                h.append('<p>' + '<br>'.join(inline(x.strip(), True) for x in ls) + '</p>')
            else:
                parts = []
                for x in ls:
                    x = x.strip()
                    if parts and not re.match(r'^\(\s*[\d၀-၉]+\s*\)', x): parts[-1] += ' ' + x
                    else: parts.append(x)
                h.append('<p>' + '<br>'.join(inline(x) for x in parts) + '</p>')
    return '\n'.join(h)


# --- a chapter -----------------------------------------------------------------------------------
def status_word(cell):
    c = cell.strip().strip('*').lower()
    for w in ('corrected', 'reviewed', 'drafted'):
        if w in c: return w
    return 'pending' if not c.strip('—-– ') or c.startswith('—') else c.split()[0]


def statuses(head_lines):
    """[(row label or None, {part: status})] from the status table before the first ##"""
    rows = [l for l in head_lines if l.startswith('|')]
    if len(rows) < 3: return []
    cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
    hdr = [c.lower() for c in cells(rows[0])]
    out = []
    if len(hdr) == 2 and 'status' in hdr[1]:
        d = {}
        for l in rows[2:]:
            a, b = cells(l)[:2]; a = a.lower()
            part = 'my' if 'burmese' in a else 'en' if 'english' in a else 'es' if ('spanish' in a or 'español' in a) else None
            if part: d[part] = status_word(b)
        if d: out.append((None, d))
    else:
        col = {p: next((i for i, h in enumerate(hdr) if k in h), None)
               for p, k in (('my', 'burmese'), ('en', 'english'), ('es', 'spanish'))}
        pp = next((i for i, h in enumerate(hdr) if 'pp' in h), None)
        for l in rows[2:]:
            c = cells(l)
            d = {p: status_word(c[i]) for p, i in col.items() if i is not None and i < len(c)}
            lab = c[pp] if pp is not None and pp < len(c) else c[0]
            out.append((lab, d))
    return out


def chapter(path):
    n = int(re.match(r'ch(\d+)', path.name).group(1))
    lines = path.read_text(encoding='utf-8').split('\n')
    title = next((l[2:].strip() for l in lines if l.startswith('# ')), path.stem)
    idx = {k: next((i for i, l in enumerate(lines) if rx.match(l)), None) for k, rx in SECTION.items()}
    first = min([i for i in idx.values() if i is not None] or [len(lines)])
    head = lines[:first]
    starts = sorted((i, k) for k, i in idx.items() if i is not None)
    sec = {}
    for j, (i, k) in enumerate(starts):
        end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        sec[k] = (lines[i], lines[i + 1:end])
    pdf = re.search(r'PDF pp?\.\s*(\d+)\s*[–-]\s*(\d+)', '\n'.join(head))
    return dict(n=n, title=title, sec=sec, status=statuses(head),
                pdf=(int(pdf.group(1)), int(pdf.group(2))) if pdf else None)


def split_pages(ls):
    """a section's lines -> [(page or None, lines)], cut at every page marker, inline ones too"""
    out = [[None, []]]
    for ln in ls:
        pos = 0
        for m in MARK.finditer(ln):
            before = ln[pos:m.start()]
            if before.strip(): out[-1][1].append(before)
            out.append([int(m.group(1)), [ln[m.start():m.end()]]])   # keep the marker as a line
            pos = m.end()
        rest = ln[pos:]
        if pos == 0: out[-1][1].append(ln)
        elif rest.strip(): out[-1][1].append(rest.lstrip())
    # merge chunks of the same page (p. 89 and p. 89, lower half)
    merged = []
    for p, l in out:
        if merged and merged[-1][0] == p and p is not None: merged[-1][1] += [''] + l
        else: merged.append([p, l])
    return [(p, l) for p, l in merged if any(x.strip() for x in l)]


def chapter_html(c):
    n = c['n']; out = [f'<section class="chap" id="ch{n}">']
    toc = {}
    titles = {}
    for lang in LANGS:
        if lang not in c['sec']: continue
        bl = blocks(c['sec'][lang][1])
        # the chapter's own title: the first heading, when it comes before any text; a heading of
        # digits alone (the chapter number, ၅) is part of it
        t = None
        # a heading of the chapter numeral alone (၄), then the title heading: one title
        for i in range(min(2, len(bl) - 1)):
            if bl[i][0] == 'h' and bl[i + 1][0] == 'h' and re.fullmatch(r'\*\*[\d၀-၉]+\*\*', bl[i][1][-1].strip()):
                bl = bl[:i] + [('h', bl[i][1] + bl[i + 1][1])] + bl[i + 2:]
                break
        if bl and bl[0][0] == 'h':
            t = ' '.join(re.sub(r'^\*\*|\*\*\s*$', '', x.strip()) for x in bl[0][1])
            t = re.sub(r'^[\d၀-၉]+\s+', '', t)
            bl = bl[1:]
        elif len(bl) > 1 and bl[0][0] == 'mark' and bl[1][0] == 'h':
            t = ' '.join(re.sub(r'^\*\*|\*\*\s*$', '', x.strip()) for x in bl[1][1])
            t = re.sub(r'^[\d၀-၉]+\s+', '', t)
            bl = bl[:1] + bl[2:]
        titles[lang] = t
        c['sec'][lang] = (c['sec'][lang][0], None, bl)
    ttl = {'en': titles.get('en') or c['title'], 'es': titles.get('es') or c['title'], 'my': titles.get('my') or c['title']}
    # heading
    out.append('<h2 class="chap-title">'
               f'<span class="tr s-tt" lang="en">{inline(ttl["en"])}</span>'
               f'<span class="tr s-tt" lang="es">{inline(ttl["es"])}</span>'
               f'<span class="my s-tm" lang="my">{E(ttl["my"])}</span></h2>')
    meta = []
    if c['pdf']:
        a, b = c['pdf']
        link = lambda p: f'<a class="pg" href="{IMG.format(p)}" target="_blank" rel="noopener">{p}</a>'
        meta.append(f'<span class="tr" lang="en">Vol. 1 (1964), PDF pp. {link(a)}–{link(b)}.</span>'
                    f'<span class="tr" lang="es">Vol. 1 (1964), págs. {link(a)}–{link(b)} del PDF.</span>')
    # status labels
    chips = []
    for lab, d in c['status']:
        for lang in ('en', 'es'):
            if d and all(v == 'pending' for v in d.values()):   # a batch not begun: one label
                parts = f'<span class="chip st-pending">{E(ST[lang]["pending"])}</span>'
            else:
                parts = ' '.join(f'<span class="chip st-{d[p] if d[p] in ST["en"] else "other"}">{PART[lang][p]}: '
                                 f'{E(ST[lang].get(d[p], d[p]))}</span>' for p in ('my', 'en', 'es') if p in d)
            pre = f'<span class="chip-lab">{E(lab if lang == "en" else lab.replace("to the start of", "hasta el comienzo de"))}</span> ' if lab else ''
            chips.append(f'<span class="tr" lang="{lang}">{pre}{parts}</span>')
    if chips:
        rows = []
        for i in range(0, len(chips), 2):
            rows.append('<div class="chips">' + chips[i] + chips[i + 1] + '</div>')
        meta.append(''.join(rows))
    out.append('<div class="chap-meta">' + ''.join(meta) + '</div>')
    # single views
    for lang in LANGS:
        if lang not in c['sec']: continue
        ids = []
        body = render(c['sec'][lang][2], lang, ids, f'ch{n}-{lang}')
        toc[lang] = ids
        cls = 's-my' if lang == 'my' else 's-tr tr'
        la = f' lang="{lang}"'
        out.append(f'<div class="sec {cls}{" my-text" if lang == "my" else ""}"{la}>{body}</div>')
    # side by side, per translation language
    if 'my' in c['sec']:
        mych = split_pages([l for kind, ls in c['sec']['my'][2] for l in _lines(kind, ls)])
        for lang in ('en', 'es'):
            if lang not in c['sec']: continue
            trl = [l for kind, ls in c['sec'][lang][2] for l in _lines(kind, ls)]
            trch = split_pages(trl)
            rows = []
            if any(p is not None for p, _ in trch):
                pages = []
                for p, _ in mych + trch:
                    if p not in pages: pages.append(p)
                for p in pages:
                    a = [l for q, l in mych if q == p]; b = [l for q, l in trch if q == p]
                    rows.append((sum(a, []), sum(b, [])))
            else:
                rows.append((sum((l for _, l in mych), []), trl))
            h = [f'<div class="pair s-pair tr" lang="{lang}">']
            for a, b in rows:
                h.append('<div class="pair-row">'
                         f'<div class="my-text" lang="my">{render(blocks(a), "my", None, f"ch{n}-my")}</div>'
                         f'<div lang="{lang}">{render(blocks(b), lang, None, f"ch{n}-{lang}")}</div></div>')
            h.append('</div>')
            out.append('\n'.join(h))
    # notes for review
    if 'notes' in c['sec']:
        hdr, ls = c['sec']['notes']
        suffix = re.sub(r'^##\s*Notes for review\s*', '', hdr).strip()
        body = render(blocks(ls), 'en')
        out.append('<details class="notes"><summary>'
                   f'<span class="tr" lang="en">Notes for review {E(suffix)}</span>'
                   f'<span class="tr" lang="es">Notas para la revisión {E(suffix.replace("batch", "tanda"))}</span>'
                   f'</summary><div lang="en">{body}</div></details>')
    out.append('</section>')
    return '\n'.join(out), ttl, toc


def _lines(kind, ls):
    """blocks back to lines (for cutting at the page markers)"""
    if kind == 'mark': return [ls[0].group(0), '']
    return ls + ['']


# --- the abbreviations ---------------------------------------------------------------------------
def abbreviations_html():
    f = DIR / 'citation-abbreviations.tsv'
    if not f.exists(): return '', 0, set()
    rows = list(csv.DictReader(f.open(encoding='utf-8'), delimiter='\t'))
    sts = {status_word(r.get('status', '')) for r in rows}
    h = ['<table class="abbr" id="abbr-table"><thead><tr>'
         '<th><span class="tr" lang="en">Abbreviation</span><span class="tr" lang="es">Abreviatura</span></th>'
         '<th><span class="tr" lang="en">Romanised</span><span class="tr" lang="es">Romanizada</span></th>'
         '<th><span class="tr" lang="en">Work</span><span class="tr" lang="es">Obra</span></th>'
         '<th class="s-mycol"><span class="tr" lang="en">As printed</span><span class="tr" lang="es">Tal como se imprime</span></th>'
         '<th><span class="tr" lang="en">List</span><span class="tr" lang="es">Lista</span></th>'
         '<th><span class="tr" lang="en">Note</span><span class="tr" lang="es">Nota</span></th>'
         '<th>p.</th></tr></thead><tbody>']
    for r in rows:
        g = lambda k: (r.get(k) or '').strip()
        lst = lambda lang: E(' '.join(x for x in ((g('list') if lang == 'en' else g('list_es') or g('list')), g('list_no')) if x))
        p = g('pdf_page')
        pl = f'<a class="pg" href="{IMG.format(int(p))}" target="_blank" rel="noopener">{E(p)}</a>' if p.isdigit() else E(p)
        h.append('<tr>'
                 f'<td class="my" lang="my">{E(g("abbr_my"))}</td>'
                 f'<td class="ro">{E(g("abbr_iast"))}</td>'
                 f'<td>{E(g("work"))}</td>'
                 f'<td class="my s-mycol" lang="my">{E(g("entry_my"))}</td>'
                 f'<td><span class="tr" lang="en">{lst("en")}</span><span class="tr" lang="es">{lst("es")}</span></td>'
                 f'<td><span class="tr" lang="en">{E(g("note_en"))}</span><span class="tr" lang="es">{E(g("note_es"))}</span></td>'
                 f'<td>{pl}</td></tr>')
    h.append('</tbody></table>')
    return '\n'.join(h), len(rows), sts


# --- the page ------------------------------------------------------------------------------------
def chapters_total():
    f = DIR / 'README.md'
    if not f.exists(): return None
    return len(re.findall(r'^\|\s*(\d+)\.\s', f.read_text(encoding='utf-8'), re.M)) or None


def page_html():
    chs = [chapter(p) for p in sorted(DIR.glob('ch*.md'), key=lambda p: int(re.match(r'ch(\d+)', p.name).group(1)))
           if re.match(r'ch\d+', p.name)]
    parts, tocs, drafts = [], [], False
    for c in chs:
        h, ttl, toc = chapter_html(c)
        parts.append(h); tocs.append((c['n'], ttl, toc))
        for _, d in c['status']:
            if any(v not in ('reviewed', 'corrected', 'pending') for v in d.values()): drafts = True
    ab, nab, absts = abbreviations_html()
    if absts - {'reviewed', 'corrected', 'pending'}: drafts = True
    # table of contents
    t = ['<nav class="toc" aria-label="Contents">',
         '<h2><span class="tr" lang="en">Contents</span><span class="tr" lang="es">Índice</span></h2><ol class="toc-ch">']
    for n, ttl, toc in tocs:
        sub = lambda lang: ''.join(f'<li><a href="#{a}">{inline(x, lang == "my")}</a></li>' for x, a in toc.get(lang, []))
        t.append(f'<li value="{n}"><a href="#ch{n}">'
                 f'<span class="tr s-tt" lang="en">{inline(ttl["en"])}</span><span class="tr s-tt" lang="es">{inline(ttl["es"])}</span>'
                 f'<span class="my s-tm" lang="my">{E(ttl["my"])}</span></a>'
                 f'<ul class="tr t-tr" lang="en">{sub("en")}</ul><ul class="tr t-tr" lang="es">{sub("es")}</ul>'
                 f'<ul class="t-my my-text" lang="my">{sub("my")}</ul></li>')
    t.append('</ol>')
    if nab:
        t.append('<p class="toc-extra"><a href="#abbreviations"><span class="tr" lang="en">Citation abbreviations</span>'
                 '<span class="tr" lang="es">Abreviaturas de las citas</span></a></p>')
    total = chapters_total()
    have = {n for n, _, _ in tocs}
    if total:
        miss = [str(i) for i in range(1, total + 1) if i not in have]
        if miss:
            t.append(f'<p class="note"><span class="tr" lang="en">Not yet transcribed: chapter{"s" if len(miss) > 1 else ""} {", ".join(miss)}.</span>'
                     f'<span class="tr" lang="es">Aún sin transcribir: capítulo{"s" if len(miss) > 1 else ""} {", ".join(miss)}.</span></p>')
    t.append('</nav>')
    banner = ('<div class="draft-banner"><span class="tr" lang="en"><strong>Draft.</strong> The Burmese was transcribed '
              'from the page images and translated into English and Spanish by Claude, an AI model; none of it has been '
              'reviewed yet. It is not a reading: check each page against its image (the <span class="pgdemo">p. N</span> '
              'links).</span><span class="tr" lang="es"><strong>Borrador.</strong> El birmano lo transcribió de las '
              'imágenes de las páginas, y lo tradujo al inglés y al español, Claude, un modelo de IA; nada está revisado '
              'todavía. No es una lectura: compare cada página con su imagen (los enlaces <span class="pgdemo">p. N</span>).'
              '</span></div>') if drafts else ''
    abbr = ''
    if nab:
        abbr = ('<section class="chap" id="abbreviations"><h2 class="chap-title"><span class="tr" lang="en">Citation abbreviations</span>'
                '<span class="tr" lang="es">Abreviaturas de las citas</span></h2>'
                f'<div class="chap-meta"><span class="tr" lang="en">The {nab} abbreviations of the works cited, with the full title as vol. 1 prints it '
                '(PDF pp. 94–97) and the work\'s place in its list of works consulted. A citation is volume.page unless the note says otherwise.</span>'
                f'<span class="tr" lang="es">Las {nab} abreviaturas de las obras citadas, con el título completo tal como lo imprime el vol. 1 '
                '(págs. 94–97 del PDF) y el lugar de la obra en su lista de obras consultadas. Una cita es volumen.página salvo que la nota diga otra cosa.</span></div>'
                '<label class="searchbox abbr-search" for="abbr-q"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
                '<input id="abbr-q" type="search" autocomplete="off" spellcheck="false" data-i18n-ph="abbr_ph"></label>'
                '<p class="note" id="abbr-n"></p><div class="abbr-wrap">' + ab + '</div></section>')
    return banner + '\n' + '\n'.join(t) + '\n' + '\n'.join(parts) + '\n' + abbr


def fill(template_text):
    return template_text.replace('<!--INTRO-->', page_html())


if __name__ == '__main__':
    src = ROOT / 'site/src/introduction/index.html'
    Path(sys.argv[1]).write_text(fill(src.read_text(encoding='utf-8')), encoding='utf-8')
