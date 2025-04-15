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

        # Find all correspContext elements
        for context in root.xpath("//tei:correspContext", namespaces=ns):
            children = list(context)

            for i, child in enumerate(children):
                if etree.QName(child).localname == "ref" and child.tag.startswith("{http://www.tei-c.org/ns/1.0}"):
                    ref_type = child.get("type", "")
                    if ref_type.startswith("next_") or ref_type.startswith("prev_"):
                        # Transfer tail to previous sibling or to parent text
                        if i > 0:
                            prev = children[i - 1]
                            if child.tail:
                                prev.tail = child.tail
                        else:
                            if child.tail:
                                context.text = child.tail

                        context.remove(child)
                        modified = True

            # If correspContext is now empty and has no meaningful text, make it self-closing
            if not list(context) and (context.text is None or context.text.strip() == ""):
                context.text = None
                modified = True

        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            print(f"✅ Cleaned correspContext refs in: {filename}")