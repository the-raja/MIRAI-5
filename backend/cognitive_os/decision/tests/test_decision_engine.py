"""Unit tests for DecisionEngine operations and deterministic tie-breaking."""

import pytest
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.decision.utility_action import UtilityAction
from backend.cognitive_os.decision.goal import Goal
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_decision_engine_makes_explainable_decision():
    engine = DecisionEngine()
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])
    mem_mgr = MemoryManager()

    # Simulate player reload 1.5s ago
    mem_mgr.insert_memory(MemoryItem(id="m1", timestamp=8.5, event_type="PlayerReloading", importance=90.0))

    decision = engine.make_decision(world_model=wm, memory_manager=mem_mgr)

    assert decision.chosen_action.name == "HeavyAttack"
    assert decision.utility_score > 80.0
    assert decision.confidence > 0.70
    assert decision.goal.type == "PRESSURE"


def test_decision_engine_deterministic_tie_breaking():
    engine = DecisionEngine()

    # Set two candidate actions with exact equal base utility scores (80.0)
    act_dash = UtilityAction(id="a1", name="Dash", base_score=80.0)
    act_block = UtilityAction(id="a2", name="Block", base_score=80.0)
    engine.candidate_actions = [act_dash, act_block]

    wm = WorldModel(timestamp=10.0)

    # Secondary alphabetical tie-breaking: 'Block' comes before 'Dash'
    decision = engine.make_decision(world_model=wm)
    assert decision.chosen_action.name == "Block"
