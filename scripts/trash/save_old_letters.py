#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, shutil


SRC, ids = "scripts/tex2tei/output/", {}
OLD, TAR = "data/letters/", "scripts/save/"
for f in os.listdir(SRC):
    old_path = os.path.join(OLD, f)
    if os.path.exists(old_path):
        shutil.copy2(old_path, TAR)
