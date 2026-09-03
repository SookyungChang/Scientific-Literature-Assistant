# app/extraction.py # PDF -> text
import json
from pprint import pprint
from collections import defaultdict
from scientific_literature_assistant.config import JSON_DIR

def detect_blocks(data: list[dict], min_text_length: int = 5) -> list[dict]:

    condition = lambda item: (item["parent"]['$ref'] == '#/body' or item["parent"]['$ref'][:8] == '#/groups') and (not item["content_layer"] == 'furniture') and (not item["label"] == 'footnote') and len(item['text']) > min_text_length

    abstract_found = False
    appendix_found = False
    main_end_found = False
    results = []
    section_title = 'Abstract'
    section_number = 0

    for i, item in enumerate(data["texts"]):    
        if item["label"] == 'section_header' and item['text'].split()[0].upper().strip() == "ABSTRACT":
            abstract_found = True
            continue
        if not main_end_found and item["label"] == 'section_header' and not item['text'].strip()[0].isdigit() and section_number != 0:
            abstract_found = False
            main_end_found = True
            continue
        if abstract_found:
            if item["label"] == 'section_header':
                section_number, section_title = item['text'].split(". ", 1)
                print()
                print(f"Found section (page {item['prov'][0]['page_no']}): {section_number} {section_title}")

            elif condition(item):
                current_block = {
                                    "section_number": section_number,
                                    "section_title": section_title,
                                    "page_number": item['prov'][0]['page_no'],
                                    "text": item['text'],
                                    "type": "main",
                                }
                results.append(current_block)

        if item["label"] == 'section_header' and item['text'].split()[0].upper().strip() == "APPENDIX":
            appendix_found = True

        if appendix_found:
            if item["label"] == 'section_header':
                section_number, section_title = item['text'].split(": ", 1)
                print()
                print(f"Found section (page {item['prov'][0]['page_no']}): {section_number} {section_title}")

            elif condition(item):
                current_block = {
                                    "section_number": section_number,
                                    "section_title": section_title,
                                    "page_number": item['prov'][0]['page_no'],
                                    "text": item['text'],
                                    "type": "appendix",
                                }
                results.append(current_block)
        
        
    return results

def detect_captions(data: list[dict]) -> list[dict]:
    captions = []
    for item in data["texts"]:
        if item["label"] == 'caption':
            captions.append(item)
    return captions


def group_by_section(structured_data: list[dict]) -> list[dict]:
    grouped = defaultdict(lambda: {
        "page": [],
        "section_number": None,
        "section_title": None,
        "text": []
    })

    for item in structured_data:
        key = item["section_number"]

        grouped[key]["page"].append(item["page_number"])
        grouped[key]["section_number"] = item["section_number"]
        grouped[key]["section_title"] = item["section_title"]
        grouped[key]["text"].append(item["text"])


    result = []

    for item in grouped.values():
        item["page"] = sorted(set(item["page"]))
        item["text"] = " ".join(item["text"])
        result.append(item)


    return result

if __name__ == "__main__":
    data = json.load(open(JSON_DIR / "Chang_Human.json", encoding="utf-8"))
    results = detect_blocks(data)
    captions = detect_captions(data)
    results = group_by_section(results)
    pprint(results)
    # for result in results:
    #     print(f"Section {result['section_number']} ({result['section_title']}) - Page {result['page_number']}")
    #     print(result['text'])
    #     print()




    
    # for i, item in enumerate(data["texts"]):
    #     if item["parent"]['$ref']== "#/body":
    #         print(
    #                 i,
    #                 # "| self_ref:", item["self_ref"],
    #                 "| label:", item["label"],
    #                 "| layer:", item["content_layer"],
    #                 "| parent:", item["parent"]['$ref'],
    #                 # "| children:", item["children"],
    #                 # "| prov:", item["prov"],
    #                 # "| orig:", item["orig"],
    #                 "| text:", repr(item["text"][:80])
    #             )
