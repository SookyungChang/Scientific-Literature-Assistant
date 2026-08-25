# app/ingestion.py # PDF -> text

import pymupdf
from scientific_literature_assistant.config import PAPERS_DIR
pymupdf.TOOLS.mupdf_display_errors(False)
import re

SECTION_PATTERN = re.compile(
    r"^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)\s*$"
)

APPENDIX_PATTERN = re.compile(
    r"^\s*Appendix\s+([A-Z])(?:\s*:\s*)?(.+?)\s*$"
)

def detect_sections(pages: list[dict]) -> list[dict]:
    sections = []
    appendices = []

    abstract_found = False
    reference_found = False
    current_number = None

    for page_number, page in enumerate(pages, start=1):
        page_number = page["page_number"]

        for line_number, line in enumerate(page["text"].splitlines()):
            line = line.strip()

            # IGNORE before ABSTRACT
            if line.upper() == "ABSTRACT":
                abstract_found = True
                continue

            if line.upper() == "REFERENCES":
                reference_found = True
                continue

            if abstract_found:       
                match = SECTION_PATTERN.match(line)

                if match:
                    section_number = match.group(1)
                    section_title = match.group(2)

                    if is_valid_section_number(section_number, current_number):
                        print(
                            f"Found section (page {page_number}, line {line_number}): {section_number} {section_title}"
                        )

                        current_section = {
                            "section_number": section_number,
                            "section_title": section_title,
                            "page_number": page_number,
                            "line_number": line_number,
                        }

                        sections.append(current_section)
                        current_number = section_number

            if reference_found:
                match = APPENDIX_PATTERN.match(line)
                if match:
                    appendix_number = match.group(1)
                    appendix_title = match.group(2)
                    print(f"Found section (page {page_number}, line {line_number}): Appendix {appendix_number} {appendix_title}")
                    current_section = {
                        "section_number": appendix_number,
                        "section_title": appendix_title,
                        "page_number": page_number,
                        "line_number": line_number,
                    }
                    appendices.append(current_section)
    all_sections = [{**section, "type": "section"} for section in sections] + [{**appendix, "type" : "appendix"} for appendix in appendices]
    all_sections.sort(key=lambda x: x["page_number"])
    return all_sections

def is_valid_section_number(
    new_number: str,
    previous_number: str | None
) -> bool:

    new_parts = [int(x) for x in new_number.split(".")]

    if previous_number is None:
        # first section must be 1.
        return new_parts == [1]

    previous_parts = [
        int(x) for x in previous_number.split(".")
    ]

    if len(new_parts) == len(previous_parts):
        
        return new_parts[:-1] == previous_parts[:-1] and new_parts[-1] == previous_parts[-1] + 1

    # subsection
    if len(new_parts) == len(previous_parts) + 1:
        return new_parts[:-1] == previous_parts and new_parts[-1] == 1

    if len(new_parts) == len(previous_parts) - 1:
        return new_parts[0] == previous_parts[0] + 1

    return False

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Args:
        pdf_path (str): The path to the PDF file.
    """
    # Open the PDF file
    pdf_document = pymupdf.open(pdf_path)
    
    # Initialize an empty list to hold the extracted text
    pages = []
    
    # Iterate through each page in the PDF
    for page_number, page in enumerate(pdf_document):

        # Extract text from the page
        pages.append({
            "page_number": page_number + 1,
            "text": page.get_text()
        })

    # Close the PDF document
    pdf_document.close()
    
    return pages

if __name__ == "__main__":
    # Example usage
    pdf_path = PAPERS_DIR / "humanVsMachine.pdf"
    pages = extract_text_from_pdf(pdf_path)
    all_sections = detect_sections(pages)


    # for section in sections:
    #     print(f"\n=====PAGE {sections["page_number"]}====")
    #     print(f"Found section: {section["section_number"]} {section["section_title"]}")
    # for page in pages:
    #     print(f"\n====PAGE {page['page_number']}===")
    #     lines = page['text'].splitlines()

    #     for line in lines:
    #         print(repr(line))

