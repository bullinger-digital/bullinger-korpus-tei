#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(
            '([\t ]*<bibl)(>Heinrich Bullinger Werke, Briefwechsel Band 21 \(Briefe von Januar bis April 1548\),)\s*(bearb. von David Mache und Paul Achim Neuendorf, Zürich 2024, 504 S., ISBN 978-3-290-18668-5.</bibl>)',
            r'\1 n="720" type="transcription"\2 \3\n\1 n="720" type="regest"\2 \3\n\1 n="720" type="footnotes"\2 \3',
            s, flags=re.S
        )
        with open(p, 'w') as fo: fo.write(s)