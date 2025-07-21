# vector_memory.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from datetime import datetime

class VectorMemory:
    def __init__(self, persist_dir="/Users/karthimurugesan/Desktop/JARVIS/jarvis_memory"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="jarvis_memory")

    def add(self, text, role, timestamp):
        embedding = self.model.encode([text])[0].tolist()
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"role": role, "timestamp": timestamp}],
            ids=[str(hash(text + timestamp))]
        )

    def search(self, query, top_k=3):
        embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        return results["documents"][0] if results["documents"] else []
