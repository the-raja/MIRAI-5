"""Unit tests for MetricsEngine accuracy, precision, recall, F1, inference time, and size calculation."""

import pytest
from backend.cognitive_os.ml.metrics import MetricsEngine, ModelMetrics


def test_metrics_engine_full_evaluation():
    preds = ["Reload", "Reload", "Dodge", "Attack", "Heal"]
    actuals = ["Reload", "Reload", "Dodge", "Attack", "Attack"]

    metrics = MetricsEngine.compute_all_metrics(
        predictions=preds,
        actuals=actuals,
        inference_times_ms=[0.12, 0.15, 0.11, 0.14, 0.13],
        training_time_seconds=0.045,
        model_size_bytes=2048
    )

    assert metrics.accuracy == 0.80  # 4/5
    assert metrics.precision > 0.0
    assert metrics.recall > 0.0
    assert metrics.f1_score > 0.0
    assert metrics.inference_time_ms > 0.0
    assert metrics.training_time_seconds == 0.045
    assert metrics.model_size_kb == 2.0

    report = MetricsEngine.format_metrics_report(metrics)
    assert "F1 Score:" in report
    assert "Model Size:       2.00 KB" in report
