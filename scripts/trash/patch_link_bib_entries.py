#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


class BibTagger:

    def __init__(self):
        self.bib = {}  # name -> id
        self.path_bib = "data/index/bibliography.xml"
        self.read_bibliography()
        self.ROOT = "data/letters/"

    def read_bibliography(self):
        with open(self.path_bib) as fi: s = fi.read()
        for b in re.findall(r'<bibl xml:id="([^"]*)">.*?<title>(.*?)</title>', s, flags=re.S):
            self.bib[b[1]] = b[0]

    def set_bibl_refs(self):
        for f in os.listdir(self.ROOT):
            if f.endswith('.xml'):
                p = os.path.join(self.ROOT, f)
                with open(p) as fi: s = fi.read()
                for b in re.findall(r'((<bibl>)(.*?)(</bibl>))', s, flags=re.S):
                    if b[2] in self.bib:
                        s = re.sub(re.escape(b[0]),
                                r'<bibl source="'+self.bib[b[2]]+'">'+b[2]+b[3],
                                s, flags=re.S)
                with open(p, 'w') as fo: fo.write(s)


tagger = BibTagger()
tagger.set_bibl_refs()
