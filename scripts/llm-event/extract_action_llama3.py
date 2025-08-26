import json
import requests
import os
import time
import re

# -----------------------------
# CONFIG
# -----------------------------
INPUT_PATH = "processed/processed_paragraphs_100.jsonl"
OUTPUT_PATH = "results/llm-event/llm_events_para100_v5.jsonl"

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3:8b"

# -----------------------------
# FUNCTIONS
# -----------------------------

def build_prompt(paragraph_text):
    """
    Generate the full prompt for one paragraph.
    """
    prompt_template = f"""You are an event extractor.

Given the following paragraph, extract all events and express each as a short, self-contained, grammatically complete sentence.

Rules:
- Each event must be written as a short, self-contained sentence.
- Each event must describe only a single action, mental state, perception, or natural phenomenon.
- Do NOT combine multiple events into a single sentence.
- Do NOT invent events that do not exist in the paragraph.
- The event sentence should reflect the meaning of the paragraph but does not need to be an exact substring.
- Keep the sentence concise but complete, including subject, verb, and object if applicable.
- Assign one of the following categories to each event:
    - action
    - mental
    - nature

IMPORTANT:
- Only extract events that represent actions, mental states, perceptions, or natural phenomena.
- Do NOT extract sentences that merely describe existence, possession, or abstract states without an action or change.
- Do NOT extract sentences that only use auxiliary or linking verbs like “be,” “have,” unless they clearly indicate an event of the above types.
- Do NOT skip any events that fit these criteria, even if they seem minor or abstract.
- Include events that describe mental impressions, feelings, observations, or perceptions (e.g. noticing, realizing, perceiving, feeling puzzled, imagining, deciding).
- For each verb describing a mental state, perception, or natural phenomenon, generate a short, independent sentence expressing it as an event.
- Each event sentence must be a grammatically complete sentence containing a subject and a main verb. Do NOT output only phrases or fragments.
- Your entire response MUST be only valid JSON and nothing else.
- Do not include any explanations.
- Only output JSON.

Return the result in this JSON format:
[
    ["event sentence", "category"],
    ...
]

If no events are found, return an empty list.

Paragraph:
{paragraph_text}
"""
    return prompt_template.strip()


def call_ollama(prompt):
    """
    Call the Ollama local API with a single prompt.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        response_json = response.json()
        return response_json["response"].strip()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def extract_json_from_response(response_text):
    """
    Attempt to extract JSON array from LLM output using regex.
    """
    match = re.search(r"\[[\s\S]*\]", response_text)
    if match:
        json_text = match.group(0)
        try:
            result = json.loads(json_text)
            return result
        except json.JSONDecodeError:
            print("[ERROR] JSON decoding failed in regex extraction.")
            return []
    else:
        return []


def process_paragraph(doc_id, para_id, text):
    """
    Process one paragraph and return the event list.
    """
    prompt = build_prompt(text)
    response_text = call_ollama(prompt)

    if response_text is None:
        # Return empty result on error
        return []

    # Try direct JSON parse first
    try:
        events = json.loads(response_text)
    except json.JSONDecodeError:
        print(f"[WARNING] Direct JSON parsing failed. Trying regex extraction for doc_id={doc_id}, para_id={para_id}")
        events = extract_json_from_response(response_text)

    # Additional check
    if not isinstance(events, list):
        events = []

    # Clean up event entries
    cleaned = []
    for item in events:
        if isinstance(item, list) and len(item) == 2:
            event_sentence = str(item[0]).strip()
            category = str(item[1]).strip()
            cleaned.append([event_sentence, category])

    return cleaned


def main():
    if not os.path.exists(os.path.dirname(OUTPUT_PATH)):
        os.makedirs(os.path.dirname(OUTPUT_PATH))

    with open(INPUT_PATH, "r", encoding="utf-8") as fin, \
         open(OUTPUT_PATH, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin):
            data = json.loads(line)
            doc_id = data.get("doc_id")
            para_id = data.get("para_id")
            text = data.get("text")

            print(f"Processing doc_id={doc_id}, para_id={para_id} ...")

            events = process_paragraph(doc_id, para_id, text)

            output_data = {
                "doc_id": doc_id,
                "para_id": para_id,
                "text": text,
                "events": events
            }

            fout.write(json.dumps(output_data, ensure_ascii=False) + "\n")

            # For testing only first 100 paragraphs
            if idx >= 99:
                break

            time.sleep(1)   # avoid flooding server

    print("Done processing!")


if __name__ == "__main__":
    main()