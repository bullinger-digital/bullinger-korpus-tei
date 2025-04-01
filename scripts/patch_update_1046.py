import re

with open("data/letters/1046.xml") as fi: s = fi.read()
s = re.sub(
    re.escape('<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="file1046" type="Verweis"'),
    '<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="file1046" type="Brief"', s, flags=re.S
)
s = re.sub('[ \t]*<ref type="child" target="file1047"/>[ \t]*\n', '', s, flags=re.S)
s = re.sub('[ \t]*<ref type="parent" target="file1047"/>[ \t]*\n', '', s, flags=re.S)
with open("data/letters/1046.xml", 'w') as fo: fo.write(s)
