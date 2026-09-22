import os
from abc import ABC, abstractmethod
from typing import Optional, List
from backend.app.schemas.schemas import SAPValidationResult
from backend.app.core.config import settings

class SAPGovernanceInterface(ABC):
    """
    Abstract interface defining the authoritative SAP Governance contract
    for cold-chain pharmaceutical recommendations and execution gating.
    """

    @abstractmethod
    def validate_recommendation(
        self,
        shipment_id: str,
        product_criticality: str,
        action: str,
        estimated_cost: float,
        risk_score: int,
        current_temperature: Optional[float] = None,
        min_temperature: Optional[float] = None,
        max_temperature: Optional[float] = None
    ) -> SAPValidationResult:
        """Validate recommendation against SAP Governance Policy."""
        pass

    @abstractmethod
    def verify_execution_permitted(self, approval_status: str, action: str) -> bool:
        """Rule 5: Verify if execution is permitted under SAP Governance."""
        pass


class MockSAPGovernanceService(SAPGovernanceInterface):
    """
    Mock SAP Governance Service simulating the native ABAP Rules Engine
    (ZCL_PHARMASHIELD_GOVERNANCE) deterministically for local development and offline testing.
    """

    COST_APPROVAL_THRESHOLD = 1000.0  # ₹1,000 threshold for human approval requirement
    HIGH_IMPACT_ACTIONS = ["REROUTE_TO_COLD_STORAGE", "REFRIGERATION_UNIT_REPLACEMENT"]

    def validate_recommendation(
        self,
        shipment_id: str,
        product_criticality: str,
        action: str,
        estimated_cost: float,
        risk_score: int,
        current_temperature: Optional[float] = None,
        min_temperature: Optional[float] = None,
        max_temperature: Optional[float] = None
    ) -> SAPValidationResult:
        applied_rules: List[str] = []
        human_approval_required = False
        autonomous_allowed = True

        # RULE 1: Temperature Excursion Check
        is_excursion = False
        if max_temperature is not None and current_temperature is not None and current_temperature > max_temperature:
            is_excursion = True
        elif min_temperature is not None and current_temperature is not None and current_temperature < min_temperature:
            is_excursion = True
        elif current_temperature is not None and (current_temperature > 8.0 or current_temperature < 2.0):
            is_excursion = True

        if is_excursion:
            applied_rules.append(
                "ABAP Rule 1: Temperature Excursion detected outside safe pharmaceutical cold-chain envelope (2°C - 8°C)."
            )

        # RULE 2: Risk Score >= 80 -> CRITICAL
        if risk_score >= 80:
            applied_rules.append("ABAP Rule 2: Risk score >= 80 -> Severity escalated to CRITICAL.")

        # RULE 3: Product Criticality HIGH & Cost > ₹1000 -> Human Approval Mandatory
        if product_criticality.upper() == "HIGH" and (estimated_cost > self.COST_APPROVAL_THRESHOLD or action in self.HIGH_IMPACT_ACTIONS):
            human_approval_required = True
            applied_rules.append(
                f"ABAP Rule 3: Product Criticality HIGH & Cost (₹{estimated_cost:.2f}) > Threshold (₹{self.COST_APPROVAL_THRESHOLD:.2f}) -> Human Manager Approval Mandatory."
            )

        # RULE 4: High Impact Action -> Autonomous Execution Prohibited
        if action in self.HIGH_IMPACT_ACTIONS:
            autonomous_allowed = False
            human_approval_required = True
            applied_rules.append(
                f"ABAP Rule 4: Action '{action}' is High-Impact -> AI Autonomous Execution Prohibited (Human Sign-off Mandatory)."
            )

        message = (
            "Recommendation validated under simulated ABAP Governance Rules Engine. Human Manager approval required before execution."
            if human_approval_required
            else "Recommendation validated under simulated ABAP Governance Rules Engine. Autonomous execution permitted."
        )

        return SAPValidationResult(
            is_valid=True,
            human_approval_required=human_approval_required,
            autonomous_execution_allowed=autonomous_allowed,
            applicable_rules=applied_rules,
            message=message
        )

    def verify_execution_permitted(self, approval_status: str, action: str) -> bool:
        """
        RULE 5: Execution requires APPROVED status for High-Impact actions.
        """
        if action in self.HIGH_IMPACT_ACTIONS and approval_status.upper() != "APPROVED":
            return False
        return True


def get_sap_governance_service() -> SAPGovernanceInterface:
    """
    Factory creating the active SAP Governance adapter based on configuration.
    """
    sap_mode = os.getenv("SAP_MODE", settings.SAP_MODE).upper()
    if sap_mode == "REAL":
        from backend.app.integrations.real_sap_governance import RealSAPGovernanceService
        return RealSAPGovernanceService()
    return MockSAPGovernanceService()


sap_governance = get_sap_governance_service()
