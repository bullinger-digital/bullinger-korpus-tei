#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" map persname ref 8451 -> 6831
Alle Einträge zu ID 8451 Johannes (Gian) Travers verschieben zu ID 6831	Johannes Travers d.Ä.. Es sind unter ID 8451
zwar weniger als 50, aber diese ID ist auch beim Korrespondenten hinterlegt, was über das Mithelfen-Tool nicht geht. """


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<persName[^>]*ref=")p8451(")', r'\1p6831\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
