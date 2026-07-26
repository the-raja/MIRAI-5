"""Integration tests for Prediction Engine -> Goal Manager -> Decision Engine cascade."""

import pytest
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.memory.memory_manager import MemoryManager
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_prediction_engine_goal_decision_pipeline():
    bus = EventBus()
    engine = DecisionEngine(event_bus=bus)
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])

    predictions = []
    decisions = []

    bus.subscribe("PREDICTION_GENERATED", lambda ev: predictions.append(ev.payload))
    bus.subscribe("DECISION_MADE", lambda ev: decisions.append(ev.payload))

    # Input: 3 consecutive attacks history -> Prediction: Reload -> Goal: PRESSURE -> Decision: HeavyAttack
    decision = engine.make_decision(
        world_model=wm,
        recent_actions=["Attack", "Attack", "Attack"]
    )
    bus.dispatch()

    assert len(predictions) == 1
    assert predictions[0].action == "Reload"
    assert predictions[0].confidence == 0.74

    assert len(decisions) == 1
    assert decision.goal.type == "PRESSURE"
    assert decision.chosen_action.name == "HeavyAttack"
    assert "Prediction: Player will Reload" in decision.reasoning_trace.reason_list[0]
