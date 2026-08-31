from typing import Dict, Any

class RiskPolicyConfig:
    MAX_TEMP_WEIGHT = 20.0
    MAX_DURATION_WEIGHT = 20.0
    MAX_CRITICALITY_WEIGHT = 25.0
    MAX_DELAY_WEIGHT = 15.0
    MAX_TRAFFIC_WEIGHT = 20.0

    @staticmethod
    def get_tier(score: int) -> str:
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"


class RiskEngine:
    """
    Transparent, deterministic risk engine for pharmaceutical cold chain monitoring.
    Calculates 0-100 risk score and provides contributing factors explanation.
    """

    @staticmethod
    def calculate_risk(
        current_temp: float,
        min_temp: float,
        max_temp: float,
        temp_history: list[float],
        product_criticality: str,
        delay_minutes: int,
        traffic_level: str
    ) -> Dict[str, Any]:
        
        reasons = []

        # 1. Temperature Risk (0 to 20 points)
        temp_score = 0.0
        if current_temp > max_temp:
            deviation = current_temp - max_temp
            temp_score = min(20.0, deviation * 12.5) # e.g. 1.6°C breach * 12.5 = 20 points
            reasons.append(f"Temperature {current_temp}°C exceeded maximum safe threshold of {max_temp}°C (+{round(deviation, 2)}°C)")
        elif current_temp < min_temp:
            deviation = min_temp - current_temp
            temp_score = min(20.0, deviation * 12.5)
            reasons.append(f"Temperature {current_temp}°C fell below minimum safe threshold of {min_temp}°C (-{round(deviation, 2)}°C)")
        else:
            reasons.append(f"Temperature {current_temp}°C is within normal safe range ({min_temp}°C–{max_temp}°C)")

        # 2. Duration / Trend Risk (0 to 20 points)
        duration_score = 0.0
        if len(temp_history) >= 2:
            excursion_readings = [t for t in temp_history if t > max_temp or t < min_temp]
            if len(excursion_readings) > 0:
                duration_score = min(20.0, len(excursion_readings) * 4.0)
                reasons.append(f"Excursion active across {len(excursion_readings)} consecutive sensor ticks")
            
            # Trend evaluation
            if temp_history[-1] > temp_history[0]:
                duration_score = min(20.0, duration_score + 5.0)
                reasons.append("Temperature trend is rapidly increasing")
        elif current_temp > max_temp or current_temp < min_temp:
            duration_score = 10.0

        # 3. Product Criticality (0 to 25 points)
        crit = product_criticality.upper()
        if crit == "HIGH":
            crit_score = 25.0
            reasons.append("Product criticality is HIGH (Vaccine / Temperature-Sensitive Biologic)")
        elif crit == "MEDIUM":
            crit_score = 15.0
            reasons.append("Product criticality is MEDIUM")
        else:
            crit_score = 5.0
            reasons.append("Product criticality is LOW")

        # 4. Delay Risk (0 to 15 points)
        if delay_minutes >= 45:
            delay_score = 15.0
            reasons.append(f"Shipment delay is severe ({delay_minutes} minutes behind schedule)")
        elif delay_minutes >= 20:
            delay_score = 10.0
            reasons.append(f"Shipment delay is moderate ({delay_minutes} minutes behind schedule)")
        elif delay_minutes > 0:
            delay_score = 5.0
            reasons.append(f"Shipment minor delay ({delay_minutes} minutes)")
        else:
            delay_score = 0.0

        # 5. Traffic / Route Risk (0 to 20 points)
        traffic = traffic_level.upper()
        if traffic == "HIGH":
            traffic_score = 20.0
            reasons.append("Traffic congestion level is HIGH along delivery route")
        elif traffic == "MODERATE":
            traffic_score = 10.0
            reasons.append("Traffic congestion level is MODERATE")
        else:
            traffic_score = 0.0

        total_score = int(round(temp_score + duration_score + crit_score + delay_score + traffic_score))
        total_score = max(0, min(100, total_score))
        tier = RiskPolicyConfig.get_tier(total_score)

        return {
            "risk_score": total_score,
            "severity": tier,
            "breakdown": {
                "temperature_risk": round(temp_score, 1),
                "duration_risk": round(duration_score, 1),
                "criticality_risk": round(crit_score, 1),
                "delay_risk": round(delay_score, 1),
                "traffic_risk": round(traffic_score, 1)
            },
            "reasons": reasons
        }
