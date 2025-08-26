import json
from collections import Counter

category_counter = Counter()

with open('evaluation/gold_standard.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        category = data.get("category")
        if category:
            category_counter[category] += 1


for cat, count in category_counter.items():
    print(f"{cat}: {count}")