"""Integration tests for Semantic Memory -> Inference Service -> XGBoost -> Goal Manager pipeline."""

import pytest
from backend.cognitive_os.decision.decision_engine import DecisionEngine
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.context.world_model import WorldModel
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_xgboost_intent_pipeline_integration():
    bus = EventBus()

    # Register XGBoost model in ModelRegistry
    xgb_model = IntentPredictionModel()
    ModelRegistry.get_registry().register_model("intent_prediction", xgb_model)

    engine = DecisionEngine(event_bus=bus)
    wm = WorldModel(timestamp=10.0, visible_entities=["player_raja_01"])

    predictions = []
    bus.subscribe("PREDICTION_GENERATED", lambda ev: predictions.append(ev.payload))

    decision = engine.make_decision(
        world_model=wm,
        recent_actions=["ATTACK", "ATTACK", "RELOAD"]
    )
    bus.dispatch()

    assert len(predictions) == 1
    assert predictions[0].source == "XGBoost Intent Model"
    assert decision.goal is not None
    assert decision.chosen_action is not None
