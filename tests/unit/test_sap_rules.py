import pytest
from backend.app.integrations.sap_governance import MockSAPGovernanceService, get_sap_governance_service

def test_sap_rule_1_temperature_excursion():
    service = MockSAPGovernanceService()
    # Normal temperature (4.0°C) -> No Rule 1 excursion
    res_normal = service.validate_recommendation(
        shipment_id="PS-1001",
        product_criticality="LOW",
        action="MONITOR_CLOSELY",
        estimated_cost=100.0,
        risk_score=20,
        current_temperature=4.0,
        min_temperature=2.0,
        max_temperature=8.0
    )
    assert not any("Rule 1" in r for r in res_normal.applicable_rules)

    # Excursion temperature (9.6°C > 8.0°C) -> Rule 1 excursion triggered
    res_excursion = service.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="REROUTE_TO_COLD_STORAGE",
        estimated_cost=2400.0,
        risk_score=91,
        current_temperature=9.6,
        min_temperature=2.0,
        max_temperature=8.0
    )
    assert any("Rule 1" in r for r in res_excursion.applicable_rules)

def test_sap_rule_2_critical_risk_score():
    service = MockSAPGovernanceService()
    res = service.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="MONITOR_CLOSELY",
        estimated_cost=100.0,
        risk_score=91
    )
    assert any("Rule 2" in r for r in res.applicable_rules)

def test_sap_rule_3_and_4_requires_human_approval():
    service = MockSAPGovernanceService()
    res = service.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="REROUTE_TO_COLD_STORAGE",
        estimated_cost=2400.0,
        risk_score=91,
        current_temperature=9.6
    )
    assert res.is_valid is True
    assert res.human_approval_required is True
    assert res.autonomous_execution_allowed is False
    assert any("Rule 3" in r for r in res.applicable_rules)
    assert any("Rule 4" in r for r in res.applicable_rules)

def test_sap_rule_5_unapproved_execution_blocked():
    service = MockSAPGovernanceService()
    permitted = service.verify_execution_permitted(
        approval_status="PENDING",
        action="REROUTE_TO_COLD_STORAGE"
    )
    assert permitted is False

    permitted_rejected = service.verify_execution_permitted(
        approval_status="REJECTED",
        action="REROUTE_TO_COLD_STORAGE"
    )
    assert permitted_rejected is False

def test_sap_rule_5_approved_execution_allowed():
    service = MockSAPGovernanceService()
    permitted = service.verify_execution_permitted(
        approval_status="APPROVED",
        action="REROUTE_TO_COLD_STORAGE"
    )
    assert permitted is True
