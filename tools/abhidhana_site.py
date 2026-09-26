#!/usr/bin/env python3
"""Build the public website (site/dist/) from the committed data. Standard library only.

    python3 tools/abhidhana_site.py            # what Cloudflare Pages runs on every push
    ABHIDHANA_SITE_OUT=/tmp/dist python3 tools/abhidhana_site.py   # build elsewhere, to test

Inputs, all in git: site/src/ (the pages, scripts, styles, _headers, _redirects),
docs/labels.md §0 (the label table, via tools/abhidhana_labels.py), site/volumes.json (one row per book: numbering, Burmese and romanised range, PDF pages, index
headwords, the page to open on), and ocr/<book>/articles.jsonl + pali.jsonl.

A book is published when its articles.jsonl and pali.jsonl exist; the others are listed as
"coming". Nothing from the typed witnesses (PCED, Pn Daza's dict.db) is read or published:
only our OCR and what the project adds (structure, labels, romanisation, attestation, status).

Output, site/dist/ (gitignored):
    everything in site/src/, with <!--VOLUMES--> in volumes/index.html filled in; index.html is Browse
    (assets/browse.js, data from tools/abhidhana_browse.py)
    introduction/index.html   <!--INTRO--> filled from docs/introduction/ (tools/abhidhana_intro.py)
    about/index.html      <!--HISTORY-EN--> / <!--HISTORY-ES--> filled from docs/history.md, but only
                          when its first lines hold `<!-- site: publish -->` (the romanised names
                          need review first); `<!-- site: draft -->` leaves them empty, unless the
                          build runs with ABHIDHANA_SITE_DRAFTS=1 (a local preview, marked draft)
    data/volumes.json     the books, their status and their figures
    data/v<book>.json     one per published book: compact records, in index order
    data/search.json      [book, id, p, h, r] per headword, for search across all books
    data/labels.json      the label table (no OCR readings), with the number of articles per label
    abbreviations/index.html  <!--LABELS--> (the label table) and <!--ABBR--> (the citation abbreviations)
    data/v<book>.json records carry t = {es|en: {x: text, s: status}} from docs/translation/meanings/<book>.jsonl

Record keys (as in the Reader, docs of tools/abhidhana_reader_data.py, plus i, s, m):
    i id  p PDF page  q printed page  h headword  r IAST  o OSBCT  x v/f/u  l label  lo OCR label
    a analysis  ai analysis IAST  b body  sp Pāḷi spans  c citations  ci citations IAST
    s status (ocr / drafted / reviewed / corrected)  m 1 if the index files it on another page
    as "pced" when the analysis comes from the typed PCED witness (tools/abhidhana_witness_analysis.py)
    hi the index's spelling of a headword corrected by hand
    cf the fields corrected by hand against the print (docs/corrections.tsv), e.g. ["analysis"]
"""
import html, json, os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'site/src'
OUT = Path(os.environ.get('ABHIDHANA_SITE_OUT', ROOT / 'site/dist'))
sys.path.insert(0, str(ROOT / 'tools'))
from abhidhana_labels import LABELS   # docs/labels.md §0: the one label table
X = {'verbatim': 'v', 'verbatim-inline': 'v', 'folded': 'v', 'fuzzy': 'f', 'unlocated': 'u'}
MAX_FILE = 25 * 1024 * 1024      # Cloudflare Pages: 25 MiB per file
MAX_FILES = 20000                # and 20,000 files per site on the free plan


def records(book):
    P = {}; TR = meanings(book)
    with (ROOT / f'ocr/{book}/pali.jsonl').open(encoding='utf-8') as f:
        for line in f:
            r = json.loads(line); P[r['id']] = r
    V = []
    with (ROOT / f'ocr/{book}/articles.jsonl').open(encoding='utf-8') as f:
        for line in f:
            r = json.loads(line); p = P.get(r['id'], {})
            d = {'i': r['id'], 'p': r['pdf_page'], 'q': r['index_page'], 'h': r['headword'],
                 'r': r.get('iast') or p.get('headword_iast') or ''}
            if r.get('osbct'): d['o'] = r['osbct']
            d['x'] = X[r['located']]
            if r.get('label'): d['l'] = r['label']
            if r.get('label_ocr') and r['label_ocr'] != r.get('label'): d['lo'] = r['label_ocr']
            if r.get('analysis'): d['a'] = r['analysis']
            b = p.get('body_joined') or re.sub(r'-\s*\n\s*', '', r.get('body') or '').replace('\n', ' ')
            if b: d['b'] = b
            if r.get('citations'): d['c'] = r['citations']
            if p.get('analysis_iast'): d['ai'] = p['analysis_iast']
            if p.get('citations_iast'): d['ci'] = p['citations_iast']
            if p.get('pali'): d['sp'] = [[s['start'], s['end'], s['iast'], s.get('tokens', 1)] for s in p['pali']]
            d['s'] = r.get('status') or 'ocr'
            if r.get('index_misfiled'): d['m'] = 1
            if r.get('headword_index'): d['hi'] = r['headword_index']   # the index's misspelling, kept (docs/corrections.tsv)
            if r.get('analysis_source') == 'pced': d['as'] = 'pced'   # analysis from the typed PCED witness
            if r.get('corrected'): d['cf'] = sorted(r['corrected'])   # fields corrected by hand (docs/corrections.tsv)
            if r['id'] in TR: d['t'] = TR[r['id']]
            V.append(d)
    return V


def meanings(book):
    """the Meaning box: docs/translation/meanings/<book>.jsonl, one row per article --
    {id, es, en, status_es, status_en, source} -> {article id: {'es': {x, s}, 'en': {x, s}}}.
    Only the Burmese explanation is translated; every row carries its status
    (drafted / reviewed / corrected), which the site shows beside the text."""
    f = ROOT / f'docs/translation/meanings/{book}.jsonl'
    out = {}
    if not f.exists(): return out
    for line in f.open(encoding='utf-8'):
        if not line.strip(): continue
        r = json.loads(line); t = {}
        for lang in ('es', 'en'):
            if r.get(lang): t[lang] = {'x': r[lang], 's': r.get(f'status_{lang}') or 'drafted'}
        if t: out[r['id']] = t
    return out


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', t)
    # Burmese script in the site's Burmese face
    return re.sub(r'[\u1000-\u109f](?:[\u1000-\u109f\s\-]*[\u1000-\u109f])?',
                  lambda m: f'<span class="my" lang="my">{m.group(0)}</span>', t)


def history_html(lang):
    """The History section of the About page, from docs/history.md (## English / ## Español,
    each running to the next ---), or '' while the file is a draft. A small Markdown subset:
    ### headings, paragraphs, '- ' lists, **bold**, *italics*, links."""
    f = ROOT / 'docs/history.md'
    if not f.exists(): return ''
    text = f.read_text(encoding='utf-8')
    publish = re.search(r'<!--\s*site:\s*publish\s*-->', text[:600]) is not None
    draft = not publish and os.environ.get('ABHIDHANA_SITE_DRAFTS') == '1'
    if not (publish or draft): return ''
    head = {'en': '## English', 'es': '## Español'}[lang]
    body = text.split(head, 1)[1].split('\n---', 1)[0]
    out = ['<h2 id="history">' + ('History' if lang == 'en' else 'Historia') + '</h2>']
    if draft:
        out.append('<p class="note"><strong>' + ('Draft, not published: the romanised names await review.'
                   if lang == 'en' else 'Borrador, no publicado: los nombres romanizados esperan revisión.') + '</strong></p>')
    out.append('<p class="note">' + ("Written from the dictionary's own front matter; page numbers are those of the PDFs."
               if lang == 'en' else 'Redactado a partir de las páginas preliminares del propio diccionario; los números de página son los de los PDF.') + '</p>')
    blocks, cur = [], []
    for line in body.strip('\n').split('\n'):
        if not line.strip():
            if cur: blocks.append(cur); cur = []
        elif line.startswith('### ') or (line.startswith('- ') and cur and not cur[-1].startswith('- ') and not cur[0].startswith('- ')):
            if cur: blocks.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur: blocks.append(cur)
    for b in blocks:
        if b[0].startswith('### '):
            out.append('<h3>' + md_inline(b[0][4:].strip()) + '</h3>')
            b = b[1:]
            if not b: continue
        if b[0].startswith('- '):
            items = []
            for ln in b:
                if ln.startswith('- '): items.append(ln[2:].strip())
                else: items[-1] += ' ' + ln.strip()
            out.append('<ul>' + ''.join('<li>' + md_inline(i) + '</li>' for i in items) + '</ul>')
        else:
            out.append('<p>' + md_inline(' '.join(ln.strip() for ln in b)) + '</p>')
    return '\n  '.join(out)


def main():
    vols = json.loads((ROOT / 'site/volumes.json').read_text(encoding='utf-8'))
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    about = OUT / 'about/index.html'
    a = about.read_text(encoding='utf-8')
    for lang in ('en', 'es'):
        a = a.replace(f'<!--HISTORY-{lang.upper()}-->', history_html(lang))
    about.write_text(a, encoding='utf-8')
    from abhidhana_intro import fill as intro_fill   # docs/introduction/ -> /introduction/
    ip = OUT / 'introduction/index.html'
    ip.write_text(intro_fill(ip.read_text(encoding='utf-8')), encoding='utf-8')
    (OUT / 'data').mkdir()
    search = []; lab_n = {}; book_records = {}
    for v in vols:
        b = v['id']
        if not ((ROOT / f'ocr/{b}/articles.jsonl').exists() and (ROOT / f'ocr/{b}/pali.jsonl').exists()):
            v['status'] = 'coming'; continue
        V = records(b); book_records[b] = V
        dump(OUT / f'data/v{b}.json', V)
        n = len(V)
        v.update(status='done', records=n, pages=len({d['p'] for d in V}),
                 located=round(100 * sum(d['x'] != 'u' for d in V) / n, 1),
                 usable=round(100 * sum(bool(d.get('l') and d.get('b')) for d in V) / n, 1))
        search += [[b, d['i'], d['p'], d['h'], d['r']] for d in V]
        for d in V:
            if d.get('l'): lab_n[d['l']] = lab_n.get(d['l'], 0) + 1
        print(f'{b:>3}: {n:,} records, {(OUT / f"data/v{b}.json").stat().st_size / 1e6:.1f} MB')
    dump(OUT / 'data/volumes.json', vols)
    from abhidhana_browse import build as browse_build   # the Browse page's data (nav, chunks, shards)
    browse_build(OUT, vols, book_records, dump)
    dump(OUT / 'data/search.json', search)
    labels = [{k: d.get(k, '') for k in ('label', 'roman', 'printed', 'pali', 'en', 'es', 'abbr_en', 'abbr_es',
                                         'status', 'es_status', 'source')}
              | {'n': lab_n.get(d['label'], 0)} for d in LABELS]
    dump(OUT / 'data/labels.json', labels)
    E = html.escape
    lrows = []
    for k, d in enumerate(labels):
        prov = lambda lang: '' if (d['status'] != 'provisional' and (lang == 'en' or d['es_status'] == 'confirmed')) else \
            '<span class="prov" data-i18n="provisional">provisional</span>'
        st = {'confirmed': ('confirmed', 'confirmada'), 'printed': ('printed in the dictionary', 'impresa en el diccionario'),
              'provisional': ('provisional', 'provisional')}[d['status']]
        lro = f'<div class="lro" lang="pi">{E(d["roman"])}</div>' if d.get('roman') else ''
        lrows.append(
            f'<tr id="l{k}"><td class="my" lang="my">({E(d["label"])}){lro}</td><td class="my" lang="my">{E(d["printed"])}</td>'
            f'<td lang="pi"><i>{E(d["pali"])}</i></td>'
            f'<td><span class="tr" lang="en">{E(d["en"])} {prov("en")}</span><span class="tr" lang="es">{E(d["es"])} {prov("es")}</span></td>'
            f'<td><span class="tr" lang="en">{E(d["abbr_en"])}</span><span class="tr" lang="es">{E(d["abbr_es"])}</span></td>'
            f'<td class="st"><span class="tr" lang="en">{st[0]}</span><span class="tr" lang="es">{st[1]}</span>'
            f'<div class="src">{E(d["source"])}</div></td>'
            f'<td class="num">{d["n"]:,}</td></tr>')
    from abhidhana_intro import abbreviations_html   # docs/introduction/citation-abbreviations.tsv
    lp = OUT / 'abbreviations/index.html'
    lp.write_text(lp.read_text(encoding='utf-8').replace('<!--LABELS-->', '\n'.join(lrows))
                  .replace('<!--ABBR-->', abbreviations_html()[0]), encoding='utf-8')
    if (OUT / 'labels').exists(): shutil.rmtree(OUT / 'labels')   # now part of /abbreviations/ (see _redirects)

    # the volume list, in the page itself (readable without JavaScript and by search engines)
    rows = []
    for v in vols:
        done = v['status'] == 'done'
        inner = (f'<span class="vn">{html.escape(v["n"])}</span><span class="rg">'
                 f'<span class="my" lang="my">{html.escape(v["range_my"])}</span>'
                 f'<span class="ro" lang="pi">{html.escape(v["range_ro"])}</span></span>')
        link = (f'<a class="vl" href="/v/{v["id"]}/{v["start"]}">{inner}</a>' if done
                else f'<span class="vl">{inner}</span>')
        stat = (f'<span class="num">{v["headwords"]:,}</span>'
                f'<span class="state {"done" if done else "coming"}" data-i18n="{"st_done" if done else "st_coming"}">'
                f'{"digitised" if done else "coming"}</span>')
        rows.append(f'<li class="vol{"" if done else " soon"}" data-id="{v["id"]}">{link}{stat}</li>')
    ix = OUT / 'volumes/index.html'
    ix.write_text(ix.read_text(encoding='utf-8').replace('<!--VOLUMES-->', '\n'.join(rows)), encoding='utf-8')

    files = [f for f in OUT.rglob('*') if f.is_file()]
    big = [f for f in files if f.stat().st_size > MAX_FILE]
    print(f'site/dist: {len(files)} files, {sum(f.stat().st_size for f in files) / 1e6:.0f} MB; '
          f'search {len(search):,} headwords; '
          f'{sum(v["status"] == "done" for v in vols)} books published, '
          f'{sum(v["status"] == "coming" for v in vols)} coming')
    if big or len(files) > MAX_FILES:
        sys.exit(f'over the Pages limits: {len(files)} files; too large: {[str(f) for f in big]}')


if __name__ == '__main__':
    main()
