// Round trip of the editor's roman input (brief §53): every headword and every PCED analysis without a
// derivation, romanised with roman.js (segment) and converted back with ROMAN.burmese, against the
// original Burmese. Prints the match rates and the failures by kind; --list KIND prints that kind's cases;
// --tsv FILE writes every failure.   node site/test/roman/roundtrip.js [--list KIND] [--tsv FILE]
'use strict';
const fs = require('fs'), path = require('path');
const REPO = path.resolve(__dirname, '../../..');
const R = require(path.join(REPO, 'site/src/assets/roman.js'));
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };

const norm = s => (s || '').normalize('NFC').replace(/\s+/g, ' ').trim();
// the kind of a failure: the first rule that explains the difference
function kind(b, back) {
  const has = (re, s) => re.test(s);
  if (/[^က-႟\s+\-()\[\]၊။]/.test(b)) return 'characters outside Burmese (Latin digits, comma, ¿, quotes, _)';
  if (has(/[း့ဲ၌၍၎၏]|ို|်(?!္)/, b)) return 'Burmese spelling (်, း, ့, ဲ, ို): prose, not Pāḷi';
  if (/([ါ-ူေဲံ])\1|[ဣဤဥဦဧဩ][ါ-ူေ]|[ါ-ူ][ါ-ူ]|္[ါ-ူ]/.test(b.replace(/ော|ေါ|ို|ုံ/g, '').replace(/ဥုံ/g, '')) || /ေော|ေေ/.test(b))
    return 'malformed OCR (doubled or stray vowel signs)';
  if (b.replace(/ါ/g, 'ာ') === back.replace(/ါ/g, 'ာ')) return 'ā/ါ (tall ā)';
  if (b.replace(/ဿ/g, 'သ္သ') === back.replace(/ဿ/g, 'သ္သ')) return 'ss/ဿ';
  if (b.replace(/ည/g, 'ဉ္ဉ') === back.replace(/ည/g, 'ဉ္ဉ')) return 'ññ/ည';
  if (/င်္|င္/.test(b + back) && b.replace(/င်္/g, 'င္') === back.replace(/င်္/g, 'င္')) return 'ṅ before a stacked letter (kinzi)';
  if (/ရ်္|ရ္/.test(b + back) && b.replace(/ရ်္/g, 'ရ္') === back.replace(/ရ်္/g, 'ရ္')) return 'r before a stacked letter (repha)';
  const med = s => s.replace(/္ယ/g, 'ျ').replace(/္ရ/g, 'ြ').replace(/္ဝ/g, 'ွ').replace(/္ဟ/g, 'ှ');
  if (med(b) === med(back)) return 'stacked y r v h (္ယ for ျ …)';
  if (/[ျြွှ]{2}/.test(b) && [...b].sort().join('') === [...back].sort().join('')) return 'order of medials';
  if (/ဥ|ဦ|ဣ|ဤ|ဧ|ဩ|အ/.test(b) && /^[က-႟]/.test(b)) {
    const ind = s => s.replace(/ဦ/g, 'ဥူ');
    if (ind(b) === ind(back)) return 'independent vowels (ဦ / ဥူ)';
  }
  if (/[ံ]/.test(b + back)) return 'ṁ/ံ';
  if (/[ျြွှ]/.test(b)) return 'medials (other)';
  if (/[၀-၉]/.test(b)) return 'digits';
  if (/္/.test(b)) return 'stacked consonants (other)';
  return 'other';
}

const rows = { headword: [], analysis: [] };
for (const book of fs.readdirSync(path.join(REPO, 'ocr')).sort()) {
  const af = path.join(REPO, 'ocr', book, 'articles.jsonl'), pf = path.join(REPO, 'ocr', book, 'pali.jsonl');
  if (!fs.existsSync(af)) continue;
  const deriv = new Set();
  if (fs.existsSync(pf)) for (const l of fs.readFileSync(pf, 'utf8').split('\n')) if (l) { const r = JSON.parse(l); if (r.analysis_derivation) deriv.add(r.id); }
  for (const l of fs.readFileSync(af, 'utf8').split('\n')) {
    if (!l) continue;
    const r = JSON.parse(l);
    if (r.headword) rows.headword.push({ id: r.id, book, b: r.headword });
    if (r.analysis && r.analysis_source === 'pced' && !deriv.has(r.id)) rows.analysis.push({ id: r.id, book, b: r.analysis });
  }
}
const fails = [];
for (const [f, list] of Object.entries(rows)) {
  let ok = 0; const kinds = {}; const uniq = new Map();
  for (const x of list) {
    const b = norm(x.b), roman = R.segment(b), back = R.burmese(roman), readback = R.segment(back);
    const good = back === b;
    if (good) ok++;
    else { const k = kind(b, back); kinds[k] = (kinds[k] || 0) + 1; fails.push({ field: f, ...x, b, roman, back, readback, k, caught: readback !== R.canon(roman) }); }
    uniq.set(b, good);
  }
  const uok = [...uniq.values()].filter(Boolean).length;
  console.log(`${f}: ${ok} of ${list.length} rows (${(100 * ok / list.length).toFixed(2)}%); distinct ${uok} of ${uniq.size} (${(100 * uok / uniq.size).toFixed(2)}%)`);
  for (const [k, n] of Object.entries(kinds).sort((a, b) => b[1] - a[1])) console.log(`  ${String(n).padStart(6)}  ${k}`);
}
const silent = fails.filter(x => !x.caught);
console.log(`failures whose read-back equals the roman (not caught by the save check): ${silent.length}`);
const L = arg('--list');
if (L) for (const x of fails.filter(x => x.k === L || (L === 'silent' && !x.caught))) console.log([x.field, x.book, x.id, x.b, x.roman, x.back].join('\t'));
const T = arg('--tsv');
if (T) fs.writeFileSync(T, 'field\tbook\tid\tburmese\troman\tback\treadback\tkind\tcaught\n' +
  fails.map(x => [x.field, x.book, x.id, x.b, x.roman, x.back, x.readback, x.k, x.caught ? 'yes' : 'no'].join('\t')).join('\n') + '\n');
