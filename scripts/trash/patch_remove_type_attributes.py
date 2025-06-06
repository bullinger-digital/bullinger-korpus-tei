#!/usr/bin/python
# -*- coding: utf8 -*-
import re, os


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<s [^>]*)\s+type="[^"]*"', r'\1', s, flags=re.S)
        s = re.sub(r'(<persName [^>]*)\s+type="[^"]*"', r'\1', s, flags=re.S)
        s = re.sub(r'(<placeName [^>]*)\s+type="[^"]*"', r'\1', s, flags=re.S)
        s = re.sub(r'(<persName)\s+type="[^"]*"', r'\1', s, flags=re.S)
        s = re.sub(r'(<placeName)\s+type="[^"]*"', r'\1', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
