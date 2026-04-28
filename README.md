# Enterprise Knowledge Assistant

Flask-based RAG application with authentication, RBAC, document ingestion, semantic search (FAISS), and chat UI with citations.

## Features
- Authentication with role-based access control (RBAC)
- PDF ingestion with metadata (document, source, uploaded_by, timestamp, category)
- Semantic search (FAISS) with strict grounding and relevance filtering
- RAG chat with grouped source citations
- Security hardening: CSRF, rate limiting, security headers, input validation
- Cloud-native config via environment variables

## Requirements
- Python 3.10+ recommended (venv)
- Windows, macOS, or Linux

## Setup (Local)
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Create a `.env` file (optional but recommended):
   - `SECRET_KEY=your-secret`
   - `DATABASE_PATH=./database/users.db`
   - `UPLOAD_FOLDER=./uploads`
   - `MAX_CONTENT_LENGTH=5242880`

## Run
- Development:
  - `python app.py`
- Production (gunicorn):
  - `gunicorn -w 2 -b 0.0.0.0:5000 app:create_app()`

## Docker
Build:
- `docker build -t enterprise-knowledge-assistant .`

Run:
- `docker run -p 5000:5000 --env-file .env enterprise-knowledge-assistant`

## Configuration
Configuration is loaded from `config.py` using environment variables with defaults:
- `SECRET_KEY`
- `DATABASE_PATH`
- `UPLOAD_FOLDER`
- `MAX_CONTENT_LENGTH`

## Key Paths
- `uploads/` - Uploaded documents
- `vector_db/` - FAISS index and metadata
- `database/users.db` - SQLite user database

## Roles
- Default role: `user`
- Admin role: `admin`
- Admin-only route: `/admin`

## Ingestion
- Upload PDFs via `/admin`
- Each chunk is stored with:
  - text
  - document
  - source
  - uploaded_by
  - timestamp
  - category

## Chat API
POST `/chat` or `/ask`

Request:
```
{ "message": "your question" }
```

Response:
```
{
  "answer": "...",
  "sources": [
    {
      "document": "file.pdf",
      "snippets": ["...", "..."]
    }
  ]
}
```

## Tests
Run:
- `pytest -q`

## Notes
- For production rate limiting, configure a persistent limiter backend.
- Set `HF_TOKEN` to avoid Hugging Face download throttling.
