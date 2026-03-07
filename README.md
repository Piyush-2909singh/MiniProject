# Enterprise Knowledge Intelligence Platform

A production-grade Enterprise AI system built with Retrieval-Augmented Generation (RAG) and Semantic Search, permitting organizations to ask natural language questions against their internal data silos (PDF, TXT, DOCX), citing sources securely using Role-Based Access Control.

## Key Features
- **Extensive Document Ingestion**: Parse text securely with Langchain and `unstructured`.
- **Semantic Vector Engine**: ChromaDB paired with HuggingFace `all-MiniLM-L6-v2` embeddings for rich contextual chunk retrieval.
- **RAG Generation Engine**: Context-grounded LLM completions using local models (e.g., TinyLlama / Mistral) ensuring enterprise data never leaves your VPC.
- **Source Citation Component**: Strict source traceability and confidence scores attached to all LLM inferences.
- **Modern React App Dashboard**: Built with Next.js 15 App router, lucide-icons, glassmorphic UI, and Tailwind CSS.
- **FastAPI Backend**: JWT token RBAC security and asynchronous DB generation with SQLAlchemy + SQLite.

## How to Run Locally

### Requirements
- Docker & Docker Compose
- Or Python 3.10+ and Node.js 20+

### Option 1: Docker Compose
```bash
docker-compose up --build
```
Navigate to `http://localhost:3000`. Backend will run on `http://localhost:8000`.

### Option 2: Run Separately
**Backend:**
```bash
cd backend
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## Creating an Admin Account
To upload documents, you need an Admin account. Go to `/register`, toggle the role select dropdown, and select "Admin", then upload your PDFs in the secure Enterprise dashboard.
