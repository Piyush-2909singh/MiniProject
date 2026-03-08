# 🚀 Enterprise Knowledge AI  
### Intelligent Document Question Answering System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)  
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)  
![AI](https://img.shields.io/badge/AI-Document%20QA-green?style=for-the-badge)  
![Database](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge)  
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

</p>

---

# 📌 Overview

**Enterprise Knowledge AI** is a lightweight **AI-inspired document assistant** that allows users to:

• Upload PDF documents  
• Ask questions from the document  
• Retrieve the most relevant answer instantly  

Instead of manually reading large documents, the system **extracts knowledge and returns answers automatically**.

This project demonstrates the **core idea behind enterprise knowledge systems, AI assistants, and Retrieval-Augmented Generation (RAG)**.

---

# 🎯 Project Motivation

Organizations store large amounts of knowledge inside:

- PDFs  
- Reports  
- Documentation  
- Research papers  
- Internal knowledge bases  

Finding information manually can be **slow and inefficient**.

This project solves the problem by enabling **AI-style interaction with documents**.

---

# ✨ Features

## 🔐 Authentication System

- User Signup  
- Secure Login  
- Session Management using **Flask-Login**  
- Access control for authorized users  

---

## 📄 Document Upload & Processing

Users can upload **PDF documents**, and the system will:

- Extract text automatically  
- Store the document securely  
- Prepare the content for querying  

---

## 🤖 Question Answering System

Users can ask questions like:

> "What is the objective of the report?"

The system will:

1. Analyze the question  
2. Search the document text  
3. Return the most relevant answer  

---

## 🖥️ Simple Dashboard

The system includes a simple interface where users can:

- Upload documents  
- Ask questions  
- View answers instantly  

---

# 🧠 How the System Works

```
User Signup
↓
User Login
↓
Upload PDF
↓
Text Extraction
↓
User Asks Question
↓
Search Document Text
↓
Return Relevant Answer
```

This workflow shows how the system processes documents and retrieves answers for the user.

---

# 🏗️ System Architecture

```
User Interface (HTML/CSS)
        │
        ▼
Flask Web Server
        │
        ▼
Authentication System
        │
        ▼
Document Upload Module
        │
        ▼
PDF Text Extraction
        │
        ▼
Question Processing Engine
        │
        ▼
Answer Retrieval System
        │
        ▼
Response to User
```

---

# 🧰 Tech Stack

## Backend

- Python  
- Flask  
- Flask-Login  
- Flask-SQLAlchemy  

---

## Document Processing

- PyMuPDF (fitz)

Used for extracting text from PDF documents.

---

## Frontend

- HTML  
- CSS  

---

## Database

- SQLite

Stores user authentication data.

---

# 📂 Project Structure

```
enterprise_knowledge
│
├── app.py
├── rag.py
├── requirements.txt
├── database.db
│
├── templates
│   ├── login.html
│   ├── signup.html
│   └── index.html
│
└── uploads
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/enterprise-knowledge-ai.git
cd enterprise-knowledge-ai
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Run the Application

```bash
python app.py
```

---

## 6️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

# 🧪 Example Usage

### Step 1  
Create an account

### Step 2  
Login to the system

### Step 3  
Upload a PDF document

### Step 4  
Ask a question

Example:

```
Question:
What is the goal of this report?

Answer:
The goal of the report is to analyze the market performance...
```

---

# ⚠️ Current Limitations

- Uses **keyword-based search**  
- No semantic understanding yet  
- Works best when question words match document words  

---

# 🔮 Future Improvements

This project can evolve into a **full enterprise AI system**.

Planned upgrades:

• Integrate **OpenAI / Gemini APIs**  
• Implement **semantic search using embeddings**  
• Add **vector database (FAISS / Chroma)**  
• Support **multiple documents**  
• Create **chat-style AI interface**  
• Build full **RAG pipeline**  
• Deploy on **cloud infrastructure**

---

# 📊 Comparison with Traditional Search

| Feature | Enterprise Knowledge AI | Traditional Search |
|------|-------------------------|--------------------|
| Document Interaction | Ask questions directly | Keyword search |
| Setup | Lightweight | Heavy enterprise systems |
| Authentication | Built-in login system | Often missing |
| Customization | Fully customizable | Limited |
| AI Expansion | Easy to extend | Harder |

---

# 🎓 Learning Outcomes

This project demonstrates:

- Backend development with **Flask**
- Document processing using **Python**
- Building **AI-style knowledge assistants**
- Basic **information retrieval systems**

---

# 👨‍💻 Author

**B.Tech AIML Student**

Interested in:

- Artificial Intelligence  
- Backend Development  
- Intelligent Systems  
- AI Knowledge Platforms  

---

# ⭐ Support the Project

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
🚀 Contribute improvements  

---

# 📜 License

This project is licensed under the **MIT License**.

---

💡 *This project represents a foundational step toward building enterprise-scale AI knowledge assistants.*
