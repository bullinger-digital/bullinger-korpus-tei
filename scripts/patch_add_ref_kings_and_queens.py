from lxml import etree  # Import XML processing library
import os  # Import OS module to handle file system operations
import re  # Import regular expressions for text matching
import pandas as pd  # Import Pandas for handling Excel data
import sys  # Import system module to handle command-line arguments

# Define the folder containing input XML files
input_folder = "./data/letters"

# Retrieve the Excel file and output folder from command-line arguments
excel_file = sys.argv[1] if len(sys.argv) > 1 else './scripts/src/leaders_modified_ele.xlsx'  # Excel file containing monarch data
output_folder = sys.argv[2] if len(sys.argv) > 2 else input_folder  # Folder where modified XML files will be saved

# Load the Excel file and read all sheets into a dictionary
data = pd.read_excel(excel_file, sheet_name=None)

# Extract relevant monarch data from each sheet and store it in a dictionary
monarchs_data = {}
for sheet_name, df in data.items():
    if {'Country', 'Start_Date', 'End_Date', 'ID_ref'}.issubset(df.columns):  # Ensure required columns exist
        monarchs_data[sheet_name] = df.to_dict(orient='records')  # Convert DataFrame to dictionary
    else:
        print(f"Skipping sheet {sheet_name}: Required columns not found")

# Define namespace for TEI XML
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Define regex pattern to match words related to "rex" and "regina"
# Manually added "regen", yes with "n", because there is 1 case in corpus where it shows up: letter 5435.xml
pattern = re.compile(r'\b(rex|regis|regi|regem|rege|reges|regum|regibus|regen|regina|reginae|reginam|reginarum|reginis|reginas)\b', re.IGNORECASE)

# Country mapping using first three letters of adjacent words
country_mapping = {
    "pol": "Poland", "gal": "France", "fra": "France", "his": "Spain",
    "dan": "Denmark", "bel": "Belgium", "nav": "Navarra", "ang": "England",
    "boh": "Bohemia", "ung": "Hungary", "nar": "Navarra", "hun": "Hungary",
    "sco": "Scotland", "por": "Portugal"
}

def get_adjacent_tokens(text, match):
    """ Extracts the previous and next words surrounding 'rex', 'regina', etc. """
    before_match = text[:match.start()].strip().split()  # Get words before match
    after_match = text[match.end():].strip().split()  # Get words after match
    prev_token = before_match[-1] if before_match else None  # Last word before match
    next_token = after_match[0] if after_match else None  # First word after match
    return prev_token, next_token

total_case_count = 0  # Counter for total identified cases

# Process all XML files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):  # Ensure the file is an XML file
        input_path = os.path.join(input_folder, filename)  # Full path to input file
        output_path = os.path.join(output_folder, filename)  # Full path to output file

        #print(f"Processing: {filename}")

        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        pers_names = root.findall(".//tei:persName", ns)  # Find all person names in the XML
        corresp_desc = root.find(".//tei:correspDesc", ns)  # Find correspondence description element
        letter_year = None  # Initialize letter year variable
        modified = False  # Track if XML file is modified
        case_count = 0  # Counter for changes made in this file

        # Extract the letter year from the XML metadata
        if corresp_desc is not None:
            when_attr = corresp_desc.get("when")  # Get 'when' attribute
            if when_attr:
                year_match = re.search(r'\b(\d{4})\b', when_attr)  # Find 4-digit year
                if year_match:
                    letter_year = int(year_match.group(1))  # Convert year to integer
            else:
                date_element = corresp_desc.find(".//tei:date", ns)  # Find nested date element
                if date_element is not None and date_element.get("when"):
                    year_match = re.search(r'\b(\d{4})\b', date_element.get("when"))
                    if year_match:
                        letter_year = int(year_match.group(1))

        # If a valid letter year is found, process monarch references
        if letter_year:
            for sheet, records in monarchs_data.items():
                for record in records:
                    try:
                        start_year = int(str(record['Start_Date'])[:4])  # Extract start year
                        end_year = int(str(record['End_Date'])[:4])  # Extract end year
                        country = str(record['Country']).strip().lower()  # Normalize country name
                        matching_ref = str(record['ID_ref']).strip() if pd.notna(record['ID_ref']) else None  # Get reference ID

                        for pers in pers_names:
                            if 'ref' not in pers.attrib and pers.text:  # If 'ref' attribute is missing
                                match = pattern.search(pers.text)  # Search for regex pattern
                                if match:
                                    prev_token, next_token = get_adjacent_tokens(pers.text, match)  # Get surrounding words
                                    prev_prefix = prev_token[:3].lower() if prev_token else None  # First 3 letters of previous word
                                    next_prefix = next_token[:3].lower() if next_token else None  # First 3 letters of next word
                                    
                                    mapped_country = country_mapping.get(prev_prefix) or country_mapping.get(next_prefix)  # Identify country
                                    
                                    # Check if the identified country and timeline match
                                    if mapped_country and mapped_country.lower() == country and start_year <= letter_year <= end_year:
                                        pers.set('ref', matching_ref)  # Assign reference ID
                                        pers.set('type', 'auto_name')
                                        modified = True  # Mark file as modified
                                        case_count += 1  # Increment file case count
                                        total_case_count += 1  # Increment global case count
                                        print(f"Marked document: {filename}, assigned ref={matching_ref} to {etree.tostring(pers, encoding='unicode')}")
                    except (ValueError, TypeError):
                        continue  # Skip invalid records

        # Save modified XML file if changes were made
        if modified:
            xml_str = etree.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")
            xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_str # Add XML declaration in our format
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str) # Save file
                
            print(f"✅ Saved modified file: {output_path} (Cases found: {case_count})\n")
        #else:
            #print(f"❌ No changes made to {filename}, skipping save.\n")

# Print total cases found across all files
print(f"🔎 Total cases found across all files: {total_case_count}")
