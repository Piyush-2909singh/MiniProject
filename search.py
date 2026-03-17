import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

NDEX_PATH = "vector_db/index.faiss"
META_PATH = "vector_db/metadata.pkl"

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = None

if os.path.exists(META_PATH):
    metadata = pickle.load(open(META_PATH,"rb"))
else:
    metadata = []


def search(query, k=3):

    if index is None or len(metadata) == 0:
        return []

    query_vec = model.encode([query])

    D, I = index.search(query_vec, k)

    results = []

    for idx in I[0]:

        if idx < len(metadata):
            results.append(metadata[idx])

    return results


    