@AbapCatalog.sqlViewName: 'ZPHARMASHIELDSHP'
@AbapCatalog.compiler.compareFilter: true
@AbapCatalog.preserveKey: true
@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'PharmaShield Cold Chain Shipment CDS Data Model'
define root view ZI_PHARMASHIELD_SHIPMENT
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
