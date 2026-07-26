"""HTNPlanner module.

Hierarchical Task Network (HTN) Planner for Planner v2.
Decomposes long-term high-level goals into primitive action task networks:
WIN -> Reduce HP -> Pressure -> Force Reload -> Punish -> Retreat
"""

from typing import List, Dict, Any, Tuple
from backend.cognitive_os.planner_v2.blackboard import Blackboard


class HTNPlanner:
    def __init__(self, blackboard: Optional[Blackboard] = None) -> None:
        self.blackboard = blackboard or Blackboard()

    def decompose_task_network(self, goal: str = "WIN") -> List[str]:
        """Decomposes high-level goal into hierarchical primitive task sequence."""
        if goal.upper() == "WIN":
            return ["Reduce HP", "Pressure", "Force Reload", "Punish", "Retreat"]
        elif goal.upper() == "DEFEND":
            return ["Create Distance", "Block Heavy Attack", "Recover Energy"]
        else:
            return ["Pressure", "Punish", "Retreat"]
