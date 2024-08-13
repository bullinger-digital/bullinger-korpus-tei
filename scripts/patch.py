#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" bugfixes """

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        nrs = dict()
        for n in re.findall(r'<note xml:id="fn(\d+)"', s, flags=re.S):
            if f in nrs: nrs[f] += [int(n)]
            else: nrs[f] = [int(n)]
        if f in nrs:
            min_ = min(nrs[f])
            max_ = max(nrs[f])
            for i in range(min_, max_+1):
                if i not in nrs[f]: print("Warning,", i, "missing in", f)
        """
        s = re.sub(r'(<persName[^>]*ref=")l', r'\1p', s, flags=re.S)
        s = re.sub(r'(<placeName ref=")p', r'\1l', s, flags=re.S)
        s = re.sub(r'<persName ref="p9780"', r'<persName ref="p9708"', s, flags=re.S)
        s = re.sub(
            r'<persName ref="p1052" cert="high">Ellicken</persName>',
            r'<placeName ref="l1052" cert="high">Ellicken</placeName>',
            s, flags=re.S
        )
        with open(p, 'w') as fo: fo.write(s)
        """
