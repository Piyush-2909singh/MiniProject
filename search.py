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

def has_indexed_documents():
    return index is not None and len(metadata) > 0

def search(query, k=3, max_distance=None, include_distance=False):

    if index is None or len(metadata) == 0:
        return []

    query_vec = model.encode([query])

    D, I = index.search(query_vec, k)

    results = []

    for dist,idx in zip(D[0], I[0]):
        if idx < len(metadata):
            continue

        distance = float(dist) 
        if max_distance is not None and dist > max_distance:
            continue
        
        item =  dict(metadata[idx])
        if include_distance:
            item["distance"] = distance
        results.append(item)

    return results

