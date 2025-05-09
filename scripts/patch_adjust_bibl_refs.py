#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        s = re.sub(r'(<bibl [^>]*ref=")(\d+")', r'\1b\2', s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
