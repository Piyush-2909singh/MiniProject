import os
import re
from datetime import datetime

import pdfplumber
from werkzeug.utils import secure_filename

from vector_store import add_document

def clean_text(text):
    text = re.sub(r'\(cid:\d+\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def ingest_document(path, uploaded_by=None, category="general"):
    try:
        text = ""

        document_name = secure_filename(os.path.basename(path))
        timestamp = datetime.now().isoformat()
        uploader = uploaded_by or "unknown"
        doc_category = category or "general"

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    t = clean_text(t)
                    text += t + "\n"

        chunk_size = 300
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            if len(chunk.strip()) > 50:
                add_document(
                    chunk,
                    path,
                    document=document_name,
                    uploaded_by=uploader,
                    timestamp=timestamp,
                    category=doc_category
                )
        return True
    except Exception as e:
        print("Ingestion Error:", e)
        return False