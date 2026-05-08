import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from rag.retrieval.retriever import retrieve_chunks
from rag.reranking.reranker import rerank
from rag.prompting.generator import generate_answer
from telemetry.logger import log_telemetry

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    telemetry_id: int

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        # 1. Retrieve
        retrieved = retrieve_chunks(query, top_k=10)
        
        # 2. Rerank
        reranked = rerank(query, retrieved, top_k=5)
        
        # 3. Generate Answer
        answer, full_prompt, prompt_tokens, comp_tokens = generate_answer(query, reranked)
        
        # 4. Hallucination Check (simplified logic - checking if model says "I don't know")
        hallucination_flag = False
        if "I don't know" in answer or "I do not know" in answer:
            pass # Not a hallucination, just standard refusal
        elif not reranked:
            hallucination_flag = True # Answered without context
            
        latency_ms = (time.time() - start_time) * 1000
        
        # 5. Log Telemetry
        telemetry_id = log_telemetry(
            db=db,
            query=query,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=comp_tokens,
            retrieved_chunks=retrieved,
            reranked_chunks=reranked,
            final_prompt=full_prompt,
            final_answer=answer,
            hallucination_flag=hallucination_flag
        )
        
        return ChatResponse(answer=answer, telemetry_id=telemetry_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
