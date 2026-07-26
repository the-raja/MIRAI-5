"""Unit tests for LearningStatistics research metrics calculation."""

import pytest
from backend.cognitive_os.learning.statistics import LearningStatistics


def test_learning_statistics_metrics_computation():
    stats = LearningStatistics()

    stats.update_metrics(
        prediction_acc=0.80,
        decision_acc=0.90,
        goal_acc=0.85,
        fight_time=80.0,
        damage_dealt=500.0,
        counter_success=0.85,
        current_memory_count=12,
        current_knowledge_count=5,
        adaptations_count=3
    )

    summary = stats.get_research_summary()
    assert summary["Total Battles Analyzed"] == 1
    assert summary["Prediction Accuracy"] == "80.0%"
    assert summary["Decision Accuracy"] == "90.0%"
    assert summary["Goal Accuracy"] == "85.0%"
    assert summary["Average Fight Time"] == "80.0s"
    assert summary["Average Damage"] == "500.0"
    assert summary["Counter Success"] == "85.0%"
    assert summary["Memory Growth"] == "12 items"
    assert summary["Knowledge Growth"] == "5 rules"
    assert summary["Learning Speed"] == "3.0 adaptations/match"
