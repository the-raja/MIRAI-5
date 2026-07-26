"""Unit tests for IntentInferenceService decoupling Cognitive OS."""

import pytest
from backend.cognitive_os.ml.intent_prediction.inference_service import IntentInferenceService
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.model_registry import ModelRegistry
from backend.cognitive_os.context.world_model import WorldModel


def test_inference_service_decoupled_prediction():
    registry = ModelRegistry()
    model = IntentPredictionModel()
    registry.register_model("intent_prediction", model)

    service = IntentInferenceService(registry=registry)
    wm = WorldModel(timestamp=10.0)

    pred = service.predict_intent(
        world_model=wm,
        recent_actions=["Attack", "Attack", "Attack", "Reload"]
    )

    assert pred.action in ["Reload", "RELOAD", "DodgeLeft", "DODGE_LEFT", "Attack", "ATTACK"]
    assert pred.confidence >= 0.70
    assert pred.source == "XGBoost Intent Model"
