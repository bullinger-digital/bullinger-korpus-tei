#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        s = re.sub(
            r'<placeName[^>]*>([^<]*)</placeName>(\s*)(StA|ZB)',
            r'\1\2\3', s, flags=re.S
        )
        with open(path, 'w') as fo: fo.write(s)
