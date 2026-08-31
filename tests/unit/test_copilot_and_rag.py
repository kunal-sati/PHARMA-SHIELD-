from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.models.entities import HistoricalIncident, KnowledgeDocument, Shipment
from backend.app.core.rag_engine import RAGEngine
from backend.app.core.copilot import ResilienceCopilotEngine

def test_rag_and_copilot_query():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    # Seed Document
    doc = KnowledgeDocument(
        id="KNOW-001",
        title="Cold Chain SOP v2.1",
        category="SOP",
        source_uri="sop://pharmashield/sop-2.1",
        content="Cold Storage Transfer Policy: Vaccines exceeding 8.0°C limit must be routed to CS-04."
    )
    ship = Shipment(
        shipment_id="PS-1026",
        product_name="Vaccine",
        product_type="Biologic",
        origin="Delhi",
        destination="Chandigarh",
        min_temperature=2.0,
        max_temperature=8.0,
        criticality="HIGH",
        current_status="CRITICAL",
        current_temperature=9.6,
        current_latitude=28.70,
        current_longitude=77.10
    )
    db.add_all([doc, ship])
    db.commit()

    # Test RAG SOP Search
    results = RAGEngine.search_knowledge_sops(db, "Cold Storage")
    assert len(results) >= 1
    assert "Cold Chain SOP" in results[0]["title"]

    # Test Copilot Contextual Response
    copilot_res = ResilienceCopilotEngine.process_query(db, "Why was CS-04 selected?", "PS-1026")
    assert "CS-04" in copilot_res["answer"]
    assert len(copilot_res["source_citations"]) >= 1
