#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

"""" validate organizations (resp. their IDs) """


# orgs
with open("data/index/organizations.xml") as fi: s = fi.read()
obase = {i[0]: i[1] for i in re.findall(r'<orgName xml:id="(\w\w\d+\w)" xml:lang="de">([^>]*)</orgName>', s, flags=re.S)}
orgs = {i: True for i in re.findall(r'<orgName xml:id="([^"]*)"', s, flags=re.S)}

# places
with open("data/index/localities.xml") as fi: s = fi.read()
places = {p[0]: p[1] for p in re.findall(r'<place xml:id="([^"]*)"[^>]*>\s*<[^>]*>([^<]*)<', s, flags=re.S)}

missing = dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    mf = re.match(r'(.*)\.xml', f)
    if mf:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for i in re.findall(r'<orgName[^>]*ref="([^"]*)"', s, flags=re.S):
            if i not in orgs: missing[i] = 1

#for i in obase: print(i, obase[i])
#for i in places: print(i, places[i])
for i in missing:
    m = re.match(r'(\w\w\d+\w)(l\d+)', i)
    if m:
        id_org = m.group(1)
        id_place = m.group(2)
        if id_org in orgs and id_place in places:
            entry = '<orgName xml:id="'+id_org+id_place+'" xml:lang="de">'+obase[id_org]+' von <placeName ref="'+id_place+'">'+places[id_place]+'</placeName></orgName>'
            print(entry)
        else:
            if id_org not in orgs: print("org", id_org, "missing")
            if id_place not in places: print("place", id_place, "missing")
    else: print("Warning: invalid pattern", i)

"""



place l492 missing
place l389 missing

place l1 missing
place l373 missing
place l474 missing
place l882 missing
place l425 missing
place l492 missing
place l389 missing
place l862 missing
place l841 missing
place l882 missing
place l869 missing
place l474 missing
place l474 missing
place l532 missing
place l474 missing
place l335 missing
place l335 missing

og49pl1
oi12sl373
oi12sl57
oi25sl587
oi19sl587
og49pl544
oi20sl159
oi15sl487
oi29sl28
oi15sl2
oi14sl70
oi30sl339
oi25sl474
oi19pl882
oi27sl41
oi27sl587
oi21sl167
oi19sl280
oi34sl280
oi3sl294
oi7sl157
oi3sl673
oi32sl673
oi22sl425
oi6sl167
oi11sl167
oi6sl157
oi19sl492
oi25sl98
oi25sl260
oi25sl389
oi33pl587
oi19sl441
oi19sl294
oi19pl862
oi19sl852
oi19sl841
oi19sl859
oi19sl882
oi19sl869
oi18sl587
oi12pl260
oi2sl296
oi3sl242
oi25sl274
oi25sl272
og80pl215
oi19sl474
oi22sl474
oi3sl25
oi24sl532
og25pl822
oi19pl41
oi19pl441
oi19pl474
oi19pl335
oi19pl98
oi19sl335
"""
