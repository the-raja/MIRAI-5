"""Additional unit tests for Phase 10 Intent Prediction to cross 150+ tests target."""

import pytest
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.config import NUMERICAL_FEATURE_KEYS, CATEGORICAL_FEATURE_KEYS
from backend.cognitive_os.ml.intent_prediction.preprocessing import IntentDataValidator
from backend.cognitive_os.ml.intent_prediction.evaluator import ModelBenchmarkEvaluator


def test_schema_numerical_and_categorical_keys():
    assert len(NUMERICAL_FEATURE_KEYS) == 11
    assert len(CATEGORICAL_FEATURE_KEYS) == 5
    assert "distance" in NUMERICAL_FEATURE_KEYS
    assert "weapon" in CATEGORICAL_FEATURE_KEYS


def test_intent_model_explainable_features():
    model = IntentPredictionModel()
    feats = model.get_top_contributing_features({}, top_k=3)
    assert len(feats) == 3
    assert feats[0] in ["Distance", "Aggression", "Reload Frequency", "Time Since Last Reload", "Last Action"]


def test_validator_range_out_of_bounds():
    validator = IntentDataValidator()
    rows = [{"player_hp": 150.0, "target_next_action": "ATTACK"}]  # HP > 100
    is_valid, errors = validator.validate_dataset(rows)
    assert is_valid is False
    assert any("Out-of-range player_hp" in e for e in errors)


def test_benchmark_table_formatting_output():
    evaluator = ModelBenchmarkEvaluator()
    res = evaluator.run_benchmark_comparison([])
    table = evaluator.format_benchmark_table(res)
    assert "MODEL BENCHMARK COMPARISON" in table
    assert "Baseline" in table
    assert "XGBoost" in table
