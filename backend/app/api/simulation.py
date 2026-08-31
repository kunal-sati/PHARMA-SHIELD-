import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, SensorReading
from backend.app.services.simulation_service import SimulationService
from backend.app.agents.disruption_agent import disruption_agent
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(prefix="/simulation", tags=["Simulation Engine"])

@router.post("/start")
def start_simulation(shipment_id: str = "PS-1026", db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    shipment.current_status = "NORMAL"
    shipment.current_temperature = 4.4
    db.commit()
    return {"message": f"Simulation started in NORMAL mode for shipment '{shipment_id}'", "temperature": 4.4}

@router.post("/temperature-excursion")
def trigger_temperature_excursion(shipment_id: str = "PS-1026", db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    # Stepwise temperature rise simulating real excursion telemetry: 5.2, 6.1, 7.3, 8.1, 8.9, 9.6
    now = datetime.datetime.now(datetime.timezone.utc)
    for i, temp in enumerate(SimulationService.EXCURSION_TEMPS):
        reading = SensorReading(
            id=f"SR-EXC-{uuid.uuid4().hex[:6].upper()}",
            shipment_id=shipment_id,
            timestamp=now + datetime.timedelta(seconds=i * 2),
            temperature=temp,
            humidity=58.0,
            latitude=28.7041 + (i * 0.005),
            longitude=77.1025 + (i * 0.005),
            speed=35.0,
            traffic_level="HIGH"
        )
        db.add(reading)

    shipment.current_temperature = 9.6
    shipment.current_status = "CRITICAL"
    db.commit()

    # Trigger Disruption Agent
    disruption_res = disruption_agent.analyze_telemetry(
        shipment_id=shipment.shipment_id,
        temperature=9.6,
        min_temp=shipment.min_temperature,
        max_temp=shipment.max_temperature,
        temp_history=SimulationService.EXCURSION_TEMPS,
        delay_minutes=shipment.delay_minutes,
        traffic_level=shipment.traffic_level,
        product_criticality=shipment.criticality
    )

    # Log Audit
    audit_agent.record_event(
        db=db,
        shipment_id=shipment_id,
        correlation_id=f"CORR-{shipment_id}-001",
        actor="SimulationEngine",
        actor_type="SYSTEM",
        agent="Simulator",
        event_type="EXCURSION_SIMULATED",
        action="TRIGGER_EXCURSION",
        decision="CRITICAL_EXCURSION_ACTIVE",
        status="SUCCESS",
        metadata_json={"peak_temperature": 9.6, "risk_score": disruption_res.risk_score}
    )

    return {
        "message": f"Temperature excursion triggered for '{shipment_id}'",
        "current_temperature": 9.6,
        "status": "CRITICAL",
        "risk_score": disruption_res.risk_score
    }

@router.post("/reset")
def reset_simulation(shipment_id: str = "PS-1026", db: Session = Depends(get_db)):
    reset_shipment = SimulationService.reset_scenario(db, shipment_id)
    return {"message": f"Scenario reset complete for '{shipment_id}'", "status": reset_shipment.current_status}
