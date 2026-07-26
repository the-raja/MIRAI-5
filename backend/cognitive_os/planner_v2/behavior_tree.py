"""BehaviorTree module for Planner v2.

Handles reactive execution, interruptions, priorities, and fallback selectors.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from backend.cognitive_os.planner_v2.blackboard import Blackboard


class NodeStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class BTNode:
    def tick(self, blackboard: Blackboard) -> NodeStatus:
        raise NotImplementedError


class ActionBTNode(BTNode):
    def __init__(self, action_name: str) -> None:
        self.action_name = action_name

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        blackboard.set("last_executed_action", self.action_name)
        return NodeStatus.SUCCESS


class SequenceBTNode(BTNode):
    def __init__(self, children: List[BTNode]) -> None:
        self.children = children

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS


class SelectorBTNode(BTNode):
    def __init__(self, children: List[BTNode]) -> None:
        self.children = children

    def tick(self, blackboard: Blackboard) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status == NodeStatus.SUCCESS:
                return NodeStatus.SUCCESS
        return NodeStatus.FAILURE
