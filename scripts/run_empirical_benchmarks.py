"""MIRAI v2 — Phase 21 Empirical Benchmark & Ablation Study Demonstrator Runner.

Outputs comparative baseline evaluation table, ablation studies, and version progression metrics.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.cognitive_os.simulation.empirical_benchmarks import EmpiricalBenchmarkEngine


def run_empirical_benchmarks_demo() -> None:
    engine = EmpiricalBenchmarkEngine()

    print("\n")
    print("====================================")
    print("MIRAI Empirical Benchmark Results")
    print("====================================")

    baselines = engine.get_baseline_comparison_results()
    for b in baselines:
        print(f"{b['architecture']:<15} | Win: {b['win_rate_pct']:>4.1f}% | Damage: {b['damage_dealt']:>5.1f} | Acc: {b['prediction_accuracy_pct']:>4.1f}% | Latency: {b['latency_ms']:>3.1f}ms")

    print("\n====================================")
    print("Ablation Study Results")
    print("====================================")
    ablations = engine.get_ablation_study_results()
    for a in ablations:
        print(f"{a['configuration']:<24} -> Win Rate: {a['win_rate_pct']:>4.1f}% ({a['status']})")

    print("\n====================================")
    print("Version Progression (v1 -> v2 -> v3)")
    print("====================================")
    prog = engine.get_version_progression_metrics()
    for p in prog:
        print(f"{p['version']} | Prediction Acc: {p['pred_acc_pct']}% | Planning Success: {p['planner_success_pct']}% | Latency: {p['latency_ms']} ms")
    print("====================================\n")


if __name__ == "__main__":
    run_empirical_benchmarks_demo()
