#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re



types = {}
subtypes = {}
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*(<listBibl>.*?</listBibl>).*', s, flags=re.S)
        if m:
            bibls = m.group(1)
            for b in re.findall(r'<bibl type="([^"]*)".*?</bibl>', bibls, flags=re.S): types[b] = 1
            for b in re.findall(r'<bibl type="([^"]*)" subtype="([^"]*)".*?</bibl>', bibls, flags=re.S):
                subtypes[b[0]+'-'+b[1]] = 1

for t in subtypes: print(t)

"""
TYPES
---
Gedruckt
Literatur
Übersetzung
EN-Übersetzung
Teildruck
Zusammenfassende__Übersetzung
Regest

SUB
---
Literatur-Erwähnung
Literatur-Zitat
Gedruckt-Teildruck
Gedruckt-Übersetzung
Gedruckt-Regest
Gedruckt-Gedruckt
Gedruckt-Zusammenfassende__Übersetzung
Literatur-Regest
Gedruckt-Maschinenschriftliche__Transkription
Literatur-Übersetzung
Gedruckt-Zusammenfassung
Gedruckt-Teilübersetzung
Gedruckt-Druck
Gedruckt-ungedruckt
Literatur-Teildruck
Gedruckt-Teilregest
Literatur-Teilregest
Literatur-nicht__in
Gedruckt-Teildruck__und__zusammenfassende__Übersetzung
Gedruckt-Druck__und__spanische__Übersetzung
Gedruckt-englische__Übersetzung
Gedruckt-nicht__in
Gedruckt-Erwähnung
Gedruckt-Zitat
Literatur-Gedruckt
Literatur-Teilübersetzung
Gedruckt-Zusammenfassende__Teilübersetzung
Gedruckt-Autograph
Gedruckt-Beilagen
Gedruckt-Kopie
Literatur-Zusammenfassung
Gedruckt-Beilage
Literatur-Inhaltsangabe
Gedruckt-Druck__und__englische__Übersetzung
Gedruckt-Typoskript
Gedruckt-Druck__der__Beilage
Literatur-Analyse
Literatur-Teilkopie
Gedruckt-Teildruck__und__Zusammenfassende__Übersetzung

"""