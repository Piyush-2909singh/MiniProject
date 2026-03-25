## Enterprise Knowledge Intelligence Platform using RAG

This project is an enterprise knowledge assistant platform that leverages Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware answers to user queries using both internal documents and uploaded files. It features user authentication, document ingestion, semantic search, and a chat interface powered by a language model.

---

### Features
- **User Authentication:** Secure login and registration system using Flask and SQLite.
- **Admin Panel:** Upload and manage documents (PDF/TXT) for knowledge ingestion.
- **Document Ingestion:** Extracts and cleans text from uploaded documents, splits into chunks, and stores semantic vectors.
- **Semantic Search:** Uses FAISS and Sentence Transformers for fast, relevant document retrieval.
- **RAG Chatbot:** Answers user questions by combining retrieved context with a language model (TinyLlama).
- **Modern UI:** Responsive, dark-themed web interface for chat, admin, and authentication.

---

### File Structure

```
├── app.py                # Main Flask app (routes, auth, upload, chat)
├── ingestion.py          # PDF/TXT ingestion and chunking logic
├── rag_pipeline.py       # RAG pipeline: search + LLM answer generation
├── search.py             # Semantic search using FAISS and embeddings
├── vector_store.py       # Vector DB management (add/search vectors)
├── documents.txt         # Example internal knowledge base
├── requirements.txt      # Python dependencies
├── uploads/              # Uploaded documents (PDF/TXT)
├── templates/            # HTML templates (chat, admin, login, etc.)
│   ├── admin.html
│   ├── chat.html
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   └── register.html
└── vector_db/            # FAISS index and metadata (auto-created)
```

---

### Setup Instructions

1. **Clone the repository**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **(Optional) Download or place PDF/TXT files in `uploads/`**
4. **Run the application:**
	```bash
	python app.py
	```
5. **Access the app:** Open [http://localhost:5000](http://localhost:5000) in your browser.

---

### Usage
- **Sign up / Log in** to access the platform.
- **Admin users** can upload documents via the Admin Panel.
- **Ask questions** in the chat interface; the system retrieves relevant context and generates answers.

---

### Dependencies
- Flask, Flask-Login
- flask-sqlalchemy
- pymupdf (PDF extraction)
- faiss, sentence-transformers
- transformers (TinyLlama model)

---

### Notes
- Uploaded documents are chunked and indexed for semantic search.
- The RAG pipeline combines search results with a language model for accurate, context-aware answers.
- Example knowledge is provided in `documents.txt`.

---

### License
This project is for educational and demonstration purposes.