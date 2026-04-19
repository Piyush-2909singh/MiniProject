from utils import load_documents, chunk_text
from vector_store import create_vector_store
from pypdf import PdfReader
from utils import chunk_text
from vector_store import add_chunks

def ingest_document(path):

    reader=PdfReader(path)

    text=""

    for p in reader.pages:
        text+=p.extract_text()

    chunks=chunk_text(text)

    add_chunks(chunks,path)
