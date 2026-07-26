"""Unit tests for SequencePrediction and PredictionFusionEngine dual prediction pipeline."""

import pytest
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.temporal.inference import SequencePrediction, TemporalInferenceService, PredictionFusionEngine


def test_sequence_prediction_top_k_alternatives():
    service = TemporalInferenceService()
    seq_pred = service.predict_next_sequence_action(
        recent_actions=["Attack", "Attack", "DodgeLeft", "Attack", "Reload"],
        top_k=3
    )

    assert seq_pred.action == "DodgeRight"
    assert seq_pred.confidence == 0.87
    assert seq_pred.sequence_length == 5
    assert len(seq_pred.top_alternatives) == 3
    assert seq_pred.top_alternatives[0][0] == "DodgeRight"


def test_dual_prediction_fusion_engine_agreement():
    xgb_p = Prediction(prediction_id="p1", timestamp=10.0, action="Reload", confidence=0.91)
    lstm_p = Prediction(prediction_id="p2", timestamp=10.0, action="Reload", confidence=0.87)

    fused = PredictionFusionEngine.fuse_predictions(xgb_p, lstm_p)

    assert fused.action == "Reload"
    assert fused.confidence > 0.90
    assert fused.source == "Dual Prediction Fusion (XGBoost + LSTM)"
    assert "Dual Prediction Fusion (Agreement)" in fused.reason
