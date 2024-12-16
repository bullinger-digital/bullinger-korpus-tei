#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Froschauer d.J. (pID 1227) in allen Briefen zwischen dem
    - 9. Februar 1532 (= Brief ID 10092) und dem
    - 5. Oktober 1547 (= Brief ID 13081)
auf Froschauer d.Ä. (pID 4851) übertragen --> 686 Erwähnungen!
"""
import re, os

def map_froschauer_dj(s): return re.sub(r'(ref=")p1227(")', r'\1p4851\2', s, flags=re.S)

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    mf = re.match(r'(.*)\.xml', f)
    if mf:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*<date when="(\d\d\d\d)([^"]*)"[^>]*cert[^>]*/>.*', s, flags=re.S)
        if m:
            year = int(m.group(1))
            m1 = re.match(r'.*<date when="(\d\d\d\d)\-(\d\d)"[^>]*cert[^>]*/>.*', s, flags=re.S)
            m2 = re.match(r'.*<date when="(\d\d\d\d)\-(\d\d)\-(\d\d)"[^>]*cert[^>]*/>.*', s, flags=re.S)
            if 1532 < year and year < 1547: s = map_froschauer_dj(s)
            elif year == 1532:
                if int(m2.group(2)) > 2: s = map_froschauer_dj(s)
                elif int(m2.group(2)) == 2 and int(m2.group(3)) > 8: s = map_froschauer_dj(s)
            elif year == 1547:
                if int(m2.group(2))<10: s = map_froschauer_dj(s)
                elif int(m2.group(2)) == 10 and int(m2.group(3)) < 6: s = map_froschauer_dj(s)
        else:
            id_ = int(mf.group(1))
            if 10091 < id_ and id_ < 13081:
                if re.match(r'.*ref="p1227"[^>]*/>.*', s, flags=re.S): print("case!") # none
        with open(p, 'w') as fo: fo.write(s)
