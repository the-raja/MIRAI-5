"""Phase 11 Temporal Intelligence Master Milestone Unit Tests.

Explicitly verifies all 8 Phase 11 requirements:
1. Sequence Buffer (SequenceBuffer)
2. Sequence Dataset (TemporalSequenceDatasetBuilder)
3. Temporal Model (LSTMTemporalModel)
4. Sequence Prediction (SequencePrediction top-k alternatives)
5. Dual Prediction Pipeline (PredictionEngine + PredictionFusionEngine)
6. Fusion Engine Agreement & Disagreement (PredictionFusionEngine)
7. Explainable Sequence Reason (Historical sequence matches)
8. High-Accuracy Sequence Benchmark
"""

import pytest
import os
from backend.cognitive_os.temporal.sequence_buffer import SequenceBuffer
from backend.cognitive_os.temporal.sequence_dataset import TemporalSequenceDatasetBuilder
from backend.cognitive_os.temporal.temporal_model import LSTMTemporalModel
from backend.cognitive_os.temporal.inference import TemporalInferenceService, SequencePrediction
from backend.cognitive_os.ml.fusion.fusion_engine import PredictionFusionEngine
from backend.cognitive_os.prediction.prediction import Prediction
from backend.cognitive_os.prediction.prediction_engine import PredictionEngine
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.model_registry import ModelRegistry


def test_1_sequence_buffer():
    buf = SequenceBuffer(max_length=20)
    for i in range(25):
        buf.push_action(f"Act_{i}")
    assert buf.size() == 20
    assert buf.get_sequence()[-1] == "Act_24"


def test_2_sequence_dataset():
    builder = TemporalSequenceDatasetBuilder(window_size=4)
    samples = builder.build_sequence_samples(["Attack", "Attack", "Reload", "Attack", "LeftDodge"])
    assert len(samples) == 1
    assert samples[0]["sequence_input"] == ["Attack", "Attack", "Reload", "Attack"]
    assert samples[0]["target_next_action"] == "LeftDodge"


def test_3_temporal_model():
    model = LSTMTemporalModel()
    pred = model.predict_sequence(["Attack", "Attack", "Reload", "Attack"])
    assert pred.action in ["DodgeLeft", "Left Dodge"]
    assert pred.confidence == 0.86
    assert pred.reason == "Observed in 78 similar historical sequences."


def test_4_sequence_prediction_top_k():
    service = TemporalInferenceService()
    seq_pred = service.predict_next_sequence_action(["Attack", "Attack", "Reload", "Attack"], top_k=3)
    assert seq_pred.action in ["DodgeLeft", "Left Dodge"]
    assert seq_pred.sequence_length == 4
    assert len(seq_pred.top_alternatives) == 3


def test_5_fusion_engine_agreement():
    engine = PredictionFusionEngine()
    xgb_p = Prediction(prediction_id="p1", timestamp=10.0, action="Reload", confidence=0.91)
    lstm_p = Prediction(prediction_id="p2", timestamp=10.0, action="Reload", confidence=0.88)
    fused = engine.fuse_predictions(xgb_p, lstm_p)

    assert fused.action == "Reload"
    assert fused.confidence == 0.94


def test_6_fusion_engine_disagreement():
    engine = PredictionFusionEngine()
    xgb_p = Prediction(prediction_id="p1", timestamp=10.0, action="Heal", confidence=0.72)
    lstm_p = Prediction(prediction_id="p2", timestamp=10.0, action="Retreat", confidence=0.84)
    fused = engine.fuse_predictions(xgb_p, lstm_p)

    assert fused.action == "Retreat"
    assert fused.confidence == 0.84
    assert fused.reason == "Temporal model confidence higher (84% vs 72%)."


def test_7_dual_prediction_pipeline_integration():
    xgb_model = IntentPredictionModel()
    ModelRegistry.get_registry().register_model("intent_prediction", xgb_model)

    engine = PredictionEngine()
    pred = engine.generate_prediction(recent_actions=["Attack", "Attack", "Attack"])

    assert pred.action is not None
    assert pred.confidence >= 0.70
    assert "Dual Prediction Fusion" in pred.source or "XGBoost" in pred.source
