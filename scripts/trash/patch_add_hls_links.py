# Add idno elements with subtype="hls" to the persons.xml file
# <person xml:id="P7941">
# 	...
# 	<idno subtype="gnd">https://d-nb.info/gnd/128679352</idno>
# 	<idno subtype="wiki">https://en.wikipedia.org/wiki/Nicolas_Colladon</idno>
#   <idno subtype="hls">https://hls-dhs-dss.ch/de/articles/016793/2003-09-01/</idno>
# </person>

from lxml import etree  # Import XML processing library

# Define namespace for TEI XML
ns = {
    None: 'http://www.tei-c.org/ns/1.0',
}

tab_separated_hls_links =  """
1770	https://hls-dhs-dss.ch/de/articles/016793/2003-09-01/
2043	https://hls-dhs-dss.ch/de/articles/016878/2008-08-25/
2844	https://hls-dhs-dss.ch/de/articles/017985/2017-09-20/
3196	https://hls-dhs-dss.ch/de/articles/017002/2006-05-12/
4862	https://hls-dhs-dss.ch/de/articles/044509/2005-04-21/
4942	https://hls-dhs-dss.ch/de/articles/023796/2006-12-11/
6140	https://hls-dhs-dss.ch/de/articles/015569/2009-10-15/
6337	https://hls-dhs-dss.ch/de/articles/015211/2010-11-29/
6338	https://hls-dhs-dss.ch/de/articles/022964/2012-01-05/
6459	https://hls-dhs-dss.ch/de/articles/046237/2011-08-19/
7276	https://hls-dhs-dss.ch/de/articles/020498/2002-05-06/
7537	https://hls-dhs-dss.ch/de/articles/019632/2007-11-29/
8012	https://hls-dhs-dss.ch/de/articles/016731/2007-11-27/
8071	https://hls-dhs-dss.ch/de/articles/025305/2012-11-22/
8199	https://hls-dhs-dss.ch/de/articles/018134/2005-11-21/
8339	https://hls-dhs-dss.ch/de/articles/018139/2002-10-29/
8433	https://hls-dhs-dss.ch/de/articles/029321/2012-01-06/
20380	https://hls-dhs-dss.ch/de/articles/014281/2002-06-14/
20433	https://hls-dhs-dss.ch/de/articles/018082/2007-08-22/
20520	https://hls-dhs-dss.ch/de/articles/025304/2011-11-03/
20616	https://hls-dhs-dss.ch/de/articles/017981/2005-10-17/
20780	https://hls-dhs-dss.ch/de/articles/021615/2009-06-17/
20859	https://hls-dhs-dss.ch/de/articles/014156/2008-01-16/
20910	https://hls-dhs-dss.ch/de/articles/018082/2007-08-22/
20971	https://hls-dhs-dss.ch/de/articles/021026/2001-12-27/
20975	https://hls-dhs-dss.ch/de/articles/016725/2006-01-03/
21015	https://hls-dhs-dss.ch/de/articles/012093/2009-10-27/
21016	https://hls-dhs-dss.ch/de/articles/017104/2008-08-19/
21017	https://hls-dhs-dss.ch/de/articles/017102/2008-05-06/
21194	https://hls-dhs-dss.ch/de/articles/017985/2017-09-20/
21320	https://hls-dhs-dss.ch/de/articles/025724/2004-08-27/"""

persons_path = "./data/index/persons.xml"
parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(persons_path, parser)
root = tree.getroot()

# Create a dictionary of HLS links
hls_links = {}
for line in tab_separated_hls_links.strip().split("\n"):
    key, value = line.split("\t")
    hls_links[key] = value

# Function to get the previous sibling of an element
def get_previous_sibling(element):
    """Returns the previous sibling of an element, or None if it has no previous sibling."""
    parent = element.getparent()
    if parent is None:
        return None  # No parent means no siblings

    children = list(parent)  # Get all children of the parent
    index = children.index(element)  # Find the index of the current element

    if index > 0:
        return children[index - 1]  # Return the previous sibling
    return None  # No previous sibling exists


# Iterate over all person elements in the XML file
for person in root.findall(".//person", ns):
    xml_id = person.get("{http://www.w3.org/XML/1998/namespace}id")
    # Ids in the persons.xml file have a "P" prefix, remove that
    xml_id = xml_id[1:]
    print(xml_id)
    if xml_id in hls_links:
        hls_link = hls_links[xml_id]
        # If the person already has an idno element with subtype="hls", replace the text
        idno = person.find(".//idno[@subtype='hls']", ns)
        if idno is not None:
            idno.text = hls_link
        else:
            # Otherwise, create a new idno element
            idno = etree.Element("idno", subtype="hls")
            idno.tail = "\n\t\t\t" # Add newline and indentation after the new idno element
            idno.text = hls_link
            person.append(idno)
            # Get previous sibling of the new idno element
            previous_sibling = get_previous_sibling(idno)
            if previous_sibling is not None:
                previous_sibling.tail = "\n\t\t\t\t" # Add newline and indentation before the new idno element
        # Remove from dictionary to keep track of processed elements
        del hls_links[xml_id]

# Log any remaining elements in the dictionary
if hls_links:
    print("Remaining elements:")
    for key, value in hls_links.items():
        print(key, value)

xml_str = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=False).decode("utf-8")
xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + xml_str # Add XML declaration in our format
with open(persons_path, "w", encoding="utf-8") as f:
    f.write(xml_str) # Save file

import re

with open(persons_path, "r", encoding="utf-8") as f:
    content = f.read()

# Restore space in self-closing tags
content = re.sub(r"(<\w+[^>]*)(/>)", r"\1 />", content)

with open(persons_path, "w", encoding="utf-8") as f:
    f.write(content)