import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment, Disruption, Recommendation, Approval, SensorReading
from backend.app.services.simulation_service import SimulationService
from backend.app.agents.disruption_agent import disruption_agent
from backend.app.agents.planning_agent import planning_agent
from backend.app.integrations.sap_governance import sap_governance
from backend.app.agents.audit_agent import audit_agent

router = APIRouter(prefix="/demo", tags=["Hackathon Demo Mode"])

@router.post("/reset")
def demo_reset(db: Session = Depends(get_db)):
    reset_shipment = SimulationService.reset_scenario(db, "PS-1026")
    return {"status": "SUCCESS", "message": "Demo scenario reset to baseline", "shipment": reset_shipment.shipment_id}

@router.post("/run-vaccine-excursion")
def run_vaccine_excursion(db: Session = Depends(get_db)):
    shipment_id = "PS-1026"
    correlation_id = f"CORR-{shipment_id}-001"

    # Step 1: Reset Baseline
    SimulationService.reset_scenario(db, shipment_id)
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()

    # Step 2: Simulate Excursion (Temp 9.6°C)
    now = datetime.datetime.now(datetime.timezone.utc)
    for i, temp in enumerate(SimulationService.EXCURSION_TEMPS):
        reading = SensorReading(
            id=f"SR-DEMO-{uuid.uuid4().hex[:6].upper()}",
            shipment_id=shipment_id,
            timestamp=now + datetime.timedelta(seconds=i),
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

    # Step 3: Disruption Sensing Agent
    disruption_res = disruption_agent.analyze_telemetry(
        shipment_id=shipment_id,
        temperature=9.6,
        min_temp=2.0,
        max_temp=8.0,
        temp_history=SimulationService.EXCURSION_TEMPS,
        delay_minutes=47,
        traffic_level="HIGH",
        product_criticality="HIGH"
    )

    disruption_record = Disruption(
        id=f"DIS-{shipment_id}",
        shipment_id=shipment_id,
        type=disruption_res.type,
        severity=disruption_res.severity,
        risk_score=disruption_res.risk_score,
        reason="; ".join(disruption_res.reasons)
    )
    db.add(disruption_record)

    audit_agent.record_event(
        db=db, shipment_id=shipment_id, correlation_id=correlation_id,
        actor="DisruptionSensingAgent", actor_type="AGENT", agent="DisruptionAgent",
        event_type="DISRUPTION_DETECTED", action="DETECT_EXCURSION", decision="CRITICAL",
        status="SUCCESS", metadata_json={"risk_score": disruption_res.risk_score, "reasons": disruption_res.reasons}
    )

    # Step 4: Scenario Planning Agent
    plan_res = planning_agent.generate_scenarios(
        shipment_id=shipment_id, product_name="Vaccine", current_temp=9.6, max_temp=8.0,
        delay_minutes=47, traffic_level="HIGH", risk_score=disruption_res.risk_score
    )

    rec_opt = next(s for s in plan_res.scenarios if s.id == plan_res.recommended_scenario_id)
    recommendation_record = Recommendation(
        id=f"REC-{shipment_id}",
        shipment_id=shipment_id,
        scenario_id=rec_opt.id,
        action=rec_opt.action,
        estimated_cost=rec_opt.estimated_cost,
        estimated_time_minutes=rec_opt.estimated_time_minutes,
        risk_level=rec_opt.risk_level,
        risk_reduction=rec_opt.risk_reduction,
        confidence=plan_res.confidence,
        reasoning=plan_res.reason
    )
    db.add(recommendation_record)

    audit_agent.record_event(
        db=db, shipment_id=shipment_id, correlation_id=correlation_id,
        actor="ScenarioPlanningAgent", actor_type="AGENT", agent="PlanningAgent",
        event_type="RECOMMENDATION_RANKED", action="RANK_SCENARIOS", decision=rec_opt.action,
        status="SUCCESS", metadata_json={"recommended_action": rec_opt.action, "cost": rec_opt.estimated_cost}
    )

    # Step 5: SAP Governance Check
    sap_val = sap_governance.validate_recommendation(
        shipment_id=shipment_id, product_criticality="HIGH", action=rec_opt.action,
        estimated_cost=rec_opt.estimated_cost, risk_score=disruption_res.risk_score
    )

    approval_id = f"APP-{shipment_id}"
    approval_record = Approval(
        id=approval_id,
        shipment_id=shipment_id,
        recommendation_id=recommendation_record.id,
        status="PENDING",
        comments="SAP Governance: High Criticality & High Cost action requires Human Approval."
    )
    db.add(approval_record)
    shipment.current_status = "AWAITING_APPROVAL"

    audit_agent.record_event(
        db=db, shipment_id=shipment_id, correlation_id=correlation_id,
        actor="SAPGovernanceAdapter", actor_type="SYSTEM", agent="SAPGovernance",
        event_type="SAP_POLICY_EVALUATED", action="VALIDATE_RULES", decision="AWAITING_APPROVAL",
        status="SUCCESS", metadata_json={"applied_rules": sap_val.applicable_rules}
    )

    db.commit()

    return {
        "status": "SUCCESS",
        "shipment_id": shipment_id,
        "current_status": "AWAITING_APPROVAL",
        "temperature": 9.6,
        "risk_score": disruption_res.risk_score,
        "recommendation": rec_opt.action,
        "approval_id": approval_id,
        "message": "Vaccine excursion primary demo pipeline triggered successfully up to AWAITING_APPROVAL."
    }
