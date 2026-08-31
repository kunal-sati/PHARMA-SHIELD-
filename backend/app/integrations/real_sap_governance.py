import os
import logging
import httpx
from backend.app.integrations.sap_governance import SAPGovernanceInterface, MockSAPGovernanceService
from backend.app.schemas.schemas import SAPValidationResult

logger = logging.getLogger("pharmashield.sap")

class RealSAPGovernanceService(SAPGovernanceInterface):
    """
    Real SAP Governance Service connecting via OData V4 to SAP BTP / SAP S/4HANA Cloud.
    Implements SAPGovernanceInterface with graceful fallback to MockSAPGovernanceService if SAP BTP is unreachable.
    """

    def __init__(
        self,
        odata_url: str = None,
        client_id: str = None,
        client_secret: str = None,
        token_url: str = None
    ):
        self.odata_url = odata_url or os.getenv("SAP_ODATA_URL", "https://my-sap-btp-tenant.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001")
        self.client_id = client_id or os.getenv("SAP_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("SAP_CLIENT_SECRET", "")
        self.token_url = token_url or os.getenv("SAP_TOKEN_URL", "")
        self.fallback_mock = MockSAPGovernanceService()
        self._cached_token = None

    def _get_oauth_token(self) -> str:
        """Fetch OAuth 2.0 Access Token from SAP BTP UAA Destination Service."""
        if self._cached_token:
            return self._cached_token
        if not self.token_url or not self.client_id:
            return None

        try:
            res = httpx.post(
                self.token_url,
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                timeout=5.0
            )
            if res.status_code == 200:
                self._cached_token = res.json().get("access_token")
                return self._cached_token
        except Exception as e:
            logger.warning(f"SAP BTP OAuth Token fetch failed: {e}")
        return None

    def validate_recommendation(
        self,
        shipment_id: str,
        product_criticality: str,
        action: str,
        estimated_cost: float,
        risk_score: int
    ) -> SAPValidationResult:
        """
        Validate recommendation against Real SAP ABAP Governance Rules Engine via OData V4.
        """
        token = self._get_oauth_token()
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        payload = {
            "ShipmentID": shipment_id,
            "Criticality": product_criticality,
            "Action": action,
            "EstimatedCost": estimated_cost,
            "RiskScore": risk_score
        }

        try:
            url = f"{self.odata_url}/ValidateRecommendation"
            res = httpx.post(url, json=payload, headers=headers, timeout=5.0)
            if res.status_code in [200, 201]:
                data = res.json()
                return SAPValidationResult(
                    is_valid=data.get("isValid", True),
                    human_approval_required=data.get("humanApprovalRequired", True),
                    autonomous_execution_allowed=data.get("autonomousExecutionAllowed", False),
                    applicable_rules=data.get("applicableRules", [
                        "Real SAP HANA ABAP Rule 2: Critical Risk Score >= 80",
                        "Real SAP HANA ABAP Rule 3: High Cost / Impact Rerouting Approval Mandatory"
                    ]),
                    message="Validated by Real SAP HANA / ABAP Governance Engine via SAP BTP OData V4."
                )
        except Exception as e:
            logger.info(f"Real SAP OData V4 endpoint unreachable ({e}). Using Mock SAP Governance fallback.")

        # Graceful fallback to deterministic local mock adapter
        return self.fallback_mock.validate_recommendation(
            shipment_id=shipment_id,
            product_criticality=product_criticality,
            action=action,
            estimated_cost=estimated_cost,
            risk_score=risk_score
        )

    def verify_execution_permitted(self, approval_status: str, action: str) -> bool:
        """
        ABAP Rule 5 Evaluation: Execution strictly prohibited unless approval_status == APPROVED.
        """
        if action in ["REROUTE_TO_COLD_STORAGE", "REFRIGERATION_UNIT_REPLACEMENT"] and approval_status != "APPROVED":
            return False
        return True
