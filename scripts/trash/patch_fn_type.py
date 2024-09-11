#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" adds footnote types (bio/lex) """

data = {}
with open("scripts/src/fn_type.csv") as fi:
    for line in fi:
        t = line.strip().split("__")
        if t[0] in data: data[t[0]].append((t[1], t[2]))
        else: data[t[0]] = [(t[1], t[2])]

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f) and f in data:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for x in data[f]: s = re.sub(r'(<note xml:id="fn'+x[0]+'" type="footnote") n', r'\1 ana="'+x[1]+'" n', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
