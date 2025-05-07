#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

''' Tex2tei: Verify mapping id_edition -> id_corpus '''

MAPPING = {  # manually by PS (correction: 3134->34 [not 29!])
    "3102": "5", "3103": "4", "3104": "6", "3105": "7", "3106": "8", "3107": "9", "3108": "10", "3109": "11",
    "3110": "12", "3111": "14", "3112": "15", "3113": "16", "3114": "17", "3115": "18", "3116": "19", "3117": "20",
    "3118": "21", "3119": "22", "3120": "23", "3121": "3", "3122": "24", "3123": "25", "3124": "26", "3125": "27",
    "3126": "58", "3127": "31", "3128": "30", "3129": "32", "3130": "33", "3131": "37", "3132": "38", "3133": "39",
    "3134": "34", "3135": "40", "3136": "35", "3137": "29", "3138": "42", "3139": "44", "3140": "43", "3141": "45",
    "3142": "46", "3143": "47", "3144": "48", "3145": "49", "3146": "50", "3147": "51", "3148": "52", "3149": "54",
    "3150": "53", "3151": "55", "3152": "57", "3153": "60", "3154": "61", "3155": "62", "3156": "63", "3157": "65",
    "3158": "66", "3159": "67", "3160": "68", "3161": "59", "3162": "69", "3163": "70", "3164": "71", "3165": "72",
    "3166": "73", "3167": "74", "3168": "76", "3169": "77", "3170": "75", "3171": "78", "3172": "79", "3173": "80",
    "3174": "81", "3175": "82", "3176": "84", "3177": "13155", "3178": "93", "3179": "86", "3180": "90", "3181": "87",
    "3182": "88", "3183": "89", "3184": "91", "3185": "92", "3186": "94", "3187": "95", "3188": "96", "3189": "97",
    "3190": "98", "3191": "99", "3192": "100", "3193": "103", "3194": "101", "3195": "102", "3196": "104", "3197": "105"
}

# verify tex2tei-output
ROOT = 'tex2tei/output/'
for id_irg in MAPPING:
    p = os.path.join(ROOT, MAPPING[id_irg]+'.xml')
    if not os.path.exists(p):
        print("*Warning, ", p, "doesn't exist!")
    else:
        with open(p) as fi: s = fi.read()
        if not re.match(r'.*<TEI[^>]*n="'+id_irg+'".*', s, flags=re.S):
            print("*Warning, unexpected ID in", p)

# restore?
hbbw_21_corpus = {}
ROOT = '../data/letters/'
for f in os.listdir(ROOT):
    p = os.path.join(ROOT, f)
    if p.endswith('.xml'):
        with open(p) as fi: s = fi.read()
        src = re.match(r'.*<TEI[^>]*source="([^"]*)".*', s, flags=re.S).group(1)
        #if not m_src: print("*Warning, source-attr. missing in", f)
        if src == 'HBBW-21': hbbw_21_corpus[f.strip('.xml')] = True

hbbw_21_mapping = [MAPPING[i] for i in MAPPING]
for id in hbbw_21_corpus:
    if id not in hbbw_21_mapping: pass # print(id)

ROOT = 'save'
for f in os.listdir(ROOT):
    id = f.strip('.xml')
    if id not in hbbw_21_mapping: print("Restore", f)
