"""PlannerVisualizerV2 module.

Formats and renders Planner v2 (HTN + Behavior Tree) execution reports.
"""

from typing import Dict, Any, List


class PlannerVisualizerV2:
    @staticmethod
    def format_planner_v2_report(execution_result: Dict[str, Any]) -> str:
        """Formats HTN + Behavior Tree execution result into clean console report card."""
        goal = execution_result.get("goal", "WIN")
        htn_tasks = execution_result.get("htn_decomposition", [])
        status = execution_result.get("execution_status", "SUCCESS")

        lines: List[str] = []
        lines.append("====================================")
        lines.append("Planner v2 (HTN + Behavior Tree)")
        lines.append("====================================")
        lines.append(f"Goal: {goal}\n")
        lines.append("HTN Task Network Hierarchy:")
        for idx, task in enumerate(htn_tasks, 1):
            lines.append(f"  {idx}. {task}")
        lines.append(f"\nBehavior Tree Execution Status: {status}")
        lines.append("====================================")

        return "\n".join(lines)
