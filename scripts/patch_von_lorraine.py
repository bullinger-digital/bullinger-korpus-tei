#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" François I. von Lorraine: persName ref 7637 -> 20225 """

# instances = dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<persName[^>]*ref=")p7637(")', r'\1p20225\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

"""     for a in re.findall(r'<persName[^>]*ref="p(7637|20225)"[^>]*>(.*?)</persName', s, flags=re.S):
            a_ = re.sub(r'[\[\]\(\)]', '', a[1])
            instances[a_] = True
for i in instances: print(i)

Caesar Galli
Francisco
Francisco 1.
Franciscus
Franciscus Lynenburgensis
Franciscus dux ab Anhalt
Franciscus quidam Gallus
Franciscus, dux Lünenburgensis
Franco
Frantzos
Frantzosen
Frantzoß
Franz
Franz I
Franz I.
Franz I.
Franz I. von Frankreich
Franz I. von Lothringen
Franz I. von Sachsen-Lauenburg
Franz I., König von Frankreich
Franz I., französischer König
Franz von Braunschweig-Lüneburg
Franz von Braunschweig-Lüneburg
Franz von Braunschweig-Lüneburg-Gifhorn
Franz Ï
Franz Ï.
Franz' I.
Franz' Ï.
Franzos
Franzosen
Franzoß
Franz’ I
Franz’ I.
Franz’ I. von Frankreich
François I
François I er
François I. von Lothringen
François II
François Ier
Galli
Gallia
Galliae
Galliam
Galliarum
Gallie regis
Gallo
Gallorum
Gallum
Gallus
Guisen
Guisio
Guysio
Guysium
Gwisa
Gwysa
Heinrich VIII. Franz I.
Hertzog Frantz von Lynenburg
Herzog <hi>Franz</hi> von Braunschweig-Lüneburg-Gifhorn
Herzog Franz von Anhalt
Herzog Franz von Braunschweig-Lüneburg-Gifhorn
Herzog Franz von Lüneburg
Herzog François I. von Lothringen
König
König Franz
König Franz I.
König Franz I. 
König Franz I. von Frankreich
König Franz I. von<pb type="edition" next="139"/> Frankreich
König Franz' I
König Franz’ I
Königs
Königs Franz I.
Lawenburg
Legatus Galli
Lotharingum
Lotharingus
Luneburgensem
Lüneburgensis
Regem
Rex
franczoß
französischen Königs
hertzog von Gwysa
konig uss Franckrych
kunning auß Francreichs
könig auß Franckreich
küng uß Franckrych
küngliche maiestet von Franckrych
künig uß Franckrych
künig von Franckrych
legato Galli
regis Galliae

"""
