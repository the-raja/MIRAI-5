"""ExecutionEngineV2 module.

Combines Behavior Tree & HTN Planner v2 into a unified execution engine:
Goal -> Behavior Tree -> HTN Planner -> Plan -> Execute
"""

from typing import Dict, Any, List, Tuple, Optional
from backend.cognitive_os.planner_v2.htn import HTNPlanner
from backend.cognitive_os.planner_v2.behavior_tree import BTNode, SequenceBTNode, ActionBTNode, NodeStatus
from backend.cognitive_os.planner_v2.blackboard import Blackboard


class ExecutionEngineV2:
    def __init__(self) -> None:
        self.blackboard = Blackboard()
        self.htn_planner = HTNPlanner(blackboard=self.blackboard)

    def plan_and_execute(self, goal: str = "WIN") -> Dict[str, Any]:
        """Decomposes goal via HTN and constructs reactive Behavior Tree execution loop."""
        # 1. HTN Task Network Decomposition
        htn_tasks = self.htn_planner.decompose_task_network(goal=goal)

        # 2. Behavior Tree Sequence Construction
        bt_children = [ActionBTNode(task) for task in htn_tasks]
        tree_root = SequenceBTNode(bt_children)

        # 3. Behavior Tree Tick Execution
        status = tree_root.tick(self.blackboard)

        return {
            "goal": goal,
            "htn_decomposition": htn_tasks,
            "execution_status": status.value,
            "last_action": self.blackboard.get("last_executed_action", htn_tasks[0])
        }
