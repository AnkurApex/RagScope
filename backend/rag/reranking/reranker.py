from typing import List, Dict, Any

def rerank(query: str, retrieved_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Re-rank the retrieved chunks.
    In a real-world scenario, you might use a CrossEncoder (e.g. Cohere or BGE).
    Here, we'll do a simple re-sorting based on existing score and return top_k to simulate the pipeline.
    """
    if not retrieved_chunks:
        return []
        
    # Chroma returns distance, where lower is better (more similar)
    # So we sort by score ascending
    sorted_chunks = sorted(retrieved_chunks, key=lambda x: x["score"])
    
    # Simulate a "re-ranked" score which would be higher is better
    for i, chunk in enumerate(sorted_chunks):
        chunk["rerank_score"] = 1.0 / (1.0 + chunk["score"]) # mock conversion to similarity
        
    return sorted_chunks[:top_k]
