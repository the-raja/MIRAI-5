"""Unit tests for ActionGraph, GoalDecomposer, and ActionCostModel."""

import pytest
from backend.cognitive_os.planner.action_graph import ActionGraph
from backend.cognitive_os.planner.goal_decomposer import GoalDecomposer
from backend.cognitive_os.planner.cost_model import ActionCostModel


def test_action_graph_search_path():
    graph = ActionGraph()
    path = graph.find_action_path(start_action="Dash", target_goal_type="PRESSURE", max_depth=4)

    assert len(path) == 4
    assert path[0] == "Dash"
    assert path[1] in ["HeavyAttack", "Attack", "Block", "Retreat"]


def test_goal_decomposer_hierarchical_subgoals():
    subgoals = GoalDecomposer.decompose_goal("WIN_FIGHT")

    assert len(subgoals) == 4
    assert subgoals[0] == "Pressure Player"
    assert subgoals[1] == "Reduce HP"
    assert subgoals[2] == "Interrupt Reload"
    assert subgoals[3] == "Finish"


def test_action_cost_model_multidimensional_evaluation():
    cost_model = ActionCostModel()
    reward, risk, energy, succ_prob = cost_model.evaluate_plan_costs(["Dash", "HeavyAttack", "Block", "Retreat"])

    assert reward > 0.0
    assert 0.0 <= risk <= 1.0
    assert energy > 0.0
    assert 0.0 <= succ_prob <= 1.0
