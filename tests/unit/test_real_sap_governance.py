from backend.app.integrations.real_sap_governance import RealSAPGovernanceService

def test_real_sap_governance_fallback():
    # Test RealSAPGovernanceService fallback when endpoint is unreachable
    service = RealSAPGovernanceService(odata_url="https://invalid-sap-endpoint.s4hana.ondemand.com/odata")
    res = service.validate_recommendation(
        shipment_id="PS-1026",
        product_criticality="HIGH",
        action="REROUTE_TO_COLD_STORAGE",
        estimated_cost=2400.0,
        risk_score=91
    )
    assert res.is_valid is True
    assert res.human_approval_required is True
    assert res.autonomous_execution_allowed is False
    assert len(res.applicable_rules) >= 1

def test_real_sap_execution_lockout():
    service = RealSAPGovernanceService()
    assert service.verify_execution_permitted("PENDING", "REROUTE_TO_COLD_STORAGE") is False
    assert service.verify_execution_permitted("APPROVED", "REROUTE_TO_COLD_STORAGE") is True
