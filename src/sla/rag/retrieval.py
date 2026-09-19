# app/retrieval.py # "What is the most relevent chunk in my pdfs to this query?"

from sla.config import Config
config = Config()

from sla.rag.embeddings import create_query_embedding
    

def retrieve(query: str, collection, top_k: int = config.TOP_K) -> list[dict]:

    query_embedding = create_query_embedding(query)

    results = collection.query(query_embedding, n_results=top_k)

    return results