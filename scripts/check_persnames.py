#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""" validate placeNames (resp. their IDs) """

pids = {}
with open("data/index/persons.xml") as fi: s = fi.read()
for id_ in re.findall(r'<persName[^>]*?(xml:id|ref)="(p\d+)"', s, flags=re.S): pids[id_[1]] = 1

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for p in re.findall(r'<persName[^>]*ref="([^"]*)"[^>]*>(.*?)</persName>', s, flags=re.S):
            if p[0] not in pids: print("*Warning", p)
