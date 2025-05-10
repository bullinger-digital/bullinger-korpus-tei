#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from lxml import etree


class DTD:

    def __init__(self):
        self.path_dtd = "data/letter.dtd"
        self.dirs = ["data/letters/"]  #, "scripts/tex2tei/output/"]
        self.is_valid = True
        # ---
        self.validate()

    def validate(self):
        print("Validating letters ...")
        dtd, n = etree.DTD(open(self.path_dtd)), 0
        for d in self.dirs:
            for f in os.listdir(d):
                if f.endswith('.xml'):
                    tree = etree.parse(open(os.path.join(d, f)))
                    valid = dtd.validate(tree)
                    if not valid:
                        print(dtd.error_log.filter_from_errors())
                        self.is_valid, n = False, n + 1
        print("Issues:", n)


if __name__ == '__main__': DTD()
