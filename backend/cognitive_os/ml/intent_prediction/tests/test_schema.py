"""Unit tests for Intent Prediction frozen feature schema v1.0.0."""

import pytest
from backend.cognitive_os.ml.intent_prediction.config import (
    FEATURE_SCHEMA_VERSION,
    CANONICAL_FEATURE_LIST,
    INTENT_CLASSES,
    NUMERICAL_FEATURE_KEYS,
    CATEGORICAL_FEATURE_KEYS
)


def test_frozen_schema_contract():
    assert FEATURE_SCHEMA_VERSION == "v1.0.0"
    assert len(CANONICAL_FEATURE_LIST) == 17
    assert len(INTENT_CLASSES) == 9

    assert "distance" in CANONICAL_FEATURE_LIST
    assert "last_5_action_histogram" in CANONICAL_FEATURE_LIST
    assert "time_since_damage" in CANONICAL_FEATURE_LIST
    assert "boss_cooldown" in CANONICAL_FEATURE_LIST

    assert "RELOAD" in INTENT_CLASSES
    assert "DODGE_LEFT" in INTENT_CLASSES
    assert "HEAVY_ATTACK" in INTENT_CLASSES
