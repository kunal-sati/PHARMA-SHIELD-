from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment
from backend.app.schemas.schemas import ShipmentCreate, ShipmentResponse

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.get("", response_model=list[ShipmentResponse])
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments

@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment_by_id(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_44_NOT_FOUND, detail=f"Shipment '{shipment_id}' not found")
    return shipment

@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(payload: ShipmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Shipment).filter_by(shipment_id=payload.shipment_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Shipment ID already exists")

    shipment = Shipment(
        shipment_id=payload.shipment_id,
        product_name=payload.product_name,
        product_type=payload.product_type,
        origin=payload.origin,
        destination=payload.destination,
        min_temperature=payload.min_temperature,
        max_temperature=payload.max_temperature,
        criticality=payload.criticality,
        current_status="NORMAL",
        current_temperature=payload.current_temperature,
        current_latitude=payload.current_latitude,
        current_longitude=payload.current_longitude,
        delay_minutes=payload.delay_minutes,
        traffic_level=payload.traffic_level
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment
