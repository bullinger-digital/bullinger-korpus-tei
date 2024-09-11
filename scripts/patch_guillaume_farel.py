#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" map persname ref 6235 -> 1049 """

# letters
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<persName[^>]*ref=")p6235(")', r'\1p1049\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

# index
with open("data/index/persons.xml") as fi: s = fi.read()
s = re.sub(r'<person xml:id="P6235">.*?</person>\s*', '', s, flags=re.S)
s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
with open("data/index/persons.xml", 'w') as fo: fo.write(s)
