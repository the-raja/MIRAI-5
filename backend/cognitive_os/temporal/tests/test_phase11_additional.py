"""Additional unit tests for Phase 11 Temporal Intelligence."""

import pytest
from backend.cognitive_os.temporal.sequence_buffer import SequenceBuffer
from backend.cognitive_os.temporal.temporal_model import LSTMTemporalModel
from backend.cognitive_os.temporal.sequence_dataset import TemporalSequenceDatasetBuilder


def test_sequence_buffer_clear_and_dict():
    buf = SequenceBuffer(max_length=5)
    buf.push_action("Attack")
    buf.push_action("Block")
    d = buf.to_dict()

    assert d["current_size"] == 2
    assert d["sequence"] == ["Attack", "Block"]

    buf.clear()
    assert buf.size() == 0


def test_lstm_model_train_empty():
    model = LSTMTemporalModel()
    res = model.train([])
    assert res["status"] == "FAILED"


def test_lstm_model_metadata():
    model = LSTMTemporalModel()
    meta = model.metadata()
    assert meta["architecture"] == "LSTM Recurrent Neural Network"
    assert meta["hidden_dim"] == 64


def test_temporal_dataset_builder_empty():
    builder = TemporalSequenceDatasetBuilder()
    samples = builder.build_sequence_samples([])
    assert samples == []
