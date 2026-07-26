"""More unit tests for Phase 13 Strategic Planning System."""

import pytest
from backend.cognitive_os.planner.action_node import ActionNode
from backend.cognitive_os.planner.plan_executor import PlanExecutor
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.context.world_model import WorldModel


def test_action_node_defaults():
    node = ActionNode(name="TestNode")
    assert node.name == "TestNode"
    assert node.energy_cost == 10.0
    assert node.risk == 0.1


def test_plan_executor_completed_plan_handling():
    executor = PlanExecutor()
    plan = Plan(plan_id="p_done", actions=["Dash"], status="COMPLETED")
    wm = WorldModel(timestamp=1.0)

    act, status, reason = executor.execute_next_step(plan, wm)
    assert act is None
    assert status == "COMPLETED"
    assert "already COMPLETED" in reason
