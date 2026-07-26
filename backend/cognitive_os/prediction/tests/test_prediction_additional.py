"""Additional unit tests for Prediction Engine components."""

import pytest
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor


def test_prediction_model_defaults():
    pred = Prediction(action="Reload", confidence=0.74, time_horizon=2.0, reason="Test", source="Test")
    assert pred.action == "Reload"
    assert pred.confidence == 0.74
    assert pred.time_horizon == 2.0


def test_baseline_predictor_supported_actions():
    predictor = BaselinePredictor()
    assert "Reload" in predictor.SUPPORTED_PREDICTIONS
    assert "Dodge" in predictor.SUPPORTED_PREDICTIONS
    assert "Heal" in predictor.SUPPORTED_PREDICTIONS
    assert "Attack" in predictor.SUPPORTED_PREDICTIONS
    assert "Retreat" in predictor.SUPPORTED_PREDICTIONS
    assert "Block" in predictor.SUPPORTED_PREDICTIONS
