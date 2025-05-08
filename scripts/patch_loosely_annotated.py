import pandas as pd
from lxml import etree

# Paths
csv_path = "./scripts/src/loosely-annotated.csv"
xml_path = "./data/index/persons.xml"

# TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Read the CSV into a dictionary {id: category}
df = pd.read_csv(csv_path)
id_to_category = dict(zip(df['id'].astype(str), df['category']))

# Parse the XML
parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(xml_path, parser)
root = tree.getroot()

# Track how many updates we make
update_count = 0

# Iterate through all <person> elements
for person in root.xpath("//tei:person", namespaces=ns):
    person_id = person.get("{http://www.w3.org/XML/1998/namespace}id")
    if not person_id or not person_id.startswith("P"):
        continue

    id_without_prefix = person_id[1:]  # Remove leading 'P'

    if id_without_prefix in id_to_category:
        # Create the <desc> element
        desc = etree.Element("{http://www.tei-c.org/ns/1.0}desc")
        desc.set("type", "loosely-annotated")
        desc.text = id_to_category[id_without_prefix]

        # Handle the .tail for proper formatting
        if len(person) > 0:
            last_child = person[-1]
            desc.tail = last_child.tail  # Copy tail from last child
            last_child.tail = (last_child.tail or "") + "\t"  # Add a tab to previous child
        else:
            desc.tail = "\n\t"  # If no children, default formatting

        # Append <desc> to <person>
        person.append(desc)
        update_count += 1

# Write back to the file
xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + xml_str

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"✅ Added {update_count} <desc> elements and updated: {xml_path}")