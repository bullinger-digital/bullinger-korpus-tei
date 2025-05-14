#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


places, tot = {}, 0
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_text = re.match(r'.*(<text .*)', s, flags=re.S)
        if m_text:
            text = m_text.group(1)
            for p in re.findall(r'<placeName[^>]*ref="([^"]*)"', text, flags=re.S):
                if p not in places: places[p] = 1
                else: places[p] += 1
                tot += 1

print("Places", len(places), tot)

se_tot, re_tot = 0, 0
se_, re_, all_ = {}, {}, {}
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m_se = re.match(r'.*<correspAction type="sent">(.*?)</correspAction>.*', s, flags=re.S)
        if m_se:
            se_tot += len(re.findall(r'<pers', m_se.group(1), flags=re.S))
            for x in re.findall(r'<pers[^>]*ref="([^"]*)"', m_se.group(1), flags=re.S):
                if x not in se_: se_[x] = 1
                else: se_[x] += 1
                if x not in all_: all_[x] = 1
                else: all_[x] += 1
        m_re = re.match(r'.*<correspAction type="received">(.*?)</correspAction>.*', s, flags=re.S)
        if m_re:
            re_tot += len(re.findall(r'<pers', m_re.group(1), flags=re.S))
            for x in re.findall(r'<pers[^>]*ref="([^"]*)"', m_re.group(1), flags=re.S):
                if x not in re_: re_[x] = 1
                else: re_[x] += 1
                if x not in all_: all_[x] = 1
                else: all_[x] += 1

print("Senders:", se_tot, len(se_))
print("Addressees:", re_tot, len(re_))
print("Tot:", se_tot+re_tot, len(all_))

# Langs
langs = {}
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for t in re.findall(r'<s [^>]*lang="([^"]*)', s, flags=re.S):
            if t not in langs: langs[t] = 1
            else: langs[t] += 1

for lang in langs:
    print(lang, langs[lang])
# - letters
langs = {}
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        m = re.match(r'.*<text [^>]*xml:lang="([^"]*)".*', s, flags=re.S)
        if m:
            if m.group(1) not in langs: langs[m.group(1)] = 1
            else: langs[m.group(1)] += 1

for lang in langs:
    print(lang, langs[lang])

# Scans
documents_with_scans = 0
scan_images = 0
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        n = len(re.findall(r'<desc ', s, flags=re.S))
        if n > 0: documents_with_scans += 1
        scan_images += n

print("Number of letter with scan images:", documents_with_scans)
print("Total number of scan images:", scan_images)


# Footnotes
fn_alpha, fn_num = 0, 0
n_footnotes, max_, f_max = 0, 0, ''
ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        n = len(re.findall(r'<note [^>]*type="footnote"', s, flags=re.S))
        if n > max_:
            max_ = n
            f_max = f
        n_footnotes += n
        fn_alpha += len(re.findall(r'<note [^>]*xml:id="fn\D+"[^>]*type="footnote"', s, flags=re.S))
        fn_num += len(re.findall(r'<note [^>]*xml:id="fn\d+"[^>]*type="footnote"', s, flags=re.S))

print("Footnotes:")
print(n_footnotes, max_, f)
print("Alpha:", fn_alpha)
print("Num:", fn_num)
print("other:", n_footnotes-fn_alpha-fn_num)

stats = {
    "documents": 0,
    "no_transcription": 0,
    "no_regest": 0,
    "no_footnotes": 0,
    "doc_types": {},
    "transcriptions": {},
    "regests": {},
    "footnotes": {},

}

# Places
settlements, districts, countries = {}, {}, {}
with open("data/index/localities.xml") as fi: s = fi.read()
for x in re.findall(r'<settlement>([^<]*)</settlement>', s, flags=re.S): settlements[x] = 1
for x in re.findall(r'<district>([^<]*)</district>', s, flags=re.S): districts[x] = 1
for x in re.findall(r'<country>([^<]*)</country>', s, flags=re.S): countries[x] = 1
print("Settlements:", len(settlements))
print("Districts:", len(districts))
print("Countries:", len(countries))

bibliography = {}
with open("data/index/bibliography.xml") as fi: s = fi.read()
for e in re.findall(r'<bibl xml:id="([^"]*)">.*?<title>(.*?)</title>', s, flags=re.S): bibliography[e[0]] = e[1]

def count_attribute_values(s, elem, attr, desc, stats):
    m = re.match(r'.*<'+elem+' [^>]*'+attr+'="([^"]*)".*', s, flags=re.S)
    if m:
        if m.group(1) not in stats[desc]: stats[desc][m.group(1)] = 1
        else: stats[desc][m.group(1)] += 1
    return stats

ROOT = "data/letters/"
for f in os.listdir(ROOT):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()

        stats["documents"] += 1
        stats = count_attribute_values(s, "TEI", "type", "doc_types", stats)

        m = re.match(r'.*<bibl source="([^"]*)" n="[^"]*" type="transcription"', s, flags=re.S)
        if m:
            b = bibliography[m.group(1)]
            if b not in stats["transcriptions"]: stats["transcriptions"][b] = 1
            else: stats["transcriptions"][b] += 1
        else: stats["no_transcription"] += 1

        m = re.match(r'.*<bibl source="([^"]*)" n="[^"]*" type="regest"', s, flags=re.S)
        if m:
            b = bibliography[m.group(1)]
            if b not in stats["regests"]: stats["regests"][b] = 1
            else: stats["regests"][b] += 1
        else: stats["no_regest"] += 1

        m = re.match(r'.*<bibl source="([^"]*)" n="[^"]*" type="footnotes"', s, flags=re.S)
        if m:
            b = bibliography[m.group(1)]
            if b not in stats["footnotes"]: stats["footnotes"][b] = 1
            else: stats["footnotes"][b] += 1
        else: stats["no_footnotes"] += 1

def print_counts(desc, text, stats, indent):
    print(indent*'\t'+"- "+text+" (" + str(sum([int(stats[desc][x]) for x in stats[desc]])) + ')')
    for t in dict(sorted(stats[desc].items(), key=lambda x: x[1], reverse=True)):
        print((indent+1)*'\t'+"- " + t + ' (' + str(stats[desc][t]) + ')')

print("- Number of documents:", stats["documents"]) # 13'114
print_counts("doc_types", "Document Types", stats, 1)
print("- Resources")
print("\t- documents without a transcription:", stats["no_transcription"])
print_counts("transcriptions", "Transkriptions", stats, 1)
print("\t- documents without a regest:", stats["no_regest"])
print_counts("regests", "Regests", stats, 1)
print("\t- documents without footnotes:", stats["no_footnotes"])
print_counts("footnotes", "Footnotes", stats, 1)
