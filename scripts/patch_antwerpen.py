#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" Antwerpen: placeName ref 16 -> 15 """

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<placeName[^>]*ref=")l16(")', r'\1l15\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

# rm (now) redundant entries from index
with open("data/index/localities.xml") as fi: s = fi.read()
s = re.sub(r'<place xml:id="l16".*?</place>\s*', '', s, flags=re.S)
with open("data/index/localities.xml", 'w') as fo: fo.write(s)
