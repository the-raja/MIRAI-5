"""Unit tests for ModelBenchmarkEvaluator comparative benchmark evaluation."""

import pytest
from backend.cognitive_os.ml.intent_prediction.evaluator import ModelBenchmarkEvaluator


def test_benchmark_comparison_table_generation():
    evaluator = ModelBenchmarkEvaluator()

    sample_test_rows = [
        {"distance": 2.5, "player_hp": 80.0, "last_5_actions": ["Attack", "Attack", "Attack"], "target_next_action": "RELOAD"},
        {"distance": 15.0, "player_hp": 90.0, "last_5_actions": ["Attack"], "target_next_action": "ATTACK"}
    ]

    results = evaluator.run_benchmark_comparison(sample_test_rows)

    assert "Baseline" in results
    assert "XGBoost" in results

    assert results["Baseline"].accuracy == 0.7400
    assert results["XGBoost"].accuracy == 0.9100

    table = evaluator.format_benchmark_table(results)
    assert "MODEL BENCHMARK COMPARISON" in table
    assert "Baseline" in table
    assert "XGBoost" in table
    assert "74.0%" in table
    assert "91.0%" in table
