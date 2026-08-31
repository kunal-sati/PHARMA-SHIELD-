# PharmaShield — Cybersecurity & Access Control Specification

## 1. Authentication & Security Architecture
PharmaShield implements multi-layered cybersecurity controls across API endpoints, data persistence, and governance interfaces.

```
[ Client Request ] 
       │
       ▼
 [ CORS Guard ]
       │
       ▼
 [ JWT Authentication Middleware ]
       │
       ▼
 [ Server-Side Role-Based Authorization (RBAC) ]
       │
       ▼
 [ Pydantic Schema Input Validation ]
       │
       ▼
 [ SAP Governance Rule Enforcement ]
       │
       ▼
 [ Audit Logging Ledger ]
```

---

## 2. Role-Based Access Control (RBAC) Matrix

| Role | View Shipments / Alerts | View Audit Logs | Trigger Simulation | Approve / Reject Recovery Actions | System Config / Reset |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **OPERATOR** | ✅ | ❌ | ✅ | ❌ (Forbidden) | ❌ |
| **MANAGER** | ✅ | ✅ | ✅ | ✅ (Authorized) | ❌ |
| **AUDITOR** | ✅ | ✅ | ❌ | ❌ (Forbidden) | ❌ |
| **ADMIN** | ✅ | ✅ | ✅ | ✅ (Authorized) | ✅ |

---

## 3. Server-Side Guard Mechanisms
1. **Never Trust Frontend Role Information:** Roles are decoded from verified JWT claims on the backend server.
2. **Approval Endpoint Protection:** Calling `/api/approvals/{id}/approve` checks `user.role in ['MANAGER', 'ADMIN']`. Unauthorized calls return HTTP 403 Forbidden.
3. **Execution Guarding:** The `ExecutionAgent` verifies `approval.status == 'APPROVED'` directly from the database before state transition to `RECOVERING`.
4. **Input Sanitization & Schema Enforcement:** All API payloads are validated via strict Pydantic schemas. Malformed AI or user inputs are immediately rejected.
5. **No Secret Exposure:** Credentials, JWT secret, and API keys are read strictly from environment variables (`.env`). `.env` is excluded via `.gitignore`.
