import os
import re

root = "scripts/save"
for f in os.listdir(root):
    p = os.path.join(root, f)
    with open(p) as fi: s = fi.read()
    m = re.match(r'.*<TEI [^>]*type="([^"]*)".*', s, flags=re.S)
    if m and m.group(1) != "Brief": print(f, m.group(1))
