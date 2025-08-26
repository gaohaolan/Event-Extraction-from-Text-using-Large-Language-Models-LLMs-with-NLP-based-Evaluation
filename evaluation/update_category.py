import json

file_in = "evaluation/gold_standard.jsonl"
file_out = "evaluation/gold_standardsssss.jsonl"

with open(file_in, "r", encoding="utf-8") as fin, \
     open(file_out, "w", encoding="utf-8") as fout:
    
    for line in fin:
        
        if not line.strip():
            continue
        
        
        obj = json.loads(line)
        
        
        if obj.get("category") == "perception":
            obj["category"] = "mental"
        
        
        fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("Done！New file:", file_out)