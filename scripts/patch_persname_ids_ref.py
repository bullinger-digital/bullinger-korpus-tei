from lxml import etree

# Define the TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

input_file = "./data/index/persons.xml"

parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(input_file, parser)
root = tree.getroot()

# Iterate through all <person> elements
for person in root.xpath("//tei:person", namespaces=ns):
    person_id = person.get("{http://www.w3.org/XML/1998/namespace}id")
    if not person_id:
        continue  # Skip if no xml:id

    for persName in person.xpath("tei:persName", namespaces=ns):
        # Remove 'ref' and existing 'xml:id'
        if 'ref' in persName.attrib:
            del persName.attrib['ref']
        if '{http://www.w3.org/XML/1998/namespace}id' in persName.attrib:
            del persName.attrib['{http://www.w3.org/XML/1998/namespace}id']

        # If it's the main name, add a new xml:id based on parent @xml:id (lowercased)
        if persName.get("type") == "main":
            new_id = person_id.lower()

            # Remove and re-add type to control attribute order (xml:id first)
            type_val = persName.attrib.pop("type", None)
            persName.set("{http://www.w3.org/XML/1998/namespace}id", new_id)
            if type_val:
                persName.set("type", type_val)


xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + xml_str
with open(input_file, "w", encoding="utf-8") as f:
    f.write(xml_str)
print(f"✅ Updated and saved: {input_file}")
