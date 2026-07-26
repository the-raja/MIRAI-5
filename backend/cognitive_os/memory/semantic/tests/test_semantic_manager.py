"""Unit tests for SemanticManager operations."""

import pytest
from backend.cognitive_os.memory.semantic.knowledge import Knowledge
from backend.cognitive_os.memory.semantic.semantic_manager import SemanticManager
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.episodic.battle_summary import BattleSummary, PlayerProfile


def test_semantic_manager_extract_merge_and_confidence():
    manager = SemanticManager()

    episodes = [
        Episode(
            episode_id="ep_1",
            timestamp=1000.0,
            player_profile=PlayerProfile(player_id="raja", preferred_dodge="Left", reload_count=15)
        )
    ]

    extracted = manager.extract_and_merge_from_episodes(episodes)
    assert len(extracted) >= 3

    # Search knowledge
    dodge_k = manager.search_knowledge("Dodge")
    assert len(dodge_k) >= 1
    k_id = dodge_k[0].id
    initial_conf = dodge_k[0].confidence

    # Increase confidence
    updated_inc = manager.increase_confidence(k_id, delta=0.05)
    assert updated_inc is not None
    assert updated_inc.confidence == round(initial_conf + 0.05, 2)

    # Decrease confidence
    updated_dec = manager.decrease_confidence(k_id, delta=0.05)
    assert updated_dec is not None
    assert updated_dec.confidence == initial_conf

    # Delete knowledge
    deleted = manager.delete_knowledge(k_id)
    assert deleted is True
    assert len(manager.search_knowledge("Dodge")) == 0
