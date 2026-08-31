from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.app.core.database import get_db
from backend.app.core.rag_engine import RAGEngine

router = APIRouter(prefix="/knowledge", tags=["Knowledge & SOP RAG Engine"])

class RAGSearchRequest(BaseModel):
    query: str
    product_category: str = "Vaccine"

@router.post("/search")
def search_knowledge_and_incidents(req: RAGSearchRequest, db: Session = Depends(get_db)):
    incidents = RAGEngine.search_similar_incidents(db, req.query, req.product_category)
    sops = RAGEngine.search_knowledge_sops(db, req.query)
    
    return {
        "query": req.query,
        "historical_incidents_found": len(incidents),
        "similar_incidents": incidents,
        "sop_documents_found": len(sops),
        "sop_citations": sops
    }
