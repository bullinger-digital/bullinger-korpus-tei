#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""

"""

for i in [10630, 10642, 10794, 10795, 10803, 10858, 10879, 10983, 10994, 11003, 11008, 11037, 11111, 11476, 12431, 297,
          457, 523, 529, 598, 623, 1919, 3020, 3052, 3563, 4047, 4194, 4703, 6752, 6759]:
    p = "data/letters/"+str(i)+'.xml'
    with open(p) as fi: s = fi.read()
    for b in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
        for b in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
            b_ = re.sub(r'(<persName ref=")p8177(")', r'\1p8178\2', b, flags=re.S)
            s = re.sub(re.escape(b), b_, s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

""" Correspondents:

p8177   --> Thomas Blarer d.Ä. (30)
p495    --> Heinrich Bullinger (Antistes)
p8055   --> Ambrosius Blarer
p4079   --> Johannes Zwick
p4082   --> Konard Zwick """
