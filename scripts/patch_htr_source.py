import os
from lxml import etree

# Namespace
NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
TEI = "{http://www.tei-c.org/ns/1.0}"

# Paths
input_folder = './data/letters'  # Adjust as needed
output_folder = input_folder     # Can be changed if desired

# Tracking
modified_count = 0
error_files = []

def process_file(path):
    global modified_count
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(path, parser)
    root = tree.getroot()

    # Check condition: @source='keine'
    if root.get('source') != 'keine':
        return

    # Check condition: at least one <lb xml:id> under ./tei:text
    text_el = root.find("./tei:text", namespaces=NS)
    if text_el is None or not text_el.xpath(".//tei:lb[@xml:id]", namespaces=NS):
        return

    # Find fileDesc/sourceDesc inside teiHeader
    source_desc = root.find("./tei:teiHeader/tei:fileDesc/tei:sourceDesc", namespaces=NS)
    if source_desc is None:
        return

    # Error if bibl[type='transcription'] already exists
    if source_desc.find("tei:bibl[@type='transcription']", namespaces=NS) is not None:
        error_files.append(os.path.basename(path))
        return

    # Modify @source to HTR
    root.set('source', 'HTR')

    # Create <bibl type="transcription">Automatische Transkription</bibl>
    new_bibl = etree.Element(TEI + "bibl", type="transcription")
    new_bibl.text = "Automatische Transkription"

    # Handle tail formatting
    children = list(source_desc)
    if children:
        new_bibl.tail = children[0].tail  # preserve tail of the first element
        source_desc.insert(0, new_bibl)
    else:
        new_bibl.tail = "\n" + " " * 16  # fallback formatting
        source_desc.append(new_bibl)

    # Write back with XML declaration
    xml_bytes = etree.tostring(tree, encoding="utf-8", xml_declaration=False, pretty_print=True)
    xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_bytes.decode("utf-8")
    # Remove trailing newline
    xml_str = xml_str.rstrip("\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    modified_count += 1
    print(f"✅ Modified: {os.path.basename(path)}")

# Traverse XML files
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
        process_file(os.path.join(input_folder, filename))

# Summary
print(f"\nModified letters: {modified_count}")
if error_files:
    print("⚠️ Error: <bibl type='transcription'> already exists in:")
    for fname in error_files:
        print(f"  - {fname}")