from lxml import etree
import re

# Define TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Load and parse XML
persons_path = "./data/index/persons.xml"
parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(persons_path, parser)
root = tree.getroot()

# Function to transform surname text
def transform_surname(text):
    if not text:
        return text
    
    # If text does not contain a comma, return with brackets replaced
    if "," not in text:
        return text
    
    # If text ends with or starts with d.Ä. or d.J., return with brackets replaced
    if text.endswith("d.Ä.") or text.endswith("d.J."):
        return text

    started_with_bracket = text.startswith("[") or text.startswith("(")

    # 1. Split on comma, semicolon, brackets
    parts = re.split(r'[,\[\]\(\);]', text)

    # 2. Trim whitespace and remove empties
    parts = [p.strip() for p in parts if p.strip()]

    # 3. Build final string
    if not parts:
        return ""

    # if started_with_bracket is true, there is no main part
    # and we need to add the brackets

    if started_with_bracket:
            extras = ", ".join(parts)
            return f"({extras})"
    else:
        if len(parts) == 1:
            return parts[0]
        else:
            main = parts[0]
            extras = ", ".join(parts[1:])
            return f"{main} ({extras})"

# Traverse person elements and modify surnames
for person in root.findall(".//tei:person", ns):
    pers_name = person.find("tei:persName[@type='main']", ns)
    if pers_name is not None:
        surname = pers_name.find("tei:surname", ns)
        if surname is not None and surname.text:
            original = surname.text
            updated = transform_surname(original)
            if original != updated:
                print(f"Updating surname: '{original}' -> '{updated}'")
                surname.text = updated

# Write changes back to file
xml_str = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=False).decode("utf-8")
xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + xml_str
with open(persons_path, "w", encoding="utf-8") as f:
    f.write(xml_str)