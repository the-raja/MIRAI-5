"""Unit tests for SequenceBuffer rolling 20-action history."""

import pytest
from backend.cognitive_os.temporal.sequence_buffer import SequenceBuffer


def test_sequence_buffer_push_and_limit():
    buf = SequenceBuffer(max_length=20)
    for i in range(25):
        buf.push_action(f"Action_{i}")

    assert buf.size() == 20
    seq = buf.get_sequence()
    assert len(seq) == 20
    assert seq[0] == "Action_5"
    assert seq[-1] == "Action_24"


def test_sequence_buffer_sliding_windows():
    buf = SequenceBuffer(max_length=20)
    actions = ["Attack", "Attack", "Block", "DodgeLeft", "Reload"]
    for act in actions:
        buf.push_action(act)

    windows = buf.get_sliding_windows(window_size=3)
    assert len(windows) == 3
    assert windows[0] == ["Attack", "Attack", "Block"]
    assert windows[-1] == ["Block", "DodgeLeft", "Reload"]
