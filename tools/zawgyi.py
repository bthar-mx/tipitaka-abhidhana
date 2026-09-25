"""Zawgyi -> Unicode for PCED's dictionary K, keeping the source's own spelling.

Built on python-myanmar's converter (pip: python-myanmar), with these corrections, each found
by comparing the output with the index's headwords and checked on PCED's own romanised key:

- tall vs round aa is kept as typed; the converter re-derives it (ပွါး -> ပွား, မ္ပါ -> မ္ပာ);
- ႆ (stacked ss) -> ဿ; ႎ (i + anusvara), and kinzi + i / ii / anusvara, lose their second
  part in the converter and are split first;
- e typed before a ligature (ṇḍ ṭṭh ṭṭ ḍḍ ḍḍh) belongs to the ligature, not to the consonant before it;
- stacked forms it leaves unconverted (ၲ ႓ ႅ ႖ ၤ ၽ ႈ ႕, and the tall u ဳ ဴ) are placed after the base consonant;
- ဥ + ီ -> ဦ, and စျ -> ဈ (Zawgyi typists write jha as ca + ya-pin).
"""
import re
from myanmar import converter as C


def _keep_aa(syl):
    return '_tall' if syl.get('aaVowel') == '\u102b' else ''


C.choose_aavowel_variant = _keep_aa

_PRE = str.maketrans({'\u1086': '\u103f', '\u108e': '\u102d\u1036',
                      '\u108b': '\u1064\u102d', '\u108c': '\u1064\u102e', '\u108d': '\u1064\u1036'})
_LIG = re.compile('\u1031([\u1091\u1092\u1097\u106e\u106f])')

_STACK = {'\u1072': '\u1039\u1010', '\u1093': '\u1039\u1018', '\u1085': '\u1039\u101c',
          '\u1096': '\u1039\u1010\u103d'}
_STACK_RE = re.compile('([\u1000-\u102a])([\u102b-\u1038\u103a-\u103e]*)([\u1072\u1093\u1085\u1096])')
_KINZI_RE = re.compile('([\u1000-\u1021])([\u103b-\u103e]*)\u1064')
_POST = str.maketrans({'\u1033': '\u102f', '\u1034': '\u1030', '\u107d': '\u103b',
                       '\u1088': '\u103e\u102f', '\u1095': '\u1037'})

RESIDUE = re.compile('[\u1050-\u109f]')


def zg2uni(s):
    s = _LIG.sub('\\1\ue000', s.translate(_PRE))
    u = C.convert(s, 'zawgyi', 'unicode').replace('\ue000', '\u1031')
    u = _STACK_RE.sub(lambda m: m.group(1) + _STACK[m.group(3)] + m.group(2), u)
    u = _KINZI_RE.sub(lambda m: '\u1004\u103a\u1039' + m.group(1) + m.group(2), u)
    u = u.translate(_POST)
    return u.replace('\u1025\u102e', '\u1026').replace('\u1005\u103b', '\u1008')
