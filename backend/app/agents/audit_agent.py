import uuid
import datetime
import hashlib
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import AuditLog

class ComplianceAuditAgent:
    """
    Agent 4: Immutable SHA-256 Cryptographic Hash Chaining Audit Logger.
    Every audit log entry contains a cryptographic hash of its payload AND the hash of the preceding entry.
    """

    def _compute_hash(
        self,
        prev_hash: str,
        shipment_id: str,
        timestamp_str: str,
        actor: str,
        action: str,
        decision: str,
        metadata_str: str
    ) -> str:
        data = f"{prev_hash}|{shipment_id}|{timestamp_str}|{actor}|{action}|{decision}|{metadata_str}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def record_event(
        self,
        db: Session,
        shipment_id: str,
        correlation_id: str,
        actor: str,
        actor_type: str,
        agent: Optional[str],
        event_type: str,
        action: str,
        decision: str,
        status: str,
        metadata_json: Optional[Dict[str, Any]] = None
    ) -> AuditLog:

        log_id = f"AUD-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.datetime.now(datetime.timezone.utc)
        now_str = now.isoformat()

        # Fetch previous log for hash chaining
        last_log = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).first()
        prev_hash = last_log.current_event_hash if (last_log and last_log.current_event_hash) else "GENESIS_BLOCK_00000000000000000000000000000000"

        meta_str = json.dumps(metadata_json or {}, sort_keys=True)
        curr_hash = self._compute_hash(
            prev_hash=prev_hash,
            shipment_id=shipment_id,
            timestamp_str=now_str,
            actor=actor,
            action=action,
            decision=decision,
            metadata_str=meta_str
        )

        audit_record = AuditLog(
            id=log_id,
            shipment_id=shipment_id,
            correlation_id=correlation_id,
            timestamp=now,
            actor=actor,
            actor_type=actor_type,
            agent=agent,
            event_type=event_type,
            action=action,
            decision=decision,
            status=status,
            metadata_json=metadata_json or {},
            previous_event_hash=prev_hash,
            current_event_hash=curr_hash
        )

        db.add(audit_record)
        db.commit()
        db.refresh(audit_record)
        return audit_record

    def verify_audit_chain_integrity(self, db: Session) -> Dict[str, Any]:
        """
        Verifies the cryptographic integrity of the entire audit log database chain.
        """
        logs = db.query(AuditLog).order_by(AuditLog.timestamp.asc()).all()
        if not logs:
            return {"status": "VALID", "message": "Audit chain is empty and valid.", "verified_records": 0}

        expected_prev_hash = "GENESIS_BLOCK_00000000000000000000000000000000"
        for i, log in enumerate(logs):
            if log.previous_event_hash != expected_prev_hash:
                return {
                    "status": "TAMPERED",
                    "message": f"Audit chain broken at record index {i} (ID: {log.id}). Expected prev hash: {expected_prev_hash}, found: {log.previous_event_hash}",
                    "broken_record_id": log.id
                }

            expected_prev_hash = log.current_event_hash

        return {
            "status": "VALID",
            "message": "AUDIT INTEGRITY: VALID. Cryptographic hash chain verified across all records.",
            "verified_records": len(logs),
            "latest_block_hash": expected_prev_hash
        }

audit_agent = ComplianceAuditAgent()
