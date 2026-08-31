from backend.app.core.risk_engine import RiskEngine

def test_normal_temperature_risk():
    res = RiskEngine.calculate_risk(
        current_temp=4.5,
        min_temp=2.0,
        max_temp=8.0,
        temp_history=[4.2, 4.4, 4.5],
        product_criticality="HIGH",
        delay_minutes=0,
        traffic_level="NORMAL"
    )
    assert res["risk_score"] < 40
    assert res["severity"] in ["LOW", "MEDIUM"]

def test_excursion_critical_risk():
    res = RiskEngine.calculate_risk(
        current_temp=9.6,
        min_temp=2.0,
        max_temp=8.0,
        temp_history=[5.2, 6.1, 7.3, 8.1, 8.9, 9.6],
        product_criticality="HIGH",
        delay_minutes=47,
        traffic_level="HIGH"
    )
    assert res["risk_score"] >= 80
    assert res["severity"] == "CRITICAL"
