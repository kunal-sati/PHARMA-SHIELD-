import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.integrations.sap_governance import MockSAPGovernanceService
from backend.app.agents.execution_agent import ExecutionAgent
from backend.app.agents.audit_agent import audit_agent
from backend.app.core.state_machine import ShipmentState

def test_ps1026_full_governed_lifecycle():
    """
    Phase 11: PS-1026 End-to-End Governance & Execution Scenario
    Shipment: PS-1026
    Temperature: 9.6°C
    Risk Score: 91
    Action: REROUTE_TO_COLD_STORAGE
    Cost: ₹2400.00
    Criticality: HIGH
    """
    # 1. Evaluate SAP Governance Rules
    sap_service = MockSAPGovernanceService()
    val_res = sap_service.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="REROUTE_TO_COLD_STORAGE",
        estimated_cost=2400.0,
        risk_score=91,
        current_temperature=9.6,
        min_temperature=2.0,
        max_temperature=8.0
    )

    # Assert all four governance policy triggers
    assert val_res.is_valid is True
    assert val_res.human_approval_required is True
    assert val_res.autonomous_execution_allowed is False
    assert any("Rule 1" in r for r in val_res.applicable_rules), "Temperature excursion not flagged"
    assert any("Rule 2" in r for r in val_res.applicable_rules), "Critical risk not flagged"
    assert any("Rule 3" in r for r in val_res.applicable_rules), "High criticality + cost not flagged"
    assert any("Rule 4" in r for r in val_res.applicable_rules), "High impact action not flagged"

    # 2. Verify Execution Lockout Before Human Approval
    exec_agent = ExecutionAgent()
    with pytest.raises(PermissionError) as exc_info:
        exec_agent.execute_recovery(
            current_state=ShipmentState.AWAITING_APPROVAL,
            approval_status="PENDING",
            action="REROUTE_TO_COLD_STORAGE",
            shipment_id="PS-1026"
        )
    assert "Execution Prohibited by SAP Governance" in str(exc_info.value)

    # 3. Manager Approval Granted -> Execution Allowed
    exec_result = exec_agent.execute_recovery(
        current_state=ShipmentState.AWAITING_APPROVAL,
        approval_status="APPROVED",
        action="REROUTE_TO_COLD_STORAGE",
        shipment_id="PS-1026"
    )
    assert exec_result["success"] is True
    assert exec_result["new_state"] == ShipmentState.APPROVED
    assert exec_result["action_executed"] == "REROUTE_TO_COLD_STORAGE"
    assert exec_result["distance_km"] == 8.4

    # 4. Record Audit Chain Event
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    log_entry = audit_agent.record_event(
        db=db,
        shipment_id="PS-1026",
        correlation_id="CORR-PS1026-001",
        actor="SAPGovernanceAdapter",
        actor_type="SYSTEM",
        agent="SAPGovernance",
        event_type="SAP_POLICY_EVALUATED",
        action="VALIDATE_RULES",
        decision="AWAITING_APPROVAL",
        status="SUCCESS",
        metadata_json={
            "rules": val_res.applicable_rules,
            "cost": 2400.0,
            "risk_score": 91
        }
    )
    assert log_entry.current_event_hash is not None
    integrity = audit_agent.verify_audit_chain_integrity(db)
    assert integrity["status"] == "VALID"
    assert integrity["verified_records"] == 1
