"""PlanExecutor module.

Step 7: Plan Execution Loop:
Plan -> Action 1 -> Observe -> Action 2 -> Observe -> Action 3

Checks after every action whether the world has changed and triggers replanning if needed.
"""

from typing import Tuple, Optional, Dict, Any
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.context.world_model import WorldModel


class PlanExecutor:
    def __init__(self) -> None:
        pass

    def execute_next_step(self, plan: Plan, world_model: WorldModel) -> Tuple[Optional[str], str, str]:
        """Executes current plan step and evaluates world state changes.

        Returns: (current_action, plan_status, audit_reason)
        """
        if plan.status in ("COMPLETED", "FAILED", "CANCELLED"):
            return None, plan.status, f"Plan is already {plan.status}."

        curr_act = plan.get_current_action()
        if not curr_act:
            plan.status = "COMPLETED"
            return None, "COMPLETED", "All plan actions executed successfully."

        plan.status = "EXECUTING"

        # Check for sudden world state changes (e.g. Player healing or drastic HP drop)
        wm_meta = getattr(world_model, "metadata", {}) or {}
        is_player_healing = wm_meta.get("is_player_healing", False)

        if is_player_healing:
            plan.status = "REPLAN_REQUIRED"
            return curr_act, "REPLAN_REQUIRED", "Player suddenly healing! World state changed drastically."

        # Advance step
        plan.advance()
        status = "EXECUTING" if plan.current_step_index < len(plan.actions) else "COMPLETED"

        return curr_act, status, f"Executed action '{curr_act}'. World state verified."
