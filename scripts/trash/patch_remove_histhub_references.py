from lxml import etree

# Define the TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

input_file = "./data/index/persons.xml"

parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(input_file, parser)
root = tree.getroot()

# Remove all <tei:idno subtype="histHub"> from within <tei:person>
for idno in root.xpath("//tei:person/tei:idno[@subtype='histHub']", namespaces=ns):
    parent = idno.getparent()
    tail = idno.tail

    # Transfer the tail to the previous sibling or the parent
    prev = idno.getprevious()
    if tail:
        if prev is not None:
            prev.tail = tail
        else:
            parent.text = tail

    parent.remove(idno)

# Serialize and save the XML
xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + xml_str
with open(input_file, "w", encoding="utf-8") as f:
    f.write(xml_str)
print(f"✅ Saved: {input_file}")