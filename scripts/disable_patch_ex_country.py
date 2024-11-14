#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" tagging additional countries (pattern <ex/in> <country> """

countries = {}
with open("data/index/localities.xml") as fi: s = fi.read()
for e in re.findall(r'<place xml:id="(l\d+)"(.*?)</place>', s, flags=re.S):
    m_settlement = re.match(r'.*<settlement>(.*?)</settlement>.*', e[1], flags=re.S)
    m_district = re.match(r'.*<district>(.*?)</district>.*', e[1], flags=re.S)
    m_country = re.match(r'.*<country>(.*?)</country>.*', e[1], flags=re.S)
    if m_settlement: countries[e[0]] = m_settlement.group(1)
    elif m_district: countries[e[0]] = m_district.group(1)
    elif m_country: countries[e[0]] = m_country.group(1)

n = 1
ROOT = "data/letters/"
n_tot = len(os.listdir(ROOT))
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*source="keine".*', s, flags=re.S):
            m_letter = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
            if m_letter:
                text = m_letter.group(1)
                for c in countries:
                    text = re.sub(
                        r'(in|ex)(\s+)('+re.escape(countries[c])+r')',
                        r'\1\2<placeName ref="'+c+r'" type="auto_name">\3</placeName>',
                        text, flags=re.S
                    )
                s = re.sub(re.escape(m_letter.group(1)), text, s, flags=re.S)
                with open(p, 'w') as fo: fo.write(s)
                print(round(n/n_tot*100, 1), f)
                n += 1
