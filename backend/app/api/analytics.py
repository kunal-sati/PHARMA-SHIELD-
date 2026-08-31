from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db

router = APIRouter(tags=["Analytics & Executive Control Tower"])

@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    return {
        "fleet_overview": {
            "total_shipments": 48,
            "normal_status": 44,
            "warning_status": 2,
            "critical_status": 1,
            "recovered_status": 1
        },
        "resilience_kpis": {
            "supply_chain_resilience_score": 96.4, # %
            "cold_chain_compliance_rate": 98.2, # %
            "recovery_success_rate": 100.0, # %
            "avg_recovery_time_minutes": 23.5,
            "total_excursions_24h": 1,
            "avoided_product_loss_val": "₹4,850,000"
        },
        "corridor_performance": [
            {"corridor": "Delhi → Chandigarh", "volume": 18, "excursion_rate": "5.5%", "status": "MONITORED"},
            {"corridor": "Mumbai → Pune", "volume": 15, "excursion_rate": "0.0%", "status": "OPTIMAL"},
            {"corridor": "Bengaluru → Hyderabad", "volume": 15, "excursion_rate": "6.6%", "status": "MONITORED"}
        ],
        "disclaimer": "Simulated operational analytics for hackathon evaluation."
    }

@router.get("/executive/kpis")
def get_executive_kpis(db: Session = Depends(get_db)):
    return {
        "resilience_score": 96.4,
        "compliance_pct": 98.2,
        "active_risk_tier": "CRITICAL (1 Active Incident)",
        "recovery_success_pct": 100.0,
        "cost_impact_mitigated": "₹2,400 Recovery Spend / ₹4.85M Saved",
        "sap_governance_status": "ENFORCED (ABAP Rules Active)"
    }
