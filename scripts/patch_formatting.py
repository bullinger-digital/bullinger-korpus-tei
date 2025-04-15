# Save all letter XML files using etree to ensure UTF-8 characters are correctly encoded
from lxml import etree
import os

# Define namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

input_folder = "./data/letters"
output_folder = input_folder

for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        parser = etree.XMLParser(remove_blank_text=False)  # Preserve original formatting
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
        xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"✅ Formatted and saved: {filename}")