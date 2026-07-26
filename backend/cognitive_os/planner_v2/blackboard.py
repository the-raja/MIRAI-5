"""Blackboard module for Planner v2.

Central shared memory for Behavior Tree & HTN execution state.
"""

from typing import Dict, Any, Optional


class Blackboard:
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._data

    def clear(self) -> None:
        self._data.clear()
