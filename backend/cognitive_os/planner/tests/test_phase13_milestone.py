"""Phase 13 Strategic Planning System Master Milestone Unit Tests.

Explicitly verifies all Phase 13 requirements:
1. Plan object as first-class cognitive entity (Plan)
2. Action Graph representation (ActionGraph & ActionNode)
3. Hierarchical Goal Decomposition (GoalDecomposer)
4. Multidimensional Cost Model (ActionCostModel)
5. Beam Search Plan Search (StrategicPlanner)
6. Step-by-Step Plan Execution (PlanExecutor)
7. Dynamic Adaptive Replanning (Replanner)
8. Plan Memory indexing & recall (PlanMemory)
"""

import pytest
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.planner.action_graph import ActionGraph
from backend.cognitive_os.planner.goal_decomposer import GoalDecomposer
from backend.cognitive_os.planner.cost_model import ActionCostModel
from backend.cognitive_os.planner.planner import StrategicPlanner
from backend.cognitive_os.planner.plan_executor import PlanExecutor
from backend.cognitive_os.planner.replanner import Replanner
from backend.cognitive_os.planner.plan_memory import PlanMemory
from backend.cognitive_os.context.world_model import WorldModel


def test_1_plan_object_contract():
    plan = Plan(plan_id="p1", goal="Pressure Player", actions=["Dash", "HeavyAttack", "Retreat"])
    assert plan.plan_id == "p1"
    assert plan.status == "PLANNED"


def test_2_action_graph():
    graph = ActionGraph()
    path = graph.find_action_path("Dash", "PRESSURE")
    assert len(path) > 0


def test_3_goal_decomposer():
    subgoals = GoalDecomposer.decompose_goal("WIN_FIGHT")
    assert "Pressure Player" in subgoals
    assert "Finish" in subgoals


def test_4_cost_model():
    cost_model = ActionCostModel()
    reward, risk, energy, succ = cost_model.evaluate_plan_costs(["Dash", "HeavyAttack"])
    assert reward > 0.0
    assert energy > 0.0


def test_5_plan_search():
    planner = StrategicPlanner()
    plan = planner.create_plan(goal="Pressure Player")
    assert len(plan.actions) > 0
    assert plan.expected_reward > 0.0


def test_6_plan_executor_and_replanning():
    executor = PlanExecutor()
    replanner = Replanner()
    plan = Plan(plan_id="p_test", actions=["Dash", "HeavyAttack"])
    wm = WorldModel(timestamp=1.0, metadata={"is_player_healing": True})

    act, status, reason = executor.execute_next_step(plan, wm)
    assert status == "REPLAN_REQUIRED"

    new_plan, explain = replanner.check_and_replan(plan, wm, reason)
    assert new_plan.goal == "Pressure Heal"
    assert new_plan.actions == ["Interrupt", "HeavyAttack", "Block"]


def test_7_plan_memory():
    memory = PlanMemory()
    plans = memory.query_successful_plans("Aggressive Sword Player")
    assert len(plans) > 0
    card = memory.format_plan_memory_card(plans[0])
    assert "Plan #42" in card
    assert "Success Rate: 94%" in card
    assert "Average Damage: 83" in card
