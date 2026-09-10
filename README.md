# 🤖 AI & Computer Science Learning Assistant
A **Retrieval-Augmented Generation (RAG)** assistant that answers Artificial Intelligence and Computer Science questions using a collection of educational PDF documents.
The system retrieves relevant information from the documents before generating an answer, helping keep responses grounded in the provided sources. Answers include **document and page citations** so users can see where the information came from.

---

## 📌 Project Overview

The **AI & Computer Science Learning Assistant** is a document-based question-answering system designed to help students learn core Artificial Intelligence and Computer Science concepts.

Instead of relying only on the language model's existing knowledge, the system follows a RAG pipeline:

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB Similarity Search
      ↓
Relevant Document Chunks
      ↓
Grounded Prompt
      ↓
Ollama LLM
      ↓
Answer + Source Citations
```

The project uses educational PDF documents covering topics such as:

* Machine Learning
* Deep Learning
* Artificial Intelligence
* Embeddings and Vector Semantics

---

## 📚 Domain & Data

### Domain

**Artificial Intelligence and Computer Science**

The document collection focuses mainly on introductory and core concepts in AI, Machine Learning, Deep Learning, and embeddings.

### Documents

The project currently uses four educational PDF documents:

| Document                         | Main Topic                                              |
| -------------------------------- | ------------------------------------------------------- |
| `01_Machine_Learning.pdf`        | Machine Learning concepts and applications              |
| `02_Deep_Learning.pdf`           | Neural networks, SGD, backpropagation and deep learning |
| `03_Artificial_Intelligence.pdf` | Artificial Intelligence concepts and definitions        |
| `04_Embeddings_and_RAG.pdf`      | Embeddings, vector semantics and related concepts       |

The documents were extracted page-by-page and divided into **74 fixed-size chunks**, using:

* Chunk size: **1000 words**
* Overlap: **200 words**

The extracted chunks retain their original **source document and page number** as metadata.

---

## 🏗️ Architecture

```text
┌──────────────────────┐
│    Streamlit UI      │
│      Frontend        │
└──────────┬───────────┘
           │
           │ HTTP / JSON
           ▼
┌──────────────────────────────┐
│       FastAPI Backend        │
│                              │
│  /health       /query        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│       RAG Pipeline           │
│                              │
│  SentenceTransformer         │
│  all-MiniLM-L6-v2            │
│            ↓                 │
│        ChromaDB              │
│            ↓                 │
│   Relevant Document Chunks   │
│            ↓                 │
│      Grounded Prompt         │
│            ↓                 │
│     Ollama llama3.2:3b       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Answer + Source Citations    │
└──────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology           | Purpose                                 |
| -------------------- | --------------------------------------- |
| Python               | Main programming language               |
| Jupyter Notebook     | RAG pipeline development and evaluation |
| PyPDF                | PDF text extraction                     |
| SentenceTransformers | Text embeddings                         |
| `all-MiniLM-L6-v2`   | Embedding model                         |
| ChromaDB             | Persistent vector database              |
| Ollama               | Local LLM inference                     |
| `llama3.2:3b`        | Language model                          |
| FastAPI              | Backend REST API                        |
| Pydantic             | Request/response validation             |
| Streamlit            | Frontend chat interface                 |
| Pytest               | Backend testing                         |

---

## 📁 Project Structure

```text
AI & COMPUTER SCIENCE LEARNING ASSISTANT/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       └── query.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── retrieval.py
│   │   │   └── generation.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── logging_config.py
│   │
│   ├── data/
│   │   └── vector_store/
│   │
│   ├── tests/
│   │   └── test_query.py
│   │
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── Data/
│   ├── 01_Machine_Learning.pdf
│   ├── 02_Deep_Learning.pdf
│   ├── 03_Artificial_Intelligence.pdf
│   └── 04_Embeddings_and_RAG.pdf
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── .env.example
│   └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── .gitignore
└── README.md
```

---

# 🔄 How the RAG Pipeline Works

### 1. Load Documents

The PDF files are loaded using PyPDF.

Each PDF page is extracted as text and stored together with:

```text
text
source
page
```

---

### 2. Chunking

Each extracted page is divided into smaller text chunks.

The project uses:

```text
Chunk size = 1000 words
Overlap = 200 words
```

The overlap helps preserve context between neighboring chunks.

---

### 3. Generate Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

These vectors allow the system to compare the meaning of the user's question with the meaning of document chunks.

---

### 4. Store Vectors

The embeddings and their corresponding text are stored in a persistent **ChromaDB** collection.

Each chunk also keeps metadata containing:

```text
source
page
```

This allows the system to provide citations in the final answer.

---

### 5. Retrieve Relevant Chunks

When a user asks a question:

1. The question is converted into an embedding.
2. ChromaDB searches for the most similar document chunks.
3. The top relevant chunks are retrieved.

The system currently retrieves **3 chunks** by default.

---

### 6. Build a Grounded Prompt

The retrieved chunks are inserted into a prompt together with the user's question.

The language model is instructed to:

* Use only the provided context.
* Avoid inventing information.
* Avoid inventing citations.
* State when the answer cannot be found in the provided documents.

---

### 7. Generate the Answer

The grounded prompt is sent to:

```text
Ollama
llama3.2:3b
```

The generated answer is returned together with the source document and page numbers.

---

# 🚀 Backend Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Basma-Alaa/AI-Computer-Science-Learning-Assistant.git
cd AI-Computer-Science-Learning-Assistant
```

## 2. Create a Virtual Environment

From the project root:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the `backend` folder based on:

```text
backend/.env.example
```

Example:

```env
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_STORE_PATH=data/vector_store
COLLECTION_NAME=cs_learning_documents
LLM_MODEL=llama3.2:3b
FRONTEND_ORIGIN=http://localhost:8501
```

---

## 5. Install and Prepare Ollama

Install Ollama and make sure the required model is available locally.

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before sending queries to the backend.

---

## 6. Start the FastAPI Backend

Make sure you are inside the `backend` directory:

```bash
cd backend
```

Then run:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Open a **second terminal** while the backend is running.

From the project root:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on:

```text
frontend/.env.example
```

Then start Streamlit:

```bash
streamlit run app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

Make sure the FastAPI backend is running before asking questions through the frontend.

---

# 🔐 Environment Variables

### Backend

| Variable            | Description                                 | Example                 |
| ------------------- | ------------------------------------------- | ----------------------- |
| `EMBEDDING_MODEL`   | SentenceTransformer embedding model         | `all-MiniLM-L6-v2`      |
| `VECTOR_STORE_PATH` | Path to the persisted ChromaDB vector store | `data/vector_store`     |
| `COLLECTION_NAME`   | ChromaDB collection name                    | `cs_learning_documents` |
| `LLM_MODEL`         | Ollama language model                       | `llama3.2:3b`           |
| `FRONTEND_ORIGIN`   | Allowed frontend origin for CORS            | `http://localhost:8501` |

> Do not commit your `.env` file. Use `.env.example` as the template.

---

# 🔌 API Reference

## GET `/health`

Checks whether the backend is running.

### Response

```json
{
  "status": "ok"
}
```

---

## POST `/query`

Sends a question to the RAG assistant.

### Request

```json
{
  "question": "What is machine learning?"
}
```

### Response

```json
{
  "answer": "Machine learning is ...",
  "sources": [
    "01_Machine_Learning.pdf, page 1",
    "01_Machine_Learning.pdf, page 2"
  ]
}
```

The exact answer and retrieved sources depend on the question.

---

## cURL Example

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Ask a Question

```bash
curl -X POST "http://127.0.0.1:8000/query" \
-H "Content-Type: application/json" \
-d "{\"question\":\"What is machine learning?\"}"
```

---

# 🧪 Testing

The backend includes tests for:

1. A successful `/query` request.
2. Invalid input handling.

Run the tests from the `backend` directory:

```bash
pytest
```

The expected behavior includes:

```text
Valid question → HTTP 200
Missing question → HTTP 422
```

---

# 📊 Evaluation

The RAG pipeline was evaluated using **10 sample questions** covering topics from the document collection.

The evaluation checks:

* **Relevance** — whether the retrieved chunks are related to the question.
* **Grounding** — whether the generated answer is supported by the retrieved context.
* **Correctness** — whether the answer is correct according to the provided documents.

### Evaluation Questions

| #  | Question                                                                     |
| -- | ---------------------------------------------------------------------------- |
| 1  | What is machine learning?                                                    |
| 2  | What is the difference between artificial intelligence and machine learning? |
| 3  | What is overfitting?                                                         |
| 4  | What is stochastic gradient descent?                                         |
| 5  | What is a neural network?                                                    |
| 6  | What is artificial intelligence?                                             |
| 7  | What is the Turing test?                                                     |
| 8  | What is the distributional hypothesis?                                       |
| 9  | What are word embeddings?                                                    |
| 10 | What is vector semantics?                                                    |

The detailed evaluation table is available in:

```text
notebooks/rag_pipeline.ipynb
```

It contains the retrieved sources, generated answers, and manual evaluation fields for relevance, grounding, and correctness.

---

# ⚠️ Failure Cases & Mitigation

Semantic similarity does not always guarantee that every retrieved chunk directly answers a question.

A retrieved chunk may be related to the topic but not contain the exact information needed to answer the question.

To reduce this problem, the system:

* Retrieves multiple chunks instead of relying on a single result.
* Preserves source and page metadata.
* Provides retrieved context to the language model.
* Instructs the model to use only the provided context.
* Instructs the model not to invent citations.
* Instructs the model to state when the answer cannot be found in the documents.

---

# 📦 Persistent Vector Store

The project uses a persistent ChromaDB vector store.

The stored collection is:

```text
cs_learning_documents
```

The current vector store contains:

```text
74 document chunks
```

The configuration records the main RAG settings, including:

```text
Chunk size:       1000
Overlap:          200
Embedding model:  all-MiniLM-L6-v2
Vector store:     Chroma
Collection:       cs_learning_documents
LLM:              llama3.2:3b
```

The backend loads the persisted vector store rather than rebuilding the embeddings for every API request.

---

# 🖥️ Frontend

The frontend is implemented using **Streamlit**.

It provides a simple chat interface where users can:

1. Enter a Computer Science or AI question.
2. Send the question to the FastAPI backend.
3. Receive the generated answer.
4. View the source documents and page citations.

---

# 🔒 Project & Security Notes

The repository should not contain:

```text
.venv/
.env
*.log
__pycache__/
```

API keys or other private credentials should never be committed to GitHub.

The `.env.example` files contain example configuration values only.

---

# 🎯 Project Goals

The main goals of this project are to:

* Build a complete RAG pipeline.
* Learn how document retrieval works.
* Convert text into embeddings.
* Store and search vectors using ChromaDB.
* Generate grounded answers using a local LLM.
* Build a REST API using FastAPI.
* Create a user interface using Streamlit.
* Provide source/page citations.
* Evaluate retrieval and answer quality.
* Build a complete end-to-end AI application.

---

# 📸 Screenshots

### Streamlit Frontend

<img width="1738" height="777" alt="Screenshot 2026-09-10 230451" src="https://github.com/user-attachments/assets/e96d249f-8b6a-4457-80ca-0c5693b8c33a" />


### FastAPI Swagger Documentation

<img width="1852" height="895" alt="image" src="https://github.com/user-attachments/assets/ff0b2cb0-3297-4a53-941c-8b94b1d74166" />



---

# ✅ End-to-End Workflow

```text
Educational PDFs
      ↓
PDF Text Extraction
      ↓
Page Documents
      ↓
Fixed-Size Chunking
1000 words / 200 overlap
      ↓
SentenceTransformer
all-MiniLM-L6-v2
      ↓
Embeddings
      ↓
Persistent ChromaDB
      ↓
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Top 3 Relevant Chunks
      ↓
Grounded Prompt
      ↓
Ollama
llama3.2:3b
      ↓
Answer + Citations
      ↓
FastAPI
      ↓
Streamlit
```

---

# 👩‍💻 Project Status

The project implements the complete **Core Track — Text-based RAG Assistant**, including:

* [x] PDF document collection
* [x] PDF text extraction
* [x] Text chunking
* [x] Text embeddings
* [x] Persistent ChromaDB vector store
* [x] Semantic retrieval
* [x] Grounded prompting
* [x] Local LLM generation with Ollama
* [x] Source/page citations
* [x] FastAPI backend
* [x] `/health` endpoint
* [x] `/query` endpoint
* [x] CORS configuration
* [x] Backend tests
* [x] Streamlit frontend
* [x] RAG evaluation
* [x] Project documentation

---

# 📄 License

This project was created for educational and training purposes.

```



