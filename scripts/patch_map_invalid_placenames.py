#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""" invalid placeNames
New:
('l23447', 'Grimoldsried') - https://de.wikipedia.org/wiki/Grimoldsried
('l8098', 'Mümpelgard') - https://de.wikipedia.org/wiki/M%C3%B6mpelgard ?
('l23674', 'Poitou') - https://de.wikipedia.org/wiki/Poitou)
"""

rm = [
    ('<placeName ref="l21707" cert="high">Valois</placeName>', 'Valois'),
    ('<placeName ref="l5504" cert="high">Konrad Konstanzer</placeName>', '<persName ref="p5504" cert="high">Konrad Konstanzer</persName>'),
    ('<placeName ref="l23447" cert="high">Grimoldsried</placeName>', 'Grimoldsried'), # 13054.xml
    ('<placeName ref="l8016" cert="high">Gotzones</placeName>', 'Gotzones') # 9461.xml
]
mapping = {
    'l1420': 'l2675',
    'l1': 'l2528',
    'l141': 'l673',
    'l674': 'l673',
    'l675': 'l673',
    'l676': 'l673',
    'l677': 'l673',
    'l2690': 'l2466',
    'l23341': 'l825',
    'l21050': 'l1229',
    'l21050': 'l1715',
    'l21987': 'l771',
    'l959': 'l2693',
    'l30040': 'l167',
    'l30038': 'l920',
}

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for pid in mapping: s = re.sub(r'ref="'+pid+'"', r'ref="'+mapping[pid]+'"', s, flags=re.S)
        for r in rm: s = re.sub(re.escape(r[0]), r[1], s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
