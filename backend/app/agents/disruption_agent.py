from backend.app.core.risk_engine import RiskEngine
from backend.app.schemas.schemas import DisruptionDetectionResult

class DisruptionSensingAgent:
    """
    Agent 1: Monitors sensor telemetry, calculates risk deterministically,
    and produces structured disruption events.
    """

    def analyze_telemetry(
        self,
        shipment_id: str,
        temperature: float,
        min_temp: float,
        max_temp: float,
        temp_history: list[float],
        delay_minutes: int,
        traffic_level: str,
        product_criticality: str
    ) -> DisruptionDetectionResult:

        # 1. Deterministic threshold breach evaluation
        temp_excursion = (temperature > max_temp) or (temperature < min_temp)

        # 2. Risk Engine calculation
        risk_result = RiskEngine.calculate_risk(
            current_temp=temperature,
            min_temp=min_temp,
            max_temp=max_temp,
            temp_history=temp_history,
            product_criticality=product_criticality,
            delay_minutes=delay_minutes,
            traffic_level=traffic_level
        )

        risk_score = risk_result["risk_score"]
        severity = risk_result["severity"]
        reasons = risk_result["reasons"]

        disruption_detected = temp_excursion or (risk_score >= 60)

        disruption_type = "TEMPERATURE_EXCURSION" if temp_excursion else ("ROUTE_DELAY" if delay_minutes > 30 else "NONE")

        return DisruptionDetectionResult(
            disruption_detected=disruption_detected,
            type=disruption_type,
            severity=severity,
            risk_score=risk_score,
            confidence=0.98,
            reasons=reasons
        )

disruption_agent = DisruptionSensingAgent()
