# RAGScope - Production RAG Platform

RAGScope is a complete, production-grade Retrieval-Augmented Generation (RAG) system built with observability, telemetry, and evaluation pipelines at its core.

## Features
- **Document Ingestion**: Upload PDFs and TXTs, automatic text extraction and chunking.
- **Embeddings**: ChromaDB vector store powered by Google Gemini embeddings.
- **RAG Pipeline**: Advanced retrieval, mock re-ranking, and grounded generation with Gemini-1.5-flash.
- **Observability & Telemetry**: Logs every query, retrieved chunk, prompt, answer, token usage, and latency to PostgreSQL.
- **Hallucination Monitoring**: Detects when the model generates answers outside the context.
- **Evaluation Pipelines**: Automated golden-dataset testing using DeepEval.
- **Modern Dashboard**: Next.js 15, Tailwind CSS, shadcn/ui, Recharts.

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind, shadcn/ui
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, ChromaDB, Google Gemini, LangChain
- **Orchestration**: Docker & docker-compose

## Getting Started

1. Clone the repository and navigate to the root directory.
2. Copy `.env.example` to `.env` and add your Google Gemini API Key:
   ```bash
   cp .env.example .env
   ```
3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs
   - Telemetry Dashboard: http://localhost:3000/dashboard

## Folder Structure
- `/frontend`: Next.js application
- `/backend`: FastAPI service
  - `/api`: API endpoints (chat, ingest, telemetry)
  - `/rag`: Embeddings, chunking, retrieval, reranking, prompting logic
  - `/database`: DB models and connection
  - `/evaluations`: DeepEval evaluation pipelines
- `/docker`: Dockerfiles and compose configs

## Running Evaluations
```bash
cd backend
pip install -r requirements.txt
python -m evaluations.evaluate
```
