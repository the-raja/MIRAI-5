"""Unit tests for EmpiricalBenchmarkEngine."""

import pytest
from backend.cognitive_os.simulation.empirical_benchmarks import EmpiricalBenchmarkEngine


def test_baseline_comparison_results():
    baselines = EmpiricalBenchmarkEngine.get_baseline_comparison_results()
    assert len(baselines) == 5

    names = [b["architecture"] for b in baselines]
    assert "Random Boss" in names
    assert "Scripted Boss" in names
    assert "Utility AI" in names
    assert "Planner Only" in names
    assert "Full MIRAI v2" in names

    full_mirai = baselines[-1]
    assert full_mirai["win_rate_pct"] == 94.0
    assert full_mirai["prediction_accuracy_pct"] == 91.0
    assert full_mirai["latency_ms"] == 4.2


def test_ablation_study_results():
    ablations = EmpiricalBenchmarkEngine.get_ablation_study_results()
    assert len(ablations) == 5

    full = ablations[0]
    assert full["win_rate_pct"] == 94.0

    no_threat = [a for a in ablations if a["configuration"] == "Without Threat Ranking"][0]
    assert no_threat["win_rate_pct"] == 81.0

    no_planner = [a for a in ablations if a["configuration"] == "Without Planner"][0]
    assert no_planner["win_rate_pct"] == 83.0


def test_version_progression_metrics():
    prog = EmpiricalBenchmarkEngine.get_version_progression_metrics()
    assert len(prog) == 3
    assert prog[0]["version"] == "v1.0"
    assert prog[2]["version"] == "v3.0"
    assert prog[2]["pred_acc_pct"] == 91.0
    assert prog[2]["latency_ms"] == 4.2
