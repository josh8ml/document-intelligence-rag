# Document Intelligence RAG Platform

A production-oriented document question-answering service built with
Retrieval-Augmented Generation. Upload PDFs, ask questions in natural
language, and get answers grounded in the source documents with page-level
citations.

> **Status:** in active development. Milestone 1 of 39 complete
> (repository foundation).

## Planned Features

- Upload and validate one or more PDF documents
- Page-aware text extraction, cleaning, and chunking
- Local sentence-transformer embeddings (no per-query API cost)
- Persistent vector search over document chunks
- Grounded answers with filename and page-number citations
- Retrieval and generation evaluation metrics
- FastAPI backend, Streamlit frontend, Docker Compose, CI

## Technology Stack

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| API | FastAPI, Pydantic |
| Frontend | Streamlit |
| PDF parsing | PyMuPDF |
| Embeddings | Sentence Transformers (local) |
| Vector store | ChromaDB |
| Generation | OpenAI-compatible LLM interface |
| Testing | pytest |
| Tooling | Ruff, mypy, Docker, GitHub Actions |

## Local Setup

Requires Python 3.11 or newer.

```bash
git clone https://github.com/josh8ml/document-intelligence-rag
cd document-intelligence-rag

python3.11 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e ".[dev]"
```

Copy the environment template:

```bash
cp .env.example .env
```

## Running Tests

```bash
pytest
```

## Project Structure

document-intelligence-rag/
├── app/ # Application package
│ └── core/ # Configuration and logging
├── tests/
│ └── unit/
├── .env.example
├── pyproject.toml
└── README.md


Directories are added as the milestones that need them are implemented.

## Cost Note

Embeddings run locally on CPU and are free. LLM generation requires an
OpenAI-compatible API key, which is only needed from Milestone 12 onward.
Automated tests mock the LLM provider and never make paid calls.

## License

MIT — see [LICENSE](LICENSE).