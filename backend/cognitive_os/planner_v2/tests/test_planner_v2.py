"""Unit tests for Planner v2 (Behavior Tree + HTN Planner)."""

import pytest
from backend.cognitive_os.planner_v2.blackboard import Blackboard
from backend.cognitive_os.planner_v2.htn import HTNPlanner
from backend.cognitive_os.planner_v2.behavior_tree import ActionBTNode, SequenceBTNode, SelectorBTNode, NodeStatus
from backend.cognitive_os.planner_v2.execution_engine import ExecutionEngineV2
from backend.cognitive_os.planner_v2.planner_visualizer import PlannerVisualizerV2


def test_blackboard_get_set_clear():
    bb = Blackboard()
    bb.set("health", 100)
    assert bb.get("health") == 100
    assert bb.has("health") is True

    bb.clear()
    assert bb.has("health") is False


def test_htn_planner_decomposition():
    htn = HTNPlanner()
    win_tasks = htn.decompose_task_network("WIN")
    assert win_tasks == ["Reduce HP", "Pressure", "Force Reload", "Punish", "Retreat"]

    defend_tasks = htn.decompose_task_network("DEFEND")
    assert defend_tasks == ["Create Distance", "Block Heavy Attack", "Recover Energy"]


def test_behavior_tree_nodes_execution():
    bb = Blackboard()
    n1 = ActionBTNode("Dash")
    n2 = ActionBTNode("Heavy Attack")

    seq = SequenceBTNode([n1, n2])
    status = seq.tick(bb)
    assert status == NodeStatus.SUCCESS
    assert bb.get("last_executed_action") == "Heavy Attack"

    sel = SelectorBTNode([n1, n2])
    sel_status = sel.tick(bb)
    assert sel_status == NodeStatus.SUCCESS


def test_execution_engine_v2_full_pipeline():
    engine = ExecutionEngineV2()
    res = engine.plan_and_execute(goal="WIN")

    assert res["goal"] == "WIN"
    assert len(res["htn_decomposition"]) == 5
    assert res["execution_status"] == "SUCCESS"
    assert res["last_action"] == "Retreat"


def test_planner_visualizer_v2_formatting():
    report = PlannerVisualizerV2.format_planner_v2_report({
        "goal": "WIN",
        "htn_decomposition": ["Reduce HP", "Pressure", "Force Reload", "Punish", "Retreat"],
        "execution_status": "SUCCESS"
    })

    assert "Planner v2" in report
    assert "Reduce HP" in report
    assert "Force Reload" in report
