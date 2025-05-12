#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re


with open("scripts/src/empty_letters.csv", 'w') as fo:
    ROOT = "data/letters/"
    for f in os.listdir(ROOT):
        if re.match(r'.*\.xml', f):
            p = os.path.join(ROOT, f)
            with open(p) as fi: s = fi.read()
            m_src = re.match(r'.*<TEI[^>]*"([^"]*)" source="(keine|)".*', s, flags=re.S)
            m_nl = re.match(r'.*<bibl>\[Keine Transkription verfügbar\.\]</bibl>.*', s, flags=re.S)
            #if m_src and not m_nl: print('*', f)
            #if not m_src and m_nl: print('**', f)
            if m_src and m_nl and m_src.group(1) not in ["Verweis", "Hinweis"]: fo.write(f+'\n')