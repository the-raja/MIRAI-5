"""Additional unit tests for Continuous Learning Engine components to reach 100+ tests target."""

import pytest
from backend.cognitive_os.learning.statistics import LearningStatistics
from backend.cognitive_os.learning.adaptation import AdaptationEngine, AdaptationRule
from backend.cognitive_os.learning.model_version import ModelVersionManager
from backend.cognitive_os.learning.checkpoint import CheckpointManager, CheckpointState
from backend.cognitive_os.learning.training_report import TrainingReport
from backend.cognitive_os.learning.learning_session import LearningSession
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary


def test_statistics_initial_defaults():
    stats = LearningStatistics()
    assert stats.total_episodes_analyzed == 0
    assert stats.prediction_accuracy == 0.0
    assert stats.memory_growth == 0


def test_statistics_multiple_updates():
    stats = LearningStatistics()
    stats.update_metrics(prediction_acc=0.80, fight_time=60.0)
    stats.update_metrics(prediction_acc=0.90, fight_time=100.0)

    assert stats.total_episodes_analyzed == 2
    assert stats.prediction_accuracy == 0.85
    assert stats.average_fight_time == 80.0


def test_adaptation_rule_instantiation():
    rule = AdaptationRule(
        rule_id="r1",
        target_component="UtilitySystem",
        description="Test rule",
        parameter_change={"delta": 5.0},
        confidence=0.95
    )
    assert rule.rule_id == "r1"
    assert rule.confidence == 0.95


def test_model_version_minor_bump():
    vm = ModelVersionManager()
    v_minor = vm.bump_minor("Minor version bump test")
    assert v_minor.version_id == "v1.1.0"
    assert len(vm.get_version_history()) == 2


def test_checkpoint_list_checkpoints(tmp_path):
    chk_dir = str(tmp_path / "checkpoints")
    mgr = CheckpointManager(checkpoint_dir=chk_dir)
    state = CheckpointState(checkpoint_id="chk_alpha", version="v1.0.0")
    mgr.save_checkpoint_state(state)

    files = mgr.list_checkpoints()
    assert "chk_alpha" in files


def test_training_report_formatting():
    session = LearningSession(
        episode_id="402",
        prediction_accuracy=0.88,
        decision_accuracy=0.95,
        knowledge_updates=[{"a": 1}],
        changes=["c1"],
        model_versions={"active_model_version": "v1.0.5"}
    )
    rep = TrainingReport.format_learning_report(session)
    assert "Episode\n402" in rep
    assert "Prediction Accuracy\n88%" in rep
    assert "Next Version\nv1.0.5" in rep


def test_learning_session_defaults():
    session = LearningSession(episode_id="ep_test")
    assert session.episode_id == "ep_test"
    assert session.prediction_accuracy == 0.0
    assert len(session.changes) == 0


def test_checkpoint_nonexistent_load(tmp_path):
    chk_dir = str(tmp_path / "checkpoints")
    mgr = CheckpointManager(checkpoint_dir=chk_dir)
    loaded = mgr.load_checkpoint_state("chk_nonexistent_9999")
    assert loaded is None
