#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


SRC, TAR = "scripts/tex2tei/output/", "data/letters/"
for f in os.listdir(SRC):
    p = os.path.join(TAR, f)
    with open(p) as fi: s = fi.read()
    s = re.sub(r'(<TEI [^>]*source=")HBBW(")', r'\1HBBW-21\2', s, flags=re.S)
    with open(p, 'w') as fo: fo.write(s)
