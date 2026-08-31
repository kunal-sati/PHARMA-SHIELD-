from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Shipment
from backend.app.integrations.sap_governance import sap_governance
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    result = sap_governance.validate_recommendation(
        shipment_id=shipment.shipment_id,
        product_criticality=shipment.criticality,
        action=action,
        estimated_cost=estimated_cost,
        risk_score=91
    )
    return result
