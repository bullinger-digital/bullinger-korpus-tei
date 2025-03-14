#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

mapping = {
    832: [2464],
    850: [2560],
    #2755: [3466],
    #1377: [2854],
    #2932: [2933],
}

# letters
ROOT = "data/letters/"
n_tot = len(os.listdir(ROOT))
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for i in mapping:
            for j in mapping[i]:
                s = re.sub(r'ref="l'+str(j)+'"', r'ref="l'+str(i)+'"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

# register
with open("data/index/localities.xml") as fi: s = fi.read()
for i in mapping:
    for j in mapping[i]:
        s = re.sub(r'<place xml:id="l'+str(j)+'".*?</place>\s*', '', s, flags=re.S)
with open("data/index/localities.xml", 'w') as fo: fo.write(s)
