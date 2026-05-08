from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.database import get_db
from models.schema import QueryTelemetry, Document

router = APIRouter()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    total_queries = db.query(QueryTelemetry).count()
    avg_latency = db.query(func.avg(QueryTelemetry.latency_ms)).scalar() or 0.0
    
    total_docs = db.query(Document).count()
    
    # Hallucinations count
    hallucination_count = db.query(QueryTelemetry).filter(QueryTelemetry.hallucination_flag == True).count()
    
    # Positive vs Negative feedback
    positive_feedback = db.query(QueryTelemetry).filter(QueryTelemetry.feedback_score == 1).count()
    negative_feedback = db.query(QueryTelemetry).filter(QueryTelemetry.feedback_score == -1).count()
    
    # Token usage avg
    avg_prompt_tokens = db.query(func.avg(QueryTelemetry.token_usage_prompt)).scalar() or 0.0
    avg_completion_tokens = db.query(func.avg(QueryTelemetry.token_usage_completion)).scalar() or 0.0

    return {
        "total_queries": total_queries,
        "avg_latency_ms": round(avg_latency, 2),
        "total_documents": total_docs,
        "hallucination_rate": round(hallucination_count / total_queries, 4) if total_queries > 0 else 0.0,
        "positive_feedback": positive_feedback,
        "negative_feedback": negative_feedback,
        "avg_prompt_tokens": round(avg_prompt_tokens, 2),
        "avg_completion_tokens": round(avg_completion_tokens, 2)
    }

@router.get("/recent")
def get_recent_queries(limit: int = 10, db: Session = Depends(get_db)):
    queries = db.query(QueryTelemetry).order_by(QueryTelemetry.timestamp.desc()).limit(limit).all()
    return queries
