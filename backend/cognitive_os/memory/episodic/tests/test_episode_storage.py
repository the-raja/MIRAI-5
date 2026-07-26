"""Unit tests for EpisodeStorage JSON disk persistence."""

import pytest
import os
import shutil
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile, BossProfile
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.episode_storage import EpisodeStorage


@pytest.fixture
def temp_storage_dir(tmp_path):
    storage_dir = str(tmp_path / "episodes")
    yield storage_dir
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir, ignore_errors=True)


def test_episode_storage_save_and_load(temp_storage_dir):
    storage = EpisodeStorage(storage_dir=temp_storage_dir)

    episode = Episode(
        episode_id="episode_0001",
        timestamp=1000.0,
        duration=84.0,
        winner="Player",
        player_profile=PlayerProfile(
            player_id="raja",
            combat_style="Aggressive",
            reload_count=15,
            preferred_dodge="Left",
            most_used_weapon="Shotgun"
        ),
        boss_profile=BossProfile(boss_id="mirai"),
        timeline=[
            TimelineEvent(event_id="e1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0)
        ],
        battle_summary=BattleSummary(match_id="episode_0001", duration_seconds=84.0, winner="Player")
    )

    filepath = storage.save_episode(episode)
    assert os.path.exists(filepath)
    assert "episode_0001.json" in filepath

    loaded = storage.load_episode("episode_0001")
    assert loaded is not None
    assert loaded.episode_id == "episode_0001"
    assert loaded.winner == "Player"
    assert loaded.player_profile.reload_count == 15
    assert loaded.player_profile.preferred_dodge == "Left"
    assert len(loaded.timeline) == 1
    assert loaded.timeline[0].event_type == "Player Reloaded"


def test_episode_storage_list_and_count(temp_storage_dir):
    storage = EpisodeStorage(storage_dir=temp_storage_dir)

    for i in range(1, 4):
        ep = Episode(episode_id=f"episode_000{i}", timestamp=1000.0 + i)
        storage.save_episode(ep)

    assert storage.get_total_episode_count() == 3
    episodes = storage.list_episodes()
    assert episodes == ["episode_0001", "episode_0002", "episode_0003"]
