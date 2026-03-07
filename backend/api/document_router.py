from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from auth import security
from database import models
from ingestion import parser
from rag import engine

router = APIRouter()

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save file to disk
        file_path = await parser.save_upload_file(file)
        
        # Parse document into text chunks
        chunks = parser.process_document(file_path)
        
        # Embed and add chunks to Chroma Vector DB
        engine.add_documents_to_db(chunks)
        
        return {
            "message": "Document uploaded and indexed successfully",
            "filename": file.filename,
            "chunks_processed": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
