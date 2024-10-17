#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""" invalid persNames

*Warning ('p3184', 'Traversii') # 4842.xml

"""

mapping = {
    'p17826': 'p3932',
}

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for pid in mapping: s = re.sub(r'ref="'+pid+'"', r'ref="'+mapping[pid]+'"', s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
