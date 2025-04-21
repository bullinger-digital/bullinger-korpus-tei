#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_letter = re.match(r'.*(<body>.*?</body>).*', s, flags=re.S)
        if m_letter:
            letter = m_letter.group(1)
            letter = re.sub(r'(<persName[^>]*)\s+cert="[^"]*"', r'\1', letter, flags=re.S)
            letter = re.sub(r'(<placeName[^>]*)\s+cert="[^"]*"', r'\1', letter, flags=re.S)
            s = re.sub(re.escape(m_letter.group(1)), letter, s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)