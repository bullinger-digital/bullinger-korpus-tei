#!/usr/bin/python
# -*- coding: utf8 -*-
# written by MVolk
# adjusted by BSc

import sys, re, os, glob
import xml.etree.ElementTree as ET


''' marks all sentences with the attribute ana="(salute|farewell)" '''


class Greetings:

    def __init__(self, path):
        self.exclude = ['ein grusenlich ellend', 'Ein gruselich persecution', 'ain grußelich geschrey',
                        'grusamlich verfolgt', 'von grusamem wüten', 'Grüschii']
        self.re_salute = '.*(' \
             'Salut(a|at|o|em|es)[\s,;]|Salut\[a\]|Saluta\[bis\]|Saluta\[n\]t|Salut\[em\]|' \
             'Saluta(bis|bitis|mus|nt|re|ri|runt|ta|te|tiones|to|tum|tus|vi)|' \
             ' (re)?salut(a|at|o|em|es)[\s\.,;]|' \
             ' (re)?saluta(bis|bit(is)?|mus|ndi|nt|ret?|ri|runt|te|tib|tis|tos?|tum|tus|vi)[\s\.,;]|' \
             'Salv(eat|eant|um|us|os)|[Ss]alvere|[Ss]alva sit|[Ss]alvi (sint|sitis)|Salvi sunt|Resaluta|' \
             'Commenda me| commenda me| me commenda| me commendar[ei]\b|(diligenter|diligentissime|accuratissime) commenda|' \
             '(Gru?(uͦ|uͤ|ü)e?t?[ßsz]|Gru[eo]?t?[ßsz]|Grie[szß]+(en)?[t]|Grie[szß]+en |[Gg]ritzen|Groiz|Groetzt| gru[eo]?t?[ßsz]| gr(uͦ|uͤ|ü|ys|ie|ouͤ|ye|üi|üe|is)t?[ßsz]|Begrützen)' \
        ').*'
        self.re_vale = '.*(Vale(te)?[\s\.,;]| vale(te)?[\s\.,;]).*'
        with open(path) as fi: s = fi.read()
        s = self.reset(s)
        s = self.tagger(s)
        with open(path, 'w') as fo: fo.write(s)

    def reset(self, s):
        s = re.sub(r'(<s [^>]*) ana="salute"', r'\1', s, flags=re.S)
        s = re.sub(r'(<s [^>]*) ana="farewell"', r'\1', s, flags=re.S)
        return s

    def rm_elements(self, s):
        s = re.sub(r'</?(persName|placeName|span|del|cit|hi|foreign|bibl|author)[^>]*>', '', s, flags=re.S)
        s = re.sub(r'<(pb|lb|ptr)[^>]*/\s*>', '', s, flags=re.S)
        s = re.sub(r'<ref[^>]*>.*?</ref>', r'', s, flags=re.S)
        m = re.match(r'.*(<note[^>]*>[^<]*</note>).*', s, flags=re.S)
        while m:
            s = re.sub(re.escape(m.group(1)), '', s, flags=re.S)
            m = re.match(r'.*(<note[^>]*>[^<]*</note>).*', s, flags=re.S)
        for x in self.exclude: s = re.sub(re.escape(x), '', s, flags=re.S)
        return s

    def tagger(self, s):
        for t in re.findall(r'((<s n="(\d+)"[^>]*)>(.*?)(</s>))', s, flags=re.S):
            if int(t[2]) > 2:  # excluce the 1st two sentences
                x, x_new = self.rm_elements(t[3]), t[0]
                if re.match(self.re_salute, x, flags=re.S): x_new = t[1] + ' ana="salute">' + t[3] + t[4]
                elif re.match(self.re_vale, x, flags=re.S): x_new = t[1] + ' ana="farewell">' + t[3] + t[4]
                s = re.sub(re.escape(t[0]), x_new, s, flags=re.S)
        return s
