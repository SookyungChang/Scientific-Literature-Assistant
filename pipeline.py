# ~/pipeline.py
import json
from sla.ingestion.structure import detect_blocks, group_by_section
from sla.rag.chunking import split_text_into_chunks
from sla.rag.embeddings import create_embeddings, create_query_embedding
from sla.rag.chroma_store import get_collection
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

    # Chunking
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
    print("Total chunks:", len(chunks_with_embeddings))
    print(
        "Documents:",
        set(chunk["document"] for chunk in chunks_with_embeddings)
    )
    collection = get_collection()

    for chunk in chunks_with_embeddings:
        collection.add(
            ids=[chunk["chunk_id"]],
            embeddings=[chunk["embedding"]],
            documents=[chunk["text"]],
            metadatas=[{
                "document": chunk["document"],
                "page_list": str(chunk["page_list"]),
                "section_number": chunk["section_number"],
                "section_title": chunk["section_title"],
            }]
        )

    print(f"DB file is saved in {config.DB_DIR}.")

    return collection


def retrieve_information(query: str) -> list[dict]:

    collection = get_collection()
    results = retrieve(query, collection, config.TOP_K)

    print("\n===== Retrieval Results =====")
    
    print("query:", query)

    print("\n" + "=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (chunk_id, text, metadata, distance) in enumerate(
        zip(ids, documents, metadatas, distances),
        start=1
    ):
        print(f"\n--- Result {i} ---")
        print(f"Document : {metadata['document']}")
        print(
            f"Chunk    : {chunk_id} | "
            f"Page     : {metadata['page_list']} | "
            f"Section  : {metadata['section_number']} - "
            f"{metadata['section_title']}"
        )
        print(f"Distance : {distance:.4f}")
        print(f"Text     : {text}")
            

if __name__ == "__main__":
    query = """
    where is the information about the hydrodynamic simulation box and the cosmological parameters?
    """
    retrieve_information(query)

    