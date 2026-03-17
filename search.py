import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")