#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re, json

""" Metadata """

def map_date(x):
    m = re.match(r'(\d\d\d\d)\-(\d\d)\-(\d\d)', x)
    if m: return ' '.join([m.group(3)+'.', get_month(m.group(2)), m.group(1)])
    else:
        m = re.match(r'(\d\d\d\d)\-(\d\d)', x)
        if m: return ' '.join([get_month(m.group(2)), m.group(1)])
    return x


def get_month(n):
    if n == '00': return '[...]'
    if n == '01': return 'Januar'
    if n == '02': return 'Februar'
    if n == '03': return 'März'
    if n == '04': return 'April'
    if n == '05': return 'Mai'
    if n == '06': return 'Juni'
    if n == '07': return 'Juli'
    if n == '08': return 'August'
    if n == '09': return 'September'
    if n == '10': return 'Oktober'
    if n == '11': return 'November'
    if n == '12': return 'Dezember'

persons = {}
with open("data/index/persons.xml") as fi: s = fi.read()
for x in re.findall(r'<persName xml:id="(p\d+)"[^>]*>\s*<surname>([^<]*)</surname>\s*<forename>([^<]*)</forename>.*?</persName>', s, flags=re.S):
    persons[x[0]] = ' '.join([x[2], x[1]])
for x in re.findall(r'<persName ref="(p\d+)"[^>]*>\s*<surname>([^<]*)</surname>\s*<forename>([^<]*)</forename>.*?</persName>', s, flags=re.S):
    persons[x[0]] = ' '.join([x[2], x[1]])


data = {}
csv = []
ROOT = "data/letters/"
files = [f for f in os.listdir(ROOT) if re.match(r'\d+\.xml', f)]
for f in sorted(files, key=lambda x: int(re.match("(\d+).*", x).group(1))):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        # head
        m = re.match(r'.*<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="file(\d+)" type="([^"]*)".*', s, flags=re.S)
        data[m.group(1)] = {}
        # sender/receiver
        data[m.group(1)]["Absender"] = {}
        data[m.group(1)]["Empfänger"] = {}
        data[m.group(1)]["Datum"] = {}



        output = [m.group(1)]
        absender = ''
        id_absender = ''
        datum = ''
        empfaender = ''
        id_empfaender = ''
        for x in re.findall(r'<correspAction type="([^"]*)">(.*?)</correspAction>', s, flags=re.S):
            if x[0] == "sent":
                for p in re.findall(r'<persName ref="([^"]*)"', x[1], flags=re.S):
                    data[m.group(1)]["Absender"][p] = persons[p]
                m_ = re.match(r'.*?<persName ref="([^"]*)".*', x[1], flags=re.S)
                if m_:
                    absender = persons[m_.group(1)]
                    id_absender = m_.group(1)
                m_date = re.match(r'.*(<date[^>]*>.*</date>|<date.*?/\s*>)', x[1], flags=re.S)
                if m_date:
                    data[m.group(1)]["Datum"] = {}
                    m_date = re.match(r'.*when="([^"]*)".*', x[1], flags=re.S)
                    if m_date:
                        datum = m_date.group(1)
                        data[m.group(1)]["Datum"]["when"] = m_date.group(1)
                        m_ymd = re.match(r'(\d+)\-0*(\d+)\-0*(\d+)', m_date.group(1))
                        m_ym = re.match(r'(\d+)\-0*(\d+)', m_date.group(1))
                        if m_ymd:
                            if m_ymd.group(1): data[m.group(1)]["Datum"]["year"] = m_ymd.group(1)
                            if m_ymd.group(2): data[m.group(1)]["Datum"]["month"] = m_ymd.group(2)
                            if m_ymd.group(3): data[m.group(1)]["Datum"]["day"] = m_ymd.group(3)
                        if m_ym:
                            if m_ym.group(1): data[m.group(1)]["Datum"]["year"] = m_ym.group(1)
                            if m_ym.group(2): data[m.group(1)]["Datum"]["month"] = m_ym.group(2)
                    else: output.append('')
                    m_date = re.match(r'.*notBefore="([^"]*)".*', x[1], flags=re.S)
                    if m_date: data[m.group(1)]["Datum"]["notBefore"] = m_date.group(1)
                    m_date = re.match(r'.*notAfter="([^"]*)".*', x[1], flags=re.S)
                    if m_date: data[m.group(1)]["Datum"]["notAfter"] = m_date.group(1)
                    m_date = re.match(r'.*<date[^>]*>(.*?)</date>.*', x[1], flags=re.S)
                    if m_date:
                        m_note = re.match(r'.*(<note[^>]*>(.*?)</note>).*', m_date.group(1), flags=re.S)
                        if m_note:
                            data[m.group(1)]["Datum"]["note"] = m_note.group(2)
                            r = re.sub(r'<note.*</note>', '', m_note.group(1), flags=re.S).strip()
                            if r: data[m.group(1)]["Datum"]["text"] = r
                        else: data[m.group(1)]["Datum"]["text"] = m_date.group(1)
            elif x[0] == "received":
                for p in re.findall(r'<persName ref="([^"]*)"', x[1], flags=re.S):
                    data[m.group(1)]["Empfänger"][p] = persons[p]
                m_ = re.match(r'.*?<persName ref="([^"]*)".*', x[1], flags=re.S)
                if m_:
                    empfaender = persons[m_.group(1)]
                    id_empfaender = m_.group(1)
        csv.append([m.group(1), re.sub(',', '', absender), id_absender, map_date(re.sub(',', '', datum)).lstrip('0').lstrip('.').strip(), re.sub(',', '', empfaender), id_empfaender])


with open("scripts/trash/metadata.json", 'w') as fo: fo.write(json.dumps(data, indent=4, separators=(',', ': ')))
with open("scripts/trash/metadata_2.csv", 'w') as fo:
    for x in csv: fo.write(', '.join(x)+'\n')

# test
with open('scripts/trash/metadata.json', encoding='utf-8') as fh:
    metadata = json.load(fh)