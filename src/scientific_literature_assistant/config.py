from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"

CHUNK_SIZE = 1000  # Number of characters per chunk
CHUNK_OVERLAP = 200  # Number of overlapping characters between chunks

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # OpenAI embedding model
OLLAMA_MODEL = "mistral"  # Ollama model for question answering

