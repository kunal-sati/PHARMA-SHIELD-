from backend.app.core.pre_shipment import PreShipmentRiskEngine

def test_pre_shipment_high_risk():
    res = PreShipmentRiskEngine.evaluate_pre_shipment(
        product_criticality="HIGH",
        supplier_reliability=85.0,
        route_risk_score=40,
        traffic_level="HIGH"
    )
    assert res["risk_tier"] == "HIGH"
    assert "REVIEW_REQUIRED" in res["recommendation"]

def test_pre_shipment_low_risk():
    res = PreShipmentRiskEngine.evaluate_pre_shipment(
        product_criticality="LOW",
        supplier_reliability=99.5,
        route_risk_score=5,
        traffic_level="NORMAL"
    )
    assert res["risk_tier"] == "LOW"
    assert "SAFE_TO_DISPATCH" in res["recommendation"]
