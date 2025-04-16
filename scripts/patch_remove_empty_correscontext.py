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

        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        modified = False

        # Locate tei:correspContext elements inside tei:teiHeader
        contexts = root.xpath("//tei:teiHeader//tei:correspContext", namespaces=ns)

        for context in contexts:
            # Remove only if empty (no children, no text)
            if not list(context) and (context.text is None or context.text.strip() == ""):
                parent = context.getparent()
                siblings = list(parent)
                index = siblings.index(context)

                # Transfer tail to previous sibling or parent text
                if context.tail:
                    if index > 0:
                        prev = siblings[index - 1]
                        prev.tail = context.tail
                    else:
                        parent.text = context.tail

                parent.remove(context)
                modified = True

        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            print(f"Cleaned: {filename}")