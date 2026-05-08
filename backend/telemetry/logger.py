from sqlalchemy.orm import Session
from models.schema import QueryTelemetry

def log_telemetry(
    db: Session,
    query: str,
    latency_ms: float,
    prompt_tokens: int,
    completion_tokens: int,
    retrieved_chunks: list,
    reranked_chunks: list,
    final_prompt: str,
    final_answer: str,
    hallucination_flag: bool = False
) -> int:
    """
    Logs RAG telemetry data into the database.
    Returns the ID of the created telemetry record.
    """
    telemetry = QueryTelemetry(
        user_query=query,
        latency_ms=latency_ms,
        token_usage_prompt=prompt_tokens,
        token_usage_completion=completion_tokens,
        retrieved_chunks=retrieved_chunks,
        reranked_chunks=reranked_chunks,
        final_prompt=final_prompt,
        final_answer=final_answer,
        hallucination_flag=hallucination_flag
    )
    
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)
    return telemetry.id
