#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for e in re.findall(r'(<note type="entity">(<.*?>)</note>)', s, flags=re.S):
            s = re.sub(re.escape(e[1]+e[0]), e[1], s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
