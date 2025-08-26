import json
import spacy
import re
from tqdm import tqdm
import os

# ------------------------------
# ① Load SpaCy
# ------------------------------
print("Loading SpaCy model...")
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# ------------------------------
# ② Normalization
# ------------------------------
DETERMINERS = {"the", "a", "an", "this", "that", "these", "those"}

def normalize(text, do_lemmatize=True):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)      
    text = re.sub(r'\s+', ' ', text).strip() 
    tokens = text.split()
    if tokens and tokens[0] in DETERMINERS:
        tokens = tokens[1:]
    new_text = " ".join(tokens)
    if do_lemmatize and new_text:
        doc = nlp(new_text)
        return " ".join([token.lemma_ for token in doc])
    return new_text

# ------------------------------
# ③ gold.jsonl
# ------------------------------
def load_gold(path):
    gold_dict = dict()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            key = (d["doc_id"], d["para_id"])
            gold_dict.setdefault(key, []).append(d)
    return gold_dict

# ------------------------------
# ④ spacy.jsonl
# ------------------------------
def load_spacy(path):
    spacy_dict = dict()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            key = (d["doc_id"], d["para_id"])
            spacy_dict[key] = d["events"]
    return spacy_dict

# ------------------------------
# ⑤ match
# ------------------------------
def is_match(gold_event, spacy_event):
    subj_gold = normalize(gold_event["subject"])
    subj_spacy = normalize(spacy_event["subject"])
    verb_gold = normalize(gold_event["verb"])
    verb_spacy = normalize(spacy_event["verb"])

    # subject match
    if subj_gold and not (subj_gold in subj_spacy or subj_spacy in subj_gold):
        return False
    # verb match
    if verb_gold and not (verb_gold in verb_spacy or verb_spacy in verb_gold):
        return False

    return True

# ------------------------------
# ⑥ evaluation
# ------------------------------
def evaluate(gold_dict, spacy_dict, unmatched_gold_path, unmatched_spacy_path):
    total_gold = 0
    matched_gold = 0
    unmatched_gold_events = []

    total_spacy = 0
    matched_spacy = 0
    unmatched_spacy_events = []

    # Recall
    for key in tqdm(gold_dict.keys(), desc="Evaluating Recall"):
        gold_events = gold_dict[key]
        spacy_events = spacy_dict.get(key, [])

        for gold_event in gold_events:
            total_gold += 1
            matched = False
            for spacy_event in spacy_events:
                if is_match(gold_event, spacy_event):
                    matched = True
                    break
            if matched:
                matched_gold += 1
            else:
                unmatched_gold_events.append(gold_event)

    recall = matched_gold / total_gold if total_gold > 0 else 0

    # Precision
    for key in tqdm(spacy_dict.keys(), desc="Evaluating Precision"):
        spacy_events = spacy_dict[key]
        gold_events = gold_dict.get(key, [])

        for spacy_event in spacy_events:
            total_spacy += 1
            matched = False
            for gold_event in gold_events:
                if is_match(gold_event, spacy_event):
                    matched = True
                    break
            if matched:
                matched_spacy += 1
            else:
                unmatched_spacy_events.append({
                    "doc_id": key[0],
                    "para_id": key[1],
                    "subject": spacy_event["subject"],
                    "verb": spacy_event["verb"],
                    "object": spacy_event["object"],
                    "verb_category": spacy_event["verb_category"]
                })

    precision = matched_spacy / total_spacy if total_spacy > 0 else 0

    # F1
    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0

    print(f"Recall: {recall:.2%} ({matched_gold}/{total_gold})")
    print(f"Precision: {precision:.2%} ({matched_spacy}/{total_spacy})")
    print(f"F1-score: {f1:.2%}")

    # Save unmatched gold
    if unmatched_gold_events:
        with open(unmatched_gold_path, "w", encoding="utf-8") as f:
            for d in unmatched_gold_events:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        print(f"Saved {len(unmatched_gold_events)} unmatched gold events to: {unmatched_gold_path}")
    else:
        print("All gold events matched!")

    # Save unmatched spacy
    if unmatched_spacy_events:
        with open(unmatched_spacy_path, "w", encoding="utf-8") as f:
            for d in unmatched_spacy_events:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        print(f"Saved {len(unmatched_spacy_events)} unmatched spaCy events to: {unmatched_spacy_path}")
    else:
        print("All spaCy events matched!")


# ------------------------------
# ⑦ main
# ------------------------------
if __name__ == "__main__":
    gold_path = "evaluation/gold_standard.jsonl"
    spacy_path = "results/spacy-result/spacy_svo_para100.jsonl"

    gold_dict = load_gold(gold_path)
    spacy_dict = load_spacy(spacy_path)

    evaluate(
    gold_dict,
    spacy_dict,
    unmatched_gold_path="evaluation/spacy_unmatched_gold_events.jsonl",
    unmatched_spacy_path="evaluation/spacy_unmatched_spacy_events.jsonl"
)
    
    