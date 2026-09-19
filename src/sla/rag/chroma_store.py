# ~/src/sla/rag/chroma_store.py

import chromadb
from sla.config import Config
config = Config()

def get_collection():
    client = chromadb.PersistentClient(
    path=config.DB_DIR
    )
    collection = client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            configuration={
                "hnsw": {
                    "space": "cosine"
                }
            }
        )
    return collection

def collection_info(collection):
    print("Number of chunks:", collection.count())

    papers = collection.get(
        include=["metadatas"]
    )

    documents = set(
        metadata["document"]
        for metadata in papers["metadatas"]
    )

    print("Documents in DB:")
    for document in documents:
        print("-", document)