"""Unit tests for Step 11 Phase 13 verification.

Covers:
1. Goal decomposition
2. Plan generation
3. Graph traversal
4. Cost calculation
5. Plan validation
6. Plan execution
7. Replanning
8. Plan memory
9. Full integration
"""

import pytest
from backend.cognitive_os.planner.goal_decomposer import GoalDecomposer
from backend.cognitive_os.planner.planner import StrategicPlanner
from backend.cognitive_os.planner.action_graph import ActionGraph
from backend.cognitive_os.planner.cost_model import ActionCostModel
from backend.cognitive_os.planner.validator import PlanValidator, PlanReportFormatter
from backend.cognitive_os.planner.plan import Plan
from backend.cognitive_os.planner.plan_executor import PlanExecutor
from backend.cognitive_os.planner.replanner import Replanner
from backend.cognitive_os.planner.plan_memory import PlanMemory
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.event_bus.event_bus import EventBus


def test_step11_1_goal_decomposition():
    subgoals = GoalDecomposer.decompose_goal("DEFEND")
    assert "Block Heavy Attacks" in subgoals
    assert "Create Distance" in subgoals


def test_step11_2_plan_generation():
    planner = StrategicPlanner()
    plan = planner.create_plan(goal="DEFEND", beam_width=5)
    assert plan.goal == "DEFEND"
    assert len(plan.actions) > 0


def test_step11_3_graph_traversal():
    graph = ActionGraph()
    path = graph.find_action_path("Retreat", "HEAL", max_depth=3)
    assert len(path) == 3
    assert path[0] == "Retreat"


def test_step11_4_cost_calculation():
    cost_model = ActionCostModel()
    reward, risk, energy, succ = cost_model.evaluate_plan_costs(["Dash", "HeavyAttack", "Block"])
    assert reward > 0.0
    assert 0.0 <= risk <= 1.0


def test_step11_5_plan_validation():
    valid_p = Plan(plan_id="v1", actions=["Dash"], risk=0.2)
    invalid_p = Plan(plan_id="v2", actions=[], risk=0.9)

    assert PlanValidator.validate_plan_safety(valid_p) is True
    assert PlanValidator.validate_plan_safety(invalid_p) is False


def test_step11_6_plan_execution():
    executor = PlanExecutor()
    plan = Plan(plan_id="p_exec", actions=["Dash", "HeavyAttack"])
    wm = WorldModel(timestamp=1.0)

    act, status, _ = executor.execute_next_step(plan, wm)
    assert act == "Dash"
    assert status == "EXECUTING"


def test_step11_7_replanning():
    replanner = Replanner()
    plan = Plan(plan_id="p_replan", actions=["Dash", "HeavyAttack"])
    wm = WorldModel(timestamp=2.0, metadata={"is_player_healing": True})

    new_plan, explain = replanner.check_and_replan(plan, wm, reason="Player healing detected")
    assert new_plan.goal == "Pressure Heal"
    assert new_plan.actions == ["Interrupt", "HeavyAttack", "Block"]


def test_step11_8_plan_memory():
    memory = PlanMemory()
    plans = memory.query_successful_plans("Aggressive Sword Player")
    assert len(plans) > 0
    card = memory.format_plan_memory_card(plans[0])
    assert "Plan #42" in card
    assert "94%" in card


def test_step11_9_full_integration():
    bus = EventBus()
    engine = DecisionEngine(event_bus=bus)
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])

    dec = engine.make_decision(world_model=wm)
    assert dec.goal is not None
    assert dec.chosen_action is not None


def test_step11_10_plan_report_formatter():
    report = PlanReportFormatter.format_strategic_planner_report("Pressure Player", [
        {"name": "Plan A", "actions": ["Dash", "Heavy Attack", "Block"], "score": 91},
        {"name": "Plan B", "actions": ["Observe", "Counter", "Heavy Attack"], "score": 74}
    ])
    assert "Strategic Planner" in report
    assert "Plan A" in report
    assert "Score 91" in report
    assert "Expected Success" in report
