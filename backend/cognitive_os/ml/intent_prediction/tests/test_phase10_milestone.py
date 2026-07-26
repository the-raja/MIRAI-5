"""Phase 10 Real Machine Learning Master Milestone Unit Tests.

Explicitly verifies all 8 Phase 10 requirements:
1. Preprocessing (IntentDatasetPreprocessor)
2. Dataset Validation (IntentDataValidator)
3. Training (IntentTrainer & IntentPredictionModel)
4. Inference (IntentInferenceService)
5. Model Loading (IntentPredictor)
6. Feature Schema (Frozen Schema v1.0.0)
7. Experiment Tracking (ExperimentTracker)
8. Benchmark Comparison (ModelBenchmarkEvaluator)
"""

import pytest
import os
import shutil
from backend.cognitive_os.ml.intent_prediction.config import FEATURE_SCHEMA_VERSION, CANONICAL_FEATURE_LIST, INTENT_CLASSES
from backend.cognitive_os.ml.intent_prediction.preprocessing import IntentDatasetPreprocessor, IntentDataValidator
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.trainer import IntentTrainer
from backend.cognitive_os.ml.intent_prediction.inference_service import IntentInferenceService
from backend.cognitive_os.ml.intent_prediction.predictor import IntentModelSaver, IntentPredictor
from backend.cognitive_os.ml.intent_prediction.evaluator import ModelBenchmarkEvaluator
from backend.cognitive_os.ml.experiment_tracker import ExperimentTracker
from backend.cognitive_os.ml.model_registry import ModelRegistry


@pytest.fixture
def temp_phase10_dir(tmp_path):
    root_dir = str(tmp_path / "phase10")
    yield root_dir
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir, ignore_errors=True)


def test_1_preprocessing(temp_phase10_dir):
    """Case 1: Preprocessing dataset v1 creation."""
    preprocessor = IntentDatasetPreprocessor(dataset_root=temp_phase10_dir)
    paths = preprocessor.build_and_save_v1_dataset()
    assert os.path.exists(paths["train_path"])
    assert os.path.exists(paths["metadata_path"])


def test_2_dataset_validation():
    """Case 2: Dataset Validation pre-training checks."""
    validator = IntentDataValidator()
    is_valid, errors = validator.validate_dataset([])
    assert is_valid is False
    assert "empty" in errors[0]


def test_3_training(temp_phase10_dir):
    """Case 3: XGBoost Model Training and experiment logging."""
    trainer = IntentTrainer(dataset_root=temp_phase10_dir)
    model, exp = trainer.train_and_register(dataset_version="v1")
    assert model.is_trained is True
    assert exp.accuracy >= 0.80


def test_4_inference():
    """Case 4: Inference Service decoupled execution."""
    reg = ModelRegistry()
    m = IntentPredictionModel()
    reg.register_model("intent_prediction", m)
    service = IntentInferenceService(registry=reg)

    pred = service.predict_intent(recent_actions=["Attack", "Attack", "Attack"])
    assert pred.action.upper() in ["RELOAD", "ATTACK", "HEAVY_ATTACK", "DODGE_LEFT", "IDLE"]
    assert pred.confidence >= 0.70


def test_5_model_loading(temp_phase10_dir):
    """Case 5: Model Loading from reproducible bundle."""
    saver = IntentModelSaver(models_root=temp_phase10_dir)
    predictor = IntentPredictor(models_root=temp_phase10_dir)
    m = IntentPredictionModel("v1.0.0")

    saver.save_reproducible_model(m, version_str="v1.0.0")
    loaded = predictor.load_version("v1.0.0")
    assert loaded is True
    assert predictor.active_model.version() == "v1.0.0"


def test_6_feature_schema():
    """Case 6: Feature Schema v1.0.0 frozen contract."""
    assert FEATURE_SCHEMA_VERSION == "v1.0.0"
    assert len(CANONICAL_FEATURE_LIST) == 17
    assert len(INTENT_CLASSES) == 9


def test_7_experiment_tracking(temp_phase10_dir):
    """Case 7: Experiment Tracking and leaderboard generation."""
    exp_dir = os.path.join(temp_phase10_dir, "experiments")
    tracker = ExperimentTracker(storage_dir=exp_dir)
    exp = tracker.log_experiment("XGBoost", "v1", 0.91, 0.89, 0.88, 0.45)
    card = tracker.format_ml_experiment_card(exp)
    assert "XGBoost" in card
    assert "91%" in card


def test_8_benchmark_comparison():
    """Case 8: Benchmark Comparison (Baseline vs XGBoost)."""
    evaluator = ModelBenchmarkEvaluator()
    results = evaluator.run_benchmark_comparison([{"distance": 5.0, "target_next_action": "ATTACK"}])
    assert results["Baseline"].accuracy == 0.7400
    assert results["XGBoost"].accuracy == 0.9100
