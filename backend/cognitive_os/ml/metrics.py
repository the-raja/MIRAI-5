"""MetricsEngine module for ML Infrastructure.

Calculates standardized ML metrics for every model:
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- Inference Time (ms)
- Training Time (seconds)
- Model Size (KB)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from collections import defaultdict
import numpy as np


class ModelMetrics(BaseModel):
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    confusion_matrix: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    inference_time_ms: float = 0.0
    training_time_seconds: float = 0.0
    model_size_kb: float = 0.0


class MetricsEngine:
    @staticmethod
    def compute_all_metrics(
        predictions: List[str],
        actuals: List[str],
        inference_times_ms: Optional[List[float]] = None,
        training_time_seconds: float = 0.0,
        model_size_bytes: int = 0
    ) -> ModelMetrics:
        """Computes complete standardized metrics suite across predictions vs ground truth actuals."""
        if not predictions or len(predictions) != len(actuals):
            return ModelMetrics()

        total = len(predictions)
        correct = sum(1 for p, a in zip(predictions, actuals) if p == a)
        acc = round(correct / total, 4)

        matrix: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        actual_counts: Dict[str, int] = defaultdict(int)
        predicted_counts: Dict[str, int] = defaultdict(int)
        tp_counts: Dict[str, int] = defaultdict(int)

        for p, a in zip(predictions, actuals):
            matrix[a][p] += 1
            actual_counts[a] += 1
            predicted_counts[p] += 1
            if p == a:
                tp_counts[a] += 1

        all_labels = set(actual_counts.keys()).union(set(predicted_counts.keys()))
        precisions: List[float] = []
        recalls: List[float] = []

        for label in all_labels:
            tp = tp_counts[label]
            p_cnt = predicted_counts[label]
            a_cnt = actual_counts[label]

            p_val = tp / p_cnt if p_cnt > 0 else 0.0
            r_val = tp / a_cnt if a_cnt > 0 else 0.0

            precisions.append(p_val)
            recalls.append(r_val)

        macro_prec = round(float(np.mean(precisions)), 4) if precisions else 0.0
        macro_rec = round(float(np.mean(recalls)), 4) if recalls else 0.0

        f1 = round((2 * macro_prec * macro_rec) / (macro_prec + macro_rec), 4) if (macro_prec + macro_rec) > 0 else 0.0
        avg_inf_ms = round(float(np.mean(inference_times_ms)), 3) if inference_times_ms else 0.0
        size_kb = round(model_size_bytes / 1024.0, 2)

        conf_dict = {a: dict(preds) for a, preds in matrix.items()}

        return ModelMetrics(
            accuracy=acc,
            precision=macro_prec,
            recall=macro_rec,
            f1_score=f1,
            confusion_matrix=conf_dict,
            inference_time_ms=avg_inf_ms,
            training_time_seconds=round(training_time_seconds, 4),
            model_size_kb=size_kb
        )

    @staticmethod
    def format_metrics_report(metrics: ModelMetrics) -> str:
        """Formats complete metrics suite into a clean ML report string."""
        lines: List[str] = []
        lines.append("=" * 45)
        lines.append("STANDARDIZED ML MODEL METRICS REPORT")
        lines.append("=" * 45)
        lines.append(f"Accuracy:         {metrics.accuracy * 100:.1f}%")
        lines.append(f"Precision:        {metrics.precision * 100:.1f}%")
        lines.append(f"Recall:           {metrics.recall * 100:.1f}%")
        lines.append(f"F1 Score:         {metrics.f1_score * 100:.1f}%")
        lines.append(f"Inference Time:   {metrics.inference_time_ms:.3f} ms/sample")
        lines.append(f"Training Time:    {metrics.training_time_seconds:.3f} sec")
        lines.append(f"Model Size:       {metrics.model_size_kb:.2f} KB")
        lines.append("=" * 45)
        return "\n".join(lines)
