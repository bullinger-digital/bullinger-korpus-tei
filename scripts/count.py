#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


# NOTES
data = {}
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for note in re.findall(r'<note([^>]*)\s*?/?\s*>', s, flags=re.S):
            m = re.match(r'.* xml:id="([^"]*)".*', note)
            if m:
                if m.group(1) not in data: data[m.group(1)] = 1
                else : data[m.group(1)] += 1

count = 0
for key in dict(sorted(data.items(), key=lambda x: x[1], reverse=True)):
    print('-', key+':', data[key])
    count += data[key]

print("Total:", count)

