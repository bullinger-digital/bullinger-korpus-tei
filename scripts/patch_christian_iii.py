#!/usr/bin/python
# -*- coding: utf8 -*-

import re, os


if __name__ == '__main__':

    for f in os.listdir("data/letters/"):
        if f != ".DS_Store":
            fp = os.path.join("data/letters/", f)
            if not os.path.isdir(fp) and os.path.isfile(fp):
                with open(fp) as fi: s = fi.read()
                s = re.sub(r'="p18449"', r'="p3671"', s, flags=re.S)
                with open(fp, 'w') as fo: fo.write(s)
                print(fp, "updated.")

    with open("data/index/persons.xml") as fi: s = fi.read()
    s = re.sub(r'<person xml:id="P18449".*?</person>\s*', '', s, flags=re.S)
    with open("data/index/persons.xml", 'w') as fo: fo.write(s)

    print("Korpus aktualisiert.")
