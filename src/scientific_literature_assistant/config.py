from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"
JSON_DIR = DATA_DIR / "json"

CHUNK_SIZE = 1000  # Number of characters per chunk
CHUNK_OVERLAP = 200  # Number of overlapping characters between chunks

EMBEDDING_MODEL = "nomic-embed-text:latest"  # Ollama model for creating embeddings
OLLAMA_MODEL = "mistral-small:latest"  


