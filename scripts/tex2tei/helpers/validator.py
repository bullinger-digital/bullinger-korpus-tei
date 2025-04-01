#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re, requests
from lxml import etree


class Validator:

    def __init__(self, config):
        self.config = config
        self.root = config["PATHS"]["OUTPUT"]
        self.url_tei_dtd = config["URL_TEI_DTD"]
        self.elements = {}

    def validate_tei(self):
        print("- Loading DTD (internet connection required) ...")
        schema = requests.get(self.url_tei_dtd).text
        relax_rng = etree.RelaxNG(etree.fromstring(bytes(schema, encoding='utf-8')))
        print("- Validating Files ...")
        is_valid = True
        for f in sorted(os.listdir(self.root)):
            if f != ".DS_Store":
                try:
                    mytree = etree.parse(open(os.path.join(self.root, f)))
                    relax_rng.assert_(mytree)
                except AssertionError as err:
                    is_valid = False
                    print('*** TEI validation error', f+':', err)
        if not is_valid: print("Letter-Validation FAILED ❌")
        else: print("Letters valid ✅")

    def validate_transformation(self):
        tot, cl, cr, env = 0, 0, 0, {}
        for f in sorted(os.listdir(self.root)):
            with open(os.path.join(self.root, f)) as fi:
                if f != '.DS_Store':
                    s = fi.read()
                    cl = len(re.findall(r'\{', s, flags=re.S))
                    cr = len(re.findall(r'\}', s, flags=re.S))
                    if cl != cr: print("***Warning:", f, cl, '{ &', cr, '}')
                    for e in re.findall(r'\\\w+', s, flags=re.S):
                        if e in self.elements: self.elements[e] += 1
                        else: self.elements[e] = 1
                        tot += 1
                    for e in re.findall(r'\\begin\{.*?\}', s, flags=re.S):
                        env[e] = 1
        if len(self.elements) > 0:
            print("---\nWARNING, Remaining TeX-Elements detected:")
            for k, v in sorted(self.elements.items(), key=lambda item: item[1], reverse=True):
                print('\t-', k, '('+str(v)+'x)')
        if len(env):
            print("---\nWARNING, Remaining TeX-Environments detected:")
            for e in env: print('\t', e, "...")
        if tot>0: print("---\nTOTAL:", tot, "unprocessed TeX-Elements.")
