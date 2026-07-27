# app/ingestion.py

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
    
    # Initialize an empty string to hold the extracted text
    extracted_text = ""
    
    # Iterate through each page in the PDF
    for page in pdf_document:

        # Extract text from the page
        extracted_text += page.get_text() + "\n"
    
    # Close the PDF document
    pdf_document.close()
    
    return extracted_text

if __name__ == "__main__":
    # Example usage
    pdf_path = PAPERS_DIR / "2508.03264v1.pdf"  # Replace with your PDF file path
    text = extract_text_from_pdf(pdf_path)
    print(text[:1000])