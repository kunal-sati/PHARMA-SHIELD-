from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.entities import HistoricalIncident, KnowledgeDocument

class RAGEngine:
    """
    PharmaShield RAG Engine.
    Retrieves relevant historical incident cases and SOP regulatory document chunks
    to provide decision context for AI Scenario Planning and Resilience Copilot.
    """

    @classmethod
    def search_similar_incidents(
        cls,
        db: Session,
        symptom_query: str = "temperature excursion",
        product_category: str = "Vaccine"
    ) -> List[Dict[str, Any]]:

        incidents = db.query(HistoricalIncident).all()
        results = []
        for inc in incidents:
            results.append({
                "id": inc.id,
                "title": inc.title,
                "symptoms": inc.symptoms,
                "selected_action": inc.selected_action,
                "outcome": inc.outcome,
                "recovery_duration_minutes": inc.recovery_duration_minutes,
                "lessons_learned": inc.lessons_learned
            })
        return results

    @classmethod
    def search_knowledge_sops(
        cls,
        db: Session,
        query: str
    ) -> List[Dict[str, Any]]:

        docs = db.query(KnowledgeDocument).all()
        results = []
        for doc in docs:
            if any(term.lower() in doc.content.lower() or term.lower() in doc.title.lower() for term in query.split()):
                results.append({
                    "id": doc.id,
                    "title": doc.title,
                    "category": doc.category,
                    "source_uri": doc.source_uri,
                    "excerpt": doc.content[:300] + "..."
                })
        
        if not results and docs:
            results = [{
                "id": docs[0].id,
                "title": docs[0].title,
                "category": docs[0].category,
                "source_uri": docs[0].source_uri,
                "excerpt": docs[0].content[:300] + "..."
            }]
        return results
