# 🤖 AI & Computer Science Learning Assistant

A Retrieval-Augmented Generation (RAG) assistant that answers computer science and AI questions grounded strictly in local PDF documents, complete with page citations.

## 📌 Domain & Data Description

- **Domain**: Computer Science & Machine Learning core concepts.
- **Source Data**: Structured course PDFs parsed and split into **74 semantic chunks**.
- **Vector Database**: ChromaDB (persisted locally under `backend/data/vector_store/`).


---

## 🏗️ Architecture

- **Frontend**: Streamlit chat UI
- **Backend**: FastAPI (`/health`, `/query`)
- **Vector Database**: ChromaDB (74 persisted document chunks)
- **Embeddings**: `SentenceTransformers` (`all-MiniLM-L6-v2`)
- **LLM**: Ollama (`llama3.2:3b`)

```text
┌─────────────────┐       HTTP / JSON       ┌────────────────────────┐
│  Streamlit UI   │ ──────────────────────> │     FastAPI Backend    │
│  (Frontend)     │ <────────────────────── │  (API & RAG Orchestrator)
└─────────────────┘                         └───────────┬────────────┘
                                                        │
                                            ┌───────────┴───────────┐
                                            ▼                       ▼
                                   ┌────────────────┐      ┌─────────────────┐
                                   │    ChromaDB    │      │   Ollama LLM    │
                                   │ (Vector Store) │      │  (llama3.2:3b)  │
                                   └────────────────┘      └─────────────────┘


---

## 📁 Directory Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/routes/    # /health and /query handlers
│   │   ├── core/         # App configuration
│   │   ├── schemas/      # QueryRequest / QueryResponse Pydantic models
│   │   ├── services/     # RAG retrieval & Ollama generation
│   │   └── main.py       # FastAPI lifecycle initialization
│   ├── data/vector_store # Persisted ChromaDB vectors
│   ├── tests/            # Pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py            # Streamlit UI
│   ├── api_client.py     # Backend API client wrapper
│   ├── .env.example
│   └── requirements.txt
├── .gitignore
└── README.md
