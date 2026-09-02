import json
from docling.document_converter import DocumentConverter
from scientific_literature_assistant.config import PAPERS_DIR, JSON_DIR

converter = DocumentConverter()
pdf_path = PAPERS_DIR / "Chang_Human.pdf"
result = converter.convert(pdf_path)
data = result.document.export_to_dict()

with open(JSON_DIR/ "Chang_Human.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)