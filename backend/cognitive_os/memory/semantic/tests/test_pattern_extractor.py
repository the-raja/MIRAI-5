"""Unit tests for PatternExtractor and SemanticMemory."""

import pytest
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile
from backend.cognitive_os.memory.semantic.pattern_extractor import PatternExtractor
from backend.cognitive_os.memory.semantic.semantic_memory import SemanticMemory


def test_pattern_extractor_from_episodes():
    extractor = PatternExtractor()

    # Generate 10 synthetic episodes with consistent player habits: Left dodge, Shotgun, 15 reloads
    episodes = []
    for i in range(1, 11):
        ep = Episode(
            episode_id=f"episode_000{i}",
            timestamp=1000.0 + i * 100,
            duration=80.0,
            winner="Player",
            player_profile=PlayerProfile(
                player_id="raja",
                combat_style="Aggressive",
                reload_count=15,
                preferred_dodge="Left",
                most_used_weapon="Shotgun"
            ),
            battle_summary=BattleSummary(
                match_id=f"episode_000{i}",
                duration_seconds=80.0,
                winner="Player",
                reload_count=15,
                most_used_weapon="Shotgun",
                average_distance=6.0,
                preferred_dodge="Left",
                aggression_score=0.85
            )
        )
        episodes.append(ep)

    knowledge_items = extractor.extract_knowledge_from_episodes(episodes)
    assert len(knowledge_items) >= 4

    types = [k.type for k in knowledge_items]
    assert "PreferredDodge" in types
    assert "PlayerReloadHabit" in types
    assert "PreferredWeapon" in types
    assert "EngagementRange" in types

    dodge_k = next(k for k in knowledge_items if k.type == "PreferredDodge")
    assert dodge_k.confidence > 0.85
    assert "Left" in dodge_k.description


def test_semantic_memory_store():
    sem_mem = SemanticMemory()
    extractor = PatternExtractor()

    episodes = [
        Episode(
            episode_id="ep_1",
            timestamp=1000.0,
            player_profile=PlayerProfile(player_id="raja", preferred_dodge="Left", most_used_weapon="Shotgun")
        )
    ]

    knowledge_items = extractor.extract_knowledge_from_episodes(episodes)
    for k in knowledge_items:
        sem_mem.upsert_knowledge(k)

    assert sem_mem.count() >= 3
    high_conf = sem_mem.get_high_confidence_knowledge(min_confidence=0.5)
    assert len(high_conf) == sem_mem.count()
