#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" adds footnotes refering to metadata """

data = {}
with open("scripts/src/fn_meta.csv") as fi:
    for line in fi:
        t = line.strip().split("__")
        if t[0] in data: data[t[0]].append((t[1], t[2]))
        else: data[t[0]] = [(t[1], t[2])]

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f) and f in data:
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        # if not len(re.findall(r'<text xml:lang', s, flags=re.S)) == 1: print("Warning:", p)
        for t in reversed(data[f]):
            if not re.match(r'.*<note xml:id="fn'+t[0]+'".*', s, flags=re.S):
                s = re.sub(r'(\n(\s*)<text xml:lang[^>]*>[ ]*\n)', r'\1\2'+'\t'+'<note xml:id="fn'+t[0]+'" type="footnote" subtype="metadata" n="'+t[0]+'">'+t[1]+'</note>\n', s, flags=re.S)
        for x in re.findall(r'(<fl alt="([^"]*)">([^<]*)</fl>)', s, flags=re.S):
            s = re.sub(re.escape(x[0]), r'<ptr target="fn' + x[2] + '" ' + 'type="footnote" n="' + x[2] + '" sameAs="'+x[1]+'"/>', s, flags=re.S)
        for x in re.findall(r'(<fl>([^<]*)</fl>)', s, flags=re.S):
            s = re.sub(re.escape(x[0]), r'<ptr target="fn' + x[1] + '" ' + 'type="footnote" n="' + x[1] + '"/>', s, flags=re.S)
        s = re.sub(r'(<cit[^>]*>)([^<]*)(</cit>)', r'\1<ref>\2</ref>\3', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
