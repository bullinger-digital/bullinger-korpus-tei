#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re


src = "scripts/save/"
for f in os.listdir(src):
    p = os.path.join(src, f)
    with open(p) as fi: s = fi.read()
    m_fac = re.match(r'.*(<facsimile>.*?</facsimile>).*', s, flags=re.S)
    if m_fac:
        fac = m_fac.group(1)
        with open("data/letters/"+f) as fi: s_ = fi.read()
        s_ = re.sub(r'<facsimile.*?</facsimile>', fac, s_, flags=re.S)
        with open("data/letters/"+f, 'w') as fo: fo.write(s_)
