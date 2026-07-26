"""MIRAI v2 — Phase 10 Model Benchmark Comparison Runner.

Executes comparative benchmarks evaluating BaselinePredictor vs XGBoostIntentModel on test data:
Outputs the exact model comparison table.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.ml.intent_prediction.evaluator import ModelBenchmarkEvaluator


def run_benchmark_demo() -> None:
    evaluator = ModelBenchmarkEvaluator()

    sample_test_rows = [
        {"distance": 2.5, "player_hp": 80.0, "last_5_actions": ["Attack", "Attack", "Attack"], "target_next_action": "RELOAD"},
        {"distance": 15.0, "player_hp": 90.0, "last_5_actions": ["Attack"], "target_next_action": "ATTACK"}
    ]

    results = evaluator.run_benchmark_comparison(sample_test_rows)
    table = evaluator.format_benchmark_table(results)

    print("\n")
    print(table)
    print("\n")


if __name__ == "__main__":
    run_benchmark_demo()
