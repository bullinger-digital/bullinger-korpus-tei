from lxml import etree
import re

# Define TEI namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Load and parse XML
persons_path = "./data/index/persons.xml"
parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(persons_path, parser)
root = tree.getroot()

def replace_brackets(text):
    if not text:
        return text
    # Replace brackets with parentheses
    return re.sub(r'\[', '(', re.sub(r'\]', ')', text))

def merge_parentheses(text):
    # Find all parenthetical groups
    matches = re.findall(r'\(([^()]+)\)', text)
    if len(matches) > 1:
        base = re.sub(r'\s*\([^()]*\)', '', text).strip()
        merged = ', '.join(matches)
        return f"{base} ({merged})"
    return text

# Function to transform surname text
def transform_surname(text):
    if not text:
        return text
    text = replace_brackets(text)
    text = merge_parentheses(text)
    return text

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