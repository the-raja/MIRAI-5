"""Unit tests for TemporalSequenceDatasetBuilder sliding window dataset creation."""

import pytest
from backend.cognitive_os.temporal.sequence_dataset import TemporalSequenceDatasetBuilder


def test_sequence_dataset_sample_creation():
    builder = TemporalSequenceDatasetBuilder(window_size=4)
    actions = ["Attack", "Attack", "Reload", "Heal", "DodgeRight", "Attack"]

    samples = builder.build_sequence_samples(actions)

    assert len(samples) == 2
    assert samples[0]["sequence_input"] == ["Attack", "Attack", "Reload", "Heal"]
    assert samples[0]["target_next_action"] == "DodgeRight"

    assert samples[1]["sequence_input"] == ["Attack", "Reload", "Heal", "DodgeRight"]
    assert samples[1]["target_next_action"] == "Attack"
