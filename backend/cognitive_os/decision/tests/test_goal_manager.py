"""Unit tests for GoalManager rule-based objective selection."""

import pytest
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.decision.goal_manager import GoalManager
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.memory_item import MemoryItem


def test_rule_1_boss_low_hp_triggers_heal():
    goal_mgr = GoalManager()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"], metadata={"boss_hp_pct": 0.15})
    goal = goal_mgr.evaluate_goal(world_model=wm)
    assert goal.type == "HEAL"
    assert goal.priority == 95.0


def test_rule_2_player_low_hp_triggers_finish():
    goal_mgr = GoalManager()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"], metadata={"player_hp_pct": 0.20, "boss_hp_pct": 1.0})
    goal = goal_mgr.evaluate_goal(world_model=wm)
    assert goal.type == "FINISH"
    assert goal.priority == 93.0


def test_rule_3_player_reloading_triggers_pressure():
    goal_mgr = GoalManager()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"], metadata={"player_hp_pct": 0.80, "boss_hp_pct": 1.0})
    mem_mgr = MemoryManager()
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    goal = goal_mgr.evaluate_goal(world_model=wm, memory_manager=mem_mgr)
    assert goal.type == "PRESSURE"
    assert goal.priority == 91.0


def test_rule_4_player_hidden_triggers_search():
    goal_mgr = GoalManager()
    wm = WorldModel(timestamp=10.0, visible_entities=[], metadata={"player_hp_pct": 0.80, "boss_hp_pct": 1.0})
    goal = goal_mgr.evaluate_goal(world_model=wm)
    assert goal.type == "SEARCH"
    assert goal.priority == 85.0
