"""Unit tests for CooldownManager timer tracking."""

import pytest
from backend.cognitive_os.decision.cooldown_manager import CooldownManager


def test_cooldown_manager_lifecycle():
    cm = CooldownManager()

    # Initial state: can execute
    assert cm.can_execute("HeavyAttack", cooldown_seconds=3.0, current_time=10.0) is True
    assert cm.remaining_cooldown("HeavyAttack", cooldown_seconds=3.0, current_time=10.0) == 0.0

    # Start cooldown at t=10.0
    cm.start_cooldown("HeavyAttack", timestamp=10.0)

    # At t=11.0: on cooldown (2.0s remaining)
    assert cm.can_execute("HeavyAttack", cooldown_seconds=3.0, current_time=11.0) is False
    assert cm.remaining_cooldown("HeavyAttack", cooldown_seconds=3.0, current_time=11.0) == 2.0

    # At t=13.0: off cooldown
    assert cm.can_execute("HeavyAttack", cooldown_seconds=3.0, current_time=13.0) is True
    assert cm.remaining_cooldown("HeavyAttack", cooldown_seconds=3.0, current_time=13.0) == 0.0

    # Reset specific action
    cm.start_cooldown("HeavyAttack", timestamp=13.0)
    cm.reset("HeavyAttack")
    assert cm.can_execute("HeavyAttack", cooldown_seconds=3.0, current_time=13.1) is True
