#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil

"""
ROOT, stats = "data/letters/", {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for e in re.findall(r'<([^/>\s]*)', s, flags=re.S):
            if e not in stats: stats[e] = 0
            stats[e] += 1

for e in stats: print(e, stats[e])
"""
"""
<TEI[^>]*type="(.*?)"
"""
ROOT, stats = "data/letters/", {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for e in re.findall(r'category', s, flags=re.S):
            if e not in stats: stats[e] = 0
            stats[e] += 1

for e in stats: print(e, stats[e])