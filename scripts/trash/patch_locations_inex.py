#!/usr/bin/python
# -*- coding: utf8 -*-
import re, os

path_data = "scripts/src/locations_inex.txt"
path_countries = "data/index/localities.xml"

data = []
with open(path_data) as fi:
    for line in fi:
        t = line.split("__")
        r = '[\[\]\(\)]*'
        if len(t)>2: data.append([t[0], r+r.join(t[1].strip()), r+r.join(t[2].strip())+r])
        else: print("*Warning:", t)

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s_old = s
        if not re.match(r'.*source="keine".*', s, flags=re.S):
            for t in data:
                s = re.sub(r'('+t[1]+r'\s+)('+t[2]+r')([.,!?:;"\)\]»\'<\s]+)', r'\1<placeName ref="'+t[0]+r'" type="auto_name">\2</placeName>\3', s, flags=re.S)
            if s != s_old:
                with open(p, 'w') as fo: fo.write(s)
