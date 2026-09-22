CLASS lhc_Shipment DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.
    METHODS get_instance_authorizations FOR INSTANCE AUTHORIZATION
      IMPORTING keys REQUEST requested_authorizations FOR Shipment RESULT result.

    METHODS get_instance_features FOR INSTANCE FEATURES
      IMPORTING keys REQUEST requested_features FOR Shipment RESULT result.

    METHODS validateRecommendation FOR MODIFY
      IMPORTING keys FOR ACTION Shipment~validateRecommendation RESULT result.

    METHODS approveAction FOR MODIFY
      IMPORTING keys FOR ACTION Shipment~approveAction RESULT result.

    METHODS executeReroute FOR MODIFY
      IMPORTING keys FOR ACTION Shipment~executeReroute RESULT result.
ENDCLASS.

CLASS lhc_Shipment IMPLEMENTATION.

  METHOD get_instance_authorizations.
  ENDMETHOD.

  METHOD get_instance_features.
  ENDMETHOD.

  METHOD validateRecommendation.
    DATA: lo_gov TYPE REF TO zcl_pharmashield_governance.
    CREATE OBJECT lo_gov.

    READ ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(lt_shipments).

    LOOP AT lt_shipments INTO DATA(ls_shipment).
      " Call authoritative ABAP governance engine
      DATA(ls_validation) = lo_gov->validate_recommendation(
        iv_shipment_id         = CONV #( ls_shipment-ShipmentID )
        iv_product_criticality = CONV #( ls_shipment-Criticality )
        iv_action              = 'REROUTE_TO_COLD_STORAGE'
        iv_estimated_cost      = 2400
        iv_risk_score          = ls_shipment-ProjectedRiskScore
        iv_current_temperature = ls_shipment-CurrentTemperature
        iv_min_temperature     = ls_shipment-MinTemperature
        iv_max_temperature     = ls_shipment-MaxTemperature
      ).

      " Return entity with current governance status
      APPEND VALUE #( %tky   = ls_shipment-%tky
                      %param = CORRESPONDING #( ls_shipment ) ) TO result.
    ENDLOOP.
  ENDMETHOD.

  METHOD approveAction.
    READ ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(lt_shipments).

    MODIFY ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      UPDATE FIELDS ( CurrentStatus UpdatedAt )
      WITH VALUE #( FOR shp IN lt_shipments (
        %tky          = shp-%tky
        CurrentStatus = 'APPROVED'
        UpdatedAt     = cl_abap_context_info=>get_system_time( )
      ) ).

    READ ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT lt_shipments.

    result = VALUE #( FOR shp IN lt_shipments ( %tky = shp-%tky %param = shp ) ).
  ENDMETHOD.

  METHOD executeReroute.
    DATA: lo_gov TYPE REF TO zcl_pharmashield_governance.
    CREATE OBJECT lo_gov.

    READ ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(lt_shipments).

    LOOP AT lt_shipments INTO DATA(ls_shipment).
      DATA(lv_permitted) = lo_gov->verify_execution_permitted(
        iv_approval_status = CONV #( ls_shipment-CurrentStatus )
        iv_action          = 'REROUTE_TO_COLD_STORAGE'
      ).

      IF lv_permitted = abap_true.
        MODIFY ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
          ENTITY Shipment
          UPDATE FIELDS ( CurrentStatus UpdatedAt )
          WITH VALUE #( (
            %tky          = ls_shipment-%tky
            CurrentStatus = 'REROUTED_TO_COLD_STORAGE'
            UpdatedAt     = cl_abap_context_info=>get_system_time( )
          ) ).
      ELSE.
        APPEND VALUE #( %tky = ls_shipment-%tky
                        %msg = new_message_with_text(
                          severity = if_abap_behv_message=>severity-error
                          text     = 'Execution prohibited by SAP Governance: Human Manager Approval required before execution.'
                        ) ) TO reported-shipment.
      ENDIF.
    ENDLOOP.

    READ ENTITIES OF zi_pharmashield_shipment IN LOCAL MODE
      ENTITY Shipment
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT lt_shipments.

    result = VALUE #( FOR shp IN lt_shipments ( %tky = shp-%tky %param = shp ) ).
  ENDMETHOD.

ENDCLASS.
