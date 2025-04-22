#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


ROOT, stats = "data/letters/", {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<note xml:id="fn)(\d+)(" type="footnote"[^>]* n=")num(">)', r'\1\2\3\2\4', s, flags=re.S)
        s = re.sub(r'(<note xml:id="fn)([^"]*)(" type="footnote"[^>]* n=")alpha(">)', r'\1\2\3\2\4', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
