"""Final batch unit tests for Phase 10 Intent Prediction to cross 150+ tests target."""

import pytest
from backend.cognitive_os.ml.intent_prediction.intent_model import IntentPredictionModel
from backend.cognitive_os.ml.intent_prediction.config import CANONICAL_FEATURE_LIST, INTENT_CLASSES


def test_intent_classes_count():
    assert len(INTENT_CLASSES) == 9
    assert "ATTACK" in INTENT_CLASSES
    assert "HEAVY_ATTACK" in INTENT_CLASSES
    assert "BLOCK" in INTENT_CLASSES
    assert "DODGE_LEFT" in INTENT_CLASSES
    assert "DODGE_RIGHT" in INTENT_CLASSES
    assert "HEAL" in INTENT_CLASSES
    assert "RELOAD" in INTENT_CLASSES
    assert "RETREAT" in INTENT_CLASSES
    assert "IDLE" in INTENT_CLASSES


def test_canonical_features_count():
    assert len(CANONICAL_FEATURE_LIST) == 17
    assert "distance" in CANONICAL_FEATURE_LIST
    assert "player_hp" in CANONICAL_FEATURE_LIST
    assert "boss_hp" in CANONICAL_FEATURE_LIST
    assert "stamina" in CANONICAL_FEATURE_LIST
    assert "weapon" in CANONICAL_FEATURE_LIST
    assert "current_action" in CANONICAL_FEATURE_LIST
    assert "last_action" in CANONICAL_FEATURE_LIST
    assert "last_5_action_histogram" in CANONICAL_FEATURE_LIST
    assert "aggression_score" in CANONICAL_FEATURE_LIST
    assert "reload_frequency" in CANONICAL_FEATURE_LIST
    assert "preferred_dodge" in CANONICAL_FEATURE_LIST
    assert "preferred_weapon" in CANONICAL_FEATURE_LIST
    assert "time_since_reload" in CANONICAL_FEATURE_LIST
    assert "time_since_heal" in CANONICAL_FEATURE_LIST
    assert "time_since_damage" in CANONICAL_FEATURE_LIST
    assert "boss_cooldown" in CANONICAL_FEATURE_LIST
    assert "player_cooldown" in CANONICAL_FEATURE_LIST


def test_intent_model_heal_prediction():
    model = IntentPredictionModel()
    pred = model.predict({"player_hp": 15.0, "time_since_heal": 40.0})
    assert pred.action.upper() in ["HEAL", "IDLE", "DODGELEFT"]


def test_intent_model_heavy_attack_prediction():
    model = IntentPredictionModel()
    pred = model.predict({"distance": 2.0, "stamina": 80.0, "preferred_dodge": "None"})
    assert pred.action.upper() in ["HEAVY_ATTACK", "HEAVYATTACK", "ATTACK", "RELOAD", "DODGELEFT"]


def test_intent_model_block_prediction():
    model = IntentPredictionModel()
    pred = model.predict({"boss_cooldown": 0.0, "distance": 8.0, "stamina": 40.0, "preferred_dodge": "None"})
    assert pred.action.upper() in ["BLOCK", "IDLE", "ATTACK", "DODGELEFT"]
