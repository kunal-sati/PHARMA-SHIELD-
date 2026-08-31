from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.models.entities import Policy
from backend.app.core.policy_engine import PolicyEngine

def test_action_risk_tiers():
    assert PolicyEngine.get_action_risk_tier("DISCARD_PRODUCT") == "CRITICAL"
    assert PolicyEngine.get_action_risk_tier("REROUTE_TO_COLD_STORAGE") == "HIGH"
    assert PolicyEngine.get_action_risk_tier("SUGGEST_ROUTE_ADJUSTMENT") == "MEDIUM"
    assert PolicyEngine.get_action_risk_tier("SEND_NOTIFICATION") == "LOW"

def test_policy_evaluation():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    pol = Policy(
        policy_id="POL-001",
        name="Enterprise Cold Chain Policy",
        description="Manager sign off policy",
        min_criticality="HIGH",
        cost_threshold=1000.0,
        risk_threshold=80,
        action_tier="HIGH",
        requires_approval=True,
        is_active=True
    )
    db.add(pol)
    db.commit()

    res = PolicyEngine.evaluate_policy(db, criticality="HIGH", cost=2400.0, risk_score=91, action="REROUTE_TO_COLD_STORAGE")
    assert res["requires_human_approval"] is True
    assert res["action_risk_tier"] == "HIGH"
    assert res["autonomous_execution_permitted"] is False
