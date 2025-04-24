import os, re


ROOT, count = "data/letters/", 0
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        s = re.sub(
            r'<body>\s*<bibl>\s*(\[[Kk]eine Transkription verfügbar\.?\])\s*</bibl>\s*</body>',
            r'<body>\n\t\t\t<div>\n\t\t\t\t<p>\n\t\t\t\t\t<bibl>\1</bibl>\n\t\t\t\t</p>\n\t\t\t</div>\n\t\t</body>',
            s, flags=re.S)
        with open(p, 'w') as fo: fo.write(s)

print("Total:", count)
