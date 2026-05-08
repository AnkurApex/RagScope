import uuid
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    # Basic cleaning
    text = text.replace('\x00', '') # remove null bytes
    return ' '.join(text.split())

def chunk_document(content: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split document content into smaller chunks natively.
    """
    cleaned_content = clean_text(content)
    
    chunks = []
    i = 0
    while i < len(cleaned_content):
        chunk = cleaned_content[i:i + chunk_size]
        chunks.append(chunk)
        i += (chunk_size - chunk_overlap)
    
    # Create structured chunks
    structured_chunks = []
    for i, chunk in enumerate(chunks):
        structured_chunks.append({
            "id": str(uuid.uuid4()),
            "text": chunk,
            "chunk_index": i
        })
    return structured_chunks
