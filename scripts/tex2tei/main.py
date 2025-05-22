#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re

from config import config

from helpers.matcher import Matcher
from helpers.parser import Parser
from helpers.validator import Validator
from helpers.sentencenizer import Sentencenicer
from helpers.tagger import Tagger


""" transforms the tex-files [input/] into xml-tei [output/] """


class Transformer:

    ''' Tex2TEI-Pipeline '''

    def __init__(self):

        # Transformation (read/write input/output)
        m = Matcher(config)  # mapping (ID_Tustep -> ID_Corpus)
        Parser(m).parse_files()  # TeX -> TEI

        # Postprocessing (read/write output)
        # - sentences
        s = Sentencenicer(config)
        s.split_sentences()
        s.set_numbers()
        s.set_lang_attributes()

        # - tagging
        t = Tagger(config)
        t.set_attr_salute_or_farewell()  # "ana"-attr. in s-elements
        t.set_tags_persons()  # persons
        t.set_tags_places()  # places
        t.remove_trivial_notes()
        t.set_links_hbbw()  # e.g. <bibl>HBBW XV</bibl>, <ref target="file12264">Nr. 2217</ref>
        t.set_bibl_refs()  # e.g. <bibl ref="b18">HBBW XV</bibl>

        # Validation
        v = Validator(config)
        v.validate_transformation()  # (remaining tex elements)
        v.validate_tei()  # XML/TEI-DTD


# Execution
if __name__ == '__main__':

    Transformer()
