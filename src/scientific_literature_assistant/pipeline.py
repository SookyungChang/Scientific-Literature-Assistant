from scientific_literature_assistant.config import PAPERS_DIR
from scientific_literature_assistant.chunking import split_text_into_chunks
from scientific_literature_assistant.ingestion import extract_text_from_pdf
from scientific_literature_assistant.embeddings import create_embeddings

def process_document(pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[dict]:
    """
    Processes a PDF document by extracting text and splitting it into chunks.

    Args:
        pdf_path (str): The path to the PDF file.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between consecutive chunks.

    Returns:
        list[dict]: A list of dictionaries containing chunk IDs and their corresponding embeddings.
    """
    # Extract text from the PDF
    pages = extract_text_from_pdf(pdf_path)
    
    # Split the extracted text into chunks
    chunks = split_text_into_chunks(
        pages, 
        document_name=pdf_path.name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Create embeddings for the chunks
    chunks_with_embeddings = create_embeddings(chunks)
    
    return chunks_with_embeddings

if __name__ == "__main__":
    # Example usage
    pdf_path = PAPERS_DIR / "Chang_Human.pdf" # Replace with your PDF file path
    chunks_with_embeddings = process_document(pdf_path, chunk_size=1000, chunk_overlap=200)
    
    print(f"Created {len(chunks_with_embeddings)} chunks from the document.")
    print(len(chunks_with_embeddings[0]["embedding"]))  # Print the dimensionality of the first embedding for verification