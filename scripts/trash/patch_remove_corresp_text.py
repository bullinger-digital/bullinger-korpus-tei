from lxml import etree
import os

# Define TEI namespace
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

        modified = False

        # Find all persName and orgName inside correspAction
        to_clean = root.xpath("//tei:correspAction//tei:persName | //tei:correspAction//tei:orgName", namespaces=ns)

        for elem in to_clean:
            had_content = (
                elem.text and elem.text.strip() or
                len(elem) > 0  # has child elements
            )

            if had_content:
                for child in list(elem):
                    elem.remove(child)
                elem.text = None
                # elem.tail = None
                modified = True

        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            print(f"✅ Cleaned and saved: {filename}")