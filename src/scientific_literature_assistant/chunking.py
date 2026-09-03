# app/chunking.py # text -> chunks
import json
from pprint import pprint
from scientific_literature_assistant.config import JSON_DIR
from scientific_literature_assistant.structure import detect_blocks, detect_captions, group_by_section
from scientific_literature_assistant.config import (CHUNK_SIZE, CHUNK_OVERLAP)

def split_text_into_chunks(sections: list[dict], document_name: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """
    Splits the input text into chunks of specified size with optional overlap.

    Args:
        sections (list[dict]): A list of dictionaries containing section information and text.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between consecutive chunks.

    Returns:
        list[dict]: A list of text chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be a non-negative integer.")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size.")

    chunks = []
    chunk_id = 0

    for section in sections:
        text = section["text"]
        start = 0

        text_length = len(text)
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk = {
                "chunk_id": chunk_id,
                "document": document_name,
                "section_number": section["section_number"],
                "section_title": section["section_title"],
                "page_list": section["page"],
                "start_index": start,
                "end_index": end,
                "text": text[start:end]
            }
            chunks.append(chunk)
            chunk_id += 1
            start += (chunk_size - chunk_overlap)

    return chunks

if __name__ == "__main__":
    data = json.load(open(JSON_DIR / "Chang_Human.json", encoding="utf-8"))
    results = detect_blocks(data)
    captions = detect_captions(data)
    results = group_by_section(results)
    chunks = split_text_into_chunks(results, "Chang_Human.json")
    pprint(chunks)