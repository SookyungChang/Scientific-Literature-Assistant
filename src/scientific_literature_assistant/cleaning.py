# app/cleaning_fix.py # text -> cleaned text
import re
import json
import ollama
from scientific_literature_assistant.config import JSON_DIR
from scientific_literature_assistant.structure import detect_blocks, detect_captions, group_by_section
from scientific_literature_assistant.artifact_detector import detect_candidates

def correct_candidate(candidate, context):
    prompt = f"""
You are a conservative scientific PDF text extraction error detector.

Your task is NOT to rewrite or improve the text.
Your ONLY task is to determine whether the candidate contains
an OCR/PDF extraction artifact.

IMPORTANT RULES:

1. Preserve the original text unless there is strong evidence
   that the candidate was corrupted during PDF extraction.

2. Do NOT correct spelling, grammar, author names, scientific
   terminology, acronyms, or proper nouns.

3. Never invent information that is not explicitly supported
   by the surrounding context.

4. If the candidate is a valid scientific term, name, acronym,
   or notation, return is_artifact=false.

5. If you are uncertain, return is_artifact=false.

6. The replacement must be derived ONLY from the provided context.
   Do not infer a different word or name from your general knowledge.

7. Do not modify text outside the candidate.

Candidate:
{candidate["text"]}

Candidate type:
{candidate["type"]}

Context:
{context}

Return ONLY valid JSON:

{{
    "is_artifact": true or false,
    "replacement": "replacement text or original candidate",
    "confidence": 0.0
}}
"""

    response = ollama.chat(
        model="mistral-small:latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
    )

    return json.loads(response["message"]["content"])

def get_context(text, start, end, window=150):
    context_start = max(0, start - window)
    context_end = min(len(text), end + window)

    return text[context_start:context_end]


def fix_decimal_spacing(text):
    return re.sub(
        r"(\d)\s+\.\s+(\d)",
        r"\1.\2",
        text
    )

if __name__ == "__main__":
    data = json.load(open(JSON_DIR / "Chang_Human.json", encoding="utf-8"))
    results = detect_blocks(data)
    captions = detect_captions(data)
    results = group_by_section(results)
    for result in results:
        candidates = detect_candidates(result['text'])
        for candidate in candidates:
            if candidate['type'] == 'decimal_spacing':
                corrected_text = fix_decimal_spacing(candidate['text'])
                print({
                    "is_artifact": True,
                    "original": candidate['text'],
                    "replacement": corrected_text,
                    "confidence": 1.0
                })
            else:
                context = get_context(result['text'], candidate['start'], candidate['end'])
                print(f"Context: {context}")
                corrected = correct_candidate(candidate, context)
                print(corrected)
                print()
