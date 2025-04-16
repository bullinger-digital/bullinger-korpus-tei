import os
from lxml import etree
import urllib.parse

# TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Input folder containing TEI XML files
input_folder = "./data/letters"

for filename in os.listdir(input_folder):
    if not filename.endswith(".xml"):
        continue

    filepath = os.path.join(input_folder, filename)
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(filepath, parser)
    root = tree.getroot()
    
    modified = False

    graphics = root.xpath("//tei:facsimile//tei:graphic", namespaces=ns)
    for graphic in graphics:
        descs = graphic.xpath(".//tei:desc[@subtype='path']", namespaces=ns)
        for desc in descs:
            path_text = desc.text.strip() if desc.text else None
            if path_text:
                encoded_path = urllib.parse.quote(path_text.replace('/', '!')).replace('%21', '!')
                full_url = f"https://media.sources-online.org/cantaloupe/iiif/3/bullinger!{encoded_path}/full/max/0/default.jpg"
                graphic.set("url", full_url)
                modified = True

    if modified:
        xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
        xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"✅ Updated graphic URLs in {filename}")