#!/usr/bin/python
# -*- coding: utf8 -*-

import re, os

from tex2tei.helpers.lang.charlm import CharLM
from tex2tei.helpers.lang.identifier import LanguageIdentifier


class LangUpdater:

    def __init__(self):
        self.analyze_only = False
        self.lang_usage = {}
        self.lang_identifier = self.train_identifier("scripts/tex2tei/helpers/lang/training/")
        self.map = {
            "la": "Latein",
            "de": "Deutsch",
            "el": "Griechisch",
            "he": "Hebräisch",
            "en": "Englisch",
            "fr": "Französisch",
            "it": "Italienisch",
        }

    def execute(self):
        ROOT = "data/letters/"
        tot = len(os.listdir(ROOT))
        for i, f in enumerate(sorted(os.listdir(ROOT))):
            if f.endswith('.xml'):
                print(f, round(100*(i+1)/tot, 2), '%')
                self.process_file(os.path.join(ROOT, f))
        print("---\nTotal (Wörter):")
        for t in self.lang_usage: print(t, self.lang_usage[t])

    def process_file(self, path):
        tokens = dict()
        with open(path) as fi: s = fi.read()
        if not re.match(r'.* source="(HTR|keine)".*', s, flags=re.S) and len(re.findall(r'<s ', s, flags=re.S)) > 0:
            for t in re.findall(r'<s [^>]*xml:lang="([^"]*)"[^>]*>(.*?)</s>', s, flags=re.S):
                lang, sent = t[0], t[1]
                sent = self.rm_elements(sent)
                sent, tokens = self.analyze(sent, tokens)
                if t[0] not in tokens: tokens[t[0]] = 0
                tokens[t[0]] += len(sent.split(' '))
        if re.match(r'.* source="HTR".*', s, flags=re.S) and len(re.findall(r'<lb ', s, flags=re.S)) > 0:
            prev = ''
            for t in re.findall(r'<lb [^>]*>([^\n]*)', s, flags=re.S):
                sent = self.rm_elements(t)
                if len(sent.strip())<5 and prev: lang = prev
                else: lang = self.lang_identifier.identify(sent)  # for "sentences" like "S."
                sent, tokens = self.analyze(sent, tokens)
                if lang not in tokens: tokens[lang] = 0
                tokens[lang] += len(sent.split(' '))
                prev = lang

        sum = 0
        for t in tokens:
            sum += int(tokens[t])
            if t not in self.lang_usage: self.lang_usage[t] = 0
            self.lang_usage[t] += int(tokens[t])
        e = ''
        if len(tokens):
            e += '\n\t\t\t<langUsage>\n'
            for t in sorted(tokens, key=lambda x: tokens[x], reverse=True):
                e += '\t\t\t\t<language ident="'+t+'" usage="'+str(round(1000*int(tokens[t])/sum))+'">'+self.map[t]+'</language>\n'
            e += '\t\t\t</langUsage>\n'
            main_lang = [t for t in sorted(tokens, key=lambda x: tokens[x], reverse=True)][0]
            s = re.sub(r'(<msContents>\s*<msItem>\s*<incipit.*?</incipit>\s*<textLang>).*?(</textLang>)', r'\1'+self.map[main_lang]+r'\2', s, flags=re.S)
            s = re.sub(r'(<incipit.*?</incipit>\n)(\s*</msItem>)', r'\1'+7*'\t'+'<textLang>'+self.map[main_lang]+r'</textLang>\n\2', s, flags=re.S)
            s = re.sub(r'(<text xml:lang=")[^"]*(">)', r'\1'+main_lang+r'\2', s, flags=re.S)
            s = re.sub('(<msDesc type="Brief"[^>]*xml:lang=")(")', r'\1'+main_lang+r'\2', s, flags=re.S)
        if e:
            m = re.match(r'.*?(\s*(<langUsage>.*?</langUsage>|<langUsage\s*/>)[ \t]*\n).*', s, flags=re.S)
            if m: s = re.sub(re.escape(m.group(1)), e, s, flags=re.S)
            else: s = re.sub(r'(.*</correspDesc>)', r'\1'+e, s, flags=re.S)
        else: s = re.sub(r'<langUsage>.*?</langUsage>', r'<langUsage/>', s, flags=re.S)

        if not self.analyze_only:
            s = re.sub(r'\n\s*\n', '\n', s, flags=re.S)
            s = re.sub(r'[\t ]*<langUsage/>[\t ]*\n', '', s, flags=re.S)
            with open(path, 'w') as fo: fo.write(s)

    def analyze(self, s, tokens):
        for f in re.findall(r'(<foreign[^>]*lang="([^"]*)"[^>]*>(.*?)</foreign>)', s, flags=re.S):
            if f[1] not in tokens: tokens[f[1]] = 0
            tokens[f[1]] += len(f[2].split(' '))
            s = re.sub(re.escape(f[0]), '', s, flags=re.S)
        return s, tokens

    def rm_elements(self, s):
        s = re.sub(r'</?(persName|placeName|span|del|cit|hi|bibl|author)[^>]*>', '', s, flags=re.S)
        s = re.sub(r'<(pb|lb|ptr)[^>]*/\s*>', '', s, flags=re.S)
        s = re.sub(r'<ref[^>]*>.*?</ref>', r'', s, flags=re.S)
        s = re.sub(r'<note[^>]*>[^<]*</note>', r'', s, flags=re.S)
        foreign = dict()
        for i, f in enumerate(re.findall(r'<foreig.*?</foreign>', s, flags=re.S)):
            foreign['@@@'+str(i)] = f
            s = re.sub(re.escape(f), '@@@'+str(i), s, flags=re.S)
        m = re.match(r'.*(<note[^>]*>[^<]*</note>).*', s, flags=re.S)
        while m:
            s = re.sub(re.escape(m.group(1)), '', s, flags=re.S)
            m = re.match(r'.*(<note[^>]*>[^<]*</note>).*', s, flags=re.S)
        for f in foreign: s = re.sub(f, foreign[f], s, flags=re.S)
        s = re.sub(r'\s+', ' ', s, flags=re.S)
        return s

    def train_identifier(self, dir, ngram_order=3):
        identifier = LanguageIdentifier()
        for lang_code in ['de', 'la']:
            model = CharLM(ngram_order)
            model.train(os.path.join(dir, lang_code+'.txt'))
            identifier.add_model(lang_code, model)
        return identifier


if __name__ == '__main__':

    LangUpdater().execute()
