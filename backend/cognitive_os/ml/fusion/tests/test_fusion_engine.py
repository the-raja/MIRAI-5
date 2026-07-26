"""Unit tests for PredictionFusionEngine and ConfidenceCalibrator."""

import pytest
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.ml.fusion.fusion_engine import PredictionFusionEngine
from backend.cognitive_os.ml.fusion.confidence_calibrator import ConfidenceCalibrator


def test_fusion_agreement_boost():
    engine = PredictionFusionEngine()
    xgb_p = Prediction(prediction_id="p1", timestamp=10.0, action="Reload", confidence=0.91)
    lstm_p = Prediction(prediction_id="p2", timestamp=10.0, action="Reload", confidence=0.88)

    fused = engine.fuse_predictions(xgb_p, lstm_p)

    assert fused.action == "Reload"
    assert fused.confidence == 0.94
    assert fused.metadata["agreement"] is True


def test_fusion_disagreement_temporal_override():
    engine = PredictionFusionEngine()
    xgb_p = Prediction(prediction_id="p1", timestamp=10.0, action="Heal", confidence=0.72)
    lstm_p = Prediction(prediction_id="p2", timestamp=10.0, action="Retreat", confidence=0.84)

    fused = engine.fuse_predictions(xgb_p, lstm_p)

    assert fused.action == "Retreat"
    assert fused.confidence == 0.84
    assert fused.reason == "Temporal model confidence higher (84% vs 72%)."
    assert fused.metadata["agreement"] is False
