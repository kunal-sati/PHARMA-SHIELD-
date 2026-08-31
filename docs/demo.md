# PharmaShield — Hackathon Demonstration Guide

## Primary Demo Scenario: Vaccine Temperature Excursion (PS-1026)

### Key Metrics
- **Shipment ID:** `PS-1026`
- **Product:** Vaccine (Temperature-sensitive pharmaceutical)
- **Safe Range:** 2.0°C – 8.0°C
- **Origin / Destination:** Delhi to Chandigarh
- **Simulated Excursion Peak:** 9.6°C (Delay: 47 mins, Traffic: HIGH)
- **Risk Score:** ~91/100 (CRITICAL)
- **Recommendation:** `REROUTE_TO_COLD_STORAGE` (Distance: 8.4 km, Cost: ₹2,400, Time: 23 mins)

---

## Interactive Demo Workflow (3 to 4 Minutes)

| Timeline | Phase | Action | System Response |
| :--- | :--- | :--- | :--- |
| **0:00–0:20** | **Normal Monitoring** | Open Dashboard (`/dashboard`) | View live map & Normal status on `PS-1026` (4.2°C - 4.8°C). |
| **0:20–0:40** | **Excursion Trigger** | Click **"Simulate Excursion"** in Control Bar | Temp rises: 5.2°C -> 6.1°C -> 7.3°C -> 8.1°C -> 8.9°C -> **9.6°C**. Status turns **CRITICAL**. |
| **0:40–1:00** | **Detection & Risk** | View Alert Sidebar & Detail Page | Disruption Agent detects excursion; Risk Engine calculates score **91/100**. |
| **1:00–1:30** | **AI Scenario Planning** | Navigate to Decision Center (`/decisions`) | Planning Agent displays 3 options & recommends `REROUTE_TO_COLD_STORAGE`. |
| **1:30–1:50** | **SAP Governance Check** | Observe SAP Policy Status | ABAP Rules 3 & 4 enforce **"Human Approval Required"** (`AWAITING_APPROVAL`). |
| **1:50–2:20** | **Human Approval** | Open Approval Center (`/approvals`) | Log in as Manager, review metrics (₹2,400 / 23m), click **APPROVE**. |
| **2:20–2:50** | **Execution / Recovery** | Watch Live State Update | Execution Agent reroutes vehicle; status updates to **RECOVERING** then **RECOVERED**. |
| **2:50–3:30** | **Audit Trail** | Navigate to Audit Center (`/audit`) | Complete event chain visible under Correlation ID `CORR-PS1026-001`. |

---

## One-Click Reset
To reset the demonstration at any time, click **"Reset Scenario"** or call `POST /api/demo/reset`.
