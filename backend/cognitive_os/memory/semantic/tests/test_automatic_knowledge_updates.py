"""Integration tests for automatic knowledge extraction on Episode completion/save."""

import pytest
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager


def test_automatic_knowledge_update_on_episode_completed():
    bus = EventBus()
    semantic_manager = SemanticManager(event_bus=bus)

    knowledge_updates = []

    def on_knowledge_updated(event: Event):
        knowledge_updates.append(event.payload)

    bus.subscribe("SEMANTIC_KNOWLEDGE_UPDATED", on_knowledge_updated)

    # Publish an EPISODE_COMPLETED event onto the bus
    episode = Episode(
        episode_id="episode_auto_01",
        timestamp=1000.0,
        winner="Player",
        player_profile=PlayerProfile(
            player_id="raja",
            combat_style="Aggressive",
            reload_count=18,
            preferred_dodge="Left",
            most_used_weapon="Shotgun"
        ),
        battle_summary=BattleSummary(
            match_id="episode_auto_01",
            duration_seconds=82.0,
            winner="Player",
            reload_count=18,
            most_used_weapon="Shotgun",
            average_distance=5.5,
            preferred_dodge="Left"
        )
    )

    bus.publish(Event(event_type="EPISODE_COMPLETED", timestamp=1000.0, source="Test", payload=episode))
    bus.dispatch()

    # Verify that SemanticManager automatically extracted knowledge and emitted SEMANTIC_KNOWLEDGE_UPDATED events
    assert len(knowledge_updates) >= 3
    assert semantic_manager.memory.count() >= 3

    # Check high-confidence knowledge item extracted
    high_conf = semantic_manager.memory.get_high_confidence_knowledge(min_confidence=0.6)
    assert len(high_conf) > 0
