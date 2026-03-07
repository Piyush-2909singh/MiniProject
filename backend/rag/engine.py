import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB_DIR = "./chroma_db"
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Use sentence-transformers (lightweight, runs securely on CPU)
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="enterprise_knowledge",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_DB_DIR
)

def add_documents_to_db(chunks):
    vector_store.add_documents(chunks)

def query_db(query: str, top_k: int = 4):
    # Returns List of Tuple[Document, float]
    results = vector_store.similarity_search_with_score(query, k=top_k)
    return results
