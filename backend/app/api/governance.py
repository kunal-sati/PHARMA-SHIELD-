from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment
from backend.app.integrations.sap_governance import get_sap_governance_service
from backend.app.integrations.real_sap_governance import SAPIntegrationError
from backend.app.schemas.schemas import SAPValidationResult

router = APIRouter(prefix="/governance", tags=["SAP Governance"])

@router.post("/validate", response_model=SAPValidationResult)
def validate_sap_rules(
    shipment_id: str,
    action: str = "REROUTE_TO_COLD_STORAGE",
    estimated_cost: float = 2400.0,
    db: Session = Depends(get_db)
):
    shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment {shipment_id} not found")

    sap_service = get_sap_governance_service()
    try:
        result = sap_service.validate_recommendation(
            shipment_id=shipment.shipment_id,
            product_criticality=shipment.criticality,
            action=action,
            estimated_cost=estimated_cost,
            risk_score=getattr(shipment, "projected_risk_score", 91),
            current_temperature=getattr(shipment, "current_temperature", None),
            min_temperature=getattr(shipment, "min_temperature", 2.0),
            max_temperature=getattr(shipment, "max_temperature", 8.0)
        )
        return result
    except SAPIntegrationError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Real SAP BTP Governance validation failed: {str(e)}"
        )
