from typing import Set

class ShipmentState:
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    RECOVERING = "RECOVERING"
    RECOVERED = "RECOVERED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class InvalidStateTransitionError(Exception):
    def __init__(self, current_state: str, new_state: str):
        super().__init__(f"Invalid shipment state transition from '{current_state}' to '{new_state}'")
        self.current_state = current_state
        self.new_state = new_state


class ShipmentStateMachine:
    """
    Centralized state transition validator for PharmaShield shipments.
    Enforces valid cold-chain lifecycle progressions.
    """

    ALLOWED_TRANSITIONS: dict[str, Set[str]] = {
        ShipmentState.NORMAL: {ShipmentState.WARNING, ShipmentState.CRITICAL},
        ShipmentState.WARNING: {ShipmentState.NORMAL, ShipmentState.CRITICAL},
        ShipmentState.CRITICAL: {ShipmentState.AWAITING_APPROVAL, ShipmentState.FAILED},
        ShipmentState.AWAITING_APPROVAL: {ShipmentState.APPROVED, ShipmentState.REJECTED},
        ShipmentState.APPROVED: {ShipmentState.RECOVERING},
        ShipmentState.RECOVERING: {ShipmentState.RECOVERED, ShipmentState.FAILED},
        ShipmentState.RECOVERED: {ShipmentState.NORMAL}, # Can reset or complete
        ShipmentState.REJECTED: {ShipmentState.CRITICAL, ShipmentState.NORMAL},
        ShipmentState.FAILED: {ShipmentState.NORMAL}
    }

    @classmethod
    def validate_transition(cls, current_state: str, new_state: str) -> bool:
        if current_state == new_state:
            return True
        allowed = cls.ALLOWED_TRANSITIONS.get(current_state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(current_state, new_state)
        return True
