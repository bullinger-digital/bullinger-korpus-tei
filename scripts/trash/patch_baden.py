#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" Baden: placeName ref {910, 2512} -> 21 """

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<placeName[^>]*ref=")l910(")', r'\1l21\2', s, flags=re.S)
        s = re.sub(r'(<placeName[^>]*ref=")l2512(")', r'\1l21\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

# rm (now) redundant entries from index and blank lines
with open("data/index/localities.xml") as fi: s = fi.read()
s = re.sub(r'<place xml:id="l910".*?</place>\s*', '', s, flags=re.S)
s = re.sub(r'<place xml:id="l2512".*?</place>\s*', '', s, flags=re.S)
s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
with open("data/index/localities.xml", 'w') as fo: fo.write(s)
