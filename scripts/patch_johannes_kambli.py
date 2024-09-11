#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" new correspondet «Johannes Kambli» """

# index
with open("data/index/persons.xml") as fi: s = fi.read()
new_id = max([int(i) for i in re.findall(r'xml:id="P(\d+)"', s, flags=re.S)])+1
new_entry = \
'\t\t\t<person xml:id="P'+str(new_id)+'" change="pending">\n\
\t\t\t\t<persName ref="p'+str(new_id)+'" type="main">\n\
\t\t\t\t\t<surname>Kamlbi</surname>\n\
\t\t\t\t\t<forename>Johannes</forename>\n\
\t\t\t\t</persName>\n\
\t\t\t</person>\n'
s = re.sub(r'(.*</person>[\t ]*\n)', r'\1'+new_entry, s, flags=re.S)
with open("data/index/persons.xml", 'w') as fo: fo.write(s)

# letters
ROOT = "data/letters/"
for f in ["9008", "9928", "9988"]:
    p = os.path.join(ROOT, f) + '.xml'
    with open(p) as fi: s = fi.read()
    for c in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
        c_ = re.sub(r'<persName ref="p8392"', r'<persName ref="p'+str(new_id)+'"', c, flags=re.S)
        s = re.sub(re.escape(c), c_, s, flags=re.S)
    with open(p, 'w') as fo: fo.write(s)
