# ~/src/sla/rag/chroma_store.py

import chromadb
from sla.config import Config
config = Config()

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="scientific_papers",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)