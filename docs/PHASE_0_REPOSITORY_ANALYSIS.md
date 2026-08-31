# Phase 0: Repository & Environment Analysis

**Project Name:** PharmaShield — An Agentic Cold Chain Resilience Platform  
**Analysis Date:** August 26, 2026  
**Environment:** macOS (Darwin arm64)  
**Workspace Path:** `/Users/siddharthsati/Desktop/PHARAMA SHIELD `

---

## 1. Repository State
- **Workspace Status:** Fresh / Empty Directory (`/Users/siddharthsati/Desktop/PHARAMA SHIELD `).
- **Existing Code:** None. No pre-existing legacy files or conflicting dependencies.
- **Git Repository:** Needs initialization (`git init`).

---

## 2. Runtime Environment Inspection
- **Python:** `3.12.6` (Available globally via `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`)
- **Node.js:** `v26.0.0`
- **npm:** `11.12.1`
- **Docker:** `29.3.1` (Docker daemon available and build-capable)
- **Database Availability:** SQLite available natively via Python standard library `sqlite3`; Docker available to spin up PostgreSQL when required.

---

## 3. SAP Connectivity & Environment Inspection
- **SAP Environment Variables:** None detected (`SAP_BASE_URL`, `SAP_CLIENT_ID`, `SAP_HANA_HOST` not present in environment).
- **SAP Integration Strategy:** As specified in Section 4 & 11 of the engineering specification, a clean integration boundary (`SAPGovernanceService`) will be implemented with a default `MockSAPGovernanceService` for local demo execution. This mock will be explicitly labeled as DEMO/MOCK integration in UI and API responses to preserve transparency.

---

## 4. Technology Decisions & Rationale

| Layer | Framework / Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | Next.js 14+ (App Router), React, TypeScript, Tailwind CSS | Enterprise command center UI, server rendering + client interactive state, responsive dark visual identity. |
| **UI Components & Icons** | Lucide React, Recharts, Leaflet / React-Leaflet | Modern data visualization for temperature graphs and route geographic mapping. |
| **Backend API & Orchestration** | Python 3.12, FastAPI, Pydantic v2 | High-performance asynchronous REST endpoints, WebSocket engine for real-time sensor streams, strict schema validation. |
| **Database & ORM** | SQLAlchemy 2.0 with SQLite (dev) / PostgreSQL (prod) | Repository pattern abstraction; clean schema switching without business logic modifications. |
| **Agent Logic & AI** | Deterministic Python Risk Engine + LLM Scenario Planner (Gemini API via Firebase/Google SDK or HTTP with mock fallback) | Deterministic rule enforcement for thresholds & governance; LLM reasoning for natural-language scenario evaluation and ranking. |
| **SAP Governance Layer** | Python `MockSAPGovernanceService` with ABAP business rule rules engine | Enforces ABAP rules (Rules 1–5), approval constraints, and business thresholds deterministically. |

---

## 5. Risk Assessment & Mitigations

1. **Risk:** Real-time sensor stream UI synchronization lag.  
   *Mitigation:* Implement WebSocket endpoint (`/ws/shipments/{shipment_id}`) in FastAPI with client fallback to polling (1s interval) during simulation.

2. **Risk:** Dependency on external LLM availability during hackathon judging demo.  
   *Mitigation:* Build a robust deterministic fallback scenario engine within the Planning Agent so that if `AI_API_KEY` is missing or fails, structured recovery scenarios are generated without failing the workflow.

3. **Risk:** State mutation bypass (e.g. going directly from `CRITICAL` to `RECOVERED` without approval).  
   *Mitigation:* Implement a centralized `ShipmentStateMachine` in `backend/app/services/state_machine.py` enforcing allowed state transitions strictly on the server side.

---

## 6. Assumptions & Constraints
- The hackathon MVP is bounded to simulated IoT sensor readings and simulated logistics routing.
- High-impact recovery decisions strictly require human approval (Role: `MANAGER` or `ADMIN`).
- All state changes, rule evaluations, AI recommendations, and approvals must emit append-only audit log records with a correlation ID (`CORR-PS1026-001`).

---

## 7. Phase 0 Recommendation
Proceed immediately with the formal **Implementation Plan Artifact**, then request human review before writing application code for Phase 1.
