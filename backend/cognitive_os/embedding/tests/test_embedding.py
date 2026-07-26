"""Unit tests for CombatSummaryEncoder."""

import pytest
from backend.cognitive_os.embedding.encoder import CombatSummaryEncoder


def test_combat_summary_encoder_dense_vector():
    encoder = CombatSummaryEncoder(vector_dim=16)
    vec1 = encoder.encode_combat_summary("Player fought aggressively with Shotgun and reloaded below 30% HP.")
    vec2 = encoder.encode_combat_summary("Player fought defensively with Bow and disengaged.")

    assert len(vec1) == 16
    assert len(vec2) == 16
    assert vec1 != vec2
