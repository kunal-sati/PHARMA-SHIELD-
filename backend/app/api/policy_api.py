from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.entities import Policy
from backend.app.core.policy_engine import PolicyEngine

router = APIRouter(prefix="/policies", tags=["Policy-as-Code & Autonomy"])

@router.get("")
def get_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()

@router.post("/evaluate")
def evaluate_policy(
    criticality: str = "HIGH",
    cost: float = 2400.0,
    risk_score: int = 91,
    action: str = "REROUTE_TO_COLD_STORAGE",
    db: Session = Depends(get_db)
):
    return PolicyEngine.evaluate_policy(db, criticality, cost, risk_score, action)
