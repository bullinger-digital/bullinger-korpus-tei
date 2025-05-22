#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re
from colorama import Fore


class Search:

    def __init__(self, dirs=None, pattern=''):
        self.pattern = pattern
        self.dirs = dirs
        self.count = 0

        self.letter_only = False
        self.sentences_only = False
        self.frame_width_l = 30
        self.frame_width_r = 30
        self.space_sub = r' '
        self.rm_untagged_fls = True

        if dirs and pattern: self.search(self.dirs, self.pattern)

    def search(self, dirs, pattern):
        for d in dirs:
            for f in os.listdir(d):
                fp = os.path.join(d, f)
                if os.path.isdir(fp): self.search([fp], pattern)
                elif os.path.isfile(fp) and f != ".DS_Store": self.search_file(fp, pattern)

    def search_file(self, path, pattern):
        f = path.split('/')[-1]
        with open(path) as fi: s = fi.read()
        if self.rm_untagged_fls: s = re.sub(r'\*\[\*.*?\]', '', s, flags=re.S)
        if self.letter_only:
            ms = re.match('.*(<letter[^>]*>.*?</letter>).*', s, flags=re.S)
            if ms: s = ms.group(1)
            else: print("*Warning, no letter in", path)
        if self.sentences_only: s = "\n".join(re.findall(r'<s .*?</s>', s, flags=re.S))
        if len(re.findall(pattern, s, flags=re.S)):
            if not self.frame_width_l and not self.frame_width_r: t = re.findall(r'([^\n]*)(' + pattern + r')([^\n]*)', s, flags=re.S)
            else: t = re.findall(r'([\w\W]{,' + str(self.frame_width_l) + r'})(' + pattern + r')([\w\W]{,' + str(self.frame_width_r) + r'})', s, flags=re.S)
            for x in t:
                self.count += 1
                output =\
                    Fore.WHITE + f"{self.count:>8}" + ' ' +\
                    Fore.RED + f"{f:<25}" + ' '+\
                    Fore.BLUE + (re.sub(r'[\n\t]', self.space_sub, x[0], flags=re.S) if self.space_sub else x[0]) +\
                    Fore.GREEN + (re.sub(r'[\n\t]', self.space_sub, x[1], flags=re.S) if self.space_sub else x[1]) +\
                    Fore.BLUE + (re.sub(r'[\n\t]', self.space_sub, x[-1], flags=re.S) if self.space_sub else x[2])
                print(output)


def print_dict_sorted_by_value(d, tot: int, reverse=True):
    if tot:
        for k, v in sorted(d.items(), key=lambda x: x[1], reverse=reverse):
            print('- ` ' + k, ' ` \t', str(v) + ', ' + str(round(v/tot*100, 2))+'%')  # .md output
    else:
        for k, v in sorted(d.items(), key=lambda x: x[1], reverse=reverse): print(k, str(v))


if __name__ == '__main__':

    x = Search()
    x.letter_only = False
    x.sentences_only = False
    x.frame_width_l = 50
    x.frame_width_r = 50
    x.space_sub = r' '
    x.rm_untagged_fls = False  # \*\[\*.*?\]

    x.search(["data/letters"], r'Eine zeitgenössische Darstellung der Ges')  #
