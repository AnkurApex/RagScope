import os
from typing import List, Dict, Any, Tuple
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def _network_is_disabled() -> bool:
    proxy_values = [
        os.getenv("HTTPS_PROXY", ""),
        os.getenv("HTTP_PROXY", ""),
        os.getenv("ALL_PROXY", ""),
    ]
    return any("127.0.0.1:9" in value for value in proxy_values)

def _fallback_answer(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    if not context_chunks:
        return "I don't know based on the ingested documents."

    excerpts = []
    for chunk in context_chunks[:3]:
        text = " ".join(chunk["text"].split())
        excerpts.append(text[:500])

    return (
        "Gemini generation is unavailable, so I found the most relevant ingested "
        f"context for your question: {query}\n\n"
        + "\n\n---\n\n".join(excerpts)
    )

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

    if (
        os.getenv("RAGSCOPE_LOCAL_LLM", "").lower() in {"1", "true", "yes"}
        or not os.getenv("GEMINI_API_KEY")
        or _network_is_disabled()
    ):
        return _fallback_answer(query, context_chunks), user_prompt, 0, 0

    try:
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        response = model.generate_content(
            user_prompt,
            generation_config={"temperature": 0.0},
        )
    except Exception as e:
        print(f"Gemini generation unavailable, using local fallback: {e}")
        return _fallback_answer(query, context_chunks), user_prompt, 0, 0

    answer = getattr(response, "text", None) or str(response)

    # Token counts vary by SDK/version; default to 0 if unavailable.
    usage = getattr(response, "usage_metadata", None)
    prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0) if usage else 0
    completion_tokens = int(getattr(usage, "candidates_token_count", 0) or 0) if usage else 0

    return answer, user_prompt, prompt_tokens, completion_tokens
