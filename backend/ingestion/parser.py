import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

UPLOAD_DIR = "./documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def process_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
        
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(docs)
    
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["document_name"] = os.path.basename(file_path)
        
    return chunks
