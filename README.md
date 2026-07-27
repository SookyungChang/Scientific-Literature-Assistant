# Scientific Literature Assistant

A RAG-based AI assistant for understanding scientific literature using Large Language Models (LLMs), vector search, and retrieval-augmented generation.

## Overview

Scientific papers contain a large amount of complex information, making it challenging to efficiently search and extract relevant knowledge.

This project aims to build an AI-powered literature assistant that allows users to interact with research papers through natural language questions.

The system processes scientific PDFs, retrieves relevant information, and generates context-aware answers using modern NLP and LLM technologies.

## Project Goals

- Extract and process text from scientific papers
- Build a semantic search pipeline for research documents
- Implement Retrieval-Augmented Generation (RAG)
- Enable question answering over scientific literature
- Deploy the application as an AI service

## Architecture

```
Scientific Paper (PDF)
        |
        v
   PDF Processing
      (PyMuPDF)
        |
        v
    Text Chunking
        |
        v
    Embedding Model
        |
        v
   Vector Database
     (ChromaDB)
        |
        v
    Retrieval
        |
        v
      LLM
    (Ollama)
        |
        v
    Generated Answer
```

## Current Progress

### Completed

- [x] Project structure setup using `pyproject.toml`
- [x] Python package structure with `src` layout
- [x] PDF text extraction pipeline using PyMuPDF
- [x] Configuration management using `pathlib`

### In Progress

- [ ] Document chunking strategy
- [ ] Embedding generation
- [ ] Vector database integration
- [ ] Retrieval-Augmented Generation pipeline
- [ ] FastAPI backend
- [ ] Docker deployment
- [ ] User interface

## Tech Stack

### Programming
- Python
- PyMuPDF

### AI / NLP
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Sentence Embeddings
- Vector Search

### Planned Technologies

- LangChain
- ChromaDB
- Ollama
- FastAPI
- Docker

## Project Structure

```
scientific-literature-assistant/

├── data/
│   └── papers/
│
├── src/
│   └── scientific_literature_assistant/
│       ├── config.py
│       ├── ingestion.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── retrieval.py
│       └── api.py
│
├── notebooks/
├── tests/
├── pyproject.toml
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd scientific-literature-assistant
```

Install the project:

```bash
pip install -e .
```

## Usage

Place scientific papers inside:

```
data/papers/
```

Run the PDF ingestion pipeline:

```bash
python -m scientific_literature_assistant.ingestion
```

## Motivation

As a physicist working with scientific data, I experienced the difficulty of extracting meaningful information from large amounts of research literature.

This project explores how modern AI systems can support researchers by combining domain knowledge with Large Language Models and retrieval-based approaches.