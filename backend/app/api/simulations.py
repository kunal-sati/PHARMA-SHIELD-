from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/simulations", tags=["What-If Route Simulator"])

class SimulationRequest(BaseModel):
    shipment_id: str = "PS-1026"
    selected_option: str = "REROUTE_TO_COLD_STORAGE" # CONTINUE_ROUTE, REROUTE_TO_COLD_STORAGE, REFRIGERATION_UNIT_REPLACEMENT

@router.post("/what-if")
def run_what_if_simulation(req: SimulationRequest):
    """
    Phase G What-If Route Simulator.
    Simulates hypothetical recovery impacts without mutating live shipment database records.
    """
    if req.selected_option == "CONTINUE_ROUTE":
        return {
            "option": "CONTINUE_ROUTE",
            "simulated_eta_minutes": 65,
            "simulated_cost": 0.0,
            "projected_risk_score": 98,
            "projected_product_health_pct": 22.0,
            "recovery_probability_pct": 12.0,
            "recommendation": "NOT RECOMMENDED (High risk of total thermal spoilage)"
        }
    elif req.selected_option == "REROUTE_TO_COLD_STORAGE":
        return {
            "option": "REROUTE_TO_COLD_STORAGE",
            "simulated_eta_minutes": 23,
            "simulated_cost": 2400.0,
            "projected_risk_score": 24,
            "projected_product_health_pct": 91.5,
            "recovery_probability_pct": 96.0,
            "recommendation": "OPTIMAL (Immediate thermal stabilization at Depot #4)"
        }
    else:
        return {
            "option": "REFRIGERATION_UNIT_REPLACEMENT",
            "simulated_eta_minutes": 35,
            "simulated_cost": 6500.0,
            "projected_risk_score": 45,
            "projected_product_health_pct": 78.0,
            "recovery_probability_pct": 82.0,
            "recommendation": "ACCEPTABLE ALTERNATIVE (Higher cost & delay)"
        }
