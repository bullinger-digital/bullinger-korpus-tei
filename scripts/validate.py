#!/usr/bin/python
# -*- coding: utf8 -*-

import os, requests
from lxml import etree

PATH_LETTERS = "data/letters/"
PATH_INDEX = "data/index/"
URL_DTD = 'https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng'


print("validating files...")
schema = requests.get('https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng').text
relaxng_doc = etree.fromstring(bytes(schema, encoding='utf-8'))
tei_relax_rng = etree.RelaxNG(relaxng_doc)

def validateTei(relax_rng, path_corpus):
    is_valid = True
    for f in sorted(os.listdir(path_corpus)):
        if not os.path.isdir(os.path.join(PATH_LETTERS, f)) and f != ".DS_Store":
            mytree = etree.parse(open(os.path.join(path_corpus, f)))
            try: relax_rng.assert_(mytree)
            except AssertionError as err:
                is_valid = False
                print('TEI validation error:', f, err)
    return is_valid

if not validateTei(tei_relax_rng, PATH_LETTERS): print("Letter-Validation FAILED.")
else: print("Letters valid.")
if not validateTei(tei_relax_rng, PATH_INDEX): print("Index-Validation FAILED.")
else: print("Index valid.")

