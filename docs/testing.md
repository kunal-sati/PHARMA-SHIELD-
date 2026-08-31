# PharmaShield — Testing Strategy & Verification Suite

## Test Architecture

```
tests/
├── unit/
│   ├── test_risk_engine.py       # Deterministic risk math & severity boundaries
│   ├── test_sap_rules.py         # ABAP business rules 1-5 evaluation
│   ├── test_state_machine.py     # Shipment state transitions & invalid paths
│   └── test_security.py          # RBAC permission checks & token verification
├── integration/
│   ├── test_agent_pipeline.py    # Disruption -> Planning -> SAP -> Approval -> Execution
│   └── test_api_endpoints.py     # FastAPI REST & WebSocket endpoints
└── e2e/
    └── test_vaccine_scenario.py  # Full hackathon vaccine excursion flow
```

---

## Execution Commands

### Unit & Integration Tests (Backend)
```bash
python3 -m pytest backend/tests -v
```

### Frontend Build & Type Verification
```bash
cd frontend && npm run build && npm run lint
```

### End-to-End Browser Verification
Executed via Antigravity `browser_subagent` inspecting DOM element states, charts, and API interactions.
