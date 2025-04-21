#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


SRC, ids = "scripts/tex2tei/output/", {}
TAR = "data/letters/"
for f in os.listdir(SRC):
    old_path = os.path.join(SRC, f)
    if os.path.exists(old_path):
        shutil.copy2(old_path, TAR)
