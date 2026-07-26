"""Unit tests for PredictionEvaluator ML metrics calculation."""

import pytest
from backend.cognitive_os.prediction.evaluation import PredictionEvaluator


def test_evaluator_accuracy_precision_recall():
    evaluator = PredictionEvaluator()

    # 10 sample predictions
    # 5 Reload predictions (4 correct, 1 wrong)
    evaluator.record_outcome("Reload", "Reload")
    evaluator.record_outcome("Reload", "Reload")
    evaluator.record_outcome("Reload", "Reload")
    evaluator.record_outcome("Reload", "Reload")
    evaluator.record_outcome("Reload", "Dodge")

    # 5 Dodge predictions (4 correct, 1 wrong)
    evaluator.record_outcome("Dodge", "Dodge")
    evaluator.record_outcome("Dodge", "Dodge")
    evaluator.record_outcome("Dodge", "Dodge")
    evaluator.record_outcome("Dodge", "Dodge")
    evaluator.record_outcome("Dodge", "Reload")

    metrics = evaluator.compute_metrics()

    assert metrics.total_samples == 10
    assert metrics.correct_predictions == 8
    assert metrics.accuracy == 0.80

    assert metrics.precision["Reload"] == 0.80  # 4/5
    assert metrics.recall["Reload"] == 0.80     # 4/5
    assert "Reload" in metrics.confusion_matrix

    report = evaluator.format_report()
    assert "EVALUATION REPORT" in report
    assert "Overall Accuracy:     80.0%" in report
