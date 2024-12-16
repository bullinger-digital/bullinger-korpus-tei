#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    mf = re.match(r'(.*)\.xml', f)
    if mf:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'<orgName ref="og49pl1"', '<orgName ref="og49pl3386"', s, flags=re.S)
        s = re.sub(r'l474"', 'l473"', s, flags=re.S)
        s = re.sub(r'l492"', 'l491"', s, flags=re.S)
        s = re.sub(r'l389"', 'l957"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

