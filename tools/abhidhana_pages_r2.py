#!/usr/bin/env python3
"""Page images for the website: render every PDF page to WebP and upload them to Cloudflare R2.

    python3 tools/abhidhana_pages_r2.py render 01 02 ...      # PDF pages -> release/pages-webp/<book>/NNNN.webp
    python3 tools/abhidhana_pages_r2.py check  01 02 ...      # compare a sample against a plain render
    python3 tools/abhidhana_pages_r2.py upload 01 02 ...      # to the bucket, as <book>/NNNN.webp
    python3 tools/abhidhana_pages_r2.py all                   # every book in site/volumes.json: render, upload
    options: --workers N (default 8), --first P --last P, --force (redo pages already done)

The site shows https://abhidhana-img.buddha-dhamma.net/<book>/<NNNN>.webp beside the articles of
PDF page NNNN (zero-padded to four digits, as in ocr/<book>/pages/).

Format (measured 25 Sep 2026 on vols. 1, 3, 13, 4/3, 23 and 24; brief §28). The scans are 1-bit,
69-96 ppi on ~2,000 x 3,000 px pages (vol. 23: 323 ppi, 2,577 px wide). Each page's own bitmap
is taken out of the PDF unchanged (pdfimages) and stored as **lossless WebP at its native size**:
about 96 KB a page, against ~210 KB for a 1,200 px lossy WebP and ~300 KB at 1,600 px, and
nothing of the print is lost, so the smallest stacked marks read as in the scan. Pages that are
not a single 1-bit image (covers, front matter in colour or grey, and all of book 14b, which is
typeset text) are rendered with pdftoppm (grey, or colour when the page is in colour) at up to
1,800 px wide and stored as lossy WebP, quality 80.

Needs, on the Mac: poppler (pdfimages, pdftoppm, pdfinfo: `brew install poppler`, already there
for the OCR), and Python with Pillow and boto3: `python3 -m pip install --user pillow boto3`.

Upload needs an R2 API token (Object Read & Write on the bucket), read from the environment or
from ~/.config/abhidhana-r2.env (KEY=value lines, chmod 600, never in the repo):
    R2_ACCOUNT_ID=...          the Cloudflare account id
    R2_ACCESS_KEY_ID=...       from the token
    R2_SECRET_ACCESS_KEY=...   from the token (shown once)
    R2_BUCKET=abhidhana-pages  optional
Upload skips objects already in the bucket with the same size, so it can be re-run at any time.
"""
import argparse, io, json, os, random, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(os.environ.get('ABHIDHANA_WEBP', ROOT / 'release/pages-webp'))   # release/ is gitignored
CACHE = 'public, max-age=2592000'    # 30 days; the names never change, but a page may be re-rendered
MAX_W = 1800                          # for pages that have to be rendered


def run(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, check=True).stdout


def pdf_pages(pdf):
    return int(re.search(r'Pages:\s+(\d+)', run('pdfinfo', pdf)).group(1))


def page_info(pdf, p):
    """(width pt, height pt, rotation) of page p"""
    s = run('pdfinfo', '-f', p, '-l', p, pdf)
    w, h = map(float, re.search(rf'Page\s+{p} size:\s+([\d.]+) x ([\d.]+)', s).groups())
    rot = int(re.search(rf'Page\s+{p} rot:\s+(\d+)', s).group(1))
    return w, h, rot


def images(pdf, p):
    """the page's images from pdfimages -list: [(width, height, color, comp, bpc, x-ppi, y-ppi)]"""
    rows = []
    for line in run('pdfimages', '-list', '-f', p, '-l', p, pdf).splitlines()[2:]:
        f = line.split()
        if len(f) > 13 and f[2] == 'image':
            rows.append((int(f[3]), int(f[4]), f[5], int(f[6]), int(f[7]), float(f[12]), float(f[13])))
    return rows


def bilevel_bitmap(imgs, pw, ph):
    """True when the page is one 1-bit image, placed undistorted (x-ppi = y-ppi within 3%) and
    covering at least 85% of the page each way. Such a bitmap is the whole scan, stored as is.
    (Until 25 Sep 2026 the test was the bitmap's aspect ratio against the page's, within 0.03; it
    sent ~3,500 pages whose scan sits in a page box with a blank margin, e.g. vol. 1 p. 500,
    2051 x 3002 px at 73 ppi on a 3,142 pt page, to the lossy render, at ~4x the size.
    Measured over all 29 books: the new test accepts every page the old one did.)"""
    if len(imgs) != 1 or imgs[0][3] != 1 or imgs[0][4] != 1: return False
    w, h, _, _, _, xp, yp = imgs[0]
    if xp <= 0 or yp <= 0 or abs(xp - yp) / max(xp, yp) > 0.03: return False
    cw, ch = w / xp * 72 / pw, h / yp * 72 / ph
    return min(cw, ch) >= 0.85 and max(cw, ch) <= 1.03


def render_page(args):
    """one page to WebP; returns (page, kind, bytes) or (page, 'error: ...', 0)"""
    book, p, force = args
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    pdf = ROOT / f'pdfs/{book}.pdf'
    out = OUT / book / f'{p:04d}.webp'
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        pw, ph, rot = page_info(pdf, p)
        if rot in (90, 270): pw, ph = ph, pw
        imgs = images(pdf, p)
        bilevel = bilevel_bitmap(imgs, pw, ph)
        if out.exists() and not force:
            # keep a page already done, unless it was rendered where the bitmap should be stored
            # (the old test): then its width is MAX_W or less and not the bitmap's
            bw, bh = imgs[0][:2] if bilevel else (0, 0)
            if rot in (90, 270): bw, bh = bh, bw
            if not bilevel or Image.open(out).width == bw:
                return p, 'kept', out.stat().st_size
        im, kind = None, None
        with tempfile.TemporaryDirectory() as td:
            if bilevel:
                run('pdfimages', '-png', '-f', p, '-l', p, pdf, f'{td}/x')
                src = Image.open(next(Path(td).glob('x-*.png'))).convert('1')
                if rot: src = src.rotate(-rot, expand=True)
                im, kind = src, 'bilevel'
            if im is None:
                dpi = min(300, max(72, round(MAX_W / (pw / 72))))
                colour = any(c[2] not in ('gray', 'index') or c[3] > 1 for c in imgs)
                run('pdftoppm', '-png', '-r', dpi, *([] if colour else ['-gray']), '-f', p, '-l', p,
                    '-singlefile', pdf, f'{td}/r')
                im = Image.open(f'{td}/r.png'); im.load()
                if im.width > MAX_W: im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
                kind = 'rendered'
        b = io.BytesIO()
        if kind == 'bilevel':
            im.convert('L').save(b, 'WEBP', lossless=True, quality=80, method=4)
        else:
            im.save(b, 'WEBP', quality=80, method=4)
        tmp = out.with_suffix('.part'); tmp.write_bytes(b.getvalue()); tmp.replace(out)
        return p, kind, len(b.getvalue())
    except Exception as e:
        return p, f'error: {e}', 0


def pages_of(book, a):
    n = pdf_pages(ROOT / f'pdfs/{book}.pdf')
    return range(max(1, a.first), min(n, a.last or n) + 1)


def cmd_render(books, a):
    for book in books:
        todo = [(book, p, a.force) for p in pages_of(book, a)]
        t0 = time.time(); kinds = {}; total = 0; errors = []
        with ProcessPoolExecutor(a.workers) as ex:
            for k, (p, kind, size) in enumerate(ex.map(render_page, todo, chunksize=4), 1):
                if kind.startswith('error'): errors.append((p, kind))
                else: kinds[kind] = kinds.get(kind, 0) + 1; total += size
                if k % 100 == 0: print(f'  {book}: {k}/{len(todo)} pages, {time.time() - t0:.0f} s', flush=True)
        print(f'{book}: {len(todo)} pages in {time.time() - t0:.0f} s; {kinds}; '
              f'{total / 1e6:.1f} MB, {total / max(1, sum(kinds.values())) / 1024:.0f} KB a page')
        for p, e in errors: print(f'  p. {p}: {e}')


def correlation(a, b):
    """Pearson correlation of two greyscale images of the same size"""
    x, y = a.tobytes(), b.tobytes(); n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((u - mx) * (v - my) for u, v in zip(x, y))
    sx = sum((u - mx) ** 2 for u in x) ** .5; sy = sum((v - my) ** 2 for v in y) ** .5
    return sxy / (sx * sy) if sx and sy else 0.0


def cmd_check(books, a):
    """render a sample plainly and compare with the stored WebP: catches a bitmap stored rotated,
    flipped or cropped differently from the page. Both at 300 px wide, blurred, compared by
    correlation at the best offset (a stored bitmap may sit inside a larger page box).
    Measured 25 Sep 2026 on vol. 1: right pages 0.95-0.98; the same pages flipped 0.53, rotated
    0.35. (The mean difference used before scored a right page ~21 and a flipped one 32.5, under
    its threshold of 35: it could not see a flip.) Pages under 0.80 are flagged."""
    from PIL import Image, ImageFilter
    for book in books:
        pdf = ROOT / f'pdfs/{book}.pdf'; ps = list(pages_of(book, a))
        bad = 0
        for p in sorted(random.Random(book).sample(ps, min(12, len(ps)))):
            f = OUT / book / f'{p:04d}.webp'
            if not f.exists(): print(f'  {book} p. {p}: not rendered'); continue
            with tempfile.TemporaryDirectory() as td:
                run('pdftoppm', '-png', '-gray', '-scale-to-x', 300, '-scale-to-y', -1, '-f', p, '-l', p, '-singlefile', pdf, f'{td}/c')
                ref = Image.open(f'{td}/c.png').convert('L')
            got = Image.open(f).convert('L')
            # a stored bitmap may be smaller than the page box (a blank margin, see
            # bilevel_bitmap): scale it as the PDF does and find where it sits on the page
            pw, ph, rot = page_info(pdf, p)
            if rot in (90, 270): pw, ph = ph, pw
            imgs = images(pdf, p)
            if bilevel_bitmap(imgs, pw, ph):
                xp = imgs[0][5]
                sw = max(1, min(ref.width, round(got.width / xp * 72 / pw * ref.width)))
                sh = max(1, min(ref.height, round(got.height / xp * 72 / ph * ref.height)))
            else:
                sw, sh = ref.size
            blur = ImageFilter.GaussianBlur(2)
            got = got.resize((sw, sh), Image.BOX).filter(blur)
            r = max(correlation(ref.crop((x, y, x + sw, y + sh)).filter(blur), got)
                    for x in range(0, ref.width - sw + 1, 3) for y in range(0, ref.height - sh + 1, 3))
            flag = '  <-- look at this page' if r < 0.80 else ''
            bad += bool(flag)
            print(f'  {book} p. {p}: correlation {r:.3f}{flag}')
        print(f'{book}: {bad} page(s) to look at')


def r2():
    cfg = Path.home() / '.config/abhidhana-r2.env'
    env = dict(os.environ)
    if cfg.exists():
        for line in cfg.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1); env.setdefault(k.strip(), v.strip().strip('"\''))
    miss = [k for k in ('R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY') if not env.get(k)]
    if miss: sys.exit(f'missing {", ".join(miss)}: set them in ~/.config/abhidhana-r2.env (see the header)')
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', endpoint_url=f'https://{env["R2_ACCOUNT_ID"]}.r2.cloudflarestorage.com',
                      aws_access_key_id=env['R2_ACCESS_KEY_ID'], aws_secret_access_key=env['R2_SECRET_ACCESS_KEY'],
                      region_name='auto', config=Config(retries={'max_attempts': 8, 'mode': 'adaptive'}))
    return s3, env.get('R2_BUCKET', 'abhidhana-pages')


def cmd_upload(books, a):
    s3, bucket = r2()
    for book in books:
        have = {}
        for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=f'{book}/'):
            for o in page.get('Contents', []): have[o['Key']] = o['Size']
        files = sorted((OUT / book).glob('*.webp'))
        if a.first or a.last:
            files = [f for f in files if (a.first or 0) <= int(f.stem) <= (a.last or 10 ** 6)]
        todo = [f for f in files if a.force or have.get(f'{book}/{f.name}') != f.stat().st_size]
        t0 = time.time()

        def put(f):
            s3.put_object(Bucket=bucket, Key=f'{book}/{f.name}', Body=f.read_bytes(),
                          ContentType='image/webp', CacheControl=CACHE)
            return f.stat().st_size
        with ThreadPoolExecutor(a.workers) as ex:
            sent = sum(ex.map(put, todo))
        print(f'{book}: {len(files)} images, {len(files) - len(todo)} already in {bucket}, '
              f'{len(todo)} uploaded ({sent / 1e6:.1f} MB) in {time.time() - t0:.0f} s')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('cmd', choices=['render', 'check', 'upload', 'all'])
    ap.add_argument('books', nargs='*')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--first', type=int, default=0)
    ap.add_argument('--last', type=int, default=0)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    books = a.books or [v['id'] for v in json.loads((ROOT / 'site/volumes.json').read_text())]
    for b in books:
        if not (ROOT / f'pdfs/{b}.pdf').exists(): sys.exit(f'no pdfs/{b}.pdf (tools/fetch_sources.sh fetches them)')
    if a.cmd in ('render', 'all'): cmd_render(books, a)
    if a.cmd == 'check': cmd_check(books, a)
    if a.cmd in ('upload', 'all'): cmd_upload(books, a)


if __name__ == '__main__':
    main()
