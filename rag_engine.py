import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class PersonalRAG:
    def __init__(self, json_path="/Users/karthimurugesan/Desktop/JARVIS/memory.json"):
        with open(json_path, "r") as f:
            data = json.load(f)

        self.qa_pairs = list(data.items())  # List of (question, answer)
        self.questions = [q for q, a in self.qa_pairs]
        self.answers = [a for q, a in self.qa_pairs]

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(self.questions, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query, top_k=3, threshold=0.7):
        query_vec = self.model.encode([query])
        D, I = self.index.search(query_vec, top_k)

        results = []
        for dist, idx in zip(D[0], I[0]):
            similarity = 1 / (1 + dist)  # Convert L2 distance to pseudo-similarity
            if similarity >= threshold:
                results.append((self.questions[idx], self.answers[idx], similarity))

        return results

    def query(self, query, top_k=3, threshold=0.7):
        matches = self.search(query, top_k=top_k, threshold=threshold)
        if not matches:
            return "Sorry, I couldn't find anything relevant from your personal memory."

        response = "Here’s what I found from your memory:\n"
        for i, (q, a, sim) in enumerate(matches, start=1):
            response += f"\n{i}. {a}"
        return response
