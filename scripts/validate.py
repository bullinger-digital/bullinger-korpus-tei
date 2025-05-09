#!/usr/bin/python
# -*- coding: utf8 -*-

import os, requests
from lxml import etree

PATH_LETTERS = "data/letters/"
PATH_INDEX = "data/index/"
URL_DTD = 'https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng'
TEI_RELAX_RNG = etree.RelaxNG(etree.fromstring(bytes(requests.get(URL_DTD).text, encoding='utf-8')))

def validate(path_corpus):
    is_valid = True
    for f in sorted(os.listdir(path_corpus)):
        f_path = os.path.join(path_corpus, f)
        if not os.path.isdir(f_path) and f.endswith('.xml'):
            if not validate_file(f_path): is_valid = False
    return is_valid

def validate_file(path):
    try:
        if not TEI_RELAX_RNG.validate(etree.parse(path)):
            for error in TEI_RELAX_RNG.error_log:
                print(f'Validation errors in file: {f}, Line {error.line}, Col {error.column}: {error.message}')
            return False
        else: return True
    except Exception as e:
        print(f'Error parsing file {f}: {e}')
        return False

def assertion(path):
    try:
        TEI_RELAX_RNG.assert_(etree.parse(open(path)))
        return True
    except AssertionError as err:
        print('Validation error:', f, err)
        return False


print("Letters valid.") if validate(PATH_LETTERS) else print("*Letter-Validation FAILED.")
print("Index valid.") if validate(PATH_INDEX) else print("*Index-Validation FAILED.")
