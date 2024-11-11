#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" ZH: verification; rm auto_name-tags in fns; rm tags in special contexts; new tagging; minor corrections """

# Verification
def verify_zh(s):
    s = re.sub(r'<placeName ref="l587" type="auto_name">', r'<placeName ref="l587" type="auto_name" cert="high">', s, flags=re.S)
    s = re.sub(r'<placeName ref="l587">', r'<placeName ref="l587" cert="high">', s, flags=re.S)
    s = re.sub(r'(<placeName[^>]*?ref="l587"[^>]*?cert=")[^"]*("[^>]*?>)', r'\1high\2', s, flags=re.S)
    s = re.sub(r'(<placeName[^>]*?cert=")[^"]*("[^>]*?ref="l587"[^>]*?>)', r'\1high\2', s, flags=re.S)
    return s

# rm tags
def rm_placename_zh(s):
    s = re.sub(r'([^<]*[\.\,]\s*)<placeName ref="l587"[^>]*>(Zürich)</placeName>(\s*\d{4}[^<]*)', r'\1\2\3', s, flags=re.S)
    s = re.sub(r'([^<]*)<placeName ref="l587"[^>]*>(Zürich)</placeName>(\s*(StA|ZB)[^<]*)', r'\1\2\3', s, flags=re.S)
    return s

# add tags
r0 = r"Zürich[a-z]*|Tyguri[a-z]*|Zurch[a-z]*"
def zh_tagger(s):
    nes = {}
    for i, p in enumerate(re.findall(r'(<placeName[^>]*>[^<]*</placeName>|<pb[^>]*?>)', s, flags=re.S)):
        esc_seq = r'@@@'+str(i)+'@@@'
        s = re.sub(re.escape(p), esc_seq, s, flags=re.S)
        nes[esc_seq] = p
    s = re.sub(r'('+r0+r')', r'<placeName ref="l587" cert="high">\1</placeName>', s, flags=re.S) # tag
    for esc_seq in nes: s = re.sub(re.escape(esc_seq), nes[esc_seq], s, flags=re.S)
    return s

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*source="keine".*', s, flags=re.S):
            m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
            if m_regest:
                s = re.sub(re.escape(m_regest.group(1)), rm_placename_zh(verify_zh(zh_tagger(m_regest.group(1)))), s, flags=re.S)
                with open(p, 'w') as fo: fo.write(s)
