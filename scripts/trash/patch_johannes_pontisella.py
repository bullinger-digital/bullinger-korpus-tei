#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" map persname ref 2627 -> 6130
ID 2627 Johannes Pontisella d.J. alle zu ID 6130 Johannes Pontisella d.Ä. verschieben.
ID 2627 aber stehen lassen, weil der junge Pontisella möglicherweise erwähnt wird (s. to do Patricia)
"""

pontisellas = dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for x in re.findall(r'<persName[^>]*ref="p(2627|6130)"[^/>]*>(.*?)</persName>', s, flags=re.S):
            pontisellas[x[1]] = True
        s = re.sub(r'(<persName[^>]*ref=")p2627(")', r'\1p6130\2', s, flags=re.S)
        s = re.sub(
            r'(<persName[^>]*ref=")p6130("[^>]*>Pontisellam iuniorem</persName>)',
            r'\1p2627\2', s, flags=re.S
        )
        with open(p, 'w') as fo: fo.write(s)

#for p in pontisellas: print(p)
