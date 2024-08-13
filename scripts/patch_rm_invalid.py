#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" delete invalid files """

invalid_file_ids = [1866, 1898, 2016, 5165, 5672, 8048, 8049, 9649]
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    for i in invalid_file_ids:
        if re.match(r'^'+str(i)+r'\.xml$', f):
            p = os.path.join(ROOT, f)
            os.remove(p)
