"""Additional unit tests for Phase 13 Strategic Planning System."""

import pytest
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.planner.plan_memory import PlanMemory
from backend.cognitive_os.planner.replanner import Replanner
from backend.cognitive_os.context.world_model import WorldModel


def test_plan_advance_bounds():
    plan = Plan(plan_id="p_bound", actions=["Dash"])
    assert plan.get_current_action() == "Dash"
    assert plan.advance() is False
    assert plan.status == "COMPLETED"
    assert plan.get_current_action() is None


def test_plan_memory_recording_update():
    memory = PlanMemory()
    rec = memory.record_plan_outcome("plan_custom", "Dagger Assassin", 90.0, True)
    assert rec["plan_id"] == "plan_custom"
    assert rec["total_uses"] == 1
    assert rec["success_rate"] == 1.0

    # Second recording
    rec2 = memory.record_plan_outcome("plan_custom", "Dagger Assassin", 60.0, False)
    assert rec2["total_uses"] == 2
    assert rec2["success_rate"] == 0.5
    assert rec2["average_damage"] == 75.0


def test_replanner_fallback_general_shift():
    replanner = Replanner()
    orig = Plan(plan_id="p_gen", actions=["Attack", "Attack"])
    wm = WorldModel(timestamp=5.0)

    new_plan, explain = replanner.check_and_replan(orig, wm, reason="Line of sight lost")
    assert new_plan.goal == "Counter Strategy"
    assert new_plan.actions == ["Block", "Dash", "HeavyAttack"]
    assert "Line of sight lost" in explain
