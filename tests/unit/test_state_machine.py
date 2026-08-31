import pytest
from backend.app.core.state_machine import ShipmentStateMachine, InvalidStateTransitionError

def test_valid_transitions():
    assert ShipmentStateMachine.validate_transition("NORMAL", "CRITICAL") is True
    assert ShipmentStateMachine.validate_transition("CRITICAL", "AWAITING_APPROVAL") is True
    assert ShipmentStateMachine.validate_transition("AWAITING_APPROVAL", "APPROVED") is True
    assert ShipmentStateMachine.validate_transition("APPROVED", "RECOVERING") is True
    assert ShipmentStateMachine.validate_transition("RECOVERING", "RECOVERED") is True

def test_invalid_direct_transition():
    with pytest.raises(InvalidStateTransitionError):
        ShipmentStateMachine.validate_transition("CRITICAL", "RECOVERING")
