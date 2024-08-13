#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" «Heinrich Bullinger» tagger (inc. common aliasses) """

rs = '\[?\]?\(?\)?'
r_ = r"Henricus Bullingerus der Ältere|Heinrich Bullingerus der Ältere|Heinrich Bullinger der Ältere|Henricus Bullinger der Ältere|Heinrich Bullingerus d\.Ä\.|Henricus Bullingerus d\.Ä\.|H\. Bullinger|Heynrichen Bullinger|H\. Bullinger|Heinrich Bullinger|Heinrich Bullinger d\.Ä\.|Henricus Bullinger d\.Ä\.|H. Bullingerus|Heinrychus Bullingerus|H\. Bullingero|Heinrychen Bullingero|Heinrichen Bullingero|H\. Bullingeri|Heinrychi Bullingeri|Heinricho Bullingero|Heinrychen Bullinger|Heinrycho Bullingero|Heinrich Bullingerus|Henricus Bullingerus|Henrycus Bullingerus|Heinricus Bulingerus|Heinrich Buellinger|Henrico Bullingero|Heinrich Bullinger|Henricus Bullinger|Heinrych Bullinger|H. Bullynger|Heinrich Bullynger|Enrico Bullingero|Enrico Bullinger|Octavius Florens|Henrik Bullinger|H\. Bullingere|Henry Bullingere|Henry Bullinger|H\. Bulinger|Henri Bulinger|Henry Bulinger|Henry Bulliger|Bullingerus|Bulingerus|Bullingere|Bullingero|Bullingers|Bullinger|Bullynger|Bulingero|Bulinger"
r0 = ''.join([c for c in r_])
print(r0)
def hb_tagger(s):
    nes = {}
    for i, p in enumerate(re.findall(r'<persName.*?</persName>', s, flags=re.S)):
        esc_seq = r'@@@'+str(i)+'@@@'
        s = re.sub(re.escape(p), esc_seq, s, flags=re.S)
        nes[esc_seq] = p
    s = re.sub(r'('+r0+r')', r'<persName ref="p495" type="auto_name">\1</persName>', s, flags=re.S) # tag
    for esc_seq in nes: s = re.sub(re.escape(esc_seq), nes[esc_seq], s, flags=re.S)
    return s


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*source="keine".*', s, flags=re.S):
            print("Tagging", f)
            m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
            m_letter = re.match(r'.*(<text.*?</text>).*', s, flags=re.S)
            if m_regest: s = re.sub(re.escape(m_regest.group(1)), hb_tagger(m_regest.group(1)), s, flags=re.S)
            if m_letter: s = re.sub(re.escape(m_letter.group(1)), hb_tagger(m_letter.group(1)), s, flags=re.S)
            with open(p, 'w') as fo: fo.write(s)
