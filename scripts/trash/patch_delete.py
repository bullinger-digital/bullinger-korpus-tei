#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
TRASH = [168, 169, 268, 269, 341, 347, 547, 548, 656, 776, 1042, 1191, 1192, 1193, 1194, 1297, 1525, 1537, 1988, 1989,
         2082, 2974, 4110, 4167, 4168, 4468, 4889, 5671, 5782, 6973, 7482, 7724, 8119, 8737, 9532, 9627, 9628, 9629]

# delete files
for id_ in TRASH:
    path = os.path.join(ROOT, str(id_)+'.xml')
    if os.path.exists(path): os.remove(path)

# delete links
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for id_ in TRASH:
            s = re.sub(r'[ \t]*<ref type="(child|parent)" target="file'+str(id_)+'"\s*/>[ \t]*\n', r'', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
