#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" bugfixes """

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'<placeName([^>]*>[^<]*</persName>)', r'<persName\1', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
