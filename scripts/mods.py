#!/usr/bin/python
# -*- coding: utf8 -*-

import re, os


def apply(mod_func, root):
    for f in os.listdir(root):
        if f != ".DS_Store":
            fp = os.path.join(root, f)
            with open(fp) as fi: s = fi.read()
            s_new = mod_func(s)
            if s_new != s:
                with open(fp, 'w') as fo: fo.write(s_new)
                print(fp, "updated.")

def mods(s: str):
    mappings = [
        ["</?ipron>", r""]
    ]
    for m in mappings:
        if m: s = re.sub(m[0], m[1], s, flags=re.S)
    return s



if __name__ == '__main__':

    for f in os.listdir("data/letters/"):
        if f != ".DS_Store":
            fp = os.path.join("data/letters/", f)
            with open(fp) as fi: s = fi.read()
            for x in re.findall(r'((<language ident="[^"]*" usage=")(\d*\.\d*)(">[^"]*</language>))', s, flags=re.S):
                s = re.sub(re.escape(x[0]), x[1]+str(int(10*float(x[2])))+x[3], s, flags=re.S)
            with open(fp, 'w') as fo: fo.write(s)
            print(fp, "updated.")

    apply(mods, "data/letters/")
    print("Korpus aktualisiert.")
