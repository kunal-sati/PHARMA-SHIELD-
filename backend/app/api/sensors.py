import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, SensorReading
from backend.app.schemas.schemas import SensorReadingCreate, SensorReadingResponse

router = APIRouter(tags=["Sensors"])

@router.post("/sensors/readings", response_model=SensorReadingResponse, status_code=status.HTTP_201_CREATED)
def post_sensor_reading(reading_in: SensorReadingCreate, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=reading_in.shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    reading = SensorReading(
        id=f"SR-{uuid.uuid4().hex[:8].upper()}",
        shipment_id=reading_in.shipment_id,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        temperature=reading_in.temperature,
        humidity=reading_in.humidity,
        latitude=reading_in.latitude,
        longitude=reading_in.longitude,
        speed=reading_in.speed,
        traffic_level=reading_in.traffic_level
    )

    shipment.current_temperature = reading_in.temperature
    shipment.current_latitude = reading_in.latitude
    shipment.current_longitude = reading_in.longitude
    shipment.traffic_level = reading_in.traffic_level

    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

@router.get("/shipments/{shipment_id}/readings", response_model=list[SensorReadingResponse])
def get_sensor_readings(shipment_id: str, db: Session = Depends(get_db)):
    readings = db.query(SensorReading).filter_by(shipment_id=shipment_id).order_by(SensorReading.timestamp.asc()).all()
    return readings
