import os
import math
import json
from google import genai
from google.genai import types
from typing import List

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> List[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return result.embeddings[0].values

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(v1, v2))
    norm_a = math.sqrt(sum(x * x for x in v1))
    norm_b = math.sqrt(sum(x * x for x in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

class PurePythonVectorStore:
    def __init__(self, db_path="./local_vec_db.json"):
        self.db_path = db_path
        self.data = {"ids": [], "documents": [], "metadatas": [], "embeddings": []}
        self.load()

    def load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                pass

    def save(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f)

    def add(self, documents, metadatas, ids):
        for doc, meta, doc_id in zip(documents, metadatas, ids):
            if doc_id in self.data["ids"]:
                continue
            emb = get_embedding(doc)
            self.data["ids"].append(doc_id)
            self.data["documents"].append(doc)
            self.data["metadatas"].append(meta)
            self.data["embeddings"].append(emb)
        self.save()

    def query(self, query_texts, n_results=10, include=None):
        if not self.data["ids"]:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        q_emb = get_embedding(query_texts[0])

        results = []
        for i in range(len(self.data["ids"])):
            score = cosine_similarity(q_emb, self.data["embeddings"][i])
            dist = 1.0 - score  # distance: lower = more similar
            results.append((dist, self.data["documents"][i], self.data["metadatas"][i]))

        results.sort(key=lambda x: x[0])
        results = results[:n_results]

        return {
            "documents": [[r[1] for r in results]],
            "metadatas": [[r[2] for r in results]],
            "distances": [[r[0] for r in results]]
        }

# Global singleton instance
_store = PurePythonVectorStore()

def get_collection(collection_name: str = "ragscope_docs"):
    return _store
