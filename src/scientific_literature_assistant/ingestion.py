# app/ingestion.py # PDF -> text

import pymupdf
from scientific_literature_assistant.config import PAPERS_DIR

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
    pdf_path = PAPERS_DIR / "Chang_Human.pdf"
    pages = extract_text_from_pdf(pdf_path)
    for page in pages:
        print(f"Page {page['page_number']}: {page['text'][:100]}...")  # Print the first 100 characters of each page

