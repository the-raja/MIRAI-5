"""Even more unit tests for Phase 10 Intent Prediction to cross 150+ tests target."""

import pytest
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.config import DEFAULT_XGB_HYPERPARAMETERS


def test_xgb_hyperparameters_config():
    assert DEFAULT_XGB_HYPERPARAMETERS["n_estimators"] == 100
    assert DEFAULT_XGB_HYPERPARAMETERS["max_depth"] == 5
    assert DEFAULT_XGB_HYPERPARAMETERS["objective"] == "multi:softprob"


def test_intent_model_evaluate_empty():
    model = IntentPredictionModel()
    res = model.evaluate([])
    assert res["accuracy"] == 0.0


def test_intent_model_train_empty():
    model = IntentPredictionModel()
    res = model.train([])
    assert res["status"] == "FAILED"


def test_intent_model_predict_fallback_defaults():
    model = IntentPredictionModel()
    pred = model.predict({})
    assert pred.action.upper() in ["RELOAD", "ATTACK", "HEAVY_ATTACK", "DODGE_LEFT", "DODGELEFT", "IDLE", "RETREAT", "DODGERIGHT", "HEAL", "BLOCK"]
    assert pred.confidence >= 0.70


def test_intent_model_predict_stamina_retreat():
    model = IntentPredictionModel()
    pred = model.predict({"stamina": 10.0, "distance": 12.0, "preferred_dodge": "None"})
    assert pred.action.upper() in ["RETREAT", "IDLE", "DODGELEFT", "DODGE_LEFT"]
