from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, Approval, Recommendation
from backend.app.agents.execution_agent import execution_agent
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(prefix="/execution", tags=["Execution Engine"])

@router.post("/{shipment_id}")
def execute_shipment_recovery(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    approval = db.query(Approval).filter_by(shipment_id=shipment_id).order_by(Approval.requested_at.desc()).first()
    approval_status = approval.status if approval else "NONE"

    recommendation = db.query(Recommendation).filter_by(shipment_id=shipment_id).first()
    action = recommendation.action if recommendation else "REROUTE_TO_COLD_STORAGE"

    try:
        exec_result = execution_agent.execute_recovery(
            current_state=shipment.current_status,
            approval_status=approval_status,
            action=action,
            shipment_id=shipment_id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    # Update shipment state to RECOVERING then RECOVERED
    shipment.current_status = "RECOVERED"
    shipment.current_temperature = 4.5
    shipment.current_latitude = exec_result["simulated_latitude"]
    shipment.current_longitude = exec_result["simulated_longitude"]
    shipment.delay_minutes = 23
    shipment.traffic_level = "NORMAL"

    db.commit()
    db.refresh(shipment)

    # Audit Logging
    audit_agent.record_event(
        db=db,
        shipment_id=shipment_id,
        correlation_id=f"CORR-{shipment_id}-001",
        actor="ExecutionAgent",
        actor_type="AGENT",
        agent="ExecutionAgent",
        event_type="RECOVERY_EXECUTED",
        action=action,
        decision="RECOVERED",
        status="SUCCESS",
        metadata_json=exec_result
    )

    return exec_result
