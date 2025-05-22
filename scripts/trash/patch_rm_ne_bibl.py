#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


def rm_nes(s):
    for b in re.findall(r'<bibl[^>]*>.*?</bibl>', s, flags=re.S):
        b_new = re.sub(r'</?(pers|place)Name[^>]*>', '', b, flags=re.S)
        s = re.sub(re.escape(b), b_new, s, flags=re.S)
    return s


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
        if m_regest:
            regest = m_regest.group(1)
            regest_new = rm_nes(regest)
            s = re.sub(re.escape(regest), regest_new, s, flags=re.S)
        m_letter = re.match(r'.*(<text.*?</text>)', s, flags=re.S)
        if m_letter:
            letter = m_letter.group(1)
            letter_new = rm_nes(letter)
            s = re.sub(re.escape(letter), letter_new, s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s)
