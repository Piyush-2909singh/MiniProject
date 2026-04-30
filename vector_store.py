import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from config import Config

model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DB_DIR = Config.VECTOR_DB_DIR
INDEX_PATH = os.path.join(VECTOR_DB_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_DB_DIR, "metadata.pkl")

os.makedirs(VECTOR_DB_DIR, exist_ok=True)

if os.path.exists(INDEX_PATH):

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH,"rb") as f:
        metadata = pickle.load(f)

else:

    index = faiss.IndexFlatL2(384)
    metadata = []


def add_document(text, source, document=None, uploaded_by=None, timestamp=None, category="general"):
    try:
        vec = model.encode([text])
        index.add(vec)
        if not document:
            document = os.path.basename(source) if source else "Unknown"
        metadata.append({
            "text": text,
            "document": document,
            "source": source,
            "uploaded_by": uploaded_by or "unknown",
            "timestamp": timestamp,
            "category": category or "general"
        })
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(metadata, f)
        return True
    except Exception as e:
        print("Vector Store Error:", e)
        return False

def search(query,k=3):
    try:
        vec = model.encode([query])
        D, I = index.search(vec, k)
        results = []
        for i in I[0]:
            if i < len(metadata):
                results.append(metadata[i])
        return results
    except Exception as e:
        print("Vector Store Error:", e)
        return []