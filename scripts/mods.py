#!/usr/bin/python
# -*- coding: utf8 -*-

import re, os


if __name__ == '__main__':

    for f in os.listdir("data/letters/"):
        if f.endswith('.xml'):
            fp = os.path.join("data/letters/", f)
            if not os.path.isdir(fp) and os.path.isfile(fp):
                with open(fp) as fi: s = fi.read()
                s = re.sub(r'"l472"', "l471", s, flags=re.S)
                with open(fp, 'w') as fo: fo.write(s)
