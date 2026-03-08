# Python Code RAG

A Retrieval-Augmented Generation (RAG) project focused on codebase understanding.

The application clones a repository, parses source code, stores semantic representations in a vector database, and answers natural-language questions using retrieved code context.

## Core Techniques Used

### 1. Retrieval-Augmented Generation (RAG) for Code
- The project follows a full RAG pipeline:
  1. ingest code,
  2. generate embeddings,
  3. retrieve top-k relevant chunks,
  4. generate an answer grounded on retrieved context.
- This reduces hallucinations by constraining the LLM to repository-specific evidence.

### 2. AST-Based Static Code Analysis (Python)
- Python files are parsed with the built-in `ast` module.
- Functions and classes are extracted as structured blocks with:
  - symbol name,
  - block type,
  - file path,
  - line boundaries,
  - exact code snippet.
- This is more reliable than plain regex-based extraction for Python syntax.

### 3. Semantic Chunk Construction
- Parsed blocks are transformed into enriched chunks containing code + metadata.
- Each chunk includes a descriptive header (symbol, file, line range), improving retrieval quality by combining natural language and source code signals.

### 4. Dense Embeddings for Code Retrieval
- The system uses OpenAI `text-embedding-3-small` to encode code chunks and user queries into vectors.
- Dense vector similarity enables semantic search beyond keyword matching.

### 5. Vector Database Indexing with ChromaDB
- Embeddings and metadata are persisted in a ChromaDB collection.
- Retrieval is done via nearest-neighbor search (`n_results = k`) over stored vectors.
- Persistent storage path is configured under `./data/chroma`.

### 6. Context-Grounded LLM Answering
- Retrieved chunks are formatted into a structured prompt context.
- A chat completion model (`gpt-4.1-mini`) produces explanations based only on retrieved code evidence.
- Prompting strategy explicitly instructs grounded answers.

### 7. Dependency Container Pattern
- Shared clients (OpenAI and ChromaDB) are initialized once in `app/core/dependencies.py`.
- This centralizes resource setup and keeps service classes focused on their responsibilities.

## Architecture Overview

- `main.py`: CLI entry point (repository URL + question input)
- `app/ingestion/`
  - `repo_cloner.py`: clones repositories with GitPython
  - `code_loader.py`: scans source files by extension
  - `code_parser.py`: AST parsing and block extraction
  - `code_chunker.py`: chunk + metadata construction
- `app/embeddings/embedding_service.py`: embedding generation and vector storage
- `app/retrieval/retriever.py`: query embedding and top-k retrieval
- `app/llm/code_explainer.py`: prompt assembly and final answer generation
- `app/core/`: configuration and shared dependencies

## Supported File Extensions

- `.py`, `.ts`, `.js`, `.java`, `.go`, `.rs`

## Requirements

- Python 3.10+
- OpenAI API key

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

```bash
python3 main.py
```

You will be prompted to:
1. provide a repository URL,
2. ask a question about the indexed codebase.

## Example Use Cases

- "How is dependency injection implemented?"
- "Where is authentication handled?"
- "How does the error handling flow work?"

## Future Improvements

- Language-specific parsers beyond Python AST
- Re-ranking step before final context assembly
- Incremental indexing for large repositories
- Evaluation metrics for retrieval and answer quality
- API endpoint for multi-user querying
