"""Unit tests for IntentModelSaver reproducible model artifact bundle creation."""

import pytest
import os
import json
import shutil
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.predictor import IntentModelSaver, IntentPredictor


@pytest.fixture
def temp_models_bundle_dir(tmp_path):
    root_dir = str(tmp_path / "intent_models")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_reproducible_model_saver_bundle(temp_models_bundle_dir):
    saver = IntentModelSaver(models_root=temp_models_bundle_dir)
    predictor = IntentPredictor(models_root=temp_models_bundle_dir)
    model = IntentPredictionModel(model_version_str="v1.0.0")

    ver_dir = saver.save_reproducible_model(model, version_str="v1.0.0")

    # Verify all 4 required files exist in models/intent_prediction/v1.0.0/
    assert os.path.exists(os.path.join(ver_dir, "model.json"))
    assert os.path.exists(os.path.join(ver_dir, "metadata.json"))
    assert os.path.exists(os.path.join(ver_dir, "feature_schema.json"))
    assert os.path.exists(os.path.join(ver_dir, "metrics.json"))

    # Verify feature_schema.json contents
    with open(os.path.join(ver_dir, "feature_schema.json"), "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert len(schema["feature_names"]) == 17
    assert len(schema["target_classes"]) == 9

    # Verify loader restores model
    loaded = predictor.load_version("v1.0.0")
    assert loaded is True
    assert predictor.active_model is not None
    assert predictor.active_model.version() == "v1.0.0"
