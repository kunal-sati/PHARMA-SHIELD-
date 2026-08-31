# PharmaShield — Agent Architecture & Pipeline Specification

## Agent 1 — Disruption Sensing Agent
- **Type:** Deterministic Sensing Engine + Signal Aggregator
- **Input:** Telemetry frame (`temperature`, `humidity`, `latitude`, `longitude`, `delay_minutes`, `traffic_level`, `product_criticality`)
- **Output:** Structured disruption event containing `disruption_detected`, `type`, `severity`, `risk_score` (0-100), `confidence`, and contributing reasons list.

---

## Agent 2 — Scenario Planning Agent
- **Type:** Hybrid LLM Planner / Rule-based Fallback Planner
- **Input:** Structured disruption event + shipment profile + available logistics resources (nearest cold storage locations, service vehicles).
- **Output:**
  - `scenarios`: Array of recovery options:
    1. `CONTINUE_ROUTE` (Time: 65m, Cost: ₹0, Risk: HIGH)
    2. `REROUTE_TO_COLD_STORAGE` (Time: 23m, Cost: ₹2,400, Risk: LOW)
    3. `REFRIGERATION_UNIT_REPLACEMENT` (Time: 35m, Cost: ₹6,500, Risk: MEDIUM)
  - `recommended_scenario_id`: `SCN-002`
  - `confidence`: `0.94`
  - `reason`: Explainable natural-language justification.

---

## Agent 3 — Execution / Rerouting Agent
- **Type:** Governance-Gated Execution Engine
- **Responsibility:** Validates human approval status, performs state transitions (`APPROVED` -> `RECOVERING` -> `RECOVERED`), updates route ETA and destination.

---

## Agent 4 — Compliance & Audit Agent
- **Type:** Immutable Event Logger
- **Responsibility:** Appends audit log entries with correlation ID (`CORR-PS1026-001`), timestamp, actor, agent name, event type, decision, and metadata.
