import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_db/index.faiss"
META_PATH = "vector_db/metadata.pkl"

os.makedirs("vector_db", exist_ok=True)

if os.path.exists(INDEX_PATH):

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH,"rb") as f:
        metadata = pickle.load(f)

else:

    index = faiss.IndexFlatL2(384)
    metadata = []
