#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" updates the numbering of all sentences """

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        s = re.sub(r'(<s [^>]*n=")\d+(")', r'\1\2', s, flags=re.S)
        m, n = re.match(r'((.*?<s [^>]*n=")(".*))', s, flags=re.S), 1
        while m:
            s = re.sub(re.escape(m.group(1)), m.group(2)+str(n)+m.group(3), s, flags=re.S)
            m, n = re.match(r'((.*?<s [^>]*n=")(".*))', s, flags=re.S), n+1
        with open(path, 'w') as fo: fo.write(s)
