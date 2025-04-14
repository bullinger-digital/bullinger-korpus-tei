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

        modified = False

        # Find all tei:roleName elements inside correspAction
        role_names = root.xpath("//tei:correspAction//tei:roleName", namespaces=ns)

        for role in role_names:
            parent = role.getparent()
            parent.remove(role)
            modified = True

            # If parent is tei:persName and also contains a placeName, remove that too
            if parent.tag == f"{{{ns['tei']}}}persName":
                place_names = parent.findall("tei:placeName", namespaces=ns)
                for place in place_names:
                    parent.remove(place)

                # If persName is now empty, remove leftover text
                is_empty = (
                    (parent.text is None or parent.text.strip() == '') and
                    len(parent) == 0 and
                    all((child.tail is None or child.tail.strip() == '') for child in parent)
                )
                if is_empty:
                    parent.text = None

        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            print(f"✅ Modified and saved: {filename}")