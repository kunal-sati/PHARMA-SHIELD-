from backend.app.integrations.sap_governance import sap_governance

def test_sap_rule_3_and_4_requires_human_approval():
    res = sap_governance.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="REROUTE_TO_COLD_STORAGE",
        estimated_cost=2400.0,
        risk_score=91
    )
    assert res.is_valid is True
    assert res.human_approval_required is True
    assert res.autonomous_execution_allowed is False
    assert any("Rule 3" in r for r in res.applicable_rules)

def test_sap_rule_5_unapproved_execution_blocked():
    permitted = sap_governance.verify_execution_permitted(
        approval_status="PENDING",
        action="REROUTE_TO_COLD_STORAGE"
    )
    assert permitted is False

def test_sap_rule_5_approved_execution_allowed():
    permitted = sap_governance.verify_execution_permitted(
        approval_status="APPROVED",
        action="REROUTE_TO_COLD_STORAGE"
    )
    assert permitted is True
