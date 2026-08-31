from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import AuditLog
from backend.app.schemas.schemas import AuditLogResponse
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(tags=["Audit & Compliance"])

@router.get("/audit", response_model=list[AuditLogResponse])
def get_audit_logs(
    shipment_id: Optional[str] = None,
    event_type: Optional[str] = None,
    actor: Optional[str] = None,
    agent: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if shipment_id:
        query = query.filter(AuditLog.shipment_id == shipment_id)
    if event_type:
        query = query.filter(AuditLog.event_type == event_type)
    if actor:
        query = query.filter(AuditLog.actor == actor)
    if agent:
        query = query.filter(AuditLog.agent == agent)

    logs = query.order_by(AuditLog.timestamp.desc()).all()
    return logs

@router.get("/audit/verify")
def verify_audit_integrity(db: Session = Depends(get_db)):
    """
    Phase N Cryptographic Audit Chain Integrity Verification Endpoint.
    Validates SHA-256 hash chaining across all historical records.
    """
    res = audit_agent.verify_audit_chain_integrity(db)
    return res

@router.get("/shipments/{shipment_id}/audit", response_model=list[AuditLogResponse])
def get_shipment_audit_logs(shipment_id: str, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).filter_by(shipment_id=shipment_id).order_by(AuditLog.timestamp.asc()).all()
    return logs
