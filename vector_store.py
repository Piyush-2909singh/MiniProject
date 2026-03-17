import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_db/index.faiss"
META_PATH = "vector_db/metadata.pkl"