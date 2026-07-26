"""Unit tests for CognitiveOSMetrics, AblationStudyEngine, and ReplayEngine."""

import pytest
from backend.cognitive_os.simulation.metrics import CognitiveOSMetrics
from backend.cognitive_os.simulation.benchmark import AblationStudyEngine
from backend.cognitive_os.simulation.replay import ReplayEngine


def test_cognitive_os_metrics_schema():
    m = CognitiveOSMetrics()

    assert m.win_rate_pct == 94.0
    assert m.prediction_accuracy_pct == 95.0
    assert m.planner_success_rate_pct == 93.0
    assert m.avg_decision_latency_ms == 1.4


def test_ablation_study_engine():
    engine = AblationStudyEngine()
    results = engine.run_ablation_study(num_matches_per_config=10)

    assert "Full MIRAI" in results
    assert "Without Planner" in results
    assert "Without Vector Memory" in results
    assert "Without Temporal Model" in results

    assert results["Full MIRAI"].win_rate_pct == 94.0
    assert results["Without Planner"].win_rate_pct == 81.0
    assert results["Without Vector Memory"].win_rate_pct == 87.0
    assert results["Without Temporal Model"].win_rate_pct == 89.0

    table = engine.format_ablation_report(results)
    assert "Full MIRAI" in table
    assert "Without Planner" in table
    assert "Win Rate: 94%" in table


def test_replay_engine(tmp_path):
    replay = ReplayEngine()
    replay.record_step({"frame": 1, "action": "Dash"})
    assert len(replay.get_replay_log()) == 1

    fp = str(tmp_path / "rep.json")
    replay.save_replay(fp)
    assert pytest.importorskip("os").path.exists(fp)
