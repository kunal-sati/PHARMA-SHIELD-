import math
from typing import Dict, Any

class DigitalTwinEngine:
    """
    PharmaShield Live Shipment Digital Twin Engine.
    Computes real-time telemetry, predictive risk projections,
    estimated time to critical, and prototype product health exposure index.
    """

    @classmethod
    def compute_digital_twin(
        cls,
        current_temp: float,
        min_temp: float,
        max_temp: float,
        temp_history: list[float],
        delay_minutes: int,
        traffic_level: str,
        product_criticality: str,
        current_risk_score: int
    ) -> Dict[str, Any]:

        # 1. Temperature Trend Calculation
        if len(temp_history) >= 2:
            delta = temp_history[-1] - temp_history[0]
            if delta > 0.5:
                trend = "RISING_RAPIDLY"
                rate_per_min = delta / max(1, len(temp_history))
            elif delta > 0.1:
                trend = "RISING"
                rate_per_min = delta / max(1, len(temp_history))
            elif delta < -0.1:
                trend = "FALLING"
                rate_per_min = delta / max(1, len(temp_history))
            else:
                trend = "STABLE"
                rate_per_min = 0.0
        else:
            trend = "STABLE"
            rate_per_min = 0.0

        # 2. Predictive Projected Risk Calculation (Phase D)
        if current_temp > max_temp:
            excursion_gap = current_temp - max_temp
            # Projected risk rises faster if trend is rising rapidly
            trend_multiplier = 1.3 if trend == "RISING_RAPIDLY" else (1.1 if trend == "RISING" else 1.0)
            projected_risk = int(min(100, current_risk_score * trend_multiplier + (excursion_gap * 5)))
            
            # Time to Critical calculation
            time_to_critical = max(5, int(round((10.0 - current_temp) / max(0.05, rate_per_min)))) if rate_per_min > 0 else 18
        else:
            projected_risk = current_risk_score
            time_to_critical = 120

        # 3. Transparent Product Health Prototype Indicator (Phase E)
        # Note: Non-medical prototype exposure index
        if current_temp > max_temp:
            exposure_penalty = min(60.0, (current_temp - max_temp) * 20.0 + (delay_minutes * 0.3))
            health_pct = round(max(20.0, 100.0 - exposure_penalty), 1)
        else:
            health_pct = 98.5

        health_factors = []
        if current_temp > max_temp:
            health_factors.append(f"Thermal breach of +{round(current_temp - max_temp, 2)}°C above safe limit ({max_temp}°C)")
        if delay_minutes > 20:
            health_factors.append(f"Transit delay of {delay_minutes} minutes in {traffic_level} traffic")
        if not health_factors:
            health_factors.append("Optimal thermal stability maintained inside 2°C–8°C safe zone")

        return {
            "current_temperature": current_temp,
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "temperature_trend": trend,
            "temperature_rate_per_min": round(rate_per_min, 3),
            "humidity_pct": 58.0,
            "current_risk_score": current_risk_score,
            "projected_risk_score": projected_risk,
            "estimated_time_to_critical_minutes": time_to_critical,
            "product_health_pct": health_pct,
            "product_health_disclaimer": "PROTOTYPE RISK INDICATOR: Non-medical, non-validated exposure score for hackathon demonstration purposes.",
            "product_health_factors": health_factors
        }
