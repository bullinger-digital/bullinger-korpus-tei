#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


with open("data/index/persons.xml") as fi: s = fi.read()

entries = [e for e in re.findall(r'[\t ]*<persName xml:id.*?</persName>', s, flags=re.S)]
nof_entries = len([p for p in re.findall(r'<persName xml:id', s, flags=re.S)])  # 19359
nof_urls = len([url for url in re.findall(r'<idno.*?</idno>', s, flags=re.S)])  # 4977
#print(set([x for x in re.findall(r'<idno subtype="([^"]*)"', s, flags=re.S)])) # {'gnd', 'portrait', 'histHub', 'wiki', 'url'}
nof_urls_gnd = len([url for url in re.findall(r'<idno subtype="gnd".*?</idno>', s, flags=re.S)])  # 2496
nof_urls_wiki = len([url for url in re.findall(r'<idno subtype="wiki".*?</idno>', s, flags=re.S)])  # 1776
nof_urls_hh = len([url for url in re.findall(r'<idno subtype="histHub".*?</idno>', s, flags=re.S)])  # 219
nof_urls_p = len([url for url in re.findall(r'<idno subtype="portrait".*?</idno>', s, flags=re.S)])  # 482
nof_urls_url = len([url for url in re.findall(r'<idno subtype="url".*?</idno>', s, flags=re.S)])  # 1

url_list = [url for url in re.findall(r'<idno subtype="portrait"[^>]*>(.*?)</idno>', s, flags=re.S)]
url_set = set(url_list)
print(len(url_set), len(url_list), len(url_list)-len(url_set))

# - doubles
doubles = [u for u in url_list if len(re.findall(re.escape(u), s, flags=re.S)) > 1]
hits = list(set([str(len(re.findall('>'+re.escape(d)+'<', s, flags=re.S)))+"x "+d for d in doubles]))
for h in hits: print(h)


""" 
2x https://data.histhub.ch/person/11484026
2x https://data.histhub.ch/person/11080392
2x https://data.histhub.ch/person/11467475

3x https://d-nb.info/gnd/11867661X
3x https://d-nb.info/gnd/101100655
2x https://d-nb.info/gnd/118787004
2x https://d-nb.info/gnd/118626183
2x https://d-nb.info/gnd/118966774
2x https://d-nb.info/gnd/131632396
2x https://d-nb.info/gnd/11707392X
2x https://d-nb.info/gnd/1089449259
2x https://d-nb.info/gnd/118803751
2x https://d-nb.info/gnd/118626671
2x https://d-nb.info/gnd/136138225
2x https://d-nb.info/gnd/11862234X
2x https://d-nb.info/gnd/118955314
2x https://d-nb.info/gnd/104206527
2x https://d-nb.info/gnd/118544225
2x https://d-nb.info/gnd/118868381
2x https://d-nb.info/gnd/118604597
2x https://d-nb.info/gnd/12360317X
2x https://d-nb.info/gnd/11947204X
2x https://d-nb.info/gnd/13610990X
2x https://d-nb.info/gnd/118810944
2x https://d-nb.info/gnd/133796078
2x https://d-nb.info/gnd/118730819
2x https://d-nb.info/gnd/11889109X
2x https://d-nb.info/gnd/138227101
2x https://d-nb.info/gnd/118738062
2x https://d-nb.info/gnd/118966219
2x https://d-nb.info/gnd/118530577
2x https://d-nb.info/gnd/118798170
2x https://d-nb.info/gnd/11874786X
2x https://d-nb.info/gnd/119214644
2x https://d-nb.info/gnd/119639246
2x https://d-nb.info/gnd/118641158
2x https://d-nb.info/gnd/118710656
2x https://d-nb.info/gnd/1012285146

2x https://de.wikipedia.org/wiki/Jacques_de_Savoie-Nemours
2x https://de.wikipedia.org/wiki/Hans_Funk_(Glasmaler)
2x https://de.wikipedia.org/wiki/August_(Sachsen)
2x https://de.wikipedia.org/wiki/Heinrich_Vogtherr_der_%C3%84ltere
2x https://de.wikipedia.org/wiki/Brunichild
2x https://de.wikipedia.org/wiki/Marcus_Terentius_Varro
2x https://de.wikipedia.org/wiki/Siegmund_von_Herberstein
2x https://de.wikipedia.org/wiki/Herennius_Modestinus
2x https://de.wikipedia.org/wiki/Epiktet
2x https://de.wikipedia.org/wiki/Aischylos
2x https://de.wikipedia.org/wiki/Gaspard_II._de_Coligny
2x https://de.wikipedia.org/wiki/Johann_Jakob_Fugger
2x https://de.wikipedia.org/wiki/Arnoldus_Vesaliensis
2x https://de.wikipedia.org/wiki/Gaius_Verres
2x https://fr.wikipedia.org/wiki/Fran%C3%A7ois_de_Luxembourg_(fils)
2x https://de.wikipedia.org/wiki/Freyberg_(Adelsgeschlecht)
2x https://de.wikipedia.org/wiki/Ulrich_R%C3%B6sch
2x https://de.wikipedia.org/wiki/Thomas_Morus
2x https://de.wikipedia.org/wiki/Liste_der_B%C3%BCrgermeister_und_Oberb%C3%BCrgermeister_von_Kempten_(Allg%C3%A4u)
2x https://de.wikipedia.org/wiki/Ernst_III._(Braunschweig-Grubenhagen)
2x https://de.wikipedia.org/wiki/Waldkirch_(Adelsgeschlecht)
2x https://de.wikipedia.org/wiki/Anton_II._(Lothringen)
2x https://de.wikipedia.org/wiki/Ulrich_Varnb%C3%BCler
2x https://de.wikipedia.org/wiki/Hans_von_Hutten
2x https://de.wikipedia.org/wiki/Marcellus_II.

2x 4516_Carion_Johannes.jpg
2x 7479_von_Frundsberg_Georg.jpg

"""