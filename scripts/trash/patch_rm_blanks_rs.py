#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for rs in re.findall(r'((<rs[^>]*>)\s*(.*?)\s*(</rs>))', s, flags=re.S):
            s = re.sub(re.escape(rs[0]), rs[1]+rs[2]+rs[3], s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)