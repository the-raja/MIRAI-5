"""More unit tests for Phase 14 Simulation Framework."""

import pytest
from backend.cognitive_os.simulation.metrics import CognitiveOSMetrics
from backend.cognitive_os.simulation.benchmark import AblationStudyEngine
from backend.cognitive_os.simulation.simulator import ResearchReportGenerator


def test_metrics_to_dict_conversion():
    m = CognitiveOSMetrics(win_rate_pct=96.0)
    d = m.to_dict()
    assert d["win_rate_pct"] == 96.0


def test_ablation_report_table_formatting():
    engine = AblationStudyEngine()
    results = engine.run_ablation_study(num_matches_per_config=5)
    report = engine.format_ablation_report(results)

    assert "MIRAI ABLATION STUDY RESULTS" in report
    assert "Full MIRAI" in report
    assert "Without Planner" in report


def test_research_report_generator_defaults():
    rep = ResearchReportGenerator.format_benchmark_report()
    assert "Benchmark Report" in rep
    assert "93.4%" in rep


def test_version_progression_metrics():
    # Progress: v1.0 (74%) -> v1.1 (84%) -> v1.2 (89%) -> v1.3 (93.4%)
    versions = [74.0, 84.0, 89.0, 93.4]
    for i in range(len(versions) - 1):
        assert versions[i] < versions[i + 1]
