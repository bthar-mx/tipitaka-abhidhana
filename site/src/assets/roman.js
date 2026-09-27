// Burmese script -> IAST, for the editor's live preview (edit mode only; the published romanisation
// is made by tools/abhidhana_romanise.py with Aksharamukha). A port of what Aksharamukha does for
// Burmese -> IAST, with ṃ written ṁ as the pipeline writes it; measured against Aksharamukha on the
// tokens of every headword and analysis and a sample of the bodies (brief §52).
'use strict';
const ROMAN = (function () {
  const C = { 'က': 'k', 'ခ': 'kh', 'ဂ': 'g', 'ဃ': 'gh', 'င': 'ṅ', 'စ': 'c', 'ဆ': 'ch', 'ဇ': 'j', 'ဈ': 'jh', 'ဉ': 'ñ', 'ည': 'ññ',
    'ဋ': 'ṭ', 'ဌ': 'ṭh', 'ဍ': 'ḍ', 'ဎ': 'ḍh', 'ဏ': 'ṇ', 'တ': 't', 'ထ': 'th', 'ဒ': 'd', 'ဓ': 'dh', 'န': 'n', 'ပ': 'p', 'ဖ': 'ph',
    'ဗ': 'b', 'ဘ': 'bh', 'မ': 'm', 'ယ': 'y', 'ရ': 'r', 'လ': 'l', 'ဝ': 'v', 'သ': 's', 'ဟ': 'h', 'ဠ': 'l̤', 'အ': '', 'ဿ': 'ss' };
  const IV = { 'ဣ': 'i', 'ဤ': 'ī', 'ဥ': 'u', 'ဦ': 'ū', 'ဧ': 'e', 'ဩ': 'o', 'ဪ': 'au' };
  const DV = { 'ာ': 'ā', 'ါ': 'ā', 'ိ': 'i', 'ီ': 'ī', 'ု': 'u', 'ူ': 'ū', 'ေ': 'e', 'ဲ': 'ai' };
  const MED = { 'ျ': 'y', 'ြ': 'r', 'ွ': 'v', 'ှ': 'h' };
  const DIG = '၀၁၂၃၄၅၆၇၈၉';
  const ASP = new Set(['k', 'g', 'c', 'j', 'ṭ', 'ḍ', 't', 'd', 'p', 'b']);   // ှ after these is written _h (k_ha, not kha)
  // one run of Burmese letters (a token) -> IAST, following Aksharamukha's quirks where the OCR
  // produces them (အ + vowel sign: ao, au; ့ as ˳; a vowel sign after ်: _ā; ော် as au; aï, aü)
  function token(s) {
    if (s === 'ဥုံ') return 'oṁ';
    let out = '', pend = false, meds = [], base = '', isA = false, killed = false, dot = false;
    const flushMeds = () => {
      if (!meds.length) return;
      for (const m of ['ှ', 'ွ', 'ျ', 'ြ']) if (meds.includes(m)) out += m === 'ှ' && ASP.has(base) ? '_h' : MED[m];
      meds = [];
    };
    const flushA = () => { flushMeds(); if (pend) { out += 'a'; pend = false; } if (dot) { out += '˳'; dot = false; } };
    const vowel = v => {
      flushMeds();
      if (isA && pend) out += v === 'ā' || v === 'ai' ? v : 'a' + v;
      else if (killed && !pend) out += '_' + v;
      else out += v;
      pend = false; isA = false; killed = false;
    };
    for (let i = 0; i < s.length; i++) {
      const ch = s[i], nx = s[i + 1];
      if (ch in C) { flushA(); out += (ch === 'ဟ' && killed && ASP.has(base) ? '_' : '') + C[ch]; pend = true; base = C[ch]; isA = ch === 'အ'; killed = false; }
      else if (ch === 'ဥ' && (nx === '်' || nx === '္' || nx === 'ှ')) {   // ဥ written for ဉ (OCR): ŭ
        flushA(); out += 'ŭ'; i++; killed = false; if (nx === 'ှ') { out += 'h'; pend = true; base = 'h'; } }
      else if (ch in IV) { flushA(); out += /a$/.test(out) && (ch === 'ဣ' || ch === 'ဥ') ? (ch === 'ဣ' ? 'ï' : 'ü') : IV[ch]; isA = false; killed = false; }
      else if (ch in MED) meds.push(ch);
      else if (ch === '္') { flushMeds(); pend = false; }
      else if (ch === '်') { flushMeds(); if (!pend && /o$/.test(out) && s[i - 1] !== '္') out = out.slice(0, -1) + 'au'; pend = false; killed = true; if (dot) { out += '˳'; dot = false; } }
      else if (ch === 'ေ' && (nx === 'ာ' || nx === 'ါ')) { vowel('o'); i++; }
      else if (ch in DV) vowel(DV[ch]);
      else if (ch === 'ံ') { flushA(); out += 'ṁ'; }
      else if (ch === 'း') { flushA(); out += 'ḥ'; }
      else if (ch === '့') { flushMeds(); if (pend) dot = true; else out += '˳'; }
      else if (DIG.includes(ch)) { flushA(); out += DIG.indexOf(ch); }
      else { flushA(); out += ch; killed = false; }
    }
    flushA();
    return out;
  }
  const TOK = /([က-၉၌-႟္]+)/;
  // a stretch of text as tools/abhidhana_romanise.py's romanise_segment: Burmese runs romanised, ၊ ။ as , .
  function segment(s) {
    return s.split(TOK).map((p, k) => k % 2 ? token(p) : p.replace(/၊/g, ',').replace(/။/g, '.'))
      .join('').replace(/\s+/g, ' ').trim();
  }
  const NOT_PALI = /[း့ဲ၌၍၎၏]|ို|်(?!္)/;
  const paliShaped = t => !NOT_PALI.test(t) && !/^[ါ-ှ]/.test(t);
  // the headword as the pipeline romanises it (digits and spaces dropped)
  const headword = h => token((h || '').replace(/[၀-၉\s]/g, ''));
  // the analysis as tools/abhidhana_romanise.py's analysis_fields: when every ။-sentence is a formula
  // (Pāḷi elements joined by +) or a note after one, the formulas in roman, a wholly Pāḷi note in roman
  // (the pipeline also turns its references into "abbr 1.23"; the preview does not), a note with
  // Burmese prose left out; otherwise the whole analysis split on + (Burmese-shaped parts kept as ⟨…⟩)
  const rom = f => f.split('+').map(p => p.trim()).filter(Boolean)
    .map(p => paliShaped(p.replace(/ /g, '')) ? segment(p) : `⟨${p}⟩`).join(' + ');
  function isFormula(x) {
    const parts = x.split('+').map(p => p.trim());
    if (parts.length < 2 || parts.some(p => !p)) return false;
    return parts.every(p => { const q = p.replace(/\([၀-၉]+\)/g, '').replace(/[()\s,၊\-]/g, '');
      return q && paliShaped(q) && !/[၀-၉"“”'‘’]/.test(q); });
  }
  function analysis(an) {
    an = an || '';
    const F = [], N = {};
    for (const m of an.match(/[^။]*(?:။|$)/g) || []) {
      if (!m.trim()) continue;
      const body = m.trim().replace(/။$/, '').trim();
      if (isFormula(body)) F.push(body);
      else if (F.length) N[F.length - 1] = (N[F.length - 1] || '') + m;
      else return rom(an);
    }
    if (!F.length) return rom(an);
    const out = [];
    F.forEach((f, i) => {
      out.push(rom(f));
      if (i in N) {
        const toks = N[i].match(/[က-၉၌-႟္]+/g) || [];
        if (toks.length && toks.every(x => paliShaped(x) && !/^[၀-၉]+$/.test(x))) out.push(segment(N[i]).replace(/\.$/, ''));
      }
    });
    return out.join('. ');
  }
  return { token, segment, headword, analysis };
})();
if (typeof module !== 'undefined') module.exports = ROMAN;
