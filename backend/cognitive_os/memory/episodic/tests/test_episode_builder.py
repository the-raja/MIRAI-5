"""Unit tests for EpisodeBuilder (The Historian)."""

import pytest
from backend.cognitive_os.memory.memory_item import MemoryItem
from backend.cognitive_os.memory.episodic.episode_builder import EpisodeBuilder
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


def test_episode_builder_timeline_and_summary_construction():
    builder = EpisodeBuilder(match_id="battle_12")
    builder.start_time = 1000.0

    memories = [
        MemoryItem(id="m1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0, related_entity="player_raja_01", metadata={"distance": 6.2}),
        MemoryItem(id="m2", timestamp=1015.0, event_type="Player Dodged Left", importance=70.0, metadata={"direction": "Left"}),
        MemoryItem(id="m3", timestamp=1040.0, event_type="BossHit", importance=80.0, metadata={"damage": 45.0})
    ]

    builder.ingest_working_memories(memories, current_time=1040.0)
    episode = builder.finish_episode(winner="Player", end_time=1084.0)

    assert episode.episode_id == "battle_12"
    assert episode.duration == 84.0
    assert episode.winner == "Player"
    assert episode.player_profile.reload_count == 1
    assert episode.player_profile.preferred_dodge == "Left"
    assert len(episode.timeline) == 3
    assert episode.battle_summary.match_id == "battle_12"


def test_episode_builder_event_bus_integration():
    bus = EventBus()
    builder = EpisodeBuilder(match_id="battle_13", event_bus=bus)
    builder.start_time = 1000.0

    completed_episodes = []

    def on_episode_completed(event: Event):
        completed_episodes.append(event.payload)

    bus.subscribe("EPISODE_COMPLETED", on_episode_completed)

    memories = [
        MemoryItem(id="m1", timestamp=1005.0, event_type="Player Reloaded", importance=90.0)
    ]
    builder.ingest_working_memories(memories, current_time=1005.0)
    builder.finish_episode(winner="Boss", end_time=1050.0)
    bus.dispatch()

    assert len(completed_episodes) == 1
    assert completed_episodes[0].episode_id == "battle_13"
    assert completed_episodes[0].winner == "Boss"
