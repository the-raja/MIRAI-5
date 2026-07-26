"""ActionCostModel module.

Step 5: Multidimensional Cost Model.
Evaluates multi-attribute costs for plan optimization:
- Energy Cost
- Cooldown Cost
- Risk
- Expected Damage
- Success Probability
"""

from typing import List, Dict, Any, Tuple
from backend.cognitive_os.planner.action_graph import ActionGraph


class ActionCostModel:
    def __init__(self, action_graph: Optional[ActionGraph] = None) -> None:
        self.action_graph = action_graph or ActionGraph()

    def evaluate_plan_costs(self, actions: List[str]) -> Tuple[float, float, float, float]:
        """Calculates total plan (expected_reward, total_risk, total_energy, success_probability)."""
        if not actions:
            return 0.0, 0.0, 0.0, 1.0

        total_damage = 0.0
        total_risk = 0.0
        total_energy = 0.0
        overall_success = 1.0

        for act in actions:
            node = self.action_graph.nodes.get(act)
            if node:
                total_damage += node.expected_damage
                total_risk += node.risk
                total_energy += node.energy_cost
                overall_success *= node.success_probability
            else:
                total_damage += 20.0
                total_risk += 0.1
                total_energy += 10.0
                overall_success *= 0.90

        expected_reward = round(total_damage - (total_risk * 10.0), 2)
        avg_risk = round(total_risk / len(actions), 4)

        return expected_reward, avg_risk, total_energy, round(overall_success, 4)
