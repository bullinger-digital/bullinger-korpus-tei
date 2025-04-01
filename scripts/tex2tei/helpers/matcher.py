#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re

""" matching between latex- and corpus-letters """


class Matcher:

    """ map: ID_TUSTEP -> ID_Corpus """

    def __init__(self, config):
        self.config = config
        self.data = {}
        self.mapping = {}
        self.unknown = 0
        self.print_info = True
        # paths
        self.root_letters = config["PATHS"]["CORPUS"]["LETTERS"]
        self.root_pers_index = config["PATHS"]["CORPUS"]["PERSONS"]
        self.root_places_index = config["PATHS"]["CORPUS"]["PLACES"]
        self.root_archives = config["PATHS"]["CORPUS"]["ARCHIVES"]
        self.root_input = config["PATHS"]["INPUT"]
        self.root_output = config["PATHS"]["OUTPUT"]
        # maps
        self.date2id = self.get_date2id()  # map: date -> list of potential file ids
        self.pers2id = self.get_pers2id()
        self.place2id = self.get_place2id()
        self.id2corr = self.get_id2corr()
        self.archive2id = self.get_archive2id()
        # ---
        self.match()

    def match(self):  # create map "self.mapping": id_tustep -> id_corpus
        if self.print_info: print("- matching letters ...")
        for f in os.listdir(self.root_output):
            os.remove(os.path.join(self.root_output, f))
        self.get_mapping_from_corpus()  # corpus-lookup
        id_candidates = []
        for f in sorted(os.listdir(self.root_input)):
            if re.match(r'.*\.tex', f):
                with open(os.path.join(self.root_input, f)) as fi: s = fi.read()
                self.tmp = {
                    "filename": f,
                    "id_tustep": '',
                    "senders": {},
                    "addressees": {},
                    "place": {},
                    "date": {},
                }
                m = re.match(r'^([^\-]+)\-([^\-]+)\-(.+?)_an_(.+?),_(.*?),_(.*?)\.tex$', f)
                if m:
                    number = m.group(2)
                    sender = m.group(3)
                    addressee = m.group(4)
                    place = m.group(5)
                    date = m.group(6)

                    self.tmp["id_tustep"] = number
                    cert = "low" if '[' in place or ']' in place or '(' in place or ')' in place else "high"
                    place = re.sub(r'_', ' ', place, flags=re.S)
                    place = re.sub(r'[\[\]\(\)]', '', place, flags=re.S)
                    if place in self.place2id or place in self.config["PLACES"]:
                        if place in self.config["PLACES"]: self.tmp["place"]["id"] = self.config["PLACES"][place]
                        else: self.tmp["place"]["id"] = self.place2id[place]
                        self.tmp["place"]["name"] = place
                        self.tmp["place"]["cert"] = cert
                    elif place: print("*Warning, couldn't identify place:", place)
                    correspondents = '_an_'.join([sender, addressee])
                    fn_new = ',_'.join([correspondents, place, date])+'.tex'
                    id_candidates = []
                    id_candidates = self.get_mapping_from_date(number, date)
                    self.get_mapping_from_correspondents(number, sender, addressee, id_candidates)
                    if number not in self.mapping and f in self.config["IDS"]:
                        self.mapping[number] = str(self.config["IDS"][f])
                    if number not in self.mapping:
                        self.unknown += 1
                        fn_new = "unknown"+str(self.unknown)+'.xml'
                        self.data["unknown"+str(self.unknown)] = self.tmp
                        print("Warning, couldn't match", f)
                    else:
                        fn_new = str(self.mapping[number]) + '.xml'
                        self.data[self.mapping[number]] = self.tmp
                    with open(os.path.join(self.root_output, fn_new), 'w') as fo: fo.write(s)
                else: print("*Warning, invalid file name:", f)
        #for d in self.data: print(d, self.data[d])

    # CORPUS
    # - ids
    def get_mapping_from_corpus(self):  # extract tustep-ids from corpus
        for f in os.listdir(self.root_letters):
            m_id_file = re.match(r'(.*)\.xml', f)
            if m_id_file:
                with open(os.path.join(self.root_letters, f)) as fi: s = fi.read()
                m_id_tustep = re.match(r'.*<TEI [^>]*source="TUSTEP" n="(\d+)">.*', s, flags=re.S)
                if m_id_tustep: self.mapping[m_id_tustep.group(1)] = m_id_file.group(1)
    # - dates
    def get_date2id(self):  # extract dates from corpus
        date2id = {}  # e.g. "1557-12-08" -> ['3428', '3429']
        for f in os.listdir(self.root_letters):
            m_id_file = re.match(r'(.*)\.xml', f)
            if m_id_file:
                id_file = m_id_file.group(1)
                with open(os.path.join(self.root_letters, f)) as fi: s = fi.read()
                m = re.match(r'.*<correspAction type="sent">(.*?)</correspAction>.*', s, flags=re.S)
                if m:
                    md = re.match(r'.*(<date.*?>).*', m.group(1), flags=re.S)
                    if md:
                        m_when = re.match(r'.*when="([^"]*)".*', md.group(1), flags=re.S)
                        m_not_before = re.match(r'.*notBefore="([^"]*)".*', md.group(1), flags=re.S)
                        m_not_after = re.match(r'.*notAfter="([^"]*)".*', md.group(1), flags=re.S)
                        cert = re.match(r'.*cert="([^"]*)".*', md.group(1), flags=re.S)
                        d_key = ''
                        if m_when: d_key = m_when.group(1)
                        else:
                            if m_not_after and m_not_after: d_key = m_not_before.group(1)+'--'+m_not_after.group(1)
                            elif m_not_before: d_key = m_not_before.group(1)
                            elif m_not_after: d_key = m_not_after.group(1)
                        if d_key:
                            if d_key in date2id: date2id[d_key].append(id_file)
                            else: date2id[d_key] = [id_file]
        return date2id

    def get_mapping_from_date(self, number, date):
        id_candidates = []
        date_key = self.get_date_key(date)
        if date_key in self.date2id:
            if len(self.date2id[date_key]) == 1 and number not in self.mapping:
                self.mapping[number] = self.date2id[date_key][0]
            else: id_candidates = self.date2id[date_key]
        return id_candidates

    def get_date_key(self, date):
        m, d1, d2 = re.match(r'(.*)\-(.*)', date), None, None
        if m: d1, d2 = self.fn_date_parser(m.group(1)), self.fn_date_parser(m.group(2))
        else: d1 = self.fn_date_parser(date)
        dstr_1 = ((d1[2] if d1[2] else '') + '-' + (d1[1] if d1[1] else '') + '-' + (d1[0] if d1[0] else '')).strip('-')
        if d2:
            dstr_2 = ((d2[2] if d2[2] else '') + '-' + (d2[1] if d2[1] else '') + '-' + (d2[0] if d2[0] else '')).strip('-')
            self.tmp["date"]["notBefore"] = dstr_1
            self.tmp["date"]["notAfter"] = dstr_2
        else:
            dstr_2 = ''
            self.tmp["date"]["when"] = dstr_1
        return (dstr_1 + '--' + dstr_2).strip('-')

    def fn_date_parser(self, date):
        cert = "low" if '\[' and '\[' in date else "high"
        date = re.sub(r'[\[\]]*', '', date)
        day, month, year = 0, 0, 0
        m1 = re.match(r'^(\[?\d+\]?)$', date)
        m2 = re.match(r'^(\[?[A-Za-zä]+\]?)_(\[?\d+\]?)$', date)
        m3 = re.match(r'^(\[?\d+\.\]?)_(\[?[A-Za-zää]+\]?)_(\[?\d+\]?)$', date)  # two different 'ä' ("März")!
        if m1:
            year = m1.group(1)
        elif m2:
            year = m2.group(2)
            month = self.map_month(m2.group(1))
        elif m3:
            year = m3.group(3)
            month = self.map_month(m3.group(2))
            day = m3.group(1).rstrip('.')
            if len(day) == 1: day = '0' + day
        self.tmp["date"]["cert"] = cert
        return [day, month, year, cert]

    def map_month(self, month):
        months = {
            "Januar": '01',
            "Februar": '02',
            "März": '03',
            "März": '03',
            "April": '04',
            "Mai": '05',
            "Juni": '06',
            "Juli": '07',
            "August": '08',
            "September": '09',
            "Oktober": '10',
            "November": '11',
            "Dezember": '12',
        }
        if month not in months: return '00'
        else: return months[month]

    # - correspondents
    def get_pers2id(self):
        data = dict()
        with open(self.root_pers_index) as fi: s = fi.read()
        for p in re.findall(r'(<persName[^>]*?ref="([^"]*)".*?</persName>)', s, flags=re.S):
            m_surname = re.match(r'.*<surname>(.*?)</surname>.*', p[0], flags=re.S)
            m_forename = re.match(r'.*<forename>(.*?)</forename>.*', p[0], flags=re.S)
            surname = m_surname.group(1) if m_surname else ''
            forename = m_forename.group(1) if m_forename else ''
            n1 = (' '.join([forename, surname])).strip()
            n2 = re.sub(r'\s+', ' ', re.sub(r'[\(\)]*', '', n1, flags=re.S).strip(), flags=re.S)
            n3 = re.sub(r'\s+', ' ', re.sub(r'\(.*?\)', '', n1, flags=re.S).strip(), flags=re.S)
            n4 = re.sub(r'\s+', ' ', re.sub(r'\[.*?\]', '', n1, flags=re.S).strip(), flags=re.S)
            n5 = re.sub(r'\s+', ' ', re.sub(r'é', 'e', n1, flags=re.S).strip(), flags=re.S)
            for name in [n1, n2, n3, n4, n5]:
                if name in data: data[name].append(p[1])
                else: data[name] = [p[1]]
        for x in data: data[x] = list(set(data[x]))
        return data

    def get_id2corr(self):
        data = dict()
        for f in os.listdir(self.root_letters):
            m_id_file = re.match(r'(.*)\.xml', f)
            if m_id_file:
                data[m_id_file.group(1)] = {'s': [], 'a': []}
                with open(os.path.join(self.root_letters, f)) as fi: s = fi.read()
                m_s = re.match(r'.*<correspAction type="sent">(.*?)</correspAction>', s, flags=re.S)
                if m_s:
                    for p in re.findall(r'<persName[^>]*ref="([^"]*)"', m_s.group(1), flags=re.S):
                        data[m_id_file.group(1)]['s'].append(p)
                m_a = re.match(r'.*<correspAction type="received">(.*?)</correspAction>', s, flags=re.S)
                if m_a:
                    for p in re.findall(r'<persName[^>]*ref="([^"]*)"', m_a.group(1), flags=re.S):
                        data[m_id_file.group(1)]['a'].append(p)
        return data

    def get_place2id(self):
        data = {}
        with open(self.root_places_index) as fi: s = fi.read()
        for p in re.findall(r'<place xml:id="([^"]*)">(.*?)</place>', s, flags=re.S):
            m_s = re.match(r'.*<settlement>([^<]*?)</settlement>.*', p[1], flags=re.S)
            m_d = re.match(r'.*<district>([^<]*?)</district>.*', p[1], flags=re.S)
            m_c = re.match(r'.*<country>([^<]*?)</country>.*', p[1], flags=re.S)
            if m_s: data[m_s.group(1)] = p[0]
            elif m_d: data[m_d.group(1)] = p[0]
            elif m_c: data[m_c.group(1)] = p[0]
        return data

    def get_mapping_from_correspondents(self, number, senders, addressees, id_candidates):
        s, a = self.extract_correspondents(senders, addressees)
        candidates = []
        for id_ in id_candidates:
            if self.cmp_corrs(id_, s, a): candidates.append(id_)
        if len(candidates) == 1 and number not in self.mapping: self.mapping[number] = candidates[0]

    def extract_correspondents(self, senders, addressees):
        s, a = {}, {}
        for s_ in [i.strip() for i in re.sub(r'_', ' ', senders, flags=re.S).split('&')]:
            id_, cert = self.identify_correspondet(s_, 's')
            if not id_: print("*Warning: unknown correspondent:", s_)
            else:
                s[id_] = s_
                self.tmp["senders"][id_] = (s_, cert)
        for a_ in [i.strip() for i in re.sub(r'_', ' ', addressees, flags=re.S).split('&')]:
            id_, cert = self.identify_correspondet(a_, 'a')
            if not id_: print("*Warning: unknown correspondent:", a_)
            else:
                a[id_] = a_
                self.tmp["addressees"][id_] = (a_, cert)
        return s, a

    def identify_correspondet(self, name, corr_type):
        cert = "low" if '[' in name or ']' in name else "high"
        name = re.sub(r'[\[\]]', '', name, flags=re.S)
        if name in ["Bullinger", "Heinrich Bullinger", "HB", "H.B."]: return ('p495', cert)
        elif name in self.pers2id and len(self.pers2id[name]) == 1: return (self.pers2id[name][0], cert)
        elif name in self.config["CORRESPONDENTS"]: return (self.config["CORRESPONDENTS"][name], cert)
        return '', cert

    def cmp_corrs(self, id_file, s, a):
        if id_file in self.id2corr:
            s_tar = self.id2corr[id_file]['s']
            a_tar = self.id2corr[id_file]['a']
            for s_ in s_tar:
                if s_ not in s: return False
            for a_ in a_tar:
                if a_ not in a: return False
            for s_ in s:
                if s_ not in s_tar: return False
            for a_ in a:
                if a_ not in a_tar: return False
            if len(s_tar) != len(s): return False
            if len(a_tar) != len(a): return False
            return True
        return False

    def get_archive2id(self):
        data = {}
        with open(self.root_archives) as fi: s = fi.read()
        for a in re.findall(r'(<org xml:id="([^"]*)".*?</org>)', s, flags=re.S):
            m_name = re.match(r'.*?<orgName>(.*?)</orgName>.*', a[0], flags=re.S)
            if m_name: data[m_name.group(1)] = a[1]
            m_name = re.match(r'.*?<addName>(.*?)</addName>.*', a[0], flags=re.S)
            if m_name: data[m_name.group(1)] = a[1]
        for a in self.config["ARCHIVES"]: data[a] = self.config["ARCHIVES"][a]
        return data


if __name__ == '__main__':

    Matcher()
