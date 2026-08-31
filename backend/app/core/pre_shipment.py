from typing import Dict, Any

class PreShipmentRiskEngine:
    """
    Feature 12: Pre-Shipment Proactive Risk Assessment Engine.
    Evaluates product, route risk, supplier reliability, facility status, and traffic before dispatch.
    """

    @classmethod
    def evaluate_pre_shipment(
        cls,
        product_criticality: str,
        supplier_reliability: float,
        route_risk_score: int,
        traffic_level: str
    ) -> Dict[str, Any]:

        risk_score = int(round((100.0 - supplier_reliability) * 1.5 + route_risk_score * 0.8))
        if product_criticality.upper() == "HIGH":
            risk_score += 15
        if traffic_level.upper() == "HIGH":
            risk_score += 10

        risk_score = max(0, min(100, risk_score))

        if risk_score >= 60:
            tier = "HIGH"
            rec = "REVIEW_REQUIRED (Select alternate low-congestion route or buffer vehicle)"
        elif risk_score >= 35:
            tier = "MEDIUM"
            rec = "SAFE_TO_DISPATCH (Monitor NH-44 traffic corridor closely)"
        else:
            tier = "LOW"
            rec = "SAFE_TO_DISPATCH (Optimal cold chain parameters verified)"

        return {
            "pre_shipment_risk_score": risk_score,
            "risk_tier": tier,
            "recommendation": rec,
            "contributing_factors": [
                f"Product Criticality: {product_criticality}",
                f"Supplier Reliability: {supplier_reliability}%",
                f"Historical Route Risk: {route_risk_score}/100",
                f"Predicted Traffic Level: {traffic_level}"
            ]
        }
