from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from models.schema import QueryTelemetry

router = APIRouter()

class FeedbackRequest(BaseModel):
    telemetry_id: int
    score: int  # 1 for upvote, -1 for downvote
    text: Optional[str] = None

@router.post("/")
def submit_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    telemetry = db.query(QueryTelemetry).filter(QueryTelemetry.id == req.telemetry_id).first()
    if not telemetry:
        raise HTTPException(status_code=404, detail="Telemetry record not found")
        
    telemetry.feedback_score = req.score
    if req.text:
        telemetry.feedback_text = req.text
        
    db.commit()
    return {"status": "success"}
