"""Unit tests for StrategicPlanner, PlanExecutor, and Replanner."""

import pytest
from backend.cognitive_os.planner.planner import StrategicPlanner
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.planner.plan_executor import PlanExecutor
from backend.cognitive_os.planner.replanner import Replanner
from backend.cognitive_os.context.world_model import WorldModel


def test_strategic_planner_beam_search_creation():
    planner = StrategicPlanner()
    plan = planner.create_plan(goal="Pressure Player")

    assert plan.goal == "Pressure Player"
    assert len(plan.actions) > 0
    assert plan.expected_reward > 0.0
    assert plan.status == "PLANNED"


def test_plan_executor_and_replanning_loop():
    planner = StrategicPlanner()
    executor = PlanExecutor()
    replanner = Replanner()

    # Original Plan: Dash -> HeavyAttack -> Retreat
    plan = Plan(
        plan_id="p_orig",
        goal="Pressure Player",
        actions=["Dash", "HeavyAttack", "Retreat"]
    )

    wm_normal = WorldModel(timestamp=10.0)
    act1, status1, _ = executor.execute_next_step(plan, wm_normal)
    assert act1 == "Dash"
    assert status1 == "EXECUTING"

    # World state shifts: Player suddenly heals!
    wm_heal = WorldModel(timestamp=11.0, metadata={"is_player_healing": True})
    act2, status2, reason2 = executor.execute_next_step(plan, wm_heal)

    assert status2 == "REPLAN_REQUIRED"
    assert "healing" in reason2.lower()

    # Trigger Replanner
    new_plan, explain = replanner.check_and_replan(plan, wm_heal, reason=reason2)

    assert plan.status == "CANCELLED"
    assert new_plan.goal == "Pressure Heal"
    assert new_plan.actions == ["Interrupt", "HeavyAttack", "Block"]
    assert "Pressure Heal" in explain
