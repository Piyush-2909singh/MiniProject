import re
import pdfplumber
from vector_store import add_document

def clean_text(text):
    text = re.sub(r'\(cid:\d+\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
