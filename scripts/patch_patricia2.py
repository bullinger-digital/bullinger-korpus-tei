#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" individual changes """

# Date corrections #28
with open("data/letters/28.xml") as fi: s = fi.read()
s = re.sub(r'\[31\. Januar 1548\]</title>', r'[31. Januar 1547]</title>', s, flags=re.S)
s = re.sub(r'<date when="1548-01-31" cert="low"/>', r'<date when="1547-01-31" cert="low"/>', s, flags=re.S)
with open("data/letters/28.xml", 'w') as fo: fo.write(s)

# Correspondent correation #4440
with open("data/letters/4440.xml") as fi: s = fi.read()
s = re.sub(r'\s*<persName ref="p2757" cert="high">\s*<roleName ref="g49" cert="high"/>\s*</persName>', '', s, flags=re.S)
with open("data/letters/4440.xml", 'w') as fo: fo.write(s)

# Org-Split Geistliche von Bergell+Veltlin
with open("data/index/organizations.xml") as fi: s = fi.read()
s = re.sub(
    r'<orgName xml:id="og26pl902" xml:lang="de">Geistliche von <placeName ref="l902">Bergell und Veltlin</placeName></orgName>',
    r'<orgName xml:id="og26pl37" xml:lang="de">Geistliche von <placeName ref="l37">Bergell</placeName></orgName>\n\t\t\t\t<orgName xml:id="og26pl520" xml:lang="de">Geistliche von <placeName ref="l520">Veltlin</placeName></orgName>',
    s, flags=re.S
)
with open("data/index/organizations.xml", 'w') as fo: fo.write(s)
with open("data/letters/4815.xml") as fi: s = fi.read()
s = re.sub(
    r'<orgName ref="og26pl902" cert="low"/>',
    r'<orgName ref="og26pl37" cert="low"/>\n\t\t\t\t\t<orgName ref="og26pl520" cert="low"/>',
    s, flags=re.S
)
with open("data/letters/4815.xml", 'w') as fo: fo.write(s)

# Johannes Pontisella d.Ä.
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        if f != "9864.xml":
            with open(p) as fi: s = fi.read()
            if f == "8950.xml":
                s = re.sub(r'(<TEI[^>]*source=")TUSTEP(" n=")42108(")', r'\1keine\2\3', s, flags=re.S)
                s = re.sub(r'\s*<bibl n="45" type="transcription">Vorläufige Transkription der HBBW\-EditorInnen</bibl>', '', s, flags=re.S)
            for c in re.findall(r'<correspAction.*?</correspAction>', s, flags=re.S):
                c_ = re.sub(r'<persName ref="p2627"', r'<persName ref="p6130"', c, flags=re.S)
                s = re.sub(re.escape(c), c_, s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)
