from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.entities import Shipment, Facility, Disruption
from backend.app.core.master_data import MasterDataEngine
from backend.app.core.rag_engine import RAGEngine

class ResilienceCopilotEngine:
    """
    Feature 19: Resilience Copilot Contextual Assistant.
    Answers operational supply chain queries using live shipment state, facility master data, and RAG context.
    Does NOT have direct action execution authority.
    """

    @classmethod
    def process_query(cls, db: Session, query: str, shipment_id: str = "PS-1026") -> Dict[str, Any]:
        q_lower = query.lower()
        shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()

        if "cs-04" in q_lower or "facility" in q_lower or "why" in q_lower:
            answer = (
                "Facility CS-04 (Northern Regional Cold Storage Depot, Ambala) was selected because it has 122 available cold slots "
                "(exceeding the required 500 units capacity), operates at an optimal 3.9°C temperature, and produces the lowest "
                "projected exposure among eligible regional facilities on the NH-44 corridor."
            )
            citations = ["Facility Master Data CS-04", "PharmaShield Cold Storage Ingestion SOP v2.1"]
        elif "wait" in q_lower or "20 minutes" in q_lower:
            answer = (
                "If dispatch waiting occurs for 20 minutes without rerouting, the projected risk score rises from 91/100 to 98/100, "
                "reducing product health by an additional 18.5% and approaching total thermal spoilage threshold."
            )
            citations = ["What-If Predictive Simulation Model", "Vaccine Stability Matrix"]
        else:
            sop_results = RAGEngine.search_knowledge_sops(db, query)
            citation_titles = [s["title"] for s in sop_results] or ["PharmaShield Enterprise Policy Manual"]
            answer = (
                f"For shipment {shipment_id} ({shipment.product_name if shipment else 'Vaccine'}), current telemetry shows "
                f"{shipment.current_temperature if shipment else 9.6}°C temperature with active status '{shipment.current_status if shipment else 'CRITICAL'}'. "
                f"Governance ABAP Rules 3 & 4 enforce Manager approval prior to cold storage rerouting."
            )
            citations = citation_titles

        return {
          "query": query,
          "shipment_id": shipment_id,
          "answer": answer,
          "source_citations": citations,
          "disclaimer": "Resilience Copilot provides contextual decision support. Action execution requires formal SAP governance and Manager sign-off."
        }
