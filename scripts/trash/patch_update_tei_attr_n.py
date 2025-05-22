#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        # remove invalid sub-IDs
        s = re.sub(
            r'(<idno subtype="url" resp="irg">[^<]*=\d+)[a-z]+(</idno>)',
            r'\1\2', s, flags=re.S
        )
        m = re.match(r'.*?<idno subtype="url" resp="irg">[^<]*=(\d+)</idno>.*', s, flags=re.S)
        if m: s = re.sub( r'(<TEI [^>]* n=)"[^"]*"', r'\1"'+m.group(1)+r'"', s, flags=re.S)
        else: s = re.sub(r'(<TEI [^>]* n=")[^"]*(")', r'\1\2', s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
