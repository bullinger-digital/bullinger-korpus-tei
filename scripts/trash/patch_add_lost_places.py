#!/usr/bin/python
# -*- coding: utf8 -*-

import re, os

"""
Ich habe festgestellt, dass in organizations.xml Ortschaften referenziert werden,
die im Register fehlen. Kannst du diese wiederherstellen? Folgende Ortschaften sind betroffen:

ref="l474" (St. Gallen)
ref="l910" (Baden/AG)
ref="l490" (Stein am Rhein)
ref="l457" (Konstanz)
ref="l114" (Diessenhofen)

Zudem gibt es in den Briefen folgende ungültigen Referenzen auf Ortschaften (vermutlich schon länger im Korpus bzw.
nicht durch das Register-Cleanup entstanden). Kannst du auch hier korrigieren?

ref="l1174"
ref="l2464"
"""

org_places = {}
with open("data/index/organizations.xml") as fi:
    for p_id in re.findall(r'<placeName[^>]*?ref="([^"]*)"', fi.read(), flags=re.S):
        org_places[p_id] = True

places = {}
with open("data/index/localities.xml") as fi:
    for p_id in re.findall(r'<place[^>]*?xml:id="([^"]*)"', fi.read(), flags=re.S):
        places[p_id] = True

for p_id in org_places:
    if p_id not in places:
        print("*Warning", p_id)

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        with open(os.path.join(ROOT, f)) as fi: s = fi.read()
        for p_id in re.findall(r'<placeName[^>]*?ref="([^"]*)"', s, flags=re.S):
            if p_id not in places:
                print(f, p_id, "is invalid.")
"""
2258.xml l2464 is invalid.
2764.xml l1174 is invalid.
"""