import json
from docling.document_converter import DocumentConverter
from scientific_literature_assistant.config import PAPERS_DIR, JSON_DIR

def convert_pdf_to_json(pdf_path: str):
    json_path = JSON_DIR / f"{pdf_path.name}.json"
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    data = result.document.export_to_dict()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pdf_name = "Chang_Human.pdf"
    convert_pdf_to_json(PAPERS_DIR / pdf_name)
