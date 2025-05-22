#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


class HBBWLinker:

    def __init__(self):
        self.map = self.get_map_from_corpus()
        #for id_ in self.map: print(id_, '-->', self.map[id_])

    def tag_letter(self, path):
        with open(path) as fi: s = fi.read()
        for m in re.findall(r'(<bibl[^>]*>HBBW\s*[IVX]*</bibl>[,\s]*\[?)(Nr\.\s*(\d+)\]?)', s, flags=re.S):
            if m[2] in self.map:
                s = re.sub(
                    re.escape(m[0]+m[1]),
                    m[0]+'<ref target="file'+self.map[m[2]]+'">'+m[1]+'</ref>',
                    s, flags=re.S
                )
        with open(path, 'w') as fo: fo.write(s)

    def get_map_from_corpus(self):
        root, map, n = "data/letters/", {}, 0
        for f in os.listdir(root):
            if f.endswith('.xml'):
                tar = f.strip('.xml')
                path = os.path.join(root, f)
                with open(path) as fi: s = fi.read()
                m = re.match(r'.*?<idno subtype="url" resp="irg">[^<]*=(\d+)</idno>.*', s, flags=re.S)
                if m:
                    map[m.group(1)] = tar
                    n += 1
        # print("Hits:", n)  # 2991
        return map


if __name__ == '__main__':

    linker = HBBWLinker()
    for f in os.listdir("scripts/save/"):
        if f.endswith('.xml'):
            path = os.path.join("data/letters/", f)
            linker.tag_letter(path)
