#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'<span type="affix">', r'<span type="pronoun">', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)