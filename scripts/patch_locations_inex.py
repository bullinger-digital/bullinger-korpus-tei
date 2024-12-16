#!/usr/bin/python
# -*- coding: utf8 -*-
import re, os

path_data = "scripts/src/locations_inex.txt"
path_countries = "data/index/localities.xml"

data = {}
with open(path_data) as fi:
    for line in fi:
        t = line.split("__")
        if len(t)>1: data[t[0]] = [t[1].strip(), t[2].strip()]
        else: print("Warning:", t)

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s_old = s
        if not re.match(r'.*source="keine".*', s, flags=re.S):
            for x in data:
                t = ' '.join(data[x])
                s = re.sub(t, data[x][0]+' <placeName ref="'+x+'" type="auto_name">'+data[x][1]+'</placeName>', s, flags=re.S)
            if s != s_old:
                with open(p, 'w') as fo: fo.write(s)
