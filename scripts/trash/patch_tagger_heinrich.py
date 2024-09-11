#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" moves "Heinrich"-Aliasses in to Bullinger-persName-Elements """

heiri = []
with open("scripts/src/heiri.csv") as fi:
    heiri = [h.strip() for h in fi if h.strip()]

# print(heiri)
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for h in heiri:
            s = re.sub(r'('+re.escape(h)+r'\s*)(<persName[^>]*ref="p495"[^>]*>)', r'\2\1', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
