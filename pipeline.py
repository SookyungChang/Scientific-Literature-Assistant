# ~/pipeline.py
import json
from sla.ingestion.structure import detect_blocks, group_by_section
from sla.rag.chunking import split_text_into_chunks
from sla.rag.embeddings import create_embeddings
from sla.rag.retrieval import retrieve
from sla.config import Config
config = Config()

def process_document(chunk_size: int = config.CHUNK_SIZE, chunk_overlap: int = config.CHUNK_OVERLAP) -> list[dict]:
    """
    Processes a PDF document by extracting text and splitting it into chunks.

    Args:
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between consecutive chunks.

    Returns:
        list[dict]: A list of dictionaries containing chunk IDs and their corresponding embeddings.
    """

    chunks = []
    
    for file in config.JSON_DIR.glob("*.json"):
        data = json.load(open(config.JSON_DIR / file.name, encoding="utf-8"))
        results = detect_blocks(data)
        # captions = detect_captions(data)
        results = group_by_section(results)

        # Split the extracted text into chunks
        file_chunks = split_text_into_chunks(
            results, 
            document_name=file.name.split('.')[0],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks.extend(file_chunks)


    # Create embeddings for the chunks
    chunks_with_embeddings = create_embeddings(chunks)

    return chunks_with_embeddings

def retrieve_information(query: str, top_k: int = 5) -> list[dict]:
    chunks_with_embeddings = process_document()
    results = retrieve(query, chunks_with_embeddings, top_k=top_k)

    print("\n===== Retrieval Results =====")
    
    print("query:", query)

    for i, result in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print(f"Document: {result['document']}")
        print(f"Chunk {result['chunk_id']}", f"| Page {result['page_list']} | Section {result['section_number']} - {result['section_title']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Text: {result['text']}")

if __name__ == "__main__":
    query = """
    where is the information about the hydrodynamic simulation box and the cosmological parameters?
    """
    retrieve_information(query, top_k=5)

    