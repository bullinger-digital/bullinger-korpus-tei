#!/usr/bin/python
# -*- coding: utf8 -*-
import re, os


ROOT, count = "data/letters/", 0
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*(<additional>.*?</additional>).*', s, flags=re.S)
        if m:
            for e in re.findall(r'(<bibl type="([^"]*)".*?</bibl>)', m.group(1), flags=re.S):
                if re.match(r'.*[Ii]nterna.*', e[0], flags=re.S):
                    count += 1
                    print(f.strip('.xml')+'\t'+e[1]+'\t'+re.match(r'.*<title>(.*)</title>.*', e[0], flags=re.S).group(1))
                    s = re.sub(re.escape(e[0]), '', s, flags=re.S)
                    s = re.sub(r'<listBibl>\s*</listBibl>', '', s, flags=re.S)
                    s = re.sub(r'<additional>\s*</additional>', '', s, flags=re.S)
                    s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)

        with open(p, 'w') as fo: fo.write(s)
