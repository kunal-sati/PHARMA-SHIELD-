from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.agents.audit_agent import audit_agent

def test_cryptographic_hash_chaining():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    # Record 1
    log1 = audit_agent.record_event(
        db=db, shipment_id="PS-1026", correlation_id="CORR-1026-001",
        actor="System", actor_type="SYSTEM", agent="Simulator",
        event_type="TELEMETRY", action="TICK", decision="NORMAL", status="SUCCESS"
    )

    # Record 2
    log2 = audit_agent.record_event(
        db=db, shipment_id="PS-1026", correlation_id="CORR-1026-001",
        actor="Agent1", actor_type="AGENT", agent="DisruptionAgent",
        event_type="EXCURSION", action="DETECT", decision="CRITICAL", status="SUCCESS"
    )

    assert log2.previous_event_hash == log1.current_event_hash

    # Verify Chain Integrity
    verify_res = audit_agent.verify_audit_chain_integrity(db)
    assert verify_res["status"] == "VALID"
    assert verify_res["verified_records"] == 2
