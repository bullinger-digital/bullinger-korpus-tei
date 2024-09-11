#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" adds footnotes refering to metadata """

src = {}
with open("scripts/src/src_empty.csv") as fi:
    for line in fi:
        f = line.strip()
        src[f] = True

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        """
        m = re.match(r'.*<TEI[^>]*source="([^"]*)".*', s, flags=re.S)
        if m:
            t = m.group(1)
            if t in src: src[t] += 1
            else: src[t] = 1
        """
        if f in src:
            s = re.sub(r'(<TEI [^>]*source=")[^"]*(")', r'\1keine\2', s, flags=re.S)
            s = re.sub(r'\n\s*<bibl n="\d+" type="transcription">[^<]*</bibl>', '', s, flags=re.S)
        s = re.sub(r'source="HE\-Hentius"', 'source="HE"', s, flags=re.S)
        s = re.sub(r'source="TAS\-TAS"', 'source="TAS"', s, flags=re.S)
        s = re.sub(r'source="GR\-GR"', 'source="GR"', s, flags=re.S)
        s = re.sub(r'source="Kessler, Sabbata"', 'source="KS"', s, flags=re.S)
        s = re.sub(r'source="0\-0"', 'source="TUSTEP-0"', s, flags=re.S)
        s = re.sub(r'source="TUSTEP\-0"', 'source="TUSTEP"', s, flags=re.S)

        with open(p, "w") as fo: fo.write(s)

# for t in src: print(t, src[t])
