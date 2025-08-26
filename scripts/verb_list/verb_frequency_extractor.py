import spacy
import json
from collections import Counter

INPUT_FILE = 'processed/processed_paragraphs.jsonl'
OUTPUT_FILE = 'verb_frequency_output.txt'

# ===== Load SpaCy =====
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# ===== Calculate =====
verb_counter = Counter()

total_paragraphs = 0

print("Processing corpus...")
with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
    for line in infile:
        total_paragraphs += 1
        record = json.loads(line.strip())
        text = record.get('text', '')
        doc = nlp(text)
        for token in doc:
            if token.pos_ == 'VERB':
                lemma = token.lemma_.lower()
                verb_counter[lemma] += 1

print(f"Total paragraphs processed: {total_paragraphs}")

# ===== Output =====
print(f"Writing verb frequency to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
    for verb, freq in verb_counter.most_common():
        outfile.write(f"{verb}\t{freq}\n")

print("Done!")