# PharmaShield — Bounded Scope & Known Limitations

## Hackathon MVP Bounded Scope
1. **Simulated Telemetry:** Sensor telemetry (temperature, GPS coordinates, humidity) is generated via an in-memory background simulator. Physical IoT hardware is intentionally out of scope.
2. **SAP Governance Adapter:** The current environment utilizes a `MockSAPGovernanceService` implementing the complete enterprise rule interface. Production deployment requires connecting to SAP S/4HANA or SAP HANA Cloud via ABAP RFC/ODATA endpoints.
3. **Database Layer:** The MVP defaults to SQLite via SQLAlchemy ORM for instant zero-friction local execution. The repository abstraction enables switching to PostgreSQL or SAP HANA with zero code modifications to core business logic.
4. **AI Scenario Generation:** LLM scenario planning uses Gemini API when `AI_API_KEY` is present, with automatic fallback to deterministic scenario rules when offline or unconfigured.
