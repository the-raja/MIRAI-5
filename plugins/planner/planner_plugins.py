"""Planner Plugin Ecosystem.

Swappable planner implementations:
- AStarPlugin
- BeamSearchPlugin
- GOAPPlugin
"""

from typing import List, Dict, Any


class BasePlannerPlugin:
    def plan(self, goal: str) -> Dict[str, Any]:
        raise NotImplementedError


class AStarPlugin(BasePlannerPlugin):
    def plan(self, goal: str) -> Dict[str, Any]:
        return {"goal": goal, "actions": ["Dash", "Attack", "Retreat"], "plugin": "A*"}


class BeamSearchPlugin(BasePlannerPlugin):
    def plan(self, goal: str) -> Dict[str, Any]:
        return {"goal": goal, "actions": ["Dash", "HeavyAttack", "Block"], "plugin": "BeamSearch"}


class GOAPPlugin(BasePlannerPlugin):
    def plan(self, goal: str) -> Dict[str, Any]:
        return {"goal": goal, "actions": ["Interrupt", "HeavyAttack", "Block"], "plugin": "GOAP"}
