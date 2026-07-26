"""MIRAI v2 — Phase 17D Planner v2 (Behavior Tree + HTN) Demonstrator Runner.

Executes combined HTN Task Network Decomposition and Behavior Tree reactive execution:
WIN -> Reduce HP -> Pressure -> Force Reload -> Punish -> Retreat
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.planner_v2.execution_engine import ExecutionEngineV2
from backend.cognitive_os.planner_v2.planner_visualizer import PlannerVisualizerV2


def run_planner_v2_demo() -> None:
    engine = ExecutionEngineV2()
    result = engine.plan_and_execute(goal="WIN")

    print("\n")
    report = PlannerVisualizerV2.format_planner_v2_report(result)
    print(report)
    print("\n")


if __name__ == "__main__":
    run_planner_v2_demo()
