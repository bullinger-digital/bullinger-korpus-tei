#!/usr/bin/python
# -*- coding: utf8 -*-

""" add mappings in case of matching issues ... """

config = {

    # Bibliography
    "YEAR": 2025,
    "EDITION_NUMBER": 21,
    "ID_BIB": 720,
    "BIBLIOGRAPHY": "Heinrich Bullinger Werke, Briefwechsel Band " + str(21) + " (Briefe von Januar bis April 1548),"
                    "bearb. von David Mache und Paul Achim Neuendorf, Zürich 2024, 504 S., ISBN 978-3-290-18668-5.",
    # Matching
    "IDS": {  # filename -> Corpus-ID (see corpus/data/letters/)
        '065-18339-Leonard_Serin_an_Bullinger,_Ulm,_19._März_1548.tex': 73,
        '076-18345-Ambrosius_Blarer_an_Bullinger,_[Konstanz],_[4.]_April_1548.tex': 13155,
        '092-18348-Johann_Valentin_Furtmüller_an_[Bullinger],_St._Gallen,_-26._April_1548.tex': 103,
        '094-18083-Joachim_Vadian_an_Bullinger,_St._Gallen,_26._April_1548.tex': 102,
        '020-18336-Bullinger_an_Rudolf_Gwalther,_Zürich,_[28.]_Januar_1548-[31.]_Januar_1548.tex': 3,
        '009-18007-Ambrosius_Blarer_an_Bullinger,_[Konstanz],_18._Januar_1548.tex': 12,
        '036-18032-Bullinger_an_Oswald_Myconius,_Zürich,_11._Februar_1548.tex': 29,
        '093-18082-Joachim_Vadian_an_Bullinger,_St._Gallen,_26._April_1548.tex': 101
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
        "Zürich": 'l587',
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
        }
    },

    # OTHER
    "URL_TEI_DTD": "https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng"
}
