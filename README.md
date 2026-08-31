# PharmaShield — An Agentic Cold Chain Resilience Platform

[![Hackathon Prototype](https://img.shields.io/badge/Status-Hackathon--MVP-brightgreen)](https://github.com/pharmashield)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)

> **Core Idea:** PharmaShield is an AI-powered platform for pharmaceutical cold-chain resilience. It continuously monitors shipment signals, detects disruptions, analyzes severity, generates recovery scenarios, applies deterministic SAP business rules, requests human approval for high-impact actions, executes approved recovery actions, and records the complete decision history for compliance auditability.

**Core Paradigm:** *AI recommends. SAP governs. Humans approve. The system executes and audits.*

---

## 1. Hackathon Demonstration Workflow

The system is pre-configured to demonstrate the primary **Vaccine Temperature Excursion** scenario:

- **Shipment ID:** `PS-1026`
- **Product:** Vaccine (2°C–8°C safe range)
- **Route:** Delhi to Chandigarh
- **Excursion Event:** Temperature rises from normal (4.2°C) to breach threshold (9.6°C)
- **Risk Score:** `91/100` (CRITICAL)
- **AI Recommendation:** `REROUTE_TO_COLD_STORAGE` (8.4 km away, Cost: ₹2,400, ETA: 23 mins)
- **Governance & Approval:** SAP Rules 3 & 4 enforce Manager Sign-Off
- **Recovery Outcome:** Vehicle rerouted, temperature restored, shipment status updated to `RECOVERED`, full audit trail tagged with correlation ID `CORR-PS1026-001`.

---

## 2. Technology Stack

- **Frontend:** Next.js 14 (App Router), React, TypeScript, Tailwind CSS, Recharts, Lucide React, Leaflet Maps.
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, WebSockets, PyJWT, passlib.
- **Agents:** 
  1. *Disruption Sensing Agent* (Deterministic threshold & risk scoring)
  2. *Scenario Planning Agent* (LLM scenario reasoning & ranking)
  3. *Execution Agent* (Governance validation & state transition engine)
  4. *Compliance Audit Agent* (Append-only immutable audit ledger)
- **SAP Integration:** `SAPGovernanceInterface` with `MockSAPGovernanceService` enforcing ABAP Rules 1–5.
- **Database:** SQLite (default for friction-free dev) / PostgreSQL (production abstraction).

---

## 3. Quick Start & Setup

### Prerequisites
- Python 3.12+
- Node.js v18+ / npm

### Step 1: Clone & Configure
```bash
cp .env.example .env
```

### Step 2: Run Backend
```bash
# From workspace root
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python3 -m backend.app.main
```
Backend API will start at `http://localhost:8000`. API docs available at `http://localhost:8000/docs`.

### Step 3: Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend Control Tower will open at `http://localhost:3000`.

---

## 4. Documentation Index

- [Architecture Specification](docs/architecture.md)
- [REST & WebSocket API Guide](docs/api.md)
- [Agentic Pipeline Architecture](docs/agents.md)
- [SAP Governance & ABAP Business Rules](docs/sap-integration.md)
- [Cybersecurity & RBAC Security Model](docs/security.md)
- [Hackathon Demo Execution Guide](docs/demo.md)
- [Testing Strategy & Test Suite](docs/testing.md)
- [Known Bounded Scope & Limitations](docs/known-limitations.md)

---

## 5. License
MIT License.
