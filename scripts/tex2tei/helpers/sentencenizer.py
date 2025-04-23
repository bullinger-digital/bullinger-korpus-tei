#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re

from helpers.lang.identifier import LanguageIdentifier
from helpers.lang.charlm import CharLM


class Sentencenicer:

    def __init__(self, config):
        self.input = config["PATHS"]["OUTPUT"]
        self.output = config["PATHS"]["OUTPUT"]
        self.print_info = True
        self.lang_identifier = self.train_identifier("helpers/lang/training/")

    def split_sentences(self):
        if self.print_info: print("- splitting/numbering sentences ...")
        for f in sorted(os.listdir(self.input)):
            with open(os.path.join(self.input, f)) as fi:
                if f != '.DS_Store':
                    t = fi.read()
                    for s in re.findall(r'(<s>(.*?)</s>)', t, flags=re.S):
                        s_, sub = self.rm_notes(s[1])
                        s_ = re.sub(r'\s+', ' ', s_, flags=re.S)
                        s_ = re.sub(r'(([a-z]{3,}|\d{4,4}|Abc@\d+abc)[\.\!\?](\s*Abc@\d+abc|))\s+([A-Z])', r'\1</s>\n\t\t\t\t\t<s>\4', s_, flags=re.S)
                        s_ = self.add_notes(s_, sub)
                        t = re.sub(re.escape(s[0]), r'<s>'+s_+r'</s>', t, flags=re.S)
                    with open(os.path.join(self.output, f), 'w') as fo: fo.write(t)

    def rm_notes(self, s):
        sub, c = {}, 0
        for empty_element in ["ptr", "pb", "ref"]:  # empty elements
            for e in re.findall(r'<'+empty_element+r'[^</>]*/>', s, flags=re.S):
                c += 1
                key = r'Abc@'+str(c)+'abc'
                s = re.sub(re.escape(e), key, s, flags=re.S)
                sub[key] = e
        m = re.match(r'.*<[^>]*?>.*', s, flags=re.S)
        while m:
            for element in ["span", "foreign", "author", "bibl", "hi", "ref", "note"]:  # regular elements
                for e in re.findall(r'<'+element+r'[^<>]*>[^<>]*</'+element+'>', s, flags=re.S):
                    c += 1
                    key = r'Abc@'+str(c)+'abc'
                    s = re.sub(re.escape(e), key, s, flags=re.S)
                    sub[key] = e
            m = re.match(r'.*<[^>]*?>.*', s, flags=re.S)
        return s, sub

    def add_notes(self, s, sub):
        m = re.match(r'.*Abc@\d+abc.*', s, flags=re.S)
        while m:
            for x in sub: s = re.sub(x, sub[x], s, flags=re.S)
            m = re.match(r'.*Abc@\d+abc.*', s, flags=re.S)
        return s

    def set_numbers(self):
        # if self.print_info: print("- Numbering sentences ...")
        for f in sorted(os.listdir(self.input)):
            with open(os.path.join(self.input, f)) as fi:
                if f != '.DS_Store':
                    t = fi.read()
                    m, c = re.match(r'((.*?<s)(>.*))', t, flags=re.S), 0
                    while m:
                        c += 1
                        t = re.sub(re.escape(m.group(1)), m.group(2)+' n="'+str(c)+'"'+m.group(3), t, flags=re.S)
                        m = re.match(r'((.*?<s)(>.*))', t, flags=re.S)
                    with open(os.path.join(self.output, f), 'w') as fo: fo.write(t)

    def set_lang_attributes(self):
        if self.print_info: print("- setting lang-attributes ...")
        for f in sorted(os.listdir(self.input)):
            if f != '.DS_Store':
                with open(os.path.join(self.input, f)) as fi:
                    t = fi.read()
                    for s in re.findall(r'((<s [^>]*)(>(.*?)</s>))', t, flags=re.S):
                        s_, sub = self.rm_notes(s[3])
                        t = re.sub(re.escape(s[0]), s[1]+' xml:lang="'+self.lang_identifier.identify(s_)+'"'+s[2], t, flags=re.S)
                    with open(os.path.join(self.output, f), 'w') as fo: fo.write(t)

    def train_identifier(self, dir, ngram_order=3):
        if self.print_info: print("- language identifier training ...")
        identifier = LanguageIdentifier()
        for lang_code in ['de', 'la']:
            model = CharLM(ngram_order)
            model.train(os.path.join(dir, lang_code+'.txt'))
            identifier.add_model(lang_code, model)
        return identifier
