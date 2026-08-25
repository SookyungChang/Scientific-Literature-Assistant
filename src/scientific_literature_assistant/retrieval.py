# app/retrieval.py # "What is the most relevent chunk in my pdfs to this query?"

import numpy as np

from scientific_literature_assistant.embeddings import (
    create_query_embedding
)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def retrieve(query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:

    query_embedding = create_query_embedding(query)

    results = []

    for chunk in chunks:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            **chunk,
            "similarity": score
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]