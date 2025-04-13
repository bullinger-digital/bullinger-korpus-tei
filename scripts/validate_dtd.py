#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from lxml import etree

DIRS = ["data/letters/", "scripts/tex2tei/output/"]


class DTD:

    def __init__(self):
        self.is_valid = True

    def validate(self) -> bool:
        print("Validating letters ...")
        dtd, n = etree.DTD(open("data/letter.dtd")), 0
        for d in DIRS:
            for f in os.listdir(d):
                if f.endswith('.xml'):
                    tree = etree.parse(open(os.path.join(d, f)))
                    valid = dtd.validate(tree)
                    if not valid:
                        print(dtd.error_log.filter_from_errors())
                        self.is_valid, n = False, n + 1
        print("Issues:", n)
        return self.is_valid


if __name__ == '__main__':

    DTD().validate()
