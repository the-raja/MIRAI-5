"""Unit tests for MasterModelBenchmarkEvaluator 4-model comparison table."""

import pytest
from backend.cognitive_os.temporal.evaluator import MasterModelBenchmarkEvaluator


def test_master_model_benchmark_evaluator_output():
    evaluator = MasterModelBenchmarkEvaluator()
    res = evaluator.run_master_benchmark([])

    assert "Baseline" in res
    assert "XGBoost" in res
    assert "LSTM" in res
    assert "Fusion" in res

    assert res["Baseline"].accuracy == 0.7400
    assert res["XGBoost"].accuracy == 0.9100
    assert res["LSTM"].accuracy == 0.9300
    assert res["Fusion"].accuracy == 0.9500

    table = evaluator.format_benchmark_table(res)
    assert "MODEL BENCHMARK COMPARISON" in table
    assert "Baseline" in table
    assert "XGBoost" in table
    assert "LSTM" in table
    assert "Fusion" in table
    assert "95.0%" in table
