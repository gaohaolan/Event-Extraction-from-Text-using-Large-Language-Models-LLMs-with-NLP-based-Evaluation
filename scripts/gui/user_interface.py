import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import re
import datetime

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3:8b"


extracted_events = []

def build_prompt(paragraph_text):
    prompt_template = f"""
You are an event extractor.

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
    match = re.search(r"\[[\s\S]*\]", response_text)
    if match:
        json_text = match.group(0)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            print("[ERROR] JSON decoding failed in regex extraction.")
            return []
    return []

def extract_events_from_text(text):
    prompt = build_prompt(text)
    response_text = call_ollama(prompt)

    if response_text is None:
        return []

    try:
        events = json.loads(response_text)
    except json.JSONDecodeError:
        events = extract_json_from_response(response_text)

    if not isinstance(events, list):
        events = []

    cleaned = []
    for item in events:
        if isinstance(item, list) and len(item) == 2:
            event_sentence = str(item[0]).strip()
            category = str(item[1]).strip()
            cleaned.append([event_sentence, category])
    return cleaned


def on_extract():
    global extracted_events
    user_text = text_input.get("1.0", tk.END).strip()
    if not user_text:
        messagebox.showwarning("Warning", "Please enter the text!")
        return

    output.delete("1.0", tk.END)
    output.insert(tk.END, "Analysing...\n")
    root.update()

    events = extract_events_from_text(user_text)
    extracted_events = events

    output.delete("1.0", tk.END)
    if not events:
        output.insert(tk.END, "No events were extracted.")
    else:
        for event in events:
            output.insert(tk.END, f"Event Phrase: {event[0]}\n")
            output.insert(tk.END, f"Category: {event[1]}\n")
            output.insert(tk.END, "-" * 50 + "\n")


def on_clear():
    text_input.delete("1.0", tk.END)
    output.delete("1.0", tk.END)


def on_export():
    if not extracted_events:
        messagebox.showinfo("Info", "No events to export.")
        return

    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{now}_EventResult.jsonl"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for event in extracted_events:
                json.dump({"event_phrase": event[0], "category": event[1]}, f, ensure_ascii=False)
                f.write("\n")
        messagebox.showinfo("Success", f"Exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {e}")

# ---------------------------
# GUI 
# ---------------------------

root = tk.Tk()
root.title("LLM Event Extraction")

tk.Label(root, text="Please enter the Lake District paragraph:").pack(anchor="w")
text_input = scrolledtext.ScrolledText(root, width=80, height=10)
text_input.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Extract", command=on_extract).pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Clear", command=on_clear).pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Export JSONL", command=on_export).pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Result:").pack(anchor="w")
output = scrolledtext.ScrolledText(root, width=80, height=15)
output.pack()

root.mainloop()