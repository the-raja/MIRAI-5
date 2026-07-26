"""PlanValidator & PlanReportFormatter module.

Step 10: Formats and prints Strategic Planner candidate plan evaluation cards:

====================================
Strategic Planner
====================================
Goal
Pressure Player

Candidate Plans

Plan A
Dash
Heavy Attack
Block
Score 91

Plan B
Observe
Counter
Heavy Attack
Score 74

Chosen Plan
Plan A

Expected Success
93%
====================================
"""

from typing import List, Dict, Any, Optional
from backend.cognitive_os.planner.plan import Plan


class PlanValidator:
    @staticmethod
    def validate_plan_safety(plan: Plan) -> bool:
        """Validates that candidate plan contains valid actions and acceptable risk thresholds."""
        if not plan.actions:
            return False
        if plan.risk > 0.80:
            return False
        return True


class PlanReportFormatter:
    @staticmethod
    def format_strategic_planner_report(
        goal: str,
        candidate_plans: List[Dict[str, Any]],
        chosen_plan_label: str = "Plan A",
        expected_success_pct: int = 93
    ) -> str:
        """Formats candidate plan comparison into exact Step 10 console card string."""
        lines: List[str] = []
        lines.append("====================================")
        lines.append("Strategic Planner")
        lines.append("====================================\n")

        lines.append("Goal")
        lines.append(f"{goal}\n")

        lines.append("Candidate Plans\n")

        for p_info in candidate_plans:
            lines.append(f"{p_info['name']}")
            for act in p_info['actions']:
                lines.append(act)
            lines.append(f"Score {p_info['score']}\n")

        lines.append("Chosen Plan")
        lines.append(f"{chosen_plan_label}\n")

        lines.append("Expected Success")
        lines.append(f"{expected_success_pct}%")
        lines.append("====================================")

        return "\n".join(lines)

    @classmethod
    def print_strategic_planner_report(
        cls,
        goal: str = "Pressure Player",
        candidate_plans: Optional[List[Dict[str, Any]]] = None,
        chosen_plan_label: str = "Plan A",
        expected_success_pct: int = 93
    ) -> None:
        """Prints Strategic Planner report to stdout."""
        c_plans = candidate_plans or [
            {
                "name": "Plan A",
                "actions": ["Dash", "Heavy Attack", "Block"],
                "score": 91
            },
            {
                "name": "Plan B",
                "actions": ["Observe", "Counter", "Heavy Attack"],
                "score": 74
            }
        ]
        print(cls.format_strategic_planner_report(goal, c_plans, chosen_plan_label, expected_success_pct))
