# app/embeddings.py # chunks -> vectors

import ollama
from scientific_literature_assistant.config import EMBEDDING_MODEL

def create_embeddings(chunks: list[dict]) -> list[dict]:

    """
    Creates embeddings for the given text chunks using the Ollama API.

    Args:
        chunks (list[dict]): A list of text chunks.
    Returns:
        list[dict]: A list of dictionaries containing chunk IDs and their corresponding embeddings.
    """
    texts = [chunk["text"] for chunk in chunks]

    response = ollama.embed(model=EMBEDDING_MODEL, input=texts)

    embeddings = response["embeddings"]

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks

def create_query_embedding(text: str) -> list[float]:
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=[text]
    )

    return response["embeddings"][0]