#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


with open("scripts/notes.csv") as fi:
    for line in fi:
        data  = line.strip().split(",\t")
        f_id = data[0]
        note = re.sub(r'\s*<br\s*/>\s*', ' ', data[2], flags=re.S)
        note = re.sub(r'\s+', ' ', note, flags=re.S)
        if re.match(r'.*[Ii]nterna.*', note, flags=re.S):
            print(data[0], '\t', note)

