import os
import xml.etree.ElementTree as ET
import re
import json

def extract_paragraphs_from_xml(file_path, doc_id=None):
    tree = ET.parse(file_path)
    root = tree.getroot()

    root_tag = root.tag
    ns_match = re.match(r"\{.*\}", root_tag)
    namespace = ns_match.group(0) if ns_match else ""

    paragraphs = []
    para_id = 0

    for elem in root.iter():
        tag = elem.tag.replace(namespace, "")
        if tag in ["p"]:  
            text = ET.tostring(elem, encoding="unicode", method="text").strip()
            if text and len(text) > 50:
                clean_text = re.sub(r'\s+', ' ', text)
                paragraphs.append({
                    "doc_id": doc_id if doc_id else os.path.basename(file_path).replace(".xml", ""),
                    "para_id": para_id,
                    "text": clean_text
                })
                para_id += 1

    return paragraphs

def process_folder(folder_path, output_path="processed_paragraphs.jsonl"):
    all_paragraphs = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            doc_id = filename.replace(".xml", "")
            print(f"Processing {filename} ...")
            paras = extract_paragraphs_from_xml(file_path, doc_id)
            all_paragraphs.extend(paras)

    with open(output_path, "w", encoding="utf-8") as f:
        for item in all_paragraphs:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Done! Extracted {len(all_paragraphs)} paragraphs to {output_path}")

if __name__ == "__main__":
    process_folder("data/LakeDistrictCorpus-master/LD80_transcribed", output_path="processed/processed_paragraphs.jsonl")
