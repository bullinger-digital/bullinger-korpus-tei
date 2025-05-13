import os
from lxml import etree

# Constants
SOURCE_ROOT = "./temp/letters_without_transcription_20250507"
TARGET_ROOT = "./data/letters"

NS_TEI = {"tei": "http://www.tei-c.org/ns/1.0"}
NS_PAGE = {"pc": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"}

def parse_page_xml(xml_path):
    tree = etree.parse(xml_path)
    page_el = tree.find(".//pc:Page", namespaces=NS_PAGE)
    image_w = page_el.get("imageWidth")
    image_h = page_el.get("imageHeight")

    lines = []
    for tl in page_el.findall(".//pc:TextLine", namespaces=NS_PAGE):
        unicode_el = tl.find("pc:TextEquiv/pc:Unicode", namespaces=NS_PAGE)
        coords_el = tl.find("pc:Coords", namespaces=NS_PAGE)
        baseline_el = tl.find("pc:Baseline", namespaces=NS_PAGE)

        lines.append({
            "text": unicode_el.text.strip() if unicode_el is not None and unicode_el.text else "",
            "points": coords_el.get("points") if coords_el is not None else "",
            "baseline": baseline_el.get("points") if baseline_el is not None else ""
        })
    return lines, image_w, image_h

def should_skip_letter(letter_id, root):
    source_attr = root.get("source")
    if source_attr is not None and source_attr.strip() != "keine":
        print(f"⚠️ Skipping {letter_id}: @source attribute is not 'keine'.")
        return True

    if root.find(".//tei:fileDesc/tei:sourceDesc/tei:bibl[@type='transcription']", namespaces=NS_TEI):
        print(f"⚠️ Skipping {letter_id}: <bibl type='transcription'> already present.")
        return True

    text_el = root.find(".//tei:text", namespaces=NS_TEI)
    if text_el is not None:
        if text_el.find(".//tei:lb", namespaces=NS_TEI) is not None or text_el.find(".//tei:s", namespaces=NS_TEI) is not None:
            print(f"⚠️ Skipping {letter_id}: <tei:text> contains <lb> or <s> elements.")
            return True

    return False

def update_graphic_dimensions(graphic_el, width, height):
    if graphic_el is not None:
        graphic_el.set("width", f"{width}px")
        graphic_el.set("height", f"{height}px")
        graphic_el.tail = "\n\t\t\t"

def create_zone_elements(surface_el, lines, surface_idx):
    for line_idx, line in enumerate(lines, start=1):
        zone_id = f"p{surface_idx + 1}z{line_idx}-0"
        is_last = (line_idx == len(lines))

        zone = etree.Element("{http://www.tei-c.org/ns/1.0}zone", nsmap=NS_TEI)
        zone.set("{http://www.w3.org/XML/1998/namespace}id", zone_id)
        zone.set("points", line["points"])
        zone.text = line["baseline"]
        zone.tail = "\n\t\t" if is_last else "\n\t\t\t"
        surface_el.append(zone)

def create_lb_elements(p_el, all_lines):
    p_el.clear()
    p_el.text = "\n\t\t\t\t\t"
    p_el.tail = "\n\t\t\t"  # Set tail of <p> element

    total_lines = sum(len(lines) for _, lines, _ in all_lines)
    line_counter = 0

    for surface_idx, lines, _ in all_lines:
        for line_idx, line in enumerate(lines, start=1):
            lb_id = f"p{surface_idx + 1}z{line_idx}"
            lb = etree.Element("{http://www.tei-c.org/ns/1.0}lb", nsmap=NS_TEI)
            lb.set("{http://www.w3.org/XML/1998/namespace}id", lb_id)

            line_counter += 1
            is_last = (line_counter == total_lines)
            lb.tail = line["text"] + ("\n\t\t\t\t" if is_last else "\n\t\t\t\t\t")

            p_el.append(lb)

def insert_transcription_bibl(root):
    source_desc_el = root.find(".//tei:fileDesc/tei:sourceDesc", namespaces=NS_TEI)
    if source_desc_el is not None:
        first_child = source_desc_el[0] if len(source_desc_el) > 0 else None
        preserved_tail = first_child.tail if first_child is not None else "\n\t\t\t\t"
        preserved_text = source_desc_el.text

        bibl_el = etree.Element("{http://www.tei-c.org/ns/1.0}bibl", nsmap=NS_TEI)
        bibl_el.set("type", "transcription")
        bibl_el.text = "Automatische Transkription"
        bibl_el.tail = preserved_tail

        source_desc_el.insert(0, bibl_el)
        source_desc_el.text = preserved_text

def update_tei(letter_id):
    letter_dir = os.path.join(SOURCE_ROOT, letter_id)
    tei_path = os.path.join(TARGET_ROOT, f"{letter_id}.xml")

    if not os.path.exists(letter_dir) or not os.path.exists(tei_path):
        print(f"Skipping {letter_id}: missing source or TEI file.")
        return

    tei_tree = etree.parse(tei_path)
    root = tei_tree.getroot()

    if should_skip_letter(letter_id, root):
        return

    root.set("source", "HTR")
    insert_transcription_bibl(root)

    surfaces = root.findall(".//tei:surface", namespaces=NS_TEI)
    p_el = root.find(".//tei:body/tei:div/tei:p", namespaces=NS_TEI)
    if p_el is None:
        print(f"No <p> element in TEI {letter_id}")
        return

    surface_filenames = sorted(f for f in os.listdir(letter_dir) if f.endswith(".xml"))
    all_lines = []

    for surface_idx, fname in enumerate(surface_filenames):
        page_path = os.path.join(letter_dir, fname)
        lines, width, height = parse_page_xml(page_path)
        all_lines.append((surface_idx, lines, fname))

    for surface_idx, lines, fname in all_lines:
        if surface_idx >= len(surfaces):
            print(f"Warning: not enough <surface> elements in {letter_id}. Skipping surface {surface_idx}")
            continue

        _, width, height = parse_page_xml(os.path.join(letter_dir, fname))
        surface_el = surfaces[surface_idx]

        update_graphic_dimensions(surface_el.find("tei:graphic", namespaces=NS_TEI), width, height)
        create_zone_elements(surface_el, lines, surface_idx)

    create_lb_elements(p_el, all_lines)

    with open(tei_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        tei_tree.write(f, encoding="utf-8", xml_declaration=False)

    print(f"✅ Updated TEI for letter {letter_id}")

def main():
    for letter_id in os.listdir(SOURCE_ROOT):
        if os.path.isdir(os.path.join(SOURCE_ROOT, letter_id)):
            update_tei(letter_id)

if __name__ == "__main__":
    main()