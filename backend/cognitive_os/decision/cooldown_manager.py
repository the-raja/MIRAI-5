"""CooldownManager module.

Tracks action usage timestamps and enforces skill/action cooldown windows.
No decision logic—pure cooldown tracking.
"""

from typing import Dict, Optional


class CooldownManager:
    def __init__(self) -> None:
        self._last_used: Dict[str, float] = {}

    def start_cooldown(self, action_name: str, timestamp: float) -> None:
        """Record the execution timestamp when an action starts its cooldown."""
        self._last_used[action_name] = timestamp

    def can_execute(self, action_name: str, cooldown_seconds: float, current_time: float) -> bool:
        """Returns True if the action is off cooldown and eligible to execute."""
        if cooldown_seconds <= 0.0:
            return True
        last = self._last_used.get(action_name, 0.0)
        return (current_time - last) >= cooldown_seconds

    def remaining_cooldown(self, action_name: str, cooldown_seconds: float, current_time: float) -> float:
        """Returns remaining cooldown duration in seconds."""
        if cooldown_seconds <= 0.0:
            return 0.0
        last = self._last_used.get(action_name, 0.0)
        elapsed = current_time - last
        return max(0.0, round(cooldown_seconds - elapsed, 2))

    def reset(self, action_name: Optional[str] = None) -> None:
        """Resets cooldown timer for a specific action or all actions if action_name is None."""
        if action_name:
            self._last_used.pop(action_name, None)
        else:
            self._last_used.clear()
