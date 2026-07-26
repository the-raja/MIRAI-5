"""More unit tests for Phase 10 Intent Prediction to cross 150+ tests target."""

import pytest
import os
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.predictor import IntentModelSaver, IntentPredictor
from backend.cognitive_os.ml.intent_prediction.preprocessing import IntentDatasetPreprocessor


def test_intent_model_save_and_load_instance(tmp_path):
    model_dir = str(tmp_path / "model_save_test")
    model = IntentPredictionModel("v2.0.0")

    filepath = os.path.join(model_dir, "model.json")
    model.save(filepath)
    assert os.path.exists(filepath)

    model2 = IntentPredictionModel()
    assert model2.load(filepath) is True
    assert model2.version() == "v2.0.0"


def test_intent_predictor_load_nonexistent(tmp_path):
    predictor = IntentPredictor(models_root=str(tmp_path / "models"))
    assert predictor.load_version("v99.99") is False


def test_intent_dataset_preprocessor_synthetic_generation():
    preprocessor = IntentDatasetPreprocessor()
    samples = preprocessor.generate_synthetic_samples(num_samples=50)
    assert len(samples) == 50
    assert "target_next_action" in samples[0]
    assert "distance" in samples[0]


def test_intent_model_metadata_contents():
    model = IntentPredictionModel()
    meta = model.metadata()
    assert meta["name"] == "XGBoost Intent Model"
    assert meta["algorithm"] == "Gradient Boosted Decision Trees (XGBoost)"
    assert len(meta["classes"]) == 9
