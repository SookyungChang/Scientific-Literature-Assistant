# ~/src/sla/config.py
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
    DATA_DIR: Path = PROJECT_ROOT / "data"
    PAPERS_DIR: Path = DATA_DIR / "papers"
    JSON_DIR: Path = DATA_DIR / "json"
    DB_DIR: Path = DATA_DIR / "chroma_db"

    # Chunking
    CHUNK_SIZE: int = 1000  # Number of characters per chunk
    CHUNK_OVERLAP: int = 300  # Number of overlapping characters between chunks

    # Model names
    EMBEDDING_MODEL: str = "nomic-embed-text:latest"  # Ollama model for creating embeddings

    # ChromaDB
    COLLECTION_NAME: str = "literature"
    TOP_K: int = 10

config = Config()