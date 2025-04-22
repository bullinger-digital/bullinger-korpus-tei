#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re


src = "data/letters"
for f in os.listdir(src):
    if f.endswith('.xml'):
        p = os.path.join(src, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(
            r'(<placeName[^>/]*)(>)\s*<orig>.*?</orig>\s*</placeName>',
            r'\1/\2', s, flags=re.S
        )
        with open(p, 'w') as fo: fo.write(s)
