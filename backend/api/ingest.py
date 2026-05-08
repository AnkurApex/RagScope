import io
import uuid
from pypdf import PdfReader
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.schema import Document
from rag.ingest.document_processor import chunk_document
from rag.embeddings.chroma_store import get_collection

router = APIRouter()

# Max file size: 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

@router.post("/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Guard: filename can be None for programmatic uploads
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a valid filename")

    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    # Read all bytes upfront — safe for both TXT and PDF, avoids stream-position bugs
    file_bytes = await file.read()

    # Enforce file size limit
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB size limit")

    content = ""
    if file.filename.lower().endswith('.txt'):
        try:
            content = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback: try latin-1 which can decode any byte sequence
            content = file_bytes.decode('latin-1', errors='replace')

    elif file.filename.lower().endswith('.pdf'):
        try:
            # Use io.BytesIO so pypdf gets a proper seekable stream
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {str(e)}")

    if not content.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the file")

    # Chunking
    chunks = chunk_document(content)

    # Store in vector store
    collection = get_collection()

    doc_id = str(uuid.uuid4())
    chunk_ids = []
    texts = []
    metadatas = []

    for chunk in chunks:
        c_id = f"{doc_id}_{chunk['chunk_index']}"
        chunk_ids.append(c_id)
        texts.append(chunk['text'])
        metadatas.append({
            "source": file.filename,
            "document_id": doc_id,
            "chunk_index": chunk['chunk_index']
        })

    # Add to vector store (embeddings generated inside collection.add)
    try:
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=chunk_ids
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding/vector store error: {str(e)}")

    # Persist document metadata to SQLite
    db_doc = Document(
        id=doc_id,
        filename=file.filename,
        content=content,
        chunk_ids=chunk_ids,
        metadata_obj={"chunks_count": len(chunks)}
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return {"status": "success", "document_id": doc_id, "chunks_indexed": len(chunks)}
