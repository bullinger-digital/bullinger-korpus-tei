#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" tagging additional countries (pattern <ex/in> <country>) """

# register
countries = {}
with open("data/index/localities.xml") as fi: s = fi.read()
for e in re.findall(r'<place xml:id="(l\d+)"(.*?)</place>', s, flags=re.S):
    m_settlement = re.match(r'.*<settlement>(.*?)</settlement>.*', e[1], flags=re.S)
    m_district = re.match(r'.*<district>(.*?)</district>.*', e[1], flags=re.S)
    m_country = re.match(r'.*<country>(.*?)</country>.*', e[1], flags=re.S)
    if m_settlement: countries[e[0]] = [m_settlement.group(1)]
    elif m_district: countries[e[0]] = [m_district.group(1)]
    elif m_country: countries[e[0]] = [m_country.group(1)]

# letters
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for p in re.findall(r'<placeName[^>]*ref="([^"]*)"[^>]*>([^<]*)</placeName>', s, flags=re.S):
            if p[0] in countries and p[1] not in countries[p[0]]: countries[p[0]].append(p[1])
            else: countries[p[0]] = [p[1]]

# corrections
def rm_placename_zh(s):
    s = re.sub(r'([^<]*[\.\,]\s*)<placeName ref="l587"[^>]*>(Zürich)</placeName>(\s*\d{4}[^<]*)', r'\1\2\3', s, flags=re.S)
    s = re.sub(r'([^<]*)<placeName ref="l587"[^>]*>(Zürich)</placeName>(\s*(StA|ZB)[^<]*)', r'\1\2\3', s, flags=re.S)
    return s


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
