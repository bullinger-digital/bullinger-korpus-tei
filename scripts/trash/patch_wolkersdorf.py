#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" Wolkersdorf, Hessen (DE) """

# register
path = "data/index/localities.xml"
with open(path) as fi: s = fi.read()
id_new = str(max([int(e) for e in re.findall(r'<place xml:id="l(\d+)"', s, flags=re.S)])+1)
s = re.sub(
    r'(</place>\n)(\s*</listPlace>)',
    r'\1\t\t\t<place xml:id="l'+id_new+'">\n'+
    r'\t\t\t\t<settlement>Wolkersdorf</settlement>\n'+
	r'\t\t\t\t<district>Hessen</district>\n'+
	r'\t\t\t\t<country>Deutschland</country>\n'+
	r'\t\t\t\t<location>\n'+
	r'\t\t\t\t\t<geo>51.019347 8.806678</geo>\n'+
	r'\t\t\t\t</location>\n'+
    r'\t\t\t</place>\n\2',
    s, flags=re.S
)
with open(path, 'w') as fo: fo.write(s)


ROOT = 'data/letters'
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*source="keine".*', s, flags=re.S):
            s = re.sub(r'(ref=")l1843(")', r'\1l'+id_new+r'\2', s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)
