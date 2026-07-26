"""Unit tests for CheckpointManager save, load, and restore functionality."""

import pytest
import os
import shutil
from backend.cognitive_os.learning.checkpoint import CheckpointManager, CheckpointState


@pytest.fixture
def temp_checkpoint_dir(tmp_path):
    chk_dir = str(tmp_path / "checkpoints")
    yield chk_dir
    if os.path.exists(chk_dir):
        shutil.rmtree(chk_dir, ignore_errors=True)


def test_checkpoint_save_and_restore(temp_checkpoint_dir):
    mgr = CheckpointManager(checkpoint_dir=temp_checkpoint_dir)

    state = CheckpointState(
        checkpoint_id="chk_test_01",
        timestamp=1000.0,
        version="v1.0.1",
        knowledge_items=[{"type": "PlayerReloadHabit", "confidence": 0.94}],
        statistics={"total_episodes_analyzed": 10},
        parameters={"reload_threshold": 3},
        utility_weights={"HeavyAttack": 60.0},
        prediction_metrics={"accuracy": 0.82}
    )

    filepath = mgr.save_checkpoint_state(state)
    assert os.path.exists(filepath)

    loaded = mgr.load_checkpoint_state("chk_test_01")
    assert loaded is not None
    assert loaded.version == "v1.0.1"
    assert loaded.utility_weights["HeavyAttack"] == 60.0
    assert loaded.prediction_metrics["accuracy"] == 0.82
