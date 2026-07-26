"""MIRAI v2 — Phase 13 Strategic Planning System Demonstrator Runner.

Executes Plan Memory retrieval and multi-step plan execution:
Outputs the exact Plan Memory console record.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.planner.plan_memory import PlanMemory


def run_planner_demo() -> None:
    plan_memory = PlanMemory()

    plans = plan_memory.query_successful_plans("Aggressive Sword Player")
    card = plan_memory.format_plan_memory_card(plans[0])

    print("\n")
    print(card)
    print("\n")


if __name__ == "__main__":
    run_planner_demo()
