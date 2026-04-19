import re
import pdfplumber
from vector_store import add_document

def clean_text(text):
    text = re.sub(r'\(cid:\d+\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def ingest_document(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:
            t = page.extract_text()

        if t:
            t = clean_text(t)
            text += t + "\n"

    # better chunking
    chunk_size = 300

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i+chunk_size]

        if len(chunk.strip()) > 50:
            add_document(chunk, path)