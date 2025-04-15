#!/usr/bin/python
# -*- coding: utf8 -*-

import os, re


new_file_types = {
    365: "Brief", 721: "Brief", 789: "Beilage", 1008: "Brief", 1022: "Brief", 1048: "Brief", 1136: "Brief",
    1250: "Brief", 1274: "Gutachten", 1688: "Brief", 1845: "Brief", 1940: "Brief", 2312: "Brief", 3117: "Brief",
    3363: "Brief", 3641: "Brief", 3700: "Brief", 3747: "Brief", 3763: "Brief", 3778: "Brief", 3779: "Brief",
    3831: "Brief", 4177: "Brief", 4229: "Brief", 4292: "Brief", 4325: "Brief", 4471: "Brief", 4831: "Brief",
    4880: "Brief", 5272: "Hinweis", 5640: "Brief", 6889: "Brief", 7068: "Brief", 7308: "Brief", 7608: "Brief",
    8424: "Brief", 8565: "Brief", 8596: "Brief", 8772: "Brief", 8850: "Brief", 9063: "Brief", 9135: "Brief",
    9519: "Brief", 9846: "Brief", 12947: "Brief"
}

ROOT = "data/letters/"
for id_ in new_file_types:
    path = os.path.join(ROOT, str(id_)+'.xml')
    with open(path) as fi: s = fi.read()
    s = re.sub(r'(<TEI [^>]*type=")[^"]*(")', r'\1'+new_file_types[id_]+r'\2', s, flags=re.S)
    with open(path, 'w') as fo: fo.write(s)
