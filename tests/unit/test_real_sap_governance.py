import pytest
import httpx
from unittest.mock import patch, MagicMock
from backend.app.integrations.real_sap_governance import RealSAPGovernanceService, SAPIntegrationError
from backend.app.integrations.sap_governance import get_sap_governance_service, MockSAPGovernanceService

def test_real_sap_governance_unreachable_raises_explicit_error():
    """
    Phase 6 Requirement: In REAL mode, unreachable SAP BTP MUST raise SAPIntegrationError.
    It MUST NEVER silently fall back to MOCK.
    """
    service = RealSAPGovernanceService(
        odata_url="https://invalid-nonexistent-sap-host-12345.s4hana.ondemand.com/odata"
    )
    with pytest.raises(SAPIntegrationError) as exc_info:
        service.validate_recommendation(
            shipment_id="PS-1026",
            product_criticality="HIGH",
            action="REROUTE_TO_COLD_STORAGE",
            estimated_cost=2400.0,
            risk_score=91,
            current_temperature=9.6
        )
    assert "unreachable" in str(exc_info.value).lower() or "failed" in str(exc_info.value).lower()

def test_real_sap_execution_lockout():
    """Test Rule 5 enforcement in RealSAPGovernanceService."""
    service = RealSAPGovernanceService()
    assert service.verify_execution_permitted("PENDING", "REROUTE_TO_COLD_STORAGE") is False
    assert service.verify_execution_permitted("REJECTED", "REROUTE_TO_COLD_STORAGE") is False
    assert service.verify_execution_permitted("APPROVED", "REROUTE_TO_COLD_STORAGE") is True
    # Low impact action can proceed without prior human approval
    assert service.verify_execution_permitted("PENDING", "MONITOR_CLOSELY") is True

def test_real_sap_successful_odata_response():
    """Test RealSAPGovernanceService successfully parsing standard OData V4 response."""
    service = RealSAPGovernanceService(
        odata_url="https://mock-live-sap-btp.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "isValid": True,
        "humanApprovalRequired": True,
        "autonomousExecutionAllowed": False,
        "applicableRules": [
            "Real SAP HANA ABAP Rule 1: Cold Chain Temperature Envelope Excursion (9.6°C > 8.0°C)",
            "Real SAP HANA ABAP Rule 2: Critical Risk Score 91 >= 80",
            "Real SAP HANA ABAP Rule 3: High Cost (₹2400) / Impact Rerouting Approval Mandatory"
        ]
    }

    with patch.object(httpx.Client, "post", return_value=mock_response):
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
        assert len(res.applicable_rules) == 3
        assert "Real SAP" in res.message

def test_sap_mode_factory_selection(monkeypatch):
    """Test get_sap_governance_service creates correct class based on SAP_MODE."""
    monkeypatch.setenv("SAP_MODE", "MOCK")
    mock_svc = get_sap_governance_service()
    assert isinstance(mock_svc, MockSAPGovernanceService)

    monkeypatch.setenv("SAP_MODE", "REAL")
    real_svc = get_sap_governance_service()
    assert isinstance(real_svc, RealSAPGovernanceService)
