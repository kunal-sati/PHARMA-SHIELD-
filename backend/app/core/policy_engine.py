from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.entities import Policy

class PolicyEngine:
    """
    Feature 20 & 21: Policy-as-Code & Controlled Autonomy Engine.
    Action Risk Tiers:
      LOW: Auto-executed if policy allows (e.g. SEND_NOTIFICATION).
      MEDIUM: Operator confirmation suggested.
      HIGH: Manager approval mandatory (e.g. REROUTE_TO_COLD_STORAGE).
      CRITICAL: Explicit authorized sign-off required (e.g. DISCARD_PRODUCT).
    """

    @classmethod
    def get_action_risk_tier(cls, action: str) -> str:
        action_upper = action.upper()
        if action_upper in ["DISCARD_PRODUCT", "CANCEL_SHIPMENT"]:
            return "CRITICAL"
        elif action_upper in ["REROUTE_TO_COLD_STORAGE", "REFRIGERATION_UNIT_REPLACEMENT"]:
            return "HIGH"
        elif action_upper in ["SUGGEST_ROUTE_ADJUSTMENT", "NOTIFY_DRIVER"]:
            return "MEDIUM"
        else:
            return "LOW"

    @classmethod
    def evaluate_policy(
        cls,
        db: Session,
        criticality: str,
        cost: float,
        risk_score: int,
        action: str
    ) -> Dict[str, Any]:

        tier = cls.get_action_risk_tier(action)
        requires_approval = tier in ["HIGH", "CRITICAL"] or (criticality == "HIGH" and cost > 1000.0)

        active_policy = db.query(Policy).filter_by(is_active=True).first()
        policy_name = active_policy.name if active_policy else "Default Enterprise Cold Chain Governance Policy v2.0"

        return {
            "policy_name": policy_name,
            "action": action,
            "action_risk_tier": tier,
            "requires_human_approval": requires_approval,
            "autonomous_execution_permitted": not requires_approval,
            "rule_summary": f"Tier '{tier}' action evaluated under '{policy_name}'. Human Approval {'Mandatory' if requires_approval else 'Not Required'}."
        }
