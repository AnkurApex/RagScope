from typing import List, Dict, Any
from rag.embeddings.chroma_store import get_collection

def retrieve_chunks(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve top-k relevant chunks from ChromaDB for a given query.
    """
    collection = get_collection()
    
    # query_texts will automatically use the embedding_function defined in chroma_store
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    if not results or not results["documents"] or len(results["documents"][0]) == 0:
        return []
        
    retrieved = []
    # results["documents"][0] contains list of document strings
    # distances are smaller = better (for cosine usually, actually cosine distance = 1 - cosine similarity)
    for doc, metadata, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        retrieved.append({
            "text": doc,
            "metadata": metadata,
            "score": distance # distance score from ChromaDB
        })
        
    return retrieved
