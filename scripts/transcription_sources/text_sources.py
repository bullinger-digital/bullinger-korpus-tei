# This script generates a CSV file summarizing the transcription sources of letters in the Bullinger Digital corpus and indicates whether facsimiles are available. It extracts information from XML files in the `letters` folder and writes the results to a CSV file.
# Run it from the root folder with: `python ./scripts/transcription_sources/text_sources.py`

import os
import csv
from lxml import etree
from pathlib import Path

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

input_folder = './data/letters'
output_csv = os.path.join(Path(__file__).resolve().parent, './2025-05-28 transcription-sources.csv')

# List of bibliography entries in the HBBW series (extracted from data/index/bibliography.xml)
hbbw_sources = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'b23', 'b24', 'b720']

# Bibliography entry `Vorläufige Transkription der HBBW-EditorInnen`
provisional_transcription_source = 'b45'

headers = [
    'id',
    'has_facsimile',
    'edited',
    'provisional_transcription',
    'automatic_transcription',
    'type',
]

# Function to get the inner text length of the tei:text element
def get_text_length(root):
    text_elem = root.find('tei:text', namespaces=ns)
    if text_elem is not None:
        return len(''.join(text_elem.itertext()))
    return 0

rows = []

for filename in os.listdir(input_folder):
    if not filename.endswith('.xml'):
        continue

    input_path = os.path.join(input_folder, filename)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_path, parser)
    root = tree.getroot()

    # Transcription source is determined by the 'source' attribute of the bibl element with type="transcription"
    transcription_source = root.xpath('./tei:teiHeader//tei:sourceDesc/tei:bibl[@type="transcription"]/@source', namespaces=ns)
    transcription_source = str(transcription_source[0] if transcription_source else '')

    source = root.attrib.get('source', '')
    type_attr = root.attrib.get('type', '')

    row = {
        'id': os.path.splitext(filename)[0],
        'has_facsimile': bool(root.xpath('.//tei:facsimile//tei:graphic', namespaces=ns)),
        # The letter is considered 'edited' if it has a transcription source that is not empty and is not a provisional transcription
        'edited': len(transcription_source) > 0 and transcription_source != provisional_transcription_source,
        'provisional_transcription': transcription_source == provisional_transcription_source,
        'automatic_transcription': source == 'HTR',
        'type': type_attr,
    }

    rows.append(row)

# Sort rows by 'id'
rows = sorted(rows, key=lambda x: int(x['id']))

with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for row in rows:    
        writer.writerow(row)

print(f"Summary written to {output_csv}")