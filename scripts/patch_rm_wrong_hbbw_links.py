#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

titles = {"Zürich StA": 1, "Zürich ZB": 1}
with open("data/index/bibliography.xml") as fi: s = fi.read()
for t in re.findall(r'<title>(.*?)</title>', s, flags=re.S):
    if not re.match(r'.*HBBW.*', t) and t.strip() and t != 'S' and t != 'Z':
        titles[t] = 1
        #print(t)

ROOT = "data/letters/"
count = 0
tot = len(os.listdir(ROOT))-1
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        count += 1
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_text = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
        if m_text:
            text = m_text.group(1)
            for t in titles:
                for h in re.findall(r'(('+re.escape(t)+'(.{,40}))<ref[^>]*>(\[?\(?Nr.*?)</ref>)', text, flags=re.S):
                    if not re.match(r'.*(s\.|[Vv]gl\.|Siehe|oben|unten|Brief)', h[1], flags=re.S):
                        text = re.sub(re.escape(h[0]), h[1]+h[3], text, flags=re.S)
                        print(str(round(100*count/tot))+'%', h[0], "\t-->", h[1]+h[3])
            s = re.sub(re.escape(m_text.group(1)), text, s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)
