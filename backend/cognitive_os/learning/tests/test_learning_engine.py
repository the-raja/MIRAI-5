"""Unit tests for LearningEngine post-match processing."""

import pytest
import os
import shutil
from backend.cognitive_os.learning.learning_engine import LearningEngine
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


@pytest.fixture
def temp_learning_dir(tmp_path):
    checkpoint_dir = str(tmp_path / "checkpoints")
    yield checkpoint_dir
    if os.path.exists(checkpoint_dir):
        shutil.rmtree(checkpoint_dir, ignore_errors=True)


def test_learning_engine_process_episode(temp_learning_dir):
    engine = LearningEngine()
    engine.checkpoint_manager.checkpoint_dir = temp_learning_dir

    ep = Episode(
        episode_id="battle_12",
        timestamp=1000.0,
        winner="Player",
        player_profile=PlayerProfile(player_id="raja", reload_count=15, preferred_dodge="Left"),
        battle_summary=BattleSummary(match_id="battle_12", reload_count=15, preferred_dodge="Left")
    )

    session = engine.process_completed_episode(ep)

    assert session.episode_id == "battle_12"
    assert len(session.changes) >= 2
    assert session.prediction_accuracy == 0.96
    assert session.statistics["total_episodes_analyzed"] == 1
    assert os.path.exists(os.path.join(temp_learning_dir, "chk_battle_12.json"))


def test_learning_engine_event_bus_integration(temp_learning_dir):
    bus = EventBus()
    engine = LearningEngine(event_bus=bus)
    engine.checkpoint_manager.checkpoint_dir = temp_learning_dir

    sessions = []

    def on_learning_session(event: Event):
        sessions.append(event.payload)

    bus.subscribe("LEARNING_SESSION_COMPLETED", on_learning_session)

    ep = Episode(
        episode_id="battle_13",
        timestamp=1000.0,
        winner="Boss",
        battle_summary=BattleSummary(match_id="battle_13")
    )

    bus.publish(Event(event_type="EPISODE_COMPLETED", timestamp=1000.0, source="Test", payload=ep))
    bus.dispatch()

    assert len(sessions) == 1
    assert sessions[0].episode_id == "battle_13"
