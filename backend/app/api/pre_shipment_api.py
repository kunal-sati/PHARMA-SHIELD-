from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.core.pre_shipment import PreShipmentRiskEngine

router = APIRouter(prefix="/pre-shipment", tags=["Pre-Shipment Intelligence"])

class PreShipmentAssessmentRequest(BaseModel):
    product_criticality: str = "HIGH"
    supplier_reliability: float = 98.5
    route_risk_score: int = 15
    traffic_level: str = "HIGH"

@router.post("/risk")
def assess_pre_shipment_risk(req: PreShipmentAssessmentRequest):
    return PreShipmentRiskEngine.evaluate_pre_shipment(
        product_criticality=req.product_criticality,
        supplier_reliability=req.supplier_reliability,
        route_risk_score=req.route_risk_score,
        traffic_level=req.traffic_level
    )
