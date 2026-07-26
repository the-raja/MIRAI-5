"""Additional unit tests for Planner v2 (Behavior Tree & HTN)."""

import pytest
from backend.cognitive_os.planner_v2.blackboard import Blackboard
from backend.cognitive_os.planner_v2.htn import HTNPlanner
from backend.cognitive_os.planner_v2.behavior_tree import ActionBTNode, SequenceBTNode, SelectorBTNode, NodeStatus
from backend.cognitive_os.planner_v2.execution_engine import ExecutionEngineV2


def test_blackboard_default_values():
    bb = Blackboard()
    assert bb.get("non_existent", "default") == "default"


def test_htn_planner_default_decomposition():
    htn = HTNPlanner()
    tasks = htn.decompose_task_network("UNKNOWN_GOAL")
    assert tasks == ["Pressure", "Punish", "Retreat"]


def test_selector_fallback():
    bb = Blackboard()

    class FailingBTNode(ActionBTNode):
        def tick(self, blackboard):
            return NodeStatus.FAILURE

    fail = FailingBTNode("FailAction")
    succ = ActionBTNode("SuccessAction")

    sel = SelectorBTNode([fail, succ])
    assert sel.tick(bb) == NodeStatus.SUCCESS
    assert bb.get("last_executed_action") == "SuccessAction"


def test_selector_all_failing():
    bb = Blackboard()

    class FailingBTNode(ActionBTNode):
        def tick(self, blackboard):
            return NodeStatus.FAILURE

    sel = SelectorBTNode([FailingBTNode("F1"), FailingBTNode("F2")])
    assert sel.tick(bb) == NodeStatus.FAILURE


def test_sequence_early_failure():
    bb = Blackboard()

    class FailingBTNode(ActionBTNode):
        def tick(self, blackboard):
            return NodeStatus.FAILURE

    seq = SequenceBTNode([FailingBTNode("F1"), ActionBTNode("Pass")])
    assert seq.tick(bb) == NodeStatus.FAILURE
