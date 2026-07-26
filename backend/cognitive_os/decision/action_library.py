"""ActionLibrary module.

Central registry for candidate actions available to the Decision Cortex.
Supports dynamic registration, retrieval, enabling, and disabling of actions.
"""

from typing import List, Dict, Optional
from backend.cognitive_os.decision.utility_action import UtilityAction, create_standard_action_set


class ActionLibrary:
    def __init__(self) -> None:
        self._actions: Dict[str, UtilityAction] = {}
        self._disabled_actions: set = set()

        for action in create_standard_action_set():
            self.register_action(action)

    def register_action(self, action: UtilityAction) -> None:
        """Register a new candidate action into the library."""
        self._actions[action.name] = action

    def unregister_action(self, action_name: str) -> bool:
        """Unregister an action by name."""
        if action_name in self._actions:
            del self._actions[action_name]
            return True
        return False

    def enable_action(self, action_name: str) -> None:
        """Enable an action for selection."""
        self._disabled_actions.discard(action_name)

    def disable_action(self, action_name: str) -> None:
        """Disable an action from being selected."""
        self._disabled_actions.add(action_name)

    def is_enabled(self, action_name: str) -> bool:
        """Check if an action is currently enabled."""
        return action_name in self._actions and action_name not in self._disabled_actions

    def get_action(self, action_name: str) -> Optional[UtilityAction]:
        """Retrieve an action by name."""
        return self._actions.get(action_name)

    def get_active_actions(self) -> List[UtilityAction]:
        """Returns all currently enabled candidate actions."""
        return [act for name, act in self._actions.items() if name not in self._disabled_actions]

    def get_all_actions(self) -> List[UtilityAction]:
        """Returns all registered candidate actions regardless of enabled state."""
        return list(self._actions.values())
