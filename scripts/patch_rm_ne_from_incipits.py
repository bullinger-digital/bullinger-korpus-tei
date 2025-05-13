#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for i in re.findall('((<incipit>)(.*?)(</incipit>))', s, flags=re.S):
            new_i = re.sub(r'<.*?>', '', i[2], flags=re.S)
            new_i = re.sub(r'\s+', ' ', new_i, flags=re.S)
            if i!= new_i:
                s = re.sub(re.escape(i[0]), i[1]+new_i+i[3], s, flags=re.S)
                with open(p, 'w') as fo: fo.write(s)
