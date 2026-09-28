#!/usr/bin/env python3
"""Tests for abhidhana_meanings.py merge (brief §65).

    python3 tools/test_meanings_merge.py                       the unit tests only (no working files needed)
    python3 tools/test_meanings_merge.py 18 tmp/meanings/v18   also: re-merge vol. 18 from its drafts, whole and
                                                               with --ids, into a scratch copy of the repository's
                                                               files; the result must equal the committed
                                                               meanings/18.jsonl byte for byte, corrected rows included

The drafts and work files (tmp/meanings/vNN) are gitignored: the second form runs where they are (the Mac, or a
session they were staged into). Nothing in docs/ is written.
"""
import json, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import abhidhana_meanings as M


def scratch(book):
    """a scratch root with the files merge reads and writes, copied from the repository"""
    d = Path(tempfile.mkdtemp(prefix='merge-test-'))
    (d / 'docs/translation/meanings').mkdir(parents=True)
    shutil.copy(ROOT / 'docs/translation/corrections-es.tsv', d / 'docs/translation/')
    for f in (ROOT / 'docs/translation/meanings').glob(f'{book}*'): shutil.copy(f, d / 'docs/translation/meanings/')
    return d


def unit():
    d = Path(tempfile.mkdtemp(prefix='merge-unit-'))
    (d / 'docs/translation').mkdir(parents=True)
    (d / 'docs/translation/corrections-es.tsv').write_text(
        'id\tbook\tiast\tes\tsenses\tby\tdate\tnote\n'
        '1\tzz\ta\tuno corregido.\twhole\tIEBH\t2026-09-27\tx\n'
        '2\tzz\tb\t(1) dos. (2) tres.\t1\tIEBH\t2026-09-27\tx\n'
        '3\tzz\tc\tigual.\twhole\tIEBH\t2026-09-27\tx\n'
        '9\tzz\tz\tsin fila.\twhole\tIEBH\t2026-09-27\tx\n'
        '1\tyy\ta\totro libro.\twhole\tIEBH\t2026-09-27\tx\n', encoding='utf-8')
    M.ROOT = d
    base = lambda i, es: {'id': i, 'iast': 'x', 'es': es, 'en': 'e', 'status_es': 'drafted', 'status_en': 'drafted',
                          'source': 'pced', 'method': 'draft'}
    rows = [base(1, 'uno.'), base(2, '(1) dos, borrador. (2) tres.'), base(3, 'igual.'), base(4, 'cuatro.')]
    out = M.corrected('zz', [dict(r) for r in rows])
    assert out[0]['es'] == 'uno corregido.' and out[0]['es_drafted'] == 'uno.' and out[0]['status_es'] == 'corrected'
    assert out[0]['corrected_es'] == {'by': 'IEBH', 'date': '2026-09-27'}
    assert out[1]['corrected_es']['senses'] == [1] and out[1]['es_drafted'] == '(1) dos, borrador. (2) tres.'
    assert 'es_drafted' not in out[2] and out[2]['status_es'] == 'corrected'   # the draft was already right
    assert out[3] == rows[3]                                                  # untouched
    again = M.corrected('zz', [dict(r) for r in out])                        # idempotent: the draft is kept
    assert again == out, 'corrected() is not idempotent'
    assert list(out[0]) == list(rows[0]) + ['es_drafted', 'corrected_es']      # the key order of §51's rows
    M.ROOT = ROOT
    print('unit: ok')


def real(book, work):
    committed = (ROOT / f'docs/translation/meanings/{book}.jsonl').read_bytes()
    C = [l.split('\t') for l in (ROOT / 'docs/translation/corrections-es.tsv').read_text(encoding='utf-8').splitlines()[1:]]
    cids = {int(c[0]) for c in C if c[1] == book}
    M.WORK = Path(work).resolve()
    for label, ids in (('whole', None), ('--ids', cids | {min(json.loads(l)['id'] for l in committed.decode().splitlines())})):
        d = scratch(book); M.ROOT = d
        M.merge(book, ids)
        got = (d / f'docs/translation/meanings/{book}.jsonl').read_bytes()
        rows = {r['id']: r for r in map(json.loads, got.decode().splitlines())}
        assert all(rows[i]['status_es'] == 'corrected' for i in cids), f'{book} {label}: a correction was dropped'
        assert got == committed, f'{book} {label}: re-merge differs from the committed file'
        print(f'{book} merge {label}: byte-identical to the committed file; {len(cids)} corrected rows kept')
        shutil.rmtree(d)
    M.ROOT = ROOT


if __name__ == '__main__':
    unit()
    if len(sys.argv) == 3: real(sys.argv[1], sys.argv[2])
