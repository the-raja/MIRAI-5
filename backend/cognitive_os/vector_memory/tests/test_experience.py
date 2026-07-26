"""Unit tests for Experience schema model."""

import pytest
from backend.cognitive_os.vector_memory.experience import Experience


def test_experience_schema_initialization():
    exp = Experience(
        experience_id="exp_001",
        episode_id="ep_001",
        player_profile={"style": "Aggressive", "preferred_weapon": "Shotgun"},
        boss_profile={"phase": 2},
        feature_vector=[0.5, 0.8, 0.2, 0.9, 0.4],
        outcome="DEFEAT",
        duration=45.5,
        tags=["high_aggression", "low_hp_clutch"]
    )

    assert exp.experience_id == "exp_001"
    assert exp.episode_id == "ep_001"
    assert len(exp.feature_vector) == 5
    assert exp.outcome == "DEFEAT"
    assert "high_aggression" in exp.tags
