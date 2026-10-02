# Counsellor Agent: An Adaptable RAG-Powered AI Agent

Counsellor Agent is an **adaptable, knowledge-driven AI agent**, not a fixed chatbot. It is built with **Retrieval-Augmented Generation (RAG)** using **LangChain**, a **Django** REST backend and a **React** frontend. The agent knows only what an administrator feeds it: upload documents through the Django admin panel, index them, and the agent answers questions grounded in that content, with citations to the source file and page.

Because its knowledge comes from the data rather than from hard-coded logic, the same codebase can serve **any topic or organization**. Feed it hospital policies and it becomes a patient-help desk; feed it HR handbooks and it becomes an employee assistant; feed it course catalogues and it becomes a student advisor. Changing its domain is a matter of changing the documents and the persona prompt, not rewriting the application.

**Current deployment:** the agent is configured as an **Admission Counsellor** that helps students with undergraduate and postgraduate technical-education admissions: eligibility, process, fees, deadlines and other doubts.

## Key Capabilities

- **Adaptable to any domain:** the admin feeds PDFs, and the agent adapts to whatever information they contain
- **Admin-managed knowledge base:** upload, index, re-index and delete documents from the Django admin, with the vector store kept in sync
- **Grounded answers with citations:** responses are built from retrieved passages and list their source file and page
- **Swappable persona:** change the role and instructions in one prompt (`rag/query.py`) to repurpose the agent
- **Modern chat UI:** React + Vite interface with sidebar, message view and input area
- **Semantic search:** ChromaDB vector search with a distance cut-off to filter irrelevant context
- **Fast LLM inference:** Groq via LangChain (`openai/gpt-oss-120b`)

## Adapting the Agent to a New Topic or Organization

1. Log in to the Django admin and upload the organization's PDFs (policies, brochures, FAQs, manuals).
2. Select them and run **"Index selected PDFs into vector store"**.
3. Edit the persona in the prompt inside `rag/query.py` (for example, change "admission counsellor" to "HR assistant").
4. Update the UI text (chat title, sidebar name) in the frontend.

No other code changes are needed.

## Architecture

```
┌──────────────┐   POST /api/admission/chat/   ┌───────────────────────────┐
│ React (Vite) │ ────────────────────────────▶ │ Django + DRF              │
│  frontend/   │ ◀──────────────────────────── │ admission.AdmissionChatView│
└──────────────┘        JSON answer            └─────────────┬─────────────┘
                                                             │
                                              ┌──────────────▼─────────────┐
                                              │ AdmissionRAGService        │
                                              └──────────────┬─────────────┘
                     ┌───────────────────────────────────────┼──────────────────────────┐
                     ▼                                       ▼                          ▼
          EmbeddingManager                          RagRetriever ─▶ VectorStore    AdvancedRAGPipeline
     (all-MiniLM-L6-v2, chunking)                          (ChromaDB)             (ChatGroq LLM + citations)
```

**Query flow:** question → embed → top-k search in ChromaDB → filter by distance → build prompt with context → Groq LLM → answer + citations.

## Project Structure

```
.
├── config/                      # Django project root (run manage.py from here)
│   ├── manage.py
│   ├── config/                  # Django settings and root URLs
│   │   ├── settings.py
│   │   └── urls.py
│   ├── admission/               # Django app exposing the chat API
│   │   ├── urls.py              # chat/ route
│   │   ├── views.py             # AdmissionChatView
│   │   └── services/
│   │       └── rag_service.py   # AdmissionRAGService (wires the RAG pieces)
│   └── rag/                     # RAG pipeline
│       ├── document_loader.py   # Reads PDFs (PyMuPDF)
│       ├── embeddings.py        # SentenceTransformer embeddings + text splitter
│       ├── vector_store.py      # ChromaDB persistent store
│       ├── retriever.py         # Similarity search
│       ├── query.py             # Prompting, LLM call, citations
│       └── load_docs.py         # One-off ingestion script
└── frontend/                    # React + Vite app
    └── src/
        ├── App.jsx
        ├── components/          # Sidebar, ChatWindow, Message, ChatInput
        └── services/api.js      # Axios helper
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Axios |
| Backend | Django 5.2, Django REST Framework, django-cors-headers |
| LLM | Groq via `langchain-groq` (`openai/gpt-oss-120b`) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector DB | ChromaDB (persistent) |
| PDF parsing | PyMuPDF via LangChain community loaders |
| Chunking | `RecursiveCharacterTextSplitter` (1000 chars, 200 overlap) |

## Prerequisites

- Python 3.10+
- Node.js 20.19+ or 22.12+ (required by Vite 8)
- A [Groq API key](https://console.groq.com/)

## Setup

### 1. Backend

```bash
cd config

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install django djangorestframework django-cors-headers python-dotenv \
            langchain-groq langchain-core langchain-community langchain-text-splitters \
            sentence-transformers chromadb pymupdf numpy
```

Create a `.env` file inside `config/` (never commit it):

```env
AI_API=your_groq_api_key_here
```

> The key is read from the `AI_API` environment variable in `rag/query.py`.

Apply migrations:

```bash
python manage.py migrate
```

### 2. Ingest admission documents

1. Place your admission PDFs (brochures, eligibility criteria, fee structures, etc.) in a `data/` folder.
2. Run the ingestion script:

```bash
cd rag
python load_docs.py
```

This loads every PDF under `./data` (recursively), splits it into chunks, generates embeddings, and stores them in ChromaDB. Re-running it adds the documents again, so clear the vector store first if you re-ingest the same files.

### 3. Run the backend

```bash
cd config
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/admission/chat/`.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (default `http://localhost:5173`).

## API Reference

### `POST /api/admission/chat/`

**Request**

```json
{ "query": "What is the eligibility for the B.Tech program?" }
```

**Response**

```json
{
  "answer": {
    "answer": "…generated answer…\n\nCitations:\n[1] brochure.pdf (page 4)",
    "sources": [
      { "source": "brochure.pdf", "page": 4, "preview": "First 120 characters of the chunk..." }
    ],
    "history": [ { "question": "...", "answer": "...", "sources": [ ] } ]
  }
}
```

**Errors**

| Status | Meaning |
|--------|---------|
| 400 | `query` missing from the request body |

## Configuration

| Setting | Location | Default |
|---------|----------|---------|
| Groq model / temperature / max tokens | `rag/query.py` | `openai/gpt-oss-120b`, 0.1, 1024 |
| Retrieval `top_k` | `AdvancedRAGPipeline.query` | 5 |
| Max embedding distance | `rag/retriever.py` (`max_distance`) | 1.5 |
| Chunk size / overlap | `EmbeddingManager.split_documents` | 1000 / 200 |
| Vector store path | `VectorStore(persist_directory=...)` | `../data/vector_store` |
| Collection name | `VectorStore(collection_name=...)` | `pdf_documents` |
| CORS origins | `config/settings.py` | `https://localhost:5173` |

## Roadmap Ideas

- Persist chat sessions per user (Django models)
- Stream responses to the UI
- Render answers as Markdown and show citations as chips
- Support more document types (DOCX, HTML, web pages)
- Add authentication and rate limiting
- Add tests for retrieval quality and the API
