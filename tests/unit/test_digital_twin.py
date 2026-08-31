from backend.app.core.digital_twin import DigitalTwinEngine

def test_digital_twin_predictive_risk():
    res = DigitalTwinEngine.compute_digital_twin(
        current_temp=9.6,
        min_temp=2.0,
        max_temp=8.0,
        temp_history=[5.2, 6.1, 7.3, 8.1, 8.9, 9.6],
        delay_minutes=47,
        traffic_level="HIGH",
        product_criticality="HIGH",
        current_risk_score=91
    )
    assert res["current_temperature"] == 9.6
    assert res["temperature_trend"] == "RISING_RAPIDLY"
    assert res["projected_risk_score"] >= 94
    assert res["estimated_time_to_critical_minutes"] > 0
    assert res["product_health_pct"] < 90.0
