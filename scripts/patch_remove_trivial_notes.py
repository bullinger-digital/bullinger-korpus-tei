#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for e in ["persName", "placeName"]:
            for x in re.findall(r'((<'+e+r'[^>]*ref="([^"]*)"[^>]*>[^<]*</'+e+r'>)\s*<note type="entity">\s*'+r'<'+e+r'[^>]*ref="([^"]*)"[^>]*>[^<]*</'+e+r'>[^<]*</note>)', s, flags=re.S):
                if x[2] == x[3]: s = re.sub(re.escape(x[0]), x[1], s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
