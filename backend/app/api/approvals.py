import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.security import require_role
from backend.app.models.entities import Approval, Shipment, Recommendation
from backend.app.schemas.schemas import ApprovalResponse, ApprovalActionRequest
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.get("/pending", response_model=list[ApprovalResponse])
def get_pending_approvals(db: Session = Depends(get_db)):
    approvals = db.query(Approval).filter_by(status="PENDING").all()
    return approvals

@router.post("/{approval_id}/approve", response_model=ApprovalResponse)
def approve_recommendation(
    approval_id: str,
    payload: ApprovalActionRequest,
    current_user: dict = Depends(require_role(["MANAGER", "ADMIN"])),
    db: Session = Depends(get_db)
):
    approval = db.query(Approval).filter_by(id=approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval request not found")

    if approval.status != "PENDING":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Approval already processed with status: {approval.status}")

    approval.status = "APPROVED"
    approval.approved_at = datetime.datetime.now(datetime.timezone.utc)
    approval.approved_by = current_user.get("name", "Manager Sarah Connor")
    approval.comments = payload.comments or "Approved cold storage rerouting."

    shipment = db.query(Shipment).filter_by(shipment_id=approval.shipment_id).first()
    if shipment:
        shipment.current_status = "APPROVED"

    db.commit()
    db.refresh(approval)

    # Audit Logging
    audit_agent.record_event(
        db=db,
        shipment_id=approval.shipment_id,
        correlation_id=f"CORR-{approval.shipment_id}-001",
        actor=current_user.get("name", "Manager Sarah Connor"),
        actor_type="HUMAN_MANAGER",
        agent="ApprovalCenter",
        event_type="HUMAN_APPROVAL_GRANTED",
        action="APPROVE_RECOVERY",
        decision="APPROVED",
        status="SUCCESS",
        metadata_json={
            "approval_id": approval_id,
            "approved_by": approval.approved_by,
            "comments": approval.comments
        }
    )

    return approval

@router.post("/{approval_id}/reject", response_model=ApprovalResponse)
def reject_recommendation(
    approval_id: str,
    payload: ApprovalActionRequest,
    current_user: dict = Depends(require_role(["MANAGER", "ADMIN"])),
    db: Session = Depends(get_db)
):
    approval = db.query(Approval).filter_by(id=approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval request not found")

    if approval.status != "PENDING":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Approval already processed with status: {approval.status}")

    approval.status = "REJECTED"
    approval.approved_at = datetime.datetime.now(datetime.timezone.utc)
    approval.approved_by = current_user.get("name", "Manager Sarah Connor")
    approval.comments = payload.comments or "Rejected recommendation."

    shipment = db.query(Shipment).filter_by(shipment_id=approval.shipment_id).first()
    if shipment:
        shipment.current_status = "REJECTED"

    db.commit()
    db.refresh(approval)

    # Audit Logging
    audit_agent.record_event(
        db=db,
        shipment_id=approval.shipment_id,
        correlation_id=f"CORR-{approval.shipment_id}-001",
        actor=current_user.get("name", "Manager Sarah Connor"),
        actor_type="HUMAN_MANAGER",
        agent="ApprovalCenter",
        event_type="HUMAN_APPROVAL_REJECTED",
        action="REJECT_RECOVERY",
        decision="REJECTED",
        status="SUCCESS",
        metadata_json={
            "approval_id": approval_id,
            "approved_by": approval.approved_by,
            "comments": approval.comments
        }
    )

    return approval
