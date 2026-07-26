"""Unit tests for BaselinePredictor action prediction targets and Prediction schema."""

import pytest
from backend.cognitive_os.prediction.baseline_predictor import BaselinePredictor


def test_baseline_predicts_reload_after_attacks():
    predictor = BaselinePredictor()
    prediction = predictor.predict(recent_actions=["Attack", "Attack", "Attack"], current_time=10.0)
    assert prediction.action == "Reload"
    assert prediction.confidence == 0.74
    assert prediction.reason == "Player reloads after 3 attacks."
    assert prediction.source == "Semantic Memory"


def test_baseline_predicts_retreat_after_dodge():
    predictor = BaselinePredictor()
    prediction = predictor.predict(recent_actions=["Dodge"], current_time=10.0)
    assert prediction.action == "Retreat"
    assert prediction.confidence == 0.65
    assert prediction.source == "Baseline Frequency Table"


def test_baseline_predicts_attack_by_default():
    predictor = BaselinePredictor()
    prediction = predictor.predict(recent_actions=["Reload"], current_time=10.0)
    assert prediction.action == "Attack"
    assert prediction.confidence == 0.70
