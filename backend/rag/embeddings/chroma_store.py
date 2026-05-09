import os
import math
import json
import hashlib
import re
from typing import List
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

LOCAL_EMBEDDING_DIM = 384
_REMOTE_EMBEDDING_UNAVAILABLE = False

def _local_embedding(text: str) -> List[float]:
    """Deterministic fallback embedding so local dev still works without Gemini access."""
    vector = [0.0] * LOCAL_EMBEDDING_DIM
    tokens = re.findall(r"[a-z0-9]+", text.lower())

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % LOCAL_EMBEDDING_DIM
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]

def _candidate_embedding_models() -> tuple[str, ...]:
    configured = os.getenv("GEMINI_EMBEDDING_MODEL")
    if configured:
        return (configured,)
    return ("models/text-embedding-004", "models/embedding-001")

def _network_is_disabled() -> bool:
    proxy_values = [
        os.getenv("HTTPS_PROXY", ""),
        os.getenv("HTTP_PROXY", ""),
        os.getenv("ALL_PROXY", ""),
    ]
    return any("127.0.0.1:9" in value for value in proxy_values)

def get_embedding(text: str, task_type: str = "retrieval_document") -> List[float]:
    """
    Returns a vector embedding for `text`.

    Gemini embeddings are preferred, but local development should not 500 when
    the configured model is unavailable, the API key is missing, or networking is
    blocked. In those cases we fall back to a deterministic hashed embedding.
    """
    global _REMOTE_EMBEDDING_UNAVAILABLE

    if os.getenv("RAGSCOPE_LOCAL_EMBEDDINGS", "").lower() in {"1", "true", "yes"}:
        return _local_embedding(text)

    if _REMOTE_EMBEDDING_UNAVAILABLE or not os.getenv("GEMINI_API_KEY") or _network_is_disabled():
        return _local_embedding(text)

    # Model name differs across Gemini SDKs; prefer the widely-available embedding model.
    # If the first model fails (e.g. older account/region), fall back.
    last_err: Exception | None = None
    for model in _candidate_embedding_models():
        try:
            res = genai.embed_content(
                model=model,
                content=text,
                task_type=task_type,
            )
            emb = res.get("embedding") if isinstance(res, dict) else getattr(res, "embedding", None)
            if emb is None:
                raise RuntimeError("Embedding response missing `embedding` field")
            return list(emb)
        except Exception as e:
            last_err = e
            continue

    _REMOTE_EMBEDDING_UNAVAILABLE = True
    print(f"Gemini embeddings unavailable, using local fallback: {last_err}")
    return _local_embedding(text)

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

        q_emb = get_embedding(query_texts[0], task_type="retrieval_query")

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
