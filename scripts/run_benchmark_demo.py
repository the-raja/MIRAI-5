"""MIRAI v2 — Phase 11 Master Model Benchmark Comparison Runner.

Executes comparative benchmarks evaluating:
Baseline vs XGBoost vs LSTM vs Dual Prediction Fusion

Outputs the exact 4-model comparison table.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.temporal.evaluator import MasterModelBenchmarkEvaluator


def run_master_benchmark_demo() -> None:
    evaluator = MasterModelBenchmarkEvaluator()

    sample_test_rows = [
        {"distance": 2.5, "player_hp": 80.0, "last_5_actions": ["Attack", "Attack", "Attack"], "target_next_action": "RELOAD"}
    ]

    results = evaluator.run_master_benchmark(sample_test_rows)
    table = evaluator.format_benchmark_table(results)

    print("\n")
    print(table)
    print("\n")


if __name__ == "__main__":
    run_master_benchmark_demo()
