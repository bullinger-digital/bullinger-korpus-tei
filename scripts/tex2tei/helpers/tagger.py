#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re
from helpers.greetings import Greetings


class Tagger:

    def __init__(self, config):
        self.output = config["PATHS"]["OUTPUT"]
        self.root_pers_index = config["PATHS"]["CORPUS"]["PERSONS"]  # "../../data/index/persons.xml"
        self.root_places_index = config["PATHS"]["CORPUS"]["PLACES"]  # = "../../data/index/localities.xml"
        self.root_letters = config["PATHS"]["CORPUS"]["LETTERS"]  # "../../data/letters"
        # ---
        self.id2pers = self.read_persons()
        self.id2place = self.read_places()
        self.tmp_persons = {}
        self.tmp_places = {}

    def set_attr_salute_or_farewell(self):
        for f in os.listdir(self.output):
            if f.endswith('.xml'):
                Greetings(os.path.join(self.output, f))

    def set_tags_persons(self):
        for f in os.listdir(self.output):
            if f.endswith('.xml'):
                path = os.path.join(self.output, f)
                self.tmp_persons = self.read_persons_from_file(f)
                with open(path) as fi: t = fi.read()
                pers_exp, place_exp = self.get_expected_entities(f)
                m_regest = re.match(r'.*?(<summary>.*?</summary>).*', t, flags=re.S)
                if m_regest:t = re.sub(re.escape(m_regest.group(1)), self.tag_persons(m_regest.group(1), pers_exp), t, flags=re.S)
                m_letter = re.match(r'.*?(<body>.*?</body>).*', t, flags=re.S)
                if m_letter: t = re.sub(re.escape(m_letter.group(1)), self.tag_persons(m_letter.group(1), pers_exp), t, flags=re.S)
                # corrections
                t = re.sub(r'<persName ref="[^"]*">([a-z][^<]*)</persName>', r'\1', t, flags=re.S)
                t = re.sub(r'<persName ref="[^"]*">(\w{1,2})</persName>', r'\1', t, flags=re.S)
                t = re.sub(r'<persName ref="p1278">(Gast)</persName>(h[äa]us)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p540">(Calvini)</persName>(ana)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p8462">(Wied)</persName>(ereinsetz)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p467">(Buc)</persName>(h)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p7295">(Müsser)</persName>(krieg)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p458">(Brent)</persName>(iana)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<persName ref="p1974">(Luther)</persName>(ische)', r'\1\2', t, flags=re.S)
                t = re.sub(r'(</persName>)([a-z]+)', r'\2\1', t, flags=re.S)
                with open(path, 'w') as fo: fo.write(t)

    def set_tags_places(self):
        for f in os.listdir(self.output):
            if f.endswith('.xml'):
                path = os.path.join(self.output, f)
                self.tmp_places = self.read_places_from_file(f)
                with open(path) as fi: t = fi.read()
                pers_exp, place_exp = self.get_expected_entities(f)
                m_regest = re.match(r'.*?(<summary>.*?</summary>).*', t, flags=re.S)
                if m_regest:t = re.sub(re.escape(m_regest.group(1)), self.tag_places(m_regest.group(1), place_exp), t, flags=re.S)
                m_letter = re.match(r'.*?(<body>.*?</body>).*', t, flags=re.S)
                if m_letter: t = re.sub(re.escape(m_letter.group(1)), self.tag_places(m_letter.group(1), place_exp), t, flags=re.S)
                # corrections
                t = re.sub(r'<placeName ref="l862">(Schweiz)</placeName>(ergard)', r'\1\2', t, flags=re.S)
                t = re.sub(r'(<author>)<placeName ref="l217">(Wiel)</placeName>(andt</author>)', r'\1\2\3', t, flags=re.S)
                t = re.sub(r'<placeName ref="l2481">(Schwaben)</placeName>(krieg)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<placeName ref="l425">(Rom)</placeName>(anus)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<placeName ref="l2528">(Sees)</placeName>(eite)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<placeName ref="l301">(Leon)</placeName>(hard)', r'\1\2', t, flags=re.S)
                t = re.sub(r'<placeName ref="l41">(Bern)</placeName>(har[dt])', r'\1\2', t, flags=re.S)
                # --
                t = re.sub(r'(</placeName>)([a-z]+)', r'\2\1', t, flags=re.S)
                with open(path, 'w') as fo: fo.write(t)

    def tag_persons(self, s, pers_exp):
        esc, ctr = {}, 0
        for p_id in pers_exp:
            if p_id in self.tmp_persons:
                for p in self.tmp_persons[p_id]:
                    ctr += 1
                    key = '@@@' + str(ctr) + '@@@'
                    s = re.sub(re.escape(p), key, s, flags=re.S)
                    esc[key] = '<persName ref="' + p_id + '">' + p + '</persName>'
            if p_id in self.id2pers:
                for p in self.id2pers[p_id]:
                    ctr += 1
                    key = '@@@' + str(ctr) + '@@@'
                    s = re.sub(re.escape(p), key, s, flags=re.S)
                    esc[key] = '<persName ref="' + p_id + '">' + p + '</persName>'
        for key in esc: s = re.sub(key, esc[key], s, flags=re.S)
        return s

    def tag_places(self, s, place_exp):
        esc, ctr = {}, 0
        for p_id in place_exp:
            if p_id in self.tmp_places:
                for p in self.tmp_places[p_id]:
                    ctr += 1
                    key = '@@@' + str(ctr) + '@@@'
                    s = re.sub(re.escape(p), key, s, flags=re.S)
                    esc[key] = '<placeName ref="' + p_id + '">' + p + '</placeName>'
            if p_id in self.id2place:
                ctr += 1
                key = '@@@' + str(ctr) + '@@@'
                s = re.sub(re.escape(self.id2place[p_id]), key, s, flags=re.S)
                esc[key] = '<placeName ref="' + p_id + '">' + self.id2place[p_id] + '</placeName>'
        for key in esc: s = re.sub(key, esc[key], s, flags=re.S)
        return s

    def get_expected_entities(self, f):
        persons, places = {}, {}
        path = os.path.join(self.root_letters, f)
        if os.path.exists(path):
            with open(path) as fi: s = fi.read()
            persons = list(set([p for p in re.findall(r'<persName[^>]*ref="([^"]*)"', s, flags=re.S) if p != 'p495']))
            places = list(set([p for p in re.findall(r'<placeName[^>]*ref="([^"]*)"', s, flags=re.S)]))
        return persons, places

    def read_places_from_file(self, f):
        places = {}
        path = os.path.join(self.root_letters, f)
        with open(path) as fi:
            s = fi.read()
            for p in re.findall(r'<placeName[^<>]*ref="([^"]*)"[^<>]*>([^<>]*)</placeName>', s, flags=re.S):
                if p[0] not in places: places[p[0]] = []
                places[p[0]].append(p[1])
        for id_ in places: places[id_] = sorted(places[id_], key=len, reverse=True)
        return places

    def read_persons_from_file(self, f):
        persons = {}
        path = os.path.join(self.root_letters, f)
        with open(path) as fi:
            s = fi.read()
            for p in re.findall(r'<persName[^<>]*ref="([^"]*)"[^<>]*>([^<>]*)</persName>', s, flags=re.S):
                if p[0] != 'p495':
                    if p[0] not in persons: persons[p[0]] = []
                    persons[p[0]].append(p[1])
        for id_ in persons: persons[id_] = sorted(persons[id_], key=len, reverse=True)
        return persons

    def read_places(self):
        id2place = {}
        with open(self.root_places_index) as fi: s = fi.read()
        for p in re.findall(r'<place xml:id="([^"]*)"[^>]*>(.*?)</place>', s, flags=re.S):
            if p[0] not in id2place: id2place[p[0]] = []
            m_settlement = re.match(r'.*<settlement>(.*?)</settlement>.*', p[1], flags=re.S)
            m_district = re.match(r'.*<district>(.*?)</district>.*', p[1], flags=re.S)
            m_country = re.match(r'.*<country>(.*?)</country>.*', p[1], flags=re.S)
            if m_settlement: id2place[p[0]] = m_settlement.group(1)
            elif m_district: id2place[p[0]] = m_district.group(1)
            elif m_country: id2place[p[0]] = m_country.group(1)
        return id2place

    def read_persons(self):
        id2pers = {}
        with open(self.root_pers_index) as fi: s = fi.read()
        for p0 in re.findall(r'<person xml:id="P(\d+)">(.*?)</person>', s, flags=re.S):
            for p in re.findall(r'(<persName[^>]*>(.*?)</persName>)', p0[1], flags=re.S):
                if p0[0] != '495':
                    if p0[0] not in id2pers: id2pers['p'+p0[0]] = []
                    m_first = re.match(r'.*<forename>(.*?)</forename>.*', p[1], flags=re.S)
                    m_last = re.match(r'.*<surname>(.*?)</surname>.*', p[1], flags=re.S)
                    id2pers['p'+p0[0]] += self.get_variations(
                        m_first.group(1) if m_first else '',
                        m_last.group(1) if m_last else '',
                    )
        for id_ in id2pers: id2pers[id_] = sorted(list(set(id2pers[id_])), key=len, reverse=True)
        return id2pers

    def get_variations(self, first_name, last_name):
        names = []
        first_name = first_name.strip().strip('...').strip()
        last_name = last_name.strip().strip('...').strip()
        if first_name and last_name:
            names += self.get_variations_(' '.join([first_name, last_name]))
            names += self.get_variations_(', '.join([last_name, first_name]))
            names += self.get_variations_((last_name))
        elif last_name:
            names = self.get_variations_(last_name)
        elif first_name:
            names = self.get_variations_(first_name)
        return names

    def get_variations_(self, name):
        names, n = [], name.strip()
        names.append(n)
        names.append(re.sub(r'\s+', ' ', re.sub(r'[\(\)]*', '', n, flags=re.S), flags=re.S).strip())
        names.append(re.sub(r'\s+', ' ', re.sub(r'\(.*?\)', '', n, flags=re.S), flags=re.S).strip())
        names.append(re.sub(r'\s+', ' ', re.sub(r'\[.*?\]', '', n, flags=re.S), flags=re.S).strip())
        return names

    def remove_trivial_notes(self):
        for f in os.listdir(self.output):
            if f.endswith('.xml'):
                path = os.path.join(self.output, f)
                with open(path) as fi: s = fi.read()
                for e in ["persName", "placeName"]:
                    for x in re.findall(r'((<'+e+r'[^>]*ref="([^"]*)"[^>]*>[^<]*</'+e+r'>)\s*<note type="entity">\s*'+r'<'+e+r'[^>]*ref="([^"]*)"[^>]*>[^<]*</'+e+r'>[^<]*</note>)', s, flags=re.S):
                        if x[2] == x[3]: s = re.sub(re.escape(x[0]), x[1], s, flags=re.S)
                with open(path, 'w') as fo: fo.write(s)
