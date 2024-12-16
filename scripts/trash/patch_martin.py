#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" tagging additional countries (pattern <ex/in> <country>) """

# register
countries = {}
with open("data/index/localities.xml") as fi: s = fi.read()
for e in re.findall(r'<place xml:id="(l\d+)"(.*?)</place>', s, flags=re.S):
    if m_country:
        countries[e[0]] = [m_country.group(1)]

n = 1
n_tot = len(os.listdir(ROOT))
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*source="keine".*', s, flags=re.S)\
            and not re.match(r'.*revisionDesc status="finished".*', s, flags=re.S):
            m_letter = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
            if m_letter:
                text = m_letter.group(1)
                for c0 in countries:
                    for c in countries[c0]:
                        for x in re.findall(r'(in|ex)(\s+)('+re.escape(c)+r')([^A-Za-zäöüéè])', text, flags=re.S):
                            text = re.sub(
                                r'(in|ex)(\s+)('+re.escape(c)+r')([^A-Za-zäöüéè])',
                                r'\1\2<placeName ref="'+c+r'" type="auto_name">\3</placeName>\4',
                                text, flags=re.S
                            )
                s = re.sub(re.escape(m_letter.group(1)), text, s, flags=re.S)
                s = rm_placename_zh(s)
                with open(p, 'w') as fo: fo.write(s)
                print(round(n/n_tot*100, 1), f)
                n += 1
