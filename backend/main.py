from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.database import init_db
from api.chat import router as chat_router
from api.ingest import router as ingest_router
from api.analytics import router as analytics_router
from api.feedback import router as feedback_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    init_db()
    yield
    # Shutdown

app = FastAPI(
    title="RAGScope API",
    description="Production-grade RAG system with telemetry and observability",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "RAGScope Backend"}

# Include routers
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(ingest_router, prefix="/api/ingest", tags=["ingestion"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
