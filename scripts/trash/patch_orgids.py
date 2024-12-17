#!/usr/bin/python
# -*- coding: utf8 -*-
import re, os

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'"og26pl389"', r'"og26pl957"', s, flags=re.S)
        s = re.sub(r'"og26pl473"', r'"og26pl474"', s, flags=re.S)
        s = re.sub(r'"og45pl492"', r'"og45pl491"', s, flags=re.S)
        s = re.sub(r'"og49pl492"', r'"og49pl491"', s, flags=re.S)
        s = re.sub(r'"og50pl473"', r'"og50pl474"', s, flags=re.S)
        s = re.sub(r'"og63pl492"', r'"og63pl491"', s, flags=re.S)
        s = re.sub(r'"og65pl114"', r'"og65pl113"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
