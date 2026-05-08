import os
from google import genai
from google.genai import types
from typing import List, Dict, Any, Tuple

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(query: str, context_chunks: List[Dict[str, Any]]) -> Tuple[str, str, int, int]:
    """
    Generate an answer using Gemini based on retrieved context.
    Returns: (answer, prompt, prompt_tokens, completion_tokens)
    """
    context_text = "\n\n---\n\n".join([f"Document Chunk:\n{c['text']}" for c in context_chunks])

    sys_prompt = (
        "You are RAGScope, a highly accurate, AI-powered assistant. "
        "Your task is to answer the user's question based strictly on the provided context.\n"
        "If the context does not contain the answer, politely state that you do not know. "
        "Do not hallucinate or make up information. Base your response solely on the context."
    )

    user_prompt = (
        f"System: {sys_prompt}\n\n"
        f"Context information is below.\n\n{context_text}\n\n"
        f"Given the context information, answer the following question: {query}"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(temperature=0.0)
    )

    answer = response.text

    # Token counts from usage metadata
    prompt_tokens = response.usage_metadata.prompt_token_count or 0
    completion_tokens = response.usage_metadata.candidates_token_count or 0

    return answer, user_prompt, prompt_tokens, completion_tokens
