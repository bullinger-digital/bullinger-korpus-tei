#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" verifies persname-elements in letters with state="finished" """

def verify_bullinger(s):
    s = re.sub(
        r'<persName ref="p495" type="auto_name">',
        r'<persName ref="p495" type="auto_name" cert="high">', s, flags=re.S)
    s = re.sub(
        r'<persName ref="p495">',
        r'<persName ref="p495" cert="high">', s, flags=re.S)
    s = re.sub(
        r'(<persName[^>]*?ref="p495"[^>]*?cert=")[^"]*("[^>]*?>)',
        r'\1high\2', s, flags=re.S)
    s = re.sub(
        r'(<persName[^>]*?cert=")[^"]*("[^>]*?ref="p495"[^>]*?>)',
        r'\1high\2', s, flags=re.S)
    return s


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*<revisionDesc[^>]*?status="([^"]*)".*', s, flags=re.S)
        if m and m.group(1) == "finished":
            m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
            m_letter = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
            if m_regest: s = re.sub(re.escape(m_regest.group(1)), verify_bullinger(m_regest.group(1)), s, flags=re.S)
            if m_letter: s = re.sub(re.escape(m_letter.group(1)), verify_bullinger(m_letter.group(1)), s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)


