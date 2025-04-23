#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


PATH = "data/index/persons.xml"
with open(PATH) as fi: s = fi.read()
s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
with open(PATH, 'w') as fo: fo.write(s)
