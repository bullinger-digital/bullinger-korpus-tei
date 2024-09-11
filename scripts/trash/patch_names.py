#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" map <placeName source= --> <placeName ref=
    and add missing letter (l/p) to place/person-name-IDs """

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<placeName[^>]*)source=', r'\1ref=', s, flags=re.S)
        s = re.sub(r'(<placeName[^>]*ref=")(\d)', r'\1l\2', s, flags=re.S)
        s = re.sub(r'(<persName[^>]*ref=")(\d)', r'\1p\2', s, flags=re.S)
        # special errors
        s = re.sub(
            r'<persName ref="p1052" cert="high">Ellicken</persName>',
            r'<placeName ref="l1052" cert="high">Ellicken</persName>',
            s, flags=re.S)
        s = re.sub(
            r'<persName ref="p296" cert="high">Londinum</persName>',
            r'<placeName ref="l296" cert="high">Londinum</placeName>',
            s, flags=re.S)
        s = re.sub(
            r'<persName ref="p555" cert="high">Wynterthur</persName>',
            r'<placeName ref="l555" cert="high">Wynterthur</placeName>',
            s, flags=re.S)
        s = re.sub(
            r'<persName ref="p2377" cert="high">Martin Mötteli</persName>',
            r'<persName ref="p2237" cert="high">Martin Mötteli</persName>',
            s, flags=re.S)
        s = re.sub(
            r'<persName ref="p1798" cert="high">Hansen Keßlers</persName>',
            r'<persName ref="p1789" cert="high">Hansen Keßlers</persName>',
            s, flags=re.S)
        s = re.sub(
            r'<persName ref="p1798" cert="high">Kessler</persName>',
            r'<persName ref="p1789" cert="high">Kessler</persName>',
            s, flags=re.S)
        # places
        s = re.sub(r'<placeName ref="l81"', '<placeName ref="l2361"', s, flags=re.S)
        s = re.sub(
            r'<placeName ref="l14" cert="high">Seine</placeName>',
            'Seine',
            s, flags=re.S)
        s = re.sub(
            r'<placeName ref="l14"',
            '<placeName ref="l837"',
            s, flags=re.S)
        s = re.sub(
            r'<placeName ref="l23674" cert="high">Poitou</placeName>',
            '<placeName ref="l23674" cert="high">Poitou</placeName>',
            s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
