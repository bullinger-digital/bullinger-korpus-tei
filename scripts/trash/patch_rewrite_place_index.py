#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


path = "data/index/localities.xml"
with open(path) as fi: s = fi.read()
s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
s = re.sub(r'(<location>)\s*(<geo>)\s*([^<]*)\s*(</geo>)\s*(</location>)', r'\1\2\3\4\5', s, flags=re.S)

'''
elements = {}
for p in re.findall(r'<place[^>]*>(.*?)</place>', s, flags=re.S):
    for x in re.findall(r'<([^/>\s*]*)[^/>]*>', p, flags=re.S):
        elements[x] = True
    if re.match(r'.*<place.*', p, flags=re.S): print("*Warning", p)
    if len(re.findall('idno', p)) > 2: print("***Warning: idno", p)
    if len(re.findall('settlement', p)) > 2: print("***Warning: settlement", p)
    if len(re.findall('district', p)) > 2: print("***Warning: district", p)
    if len(re.findall('country', p)) > 2: print("***Warning: country", p)
    if len(re.findall('location', p)) > 2: print("***Warning: location", p)
for e in elements: print(e) # --> {settlement, district, country, location/geo, idno}
'''

for p in re.findall(r'(<place[^>]*>(.*?)</place>)', s, flags=re.S):
    m_settlement = re.match(r'.*<settlement>\s*(.*?)\s*</settlement>.*', p[1], flags=re.S)
    m_district = re.match(r'.*<district>\s*(.*?)\s*</district>.*', p[1], flags=re.S)
    m_country = re.match(r'.*<country>\s*(.*?)\s*</country>.*', p[1], flags=re.S)
    m_location = re.match(r'.*<location>\s*(.*?)\s*</location>.*', p[1], flags=re.S)
    m_idno = re.match(r'.*<idno[^>]*>\s*(.*?)\s*</idno>.*', p[1], flags=re.S)
    new = '\n'
    if m_settlement: new += 4*'\t'+'<settlement>'+re.sub(r'\s+', ' ', m_settlement.group(1))+'</settlement>\n'
    if m_district: new += 4 * '\t' + '<district>' + re.sub(r'\s+', ' ', m_district.group(1)) + '</district>\n'
    if m_country: new += 4 * '\t' + '<country>' + re.sub(r'\s+', ' ', m_country.group(1)) + '</country>\n'
    if m_location: new += 4 * '\t' + '<location>' + re.sub(r'\s+', ' ', m_location.group(1)) + '</location>\n'
    if m_idno: new += 4 * '\t' + '<idno subtype="geonames">' + re.sub(r'\s+', ' ', m_idno.group(1)) + '</idno>\n'
    p_new = re.sub(re.escape(p[1]), new, p[0], flags=re.S)
    s = re.sub(re.escape(p[0]), p_new, s, flags=re.S)

s = re.sub(r'\s*(</place>)', r'\n\t\t\t\1', s, flags=re.S)
s = re.sub(r'(<geo>)', r'\n\t\t\t\t\t\1', s, flags=re.S)
s = re.sub(r'(</geo>)', r'\1\n\t\t\t\t', s, flags=re.S)

with open(path, 'w') as fo: fo.write(s)
