#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" rm bib doubles """

# rm true doubles
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_bib = re.match(r'.*(<additional.*?</additional>).*', s, flags=re.S)
        if m_bib:
            titles = dict()
            for t in re.findall(r'<bibl.*?</bibl>', m_bib.group(1), flags=re.S):
                if t not in titles: titles[t] = True
                else:
                    s = re.sub(
                        r'('+re.escape(t)+r'.*?)'+re.escape(t)+r'\s*',
                        r'\1', s, flags=re.S
                    )
            if f == "5654.xml":
                s = re.sub(
                    r'\s*<bibl type="Literatur">\s*<title>Benrath, Erast, in: HBGesA II \(1975\), 97, Anm\. 16\.</title>\s*</bibl>', '', s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)
