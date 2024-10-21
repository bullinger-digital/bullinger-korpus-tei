#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""
Bei folgenden Briefen muss der Korrespondent geändert werden von pID 8128 Dionysius Melander (Schwarzmann) d.J.
zu pID 8413 Dionysius Melander (Schwarzmann) d.Ä.:

    10379, 10421, 10476, 10577, 11220, 11292, 11462, 11575.

"""

for f in [10379, 10421, 10476, 10577, 11220, 11292, 11462, 11575]:
    p = "data/letters/"+str(f)+'.xml'
    with open(p) as fi: s = fi.read()
    for b in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
        b_ = re.sub(r'(<persName ref=")p8128(")', r'\1p8413\2', b, flags=re.S)
        s = re.sub(re.escape(b), b_, s, flags=re.S)
    with open(p, 'w') as fo: fo.write(s)