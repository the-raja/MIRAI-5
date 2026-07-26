"""Unit tests for AdaptationEngine parameter tuning."""

import pytest
from backend.cognitive_os.learning.adaptation import AdaptationEngine
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary


def test_adaptation_low_prediction_accuracy():
    engine = AdaptationEngine()
    ep = Episode(episode_id="ep_low_pred", timestamp=1000.0, battle_summary=BattleSummary(match_id="ep_low_pred"))

    rules = engine.evaluate_adaptations(episode=ep, prediction_accuracy=0.40)
    assert len(rules) >= 1
    low_rule = next(r for r in rules if r.target_component == "PredictionEngine")
    assert "Need Improvement" in low_rule.description


def test_adaptation_high_accuracy_increases_confidence():
    engine = AdaptationEngine()
    ep = Episode(episode_id="ep_high_pred", timestamp=1000.0, battle_summary=BattleSummary(match_id="ep_high_pred", reload_count=12))

    rules = engine.evaluate_adaptations(episode=ep, prediction_accuracy=0.96)
    assert len(rules) >= 1
    high_rule = next(r for r in rules if r.target_component == "SemanticMemory")
    assert "increasing PlayerReloadHabit confidence" in high_rule.description
