#!/usr/bin/python
# -*- coding: utf8 -*-

""" Absendeort 333 (Mömpelgard) verschieben zu pID 327 Montbéliard (Mömpelgard) """

import re, os


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    mf = re.match(r'(.*)\.xml', f)
    if mf:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'<placeName ref="l333"', '<placeName ref="l327"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
