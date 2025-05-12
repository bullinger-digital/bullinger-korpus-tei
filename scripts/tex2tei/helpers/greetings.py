#!/usr/bin/python
# -*- coding: utf8 -*-
# written by MVolk
# adjusted by BSc

import sys, re, os, glob
import xml.etree.ElementTree as ET


''' marks all sentences with the attribute ana="(salute|farewell)" '''


class Greetings:

    def __init__(self, path):
        with open(path) as fi: s = fi.read()
        s = self.reset(s)

        #with open(path, 'w') as fo: fo.write(s)
