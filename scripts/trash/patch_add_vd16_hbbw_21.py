#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


root = "scripts/save/"
for f in os.listdir(root):
    path = os.path.join("data/letters/", f)
    with open(path) as fi: s = fi.read()
    for vd in re.findall(r'<ref target="https://gateway-bayern\.de/VD16[^"]*">[^<]*</ref>', s, flags=re.S):
        s = re.sub(
            re.escape(vd),
            r'<bibl source="b652">VD16</bibl> '+vd, s, flags=re.S
        )
        s = re.sub(
            r'<bibl source="b652">VD16</bibl>\s*<bibl source="b652">VD16</bibl>',
            '<bibl source="b652">VD16</bibl>', s, flags=re.S
        )
    with open(path, 'w') as fo: fo.write(s)
