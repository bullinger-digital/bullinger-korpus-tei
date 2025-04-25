#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<bibl>)\s*(HBBW|hbbw)\s*\-?\s*(</bibl>)\s*\-?\s*([IVX\d+]+)', r'\1\2 \4\3', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
