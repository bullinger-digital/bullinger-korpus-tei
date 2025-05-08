#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


ROOT = "data/letters/"
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        # Regest
        m_regest = re.match(r'.*(<summary.*?</summary>).*', s, flags=re.S)
        if m_regest:
            regest = m_regest.group(1)
            for p in re.findall(r'((<p[^/>]*>)\s*(.*?)\s*(</p>))', regest, flags=re.S):
                p_ = p[1]+re.sub(r'\s+', ' ', p[2], flags=re.S)+p[3]
                regest = re.sub(re.escape(p[0]), p_, regest, flags=re.S)
            s = re.sub(re.escape(m_regest.group(1)), regest, s, flags=re.S)
            s = re.sub(r'\s*(<p xml:id="regest)', '\n'+7*'\t'+r'\1', s, flags=re.S)
        # Dates
        for d in re.findall(r'((<date[^/>]*>)\s*(.*?)\s*(</date>))', s, flags=re.S):
            d_ = d[1] +re.sub(r'\s+', ' ', d[2], flags=re.S) + d[3]
            s = re.sub(re.escape(d[0]), d_, s, flags=re.S)
        # Sentences
        for x in re.findall(r'((<s [^/>]*>)\s*(.*?)\s*(</s>))', s, flags=re.S):
            x_ = x[1] +re.sub(r'\s+', ' ', x[2], flags=re.S) + x[3]
            s = re.sub(re.escape(x[0]), x_, s, flags=re.S)
        # rs
        for x in re.findall(r'((<rs[^/>]*>)\s*(.*?)\s*(</rs>))', s, flags=re.S):
            x_ = x[1] +re.sub(r'\s+', ' ', x[2], flags=re.S) + x[3]
            s = re.sub(re.escape(x[0]), x_, s, flags=re.S)

        # Scans
        s = re.sub(r'\s*(<(zone|/?graphic))', r'\n\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(<desc )', r'\n\t\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*(</surf)', r'\n\t\t\1', s, flags=re.S)

        s = re.sub(r'\s*(<div)', r'\n\t\t\t\1', s, flags=re.S)
        s = re.sub(r'\s*\n', r'\n', s, flags=re.S)
        s = re.sub(r'  ', r' ', s, flags=re.S)
        s = re.sub(r'\s+(</note>)', r'\1', s, flags=re.S)
        with open(path, 'w') as fo: fo.write(s.strip())

# check
data = {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for e in re.findall(r'(\s*)<([^/\s>]+)', s, flags=re.S):
            if e[1] not in data: data[e[1]] = []
            if e[0] not in data[e[1]]: data[e[1]].append(e[0])
for e in data:
    if len(data[e]) > 1:
        print(e, len(data[e]), data[e])

"""
title 2 ['\n\t\t\t\t', '\n\t\t\t\t\t\t\t\t']
idno 3 ['\n\t\t\t\t', '\n\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t']
date 3 ['\n\t\t\t\t', '\n\t\t\t\t\t', '']
bibl 5 ['\n\t\t\t\t', '\n\t\t\t\t\t\t\t', ' ', '', '\n\t\t\t\t\t']
p 3 ['\n\t\t\t\t\t\t\t', '\n\t\t\t\t', '']
persName 3 ['', ' ', '\n\t\t\t\t\t']
note 5 ['', '\n\t\t', '\n\t\t\t\t\t', ' ', '\n\t\t\t\t\t\t\t\t']
placeName 3 ['\n\t\t\t\t\t', ' ', '']
ref 3 [' ', '', '\n\t\t\t\t\t']
ptr 2 ['', ' ']
hi 2 ['', ' ']
s 2 ['\n\t\t\t\t\t', '']
author 2 ['', '\n\t\t\t\t\t\t\t']
foreign 2 [' ', '']
lb 3 ['\n\t\t\t\t\t', '', ' ']
pb 3 ['\n\t\t\t\t\t', '', ' ']
cit 2 ['', ' ']
span 2 [' ', '']
"""

data = {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.xml'):
        path = os.path.join(ROOT, f)
        with open(path) as fi: s = fi.read()
        for e in re.findall(r'(\s*)</([^/\s>]+)', s, flags=re.S):
            if e[1] not in data: data[e[1]] = []
            if e[0] not in data[e[1]]: data[e[1]].append(e[0])
print("=====")
for e in data:
    if len(data[e]) > 1:
        print(e, len(data[e]), data[e])

'''
p 2 ['', '\n\t\t\t\t']
bibl 2 ['\n\t\t\t\t\t\t\t', '']
'''