"""Planner API module for Runtime."""

from typing import Dict, Any
from backend.cognitive_os.planner.planner import StrategicPlanner
from backend.cognitive_os.planner.plan import Plan


class PlannerAPI:
    def __init__(self, planner: StrategicPlanner) -> None:
        self.planner = planner

    def create_plan(self, goal: str = "Pressure Player") -> Plan:
        return self.planner.create_plan(goal=goal)
