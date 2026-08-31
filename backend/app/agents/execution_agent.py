from typing import Dict, Any
from backend.app.core.state_machine import ShipmentStateMachine, ShipmentState
from backend.app.integrations.sap_governance import sap_governance

class ExecutionAgent:
    """
    Agent 3: Governed execution agent that updates shipment states, simulates rerouting,
    and updates ETA strictly after SAP governance & human approval criteria are met.
    """

    def execute_recovery(
        self,
        current_state: str,
        approval_status: str,
        action: str,
        shipment_id: str
    ) -> Dict[str, Any]:
        
        # 1. Verify SAP rule 5 (Approval verification)
        is_permitted = sap_governance.verify_execution_permitted(approval_status, action)
        if not is_permitted:
            raise PermissionError(
                f"Execution Prohibited by SAP Governance: Action '{action}' requires approval_status='APPROVED'. Current status is '{approval_status}'."
            )

        # 2. State transition progression
        if current_state == ShipmentState.AWAITING_APPROVAL and approval_status == "APPROVED":
            next_state = ShipmentState.APPROVED
        elif current_state == ShipmentState.APPROVED:
            next_state = ShipmentState.RECOVERING
        else:
            next_state = ShipmentState.RECOVERING

        ShipmentStateMachine.validate_transition(current_state, next_state)

        # Simulated cold storage rerouting targets (Nearest cold storage 8.4 km)
        simulated_lat = 28.7841
        simulated_lon = 77.1425
        simulated_eta = 23 # minutes
        recovered_temp = 4.5 # °C after cold storage arrival

        return {
            "success": True,
            "previous_state": current_state,
            "new_state": next_state,
            "action_executed": action,
            "destination_facility": "Northern Regional Cold Storage Depot #4",
            "distance_km": 8.4,
            "simulated_latitude": simulated_lat,
            "simulated_longitude": simulated_lon,
            "new_eta_minutes": simulated_eta,
            "target_temperature": recovered_temp,
            "message": f"Execution Agent successfully initiated reroute '{action}' to Northern Regional Cold Storage Depot."
        }

execution_agent = ExecutionAgent()
