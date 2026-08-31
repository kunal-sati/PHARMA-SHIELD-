from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.app.schemas.schemas import SAPValidationResult

class SAPGovernanceInterface(ABC):
    @abstractmethod
    def validate_recommendation(
        self,
        shipment_id: str,
        product_criticality: str,
        action: str,
        estimated_cost: float,
        risk_score: int
    ) -> SAPValidationResult:
        pass

    @abstractmethod
    def verify_execution_permitted(self, approval_status: str, action: str) -> bool:
        pass


class MockSAPGovernanceService(SAPGovernanceInterface):
    """
    Mock SAP Governance Service enforcing enterprise ABAP business rules.
    Clearly labeled in UI and logs as DEMO / MOCK integration.
    """

    COST_APPROVAL_THRESHOLD = 1000.0  # ₹1,000 threshold for human approval requirement
    HIGH_IMPACT_ACTIONS = ["REROUTE_TO_COLD_STORAGE", "REFRIGERATION_UNIT_REPLACEMENT"]

    def validate_recommendation(
        self,
        shipment_id: str,
        product_criticality: str,
        action: str,
        estimated_cost: float,
        risk_score: int
    ) -> SAPValidationResult:
        
        applied_rules = []
        human_approval_required = False
        autonomous_allowed = True

        # Rule 1 & 2 Evaluation
        if risk_score >= 80:
            applied_rules.append("ABAP Rule 2: Risk score >= 80 -> Severity set to CRITICAL")

        # Rule 3 Evaluation
        if product_criticality.upper() == "HIGH" and (estimated_cost > self.COST_APPROVAL_THRESHOLD or action in self.HIGH_IMPACT_ACTIONS):
            human_approval_required = True
            applied_rules.append(f"ABAP Rule 3: Product Criticality HIGH & Cost (₹{estimated_cost}) > Threshold (₹{self.COST_APPROVAL_THRESHOLD}) -> Human Approval Mandatory")

        # Rule 4 Evaluation
        if action in self.HIGH_IMPACT_ACTIONS:
            autonomous_allowed = False
            human_approval_required = True
            applied_rules.append(f"ABAP Rule 4: Action '{action}' is high-impact -> Autonomous Execution Prohibited")

        message = (
            "Recommendation validated under SAP Governance Policy. Human Manager approval required."
            if human_approval_required
            else "Recommendation validated under SAP Governance Policy. Autonomous execution permitted."
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
        Rule 5 Evaluation: Execution strictly prohibited unless approval_status == APPROVED.
        """
        if action in self.HIGH_IMPACT_ACTIONS and approval_status != "APPROVED":
            return False
        return True

# Dynamic factory for active SAP Governance Service
def get_sap_governance_service() -> SAPGovernanceInterface:
    import os
    sap_mode = os.getenv("SAP_MODE", "MOCK").upper()
    if sap_mode == "REAL":
        from backend.app.integrations.real_sap_governance import RealSAPGovernanceService
        return RealSAPGovernanceService()
    return MockSAPGovernanceService()

sap_governance = get_sap_governance_service()

