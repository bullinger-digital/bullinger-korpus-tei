#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" new letter """

# new id
ids = []
for f in os.listdir("data/letters/"):
    m = re.match(r'(\d+)\.xml', f)
    if m: ids.append(m.group(1))
new_id = str(max([int(i) for i in ids])+1)

# new letter
with open("scripts/src/new_letter.xml") as fi: s = fi.read()
s = re.sub(r'(<TEI xmlns="http://www\.tei-c\.org/ns/1\.0" xml:id=")file\d+', r'\1file'+new_id, s, flags=re.S)
with open("data/letters/"+new_id+'.xml', 'w') as fo: fo.write(s)
