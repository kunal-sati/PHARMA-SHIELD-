from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, SensorReading, Disruption
from backend.app.core.digital_twin import DigitalTwinEngine

router = APIRouter(prefix="/shipments", tags=["Digital Twin & Telemetry"])

@router.get("/{shipment_id}/digital-twin")
def get_digital_twin(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    readings = db.query(SensorReading).filter_by(shipment_id=shipment_id).order_by(SensorReading.timestamp.asc()).all()
    temp_history = [r.temperature for r in readings] or [shipment.current_temperature]

    disruption = db.query(Disruption).filter_by(shipment_id=shipment_id).first()
    current_risk = disruption.risk_score if disruption else 91

    twin_metrics = DigitalTwinEngine.compute_digital_twin(
        current_temp=shipment.current_temperature,
        min_temp=shipment.min_temperature,
        max_temp=shipment.max_temperature,
        temp_history=temp_history,
        delay_minutes=shipment.delay_minutes,
        traffic_level=shipment.traffic_level,
        product_criticality=shipment.criticality,
        current_risk_score=current_risk
    )

    return {
        "shipment_id": shipment.shipment_id,
        "product_name": shipment.product_name,
        "product_type": shipment.product_type,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "criticality": shipment.criticality,
        "current_status": shipment.current_status,
        "coordinates": {
            "latitude": shipment.current_latitude,
            "longitude": shipment.current_longitude
        },
        "digital_twin": twin_metrics
    }
