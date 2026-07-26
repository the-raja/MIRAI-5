"""Phase 4 Episodic Memory Milestone Unit Tests.

Explicitly verifies the 8 core episodic memory contracts:
1. Episode Creation
2. Episode Save
3. Episode Load
4. Timeline Integrity
5. Battle Summary Generation
6. Episode Manager
7. Storage
8. Builder
"""

import pytest
import os
import shutil
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.timeline_event import TimelineEvent
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile, BossProfile
from backend.cognitive_os.memory.episodic.episode_builder import EpisodeBuilder
from backend.cognitive_os.memory.episodic.episode_storage import EpisodeStorage
from backend.cognitive_os.memory.episodic.episode_manager import EpisodeManager
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.event_bus.event_bus import EventBus


@pytest.fixture
def temp_episodic_dir(tmp_path):
    storage_dir = str(tmp_path / "episodes")
    yield storage_dir
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir, ignore_errors=True)


def test_1_episode_creation():
    """Case 1: Episode Creation and Schema Validation."""
    ep = Episode(
        episode_id="Episode_00012",
        timestamp=1000.0,
        duration=82.0,
        winner="Player",
        player_profile=PlayerProfile(player_id="raja", reload_count=15, preferred_dodge="Left"),
        boss_profile=BossProfile(boss_id="mirai"),
        battle_summary=BattleSummary(match_id="Episode_00012", duration_seconds=82.0, winner="Player")
    )
    assert ep.episode_id == "Episode_00012"
    assert ep.duration == 82.0
    assert ep.winner == "Player"


def test_2_episode_save(temp_episodic_dir):
    """Case 2: Episode Save JSON disk serialization."""
    storage = EpisodeStorage(storage_dir=temp_episodic_dir)
    ep = Episode(episode_id="Episode_00012", timestamp=1000.0, duration=82.0, winner="Player")

    filepath = storage.save_episode(ep)
    assert os.path.exists(filepath)
    assert "Episode_00012.json" in filepath


def test_3_episode_load(temp_episodic_dir):
    """Case 3: Episode Load JSON deserialization."""
    storage = EpisodeStorage(storage_dir=temp_episodic_dir)
    ep = Episode(episode_id="Episode_00012", timestamp=1000.0, duration=82.0, winner="Player")
    storage.save_episode(ep)

    loaded = storage.load_episode("Episode_00012")
    assert loaded is not None
    assert loaded.episode_id == "Episode_00012"
    assert loaded.duration == 82.0


def test_4_timeline_integrity():
    """Case 4: Timeline Integrity filtering and timestamp ordering."""
    builder = EpisodeBuilder(match_id="Episode_00012")
    builder.start_time = 1000.0

    memories = [
        MemoryItem(id="m1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0),
        MemoryItem(id="m2", timestamp=1010.0, event_type="LowSalienceNoise", importance=20.0),  # Noise ignored (<60)
        MemoryItem(id="m3", timestamp=1020.0, event_type="Boss Heavy Attack", importance=85.0)
    ]
    builder.ingest_working_memories(memories, current_time=1020.0)

    assert len(builder.timeline) == 2
    assert builder.timeline[0].event_type == "Player Reloaded"
    assert builder.timeline[1].event_type == "Boss Heavy Attack"
    assert builder.timeline[0].timestamp < builder.timeline[1].timestamp


def test_5_battle_summary_generation():
    """Case 5: Battle Summary Generation feature matrix calculation."""
    builder = EpisodeBuilder(match_id="Episode_00012")
    builder.start_time = 1000.0

    memories = [
        MemoryItem(id="m1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0, metadata={"distance": 4.0}),
        MemoryItem(id="m2", timestamp=1010.0, event_type="Player Reloaded", importance=90.0, metadata={"distance": 6.0})
    ]
    builder.ingest_working_memories(memories, current_time=1010.0)

    episode = builder.finish_episode(winner="Player", end_time=1082.0)
    summary = episode.battle_summary

    assert summary.match_id == "Episode_00012"
    assert summary.duration_seconds == 82.0
    assert summary.reload_count == 2
    assert summary.average_distance == 5.0
    assert summary.aggression_score > 0.0


def test_6_episode_manager(temp_episodic_dir):
    """Case 6: Episode Manager CRUD and search integration."""
    bus = EventBus()
    manager = EpisodeManager(storage_dir=temp_episodic_dir, event_bus=bus)

    ep = Episode(episode_id="Episode_00012", timestamp=1000.0, duration=82.0, winner="Player")
    manager.save_episode(ep)

    assert manager.get_total_count() == 1
    found = manager.search_by_id("00012")
    assert len(found) == 1
    assert found[0].winner == "Player"


def test_7_storage(temp_episodic_dir):
    """Case 7: Storage counting and listing."""
    storage = EpisodeStorage(storage_dir=temp_episodic_dir)
    storage.save_episode(Episode(episode_id="Episode_00001", timestamp=1000.0))
    storage.save_episode(Episode(episode_id="Episode_00002", timestamp=1001.0))

    assert storage.get_total_episode_count() == 2
    assert storage.list_episodes() == ["Episode_00001", "Episode_00002"]


def test_8_builder():
    """Case 8: Builder lifecycle finish_episode."""
    builder = EpisodeBuilder(match_id="Episode_00012")
    builder.start_time = 1000.0
    episode = builder.finish_episode(winner="Boss", end_time=1082.0)

    assert episode.episode_id == "Episode_00012"
    assert episode.winner == "Boss"
    assert episode.duration == 82.0
    assert not builder.is_active
