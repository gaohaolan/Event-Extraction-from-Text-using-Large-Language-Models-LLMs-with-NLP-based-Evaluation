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
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            key = (d["doc_id"], d["para_id"])
            gold_dict.setdefault(key, []).append(d)
    return gold_dict

# ------------------------------
# ④ llm.jsonl
# ------------------------------
def load_llm(path):
    llm_dict = dict()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            key = (d["doc_id"], d["para_id"])
            llm_dict[key] = d["events"]
    return llm_dict

# ------------------------------
# ⑤ token overlap function
# ------------------------------
def is_match_llm_overlap(gold_phrase, llm_phrase, threshold=0.5):
    gold_norm = normalize(gold_phrase)
    llm_norm = normalize(llm_phrase)

    gold_tokens = set(gold_norm.split())
    llm_tokens = set(llm_norm.split())

    if not gold_tokens:
        return False

    overlap = gold_tokens & llm_tokens
    ratio = len(overlap) / len(gold_tokens)
    return ratio >= threshold

# ------------------------------
# ⑥ Evaluation
# ------------------------------
def evaluate_llm(gold_dict, llm_dict, unmatched_gold_path, unmatched_llm_path, overlap_threshold=0.5):
    total_gold = 0
    matched_gold = 0
    unmatched_gold_events = []

    total_llm = 0
    matched_llm = 0
    unmatched_llm_events = []

    # Recall
    for key in tqdm(gold_dict.keys(), desc="Evaluating LLM Recall"):
        gold_events = gold_dict[key]
        llm_events = llm_dict.get(key, [])

        for gold_event in gold_events:
            total_gold += 1
            matched = False
            for llm_event in llm_events:
                llm_phrase = llm_event[0]
                if is_match_llm_overlap(gold_event["event_phrase"], llm_phrase, threshold=overlap_threshold):
                    matched = True
                    break
            if matched:
                matched_gold += 1
            else:
                unmatched_gold_events.append(gold_event)

    recall = matched_gold / total_gold if total_gold > 0 else 0

    # Precision
    for key in tqdm(llm_dict.keys(), desc="Evaluating LLM Precision"):
        llm_events = llm_dict[key]
        gold_events = gold_dict.get(key, [])

        for llm_event in llm_events:
            llm_phrase = llm_event[0]
            total_llm += 1
            matched = False
            for gold_event in gold_events:
                if is_match_llm_overlap(gold_event["event_phrase"], llm_phrase, threshold=overlap_threshold):
                    matched = True
                    break
            if matched:
                matched_llm += 1
            else:
                unmatched_llm_events.append({
                    "doc_id": key[0],
                    "para_id": key[1],
                    "llm_phrase": llm_phrase,
                    "llm_category": llm_event[1]
                })

    precision = matched_llm / total_llm if total_llm > 0 else 0

    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0

    print(f"\n===== LLM Evaluation Results (Overlap ≥ {overlap_threshold}) =====")
    print(f"LLM Recall: {recall:.2%} ({matched_gold}/{total_gold})")
    print(f"LLM Precision: {precision:.2%} ({matched_llm}/{total_llm})")
    print(f"LLM F1-score: {f1:.2%}\n")

    # Save unmatched gold
    if unmatched_gold_events:
        os.makedirs(os.path.dirname(unmatched_gold_path), exist_ok=True)
        with open(unmatched_gold_path, "w", encoding="utf-8") as f:
            for d in unmatched_gold_events:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        print(f"Saved {len(unmatched_gold_events)} unmatched gold events to: {unmatched_gold_path}")
    else:
        print("All gold events matched!")

    # Save unmatched LLM
    if unmatched_llm_events:
        os.makedirs(os.path.dirname(unmatched_llm_path), exist_ok=True)
        with open(unmatched_llm_path, "w", encoding="utf-8") as f:
            for d in unmatched_llm_events:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        print(f"Saved {len(unmatched_llm_events)} unmatched LLM events to: {unmatched_llm_path}")
    else:
        print("All LLM events matched!")

# ------------------------------
# ⑦ main
# ------------------------------
if __name__ == "__main__":
    gold_path = "evaluation/gold_standard.jsonl"
    llm_path = "results/llm-event/llm_events_para100_v5.jsonl"
    unmatched_gold_out = "evaluation/unmatched/5-llm_unmatched_gold_events.jsonl"
    unmatched_llm_out = "evaluation/unmatched/5-llm_unmatched_llm_events.jsonl"

    gold_dict = load_gold(gold_path)
    llm_dict = load_llm(llm_path)

    evaluate_llm(
        gold_dict,
        llm_dict,
        unmatched_gold_out,
        unmatched_llm_out,
        overlap_threshold=0.5
    )