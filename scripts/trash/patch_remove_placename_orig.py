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

        # Find all tei:placeName elements inside tei:correspAction
        place_elems = root.xpath("//tei:correspAction//tei:placeName", namespaces=ns)

        for place in place_elems:
            for child in list(place):
                # Check if child is tei:orig
                if etree.QName(child).localname == "orig" and child.tag.startswith("{http://www.tei-c.org/ns/1.0}"):
                    # Check if the element has only whitespace
                    if not (child.text and child.text.strip()):
                        child.text = None
                    place.remove(child)
                    modified = True

        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            print(f"✅ Cleaned tei:orig in placeName: {filename}")