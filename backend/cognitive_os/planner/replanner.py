"""Replanner module.

Step 8: Adaptive Dynamic Replanning.
When world state changes (e.g. Player suddenly heals):
Old Plan: Cancelled -> New Goal: Pressure Heal -> New Plan: Interrupt -> Heavy Attack -> Block

Plans are not fixed—they adapt dynamically to runtime events.
"""

from typing import Tuple, Dict, Any, Optional
import time
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.context.world_model import WorldModel


class Replanner:
    def __init__(self) -> None:
        pass

    def check_and_replan(
        self,
        current_plan: Plan,
        world_model: WorldModel,
        reason: str = "World state changed"
    ) -> Tuple[Plan, str]:
        """Cancels old plan and generates new adaptive plan based on new world state."""
        # 1. Cancel old plan
        current_plan.status = "CANCELLED"

        wm_meta = getattr(world_model, "metadata", {}) or {}
        is_player_healing = wm_meta.get("is_player_healing", False)

        # 2. Formulate new goal and adaptive actions
        if is_player_healing or "healing" in reason.lower():
            new_goal = "Pressure Heal"
            new_actions = ["Interrupt", "HeavyAttack", "Block"]
            explain_reason = "Old Plan Cancelled -> New Goal: Pressure Heal -> New Plan: Interrupt -> HeavyAttack -> Block"
        else:
            new_goal = "Counter Strategy"
            new_actions = ["Block", "Dash", "HeavyAttack"]
            explain_reason = f"Old Plan Cancelled ({reason}) -> Adaptive Re-plan executed."

        # 3. Construct new adapted Plan
        new_plan = Plan(
            plan_id=f"plan_replan_{int(time.time()*1000)}",
            goal=new_goal,
            actions=new_actions,
            expected_reward=90.0,
            risk=0.20,
            estimated_duration=round(len(new_actions) * 1.0, 1),
            success_probability=0.85,
            status="EXECUTING"
        )

        return new_plan, explain_reason
