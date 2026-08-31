# PharmaShield — REST & WebSocket API Specification

## Base URL
- Local Backend: `http://localhost:8000/api`
- WebSocket Base: `ws://localhost:8000/ws`

---

## 1. Authentication API (`/api/auth`)

### POST `/api/auth/login`
Authenticates a user and issues a JWT token.
- **Request Body:**
```json
{
  "email": "manager@pharmashield.io",
  "password": "Password123!"
}
```
- **Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer",
  "user": {
    "id": "USR-002",
    "name": "Sarah Connor",
    "email": "manager@pharmashield.io",
    "role": "MANAGER"
  }
}
```

### GET `/api/auth/me`
Gets current logged-in user profile.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** User object.

---

## 2. Shipment API (`/api/shipments`)

### GET `/api/shipments`
Lists all tracked cold-chain shipments.
- **Query Parameters:** `status` (optional), `product_type` (optional).
- **Response (200 OK):**
```json
[
  {
    "shipment_id": "PS-1026",
    "product_name": "Vaccine",
    "product_type": "Temperature-sensitive pharmaceutical",
    "origin": "Delhi",
    "destination": "Chandigarh",
    "min_temperature": 2.0,
    "max_temperature": 8.0,
    "criticality": "HIGH",
    "current_status": "CRITICAL",
    "current_temperature": 9.6,
    "current_latitude": 28.7041,
    "current_longitude": 77.1025,
    "updated_at": "2026-08-26T10:31:05Z"
  }
]
```

### GET `/api/shipments/{shipment_id}`
Returns details for a single shipment including safe ranges, risk score, and current coordinates.

### POST `/api/shipments`
Creates a new shipment record.

---

## 3. Sensor API (`/api/sensors`)

### POST `/api/sensors/readings`
Ingests IoT telemetry data point for a shipment.
- **Request Body:**
```json
{
  "shipment_id": "PS-1026",
  "temperature": 9.6,
  "humidity": 55.4,
  "latitude": 28.7041,
  "longitude": 77.1025,
  "speed": 42.0,
  "traffic_level": "HIGH"
}
```
- **Response (200 OK):** Detection result & status update.

### GET `/api/shipments/{shipment_id}/readings`
Retrieves historical sensor readings for charting.

---

## 4. Simulation API (`/api/simulation`)

### POST `/api/simulation/start`
Starts normal sensor telemetry simulation.

### POST `/api/simulation/temperature-excursion`
Triggers the primary hackathon demo scenario on `PS-1026`: temperature rises stepwise from 4.2°C up to 9.6°C.

### POST `/api/simulation/reset`
Resets shipment state and sensor history to baseline.

---

## 5. Agent Pipelines API (`/api/agents`)

### POST `/api/agents/detect`
Executes Disruption Sensing Agent on target shipment.

### POST `/api/agents/plan`
Executes Scenario Planning Agent to generate recovery options.

---

## 6. SAP Governance API (`/api/governance`)

### POST `/api/governance/validate`
Validates recommendation against SAP ABAP business rules.

---

## 7. Approval API (`/api/approvals`)

### GET `/api/approvals/pending`
Returns pending approval requests.

### POST `/api/approvals/{approval_id}/approve`
Approves a recovery action. **Requires role `MANAGER` or `ADMIN`.**
- **Request Body:**
```json
{
  "comments": "Approved reroute to nearest cold storage due to severe excursion risk."
}
```

### POST `/api/approvals/{approval_id}/reject`
Rejects a recovery action. **Requires role `MANAGER` or `ADMIN`.**

---

## 8. Execution API (`/api/execution`)

### POST `/api/execution/{shipment_id}`
Triggers recovery execution. Rejects if approval requirements are not satisfied.

---

## 9. Audit API (`/api/audit`)

### GET `/api/audit`
Returns chronological audit records. Supports filtering by `shipment_id`, `event_type`, `actor`, `agent`, `severity`.

### GET `/api/shipments/{shipment_id}/audit`
Returns audit timeline for specific shipment.

---

## 10. Demo Hackathon Endpoints (`/api/demo`)

### POST `/api/demo/run-vaccine-excursion`
One-click trigger executing the complete hackathon sequence deterministically.

### POST `/api/demo/reset`
Resets demo environment.

---

## 11. WebSocket API (`/ws/shipments/{shipment_id}`)
Pushes real-time JSON frames:
```json
{
  "event": "SENSOR_TICK",
  "shipment_id": "PS-1026",
  "temperature": 9.6,
  "status": "CRITICAL",
  "risk_score": 91,
  "timestamp": "2026-08-26T10:31:05Z"
}
```
