#!/usr/bin/python
# -*- coding: utf8 -*-

""" provide additional information in case of matching issues """

config = {

    # Bibliography
    "YEAR": 2025,
    "EDITION_NUMBER": 21,
    "ID_BIB": 720,  # see corpus/data/index/bibliography.xml
    "BIBLIOGRAPHY": "Heinrich Bullinger Werke, Briefwechsel Band " + str(21) + " (Briefe von Januar bis April 1548), bearb. von David Mache und Paul Achim Neuendorf, Zürich 2024, 504 S., ISBN 978-3-290-18668-5.",
    # Matching
    "IDS": {  # filename -> Corpus-ID (see corpus/data/letters/)
        "3131-18028-Leonhard_Serin_an_Bullinger,_[Ulm],_6._Februar_1548.tex": 37,
        "3132-18029-Joachim_Vadian_an_Bullinger,_St._Gallen,_6._Februar_1548.tex": 38,
        '3110-18007-Ambrosius_Blarer_an_Bullinger,_[Konstanz],_18._Januar_1548.tex': 12,
        '3137-18032-Bullinger_an_Oswald_Myconius,_Zürich,_11._Februar_1548.tex': 29,
        '3195-18083-Joachim_Vadian_an_Bullinger,_[St._Gallen],_[26._April_1548].tex': 102,
        '3148-18042-Bullinger_an_Oswald_Myconius,_Zürich,_25._Februar_1548.tex': 52,
        '3188-18079-Ambrosius_Blarer_an_Bullinger,_[Konstanz],_18._April_1548.tex': 96,
        '3189-18346-Paul_Wala_Schuler_an_Bullinger,_Schwanden,_18._April_1548.tex': 97,
        '3190-18347-Bullinger_an_Paul_Wala_Schuler,_Zürich,_20._April_1548.tex': 98,
        '3194-18082-Joachim_Vadian_an_Bullinger,_St._Gallen,_26._April_1548.tex': 101,
        '3193-18348-Johann_Valentin_Furtmüller_an_[Bullinger],_St._Gallen,_9._April_1548-26._April_1548.tex': 103,
    },
    "CORRESPONDENTS": { # persName -> id (see corpus/data/index/persons.xml)
        "Heinrich Bullinger [Antistes]": 'p495',
        "Georg von Württemberg-Mömpelgard": 'p8098',
        "Georg Frölich": 'p8354',
        "Benedikt Schürmeister": 'p2938',
        "Sebastian Schertlin": 'p2916',
        "Béat Comte": 'p6148',
        "Gilbert Cousin (Cognatus)": 'p8073',
    },
    "PLACES": { # placeName -> id (see corpus/data/index/localities.xml)
        "Zürich": 'l587',  # die Stadt, nicht der Kanton
        "Biel": 'l49',
        "Reichenweier": 'l411',
        "Strassburg": 'l491'
    },
    "ARCHIVES": { # archiveName -> id (see corpus/data/index/archives.xml)
        "St. Gallen Kantonsbibliothek Vadiana": 'a78',
    },

    # PATHS
    "PATHS": {
        "INPUT": "input/",
        "OUTPUT": "output/",
        "CORPUS": {
            "LETTERS": "../../data/letters",
            "PERSONS": "../../data/index/persons.xml",
            "PLACES": "../../data/index/localities.xml",
            "ARCHIVES": "../../data/index/archives.xml",
            "BIBLIOGRAPHY": "../../data/index/bibliography.xml"
        }
    },

    # OTHER
    "URL_TEI_DTD": "https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng"
}
