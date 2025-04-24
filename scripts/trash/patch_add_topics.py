import pandas as pd
from lxml import etree
import os

# TEI namespace
NS = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Paths
csv_path = './scripts/src/merged_topics_ids.csv'
input_folder = './data/letters'
output_folder = input_folder

# Load CSV with File ID and Topics columns
df = pd.read_csv(csv_path, converters={'File ID': str})
df['File ID'] = df['File ID'].str.strip()

# Convert topic string to list of ints
df['Topics'] = df['Topics'].apply(eval)

def create_encoding_desc(topics):
    """Create the <encodingDesc> element with topic-based categories."""
    encoding_desc = etree.Element("{http://www.tei-c.org/ns/1.0}encodingDesc")
    encoding_desc.text = "\n\t\t\t"
    encoding_desc.tail = "\n\t\t"
    class_decl = etree.SubElement(encoding_desc, "{http://www.tei-c.org/ns/1.0}classDecl")
    class_decl.text = "\n\t\t\t\t"
    class_decl.tail = "\n\t\t"
    taxonomy = etree.SubElement(class_decl, "{http://www.tei-c.org/ns/1.0}taxonomy")
    taxonomy.text = "\n\t\t\t\t\t"
    taxonomy.tail = "\n\t\t\t"
    
    for topic in topics:
        t = etree.SubElement(taxonomy, "{http://www.tei-c.org/ns/1.0}category", n=f"t{topic}")
        # If last one, one less indent
        if topic == topics[-1]:
            t.tail = "\n\t\t\t\t"
        else:
            t.tail = "\n\t\t\t\t\t"
    
    return encoding_desc

def insert_encoding_desc(tei_header, encoding_desc):
    """Insert <encodingDesc> before <revisionDesc>, or at the end if it doesn't exist."""
    revision_desc = tei_header.find("tei:revisionDesc", namespaces=NS)
    
    if revision_desc is not None:
        tei_header.insert(tei_header.index(revision_desc), encoding_desc)
    else:
        tei_header.append(encoding_desc)

# Parse and update each TEI file
for filename in os.listdir(input_folder):
    if not filename.endswith('.xml'):
        continue

    file_id = filename.replace('.xml', '')
    row = df[df['File ID'] == file_id]

    if row.empty:
        continue

    topics = row.iloc[0]['Topics']
    if not topics:
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(input_path, parser)
    root = tree.getroot()

    tei_header = root.find("tei:teiHeader", namespaces=NS)
    if tei_header is None:
        print(f"No <teiHeader> in {filename}")
        continue

    encoding_desc = create_encoding_desc(topics)
    insert_encoding_desc(tei_header, encoding_desc)

    # Write updated XML
    xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
    xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"✅ {filename} written")