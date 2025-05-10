#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


data = {}
with open("scripts/src/page_number_regests.csv") as fi:
    for line in fi:
        t = line.strip('\n').split(",\t")
        if t[0] not in data: data[t[0]] = []
        data[t[0]].append({ "fk_bib": t[1], "num": t[2], "page": t[3] if len(t) > 3 else '' })

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match('.*<bibl source="b(\d+)" n="([^"]*)" type="regest"/>', s, flags=re.S)
        if m:
            f_id = f.strip('.xml')
            fk_bib = m.group(1)
            num = m.group(2)
            if f_id in data:
                for t in data[f_id]:
                    if fk_bib == t["fk_bib"]:
                        if num != t["num"] or (not num and t["num"]):
                            s = re.sub(
                                r'(<bibl source="b\d+" n=)"[^"]*"( type="regest"/>)',
                                r'\1"'+t["num"]+r'"\2', s, flags=re.S
                            )
                        if t["page"]:
                            s = re.sub(
                                r'(<bibl source="b\d+" n="[^"]*" type="regest")/>',
                                r'\1>S. '+t["page"]+'</bibl>', s, flags=re.S
                            )
        with open(p, 'w') as fo: fo.write(s)
