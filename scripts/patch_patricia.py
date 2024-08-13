#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" adds footnote types (bio/lex) """


ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()

        s = re.sub(r'<placeName ref="l7" cert="high">D', '<placeName ref="l2498" cert="high">D', s, flags=re.S)
        s = re.sub(r'(<placeName ref=")l35(" cert="high">(Ö|A))', r'\1l2560\2', s, flags=re.S)
        s = re.sub(r'<placeName ref="l11"', r'<placeName ref="l2464"', s, flags=re.S)
        s = re.sub(r'<placeName ref="l9" cert="high">E', r'<placeName ref="l830" cert="high">E', s, flags=re.S)
        s = re.sub(r'<placeName ref="l9" cert="high">J', r'<placeName ref="l830" cert="high">J', s, flags=re.S)
        s = re.sub(
            r'(<placeName ref=")l1976((" cert="high"|)>(Augsburg|Augspurg|Augsburger|Augsburgs)</placeName>)',
            r'\1l18\2', s, flags=re.S)
        s = re.sub(r'<placeName ref="l910"', r'<placeName ref="l21"', s, flags=re.S)
        s = re.sub(r'(<persName[^>]*ref=)"p20225"', r'\1"p7637"', s, flags=re.S)
        s = re.sub(
            r'<placeName ref="l20" cert="high"><orig>Backnang</orig></placeName>',
            r'<placeName ref="l2326" cert="high"><orig>Backnang</orig></placeName>', s, flags=re.S)
        s = re.sub(r'<placeName ref="l473"', r'<placeName ref="l474"', s, flags=re.S)
        s = re.sub(r'"l(15|16)("[^>]*>A)', r'"l15\2', s, flags=re.S)
        s = re.sub(r'"l(15|16)("[^>]*>I)', r'"l834\2', s, flags=re.S)
        s = re.sub(r'(<persName[^>]*ref=)"p18574"', r'\1"p3590"', s, flags=re.S)

        with open(p, 'w') as fo: fo.write(s)
