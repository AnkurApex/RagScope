from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    upload_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    chunk_ids = Column(JSON) # List of chunk UUIDs
    metadata_obj = Column(JSON) # extra metadata
    
    # telemetry mapping
    queries = relationship("QueryTelemetry", back_populates="document")

class QueryTelemetry(Base):
    __tablename__ = "query_telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # RAG results
    retrieved_chunks = Column(JSON) # list of text chunks and their scores
    reranked_chunks = Column(JSON)
    final_prompt = Column(Text)
    final_answer = Column(Text)
    
    # Metrics
    latency_ms = Column(Float)
    token_usage_prompt = Column(Integer)
    token_usage_completion = Column(Integer)
    
    # Quality / Observation
    hallucination_flag = Column(Boolean, default=False)
    feedback_score = Column(Integer, nullable=True) # 1 for up, -1 for down
    feedback_text = Column(Text, nullable=True)
    
    # Reference
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    document = relationship("Document", back_populates="queries")
