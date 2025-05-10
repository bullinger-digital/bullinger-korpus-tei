#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re



ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        # icl
        s = re.sub(
            r'<idno subtype="url">https://www\.bullinger\-digital\.ch/</idno>',
            r'<idno type="url" subtype="icl">https://www.bullinger-digital.ch/letter/'+f.strip('.xml')+'</idno>',
            s, flags=re.S)
        s = re.sub(r'(<correspDesc) ref=".*?(>)', r'\1\2', s, flags=re.S)
        # irg
        num = ''
        m_t = re.match(r'.*?<bibl source="b(\d+)" n="([^"]*)" type="transcription"/>.*', s, flags=re.S)
        m_r = re.match(r'.*?<bibl source="b(\d+)" n="([^"]*)" type="regest"/>.*', s, flags=re.S)
        m_f = re.match(r'.*?<bibl source="b(\d+)" n="([^"]*)" type="footnotes"/>.*', s, flags=re.S)
        for m in [m_t, m_r, m_f]:
            if m:
                if int(m.group(1)) < 25 or int(m.group(1)) == 720 and m.group(2) and not num:
                    num = m.group(2)
        if num:
            s = re.sub(
                r'(<idno type="url" subtype="icl">.*?</idno>)',
                r'\1\n\t\t\t\t<idno type="url" subtype="irg">http://teoirgsed.uzh.ch/SedWEB.cgi?fld_418='+num+'</idno>',
                s, flags=re.S
            )
        with open(p, 'w') as fo: fo.write(s)
