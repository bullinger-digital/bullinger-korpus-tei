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
            if ms:
                s = ms.group(1)
                # Search.bracket_analyzer(s, path, a=r'\{', b=r'\}')
                # Search.bracket_analyzer(s, path, a=r'\(', b=r'\)')
                # Search.bracket_analyzer(s, path, a=r'\[', b=r'\]')
                # Search.bracket_analyzer(s, path, a=r'\«', b=r'\»')
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
            # fo.write(str(self.count) + '\t' + f + '\t' + re.sub(r'[\n\t]', self.space_sub, ' '.join(x), flags=re.S).strip() + '\n')

    @staticmethod
    def bracket_analyzer(s, path, a=r'{', b=r'}'):
        if len(re.findall(a, s)) != len(re.findall(b, s)): print(
            '*Warning: '+a+' OR '+b+' is missing in', path,
            "("+str(len(re.findall(a, s)))+" vs. "+str(len(re.findall(b, s)))+")"
        )


class Analyze:

    def __init__(self, dirs: list):
        self.dirs = dirs
        self.number_of_files = 0
        self.xml = dict()  # element name --> count
        self.attr = dict()  # element name --> attributes --> count
        self.chars = dict()

        self.analyze(self.dirs)

        elements_tot = sum([self.xml[e] for e in self.xml])
        attributes_tot = sum([sum([self.attr[e][a] for a in self.attr[e]]) for e in self.attr])
        print(2 * "\n" + "XML-Elements/Attributes (" + str(elements_tot) + " elements, "+str(attributes_tot) + " attributes)\n")
        for e in self.xml: print(e, self.xml[e], self.attr[e] if e in self.attr else [])

        chars_tot = sum([self.chars[d] for d in self.chars])
        print(2 * "\n" + "Characters (" + str(elements_tot) + ")\n")
        print_dict_sorted_by_value(self.chars, chars_tot, reverse=True)

    def analyze(self, dirs: list):
        for d in dirs:
            for f in os.listdir(d):
                fp = os.path.join(d, f)
                if os.path.isdir(fp): self.analyze([fp])
                elif os.path.isfile(fp) and f != ".DS_Store":
                    self.xml_elements(fp, letters_only=True)
                    self.char_count(fp)

    def xml_elements(self, fp: str, letters_only=True):
        """ counts xml elements/attributes for file with url <fp> """
        with open(fp) as fi: s = fi.read()
        if letters_only:
            ml = re.match(r'.*(<letter.*?</letter>).*', s, flags=re.S)
            s = ml.group(1) if ml else ''
        else: print("*Warning, no letter-element in", fp)
        for e in re.findall(r'<(\w+)', s, flags=re.S):
            self.xml[e] = 1 if e not in self.xml else self.xml[e] + 1
        for a in re.findall(r' (\w+)="[^"]*"', s, flags=re.S):
            for ea in re.findall(r'<(\w+)[^>]*\s+'+re.escape(a), s, flags=re.S):
                if ea not in self.attr: self.attr[ea] = {a: 1}
                elif a not in self.attr[ea]: self.attr[ea][a] = 1
                else: self.attr[ea][a] += 1

    def char_count(self, fp):
        with open(fp) as fi: s = fi.read()
        s = re.sub(r'\s+', ' ', ''.join([t for t in re.findall(r'<s [^>]*>(.*?)</s>', s, flags=re.S)]), flags=re.S)
        for e in ['letter', 'p', 's', 'el', 'he', 'la', 'div', 'de']: s = Analyze.remove_element(s, e, entirely=False)
        for e in ['fn', 'note', 'zzl']: s = Analyze.remove_element(s, e, entirely=True)
        for e in ['letter', 'p', 's', 'el', 'he', 'la', 'div', 'de',
                  'fn', 'note', 'zzl'
                  'pb_edition', 'pb_scan', 'del']: s = Analyze.remove_element(s, e)
        if re.match(r'<.*?>', s): print("*Warning: Annotations detected in", fp)
        for c in re.sub(r'\s+', '', s, flags=re.S): self.chars[c] = (self.chars[c] + 1) if c in self.chars else 1
        # s1, s2 = len(re.findall(r'\«', s, flags=re.S)), len(re.findall(r'\»', s, flags=re.S))
        # if s1 != s2: print("*Warning:", fp)

    @staticmethod
    def remove_empty_element(s, e): return re.sub(r'<' + e + r'[^>]*/>', '', s, flags=re.S)

    @staticmethod
    def remove_element(s, e, entirely=False):
        if entirely: return re.sub(r'<' + e + r'[^>]*>.*?' + r'</' + e + r'>', '', s, flags=re.S)
        else: return re.sub(r'</?'+e+r'\s+[^>]*>', '', s, flags=re.S)

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

    x.search(["data/letters"], r'\[[Ii]nterna\]')
