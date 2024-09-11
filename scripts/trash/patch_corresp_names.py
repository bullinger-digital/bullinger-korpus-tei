#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

# read data
# - persons
persons = dict()
with open("data/index/persons.xml") as fi: s = fi.read()
# -- small corrections
s = re.sub(r'(<surname>)\s*([^<]*)\s*(</surname>)', r'\1\2\3', s, flags=re.S)
s = re.sub(r'(<forename>)\s*([^<]*)\s*(</forename>)', r'\1\2\3', s, flags=re.S)
with open("data/index/persons.xml", 'w') as fo: fo.write(s)
for p in re.findall(r'<persName xml:id="p(\d+)" ref="p(\d+)" type="main">\s*<surname>([^<]*)</surname>\s*<forename>([^<]*)</forename>\s*</persName>', s, flags=re.S): persons[p[0]] = ' '.join([p[3], p[2]])
for p in re.findall(r'<persName xml:id="p(\d+)" ref="p(\d+)" type="main">\s*<surname>([^<]*)</surname>\s*<forename\s*/>\s*</persName>', s, flags=re.S): persons[p[0]] = ' '.join([p[2]])
for p in re.findall(r'<persName xml:id="p(\d+)" ref="p(\d+)" type="main">\s*<surname>([^<]*)</surname>\s*</persName>', s, flags=re.S): persons[p[0]] = ' '.join([p[2]])
for p in re.findall(r'<persName xml:id="p(\d+)" ref="p(\d+)" type="alias">\s*<surname>([^<]*)</surname>\s*<forename>([^<]*)</forename>\s*</persName>', s, flags=re.S): persons[p[0]] = persons[p[1]]

# - roles
roles = dict()
with open("data/index/groups.xml") as fi: s = fi.read()
for g in re.findall(r'<nym xml:id="g(\d+)"(.*?)</nym>', s, flags=re.S):
    m = re.match(r'.*<form xml:lang="de" type="sg">([^<]*)</form>.*', g[1], flags=re.S)
    if m: roles[g[0]] = m.group(1)

# - organizations
orgs = dict()
with open('data/index/organizations.xml') as fi: s = fi.read()
for x in re.findall(r'<orgName xml:id="([^"]*)" xml:lang="de">(.*?)</orgName>', s, flags=re.S):
    orgs[x[0]] = x[1]

missing = dict()
# - MISSING ORGANIZATIONS
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for b in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
            for x in re.findall(r'((<orgName ref="([^"]*)"[^>]*)\s*/>)', b, flags=re.S):
                if x[2] not in orgs: missing[x[2]] = True
# - places
places = dict()
with open(r'data/index/localities.xml') as fi: s = fi.read()
for x in re.findall(r'<place xml:id="l(\d+)"[^>]*>(.*?)</place>', s, flags=re.S):
    ms = re.match(r'.*<settlement>([^<]*)</settlement>.*', x[1], flags=re.S)
    md = re.match(r'.*<district>([^<]*)</district>.*', x[1], flags=re.S)
    mc = re.match(r'.*<country>([^<]*)</country>.*', x[1], flags=re.S)
    if ms: places[x[0]] = ms.group(1)
    elif md: places[x[0]] = md.group(1)
    elif mc: places[x[0]] = mc.group(1)

institutions_s = dict()
institutions_p = dict()
with open(r'data/index/institutions.xml') as fi: s = fi.read()
for x in re.findall(r'<org xml:id="i(\d+)">(.*?)</org>', s, flags=re.S):
    ms = re.match(r'.*<name xml:lang="de" type="sg">(.*?)</name>.*', x[1], flags=re.S)
    if ms: institutions_s[x[0]] = ms.group(1)
    mp = re.match(r'.*<name xml:lang="de" type="pl">(.*?)</name>.*', x[1], flags=re.S)
    if mp: institutions_p[x[0]] = mp.group(1)

#print("S-institutions")
#for x in institutions_s: print(x, institutions_s[x])
#print("P-institutions")
#for x in institutions_p: print(x, institutions_p[x])

new_orgs = dict()
for m in missing:
    ms = re.match(r'oi(\d+)sl(\d+)', m, flags=re.S)
    mp = re.match(r'oi(\d+)pl(\d+)', m, flags=re.S)
    if not ms and not mp: print("*Warning,", m, "invalid")
    elif ms:
        id_ = 'oi'+ms.group(1)+'sl'+ms.group(2)
        if ms.group(1) not in institutions_s: print("s-institution does not exist:", ms.group(1))
        if ms.group(2) not in places: print("place", ms.group(2), "does not exist")
        new_orgs[id_] = '<orgName xml:id="'+id_+'" xml:lang="de">'+institutions_s[ms.group(1)]+' von '+'<placeName ref="l'+ms.group(2)+'">'+places[ms.group(2)]+'</placeName></orgName>'
    elif mp:
        id_ = 'oi'+mp.group(1)+'pl'+mp.group(2)
        if mp.group(1) not in institutions_p: print("p-institution does not exist:", mp.group(1))
        if mp.group(2) not in places: print("place", mp.group(2), "does not exist")
        new_orgs[id_] = '<orgName xml:id="'+id_+'" xml:lang="de">'+institutions_p[mp.group(1)]+' von '+'<placeName ref="l'+mp.group(2)+'">'+places[mp.group(2)]+'</placeName></orgName>'

# add missing orgs to register
id_org_main = dict()
with open('data/index/organizations.xml') as fi: s = fi.read()
for x in re.findall(r'<org xml:id="([^"]*)"', s, flags=re.S):
    id_org_main[x] = True

for n in new_orgs:
    m_id = re.match(r'oi(\d+)([ps])l(\d+)', n, flags=re.S)
    if not m_id: print("Warning, invalid id:", m_id.group(1))
    else:
        test_id = "Oi"+m_id.group(1) + m_id.group(2)
        if test_id not in id_org_main: print("Add new main entry to orgs:", test_id) # -> none
        else:
            s = re.sub(
                r'(<org xml:id="'+test_id+'"[^>]*>.*?\n)(\t\t\t</org>)',
                r'\1\t\t\t\t'+new_orgs[n].strip()+r'\n\2', s, flags=re.S
            )
s = re.sub(r'\n\s*\n', r'\n', s, flags=re.S)
with open('data/index/organizations.xml', 'w') as fo: fo.write(s)

# re-read orgs
orgs = dict()
with open('data/index/organizations.xml') as fi: s = fi.read()
for x in re.findall(r'<orgName xml:id="([^"]*)" xml:lang="de">(.*?)</orgName>', s, flags=re.S):
    orgs[x[0]] = x[1]

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for b in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
            b_ = b
            for x in re.findall(r'((<persName ref="p(\d+)"[^>]*)\s*/>)', b_, flags=re.S):
                b_ = re.sub(re.escape(x[0]), x[1]+'>'+persons[x[2]]+'</persName>', b_, flags=re.S)
            for x in re.findall(r'((<orgName ref="([^"]*)"[^>]*)\s*/>)', b_, flags=re.S):
                if x[2] not in orgs: print("Warning:", x[2], "is invalid")
                else: b_ = re.sub(re.escape(x[0]), x[1]+'>'+orgs[x[2]]+'</orgName>', b_, flags=re.S)
            for x in re.findall(r'(\n([\t ]*)(<persName ref="p(\d+)"[^>/]*>)\s*(<roleName ref="g(\d+)"[^>]*)/>\s*(</persName>))', b_, flags=re.S):
                if x[3] not in persons: print("Unknown person:", x[4], "in file", f)
                elif x[5] not in roles: print("Unknown role:", x[6], "in file", f)
                else:
                    b_ = re.sub(
                        re.escape(x[0]),
                        '\n'+x[1]+x[2]+'\n'+x[1]+'\t'+x[4]+'>'+roles[x[5]]+'</roleName>\n'+x[1]+'\t'+persons[x[3]]+'\n'+x[1]+x[6],
                        b_, flags=re.S
                    )
            s = re.sub(re.escape(b), b_, s, flags=re.S)

        with open(p, 'w') as fo: fo.write(s)


"""
					<persName ref="p2680" cert="low">
						<roleName ref="g49" cert="low"/>
				</persName>

"""