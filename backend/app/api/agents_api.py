from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, SensorReading, Disruption
from backend.app.agents.disruption_agent import disruption_agent
from backend.app.agents.planning_agent import planning_agent
from backend.app.agents.audit_agent import audit_agent
from backend.app.schemas.schemas import DisruptionDetectionResult, PlanningAgentOutput

router = APIRouter(prefix="/agents", tags=["Agent Pipelines"])

@router.post("/detect", response_model=DisruptionDetectionResult)
def trigger_disruption_agent(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    readings = db.query(SensorReading).filter_by(shipment_id=shipment_id).order_by(SensorReading.timestamp.asc()).all()
    temp_history = [r.temperature for r in readings] or [shipment.current_temperature]

    result = disruption_agent.analyze_telemetry(
        shipment_id=shipment.shipment_id,
        temperature=shipment.current_temperature,
        min_temp=shipment.min_temperature,
        max_temp=shipment.max_temperature,
        temp_history=temp_history,
        delay_minutes=shipment.delay_minutes,
        traffic_level=shipment.traffic_level,
        product_criticality=shipment.criticality
    )

    if result.disruption_detected:
        shipment.current_status = result.severity
        disruption_rec = Disruption(
            id=f"DIS-{shipment.shipment_id}",
            shipment_id=shipment.shipment_id,
            type=result.type,
            severity=result.severity,
            risk_score=result.risk_score,
            reason="; ".join(result.reasons)
        )
        db.add(disruption_rec)
        db.commit()

        # Record Audit
        audit_agent.record_event(
            db=db,
            shipment_id=shipment.shipment_id,
            correlation_id=f"CORR-{shipment.shipment_id}-001",
            actor="DisruptionSensingAgent",
            actor_type="AGENT",
            agent="DisruptionAgent",
            event_type="DISRUPTION_DETECTED",
            action="EVALUATE_TELEMETRY",
            decision=result.severity,
            status="SUCCESS",
            metadata_json={
                "risk_score": result.risk_score,
                "reasons": result.reasons,
                "temperature": shipment.current_temperature
            }
        )

    return result

@router.post("/plan", response_model=PlanningAgentOutput)
def trigger_planning_agent(shipment_id: str, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    disruption = db.query(Disruption).filter_by(shipment_id=shipment_id).first()
    risk_score = disruption.risk_score if disruption else 91

    output = planning_agent.generate_scenarios(
        shipment_id=shipment.shipment_id,
        product_name=shipment.product_name,
        current_temp=shipment.current_temperature,
        max_temp=shipment.max_temperature,
        delay_minutes=shipment.delay_minutes,
        traffic_level=shipment.traffic_level,
        risk_score=risk_score
    )

    # Record Audit
    audit_agent.record_event(
        db=db,
        shipment_id=shipment.shipment_id,
        correlation_id=f"CORR-{shipment.shipment_id}-001",
        actor="ScenarioPlanningAgent",
        actor_type="AGENT",
        agent="PlanningAgent",
        event_type="SCENARIOS_GENERATED",
        action="PLAN_RECOVERY",
        decision=output.recommended_scenario_id,
        status="SUCCESS",
        metadata_json={
            "scenarios_count": len(output.scenarios),
            "recommended": output.recommended_scenario_id,
            "confidence": output.confidence,
            "reason": output.reason
        }
    )

    return output
