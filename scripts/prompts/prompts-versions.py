# version 1 (basic)
"""
You are an event extractor.
Given the following paragraph, extract all short event sentences.

Rules:
- Each event must be written as a short, self-contained sentence.
- Each event must describe only a single action, mental state, perception, or natural phenomenon.
- The event sentence should reflect the meaning of the paragraph but does not need to be an exact substring.
- Keep the sentence concise but complete, including subject, verb, and object if applicable.
- Assign one of the following categories to each event:
    - action
    - mental
    - nature

IMPORTANT:
- Your entire response MUST be only valid JSON and nothing else.
- Do not include any explanations.
- Do not include any concluding remarks.
- Only output JSON.

Return the result in this JSON format:
[
    ["event sentence", "category"], ...
]
If no events are found, return an empty list.

Paragraph:
{paragraph_text}
"""


# v2
"""
You are an event extractor.

Given the following paragraph, extract all short event sentences.

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
- Do NOT skip any events that fit these criteria, even if they seem minor or short.
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


# v3
"""You are an event extractor.

Given the following paragraph, extract all short event sentences.

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


# v4 （more rules, more complicated, but worse f1 score）
"""You are an event extractor.

Given the following paragraph, extract all short event sentences.

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
- Also include events that express decisions, intentions, or plans, even if the action was not completed.
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


# version 5  (the best)
"""You are an event extractor.

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

