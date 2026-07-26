"""Unit tests for LSTMTemporalModel sequence prediction."""

import pytest
from backend.cognitive_os.temporal.temporal_model import LSTMTemporalModel


def test_lstm_sequence_prediction():
    model = LSTMTemporalModel()

    # Test sequence: Attack -> Attack -> DodgeLeft -> Attack -> Reload -> Next: DodgeRight (87% conf)
    sequence = ["Attack", "Attack", "DodgeLeft", "Attack", "Reload"]
    pred = model.predict_sequence(sequence)

    assert pred.action in ["DodgeRight", "Right Dodge"]
    assert pred.confidence == 0.87
    assert pred.source == "LSTM Temporal Model"
    assert "Observed in" in pred.reason
