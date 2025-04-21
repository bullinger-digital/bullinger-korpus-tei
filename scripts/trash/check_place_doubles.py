#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


with open("data/index/localities.xml") as fi: s = fi.read()

# idno-elements
nof_entries = len([p for p in re.findall(r'<place xml:id="l', s, flags=re.S)])  # 3454
nof_urls_geonames = len([url for url in re.findall(r'<idno subtype="geonames">.*?</idno>', s, flags=re.S)])  # 2448
nof_urls = len([url for url in re.findall(r'<idno.*?</idno>', s, flags=re.S)])  # 2449
if nof_urls - nof_urls_geonames > 1: print("*Warning, there might be doubles...")
'''
a = [url for url in re.findall(r'<idno subtype="geonames">.*?</idno>', s, flags=re.S)]
b = [url for url in re.findall(r'<idno.*?</idno>', s, flags=re.S)]
for p in b:
    if p not in a:
        print("***", p)  # <idno subtype="url">https://www.bullinger-digital.ch/</idno> --> ok
'''

entries = [e for e in re.findall(r'[\t ]*<place xml:id.*?</place>', s, flags=re.S)]


# urls
url_list = [url for url in re.findall(r'<idno subtype="geonames">(.*?)</idno>', s, flags=re.S)]
url_set = set(url_list)
print(len(url_set), len(url_list), len(url_list)-len(url_set))  # 2437 2448 11
# - doubles
doubles = [u for u in url_list if len(re.findall(re.escape(u), s, flags=re.S)) > 1]
fishy_entries = []
for d in doubles:
    multiples = []
    for e in entries:
        if d in e: multiples.append(e)
    if len(multiples)>1: fishy_entries.append(multiples)
watch_list = []
for m in fishy_entries:
    ids = []
    settlements = []
    districts = []
    countries = []
    for e in m:
        m_id = re.match(r'.*xml:id="([^"]*)".*', e, flags=re.S)
        m_settlement = re.match(r'.*<settlement>([^<]*)</settlement>.*', e, flags=re.S)
        m_district = re.match(r'.*<district>([^<]*)</district>.*', e, flags=re.S)
        m_country = re.match(r'.*<country>([^<]*)</country>.*', e, flags=re.S)
        if m_id: ids.append(m_id.group(1))
        if m_settlement: settlements.append(m_settlement.group(1))
        if m_district: districts.append(m_district.group(1))
        if m_country: countries.append(m_country.group(1))
    #print(ids, settlements, districts, countries)
    watch_list.append(
        ','.join(list(set(ids)))+' : '
        +' VS. '.join(list(set(settlements)))+' --- '
        + ' VS. '.join(list(set(districts)))+' --- '
        + ' VS. '.join(list(set(countries)))
    )

for e in set(watch_list): print(e)


"""
l3466,l2755 : Thur ---  --- Schweiz
l2854,l1377 : St. Fiden --- St. Gallen --- Schweiz
l2933,l2932 : Dillenburg --- Hessen --- Deutschland
l1893,l2171 : Wasselonne/Wasselnheim VS. Wasselnheim --- Gran Est VS. Grand Est --- Frankreich
l399,l911 : Poschiavo VS. Puschlav --- Graubünden --- Schweiz
l735,l734 : Ostfriesland --- Ost-Friesland VS. Niedersachsen --- Deutschland
l3654,l1013 : Saint-Hippolyte/St. Pilt VS. St. Pilt --- Grand-Est VS. Grand Est --- Frankreich
l648,l893 : Drei Bünde --- Graubünden --- Schweiz
l1216,l608 : Chevron VS. Aigle --- Aigle  VS. Vaud --- Schweiz
l173,l192 : Gyrenbad VS. Girenbad --- Zürich --- Schweiz
"""