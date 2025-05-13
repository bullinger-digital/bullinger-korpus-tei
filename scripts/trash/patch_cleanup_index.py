#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" delete unreferenced persons/places """

# IDs in usage
pers_ids, place_ids = dict(), dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for p_id in re.findall(r'<persName[^>]*ref="p([^"]*)"', s, flags=re.S): pers_ids[p_id] = True
        for p_id in re.findall(r'<placeName[^>]*ref="l([^"]*)"', s, flags=re.S): place_ids[p_id] = True

# pers-index
with open("data/index/persons.xml") as fi: s = fi.read()
tot, delete = 0, 0
for p in re.findall(r'(<person xml:id="P(\d+)">.*?</person>\s*)', s, flags=re.S):
    tot += 1
    if p[1] not in pers_ids:
        delete += 1
        s = re.sub(re.escape(p[0]), '', s, flags=re.S)
with open("data/index/persons.xml", 'w') as fo: fo.write(s)
print("Person-Index: Deleted", 100*delete/tot, '%')

# place-index
with open("data/index/localities.xml") as fi: s = fi.read()
tot, delete = 0, 0
for p in re.findall(r'(<place xml:id="l(\d+)">.*?</place>\s*)', s, flags=re.S):
    tot += 1
    if p[1] not in place_ids:
        delete += 1
        s = re.sub(re.escape(p[0]), '', s, flags=re.S)
with open("data/index/localities.xml", 'w') as fo: fo.write(s)
print("Place-Index: Deleted", 100*delete/tot, '%')

'''
Person-Index: Deleted 10.798331843908251 %
Place-Index: Deleted 10.36691904484566 %
'''
