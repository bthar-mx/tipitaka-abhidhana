#!/usr/bin/env python3
"""Bring the editor's edits from the site's editor mode (docs/editor-mode.md) into the repository.

The edits live in the Cloudflare D1 database `edits` (site/d1/schema.sql), one row per save, the
latest per id + field + sense counting. This tool reads them and writes

    es, en, status        -> docs/translation/meanings/<book>.jsonl (the Meaning box), and every
                             Spanish correction also -> docs/translation/corrections-es.tsv, the record
                             a later `abhidhana_meanings.py merge` must re-apply (brief §51)
    headword, label,
    analysis, body        -> docs/corrections.tsv (applied by abhidhana_articles.py as its last step)

and lists the books whose article step must be re-run on the Mac (abhidhana_articles.py NN, then
abhidhana_romanise.py NN) for the corrections.tsv rows to reach ocr/<book>/. The Meaning rows need no
re-run: the site build reads them directly.

Input, one of:
    --api [URL]     the public read API, every book (default https://abhidhana.buddha-dhamma.net/api/edits?book=all)
    --d1 FILE       a D1 export: the .sql of `wrangler d1 export abhidhana-edits --remote --output FILE`,
                    or the .json of `wrangler d1 execute abhidhana-edits --remote --json
                    --command "SELECT rowid AS n, * FROM edits"`

    python3 tools/abhidhana_edits_export.py --d1 edits.sql            # what would change (nothing written)
    python3 tools/abhidhana_edits_export.py --d1 edits.sql --write    # write it

The Spanish status follows what the site shows (site/src/assets/browse.js ov()): a new Spanish text is
`corrected`; a status saved at the same time or later replaces that, for the whole Meaning or by sense.
Every row is written `by` IEBH. Running it twice changes nothing the second time. An edit whose `old`
(what the page showed) differs from the repository's text now is written anyway and reported.
Withdrawn edits (status `reverted`) are skipped; if one had been exported before, the repository keeps
it: the tool says so, and the line is removed by hand.
"""
import argparse, csv, io, json, sqlite3, sys, unicodedata, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = 'https://abhidhana.buddha-dhamma.net/api/edits?book=all'
ARTICLE_FIELDS = ('headword', 'label', 'analysis', 'body')
nfc = lambda s: unicodedata.normalize('NFC', s or '')


# --- reading ----------------------------------------------------------------------------------------
def rows_from_api(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        j = json.load(r)
    return j['edits'], 'latest'


def rows_from_d1(path):
    """every row of the table, in insertion order"""
    p = Path(path); text = p.read_text(encoding='utf-8')
    if p.suffix == '.json':
        j = json.loads(text)
        res = j[0]['results'] if isinstance(j, list) else j.get('results', j)
        return sorted(res, key=lambda r: (r.get('n') or 0, r['date'])), 'all'
    db = sqlite3.connect(':memory:'); db.executescript(text)
    cur = db.execute('SELECT rowid, id, book, field, sense, value, old, status, date FROM edits ORDER BY rowid')
    keys = ['n', 'id', 'book', 'field', 'sense', 'value', 'old', 'status', 'date']
    return [dict(zip(keys, r)) for r in cur], 'all'


def latest(rows, kind):
    """-> (the latest saved row per id + field + sense, the keys whose latest row is a withdrawal)"""
    if kind == 'latest': return [r for r in rows if r.get('status', 'saved') != 'reverted'], []
    last, first = {}, {}
    for r in rows:
        k = (r['id'], r['field'], r['sense'] or '')
        if r['status'] == 'reverted' or k not in first: first[k] = r['old']   # a field edited twice: what the page
        last[k] = dict(r, old=first[k])                                       # showed before the first save counts
    keep = [r for r in last.values() if r['status'] != 'reverted']
    gone = [r for r in last.values() if r['status'] == 'reverted']
    return sorted(keep, key=lambda r: (r['book'], r['id'], r['field'], r['sense'] or '')), gone


# --- the Spanish status, as the site computes it -------------------------------------------------------
def es_status(E):
    """E: an article's latest rows. -> (status, senses, date) for the Spanish, or None if nothing to say"""
    text = next((e for e in E if e['field'] == 'es'), None)
    st = [e for e in E if e['field'] == 'status']
    out = ('corrected', [], text['date']) if text else None
    whole = max((e for e in st if not e['sense']), key=lambda e: e['date'], default=None)
    base = whole if whole and (not text or whole['date'] >= text['date']) else None
    if base: out = (base['value'], [], base['date'])
    since = base['date'] if base else (text['date'] if text else '')
    per = [e for e in st if e['sense'] and e['date'] >= since]
    senses = lambda v: sorted({int(x) for e in per if e['value'] == v for x in e['sense'].split(',')})
    corr, rev = senses('corrected'), senses('reviewed')
    last = max((e['date'] for e in per), default='')
    if corr: out = ('corrected', corr, last)
    elif rev and (out is None or out[0] == 'drafted'): out = ('reviewed', rev, last)
    return out


# --- writing ----------------------------------------------------------------------------------------
def read_jsonl(f):
    return [json.loads(l) for l in f.open(encoding='utf-8') if l.strip()] if f.exists() else []


def article_rows(book):
    f = ROOT / f'ocr/{book}/articles.jsonl'
    return {r['id']: r for r in read_jsonl(f)}


def headword_iast(book, i):
    for r in read_jsonl(ROOT / f'ocr/{book}/pali.jsonl'):
        if r['id'] == i: return r.get('headword_iast', '')
    return ''


def meanings(book, E_by_id, report):
    """apply es / en / status to docs/translation/meanings/<book>.jsonl; returns (lines, changed ids, es corrections)"""
    f = ROOT / f'docs/translation/meanings/{book}.jsonl'
    rows = read_jsonl(f); by = {r['id']: r for r in rows}
    changed, es_corr = [], []
    for i, E in sorted(E_by_id.items()):
        if not any(e['field'] in ('es', 'en', 'status') for e in E): continue
        r = by.get(i)
        before = json.dumps(r, ensure_ascii=False, sort_keys=True) if r else None
        if r is None:
            if not any(e['field'] == 'es' or e['field'] == 'en' for e in E):
                report.append(f'{book} {i}: a status for a row with no Meaning; skipped'); continue
            r = {'id': i, 'iast': headword_iast(book, i), 'source': 'editor', 'method': 'editor'}
            rows.append(r); by[i] = r
        for lang in ('es', 'en'):
            e = next((x for x in E if x['field'] == lang), None)
            if not e: continue
            if nfc(e['old']) and nfc(e['old']) != nfc(r.get(lang)):
                report.append(f'{book} {i} {lang}: the page showed {e["old"]!r}, the repository has {r.get(lang)!r}; written anyway')
            if r.get(lang) != e['value']:
                if r.get(lang) and f'{lang}_drafted' not in r and (r.get(f'status_{lang}') or 'drafted') == 'drafted':
                    r[f'{lang}_drafted'] = r[lang]   # the draft is kept beside the correction, as in brief §51
                r[lang] = e['value']
            if lang == 'en':
                r['status_en'] = 'corrected'; r['corrected_en'] = {'by': 'IEBH', 'date': e['date'][:10]}
        s = es_status(E)
        if s and 'es' in r:
            st, senses, date = s
            r['status_es'] = st
            for k in ('corrected', 'reviewed'):
                if k != st: r.pop(f'{k}_es', None)
            if st in ('corrected', 'reviewed'):
                r[f'{st}_es'] = {'by': 'IEBH', 'date': date[:10]} | ({'senses': senses} if senses else {})
            if st == 'corrected': es_corr.append((i, r, senses, date[:10]))
        if json.dumps(r, ensure_ascii=False, sort_keys=True) != before: changed.append(i)
    return ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), changed, es_corr


def tsv_rows(f):
    if not f.exists(): return None, []
    with f.open(encoding='utf-8', newline='') as h:
        rd = csv.DictReader(h, delimiter='\t')
        return rd.fieldnames, list(rd)


def tsv_text(head, rows):
    out = io.StringIO()
    w = csv.DictWriter(out, head, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')
    w.writeheader(); w.writerows(rows)
    return out.getvalue()


def main():
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--api', nargs='?', const=API, help='read the public API (default: the live site)')
    src.add_argument('--d1', help='a D1 export (.sql or .json)')
    ap.add_argument('--write', action='store_true', help='write the files (default: only report)')
    ap.add_argument('--root', help='the repository to write into (default: this one); for tests')
    a = ap.parse_args()
    if a.root: ROOT = Path(a.root).resolve()
    rows, kind = rows_from_api(a.api) if a.api else rows_from_d1(a.d1)
    keep, gone = latest(rows, kind)
    for r in keep: r['sense'] = r['sense'] or ''
    report = []
    books = {}
    for r in keep: books.setdefault(r['book'], {}).setdefault(r['id'], []).append(r)
    print(f'{len(rows)} rows read ({"every save" if kind == "all" else "latest per id + field + sense"}); '
          f'{len(keep)} edits in force in {len(books)} book(s); {len(gone)} withdrawn')

    # the article fields -> docs/corrections.tsv
    cf = ROOT / 'docs/corrections.tsv'
    head, crows = tsv_rows(cf)
    at = {(int(c['id']), c['field']): c for c in crows}
    rerun, n_art = set(), 0
    for book, E_by_id in sorted(books.items()):
        arts = None
        for i, E in sorted(E_by_id.items()):
            for e in E:
                if e['field'] not in ARTICLE_FIELDS: continue
                if arts is None: arts = article_rows(book)
                art = arts.get(i)
                if art is None: report.append(f'{book} {i}: no such article; {e["field"]} skipped'); continue
                now = art.get(e['field']) or ''
                ocr = (art.get('corrected') or {}).get(e['field'], {}).get('ocr', now)
                if nfc(e['old']) and nfc(e['old']) != nfc(now):
                    report.append(f'{book} {i} {e["field"]}: the page showed {e["old"]!r}, the repository has {now!r}; written anyway')
                note = f'{art.get("iast") or headword_iast(book, i)}, PDF p. {art.get("pdf_page")}: editor mode, {e["date"][:10]}'
                c = at.get((i, e['field']))
                if c and c['value'] == e['value']: continue
                if c: c.update(value=e['value'], by='IEBH', date=e['date'][:10], note=note)
                else:
                    c = {'id': str(i), 'book': book, 'field': e['field'], 'value': e['value'], 'ocr': ocr,
                         'by': 'IEBH', 'date': e['date'][:10], 'note': note}
                    crows.append(c); at[(i, e['field'])] = c
                rerun.add(book); n_art += 1
                print(f'  corrections.tsv  {book} {i} {e["field"]}: {now!r} -> {e["value"]!r}')

    # the Meaning -> docs/translation/meanings/<book>.jsonl and corrections-es.tsv
    ef = ROOT / 'docs/translation/corrections-es.tsv'
    ehead, erows = tsv_rows(ef)
    eat = {int(c['id']): c for c in erows}
    out, n_mean, n_es = {}, 0, 0
    for book, E_by_id in sorted(books.items()):
        text, changed, es_corr = meanings(book, E_by_id, report)
        if changed:
            out[book] = text; n_mean += len(changed)
            print(f'  meanings/{book}.jsonl: {len(changed)} row(s): {", ".join(map(str, changed[:20]))}{" …" if len(changed) > 20 else ""}')
        for i, r, senses, date in es_corr:
            want = {'id': str(i), 'book': book, 'iast': r.get('iast', ''), 'es': r['es'],
                    'senses': ','.join(map(str, senses)) or 'whole', 'by': 'IEBH', 'date': date, 'note': 'editor mode'}
            c = eat.get(i)
            if c and all(c.get(k) == want[k] for k in ('es', 'senses')): continue
            if c: want['note'] = (c.get('note') or '') + ('; ' if c.get('note') else '') + f'editor mode {date}'; c.update(want)
            else: erows.append(want); eat[i] = want
            n_es += 1

    for w in gone:
        report.append(f'{w["book"]} {w["id"]} {w["field"]}{" sense " + w["sense"] if w.get("sense") else ""}: '
                      'withdrawn in editor mode; if it was exported before, remove it from the repository by hand')
    for m in report: print('  note:', m)
    print(f'{n_art} correction(s) to docs/corrections.tsv, {n_mean} Meaning row(s), {n_es} line(s) to corrections-es.tsv')
    if rerun:
        print('On the Mac, for the corrections to reach the articles, re-run in this order:')
        for b in sorted(rerun): print(f'  python3 tools/abhidhana_articles.py {b} && python3 tools/abhidhana_romanise.py {b}')
    else:
        print('No article step to re-run.')
    if not a.write:
        print('(nothing written: add --write)'); return
    if not (n_art or n_es or out):
        print('nothing to write.'); return
    if n_art: cf.write_text(tsv_text(head, crows), encoding='utf-8')
    if n_es: ef.write_text(tsv_text(ehead, erows), encoding='utf-8')
    for book, text in out.items(): (ROOT / f'docs/translation/meanings/{book}.jsonl').write_text(text, encoding='utf-8')
    if n_art:
        sys.path.insert(0, str(ROOT / 'tools'))
        import abhidhana_corrections as C
        C.FILE = cf; C.load()   # the file still passes the pipeline's own check
    print('written.')


if __name__ == '__main__':
    main()
