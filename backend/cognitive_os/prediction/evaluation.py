"""Evaluation module for ML Predictors.

Tracks prediction outcomes against actual player actions and calculates:
- Overall Accuracy
- Precision per action
- Recall per action
- Confusion Matrix (Actual vs Predicted)
- Per-action Accuracy

Establishes standard ML evaluation benchmarks for baseline and future ML models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from collections import defaultdict


class EvaluationMetrics(BaseModel):
    total_samples: int = 0
    correct_predictions: int = 0
    accuracy: float = 0.0
    precision: Dict[str, float] = Field(default_factory=dict)
    recall: Dict[str, float] = Field(default_factory=dict)
    per_action_accuracy: Dict[str, float] = Field(default_factory=dict)
    confusion_matrix: Dict[str, Dict[str, int]] = Field(default_factory=dict)


class PredictionEvaluator:
    def __init__(self) -> None:
        self.total_samples: int = 0
        self.correct_predictions: int = 0
        self._history: List[Dict[str, str]] = []
        # Confusion matrix structure: actual -> predicted -> count
        self.matrix: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.actual_counts: Dict[str, int] = defaultdict(int)
        self.predicted_counts: Dict[str, int] = defaultdict(int)
        self.correct_per_action: Dict[str, int] = defaultdict(int)

    def record_outcome(self, predicted_action: str, actual_action: str) -> None:
        """Records a single prediction vs actual outcome pair."""
        self.total_samples += 1
        self._history.append({"predicted": predicted_action, "actual": actual_action})

        self.matrix[actual_action][predicted_action] += 1
        self.actual_counts[actual_action] += 1
        self.predicted_counts[predicted_action] += 1

        if predicted_action == actual_action:
            self.correct_predictions += 1
            self.correct_per_action[actual_action] += 1

    def compute_metrics(self) -> EvaluationMetrics:
        """Computes accuracy, precision, recall, and confusion matrix metrics."""
        if self.total_samples == 0:
            return EvaluationMetrics()

        accuracy = round(self.correct_predictions / self.total_samples, 4)
        precision_map: Dict[str, float] = {}
        recall_map: Dict[str, float] = {}
        per_action_acc_map: Dict[str, float] = {}

        all_actions = set(self.actual_counts.keys()).union(set(self.predicted_counts.keys()))

        for act in all_actions:
            corr = self.correct_per_action[act]
            pred_count = self.predicted_counts[act]
            act_count = self.actual_counts[act]

            prec = round(corr / pred_count, 4) if pred_count > 0 else 0.0
            rec = round(corr / act_count, 4) if act_count > 0 else 0.0
            p_acc = rec  # Per-action accuracy (recall)

            precision_map[act] = prec
            recall_map[act] = rec
            per_action_acc_map[act] = p_acc

        # Format confusion matrix dict
        conf_dict = {act: dict(preds) for act, preds in self.matrix.items()}

        return EvaluationMetrics(
            total_samples=self.total_samples,
            correct_predictions=self.correct_predictions,
            accuracy=accuracy,
            precision=precision_map,
            recall=recall_map,
            per_action_accuracy=per_action_acc_map,
            confusion_matrix=conf_dict
        )

    def format_report(self) -> str:
        """Generates a human-readable ML Evaluation Report string."""
        metrics = self.compute_metrics()
        lines: List[str] = []
        lines.append("=" * 45)
        lines.append("PREDICTION ENGINE ML EVALUATION REPORT")
        lines.append("=" * 45)
        lines.append(f"Total Samples Tested: {metrics.total_samples}")
        lines.append(f"Overall Accuracy:     {metrics.accuracy * 100:.1f}%\n")

        lines.append("Per-Action Precision & Recall")
        lines.append("-----------------------------")
        for act in sorted(metrics.precision.keys()):
            prec = metrics.precision[act] * 100.0
            rec = metrics.recall[act] * 100.0
            lines.append(f"{act:<14} | Precision: {prec:5.1f}% | Recall: {rec:5.1f}%")

        lines.append("\nConfusion Matrix (Rows: Actual, Cols: Predicted)")
        lines.append("------------------------------------------------")
        for actual, preds in metrics.confusion_matrix.items():
            pred_str = ", ".join([f"{p}:{c}" for p, c in preds.items()])
            lines.append(f"Actual {actual:<10} -> [{pred_str}]")

        lines.append("=" * 45)
        return "\n".join(lines)
