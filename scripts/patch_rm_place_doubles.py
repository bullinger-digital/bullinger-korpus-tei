#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re

mapping = {
    801: [584],
    781: [516],
    1274: [3083, 3082],
    862: [2502, 2463, 2564, 2516],
    489: [490],
    3340: [3341],
    473: [474],
    2651: [3047],
    435: [3102],
    73: [415],
    2604: [2622],
    2786: [2970],
    159: [2521],
    1268: [2700],
    113: [114],
    2826: [2867],
    28: [29],
    2459: [2845, 2782, 2533],
    1725: [2714],
    3114: [3143],
    1123: [2306],
    2952: [3243],
    3206: [2628],
    1044: [1448],
    1521: [2567],
    2440: [2969],
    2507: [3107, 3241],
    360: [2820],
    713: [2897],
    2983: [3352],
    337: [338],
    2297: [3266],
    1682: [2630],
    701: [3166],
    213: [664],
    822: [2555, 2496, 2544, 2498, 2513],
    1686: [3155],
    572: [609],
    1280: [3020],
    491: [492],
    404: [405],
    2464: [2497, 3217],
    1690: [2053],
    1958: [3064],
    1290: [2809],
    2414: [3100],
    1864: [3377],
    3138: [2654],
    93: [96],
    2566: [2494],
    957: [389],
    184: [1295]
}

# letters
ROOT = "data/letters/"
n_tot = len(os.listdir(ROOT))
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        for i in mapping:
            for j in mapping[i]:
                s = re.sub(r'ref="l'+str(j)+'"', r'ref="l'+str(i)+'"', s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

# register
with open("data/index/localities.xml") as fi: s = fi.read()
for i in mapping:
    for j in mapping[i]:
        s = re.sub(r'<place xml:id="l'+str(j)+'".*?</place>\s*', '', s, flags=re.S)
with open("data/index/localities.xml", 'w') as fo: fo.write(s)
