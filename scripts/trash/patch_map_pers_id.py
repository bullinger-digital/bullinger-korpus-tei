#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


mapping = {
    'p18505': 'p8375',
}

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for pid in mapping: s = re.sub(r'ref="'+pid+'"', r'ref="'+mapping[pid]+'"', s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
