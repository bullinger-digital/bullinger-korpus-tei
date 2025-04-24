import os, re


ROOT, count = "data/letters/", 0
for f in os.listdir(ROOT):
    if f.endswith('.xml'):
        p = os.path.join(ROOT, f)
        with open(p) as fi: s = fi.read()
        nlb = len(re.findall(r'<lb ', s, flags=re.S))
        ns = len(re.findall(r'<s ', s, flags=re.S))
        m_is_empty = re.match(r'.*Keine Transkription verfügbar.*', s, flags=re.S)
        m_has_transtripction = re.match(r'<bibl[^>]*type="transcription">', s, flags=re.S)
        m_has_source = re.match(r'.*<TEI [^>]*source="keine".*', s, flags=re.S)
        if ns == 0 and not m_has_source:
            print("***Warning", f)
            count += 1

print("Total:", count)

