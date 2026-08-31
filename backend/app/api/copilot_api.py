from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.copilot import ResilienceCopilotEngine

router = APIRouter(prefix="/copilot", tags=["Resilience Copilot Assistant"])

class CopilotQueryRequest(BaseModel):
    query: str
    shipment_id: str = "PS-1026"

@router.post("/query")
def ask_copilot(req: CopilotQueryRequest, db: Session = Depends(get_db)):
    return ResilienceCopilotEngine.process_query(db, req.query, req.shipment_id)
