#!/usr/bin/env python3
"""Fold spellings that print, index and OCR disagree on, for matching headwords only.

Each fold replaces one character by one, so offsets into folded text are offsets into the
original. Nothing folded is ever written out: the index spelling stays the headword.

    ါ -> ာ          the print writes ာ where the index writes ါ after a stacked consonant
                    (အလမ္ပာန / အလမ္ပါန, vol. 3 p. 654; brief §13). Folded everywhere: the two
                    are one vowel in two shapes.
    ဉ -> ည          ဉာ / ညာ: 4b prints ညာ where the index writes ဉာ (p. 74; brief §15).
    ဌ ဠ -> ဋ        ဋ read ဌ or ဠ (vol. 5; brief §17).
    ည္ဇ ည္ဆ -> ည္စ   stacked ဇ and ဆ read as စ (vols. 3 on, 4a; brief §14, §17).
    ဏ္ဍ ဏ္ဏ -> ဏ္ဋ   ဏ္ဌ read ဏ္ဍ or ဏ္ဏ (vol. 5); ဌ is already ဋ by the rule above.
"""
SIMPLE = {'ါ': 'ာ', 'ဉ': 'ည', 'ဌ': 'ဋ', 'ဠ': 'ဋ'}
AFTER = {'ည္': {'ဇ': 'စ', 'ဆ': 'စ'}, 'ဏ္': {'ဍ': 'ဋ', 'ဏ': 'ဋ'}}


def fold(s):
    out = []
    for ch in s:
        c = SIMPLE.get(ch, ch)
        prev = ''.join(out[-2:])
        if prev in AFTER: c = AFTER[prev].get(c, c)
        out.append(c)
    r = ''.join(out)
    assert len(r) == len(s)
    return r


if __name__ == '__main__':
    for a, b in [('အလမ္ပါန', 'အလမ္ပာန'), ('ဥဒယဗ္ဗယဉာဏ', 'ဥဒယဗ္ဗယညာဏ'), ('ကဉ္ဇိက', 'ကဉ္စိက'),
                 ('ဉ္ဆ', 'ဉ္စ'), ('ကဏ္ဌ', 'ကဏ္ဍ'), ('ကဏ္ဌ', 'ကဏ္ဏ'), ('ဝိဟေဌ', 'ဝိဟေဠ')]:
        print(a, b, fold(a) == fold(b))
