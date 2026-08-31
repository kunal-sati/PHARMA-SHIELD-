import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Incident, Shipment
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(prefix="/incidents", tags=["Incident Management"])

@router.get("")
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    if not incidents:
        # Create baseline incident for PS-1026 if empty
        shipment = db.query(Shipment).filter_by(shipment_id="PS-1026").first()
        if shipment:
            inc = Incident(
                id="INC-PS1026-001",
                shipment_id="PS-1026",
                severity="CRITICAL",
                status="ACTION_REQUIRED",
                owner="Cold Chain Operations Center (Delhi Corridor)",
                sla_minutes=30,
                reason="Vaccine temperature excursion to 9.6°C (+1.6°C breach over safe max 8.0°C limit)."
            )
            db.add(inc)
            db.commit()
            db.refresh(inc)
            incidents = [inc]
    return incidents

@router.get("/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter_by(id=incident_id).first()
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc

@router.post("/{incident_id}/transition")
def transition_incident(incident_id: str, new_status: str, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter_by(id=incident_id).first()
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    old_status = inc.status
    inc.status = new_status
    inc.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()

    # Log Audit
    audit_agent.record_event(
        db=db,
        shipment_id=inc.shipment_id,
        correlation_id=f"CORR-{inc.shipment_id}-001",
        actor="OperationsCenter",
        actor_type="HUMAN_OPERATOR",
        agent="IncidentManager",
        event_type="INCIDENT_STATUS_TRANSITION",
        action=f"TRANSITION_{old_status}_TO_{new_status}",
        decision=new_status,
        status="SUCCESS",
        metadata_json={"incident_id": incident_id, "previous_status": old_status, "new_status": new_status}
    )

    return inc
