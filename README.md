# Scientific Literature Assistant

A lightweight retrieval-augmented generation (RAG) project for searching and querying scientific literature stored as structured JSON extracted from PDFs. The system ingests paper content, splits it into semantically meaningful sections, embeds each chunk with Ollama, stores the vectors in ChromaDB, and retrieves the most relevant passages for a natural-language query.

This repository is designed for research workflows where you want to ask targeted questions across multiple scientific papers without manually reading each document.

## Overview

The project follows a simple RAG pipeline:

- Extract structured text from scientific paper data
- Detect and group main sections of the document
- Split large sections into overlapping chunks
- Generate embeddings using Ollama
- Store embeddings in a persistent ChromaDB collection
- Retrieve relevant chunks for a user query

In short:

```text
PDF/JSON source data
        ↓
section detection + grouping
        ↓
chunking
        ↓
embedding generation (Ollama)
        ↓
ChromaDB vector storage
        ↓
query-time retrieval
```

## Features

- Section-aware literature parsing from document JSON structures
- Chunking with overlap for preserving contextual continuity
- Vector embedding generation via Ollama
- Persistent vector database using ChromaDB
- Query retrieval based on cosine similarity
- Metadata-rich stored chunks, including document name, page list, and section title
- Config-driven behavior to adjust chunk size, overlap, model selection, and retrieval depth

## Project structure

```text
Scientific-Literature-Assistant/
├── pipeline.py                     # main runtime script for indexing and retrieval
├── pyproject.toml                 # package metadata and dependencies
├── README.md                      # project documentation
├── data/
│   ├── json/                     # input paper JSON files
│   ├── papers/                   # raw PDFs (if used locally)
│   └── chroma_db/                # persistent ChromaDB storage
├── src/
│   └── sla/
│       ├── __init__.py
│       ├── config.py             # global settings
│       ├── ingestion/
│       │   ├── artifact_detector.py
│       │   ├── cleaning.py
│       │   ├── structure.py
│       │   └── extraction.py
│       └── rag/
│           ├── chroma_store.py
│           ├── chunking.py
│           ├── embeddings.py
│           └── retrieval.py
└── uv.lock
```

## Core pipeline

### 1. Configuration

The central settings live in `src/sla/config.py`.

Key defaults include:

- data directory: `data/`
- JSON input directory: `data/json/`
- vector database directory: `data/chroma_db/`
- chunk size: `1000` characters
- chunk overlap: `300` characters
- embedding model: `nomic-embed-text:latest`
- ChromaDB collection: `literature`
- retrieval depth: `TOP_K = 10`

### 2. Document structure extraction

The ingestion logic is primarily handled by the files under `src/sla/ingestion/`.

- `structure.py` extracts text blocks from JSON document data and groups them by section.
- `artifact_detector.py` and `cleaning.py` help detect PDF/OCR-style extraction artifacts such as:
  - decimal spacing issues
  - line-break hyphen breaks
  - suspicious token concatenations
  - scientific term spacing artifacts
- `extraction.py` is the PDF/JSON document parsing layer that filters relevant text elements and organizes them into sections.

This stage turns raw structured paper data into section-based text blocks with metadata such as:

- `section_number`
- `section_title`
- `page_number`
- `text`

### 3. Chunking

The chunking layer is in `src/sla/rag/chunking.py`.

`split_text_into_chunks(...)`:

- iterates over grouped sections
- slices each section into text windows of `chunk_size`
- applies overlap between chunks
- stores chunk metadata like document name, section, and page range

This is important because embeddings work best when text is broken down into manageable, contextual units.

### 4. Embeddings and retrieval

The embedding code is in `src/sla/rag/embeddings.py`.

- `create_embeddings(chunks)` calls Ollama embedding generation for all chunk texts
- `create_query_embedding(text)` produces a vector for the user query

The retrieval layer is in `src/sla/rag/retrieval.py`.

- `retrieve(query, collection, top_k)` sends the query embedding to ChromaDB
- it returns the top matching chunks

The vector store setup is in `src/sla/rag/chroma_store.py`.

- it creates a persistent ChromaDB client at `data/chroma_db`
- it creates or reuses the `literature` collection
- the collection uses cosine similarity storage

## Usage

### Install dependencies

This project uses Python 3.12+ and includes package metadata in `pyproject.toml`.

To install the project in editable mode:

```bash
python -m pip install -e .
```

If using a virtual environment, activate it first.

### Install Ollama models

The project expects Ollama to be available locally and the configured models to be downloaded.

```bash
ollama pull nomic-embed-text:latest
```

### Build the vector database

The main index-building flow is exposed through `pipeline.py`.

Example in Python:

```python
from pipeline import process_document

process_document()
```

This function:

- reads all JSON files in `data/json/`
- detects and groups document sections
- creates chunks
- embeds them
- stores them in ChromaDB

### Example behavior

The retrieval result prints:

- document name
- chunk ID
- section number and title
- page list
- distance score
- matching text snippet

This makes it easy to inspect which passages are most relevant to the query.

## Important notes about the current implementation

This repository is a working research prototype rather than a polished production SaaS application.

Some current characteristics:

- the main workflow is script-based, not exposed through a CLI or web interface
- retrieval is based on ChromaDB and Ollama locally
- the ingestion path expects structured JSON from document extraction rather than raw PDFs alone
- there are helper modules for cleaning and artifact detection, but the current runtime focuses on the document-to-vector pipeline

## Example usage flow

```python
from pipeline import process_document, retrieve_information

process_document(chunk_size=1000, chunk_overlap=300)
retrieve_information("here is the information about the hydrodynamic simulation box and the cosmological parameters?")
```

## Dependencies

The package is configured in `pyproject.toml` and includes:

- `docling`
- `numpy`
- `ollama`
- `chromadb`

Optional development dependency:

- `ipykernel`

## Summary

Scientific Literature Assistant is a compact, document-centric RAG system for exploring scientific literature stored as extracted JSON. It is especially useful for exploratory literature review, targeted fact retrieval, and searching through large volumes of scientific text while preserving section-level context.
