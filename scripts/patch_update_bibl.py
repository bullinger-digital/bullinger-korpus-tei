#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


bib, SRC_PATH = {}, "scripts/src/text_bib.csv"
with open(SRC_PATH) as fi:
    for line in fi:
        t = line.strip().split(',\t')
        bib[t[0]] = { # id_file
            "id_edition": t[2],
            "fk_bib": t[3],
            "page": t[4] if len(t)>4 else '',
            "orig": t[1]
        }

ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        f_id = re.match(r'(\d+)\.xml', f).group(1)
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_n = re.match(r'.*<TEI[^>]*n="([^"]*)".*', s, flags=re.S)
        n = m_n.group(1) if m_n else ''
        s = re.sub(r'<bibl n="(\d+)" type="(transcription)">.*?</bibl>', r'<bibl ref="\1" n="" type="\2"/>', s, flags=re.S)
        s = re.sub(r'<bibl n="(\d+)" type="(regest)">.*?</bibl>', r'<bibl ref="\1" n="" type="\2"/>', s, flags=re.S)
        s = re.sub(r'<bibl n="(\d+)" type="(footnotes)">.*?</bibl>', r'<bibl ref="\1" n="" type="\2"/>', s, flags=re.S)
        if not re.match(r'.*<TEI[^>]*source="(keine|HTR)".*', s, flags=re.S):
            s = re.sub(r'(<bibl ref="[^"]*" n=)""( type="transcription")', r'\1"'+n+r'"\2', s, flags=re.S)
            if f_id in bib:
                if bib[f_id]["orig"] == "HBBW" and bib[f_id]["id_edition"]:
                    s = re.sub(r'(<bibl ref="\d*" n=)""( type="(regest|footnotes)"/>)', r'\1"'+bib[f_id]["id_edition"]+r'"\2', s, flags=re.S)
        s = re.sub(r'(<bibl ref="\d*" n=)""( type="(regest|footnotes)"/>)', r'\1"'+n+r'"\2', s, flags=re.S)
        if f_id in bib and bib[f_id]["id_edition"]:
            s = re.sub(r'(<bibl ref="\d*" n=)""( type="(regest|footnotes)"/>)', r'\1"' + bib[f_id]["id_edition"] + r'"\2', s, flags=re.S)
        if re.match(r'.*<TEI[^>]*source="(keine|HTR)".*', s, flags=re.S):
            if f_id in bib and bib[f_id]["id_edition"]:
                s = re.sub(r'(<bibl ref="45" n=)""( type="transcription"/>)', r'\1"' + bib[f_id]["id_edition"] + r'"\2', s, flags=re.S)

        with open(p, 'w') as fo: fo.write(s)
