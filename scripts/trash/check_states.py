#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" <revisionDesc status="?" """

states = dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*<revisionDesc[^>]*?status="([^"]*)".*', s, flags=re.S)
        if m:
            if m.group(1) in states: states[m.group(1)] += 1
            else: states[m.group(1)] = 1

for s in states: print(s, states[s])

""" [4.9.2023:]
finished 1653
untouched 11498
"""