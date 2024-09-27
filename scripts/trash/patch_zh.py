#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" rm auto_name zh in fns """

def tag_zh_in_fns(s):
    m = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
    if m:
        s_ = m.group(1)
        for fn in re.findall(r'<note[^>]*type="footnote"[^>]*>.*?</note>', s_, flags=re.S):
            fn_ = re.sub(r"Zürich", r'<placeName ref="l587" cert="high">Zürich</placeName>', fn, flags=re.S)
            fn_ = re.sub(r'<placeName ref="l587"[^>]*>([^<]*[\.\,]\s*Zürich\s*\d{4}[^<]*)</placeName>', r'\1', fn_, flags=re.S)
            fn_ = re.sub(r'<placeName ref="l587"[^>]*>([^<]*Zürich\s*(StA|ZB)[^<]*)</placeName>', r'\1', fn_, flags=re.S)
            s_ = re.sub(re.escape(fn), fn_, s_, flags=re.S)
        s = re.sub(re.escape(m.group(1)), s_, s, flags=re.S)
        s = re.sub(r'(<placeName[^>]*>[^<]*)<placeName[^>]*>([^<]*)</placeName>([^<]*</placeName>)', r'\1\2\3', s, flags=re.S)
    return s

def rm_placename_zh(s):
    s = re.sub(r'([^<]*[\.\,]\s*)<placeName ref="l587" type="auto_name">(Zürich)</placeName>(\s*\d{4}[^<]*)', r'\1\2\3', s, flags=re.S)
    s = re.sub(r'([^<]*)<placeName ref="l587" type="auto_name">(Zürich)</placeName>(\s*(StA|ZB)[^<]*)', r'\1\2\3', s, flags=re.S)
    return s

def verify_zh(s):
    s = re.sub(
        r'<placeName ref="l587" type="auto_name">',
        r'<placeName ref="l587" type="auto_name" cert="high">', s, flags=re.S)
    s = re.sub(
        r'<placeName ref="l587">',
        r'<placeName ref="l587" cert="high">', s, flags=re.S)
    s = re.sub(
        r'(<placeName[^>]*?ref="l587"[^>]*?cert=")[^"]*("[^>]*?>)',
        r'\1high\2', s, flags=re.S)
    s = re.sub(
        r'(<placeName[^>]*?cert=")[^"]*("[^>]*?ref="l587"[^>]*?>)',
        r'\1high\2', s, flags=re.S)
    return s

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        """
        for fn in re.findall(r'<note[^>]*type="footnote".*?</note>', s, flags=re.S): s = re.sub(re.escape(fn), rm_placename_zh(fn), s, flags=re.S)
        m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
        m_letter = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
        if m_regest: s = re.sub(re.escape(m_regest.group(1)), verify_zh(m_regest.group(1)), s, flags=re.S)
        if m_letter: s = re.sub(re.escape(m_letter.group(1)), verify_zh(m_letter.group(1)), s, flags=re.S)
        """
        s = tag_zh_in_fns(s)
        with open(p, 'w') as fo: fo.write(s)
