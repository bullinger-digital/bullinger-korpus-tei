#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


map = {
    "la": "Latein",
    "el": "Griechisch",
    "de": "Deutsch",
    "he": "Hebräisch",
    "fr": "Französisch"
}


text_langs = dict()
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for t in re.findall(r'((<textLang>)(.*?)(</textLang>))', s, flags=re.S):
            if t[2] in map: s = re.sub(re.escape(t[0]), t[1]+map[t[2]]+t[3], s, flags=re.S)
            if t[2] not in text_langs: text_langs[t[2]] = 0
            text_langs[t[2]] += 1
        with open(p, 'w') as fo: fo.write(s)

for t in text_langs: print(text_langs[t], '\t', t)

"""
Vorher:

6407 	 <textLang>Latein</textLang>
1883 	 <textLang>la</textLang>
1852 	 <textLang>Deutsch</textLang>
194 	 <textLang>el</textLang>
1245 	 <textLang>de</textLang>
2 	 <textLang>Italienisch</textLang>
7 	 <textLang>Französisch</textLang>
5 	 <textLang>he</textLang>
2 	 <textLang>fr</textLang>
"""
