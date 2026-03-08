# 🤖 Enterprise Knowledge AI — Document Question Answering System

This project is a simple AI-inspired document assistant that allows users to upload a PDF document and ask questions related to the document.

Instead of manually searching through large documents, the system extracts the text from the uploaded file and returns the most relevant answer based on the user’s query.

The goal of this project is to demonstrate a basic document knowledge retrieval system using Python and Flask.

---

## 📌 About This Project

• Built as a learning project for backend development  
• Demonstrates document-based question answering  
• Works with uploaded PDF files  
• Includes user authentication system  
• Simple AI-style interface for interaction  

---

## 🚀 Key Features

✔ User Signup and Login System  
✔ Secure Authentication using Flask-Login  
✔ Upload PDF Documents  
✔ Automatic Text Extraction from PDF  
✔ Ask Questions from Uploaded Document  
✔ Retrieve Relevant Answers from Document Text  
✔ Simple Dashboard Interface  

---

## 🧩 System Components

Authentication Module  
Handles user signup, login and logout. Only authenticated users can access the system.

Document Upload Module  
Allows users to upload PDF documents which are stored in the uploads folder.

Text Extraction Module  
Extracts text from uploaded PDF documents using PyMuPDF.

Question Processing Module  
Processes the question entered by the user.

Answer Retrieval Module  
Searches the document text and returns the most relevant sentence.

---

## 🛠️ Technologies Used

Backend  
Python  
Flask  
Flask-Login  
Flask-SQLAlchemy  

Document Processing  
PyMuPDF (fitz)

Frontend  
HTML  
CSS  

Database  
SQLite

---

## ⚙️ System Workflow

User Signup  
↓  
User Login  
↓  
Upload PDF Document  
↓  
Extract Text from PDF  
↓  
User Asks Question  
↓  
System Searches Document Text  
↓  
Relevant Answer Returned

---

## 📂 Project Structure

enterprise_knowledge

app.py  
rag.py  
requirements.txt  
database.db  

templates  
login.html  
signup.html  
index.html  

uploads  

---

## 🧪 How to Run the Project

Step 1 — Open terminal inside the project folder

cd enterprise_knowledge

Step 2 — Create virtual environment

python -m venv venv

Step 3 — Activate virtual environment

Windows

venv\Scripts\activate

Step 4 — Install required libraries

pip install -r requirements.txt

Step 5 — Run the application

python app.py

Step 6 — Open in browser

http://127.0.0.1:5000

---

## 📊 Example Usage

1. Create an account  
2. Login to the system  
3. Upload a PDF document  
4. Ask a question related to the document  
5. The system retrieves the most relevant answer  

---

## ⚠️ Current Limitations

Currently the system uses keyword-based search to retrieve answers. If the question wording is very different from the document text, the accuracy of the answer may decrease.

---

## 🔮 Future Improvements

• Integrate AI APIs such as OpenAI or Gemini  
• Implement semantic search using embeddings  
• Support multiple document uploads  
• Add chat-style interface for asking questions  
• Improve answer ranking using RAG techniques  
• Build a knowledge base for enterprise use  

---

## 🎯 Purpose of This Project

• Practice backend development using Flask  
• Understand document processing with Python  
• Explore the concept of document-based knowledge retrieval  
• Build a simple AI-style information retrieval system  

---

## 👩‍💻 Author

B.Tech AIML Student  
Interested in AI, backend development and intelligent systems

---

⭐ This project represents a learning step towards building intelligent document assistants.
