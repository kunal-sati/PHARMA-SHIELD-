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
        iv_current_temperature TYPE decfloat34 OPTIONAL
        iv_min_temperature     TYPE decfloat34 OPTIONAL
        iv_max_temperature     TYPE decfloat34 OPTIONAL
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

    " RULE 1: Temperature > 8°C OR < 2°C (or outside product bounds) = Temperature Excursion
    IF ( iv_max_temperature IS NOT INITIAL AND iv_current_temperature > iv_max_temperature )
       OR ( iv_min_temperature IS NOT INITIAL AND iv_current_temperature < iv_min_temperature )
       OR ( iv_current_temperature > 8 OR ( iv_current_temperature < 2 AND iv_current_temperature IS NOT INITIAL ) ).
      APPEND 'ABAP Rule 1: Temperature Excursion detected outside safe pharmaceutical cold-chain envelope (2°C - 8°C).' TO lt_rules.
    ENDIF.

    " RULE 2: Risk score >= 80 = CRITICAL severity
    IF iv_risk_score >= 80.
      APPEND 'ABAP Rule 2: Risk score >= 80 -> Severity escalated to CRITICAL.' TO lt_rules.
    ENDIF.

    " RULE 3: HIGH product criticality AND cost > ₹1000 = Human Approval Required
    IF iv_product_criticality = 'HIGH' AND ( iv_estimated_cost > 1000 OR iv_action = 'REROUTE_TO_COLD_STORAGE' ).
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 3: Product Criticality HIGH & Cost > Threshold (₹1000) -> Human Manager Approval Mandatory.' TO lt_rules.
    ENDIF.

    " RULE 4: AI cannot autonomously execute high-impact actions (Reroute / Unit Replacement)
    IF iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT'.
      rs_result-autonomous_execution_allowed = abap_false.
      rs_result-human_approval_required = abap_true.
      APPEND 'ABAP Rule 4: Action is High-Impact -> AI Autonomous Execution Prohibited (Human Sign-off Mandatory).' TO lt_rules.
    ENDIF.

    rs_result-applicable_rules = lt_rules.
    IF rs_result-human_approval_required = abap_true.
      rs_result-message = 'Recommendation validated under native ABAP Governance Rules Engine. Human Manager approval required before execution.'.
    ELSE.
      rs_result-message = 'Recommendation validated under native ABAP Governance Rules Engine. Autonomous execution permitted.'.
    ENDIF.
  ENDMETHOD.

  METHOD verify_execution_permitted.
    " RULE 5: Execution requires APPROVED status for High-Impact actions
    IF ( iv_action = 'REROUTE_TO_COLD_STORAGE' OR iv_action = 'REFRIGERATION_UNIT_REPLACEMENT' )
       AND iv_approval_status <> 'APPROVED'.
      rv_permitted = abap_false.
    ELSE.
      rv_permitted = abap_true.
    ENDIF.
  ENDMETHOD.

ENDCLASS.
