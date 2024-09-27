#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

""" Augsburg: placeName ref 1976 -> 18
Augusta Vindelicorum, Augsburger, Augusta, Augustae, Augustam, Ougspurger, Augustę, Confessio Augustana, Augustano,
Augustanis, Auguste, Augustensis, Augustani, Augsburg, Ougstpurg, Ougspurg, Ogspurg, Augustensia, Augustana,
Augsburgische, Augustanus, Saxonicam, Auguste Vindelice, Augspurg, Augustanum, Augustanos, Augustensibus, Augusti,
Augustanorum, Augustanam, Augsburgischen, Augustanae, Ougsburg, Augustae Vindelicorum, Ougstburg, Augustanę,
Augustam Vindeliciae, Augustae Vindelicę, Augustiniano, Augustę Vindelicorum, Augustensium, Augspurger,
Auguste Vindelicorum, Augsburgern, Augustiner, Augustanae Vindelicorum, Augustie Vindelicorum, Augustam Vindelicorum,
Augspurgischen, Augustana Vindelicorum, Augustensi, Augustum, Monuimus, Augustanosque, Augspurgeren,
Augustia Vindelicorum, Augustinum, augsburgischen, Augustane, Augusta Rhetica Vindelicorum, Axspurg """


#instances = dict()
ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(r'(<placeName[^>]*ref=")l1976(")', r'\1l18\2', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)
"""     for a in re.findall(r'<placeName[^>]*ref="l1976"[^>]*>(.*?)</placeName', s, flags=re.S):
            a_ = re.sub(r'[\[\]\(\)]', '', a)
            instances[a_] = True
for i in instances: print(i) """