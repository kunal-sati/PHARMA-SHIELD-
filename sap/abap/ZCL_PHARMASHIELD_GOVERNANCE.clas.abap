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

    " Rule 1 & 2 Evaluation: Risk Score >= 80 -> Severity set to CRITICAL
    IF iv_risk_score >= 80.
      APPEND 'ABAP Rule 2: Risk score >= 80 -> Severity set to CRITICAL' TO lt_rules.
    ENDIF.

    " Rule 3 Evaluation: High Criticality & Cost > 1000 -> Human Approval Mandatory
    IF iv_product_criticality = 'HIGH' AND ( iv_estimated_cost > 1000 OR iv_action = 'REROUTE_TO_COLD_STORAGE' ).
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 3: Product Criticality HIGH & Cost > Threshold (₹1000) -> Human Approval Mandatory' TO lt_rules.
    ENDIF.

    " Rule 4 Evaluation: High Impact Action -> Autonomous Execution Prohibited
    IF iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT'.
      rs_result-autonomous_execution_allowed = abap_false.
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 4: Action is high-impact -> Autonomous Execution Prohibited' TO lt_rules.
    ENDIF.

    rs_result-applicable_rules = lt_rules.
    rs_result-message = 'Validated under native ABAP Governance Rules Engine.'.
  ENDMETHOD.

  METHOD verify_execution_permitted.
    " Rule 5 Evaluation: Execution strictly prohibited unless approval_status == APPROVED.
    IF ( iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT' )
       AND iv_approval_status <> 'APPROVED'.
      rv_permitted = abap_false.
    ELSE.
      rv_permitted = abap_true.
    ENDIF.
  ENDMETHOD.

ENDCLASS.
