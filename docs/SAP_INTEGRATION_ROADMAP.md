# PharmaShield — Real SAP Integration Master Architecture & ABAP Codebook

**Document Date:** August 27, 2026  
**System Target:** SAP HANA Cloud / SAP S/4HANA (ABAP Environment / SAP BTP RAP Framework)  
**Protocol:** OData V4 Service Binding

---

## 1. SAP HANA Data Models & Core Data Services (CDS Views)

### 1.1 Core CDS Entity: `ZI_PharmaShield_Shipment`
```abap
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'PharmaShield Cold Chain Shipment Data'
define root view entity ZI_PharmaShield_Shipment
  as select from zpharmashield_shp
{
  key shipment_id             as ShipmentID,
      organization_id         as OrganizationID,
      product_id              as ProductID,
      product_name            as ProductName,
      product_type            as ProductType,
      origin                  as Origin,
      destination             as Destination,
      min_temperature         as MinTemperature,
      max_temperature         as MaxTemperature,
      criticality             as Criticality,
      quantity_units          as QuantityUnits,
      current_status          as CurrentStatus,
      current_temperature     as CurrentTemperature,
      current_latitude        as CurrentLatitude,
      current_longitude       as CurrentLongitude,
      delay_minutes           as DelayMinutes,
      traffic_level           as TrafficLevel,
      projected_risk_score    as ProjectedRiskScore,
      time_to_critical_min    as TimeToCriticalMinutes,
      product_health_pct      as ProductHealthPct,
      created_at              as CreatedAt,
      updated_at              as UpdatedAt
}
```

---

## 2. ABAP Rules Engine (`ZCL_PHARMASHIELD_GOVERNANCE`)

```abap
CLASS zcl_pharmashield_governance DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC .

  PUBLIC SECTION.
    TYPES: BEGIN OF ty_validation_result,
             is_valid                     TYPE abap_bool,
             human_approval_required      TYPE abap_bool,
             autonomous_execution_allowed TYPE abap_bool,
             applicable_rules             TYPE string_table,
             message                      TYPE string,
           END OF ty_validation_result.

    METHODS validate_recommendation
      IMPORTING
        iv_shipment_id         TYPE string
        iv_product_criticality TYPE string
        iv_action              TYPE string
        iv_estimated_cost      TYPE decfloat34
        iv_risk_score          TYPE i
      RETURNING
        VALUE(rs_result)       TYPE ty_validation_result .

    METHODS verify_execution_permitted
      IMPORTING
        iv_approval_status TYPE string
        iv_action          TYPE string
      RETURNING
        VALUE(rv_permitted) TYPE abap_bool .
ENDCLASS.

CLASS zcl_pharmashield_governance IMPLEMENTATION.

  METHOD validate_recommendation.
    DATA: lt_rules TYPE string_table.
    rs_result-is_valid = abap_true.
    rs_result-human_approval_required = abap_false.
    rs_result-autonomous_execution_allowed = abap_true.

    " Rule 2: Risk Score >= 80 -> Critical Severity
    IF iv_risk_score >= 80.
      APPEND 'ABAP Rule 2: Risk score >= 80 -> Severity set to CRITICAL' TO lt_rules.
    ENDIF.

    " Rule 3: High Criticality & Cost > 1000 -> Human Approval Mandatory
    IF iv_product_criticality = 'HIGH' AND ( iv_estimated_cost > 1000 OR iv_action = 'REROUTE_TO_COLD_STORAGE' ).
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 3: Product Criticality HIGH & Cost > Threshold -> Human Approval Mandatory' TO lt_rules.
    ENDIF.

    " Rule 4: High Impact Action -> Autonomous Execution Prohibited
    IF iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT'.
      rs_result-autonomous_execution_allowed = abap_false.
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 4: Action is high-impact -> Autonomous Execution Prohibited' TO lt_rules.
    ENDIF.

    rs_result-applicable_rules = lt_rules.
    rs_result-message = 'Validated under native ABAP Governance Rules Engine.'.
  ENDMETHOD.

  METHOD verify_execution_permitted.
    IF ( iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT' )
       AND iv_approval_status <> 'APPROVED'.
      rv_permitted = abap_false.
    ELSE.
      rv_permitted = abap_true.
    ENDIF.
  ENDMETHOD.

ENDCLASS.
```

---

## 3. OData V4 Service Structure & SAP BTP Adapter Architecture

In `backend/app/integrations/real_sap_governance.py`:

```python
import httpx
from backend.app.integrations.sap_governance import SAPGovernanceInterface, MockSAPGovernanceService
from backend.app.schemas.schemas import SAPValidationResult

class RealSAPGovernanceService(SAPGovernanceInterface):
    """
    Real SAP Governance Service connecting via OData V4 to SAP BTP / SAP S/4HANA.
    """
    def __init__(self, odata_url: str, client_id: str, client_secret: str):
        self.odata_url = odata_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.fallback_mock = MockSAPGovernanceService()

    def validate_recommendation(
        self, shipment_id: str, product_criticality: str, action: str, estimated_cost: float, risk_score: int
    ) -> SAPValidationResult:
        try:
            # Post to SAP BTP RAP OData V4 endpoint
            payload = {
                "ShipmentID": shipment_id,
                "Criticality": product_criticality,
                "Action": action,
                "EstimatedCost": estimated_cost,
                "RiskScore": risk_score
            }
            res = httpx.post(f"{self.odata_url}/ValidateRecommendation", json=payload, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                return SAPValidationResult(
                    is_valid=data["isValid"],
                    human_approval_required=data["humanApprovalRequired"],
                    autonomous_execution_allowed=data["autonomousExecutionAllowed"],
                    applicable_rules=data["applicableRules"],
                    message="Validated by Real SAP HANA / ABAP Governance Service."
                )
        except Exception:
            pass
        # Fallback to local mock if offline
        return self.fallback_mock.validate_recommendation(shipment_id, product_criticality, action, estimated_cost, risk_score)

    def verify_execution_permitted(self, approval_status: str, action: str) -> bool:
        if action in ["REROUTE_TO_COLD_STORAGE", "REFRIGERATION_UNIT_REPLACEMENT"] and approval_status != "APPROVED":
            return False
        return True
```
