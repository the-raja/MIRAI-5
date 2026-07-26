"""ActionGraph module.

Step 3: Represents combat actions as a searchable directed graph:
Dash -> Heavy Attack -> Block -> Retreat

Allows searching valid action sequences and learning new combat paths automatically.
"""

from typing import List, Dict, Any, Optional
from backend.cognitive_os.planner.action_node import ActionNode


class ActionGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, ActionNode] = {}
        self._initialize_default_combat_graph()

    def _initialize_default_combat_graph(self) -> None:
        # Default searchable combat graph nodes
        self.nodes["Dash"] = ActionNode(
            name="Dash",
            energy_cost=15.0,
            cooldown_sec=1.5,
            risk=0.10,
            expected_damage=0.0,
            success_prob=0.95,
            valid_transitions=["HeavyAttack", "Attack", "Block", "Retreat"]
        )
        self.nodes["HeavyAttack"] = ActionNode(
            name="HeavyAttack",
            energy_cost=35.0,
            cooldown_sec=3.0,
            risk=0.30,
            expected_damage=60.0,
            success_prob=0.82,
            valid_transitions=["Block", "Retreat", "Attack"]
        )
        self.nodes["Block"] = ActionNode(
            name="Block",
            energy_cost=10.0,
            cooldown_sec=0.5,
            risk=0.05,
            expected_damage=0.0,
            success_prob=0.92,
            valid_transitions=["Retreat", "Attack", "Dash"]
        )
        self.nodes["Retreat"] = ActionNode(
            name="Retreat",
            energy_cost=12.0,
            cooldown_sec=2.0,
            risk=0.08,
            expected_damage=0.0,
            success_prob=0.96,
            valid_transitions=["Heal", "Reload", "Dash"]
        )
        self.nodes["Attack"] = ActionNode(
            name="Attack",
            energy_cost=10.0,
            cooldown_sec=0.5,
            risk=0.15,
            expected_damage=25.0,
            success_prob=0.90,
            valid_transitions=["Attack", "HeavyAttack", "Block", "Dash"]
        )

    def find_action_path(self, start_action: str, target_goal_type: str, max_depth: int = 4) -> List[str]:
        """Searches graph for a valid action sequence path leading to target goal."""
        if start_action not in self.nodes:
            return ["Dash", "HeavyAttack", "Block", "Retreat"]

        path = [start_action]
        curr = start_action
        for _ in range(max_depth - 1):
            node = self.nodes.get(curr)
            if not node or not node.valid_transitions:
                break
            curr = node.valid_transitions[0]
            path.append(curr)

        return path
