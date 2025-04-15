import pandas as pd
from lxml import etree
import os

# Define TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Paths
excel_path = './scripts/src/2025-04-14 export-addresses.xlsx'
input_folder = './data/letters'
output_folder = input_folder

# Read the Excel file and ensure ID is treated as a string
df = pd.read_excel(excel_path, dtype={'id': str})
df['id'] = df['id'].str.strip()

# Helper function to insert element with correct indentation before it
def append_with_indent(parent, new_elem, indent_level="\t\t\t\t"):
    children = list(parent)
    new_elem.tail = "\n" + indent_level
    if children:
        last = children[-1]
        if last.tail is None or last.tail.strip() == "":
            last.tail = "\n" + indent_level + "\t"
    else:
        parent.text = "\n" + indent_level + "\t"
    parent.append(new_elem)

# Iterate over XML files
for filename in os.listdir(input_folder):
    if not filename.endswith(".xml"):
        continue

    file_id = filename.replace('.xml', '')
    row = df[df['id'] == file_id]

    if row.empty:
        continue

    sender_title = row.iloc[0].get('new_senders_text')
    receiver_title = row.iloc[0].get('new_receivers_text')

    if pd.isna(sender_title) and pd.isna(receiver_title):
        continue  # Skip if no new sender or receiver text

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(input_path, parser)
    root = tree.getroot()
    modified = False

    # Add <rs type="title"> inside <correspAction type="sent">
    if pd.notna(sender_title):
        sent = root.find(".//tei:correspAction[@type='sent']", namespaces=ns)
        if sent is not None:
            rs_elem = etree.Element("{http://www.tei-c.org/ns/1.0}rs", type="title")
            rs_elem.text = str(sender_title)
            append_with_indent(sent, rs_elem)
            modified = True

    # Add <rs type="title"> inside <correspAction type="received">
    if pd.notna(receiver_title):
        received = root.find(".//tei:correspAction[@type='received']", namespaces=ns)
        if received is not None:
            rs_elem = etree.Element("{http://www.tei-c.org/ns/1.0}rs", type="title")
            rs_elem.text = str(receiver_title)
            append_with_indent(received, rs_elem)
            modified = True

    if modified:
        xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
        xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"✅ Updated and saved: {filename}")