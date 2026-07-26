"""Phase 8 Continuous Learning Engine Milestone Unit Tests.

Explicitly verifies all 7 continuous learning core contracts:
1. Learning Session
2. Statistics
3. Adaptation
4. Versioning
5. Checkpoints
6. Reports
7. Full Learning Pipeline
"""

import pytest
import os
import shutil
from backend.cognitive_os.learning.learning_session import LearningSession
from backend.cognitive_os.learning.statistics import LearningStatistics
from backend.cognitive_os.learning.adaptation import AdaptationEngine, AdaptationRule
from backend.cognitive_os.learning.model_version import ModelVersionManager
from backend.cognitive_os.learning.checkpoint import CheckpointManager, CheckpointState
from backend.cognitive_os.learning.training_report import TrainingReport
from backend.cognitive_os.learning.learning_engine import LearningEngine
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


@pytest.fixture
def temp_learning_dir(tmp_path):
    chk_dir = str(tmp_path / "checkpoints")
    yield chk_dir
    if os.path.exists(chk_dir):
        shutil.rmtree(chk_dir, ignore_errors=True)


def test_1_learning_session():
    """Case 1: Learning Session model structure."""
    session = LearningSession(
        episode_id="34",
        prediction_accuracy=0.82,
        decision_accuracy=0.91,
        changes=["Updated utility score", "Increased confidence"],
        knowledge_updates=[{"type": "PlayerReloadHabit"}]
    )
    assert session.episode_id == "34"
    assert session.prediction_accuracy == 0.82
    assert session.decision_accuracy == 0.91


def test_2_statistics():
    """Case 2: Research Statistics calculation."""
    stats = LearningStatistics()
    stats.update_metrics(prediction_acc=0.82, decision_acc=0.91, goal_acc=0.85, fight_time=75.0)
    summary = stats.get_research_summary()
    assert summary["Prediction Accuracy"] == "82.0%"
    assert summary["Decision Accuracy"] == "91.0%"


def test_3_adaptation():
    """Case 3: Adaptation parameter tuning rules."""
    engine = AdaptationEngine()
    ep = Episode(episode_id="34", timestamp=1000.0, winner="Player", battle_summary=BattleSummary(match_id="34", reload_count=12))
    rules = engine.evaluate_adaptations(episode=ep, prediction_accuracy=0.96)
    assert len(rules) >= 1
    assert any("PlayerReloadHabit" in r.description for r in rules)


def test_4_versioning():
    """Case 4: Model Versioning lineage (Model v1 -> Model v2 -> Model v3)."""
    vm = ModelVersionManager()
    v1 = vm.get_current_version()
    v2 = vm.create_next_version("Post-match 34 adaptation")
    assert v1.version_id == "v1.0.0"
    assert v2.version_id == "v1.0.1"


def test_5_checkpoints(temp_learning_dir):
    """Case 5: Checkpoint saving and loading."""
    mgr = CheckpointManager(checkpoint_dir=temp_learning_dir)
    state = CheckpointState(checkpoint_id="chk_34", version="v1.0.1", utility_weights={"HeavyAttack": 60.0})
    filepath = mgr.save_checkpoint_state(state)
    assert os.path.exists(filepath)
    loaded = mgr.load_checkpoint_state("chk_34")
    assert loaded.version == "v1.0.1"


def test_6_reports():
    """Case 6: Training Report output formatting."""
    session = LearningSession(
        episode_id="34",
        prediction_accuracy=0.82,
        decision_accuracy=0.91,
        changes=["c1", "c2"],
        knowledge_updates=[{"t": 1}, {"t": 2}, {"t": 3}],
        statistics={"knowledge_growth": 5},
        model_versions={"active_model_version": "v0.8.14"}
    )
    report = TrainingReport.format_learning_report(session)
    assert "Learning Report" in report
    assert "Episode\n34" in report
    assert "Prediction Accuracy\n82%" in report
    assert "Next Version\nv0.8.14" in report


def test_7_full_learning_pipeline(temp_learning_dir):
    """Case 7: Full Continuous Learning Pipeline execution."""
    bus = EventBus()
    engine = LearningEngine(event_bus=bus)
    engine.checkpoint_manager.checkpoint_dir = temp_learning_dir

    episodes_processed = []
    bus.subscribe("LEARNING_SESSION_COMPLETED", lambda ev: episodes_processed.append(ev.payload))

    ep = Episode(episode_id="34", timestamp=1000.0, winner="Boss", battle_summary=BattleSummary(match_id="34", reload_count=10))
    session = engine.process_completed_episode(ep)

    assert session.episode_id == "34"
    assert os.path.exists(os.path.join(temp_learning_dir, "chk_34.json"))
