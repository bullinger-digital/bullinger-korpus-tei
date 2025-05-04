import os, re

print("New Letters:", len([f for f in os.listdir("scripts/tex2tei/output") if f.endswith('.xml')]))  # 95

ROOT, count = "data/letters/", 0
for f in sorted(os.listdir(ROOT)):
    if re.match(r'.*\.xml', f):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        if re.match(r'.*source="HBBW\-21".*', s, flags=re.S): count += 1

print("HBBW-21 (Corpus):", count)  # 95

# analysis.py: «source="HBBW\-21"» --> 95
