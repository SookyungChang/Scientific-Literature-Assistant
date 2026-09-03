import json
from pathlib import Path
from docling.document_converter import DocumentConverter
from scientific_literature_assistant.config import PAPERS_DIR, JSON_DIR

converter = DocumentConverter()

def convert_pdf_to_json():
    for file in PAPERS_DIR.glob("*.pdf"):
            json_name = f"{file.name.split('.')[0]}.json"
            if json_name not in [f.name for f in JSON_DIR.iterdir()]:
                json_path = JSON_DIR / json_name
                pdf_path = PAPERS_DIR / file.name
                result = converter.convert(pdf_path)
                data = result.document.export_to_dict()
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"\n##### Converted {file.name} to {json_name} and saved to {json_path}.\n")
            else:
                print(f"\n##### JSON file for {file.name} already exists. Skipping conversion.\n")
                continue
    

if __name__ == "__main__":
    convert_pdf_to_json()

