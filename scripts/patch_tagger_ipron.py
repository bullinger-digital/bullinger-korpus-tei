#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" Affixes
    Eg. <persName ref="p2336" cert="high">Bernardinus ille Ochinus</persName>
    --> <persName ref="p2336" cert="high">Bernardinus <span type="affix">ille</span> Ochinus</persName>
"""

data = {}
with open("scripts/src/ipron.csv") as fi:
    for line in fi:
        t = line.strip().split("__")
        data[t[0]] = t[1]

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for x in data:
            for y in re.findall(r'<persName[^>]*>'+re.escape(x)+r'</persName>', s, flags=re.S):
                new_ = re.sub(r'('+re.escape(data[x])+')', r'<span type="affix">\1</span>', y, flags=re.S)
                s = re.sub(re.escape(y), new_, s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
