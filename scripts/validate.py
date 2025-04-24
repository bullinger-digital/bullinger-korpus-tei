#!/usr/bin/python
# -*- coding: utf8 -*-

import os, requests
from lxml import etree

PATH_LETTERS = "data/letters/"
PATH_INDEX = "data/index/"
URL_DTD = 'https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng'
TEI_RELAX_RNG = etree.RelaxNG(etree.fromstring(bytes(requests.get(URL_DTD).text, encoding='utf-8')))

def validateTei(relax_rng, path_corpus):
    is_valid = True
    for f in sorted(os.listdir(path_corpus)):
        if not os.path.isdir(os.path.join(path_corpus, f)) and f != ".DS_Store":
            try: relax_rng.assert_(etree.parse(open(os.path.join(path_corpus, f))))
            except AssertionError as err:
                is_valid = False
                print('TEI validation error:', f, err)
    return is_valid

print("Letters valid.") if validateTei(TEI_RELAX_RNG, PATH_LETTERS) else print("*Letter-Validation FAILED.")
print("Index valid.") if validateTei(TEI_RELAX_RNG, PATH_INDEX) else print("*Index-Validation FAILED.")
