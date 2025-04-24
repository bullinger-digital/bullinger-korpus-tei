#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for i in range(6495, 9678):
    p = os.path.join(ROOT, str(i)+'.xml')
    if os.path.isfile(p):
        with open(p) as fi: s = fi.read()
        s = re.sub(r'"p8039"', r'"p8017"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
