"""More unit tests for Phase 11 Temporal Intelligence."""

import pytest
import os
from backend.cognitive_os.temporal.temporal_model import LSTMTemporalModel
from backend.cognitive_os.temporal.inference import SequencePrediction


def test_lstm_model_save_and_load_instance(tmp_path):
    filepath = str(tmp_path / "lstm_model.json")
    model = LSTMTemporalModel("v3.0.0", hidden_dim=128)

    model.save(filepath)
    assert os.path.exists(filepath)

    model2 = LSTMTemporalModel()
    assert model2.load(filepath) is True
    assert model2.version() == "v3.0.0"
    assert model2.hidden_dim == 128


def test_sequence_prediction_metadata_dict():
    pred = SequencePrediction(
        prediction_id="p_seq_1",
        timestamp=100.0,
        action="DodgeRight",
        confidence=0.87,
        sequence_length=5,
        top_alternatives=[("DodgeRight", 0.87), ("Attack", 0.10)]
    )

    assert pred.sequence_length == 5
    assert pred.top_alternatives[0][0] == "DodgeRight"
    assert pred.metadata["sequence_length"] == 5
