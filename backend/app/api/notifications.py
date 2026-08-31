import uuid
import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Notification

router = APIRouter(prefix="/notifications", tags=["In-App Notifications"])

@router.get("")
def get_notifications(db: Session = Depends(get_db)):
    notes = db.query(Notification).order_by(Notification.created_at.desc()).all()
    if not notes:
        n1 = Notification(
            id=f"NOT-{uuid.uuid4().hex[:6].upper()}",
            type="CRITICAL_ALERT",
            title="Temperature Excursion on PS-1026",
            message="Vaccine temperature reached 9.6°C (+1.6°C breach over safe max 8.0°C limit).",
            shipment_id="PS-1026"
        )
        n2 = Notification(
            id=f"NOT-{uuid.uuid4().hex[:6].upper()}",
            type="APPROVAL_REQUIRED",
            title="Manager Sign-off Mandatory",
            message="ABAP Rules 3 & 4 enforce Manager approval for cold storage rerouting (₹2,400 / 23m ETA).",
            shipment_id="PS-1026"
        )
        db.add_all([n1, n2])
        db.commit()
        notes = [n1, n2]
    return notes

@router.post("/{notification_id}/read")
def mark_notification_read(notification_id: str, db: Session = Depends(get_db)):
    note = db.query(Notification).filter_by(id=notification_id).first()
    if note:
        note.is_read = True
        db.commit()
    return {"status": "SUCCESS"}
