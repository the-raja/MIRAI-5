"""Unit tests for Plan schema model."""

import pytest
from backend.cognitive_os.planner.plan import Plan


def test_plan_initialization_and_advancement():
    plan = Plan(
        plan_id="plan_001",
        goal="Pressure Player",
        actions=["Dash", "Heavy Attack", "Block", "Retreat"],
        expected_reward=85.0,
        risk=0.15,
        estimated_duration=4.5,
        success_probability=0.88
    )

    assert plan.plan_id == "plan_001"
    assert plan.goal == "Pressure Player"
    assert len(plan.actions) == 4
    assert plan.get_current_action() == "Dash"
    assert plan.status == "PLANNED"

    # Advance plan
    assert plan.advance() is True
    assert plan.get_current_action() == "Heavy Attack"
    assert plan.advance() is True
    assert plan.get_current_action() == "Block"
    assert plan.advance() is True
    assert plan.get_current_action() == "Retreat"

    # Complete plan
    assert plan.advance() is False
    assert plan.status == "COMPLETED"
