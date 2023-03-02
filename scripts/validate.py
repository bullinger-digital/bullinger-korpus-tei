#!/usr/bin/python
# -*- coding: utf8 -*-

import os, requests
from lxml import etree


PATH_DTD = "tei.dtd"
PATH_LETTERS = "data/letters/"
PATH_INDEX = "data/index/"
URL_DTD = 'https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng'


class Validation:

    @staticmethod
    def validate():
        schema = requests.get(URL_DTD).text
        tei_relax_rng = etree.RelaxNG(etree.fromstring(bytes(schema, encoding='utf-8')))
        if not Validation.validate_files(tei_relax_rng, [PATH_LETTERS, PATH_INDEX]): print("FAILED.")
        else: print("PASSED.")

    @staticmethod
    def validate_files(relax_rng, dirs):
        is_valid = False
        for d in dirs:
            for f in sorted(os.listdir(d)):
                if f != ".DS_Store":
                    try: relax_rng.assert_(etree.parse(open(os.path.join(d, f))))
                    except AssertionError as err:
                        is_valid = False
                        print('TEI validation error:', f, err)
        return is_valid


if __name__ == '__main__':

    print("Validating files...")
    Validation.validate()
