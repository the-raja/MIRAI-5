"""MIRAI v2 — Phase 13 Strategic Planning System Demonstrator Runner.

Executes Strategic Planner candidate plan evaluation and Plan Memory retrieval:
Outputs the exact Strategic Planner console report.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.planner.validator import PlanReportFormatter
from backend.cognitive_os.planner.plan_memory import PlanMemory


def run_planner_demo() -> None:
    print("\n")
    PlanReportFormatter.print_strategic_planner_report(
        goal="Pressure Player",
        candidate_plans=[
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
        ],
        chosen_plan_label="Plan A",
        expected_success_pct=93
    )
    print("\n")

    plan_memory = PlanMemory()
    plans = plan_memory.query_successful_plans("Aggressive Sword Player")
    card = plan_memory.format_plan_memory_card(plans[0])
    print(card)
    print("\n")


if __name__ == "__main__":
    run_planner_demo()
