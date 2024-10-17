#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""" vd-16 links """

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for n in re.findall(r'(<bibl>([^<]*VD[^<]*)</bibl>)', s, flags=re.S):
            m = re.match(r'.*?(VD\s*16|VD|)\s*([A-Z]*)\s*(\d+).*', n[1], flags=re.S)
            if m:
                ref = "https://gateway-bayern.de/VD16+"+m.group(2)+'+'+m.group(3)
                if not re.match(r'.*\+\+.*', ref, flags=re.S):
                    s = re.sub(re.escape(n[0]), r'<bibl source="'+ref+'">'+n[1]+'</bibl>', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
